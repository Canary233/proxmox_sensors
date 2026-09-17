"""CLUSTER-only aggregate references and technically owned Replication jobs."""

import re

from .layout import get_dashboard_layout

_KEYS = {
    "header": ("cluster_status",),
    "cluster_health": ("cluster_cpu_usage", "cluster_ram_usage"),
    "nodes": ("cluster_nodes_online",),
    "guests": ("cluster_vms_running", "cluster_cts_running"),
    "storage": ("cluster_storage_usage",),
    "backup_health": ("cluster_backup_jobs", "cluster_backup_age", "cluster_backup_health"),
    "ha": ("cluster_ha_status",),
    "tasks": ("cluster_failed_tasks",),
    "diagnostics": ("cluster_firewall",),
}


def build_cluster_dashboard_model(inventory, layout=None):
    """Map existing aggregates; no aggregation, guest selection or identity changes."""
    layout = get_dashboard_layout("cluster") if layout is None else layout
    if layout["type"] != "cluster":
        raise ValueError("CLUSTER resource mapping requires a CLUSTER layout")
    groups = []
    for entry in sorted(inventory["entries"], key=lambda item: item["entry_id"]):
        if entry["platform_type"] != "CLUSTER" or not entry.get("cluster_id"):
            continue
        scope = entry["cluster_id"]
        pattern = re.compile(r"pve_cluster_" + re.escape(scope)
                             + r"_replication_(?:(jobs|status)|([0-9]+-.+)_(duration|last_sync|next_sync))")
        blocks = {block["id"]: {} for block in layout["blocks"]}
        seen = set()
        for resource in sorted(inventory["resources"], key=lambda item: item["resource_id"]):
            if resource.get("cluster_id") != scope:
                continue
            for entity in sorted(resource["entities"], key=lambda item: item["entity_id"]):
                if (entity["config_entry_id"] != entry["entry_id"] or entity["domain"] != "sensor"
                        or entity["entity_id"] in seen):
                    continue
                key = entity.get("translation_key")
                match = pattern.fullmatch(entity.get("unique_id") or "") if entity["family"] == "replication" else None
                job_id = None
                if match:
                    block = "replication"
                    metric = match[1] or match[3]
                    job_id = match[2]
                    if job_id is None and resource["entry_id"] != entry["entry_id"]:
                        continue
                else:
                    if resource["entry_id"] != entry["entry_id"] or resource["kind"] in ("vm", "ct"):
                        continue
                    block = next((name for name, keys in _KEYS.items() if key in keys), None)
                    if block is None:
                        continue
                    metric = key.removeprefix("cluster_")
                item = blocks[block].setdefault(resource["resource_id"], {
                    "resource_id": resource["resource_id"], "kind": resource["kind"],
                    "title": resource["title"], "references": [],
                })
                if resource.get("guest_id") is not None:
                    item["guest_id"] = resource["guest_id"]
                ref = {"entity_id": entity["entity_id"], "metric": metric}
                if job_id is not None:
                    ref["job_id"] = job_id
                item["references"].append(ref)
                seen.add(entity["entity_id"])
        result = {}
        for block, resources in blocks.items():
            def resource_order(item):
                if block == "replication":
                    guest = str(item.get("guest_id", ""))
                    return (any("job_id" in ref for ref in item["references"]),
                            int(guest) if guest.isdigit() else -1, item["resource_id"])
                return (item["title"].casefold(), item["resource_id"])
            result[block] = sorted(resources.values(), key=resource_order)
            order = [key.removeprefix("cluster_") for key in _KEYS.get(block, ())]
            for resource in result[block]:
                def ref_order(ref):
                    if block == "replication":
                        guest, _, job = ref.get("job_id", "").partition("-")
                        return ("job_id" in ref, int(guest) if guest.isdigit() else -1,
                                (0, int(job)) if job.isdigit() else (1, job),
                                ("jobs", "status", "duration", "last_sync", "next_sync").index(ref["metric"]), ref["entity_id"])
                    return (order.index(ref["metric"]), ref["entity_id"])
                resource["references"].sort(key=ref_order)
        if any(result.values()):
            groups.append({"entry_id": entry["entry_id"], "cluster_id": scope, "blocks": result})
    return {"schema_version": 1, "type": "cluster", "groups": groups}
