# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 Verbindung
**Keine Verbindung:** Erreichbarkeit, User/Realm, aktiven Token, Secret, API-Rechte und SSL-Einstellungen prüfen. `Permission denied` weist meist auf fehlende Benutzer-/Tokenrechte oder Privilege Separation hin.

## 🌡️ Hardware und Sidecar
Bei fehlenden Temperaturen zuerst `sensors`, dann `systemctl status pve-sensors.service` und `http://DEINE_PROXMOX_IP:9000/sensors` prüfen.

**Sidecar Status** fasst Memory, Mounts, Sensors und SMART zusammen (`ok`, `degraded`, `error`, `unknown`). Bei Ausfall bleiben letzte gültige Hardwarewerte nach Möglichkeit erhalten.

## 🖥️ VM/LXC-Migration
V5 verwendet clusterweite Guest-Identität. `unique_id`, `entity_id`, Verlauf, Statistiken, Automationen und Dashboards sollen bei Migration erhalten bleiben. Das Quellknoten-Gerät kann während der Reconciliation kurzzeitig leer bleiben.

VM-Datenträger % wird bewusst nicht angeboten; CT-Datenträger % ist verfügbar, wenn die Daten vorliegen.

## 🔁 PVE-Replikation
V5 bietet clusterweiten Status sowie Dauer, letzte und nächste Replikation pro Job. Ein temporärer API-/Runtime-Fehler wird nicht automatisch als echter Replikationsfehler gewertet.

## 🗄️ PBS
Unterstützt werden GC, Prune, Verify und Sync.

> **Sicherheitsänderung in V5:** Anders als in V4.x werden **Prune, Verify und Sync nicht mehr als direkte, von der Integration erzeugte Wartungsoperationen ausgeführt**. V5 startet den entsprechenden, bereits in PBS konfigurierten **Job**. Dadurch bleiben die PBS-Richtlinien maßgeblich; insbesondere bei Prune werden die konfigurierten Aufbewahrungsregeln berücksichtigt.

**GC bleibt absichtlich eine direkte Datastore-Aktion**, da Garbage Collection nicht referenzierten Speicher freigibt und sich deshalb gut für Home-Assistant-Automationen bei knappem Backup-Speicher eignet.

Prune, Verify und Sync benötigen jeweils einen passenden **Prune Job, Verify Job bzw. Sync Job** in PBS. Fehlt der entsprechende Job, **meldet die Integration einen Fehler und führt keine direkte Ersatzoperation aus**. Das ist beabsichtigtes Sicherheitsverhalten und kein Fehler der Integration.

Home-Assistant-Aktionen werden über die PBS-UPID bis zum tatsächlichen Ergebnis verfolgt. Mehrere PBS-Server erhalten persistente Identitäten.

## 🛡️ Teilfehler
Ein alter Wert während eines API-Problems kann beabsichtigt sein: V5 bewahrt nach Möglichkeit den letzten gültigen Wert, bis wieder frische Daten verfügbar sind.

## 🎨 Dashboard
Das Dashboard ist optional. Benötigt werden V5, Card Mod und `/proxmox_sensors/proxmox-dashboard.js`. Mit **Take Control** kann es anschließend normal bearbeitet werden.

## 🧾 Vor einem Issue
Erreichbarkeit, Zugangsdaten, Token, Rechte, HA-Neustart, Sidecar bei Hardwareproblemen und Logs prüfen. Bei Prune-/Verify-/Sync-Fehlern zusätzlich prüfen, ob der entsprechende PBS Job existiert und korrekt konfiguriert ist. Passwörter und Token Secrets aus Logs/Screenshots entfernen.

## Bekannte Einschränkungen
- kein VM-Datenträger-Prozentsensor
- Managed PBS kann weniger Daten liefern
- Hardwaredaten hängen von Host/Treibern/Sidecar ab
- nach VM/LXC-Migration kann das Quellgerät vorübergehend leer sein

[⬅ Zurück zur V5-Dokumentation](README.md)
