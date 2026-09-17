# 📚 Proxmox Extended Sensors V5 — Documentatie

Deze documentatie behandelt installatie, Proxmox-voorbereiding, authenticatie, Home Assistant-configuratie, hardwaremonitoring en probleemoplossing voor **Proxmox Extended Sensors V5**.

## Handleidingen
- 🌡️ [01. Hardwaresensoren en Sidecar](01-install-sensors.md)
- 🔐 [02. Proxmox-gebruiker en rechten](02-proxmox-config.md)
- 🔌 [03. Home Assistant-configuratie — PVE, PBS en CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ en probleemoplossing](04-faq.md)

[⬅ Terug naar de hoofd-README](../../README.md)

---

## 🚀 Nieuw in V5

### 🔄 Migratievaste VM/LXC-identiteit
VM- en LXC-entiteiten worden clusterbreed gevolgd. Bij migratie zijn `unique_id`, `entity_id`, geschiedenis, statistieken, dashboards, automatiseringen en guest-controls ontworpen om behouden te blijven.

### 🛡️ Weerbaarheid tegen gedeeltelijke storingen
PVE-, PBS- en CLUSTER-data worden in onafhankelijke secties vernieuwd. Een tijdelijke API-storing hoeft andere data niet te wissen; waar mogelijk blijven de laatste geldige waarden behouden.

### 🔁 Native PVE-replicatiemonitoring
V5 voegt clusterstatus en per job **Duur**, **Laatste replicatie** en **Volgende replicatie** toe. De jobidentiteit blijft stabiel na guest-migratie.

### 🗄️ PBS-onderhoud

PBS-onderhoudsacties omvatten:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify en Sync voeren de in PBS geconfigureerde Jobs uit. Garbage Collection (GC) wordt rechtstreeks op de datastore uitgevoerd.**

Acties die vanuit Home Assistant worden gestart, worden gekoppeld aan de exacte UPID van de PBS-taak, zodat hun werkelijke status van start tot voltooiing kan worden gevolgd.

### 🧩 Multi-PBS, ❤️ Sidecar Status en 📊 percentages
Meerdere PBS-servers krijgen persistente identiteiten. Sidecar Status vat Memory, Mounts, Sensors en SMART per PVE-node samen. V5 voegt CT-geheugen %, CT-schijf % en VM-geheugen % toe. VM-schijf % ontbreekt bewust wegens onvoldoende betrouwbare brondata.

---

## 🎨 Dynamisch Proxmox-dashboard
V5 bevat een optioneel Lovelace-dashboard voor **PVE, PBS en CLUSTER**, gegenereerd uit werkelijk aanwezige resources.

### Vereisten
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Installatie
1. Installeer Card Mod via HACS.
2. Voeg `/proxmox_sensors/proxmox-dashboard.js` toe als Lovelace **JavaScript Module**.
3. Herlaad de browser.
4. Maak een dashboard met de communitystrategie **Proxmox Extended Sensors**.
5. Kies **PVE**, **PBS** of **CLUSTER** uit de aangeboden typen.

Met **Take Control** wordt het dashboard normaal bewerkbaar. Het dashboard is volledig optioneel.

---

## 🌐 Monitoring, backups en PBS
Afhankelijk van beschikbare data kan V5 nodes, quorum, CPU/RAM/load/I/O wait, RX/TX, KSM, storages, mounts, fysieke schijven, SMART, temperaturen, VM's, LXC's, mislukte taken, backupstatus en PVE-replicatie tonen.

`create_vzdump_backup` en `backup_all` gebruiken native Proxmox-backups. PBS omvat datastoregebruik, backups, deduplicatie, taken en onderhoud, met koppeling aan de echte PBS-taken.

---

## 🧩 Installatie
### Via HACS — aanbevolen
[![Open Proxmox Extended Sensors in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors staat in de standaard HACS-repository. Een custom repository is niet nodig.**

1. Open **HACS → Integraties**.
2. Zoek **Proxmox Extended Sensors** en download.
3. Herstart Home Assistant.
4. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen** en zoek de integratie.

Handmatig: kopieer naar `/config/custom_components/proxmox_sensors` en herstart Home Assistant.

---

## 🧩 Ondersteunde omgevingen
Het project ondersteunt moderne installaties van Proxmox VE, Proxmox Backup Server en Home Assistant. Exacte minimumversies moeten vóór publicatie met de actuele release notes worden gecontroleerd.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
