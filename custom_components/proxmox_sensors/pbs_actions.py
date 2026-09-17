"""PBS Actions for Proxmox Extended Sensors."""

import logging

_LOGGER = logging.getLogger(__name__)

BASE = "admin/datastore"


async def run_gc(client, hass, datastore: str):
    _LOGGER.info("PBS: Running GC in %s", datastore)
    endpoint = f"{BASE}/{datastore}/gc"
    result = await client.pbs_post(hass, endpoint)
    return result


async def run_prune(client, hass, datastore: str, job_id: str | None = None):
    if not job_id:
        _LOGGER.warning("PBS: No Prune Job configured for datastore %s", datastore)
        return None

    _LOGGER.info("PBS: Running configured PRUNE job %s for %s", job_id, datastore)
    return await client.pbs_post(hass, f"admin/prune/{job_id}/run", {})


async def run_verify(client, hass, datastore: str, job_id: str | None = None):
    """Run the configured PBS verification job."""

    if not job_id:
        _LOGGER.warning(
            "PBS: No Verify Job configured for datastore %s",
            datastore,
        )
        return None

    _LOGGER.info(
        "PBS: Running configured VERIFY job %s for %s",
        job_id,
        datastore,
    )

    endpoint = f"admin/verify/{job_id}/run"
    result = await client.pbs_post(hass, endpoint, {})
    return result


async def run_sync(client, hass, datastore: str, job_id: str | None = None):
    if not job_id:
        _LOGGER.warning(
            "PBS: No Sync Job configured for datastore %s",
            datastore,
        )
        return None

    _LOGGER.info(
        "PBS: Running configured SYNC job %s for %s",
        job_id,
        datastore,
    )

    endpoint = f"admin/sync/{job_id}/run"
    return await client.pbs_post(hass, endpoint, {})

