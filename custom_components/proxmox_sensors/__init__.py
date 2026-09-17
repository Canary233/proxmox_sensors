"""INIT for Proxmox Extended Sensors."""

from __future__ import annotations
import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr

from .services import register_services
from .dashboard.preview import async_register_preview
from .dashboard.websocket import async_register_dashboard_websocket
from .dashboard.frontend import async_setup_dashboard_frontend
from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_USER,
    CONF_PASSWORD,
    CONF_TOKEN_ID,
    CONF_TOKEN_SECRET,
    CONF_NODE,
    CONF_PLATFORM_TYPE,
    CONF_VERIFY_SSL,
)

from .api import ProxmoxClient
from .coordinator import create_proxmox_coordinator, create_cluster_coordinator
from .pbs_identity import async_remember_pbs_identity
from .pbs_devices import reconcile_pbs_devices

_LOGGER = logging.getLogger(__name__)

ENTRY_VERSION = 3

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BUTTON,
    Platform.BINARY_SENSOR,
]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register global diagnostics, including while individual entries are unloaded."""
    async_register_preview(hass)
    async_register_dashboard_websocket(hass)
    try:
        await async_setup_dashboard_frontend(hass)
    except Exception:
        _LOGGER.exception("Could not serve dashboard strategy; integration monitoring remains available")
    return True


def _entry_platform_type(config_entry: ConfigEntry) -> str:
    return (
        config_entry.data.get(CONF_PLATFORM_TYPE)
        or config_entry.data.get("server_type")
        or ""
    ).upper()


def _next_pbs_server_id(hass: HomeAssistant) -> str:
    max_index = 0
    for entry in hass.config_entries.async_entries(DOMAIN):
        if _entry_platform_type(entry) != "PBS":
            continue
        server_id = str(entry.data.get("server_id", "")).lower()
        if not server_id.startswith("pbs_"):
            continue
        suffix = server_id.removeprefix("pbs_")
        if suffix.isdigit():
            max_index = max(max_index, int(suffix))
    return f"pbs_{max_index + 1}"


def _ensure_pbs_server_id(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    if _entry_platform_type(config_entry) != "PBS":
        return False

    if config_entry.data.get("server_id"):
        return False

    ent_reg = er.async_get(hass)
    entries = er.async_entries_for_config_entry(ent_reg, config_entry.entry_id)
    if any(
        (entity.unique_id or "").lower().startswith("pbs_default_")
        for entity in entries
    ):
        server_id = "default"
    else:
        server_id = _next_pbs_server_id(hass)

    hass.config_entries.async_update_entry(
        config_entry, data={**config_entry.data, "server_id": server_id}
    )
    _LOGGER.info(
        "Persisted stable PBS server_id %s for legacy entry %s",
        server_id,
        config_entry.entry_id,
    )
    return True


async def async_migrate_entry(hass, config_entry):
    """Migrate Proxmox entry to prefixed unique_id format."""

    if config_entry.version >= ENTRY_VERSION:
        return True

    _LOGGER.info(
        "Migrating Proxmox entry %s from version %s to %s",
        config_entry.entry_id,
        config_entry.version,
        ENTRY_VERSION,
    )

    ent_reg = er.async_get(hass)
    entries = er.async_entries_for_config_entry(ent_reg, config_entry.entry_id)

    _ensure_pbs_server_id(hass, config_entry)
    server_id = (config_entry.data.get("server_id") or "default").lower()
    server_type = _entry_platform_type(config_entry).lower()

    _LOGGER.debug("Migration server_type raw value: %s", server_type)

    if server_type == "pbs":
        prefix = "pbs"
    elif server_type == "pve":
        prefix = "pve"
    else:
        if any("datastore" in (e.unique_id or "") for e in entries):
            prefix = "pbs"
            _LOGGER.info("Legacy entry detected as PBS")
        else:
            prefix = "pve"
            _LOGGER.info("Legacy entry detected as PVE")

    for entity in entries:
        old_unique_id = entity.unique_id
        if not old_unique_id:
            continue
        if old_unique_id.startswith(f"{prefix}_{server_id}_"):
            continue
        new_unique_id = f"{prefix}_{server_id}_{old_unique_id}".lower()
        ent_reg.async_update_entity(entity.entity_id, new_unique_id=new_unique_id)
        _LOGGER.debug("Updated unique_id: %s -> %s", old_unique_id, new_unique_id)


    if server_type == "pve":
        await _migrate_guest_ids_to_cluster_scope(hass, config_entry)

    hass.config_entries.async_update_entry(config_entry, version=ENTRY_VERSION)
    _LOGGER.info("Migration completed for entry %s", config_entry.entry_id)
    return True


async def _migrate_guest_ids_to_cluster_scope(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Rewrite VM/CT unique_ids from per-node to cluster-scoped format.

    This only runs when a sibling CLUSTER entry is ALREADY configured for
    this same cluster (matching the behaviour of ``_resolve_cluster_id`` in
    sensor/__init__.py), so it never fires for standalone/single-node
    installs. Guests keep their legacy per-node unique_id in that case,
    which is a no-op and requires no migration.

    A CLUSTER entry stores the cluster name in ``cluster_name`` and is
    created automatically by this integration once the cluster is first
    detected, so if it exists, we can read the cluster id directly from it
    without another API call.
    """
    node = (config_entry.data.get(CONF_NODE) or "").lower()
    if not node:
        return

    cluster_entry = next(
        (
            e
            for e in hass.config_entries.async_entries(DOMAIN)
            if e.data.get(CONF_PLATFORM_TYPE) == "CLUSTER"
        ),
        None,
    )
    if cluster_entry is None:
        _LOGGER.debug(
            "No CLUSTER entry configured yet, skipping guest id migration for %s",
            node,
        )
        return

    cluster_id = (cluster_entry.data.get("cluster_name") or "").lower()
    if not cluster_id:
        return

    legacy_vm_prefix = f"pve_{node}_proxmox_vm_{node}_"
    legacy_ct_prefix = f"pve_{node}_proxmox_ct_{node}_"

    ent_reg = er.async_get(hass)
    dev_reg = dr.async_get(hass)
    entries = er.async_entries_for_config_entry(ent_reg, config_entry.entry_id)

    migrated = 0

    for entity in entries:
        old_unique_id = (entity.unique_id or "").lower()

        for kind, legacy_prefix in (("vm", legacy_vm_prefix), ("ct", legacy_ct_prefix)):
            if not old_unique_id.startswith(legacy_prefix):
                continue

            # remainder is "<vmid>_<suffix...>", e.g. "100_status_v1"
            remainder = old_unique_id[len(legacy_prefix):]
            vmid, sep, suffix = remainder.partition("_")
            if not sep or not vmid.isdigit():
                continue

            new_unique_id = (
                f"pve_cluster_{cluster_id}_proxmox_{kind}_{cluster_id}_{vmid}_{suffix}"
            )

            ent_reg.async_update_entity(
                entity.entity_id, new_unique_id=new_unique_id
            )
            migrated += 1
            _LOGGER.info(
                "Migrated guest entity to cluster-scoped id: %s -> %s",
                old_unique_id,
                new_unique_id,
            )

            old_device_identifier = f"proxmox_{kind}_{node}_{vmid}_v1"
            device = dev_reg.async_get_device_by_identifier(
                (DOMAIN, old_device_identifier), config_entry_id=config_entry.entry_id
            )
            if device is not None:
                new_device_identifier = (
                    f"proxmox_{kind}_cluster_{cluster_id}_{vmid}_v1"
                )
                dev_reg.async_update_device(
                    device.id,
                    new_identifiers={(DOMAIN, new_device_identifier)},
                )

            break

    if migrated:
        _LOGGER.info(
            "Cluster-scoped guest id migration: %d entities updated for %s",
            migrated,
            node,
        )


async def _async_manage_cluster_entry(
    hass: HomeAssistant,
    pve_entry: ConfigEntry,
    cluster_name: str,
    enable_cluster: bool,
):
    """Create or remove the CLUSTER config entry based on enable_cluster flag."""

    existing = [
        e
        for e in hass.config_entries.async_entries(DOMAIN)
        if e.data.get(CONF_PLATFORM_TYPE) == "CLUSTER"
        and e.data.get("cluster_name") == cluster_name
    ]

    if not enable_cluster:
        # Remove cluster entry if it exists and was created by this PVE entry
        for e in existing:
            if e.data.get("parent_entry_id") == pve_entry.entry_id:
                _LOGGER.info("Removing CLUSTER entry for %s", cluster_name)
                await hass.config_entries.async_remove(e.entry_id)
        return

    if existing:
        _LOGGER.debug("CLUSTER entry for %s already exists, skipping", cluster_name)
        return

    _LOGGER.info("Auto-creating CLUSTER entry for %s", cluster_name)

    data = pve_entry.data
    cluster_data = {
        CONF_HOST: data[CONF_HOST],
        CONF_USER: data[CONF_USER],
        CONF_PASSWORD: data.get(CONF_PASSWORD),
        CONF_TOKEN_ID: data.get(CONF_TOKEN_ID),
        CONF_TOKEN_SECRET: data.get(CONF_TOKEN_SECRET),
        CONF_VERIFY_SSL: data.get(CONF_VERIFY_SSL, False),
        CONF_PLATFORM_TYPE: "CLUSTER",
        CONF_NODE: data.get(CONF_NODE, ""),
        "cluster_name": cluster_name,
        "parent_entry_id": pve_entry.entry_id,
        "server_id": f"cluster_{cluster_name.lower()}",
    }


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    #  CLUSTER entry (autocreated)
    if entry.data.get(CONF_PLATFORM_TYPE) == "CLUSTER":
        return await _async_setup_cluster_entry(hass, entry)

    #  Normal PVE / PBS entry
    if entry.version < ENTRY_VERSION:
        migrated = await async_migrate_entry(hass, entry)
        if not migrated:
            return False

    _ensure_pbs_server_id(hass, entry)

    data = entry.data

    client = ProxmoxClient(
        host=data[CONF_HOST],
        user=data[CONF_USER],
        password=data.get(CONF_PASSWORD),
        token_id=data.get(CONF_TOKEN_ID),
        token_secret=data.get(CONF_TOKEN_SECRET),
        server_type=data[CONF_PLATFORM_TYPE],
        verify_ssl=data.get(CONF_VERIFY_SSL, False),
    )

    coordinator = await create_proxmox_coordinator(hass, entry, client)

    if entry.data.get(CONF_PLATFORM_TYPE) == "PBS":
        try:
            pbs_instance_id = await client.get_pbs_instance_id(hass)
            hostname = entry.data.get("hostname") or await client.get_pbs_hostname(hass)

            new_data = entry.data
            if (
                pbs_instance_id
                and entry.data.get("pbs_instance_id") != pbs_instance_id
            ):
                new_data = {**new_data, "pbs_instance_id": pbs_instance_id}

            await async_remember_pbs_identity(
                hass, pbs_instance_id, entry.data.get("server_id")
            )

            if hostname:
                new_title = f"PBS: {hostname}"

                if entry.data.get("hostname") != hostname:
                    new_data = {**new_data, "hostname": hostname}

                if entry.title != new_title or new_data is not entry.data:
                    hass.config_entries.async_update_entry(
                        entry,
                        data=new_data,
                        title=new_title,
                    )
            elif new_data is not entry.data:
                hass.config_entries.async_update_entry(entry, data=new_data)

        except Exception as e:
            _LOGGER.error("PBS title update failed: %s", e)
    try:
        async with asyncio.timeout(20):
            await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(
            f"Unable to connect to Proxmox {data[CONF_HOST]}"
        ) from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": data[CONF_NODE],
        "server_type": client._server_type,
        "features": data.get("features", {}),
    }

    if data.get(CONF_PLATFORM_TYPE) == "PBS":
        reconcile_pbs_devices(hass, entry, coordinator.data.get("pbs_datastores", {}))

    register_services(hass, entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    hass.data[DOMAIN][entry.entry_id]["services_ready"] = True

    if data.get(CONF_PLATFORM_TYPE) == "PVE":
        enable_cluster = entry.options.get(
            "enable_cluster", data.get("enable_cluster", True)
        )

        async def _safe_manage_cluster():
            """Create cluster entry without risking the PVE entry setup."""
            try:
                # Small delay to ensure PVE entry is fully registered first
                await asyncio.sleep(2)

                c_data = coordinator.data or {}
                cluster_info = c_data.get("cluster_status", {})
                cluster_name = cluster_info.get("name") if cluster_info else None

                if not cluster_name:
                    return

                await _async_manage_cluster_entry(
                    hass, entry, cluster_name, enable_cluster
                )

            except Exception as err:
                _LOGGER.error(
                    "Error managing CLUSTER entry (PVE entry unaffected): %s", err
                )

        hass.async_create_task(_safe_manage_cluster())

    return True


async def _async_setup_cluster_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a CLUSTER-type config entry."""

    data = entry.data

    client = ProxmoxClient(
        host=data[CONF_HOST],
        user=data[CONF_USER],
        password=data.get(CONF_PASSWORD),
        token_id=data.get(CONF_TOKEN_ID),
        token_secret=data.get(CONF_TOKEN_SECRET),
        server_type="PVE",  # uses PVE API
        verify_ssl=data.get(CONF_VERIFY_SSL, False),
    )

    coordinator = await create_cluster_coordinator(hass, entry, client)

    try:
        async with asyncio.timeout(20):
            await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(
            f"Unable to connect to Proxmox cluster {data[CONF_HOST]}"
        ) from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": data.get(CONF_NODE, ""),
        "server_type": "CLUSTER",
        "features": {},
    }

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if runtime is not None:
        runtime["unloading"] = True

    try:
        if entry.data.get(CONF_PLATFORM_TYPE) == "CLUSTER":
            unload_ok = await hass.config_entries.async_unload_platforms(
                entry, [Platform.SENSOR]
            )
        else:
            unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    finally:
        if runtime is not None:
            runtime.pop("unloading", None)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok
