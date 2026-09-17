# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 Connessione
Controlla raggiungibilità, user/realm, token attivo, secret, permessi API e SSL. `Permission denied` indica spesso permessi insufficienti.

## 🌡️ Hardware e Sidecar
Se mancano temperature: `sensors`, `systemctl status pve-sensors.service`, poi `http://IP_PROXMOX:9000/sensors`.

**Sidecar Status** riassume Memory, Mounts, Sensors e SMART (`ok`, `degraded`, `error`, `unknown`). V5 conserva quando possibile gli ultimi valori validi.

## 🖥️ Migrazione VM/LXC
V5 usa identità cluster-wide per conservare `unique_id`, `entity_id`, cronologia, statistiche, automazioni e dashboard. Il device del nodo sorgente può restare temporaneamente vuoto durante la riconciliazione.

Nessuna percentuale disco VM per mancanza di una metrica affidabile; quella disco CT è disponibile quando esistono i dati.

## 🔁 Replica PVE
Stato cluster più durata, ultima e prossima replica per job. Un errore API/runtime temporaneo non equivale automaticamente a un reale fallimento della replica.

## 🗄️ PBS
V5 supporta GC, Prune, Verify e Sync.

> **Modifica di sicurezza V5:** a differenza di V4.x, **Prune, Verify e Sync non vengono più eseguiti come operazioni dirette costruite dall'integrazione**. V5 avvia il **Job corrispondente già configurato in PBS**. In questo modo si rispettano le policy PBS, in particolare le regole di retention del Prune Job che stabiliscono quali backup possono essere eliminati.

**GC rimane intenzionalmente un'azione diretta sul datastore.** Garbage Collection recupera spazio non referenziato ed è utile nelle automazioni Home Assistant quando lo spazio disponibile per i backup è ridotto.

Prune, Verify e Sync richiedono rispettivamente un **Prune Job, Verify Job o Sync Job** configurato in PBS. Se manca il Job necessario, **l'integrazione restituisce un errore e non esegue alcuna operazione diretta alternativa**. È un comportamento di sicurezza intenzionale, non un malfunzionamento.

Le azioni HA vengono seguite tramite UPID fino al risultato reale. Più PBS mantengono identità persistenti.

## 🛡️ Guasti parziali
Un valore precedente durante un problema API può essere intenzionale: V5 conserva gli ultimi dati validi finché non tornano dati freschi.

## 🎨 Dashboard
Opzionale. Richiede V5, Card Mod e `/proxmox_sensors/proxmox-dashboard.js`. **Take Control** consente la personalizzazione.

## 🧾 Prima di aprire una issue
Controlla connessione, credenziali, token, permessi, riavvio HA, sidecar se coinvolto e log. Per errori Prune/Verify/Sync controlla anche che il Job PBS corrispondente esista e sia configurato correttamente. Rimuovi password e Token Secret da screenshot/log.

## Limitazioni note
- nessuna percentuale disco VM
- PBS gestito può esporre meno dati
- hardware dipende da host, driver e sidecar
- device sorgente temporaneamente vuoto possibile dopo migrazione

[⬅ Torna alla documentazione V5](README.md)
