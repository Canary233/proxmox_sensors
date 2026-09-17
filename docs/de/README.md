# 📚 Proxmox Extended Sensors V5 — Dokumentation

Diese Dokumentation behandelt Installation, Proxmox-Vorbereitung, Authentifizierung, Home-Assistant-Einrichtung, Hardware-Monitoring und Fehlerbehebung für **Proxmox Extended Sensors V5**.

## Anleitungen

- 🌡️ [01. Hardware-Sensoren und Sidecar](01-install-sensors.md)
- 🔐 [02. Proxmox-Benutzer und Berechtigungen](02-proxmox-config.md)
- 🔌 [03. Home-Assistant-Einrichtung — PVE, PBS und CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ und Fehlerbehebung](04-faq.md)

[⬅ Zurück zum Haupt-README](../../README.md)

---

## 🚀 Neuerungen in V5

V5 behält die Monitoring- und Steuerungsfunktionen früherer Versionen bei und ergänzt eine robustere Architektur sowie stabile Entitätsidentitäten bei realen Proxmox-Vorgängen.

### 🔄 Migrationssichere VM- und LXC-Identität
VM- und LXC-Entitäten werden clusterweit verfolgt. Bei einer Migration zwischen Proxmox-Knoten bleiben `unique_id`, `entity_id`, Verlauf, Statistiken, Dashboards, Automationen und Guest-Steuerungen erhalten.

### 🛡️ Widerstandsfähigkeit bei Teilfehlern
PVE-, PBS- und CLUSTER-Daten werden in unabhängigen Bereichen aktualisiert. Fällt ein API-Bereich vorübergehend aus, können andere Daten weiter aktualisiert und die letzten gültigen Werte des betroffenen Bereichs nach Möglichkeit beibehalten werden.

### 🔁 Native PVE-Replikationsüberwachung
V5 ergänzt clusterweiten Replikationsstatus sowie Entitäten pro Job für **Dauer**, **Letzte Replikation** und **Nächste Replikation**. Die Job-Identität bleibt auch nach einer Guest-Migration stabil.

### 🗄️ Erweiterte PBS-Wartung

Die PBS-Wartungsaktionen umfassen:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify und Sync führen die in PBS konfigurierten Jobs aus. Garbage Collection (GC) wird direkt auf dem Datastore ausgeführt.**

Von Home Assistant gestartete Aktionen werden mit der exakten UPID der PBS-Aufgabe korreliert, sodass ihr tatsächlicher Status vom Start bis zum Abschluss verfolgt werden kann.

### 🧩 Multi-PBS und ❤️ Sidecar Status
Mehrere PBS-Server erhalten persistente Identitäten. Pro PVE-Knoten fasst **Sidecar Status** den Zustand von Memory, Mounts, Sensors und SMART zusammen.

### 📊 Neue Prozent-Sensoren
V5 ergänzt CT-Speicher %, CT-Datenträger % und VM-Speicher %. VM-Datenträger % wird mangels ausreichend zuverlässiger Quelldaten bewusst nicht angeboten.

---

## 🎨 Dynamisches Proxmox-Dashboard

V5 enthält ein optionales Lovelace-Dashboard-System für **PVE, PBS und CLUSTER**, das aus den tatsächlich vorhandenen Entitäten und Ressourcen erzeugt wird.

### Voraussetzungen
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Installation
1. **Card Mod** über HACS installieren.
2. `/proxmox_sensors/proxmox-dashboard.js` als **JavaScript-Modul** zu den Lovelace-Ressourcen hinzufügen.
3. Browser neu laden.
4. Neues Dashboard erstellen und die Community-Strategie **Proxmox Extended Sensors** wählen.
5. Einen angebotenen Typ auswählen: **PVE**, **PBS** oder **CLUSTER**.

Mit **Take Control** kann das erzeugte Dashboard anschließend wie ein normales Lovelace-Dashboard bearbeitet werden. Das Dashboard ist optional.

---

## 🌐 Monitoring und Steuerung

Je nach Servertyp und verfügbaren Daten kann V5 Knoten, Clusterzustand und Quorum, CPU/RAM/Load/I/O Wait, RX/TX, KSM, Storages, Mounts, physische Datenträger, SMART, Temperaturen, VMs, LXC, fehlgeschlagene Tasks, Backup-Zustand und PVE-Replikation darstellen.

VM- und LXC-Steuerungen erscheinen als Home-Assistant-Button-Entitäten, wenn die jeweilige Aktion verfügbar ist. `onboot` und der erwartete Startzustand werden ebenfalls berücksichtigt.

---

## 💾 Backup und PBS

Die Dienste `create_vzdump_backup` und `backup_all` verwenden die native Proxmox-Backup-Ausführung und unterstützen die in PVE verfügbaren lokalen, Netzwerk- und PBS-Ziele.

PBS-Monitoring umfasst Datastore-Nutzung, Backups, Deduplizierung, Tasks und Wartungsstatus. V5 korreliert Wartungsaktionen mit den realen PBS-Tasks statt einen akzeptierten POST bereits als Abschluss zu behandeln.

---

## 🧩 Installation

### Über HACS — empfohlen

[![Proxmox Extended Sensors in HACS öffnen.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors ist im Standard-HACS-Repository enthalten. Ein benutzerdefiniertes Repository ist nicht erforderlich.**

1. **HACS → Integrationen** öffnen.
2. Nach **Proxmox Extended Sensors** suchen und herunterladen.
3. Home Assistant neu starten.
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen** öffnen.
5. Nach **Proxmox Extended Sensors** suchen.

Manuell: nach `/config/custom_components/proxmox_sensors` kopieren und Home Assistant neu starten.

---

## 🧩 Unterstützte Umgebungen

Das Projekt unterstützt moderne Proxmox-VE-, Proxmox-Backup-Server- und Home-Assistant-Installationen. Die exakten Mindestversionen sollten vor Veröffentlichung mit den aktuellen Release Notes abgeglichen werden.

---

<p align="center"><i>Maintained by Javisen — MIT License</i></p>
