"""SERVICES for Proxmox Extended Sensors."""

import logging
import asyncio
import time
from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _run_vzdump_task(client, hass, node, vmid, storage, mode, compress):
    """Start a backup and report success only after its UPID reaches a terminal OK state."""
    accepted = await client.start_vzdump(
        hass, node=node, vmid=vmid, storage=storage, mode=mode,
        compress=compress, notes="HA-{{vmid}}, {{guestname}}",
    )
    if not isinstance(accepted, str) or not accepted.strip():
        return vmid, False, {"accepted": accepted, "error": "Invalid task UPID"}
    waiter = getattr(client, "wait_for_task", None)
    if waiter is None:
        return vmid, False, {"upid": accepted, "error": "Task status API unavailable"}
    try:
        task = await waiter(hass, accepted)
    except Exception as err:
        return vmid, False, {"upid": accepted, "error": str(err)}
    if not isinstance(task, dict):
        return vmid, False, {"upid": accepted, "error": "Invalid task result"}
    return vmid, task.get("status") == "OK", {"upid": accepted, "task": task}


def _backup_scheduler(max_concurrent, delay_between):
    """Coordinate active remote tasks and minimum intervals between their starts."""
    condition = asyncio.Condition()
    active = 0
    last_start = None

    async def acquire():
        nonlocal active, last_start
        async with condition:
            while True:
                while active >= max_concurrent:
                    await condition.wait()
                if last_start is not None:
                    remaining = delay_between - (time.monotonic() - last_start)
                    if remaining > 0:
                        try:
                            await asyncio.wait_for(condition.wait(), remaining)
                        except asyncio.TimeoutError:
                            pass
                        continue
                active += 1
                last_start = time.monotonic()
                return

    async def release():
        nonlocal active
        async with condition:
            active -= 1
            condition.notify_all()

    return acquire, release


def _resolve_pve_target(hass, data, *, allow_auto=False):
    """Resolve configured ownership, never cluster visibility or load order."""
    node = data.get("node")
    if not node and not allow_auto:
        raise ValueError("Node is required")
    entry_id = data.get("entry_id")
    candidates = []
    for candidate in hass.config_entries.async_entries(DOMAIN):
        if candidate.data.get("platform_type") != "PVE":
            continue
        if entry_id is not None and candidate.entry_id != entry_id:
            continue
        configured_node = candidate.data.get("node")
        if not configured_node or (node and configured_node != node):
            continue
        # Count configured owners before testing runtime availability: an offline
        # duplicate must not silently redirect a call to a different installation.
        candidates.append(candidate)
    if not candidates:
        raise ValueError("No PVE entry owns the requested node/entry_id")
    if len(candidates) != 1:
        raise ValueError("Ambiguous PVE destination; specify node and entry_id")
    selected = candidates[0]
    runtime = hass.data.get(DOMAIN, {}).get(selected.entry_id, {})
    if (not runtime.get("services_ready") or runtime.get("unloading")
            or not runtime.get("client") or not runtime.get("coordinator")):
        raise ValueError("The selected PVE entry is not loaded")
    return selected, runtime, selected.data["node"]


def register_services(hass: HomeAssistant, entry=None):
    """Keep domain services registered; resolve live entry state on every call."""
    if hass.services.has_service(DOMAIN, "create_vzdump_backup"):
        return

    # ====== SIMPLE / MULTI BACKUP SERVICE ==========
    async def handle_create_vzdump_backup(call: ServiceCall):
        selected, entry_data, node = _resolve_pve_target(hass, call.data)
        guests = call.data.get("guests") or call.data.get("vmid")
        storage = call.data.get("storage")
        mode = call.data.get("mode", "snapshot")
        compress = call.data.get("compress", "zstd")

        max_concurrent = int(call.data.get("max_concurrent", 1))
        delay_between = float(call.data.get("delay_between", 0))
        if max_concurrent < 1 or delay_between < 0:
            raise ValueError("max_concurrent must be at least 1 and delay_between cannot be negative")

        if not node:
            raise ValueError("Node is required")

        if not guests:
            raise ValueError("Guests list is required")

        if not storage:
            raise ValueError("Storage is required")

        storage = str(storage).strip().replace("\n", "").replace("\r", "")

        if isinstance(guests, str):
            guests = [g.strip() for g in guests.split(",") if g.strip()]
        elif isinstance(guests, int):
            guests = [guests]
        elif not isinstance(guests, list):
            raise ValueError("Guests must be int, list or comma-separated string")

        targets = [int(g) for g in guests]

        _LOGGER.info(
            f"Backup requested for guests {targets} on node {node} "
            f"with mode={mode}, compress={compress}"
        )

        success_count = 0
        error_count = 0
        detailed_results = []

        acquire, release = _backup_scheduler(max_concurrent, delay_between)
        async def backup_one(vmid):
            await acquire()
            try:
                _LOGGER.info(f"Starting backup of {vmid}...")
                _, current, _ = _resolve_pve_target(hass, call.data)
                if current is not entry_data:
                    raise ValueError("PVE entry changed during backup request; retry the service")
                _, success, result = await _run_vzdump_task(
                    current["client"], hass, node, vmid, storage, mode, compress
                )
                if not success:
                    _LOGGER.error(f"Backup of {vmid} did not complete successfully: {result}")
                return vmid, success, result
            except Exception as e:
                _LOGGER.error(f"Error in backup of {vmid}: {e}")
                return vmid, False, str(e)
            finally:
                await release()

        results = await asyncio.gather(*(backup_one(vmid) for vmid in targets))
        for vmid, success, result in results:
            if success:
                success_count += 1
            else:
                error_count += 1
            detailed_results.append({"vmid": vmid, "success": success, "detail": result})

        _LOGGER.info(
            f"Simple/Multi backup completed. "
            f"Success: {success_count} | Failures: {error_count} | Total: {len(targets)}"
        )
        return detailed_results

    hass.services.async_register(
        DOMAIN, "create_vzdump_backup", handle_create_vzdump_backup
    )

    # =======MASSIVE BACKUP=========

    async def handle_backup_all(call: ServiceCall):
        selected, entry_data, node = _resolve_pve_target(hass, call.data)
        storage = call.data.get("storage")
        mode = call.data.get("mode", "snapshot")
        compress = call.data.get("compress", "zstd")
        max_concurrent = int(call.data.get("max_concurrent", 1))
        delay_between = float(call.data.get("delay_between", 30))
        if max_concurrent < 1 or delay_between < 0:
            raise ValueError("max_concurrent must be at least 1 and delay_between cannot be negative")

        if not node:
            raise ValueError("Node is required")

        if not storage:
            raise ValueError("Storage is required")

        storage = str(storage).strip().replace("\n", "").replace("\r", "")

        # Validate mode values
        valid_modes = ["snapshot", "suspend", "stop"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode. Must be one of: {', '.join(valid_modes)}")

        valid_compress = ["zstd", "gzip", "lzo", "none", "0", "1"]
        if compress not in valid_compress:
            raise ValueError(
                f"Invalid compress. Must be one of: {', '.join(valid_compress)}"
            )

        if compress == "none":
            compress = "0"

        include_vms = call.data.get("include_vms", False)
        include_cts = call.data.get("include_cts", False)

        if not include_vms and not include_cts:
            _LOGGER.warning("Massive backup requested without selecting VMs or CTs")
            return

        coordinator = entry_data["coordinator"]
        data = coordinator.data

        vm_list = []
        ct_list = []

        # VMs
        if include_vms and "vms" in data:
            for vm_data in data["vms"].values():
                if not isinstance(vm_data, dict):
                    continue
                if vm_data.get("node") != node:
                    continue
                vmid = vm_data.get("vmid")
                if vmid is not None:
                    vm_list.append(str(vmid))

        # CTs
        if include_cts and "cts" in data:
            for ct_data in data["cts"].values():
                if not isinstance(ct_data, dict):
                    continue
                if ct_data.get("node") != node:
                    continue
                ctid = ct_data.get("vmid")
                if ctid is not None:
                    ct_list.append(str(ctid))

        targets = vm_list + ct_list

        if not targets:
            _LOGGER.warning(f"No machines found for backup on node {node}")
            return

        _LOGGER.info(
            f"Massive backup started on node {node}. "
            f"VMs: {len(vm_list)} | CTs: {len(ct_list)} | "
            f"Mode: {mode} | Compress: {compress} | "
            f"Concurrent: {max_concurrent} | Delay: {delay_between}s"
        )

        acquire, release = _backup_scheduler(max_concurrent, delay_between)
        results = []

        async def backup_with_limit(vmid):
            await acquire()
            try:
                _LOGGER.info(f"Starting backup of {vmid}...")
                _, current, _ = _resolve_pve_target(hass, call.data)
                if current is not entry_data:
                    raise ValueError("PVE entry changed during backup request; retry the service")
                return await _run_vzdump_task(
                    current["client"], hass, node, vmid, storage, mode, compress
                )
            except Exception as e:
                _LOGGER.error(f"Error in backup of {vmid}: {e}")
                return (vmid, False, str(e))
            finally:
                await release()

        tasks = [backup_with_limit(vmid) for vmid in targets]
        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        success_count = 0
        error_count = 0
        detailed_results = []

        for result in results:
            if isinstance(result, tuple) and len(result) == 3:
                vmid, success, detail = result
                if success:
                    success_count += 1
                else:
                    error_count += 1
                detailed_results.append(
                    {"vmid": vmid, "success": success, "detail": detail}
                )
            else:
                error_count += 1
                detailed_results.append(
                    {
                        "vmid": "unknown",
                        "success": False,
                        "detail": str(result) if result else "Unknown error",
                    }
                )

        _LOGGER.info(
            f"Massive backup completed. "
            f"Success: {success_count} | Failures: {error_count} | Total: {len(targets)}"
        )

        if error_count > 0:
            notification_id = f"proxmox_backup_summary_{node}"
            message = (
                f"📊 **Massive Backup Summary - Node: {node}**\n\n"
                f"✅ Success: {success_count}\n"
                f"❌ Failures: {error_count}\n"
                f"📦 Total: {len(targets)}\n\n"
                f"💾 Storage: {storage}\n"
                f"⚙️ Mode: {mode}\n"
                f"🗜️ Compression: {compress}"
            )

            persistent_notification.create(
                hass, message, "Proxmox Backup Summary", notification_id
            )

        return detailed_results

    hass.services.async_register(DOMAIN, "backup_all", handle_backup_all)

    # ========SHUTDOWN NODE===========

    async def handle_confirm_shutdown(call: ServiceCall):
        selected, entry_data, node = _resolve_pve_target(hass, call.data)
        confirm = call.data.get("confirm", False)

        if not confirm:
            notification_id = f"proxmox_shutdown_confirm_{selected.entry_id}_{node}"
            message = (
                f"⚠️ **Shutdown node {node}**\n\n"
                f"To confirm, run this service again with `confirm: true`, "
                f"`node: {node}` and `entry_id: {selected.entry_id}`."
            )

            persistent_notification.create(
                hass, message, "Confirm Proxmox Shutdown", notification_id
            )
            return

        try:
            result = await entry_data["client"].shutdown_node(hass, node)
            if result:
                persistent_notification.dismiss(
                    hass, f"proxmox_shutdown_confirm_{selected.entry_id}_{node}"
                )
        except Exception as e:
            _LOGGER.error(f"Error shutting down node {node}: {e}")

    hass.services.async_register(
        DOMAIN, "confirm_shutdown_node", handle_confirm_shutdown
    )

    # =======REBOOT NODE==========

    async def handle_confirm_reboot(call: ServiceCall):
        selected, entry_data, node = _resolve_pve_target(hass, call.data)
        confirm = call.data.get("confirm", False)

        if not confirm:
            notification_id = f"proxmox_reboot_confirm_{selected.entry_id}_{node}"
            message = (
                f"🔄 **Reboot node {node}**\n\n"
                f"To confirm, run this service again with `confirm: true`, "
                f"`node: {node}` and `entry_id: {selected.entry_id}`."
            )

            persistent_notification.create(
                hass, message, "Confirm Proxmox Reboot", notification_id
            )
            return

        try:
            result = await entry_data["client"].reboot_node(hass, node)
            if result:
                persistent_notification.dismiss(hass, f"proxmox_reboot_confirm_{selected.entry_id}_{node}")
        except Exception as e:
            _LOGGER.error(f"Error rebooting node {node}: {e}")

    hass.services.async_register(DOMAIN, "confirm_reboot_node", handle_confirm_reboot)

    # ======= WAKE NODE (WOL) ==========

    async def handle_wake_node(call: ServiceCall):
        selected, entry_data, node = _resolve_pve_target(hass, call.data, allow_auto=True)
        mac = (call.data["mac"] if "mac" in call.data else
               selected.options.get("wol_macs", {}).get(node))

        # -------- MAC VALIDATION --------
        if not mac:
            raise ValueError("MAC address is required for WOL")

        mac_clean = mac.replace(":", "").replace("-", "")
        if len(mac_clean) != 12:
            raise ValueError(f"Invalid MAC address format: {mac}")

        try:
            _LOGGER.info(f"Sending WOL packet to node {node} ({mac})")

            await hass.services.async_call(
                "wake_on_lan",
                "send_magic_packet",
                {"mac": mac},
                blocking=True,
            )

            _LOGGER.info(f"WOL packet sent to {node}")

        except Exception as e:
            _LOGGER.error(f"Error sending WOL to node {node}: {e}")

    hass.services.async_register(DOMAIN, "wake_node", handle_wake_node)
