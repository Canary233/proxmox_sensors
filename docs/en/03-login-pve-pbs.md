# 🔌 Step 3: Home Assistant Setup — PVE, PBS and CLUSTER

This guide explains how to install **Proxmox Extended Sensors V5** and add PVE, PBS or CLUSTER connections to Home Assistant.

---

## 1. Install via HACS

[![Open your Home Assistant instance and open Proxmox Extended Sensors in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors is included in the default HACS repository. You do not need to add a custom repository.**

1. Open **HACS → Integrations**.
2. Search for **Proxmox Extended Sensors**.
3. Download it.
4. Restart Home Assistant.

---

## 2. Add the integration

After restarting Home Assistant:

1. Go to **Settings → Devices & Services**.
2. Click **Add Integration**.
3. Search for **Proxmox Extended Sensors**.

The first setup screen asks for:

- Host
- Server type

Available server types are:

- **PVE** — Proxmox Virtual Environment
- **PBS** — Proxmox Backup Server
- **CLUSTER** — Proxmox cluster view

---

## 3. Host

Enter the server IP address or hostname, for example:

```text
192.168.1.50
```

or:

```text
pve.example.local
```

The integration handles the connection scheme internally, so normally you should enter only the host value requested by the setup form.

---

## 4. Authentication

### PVE

V5 supports:

- Username + password
- API Token

### PBS

The current V5 setup flow uses **API Token authentication** for PBS.

### CLUSTER

CLUSTER authentication follows its own setup flow and uses the credentials configured for cluster access.

---

## 5. API Token fields

When token authentication is selected, enter:

- **User** → complete user and realm, for example `homeassistant@pve`
- **Token ID** → token name only, for example `ha-token`
- **Token Secret** → generated token secret

Do not place the complete combined token string in the Token ID field.

---

## 6. PVE node and resource selection

After a valid PVE connection, the integration discovers the available Proxmox resources and continues through its node/resource selection flow.

Depending on the environment, you can configure monitoring for resources such as:

- nodes
- VMs
- LXC containers
- storages
- hardware information

V5 is cluster-aware for VM/LXC identity, so guest entities can follow migrations between nodes while preserving their Home Assistant identity.

---

## 7. PBS setup

A PBS connection creates its own Home Assistant config entry.

V5 assigns a persistent PBS server identity so multiple PBS instances can coexist without mixing maintenance actions or datastore state.

PBS monitoring can include:

- datastore usage
- backup information
- deduplication
- task status
- GC
- Prune
- Verify
- Sync when a Sync Job exists

---

## 8. CLUSTER setup

The CLUSTER server type is used for cluster-wide entities such as:

- quorum and node state
- aggregate CPU and RAM
- VM and CT counts
- cluster storage information
- failed tasks
- backup health
- PVE replication status

---

## 9. Optional Dynamic Proxmox Dashboard

V5 includes an optional dashboard generator for PVE, PBS and CLUSTER.

### Requirements

- Proxmox Extended Sensors V5
- Card Mod

### Installation

1. Install **Card Mod** from HACS.
2. Add this Lovelace resource as a **JavaScript Module**:

   ```text
   /proxmox_sensors/proxmox-dashboard.js
   ```

3. Reload the browser.
4. Create a new dashboard and choose the **Proxmox Extended Sensors** community strategy.
5. Select one of the dashboard types offered for your installation: **PVE**, **PBS** or **CLUSTER**.

The dashboard remains strategy-driven until you choose **Take Control**. After that, you can edit it like any normal Lovelace dashboard.

---

## 10. Managed PBS services

On hosted or multi-tenant PBS services, the provider may restrict low-level node and hardware information.

That does not necessarily indicate an integration error. The available entities depend on what the provider exposes through your PBS account and API permissions.

---

## ✔ Conclusion

Your PVE, PBS and/or CLUSTER connection should now be available in Home Assistant.

Next: [04. FAQ and Troubleshooting](04-faq.md)
