# 🔐 Schritt 2: Proxmox-Benutzer und Berechtigungen

Verwende nach Möglichkeit ein eigenes Home-Assistant-Konto statt `root`. Die benötigten Rechte hängen davon ab, ob nur überwacht oder auch Guests, Backups und PBS-Wartung gesteuert werden sollen.

## 1. Authentifizierung
**PVE:** Benutzer + Passwort oder API Token. Für ein dediziertes Konto wird ein API Token empfohlen.

**PBS:** Der aktuelle V5-Konfigurationsfluss verwendet API-Token-Authentifizierung mit User, Token ID und Token Secret.

## 2. Benutzer anlegen
In PVE: **Datacenter → Permissions → Users**, z. B. `homeassistant@pve`. Für PBS muss ein eigener PBS-Benutzer mit dem korrekten Realm angelegt werden. PVE- und PBS-Benutzer sind nicht automatisch identisch.

## 3. Rechte
Für eine Installation mit vollem Funktionsumfang verwendet die Projektdokumentation traditionell **PVEAdmin** auf `/` für PVE und **Administrator** auf `/` für PBS. Das sind weitreichende Rollen. Bei restriktiveren Rollen müssen insbesondere VM/CT-Steuerung, Backups, Cluster/Tasks, Storage, PVE-Replikation sowie PBS GC/Prune/Verify/Sync getestet werden.

V5 kann eine Verbindung mit Mindestzugriff erkennen, auch wenn optionale Endpoints wegen eingeschränkter Rechte fehlen.

## 4. API Token
In PVE: **Datacenter → Permissions → API Tokens**. Erstelle z. B. `ha-token` und speichere das Secret sofort sicher.

Bei aktivierter **Privilege Separation** kann der Token zusätzlich zu den Benutzerrechten eigene explizite Berechtigungen benötigen.

## 5. Werte in Home Assistant
- **User:** vollständiger Benutzer mit Realm, z. B. `homeassistant@pve`
- **Token ID:** nur der Tokenname, z. B. `ha-token`
- **Token Secret:** erzeugtes Secret

Nicht die kombinierte Proxmox-Token-Zeichenfolge in Token ID eintragen.

Weiter: [03. Home-Assistant-Einrichtung](03-login-pve-pbs.md)
