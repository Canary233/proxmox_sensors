"""Pure, static dashboard plan using native card configurations only."""

from .selection import representable_entities


def generate_dashboard(inventory, *, include_controls=False):
    """Return a JSON-compatible plan, not a registered Lovelace dashboard.

    IDs/resource metadata describe the plan; Phase 2 can adapt it to a Lovelace
    view schema. State changes do not change the generated layout.
    """
    views = []
    for entry in sorted(inventory["entries"], key=lambda e: e["entry_id"]):
        sections = []
        for resource in sorted(inventory["resources"], key=lambda r: r["resource_id"]):
            if resource["entry_id"] != entry["entry_id"]:
                continue
            entities = sorted(representable_entities(resource, include_controls=include_controls),
                              key=lambda e: e["entity_id"])
            if not entities:
                continue
            card_rows = []
            for entity in entities:
                card_rows.append({"entity": entity["entity_id"]})
                card_rows.extend({"type": "attribute", "entity": entity["entity_id"], "attribute": attr}
                                 for attr in entity["attributes"])
            sections.append({"resource_id": resource["resource_id"], "kind": resource["kind"],
                             "title": resource["title"], "entities": [e["entity_id"] for e in entities],
                             "cards": [{"type": "entities", "title": resource["title"],
                                        "show_header_toggle": False, "entities": card_rows}]})
        if sections:
            views.append({"id": entry["entry_id"], "title": entry["title"],
                          "platform_type": entry["platform_type"], "sections": sections})
    return {"schema_version": 1, "title": "Proxmox Extended Sensors", "views": views}
