"""Persistent PBS identity mapping."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import CONF_PLATFORM_TYPE, DOMAIN

STORAGE_KEY = f"{DOMAIN}.pbs_identity"
STORAGE_VERSION = 1


def _entry_platform_type(entry: ConfigEntry) -> str:
    return (
        entry.data.get(CONF_PLATFORM_TYPE) or entry.data.get("server_type") or ""
    ).upper()


async def async_load_pbs_identity_map(hass: HomeAssistant) -> dict[str, str]:
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    data = await store.async_load() or {}
    identities = data.get("identities", {})
    if not isinstance(identities, dict):
        return {}
    return {
        str(identity): str(server_id)
        for identity, server_id in identities.items()
        if identity and server_id
    }


async def async_save_pbs_identity_map(
    hass: HomeAssistant, identities: dict[str, str]
) -> None:
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    await store.async_save({"identities": identities})


async def async_remember_pbs_identity(
    hass: HomeAssistant, pbs_instance_id: str | None, server_id: str | None
) -> None:
    if not pbs_instance_id or not server_id:
        return

    identities = await async_load_pbs_identity_map(hass)
    if identities.get(pbs_instance_id) == server_id:
        return

    identities[pbs_instance_id] = server_id
    await async_save_pbs_identity_map(hass, identities)


async def async_server_id_for_pbs_identity(
    hass: HomeAssistant, pbs_instance_id: str | None
) -> str | None:
    if not pbs_instance_id:
        return None
    return (await async_load_pbs_identity_map(hass)).get(pbs_instance_id)


async def async_reserved_pbs_server_ids(hass: HomeAssistant) -> set[str]:
    return set((await async_load_pbs_identity_map(hass)).values())


def active_pbs_entry_with_server_id(
    hass: HomeAssistant, server_id: str, exclude_entry_id: str | None = None
) -> ConfigEntry | None:
    for entry in hass.config_entries.async_entries(DOMAIN):
        if exclude_entry_id and entry.entry_id == exclude_entry_id:
            continue
        if _entry_platform_type(entry) != "PBS":
            continue
        if entry.data.get("server_id") == server_id:
            return entry
    return None


def pbs_server_id_available_for_identity(
    hass: HomeAssistant,
    server_id: str,
    pbs_instance_id: str | None,
    exclude_entry_id: str | None = None,
) -> bool:
    entry = active_pbs_entry_with_server_id(hass, server_id, exclude_entry_id)
    if entry is None:
        return True
    return bool(
        pbs_instance_id
        and entry.data.get("pbs_instance_id")
        and entry.data.get("pbs_instance_id") == pbs_instance_id
    )
