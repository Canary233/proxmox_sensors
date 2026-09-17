# 🔌 Stap 3: Home Assistant — PVE, PBS en CLUSTER

## 1. HACS
[![Open in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

De integratie staat in de standaard HACS-repository; geen custom repository nodig. Zoek **Proxmox Extended Sensors** in **HACS → Integraties**, download en herstart Home Assistant.

## 2. Integratie toevoegen
**Instellingen → Apparaten & diensten → Integratie toevoegen → Proxmox Extended Sensors**. Typen: **PVE**, **PBS**, **CLUSTER**.

## 3. Host en authenticatie
Voer IP of hostname in. PVE ondersteunt gebruiker/wachtwoord of API Token; PBS gebruikt API Token in de huidige V5-flow. Bij token: volledige User+realm, alleen tokennaam als Token ID en Token Secret.

## 4. PVE
Na verbinding ontdekt de integratie nodes en resources zoals VM's, LXC's, storages en hardware. V5's clusterbrede identiteit laat VM/LXC-entiteiten migraties volgen.

## 5. PBS
Elke PBS krijgt een eigen config entry en persistente identiteit. Monitoring kan datastore, backups, deduplicatie, taken, GC, Prune, Verify en Sync met Sync Job omvatten.

## 6. CLUSTER
Omvat quorum, nodes, geaggregeerde CPU/RAM, VM/CT-aantallen, clusterstorage, mislukte taken, backupstatus en PVE-replicatie.

## 7. Optioneel dashboard
Installeer Card Mod, voeg `/proxmox_sensors/proxmox-dashboard.js` als JavaScript Module toe, herlaad browser en maak een dashboard met **Proxmox Extended Sensors** communitystrategie. Kies PVE/PBS/CLUSTER. **Take Control** maakt normale Lovelace-bewerking mogelijk.

## 8. Hosted PBS
Providers kunnen hardware/low-level data beperken. Beschikbare entiteiten hangen af van API-toegang en rechten.

Volgende: [04. FAQ](04-faq.md)
