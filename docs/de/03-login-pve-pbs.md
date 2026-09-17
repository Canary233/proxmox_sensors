# 🔌 Schritt 3: Home Assistant — PVE, PBS und CLUSTER

## 1. Installation über HACS
[![In HACS öffnen.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

Die Integration ist im Standard-HACS-Repository enthalten; kein Custom Repository nötig. Unter **HACS → Integrationen** nach **Proxmox Extended Sensors** suchen, herunterladen und Home Assistant neu starten.

## 2. Integration hinzufügen
**Einstellungen → Geräte & Dienste → Integration hinzufügen → Proxmox Extended Sensors**.

Servertypen:
- **PVE** — Proxmox Virtual Environment
- **PBS** — Proxmox Backup Server
- **CLUSTER** — clusterweite Ansicht

## 3. Host und Authentifizierung
IP oder Hostname eingeben. PVE unterstützt Benutzer/Passwort und API Token; PBS verwendet im aktuellen V5-Flow API Token. Bei Token-Login: vollständigen User+Realm, nur den Token-Namen als Token ID und das Token Secret eintragen.

## 4. PVE
Nach erfolgreicher Verbindung erkennt die Integration Knoten und Ressourcen wie VMs, LXC, Storages und Hardware. V5 verfolgt VM/LXC clusterweit, sodass ihre Home-Assistant-Identität bei Migrationen erhalten bleibt.

## 5. PBS
Jede PBS-Verbindung erhält eine eigene Config Entry und persistente Serveridentität. Monitoring kann Datastore-Nutzung, Backups, Deduplizierung, Tasks, GC, Prune, Verify und Sync bei vorhandenem Sync Job umfassen.

## 6. CLUSTER
CLUSTER stellt unter anderem Quorum, Knotenzustand, aggregierte CPU/RAM, VM/CT-Anzahlen, Cluster-Storage, fehlgeschlagene Tasks, Backup-Zustand und PVE-Replikation bereit.

## 7. Optionales Dashboard
Card Mod installieren, `/proxmox_sensors/proxmox-dashboard.js` als JavaScript-Modul hinzufügen, Browser neu laden und ein Dashboard mit der Community-Strategie **Proxmox Extended Sensors** erstellen. Danach PVE, PBS oder CLUSTER wählen. Mit **Take Control** wird es normal editierbar.

## 8. Gehostetes PBS
Bei Managed/Multi-Tenant-PBS kann der Anbieter Low-Level- und Hardwaredaten einschränken. Die verfügbaren Entitäten hängen von API-Zugriff und Berechtigungen ab.

Weiter: [04. FAQ und Fehlerbehebung](04-faq.md)
