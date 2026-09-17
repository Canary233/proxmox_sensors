# 📚 Proxmox Extended Sensors V5 — Documentation

This documentation covers installation, Proxmox preparation, authentication, Home Assistant setup, hardware monitoring and troubleshooting for **Proxmox Extended Sensors V5**.

## Guides

- 🌡️ [01. Hardware Sensors Configuration](01-install-sensors.md)
- 🔐 [02. Proxmox User and Permissions](02-proxmox-config.md)
- 🔌 [03. Home Assistant Setup — PVE, PBS and CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ and Troubleshooting](04-faq.md)

[⬅ Back to the main README](../../README.md)

---

## 🚀 What V5 adds

V5 keeps the monitoring and control features from previous versions while introducing a more resilient architecture and stable entity identity across real Proxmox operations.

### 🔄 Migration-safe VM and LXC identity

VM and LXC entities are tracked at cluster scope. When a guest migrates between Proxmox nodes, Home Assistant keeps the same logical identity instead of creating replacement entities.

This is designed to preserve:

- `unique_id`
- `entity_id`
- history and statistics
- dashboards
- automations
- guest controls

### 🛡️ Partial-failure resilience

PVE, PBS and CLUSTER data are refreshed in independent sections. If one API area temporarily fails, unrelated data can continue updating and the last valid values of the affected section are preserved where possible.

### 🔁 Native PVE replication monitoring

V5 adds cluster-level replication status plus per-job entities such as:

- Duration
- Last Replication
- Next Replication

Replication job identity remains stable when the guest moves to another node.

### 🗄️ Expanded PBS maintenance monitoring

PBS maintenance actions include:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify and Sync execute the Jobs configured in PBS. Garbage Collection (GC) runs directly on the datastore.**

Actions started from Home Assistant are correlated with the exact PBS task UPID, allowing the integration to follow their real state from start to completion.

### 🧩 Multi-PBS identity

Multiple PBS servers can coexist without mixing maintenance state or datastore actions. V5 assigns persistent PBS server identities and keeps them isolated inside Home Assistant.

### ❤️ Sidecar Status

Each PVE node exposes a **Sidecar Status** diagnostic sensor summarizing the state of the hardware sidecar endpoints used for:

- Memory
- Mounts
- Sensors
- SMART

### 📊 Additional percentage sensors

V5 adds:

- CT memory percentage
- CT disk percentage
- VM memory percentage

VM disk percentage is intentionally not exposed because no sufficiently reliable source metric is currently available.

---

## 🎨 Dynamic Proxmox Dashboard

V5 includes an optional Lovelace dashboard system for **PVE, PBS and CLUSTER**.

The dashboard is generated from the entities and resources actually available in your Home Assistant installation, so sections that are not present in your environment are not offered as empty dashboards.

### Requirements

- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Dashboard installation

1. Install **Card Mod** from HACS if needed.
2. Add this Lovelace resource as a **JavaScript Module**:

   ```text
   /proxmox_sensors/proxmox-dashboard.js
   ```

3. Reload the browser.
4. Create a new dashboard and select the **Proxmox Extended Sensors** community strategy.
5. Choose one of the dashboard types available for your installation: **PVE**, **PBS** or **CLUSTER**.

The generated dashboard remains strategy-driven until you choose Home Assistant's **Take Control** option. After taking control, you can edit it like a normal Lovelace dashboard.

> The dashboard is optional. The integration works normally without it.

---

## 🌐 PVE and CLUSTER monitoring

Depending on the configured server type and available data, the integration can expose information for:

- Proxmox nodes
- cluster health and quorum
- CPU, RAM, load and I/O wait
- network RX/TX
- KSM
- storages and mounted disks
- physical disks and SMART
- hardware temperatures
- virtual machines
- LXC containers
- failed tasks
- backup jobs and backup health
- PVE replication

---

## 🖥️ Virtual Machines and Containers

VM and LXC devices can expose status, uptime, CPU, memory, network traffic and other guest information available through Proxmox.

V5 also tracks expected boot state (`onboot`) and keeps guest identity stable during migrations between nodes.

Guest controls are exposed as Home Assistant button entities when the corresponding action is available.

---

## 💾 Backup services

The integration provides Home Assistant services for Proxmox VE guest backups.

### `create_vzdump_backup`

- Supports one or multiple guest IDs.
- Uses native Proxmox backup execution.
- Supports local, network and PBS storage targets available to PVE.

### `backup_all`

- Backs up the selected guests on a node.
- Supports configurable concurrency and delays.
- Can be used from Home Assistant automations.

---

## 🗄️ Proxmox Backup Server

PBS monitoring includes datastore usage, backup information, deduplication data, task state and maintenance information exposed by the PBS API.

V5 improves maintenance tracking by correlating actions with their actual PBS tasks rather than treating a successful POST request as task completion.

---

## 🧩 Installation

### Via HACS — recommended

[![Open your Home Assistant instance and open Proxmox Extended Sensors in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors is included in the default HACS repository. No custom repository is required.**

1. Open **HACS → Integrations**.
2. Search for **Proxmox Extended Sensors**.
3. Download the integration.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration**.
6. Search for **Proxmox Extended Sensors**.

Continue with [03. Home Assistant Setup — PVE, PBS and CLUSTER](03-login-pve-pbs.md).

### Manual installation

Copy the integration to:

```text
/config/custom_components/proxmox_sensors
```

Then restart Home Assistant and add the integration from **Settings → Devices & Services**.

---

## 🧩 Supported environments

The project supports modern Proxmox VE, Proxmox Backup Server and Home Assistant installations. Exact minimum supported versions should be checked against the current release notes before publication.

---

## 🤝 Contributions and Community

Issues and pull requests are welcome in the official repository:

https://github.com/Javisen/proxmox_sensors

If the integration is useful to you, consider leaving a ⭐ on GitHub.

---

<p align="center"><i>Maintained by Javisen — MIT License</i></p>
