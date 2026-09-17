"""PBS-only declarative resource binding, without runtime access or actions."""

import json

from .layout import get_dashboard_layout

# Ordered, exact translation keys declared by sensor/pbs.py and button.py.
_SENSORS = {
    "header": ("pbs_version", "pbs_release"),
    "server_health": ("pbs_auth_status", "pbs_cpu_usage", "pbs_ram_usage",
                      "pbs_ram_total", "pbs_ram_used", "pbs_ram_free"),
    "datastores": ("pbs_datastore_usage", "pbs_datastore_total", "pbs_datastore_used",
                   "pbs_datastore_free", "pbs_dedup"),
    "backups": ("pbs_backups_summary", "pbs_backup_errors", "pbs_last_backup_time",
                "pbs_last_backup_size", "pbs_last_backup_status"),
    "maintenance": ("pbs_gc_status", "pbs_prune_status", "pbs_verify_status"),
    "tasks": ("last_action", "pbs_last_task", "pbs_last_task_type", "pbs_last_task_status",
              "pbs_last_task_duration", "pbs_last_task_message"),
}
_BUTTONS = ("pbs_gc", "pbs_prune", "pbs_verify", "pbs_sync")
_STORE_KEYS = set(_SENSORS["datastores"] + _SENSORS["backups"] + _SENSORS["maintenance"] + ("last_action",))


def build_pbs_dashboard_model(inventory, layout=None):
    """Return references grouped by existing PBS entry/server and resource IDs."""
    layout = get_dashboard_layout("pbs") if layout is None else layout
    if layout["type"] != "pbs":
        raise ValueError("PBS resource mapping requires a PBS layout")
    groups = []
    for entry in sorted(inventory["entries"], key=lambda item: item["entry_id"]):
        if entry["platform_type"] != "PBS" or not entry.get("server_id"):
            continue
        blocks = {block["id"]: {} for block in layout["blocks"]}
        seen = set()
        for resource in sorted(inventory["resources"], key=lambda item: item["resource_id"]):
            if (resource["entry_id"] != entry["entry_id"]
                    or resource.get("server_id") != entry["server_id"]):
                continue
            # Normalized datastore IDs encode [entry, server, "datastore", name].
            # The shared logical title must not inherit either device's label.
            title = (json.loads(resource["resource_id"])[3]
                     if resource["kind"] == "datastore" else resource["title"])
            for entity in sorted(resource["entities"], key=lambda item: item["entity_id"]):
                if entity["config_entry_id"] != entry["entry_id"] or entity["entity_id"] in seen:
                    continue
                key = entity.get("translation_key")
                block = None
                if entity["domain"] == "button" and key in _BUTTONS and resource["kind"] == "datastore":
                    block = "maintenance"
                elif entity["domain"] == "sensor":
                    if key in _STORE_KEYS and resource["kind"] != "datastore":
                        continue
                    if key not in _STORE_KEYS and resource["kind"] == "datastore":
                        continue
                    block = next((name for name, keys in _SENSORS.items() if key in keys), None)
                if block is None:
                    continue
                item = blocks[block].setdefault(resource["resource_id"], {
                    "resource_id": resource["resource_id"], "kind": resource["kind"],
                    "title": title, "references": [],
                })
                ref = {"entity_id": entity["entity_id"], "metric": key.removeprefix("pbs_")}
                if block == "maintenance":
                    ref["operation"] = key.removeprefix("pbs_").removesuffix("_status")
                item["references"].append(ref)
                seen.add(entity["entity_id"])
        result = {}
        for block, resources in blocks.items():
            result[block] = sorted(resources.values(), key=lambda item: (item["title"].casefold(), item["resource_id"]))
            keys = _SENSORS.get(block, ()) + (_BUTTONS if block == "maintenance" else ())
            order = [key.removeprefix("pbs_") for key in keys]
            for resource in result[block]:
                def ref_order(ref):
                    if block == "maintenance":
                        return (("gc", "prune", "verify", "sync").index(ref["operation"]),
                                ref["metric"] == ref["operation"], ref["entity_id"])
                    return (order.index(ref["metric"]), ref["entity_id"])
                resource["references"].sort(key=ref_order)
        if any(result.values()):
            groups.append({"entry_id": entry["entry_id"], "server_id": entry["server_id"], "blocks": result})
    return {"schema_version": 1, "type": "pbs", "groups": groups}
