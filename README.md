<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

> **Advanced Proxmox VE & PBS monitoring, control and dashboard integration for Home Assistant.**

# 🚀 Proxmox Extended Sensors (v5)

## 📚 Documentation & Guides

**Select your language to start the installation and configuration:**

[![English](https://img.shields.io/badge/ENGLISH-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/en/README.md)
[![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/zh/README.md)
[![Español](https://img.shields.io/badge/ESPA%C3%91OL-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/es/README.md)
[![Italiano](https://img.shields.io/badge/ITALIANO-green?style=for-the-badge&logo=translate&logoColor=white)](docs/it/README.md)
[![Français](https://img.shields.io/badge/FRAN%C3%87AIS-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/fr/README.md)
[![Deutsch](https://img.shields.io/badge/DEUTSCH-red?style=for-the-badge&logo=translate&logoColor=white)](docs/de/README.md)
[![Nederlands](https://img.shields.io/badge/NEDERLANDS-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/nl/README.md)
[![Português](https://img.shields.io/badge/PORTUGU%C3%8AS-green?style=for-the-badge&logo=translate&logoColor=white)](docs/pt/README.md)
[![Русский](https://img.shields.io/badge/%D0%A0%D0%A3%D0%A1%D0%A1%D0%9A%D0%98%D0%99-lightgrey?style=for-the-badge&logo=translate&logoColor=white)](docs/ru/README.md)
[![Українська](https://img.shields.io/badge/%D0%A3%D0%9A%D0%A0%D0%90%D0%87%D0%9D%D0%A1%D0%AC%D0%9A%D0%90-yellow?style=for-the-badge&logo=translate&logoColor=white)](docs/uk/README.md)

---

## 📑 Table of Contents

- [Introduction](#-introduction)
- [What's New in V5](#-whats-new-in-v5)
- [Dynamic Proxmox Dashboard](#-dynamic-proxmox-dashboard)
- [Migration-Safe VM & LXC Monitoring](#-migration-safe-vm--lxc-monitoring)
- [Resilient Monitoring & Fault Isolation](#-resilient-monitoring--fault-isolation)
- [PVE Replication Status](#-pve-replication-status)
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)
- [Multi-PBS Support](#-multi-pbs-support)
- [Sidecar Status](#-sidecar-status)
- [Cluster Monitoring](#-cluster-monitoring)
- [Mounted Disks & Network Storage](#-mounted-disks--network-storage)
- [Hardware & Node Monitoring](#-hardware--node-monitoring)
- [Virtual Machines & Containers](#-virtual-machines--containers)
- [Backup Services](#-backup-services-vms--cts)
- [Supported Versions](#-supported-versions)
- [Installation](#-installation)

---

## 🚀 Introduction

**Proxmox Extended Sensors v5** is the next major evolution of the integration, focused on resilience, stable entity identity, cluster-aware guest tracking and a much richer Home Assistant experience.

V5 keeps the detailed monitoring introduced in previous versions while making the integration safer during real-world events such as VM/LXC migrations, temporary API failures, PBS maintenance tasks and replication changes.

It also introduces an optional **dynamic Lovelace dashboard for PVE, PBS and CLUSTER**, generated from the resources that actually exist in your Home Assistant installation. The dashboard gives you a complete starting point and can later be customized using Home Assistant's **Take Control** feature.

---

## ✨ What's New in V5

- 🔄 **Migration-safe VM/LXC identity** — guests keep their Home Assistant identity when moving between Proxmox nodes.
- 🛡️ **Partial-failure resilience** — valid data is preserved when only one API section or subsystem fails.
- 🔁 **Native PVE Replication monitoring** — global replication status plus per-job runtime information.
- 🗄️ **Improved PBS maintenance actions** — GC, Prune, Verify and Sync tracking with exact UPID correlation.
- 🧩 **Stable multi-PBS identity** — multiple PBS servers remain isolated without entity collisions.
- ❤️ **Sidecar Status** — one diagnostic entity per PVE node reports the health of Memory, Mounts, Sensors and SMART sidecar endpoints.
- 📊 **New percentage sensors** — CT memory, CT disk and VM memory percentages.
- 🎨 **Dynamic Proxmox Dashboard** — PVE, PBS and CLUSTER dashboards generated from the resources actually available.
- 🧱 **Future-ready Device Registry support** — updated relationship handling for upcoming Home Assistant changes.
  
> [!CAUTION]
> **Upgrading from a previous version?**  
> Update the sidecar script and restart its service on **every PVE node**. This is required for the new KSM Status sensor and to keep the sidecar endpoints aligned with V5.

<details>
<summary>Update <code>pve-sensors-api.py</code></summary>

```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
systemctl restart pve-sensors.service
```

</details>


<details>
<summary><b>🔎 More about the V5 reliability architecture</b></summary>

V5 isolates API work into independent tasks with individual timeouts and controlled concurrency. A failure in one section no longer needs to invalidate unrelated data.

The integration preserves the last valid values for affected sections and automatically returns to fresh data when communication is restored. This behavior applies across PVE node data, hardware, storage, VM/LXC information, PBS sections and CLUSTER metadata.

Guest discovery is cluster-aware, allowing VM and LXC entities to follow their guest between nodes without creating replacement entities or losing Home Assistant history.

</details>

---

## 🎨 Dynamic Proxmox Dashboard

V5 adds an optional dashboard system that builds a complete Lovelace starting point from the entities and resources discovered in your installation.

### Available dashboard types

- **PVE** — node health, temperatures, node information, storage, CTs, VMs, diagnostics and replication.
- **PBS** — server health, datastores, backup information, maintenance, tasks and actions.
- **CLUSTER** — cluster health, resources, system state, backup health and replication.

Only dashboard types backed by real resources are offered. The integration never creates an empty PVE, PBS or CLUSTER dashboard.

### Why use it?

- No need to design the entire Proxmox dashboard from scratch.
- Uses the resources actually discovered in your installation.
- Keeps PVE, PBS and CLUSTER logically separated.
- Built on Lovelace so it remains part of the normal Home Assistant dashboard system.
- You can use **Take Control** and then move, remove or add cards exactly as you would in any other Lovelace dashboard.

> The dashboard is completely optional. Proxmox Extended Sensors works normally without installing it.

<details>
<summary><b>📦 Dashboard requirements & installation</b></summary>

### Requirements

- Proxmox Extended Sensors v5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Installation

1. Install **Card Mod** from HACS if it is not already installed.
2. Add the following Lovelace resource as a **JavaScript Module**:

   ```text
   /proxmox_sensors/proxmox-dashboard.js
   ```

3. Reload the browser.
4. Create a new dashboard from **Settings → Dashboards → Add dashboard → Community**.
5. Select **Proxmox Extended Sensors**.
6. Choose one of the dashboard types offered for your installation: **PVE**, **PBS** or **CLUSTER**.

The generated dashboard remains strategy-driven until you choose **Take Control**.

</details>

<details>
<summary><b>🛠️ What happens when I use Take Control?</b></summary>

Home Assistant converts the generated dashboard into a normal editable Lovelace configuration.

From that point you can reorganize the layout, remove cards, add your own entities and combine Proxmox information with anything else in Home Assistant.

The integration does not overwrite a dashboard that you have taken control of.

</details>



## 📸 Dashboard screenshots

<details>
<summary><b>PVE</b></summary>

<br>
<img src="https://github.com/Javisen/test_javisen/raw/refs/heads/main/img/Dashb_Node.png" alt="PVE dashboard" width="100%">

</details>

<details>
<summary><b>PBS</b></summary>

<br>
<img src="https://github.com/Javisen/test_javisen/raw/refs/heads/main/img/Dashb_PBS.png" alt="PBS dashboard" width="100%">

</details>

<details>
<summary><b>CLUSTER</b></summary>

<br>
<img src="https://github.com/Javisen/test_javisen/raw/refs/heads/main/img/Dashb_Cluster.png" alt="CLUSTER dashboard" width="100%">

</details>

---

## 🔄 Migration-Safe VM & LXC Monitoring

V5 tracks guests at cluster scope instead of treating the physical node as part of the guest identity.

When a VM or LXC migrates between Proxmox nodes, Home Assistant keeps the same logical entity identity instead of creating a new guest representation.

- Existing `unique_id` continuity is preserved.
- Existing `entity_id` continuity is preserved.
- History and statistics remain attached to the same entities.
- Dashboards and automations continue referencing the same entities.
- Guest controls follow the migrated VM/LXC.

<details>
<summary><b>🔎 Migration behavior and known limitation</b></summary>

Migration reconciliation is progressive. Immediately after a guest moves, the device associated with the source node can remain temporarily empty while sensors, replication information and cleanup converge over subsequent coordinator cycles.

This temporary state is accepted by design in order to prioritize entity continuity and safe reconciliation.

</details>

---

## 🛡️ Resilient Monitoring & Fault Isolation

V5 is designed so that one failing subsystem does not unnecessarily invalidate the rest of the integration.

- Independent API task timeouts.
- Controlled concurrency to avoid API saturation.
- Section-level preservation of the last valid data.
- Automatic recovery when the affected endpoint becomes available again.
- Safe cleanup during partial first refreshes.
- Cluster metadata preservation without creating duplicate VM/LXC devices.

<details>
<summary><b>⚙️ Technical details</b></summary>

The coordinator uses independent task protection together with controlled asynchronous concurrency. Partial failures are isolated and the integration can preserve previously valid data for the affected section while unrelated sections continue to update normally.

This protection covers PVE, PBS, CLUSTER metadata and sidecar-backed hardware information.

</details>

---

## 🔁 PVE Replication Status

V5 adds native monitoring for Proxmox VE replication jobs.

### Cluster-level entities

- **Replication Jobs** — number and inventory of configured replication jobs.
- **Replication Status** — global replication state and failed-job details.

### Per-job information

Each replication job can expose:

- Duration
- Last Replication
- Next Replication
- Source and target
- Guest and VM type
- Failure count
- Runtime freshness and error details

Replication identity is based on the Proxmox replication job ID rather than the physical node, so replication information continues to follow a VM/LXC when it migrates.

<details>
<summary><b>🔎 Failure handling</b></summary>

Inventory and runtime information are preserved independently. A temporary failure querying the replication runtime is not automatically interpreted as a failed replication job.

The integration distinguishes fresh data, preserved data and unknown runtime state.

</details>

---

## 🗄️ Proxmox Backup Server (PBS)

V5 significantly expands PBS monitoring and action tracking.

### Maintenance actions

- **Garbage Collection (GC)** — direct datastore action.
- **Prune** — runs the configured Prune Job for the datastore.
- **Verify** — runs the configured Verify Job.
- **Sync** — runs the configured Sync Job when available.

Actions launched from Home Assistant are tracked using the exact **UPID** returned by PBS.

This allows the integration to distinguish between:

**Started → Running → OK / Error**

instead of treating an accepted POST request as a completed task.

### Datastore visibility

PBS monitoring includes datastore usage, backup information, deduplication and maintenance status using the real metrics exposed by PBS.

<details>
<summary><b>🔎 How PBS action tracking works</b></summary>

The UPID returned by PBS is kept per server, datastore and action. When that exact task appears in the PBS task list, the integration follows its real runtime and final result.

When no Home Assistant-triggered UPID is available, the integration can still fall back to the most recent matching job for tasks launched directly from PBS or by a schedule.

GC runs directly against the datastore. Prune, Verify and Sync use their configured PBS jobs.

</details>

---

## 🧩 Multi-PBS Support

V5 introduces persistent PBS server identity so multiple Proxmox Backup Server instances remain isolated inside Home Assistant.

- Stable `server_id` allocation.
- Re-added PBS instances can recover their previous identity.
- New PBS instances do not reuse reserved historical IDs.
- Maintenance actions and last-action tracking remain associated with the correct PBS server.
- Datastores with the same name on different PBS instances do not collide functionally.

---

## ❤️ Sidecar Status

Each PVE node exposes a single **Sidecar Status** diagnostic sensor summarizing the health of the existing `pve-sensors` endpoints:

- Memory
- Mounts
- Sensors
- SMART

Possible states:

- `ok`
- `degraded`
- `error`
- `unknown`

When the sidecar fails, previously valid hardware values are preserved instead of disappearing immediately.

---

## 🌐 Cluster Monitoring

Monitor the Proxmox cluster as a whole with dedicated entities for:

- Nodes online
- CPU and RAM usage
- Running VMs
- Running CTs
- Storage usage
- Firewall state
- Failed tasks
- Backup jobs, backup age and backup health
- Replication jobs and replication status

---

## 💽 Mounted Disks & Network Storage

Deep visibility into each node's storage layer:

- Automatic discovery of local and network mounts.
- CIFS/SMB and NFS information.
- Usage and mount details.
- Detection of missing mounts.
- Filtering of irrelevant temporary/system mounts.

---

## 🧠 Hardware & Node Monitoring

- CPU and system health information.
- Package/core thermal monitoring where available.
- Chipset and NVMe temperatures.
- NVMe SMART and health information.
- DIMM/SMBIOS information where supported by the sidecar.
- I/O Wait and network traffic.
- KSM information.
- Node update information.

---

## 🖥️ Virtual Machines & Containers

VM and LXC monitoring includes the guest state and resource information exposed by Proxmox and the integration.

V5 additionally includes:

- **CT memory percentage**
- **CT disk percentage**
- **VM memory percentage**
- `onboot`, expected state and state/onboot matching information
- Cluster-aware migration continuity

> VM disk percentage is not exposed because V5 does not currently have a sufficiently reliable source metric for it.

---

## 💾 Backup Services (VMs & CTs)

The integration provides backup orchestration directly from Home Assistant.

### 🟦 Single/Batch Backup (`create_vzdump_backup`)

- Supports local storage, NFS and PBS targets.
- Multiple guest IDs can be backed up in one operation.
- Native Proxmox backup execution preserves compatibility with PBS deduplication.

### 🟩 Massive Backup (`backup_all`)

- Back up all guests on a node.
- Configurable concurrency and delays.
- Suitable for scheduled Home Assistant automations.

---

## 🧩 Supported Versions

- Proxmox VE 7.x / 8.x / 9.x
- Proxmox Backup Server 3.x / 4.x
- Home Assistant 2026.5+

---

## 🧩 Installation

### 🔹 Via HACS (Recommended)

[![Open your Home Assistant instance and open Proxmox Extended Sensors in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors is available in the default HACS repository — no custom repository is required.**

1. Open **HACS → Integrations**.
2. Search for **Proxmox Extended Sensors**.
3. Click **Download**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration**.
6. Search for **Proxmox Extended Sensors** and configure your PVE, PBS and/or CLUSTER connection.

> The optional Proxmox Dashboard is installed separately.
> See [Dynamic Proxmox Dashboard](#-dynamic-proxmox-dashboard).

---

## 🙌 Special Thanks

Special thanks to the community members who tested the integration across different hardware and Proxmox environments and contributed bug reports, diagnostics and validation.

Previous development cycles especially benefited from testing around:

- lm-sensors compatibility
- PBS behavior
- cluster monitoring
- backup jobs
- storage layouts
- hardware differences between systems

V5 additionally benefited from real-world testing of guest migration, replication behavior, PBS maintenance tracking, sidecar failures and dashboard generation.

Thank you to everyone who reports issues, tests fixes and helps make the integration more reliable. ❤️

---

## 🤝 Contributing

Contributions, testing and bug reports are welcome.

Please use the GitHub issue tracker for reproducible problems and include relevant Home Assistant / Proxmox logs where appropriate.

---

## 📄 License

MIT License

Copyright (c) Javisen
