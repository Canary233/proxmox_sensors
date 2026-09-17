# 🔌 Passo 3: Home Assistant — PVE, PBS e CLUSTER

## 1. HACS
[![Apri in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

L'integrazione è nel repository HACS predefinito: non serve un repository personalizzato. Cerca **Proxmox Extended Sensors** in **HACS → Integrazioni**, scarica e riavvia Home Assistant.

## 2. Aggiungi l'integrazione
**Impostazioni → Dispositivi e servizi → Aggiungi integrazione → Proxmox Extended Sensors**.

Tipi: **PVE**, **PBS**, **CLUSTER**.

## 3. Host e autenticazione
Inserisci IP o hostname. PVE accetta utente/password o API Token; PBS usa API Token nel flusso V5 attuale. Con token inserisci User completo con realm, solo il nome come Token ID e il Token Secret.

## 4. PVE
Dopo la connessione vengono rilevati nodi e risorse come VM, LXC, storage e hardware. L'identità cluster-wide di V5 permette alle entità VM/LXC di seguire le migrazioni.

## 5. PBS
Ogni PBS ha una config entry e identità persistente proprie. Può includere datastore, backup, deduplicazione, task, GC, Prune, Verify e Sync se esiste un Sync Job.

## 6. CLUSTER
Include quorum, nodi, CPU/RAM aggregate, conteggi VM/CT, storage cluster, task falliti, salute backup e replica PVE.

## 7. Dashboard opzionale
Installa Card Mod, aggiungi `/proxmox_sensors/proxmox-dashboard.js` come Modulo JavaScript, ricarica il browser e crea una dashboard con la strategia **Proxmox Extended Sensors**. Scegli PVE/PBS/CLUSTER. **Take Control** consente poi la normale modifica Lovelace.

## 8. PBS gestito
Un provider PBS può limitare dati hardware o di basso livello. Le entità dipendono da accesso API e permessi disponibili.

Avanti: [04. FAQ](04-faq.md)
