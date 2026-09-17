"""Utilities for stable guest keys across cluster nodes"""

from __future__ import annotations

from .. import const


def make_guest_key(node, vmid):

    return f"{str(node).lower()}:{str(vmid)}"


def make_cluster_guest_key(cluster_id, vmid):

    return f"cluster_{str(cluster_id).lower()}_{str(vmid)}"


def matches_selected_guest(selected_values, node, vmid, guest_key=None):

    if selected_values is None:
        return True

    if not selected_values:
        return False

    normalized = {str(value) for value in selected_values}
    vmid_str = str(vmid)
    canonical_key = make_guest_key(node, vmid)
    explicit_key = str(guest_key) if guest_key is not None else canonical_key
    raw_node_key = f"{node}:{vmid_str}"

    return any(
        candidate in normalized
        for candidate in (vmid_str, explicit_key, canonical_key, raw_node_key)
    )


def resolve_cluster_id(hass, c_data: dict) -> str | None:

    cluster_id = c_data.get("cluster_id")
    if not cluster_id:
        return None

    has_cluster_entry = any(
        e.data.get(const.CONF_PLATFORM_TYPE) == "CLUSTER"
        and e.data.get("cluster_name") == cluster_id
        for e in hass.config_entries.async_entries(const.DOMAIN)
    )
    return cluster_id if has_cluster_entry else None


def find_guest_node_in_resources(cluster_resources, kind: str, vmid) -> str | None:
    """Return the node currently hosting ``vmid`` per ``/cluster/resources``.

    ``kind`` is ``"vm"`` or ``"ct"`` (mapped to Proxmox's own ``qemu``/``lxc``
    resource types). Returns ``None`` if the guest isn't listed at all in the
    given cluster_resources snapshot.
    """
    proxmox_type = "qemu" if kind == "vm" else "lxc"
    vmid_str = str(vmid)
    for resource in cluster_resources or []:
        if not isinstance(resource, dict):
            continue
        if resource.get("type") != proxmox_type:
            continue
        if str(resource.get("vmid")) == vmid_str:
            return resource.get("node")
    return None
