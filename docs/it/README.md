# 📚 Proxmox Extended Sensors V5 — Documentazione

Questa documentazione copre installazione, preparazione di Proxmox, autenticazione, configurazione di Home Assistant, monitoraggio hardware e risoluzione dei problemi di **Proxmox Extended Sensors V5**.

## Guide
- 🌡️ [01. Sensori hardware e Sidecar](01-install-sensors.md)
- 🔐 [02. Utente e permessi Proxmox](02-proxmox-config.md)
- 🔌 [03. Configurazione Home Assistant — PVE, PBS e CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ e risoluzione problemi](04-faq.md)

[⬅ Torna al README principale](../../README.md)

---

## 🚀 Novità di V5

### 🔄 Identità VM/LXC resistente alle migrazioni
Le entità VM e LXC vengono tracciate a livello di cluster. Durante una migrazione V5 è progettata per conservare `unique_id`, `entity_id`, cronologia, statistiche, dashboard, automazioni e controlli del guest.

### 🛡️ Resilienza ai guasti parziali
PVE, PBS e CLUSTER vengono aggiornati in sezioni indipendenti. Un errore temporaneo di una parte dell'API non deve cancellare i dati non correlati e, quando possibile, vengono mantenuti gli ultimi valori validi.

### 🔁 Replica PVE nativa
V5 aggiunge stato globale della replica e, per ogni job, **Durata**, **Ultima replica** e **Prossima replica**. L'identità del job resta stabile anche dopo la migrazione del guest.

### 🗄️ Manutenzione PBS

Le azioni di manutenzione PBS includono:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify e Sync eseguono i Job configurati in PBS. Garbage Collection (GC) viene eseguita direttamente sul datastore.**

Le azioni avviate da Home Assistant vengono correlate all'UPID esatto del task PBS, consentendo di seguirne lo stato reale dall'avvio fino al completamento.

### 🧩 Multi-PBS, ❤️ Sidecar Status e 📊 percentuali
Più server PBS mantengono identità persistenti. Sidecar Status riassume Memory, Mounts, Sensors e SMART per nodo PVE. V5 aggiunge percentuale memoria CT, disco CT e memoria VM; il disco VM non viene esposto per mancanza di una metrica sufficientemente affidabile.

---

## 🎨 Dashboard Proxmox dinamica
V5 include una dashboard Lovelace opzionale per **PVE, PBS e CLUSTER**, generata dalle risorse realmente disponibili.

### Requisiti
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Installazione
1. Installa Card Mod da HACS.
2. Aggiungi `/proxmox_sensors/proxmox-dashboard.js` come **Modulo JavaScript** Lovelace.
3. Ricarica il browser.
4. Crea una dashboard usando la strategia community **Proxmox Extended Sensors**.
5. Scegli **PVE**, **PBS** o **CLUSTER** tra i tipi disponibili.

Con **Take Control** puoi modificarla come una normale dashboard Lovelace. La dashboard è completamente opzionale.

---

## 🌐 Monitoraggio, backup e PBS
In base ai dati disponibili, V5 può mostrare nodi, quorum, CPU/RAM/load/I/O wait, RX/TX, KSM, storage, mount, dischi fisici, SMART, temperature, VM, LXC, task falliti, salute backup e replica PVE.

I servizi `create_vzdump_backup` e `backup_all` usano il backup nativo Proxmox. PBS include utilizzo datastore, backup, deduplicazione, task e manutenzione, correlando le azioni ai task PBS reali.

---

## 🧩 Installazione
### Via HACS — consigliato
[![Apri Proxmox Extended Sensors in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors è incluso nel repository HACS predefinito. Non serve un repository personalizzato.**

1. Apri **HACS → Integrazioni**.
2. Cerca **Proxmox Extended Sensors** e scaricalo.
3. Riavvia Home Assistant.
4. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione** e cerca l'integrazione.

Installazione manuale: copia in `/config/custom_components/proxmox_sensors` e riavvia Home Assistant.

---

## 🧩 Ambienti supportati
Il progetto supporta installazioni moderne di Proxmox VE, Proxmox Backup Server e Home Assistant. Le versioni minime esatte vanno verificate nelle note di rilascio prima della pubblicazione.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
