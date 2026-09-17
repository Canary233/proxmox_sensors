"""LAST ACTION for Proxmox Extended Sensors."""

import logging
import time
from ..const import DOMAIN
from ..pbs_devices import pbs_device_identifier, pbs_parent_device
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback

_logger = logging.getLogger(__name__)


class PBSLastActionSensor(CoordinatorEntity, SensorEntity):

    _attr_has_entity_name = True

    def __init__(self, coordinator, server_id, datastore):
        super().__init__(coordinator)

        self._server_id = server_id.lower()
        self._datastore = datastore

        self._attr_translation_key = "last_action"
        self._attr_unique_id = f"pbs_{self._server_id}_{datastore.lower()}_last_action"
        self._attr_should_poll = False

        self._state = STATE_UNKNOWN
        self._attr_extra_state_attributes = {}
        self._completed_tasks = {}

        self._attr_device_info = {
            "identifiers": {(DOMAIN, pbs_device_identifier("maintenance", self._server_id, datastore))},
            "via_device_id": pbs_parent_device(self.coordinator),
            "name": f"Maintenance: {datastore}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
        }

    @property
    def state(self):
        return self._state

    def _map_task_type(self, task_type: str) -> str:
        task_type = (task_type or "").lower()

        mapping = {
            "garbage_collection": "GC",
            "prune": "Prune",
            "verify": "Verify",
            "sync": "Sync",
        }

        return mapping.get(task_type, task_type.capitalize())

    @callback
    def _handle_coordinator_update(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])

        actions = self.hass.data.get(DOMAIN, {}).get(
            self.coordinator.config_entry.entry_id, {}
        ).get("pbs_action_upids", {}).get(self._server_id, {}).get(self._datastore, {})
        actions = {
            action: upid for action, upid in actions.items()
            if action in ("gc", "prune", "verify", "sync")
            and isinstance(upid, str) and upid.startswith("UPID:")
        }
        # Correlate all accepted actions only by exact UPID, within this PBS.
        by_upid = {task.get("upid"): task for task in tasks
                   if isinstance(task, dict) and isinstance(task.get("upid"), str)}
        self._completed_tasks = {
            upid: task for upid, task in self._completed_tasks.items()
            if upid in actions.values()
        }
        for upid in actions.values():
            task = by_upid.get(upid)
            if task and task.get("endtime") is not None and task.get("status"):
                self._completed_tasks[upid] = dict(task)

        if actions:
            action = next(reversed(actions))
            upid = actions[action]
            task = self._completed_tasks.get(upid) or by_upid.get(upid)
            label = "GC" if action == "gc" else action.title()
            attrs = {"upid": upid}
            outcome = "Iniciado"
            if task is not None:
                attrs.update({key: task[key] for key in (
                    "status", "starttime", "endtime", "duration", "error",
                    "message", "exitstatus",
                ) if task.get(key) is not None})
                end = task.get("endtime")
                status = task.get("status")
                if end is None:
                    outcome = "Running"
                elif status == "OK":
                    outcome = "OK"
                elif status:
                    outcome = "Error"
                    attrs.setdefault("error", status)
                start = task.get("starttime")
                if "duration" not in attrs and isinstance(start, (int, float)):
                    finish = end if end is not None else time.time()
                    if isinstance(finish, (int, float)) and finish >= start:
                        attrs["duration"] = finish - start
            self._state = f"{label} {outcome}"
            self._attr_extra_state_attributes = attrs
            self.async_write_ha_state()
            return

        tasks = [
            t
            for t in tasks
            if (
                t.get("datastore") == self._datastore
                or (t.get("worker_id") or "").startswith(self._datastore)
            )
        ]

        if not tasks:
            self._state = "Idle"
            self.async_write_ha_state()
            return

        latest_task = max(tasks, key=lambda t: t.get("starttime", 0))

        raw_type = (
            latest_task.get("type") or latest_task.get("worker_type") or "unknown"
        )

        self._state = self._map_task_type(raw_type)

        self._attr_extra_state_attributes = {
            "raw_type": raw_type,
            "status": latest_task.get("status"),
            "starttime": latest_task.get("starttime"),
        }

        self.async_write_ha_state()
