# ❓ FAQ — Proxmox Extended Sensors V5

This page covers common setup and troubleshooting questions for **Proxmox Extended Sensors V5**.

---

## 🔐 Connection problems

### I cannot connect

Check the basics first:

- the Proxmox host is reachable from Home Assistant
- the user and realm are correct
- the token is enabled
- the token secret is correct
- the account has permission to access the required API endpoints
- SSL verification is configured appropriately for your environment

For token setup, see [02. Proxmox User and Permissions](02-proxmox-config.md).

---

### I get `Permission denied`

This usually means the credentials are valid but the account or token cannot access one or more required endpoints.

Check:

- the parent user permissions
- token permissions / Privilege Separation
- permissions assigned at the required path
- whether you are using a deliberately restricted role

V5 distinguishes minimum connectivity from optional endpoint access, so a connection may work while some features remain unavailable because of limited permissions.

---

## 🌡️ Hardware and Sidecar

### Temperatures do not appear

Verify the Proxmox host first:

```bash
sensors
```

Then check the sidecar:

```bash
systemctl status pve-sensors.service
```

And test:

```text
http://YOUR_PROXMOX_IP:9000/sensors
```

See [01. Hardware Sensors and Sidecar Setup](01-install-sensors.md).

---

### What does `Sidecar Status` mean?

V5 exposes one Sidecar Status diagnostic sensor per PVE node.

It summarizes the state of the sidecar sections used for Memory, Mounts, Sensors and SMART. Typical states are `ok`, `degraded`, `error` and `unknown`.

A sidecar failure does not necessarily clear every hardware sensor immediately. V5 preserves the last valid hardware values where possible until fresh data is available again.

---

### Some SMART or temperature sensors are missing

The integration can only expose values available from the host hardware, kernel drivers, `lm-sensors`, SMART tools and the sidecar. Missing values can be normal when a controller does not expose SMART data, a sensor driver is unavailable, the device does not report the metric or the hardware is virtualized.

---

## 🖥️ VMs and LXC containers

### What happens when a VM or CT migrates to another node?

V5 uses cluster-scoped guest identity. The goal is that the same Home Assistant entities continue following the VM/LXC after migration, preserving `unique_id`, `entity_id`, history, statistics, automations and dashboards.

Immediately after a migration, the old node device can remain temporarily empty while reconciliation completes. This is expected and avoids deleting/recreating guest entities.

---

### Why is there no VM disk percentage sensor?

V5 intentionally does not expose VM disk percentage because the available Proxmox data does not provide a sufficiently reliable source metric for it. CT disk percentage is available when the required data exists.

---

## 🔁 PVE Replication

### Where does replication information appear?

V5 exposes cluster-level replication status plus per-job entities associated with the guest, including Duration, Last Replication and Next Replication. Replication job identity is based on the Proxmox replication job rather than the physical node, so it can survive guest migration.

### Does an API error automatically mean the replication failed?

No. V5 keeps replication inventory and runtime information separate. A temporary API/runtime query failure is not automatically treated as a real replication job failure.

---

## 🗄️ Proxmox Backup Server

### Which PBS maintenance actions are supported?

V5 supports Garbage Collection (GC), Prune, Verify and Sync.

> **V5 safety change:** unlike V4.x, **Prune, Verify and Sync are no longer executed as direct maintenance operations built by the integration**. V5 runs the corresponding **PBS Job already configured by the administrator**. This keeps the operation under PBS policy and is especially important for Prune, where the configured retention rules must determine which backups are eligible for removal.

**GC is intentionally kept as a direct datastore action.** Garbage Collection reclaims unreferenced space and is useful for Home Assistant automations, for example when backup storage is running low.

Home Assistant-triggered actions are tracked using the PBS task UPID so the integration can follow the actual task result.

### Why does Prune, Verify or Sync return an error?

Each of these actions requires its corresponding Job to exist in PBS. Before using the Home Assistant action, configure the appropriate **Prune Job, Verify Job or Sync Job** in Proxmox Backup Server.

If no compatible Job exists, **the integration returns an error and does not fall back to a direct operation**. This is intentional safety behavior, not a malfunction.

### Why is Sync unavailable?

Sync requires a configured PBS Sync Job. If the PBS server has no Sync Job, there is nothing for the integration to run and the action will report an error rather than attempting an alternative operation.

### Can I add more than one PBS server?

Yes. V5 assigns persistent PBS identities so actions, datastores and maintenance state remain associated with the correct PBS instance.

### Hosted or managed PBS shows fewer entities

Hosted PBS providers can restrict node-level or hardware information. The available entities depend on the API access and permissions the provider exposes to your account.

---

## 🛡️ Partial failures and preserved values

### Why does an entity still show its previous value during an API problem?

This can be intentional in V5. The integration refreshes major sections independently and preserves the last valid data for an affected section where possible. When the endpoint becomes available again, fresh values replace the preserved data automatically.

---

## 🎨 Dynamic Proxmox Dashboard

### Is the dashboard required?

No. The dashboard is completely optional. The integration works without it.

### What do I need to use the V5 dashboard?

You need Proxmox Extended Sensors V5, Card Mod and the Lovelace JavaScript resource:

```text
/proxmox_sensors/proxmox-dashboard.js
```

Then create a dashboard using the **Proxmox Extended Sensors** community strategy.

### Can I edit the generated dashboard?

Yes. Use Home Assistant's **Take Control** feature. After taking control, you can customize the dashboard like normal Lovelace.

---

## 🔄 Updates and performance

### How often does the integration update?

The integration uses coordinated asynchronous updates and controlled concurrency to avoid unnecessarily saturating Proxmox APIs. Do not rely on an old fixed interval documented for previous versions; the effective behavior depends on the current coordinator implementation and server type.

---

## 🧾 Before opening an issue

Please check Proxmox connectivity, credentials and realm, API Token status, required permissions, Home Assistant restart after installation/update, `pve-sensors.service` when hardware data is involved, and relevant Home Assistant logs. For Prune, Verify or Sync errors, also confirm that the corresponding PBS Job exists and is correctly configured.

When reporting an issue, remove passwords, token secrets and other credentials from screenshots and logs.

---

## Known limitations

- VM disk percentage is not exposed because there is no sufficiently reliable metric.
- Hosted PBS environments can expose less information than a locally managed PBS.
- Hardware data depends on the host, drivers and sidecar endpoints.
- Immediately after VM/LXC migration, the source-node device can remain temporarily empty while reconciliation completes.

---

[⬅ Back to the V5 documentation](README.md)
