# 🌡️ Schritt 1: Hardware-Sensoren und Sidecar

Diese Anleitung bereitet einen Proxmox-VE-Knoten für Hardwaredaten vor, die nicht über die Standard-Proxmox-API verfügbar sind. V5 nutzt den Sidecar unter anderem für Temperaturen, Speicherinformationen, Mounts und SMART und stellt zusätzlich **Sidecar Status** bereit.

## 1. Pakete installieren
```bash
apt update && apt install lm-sensors smartmontools -y
```
`lm-sensors` liefert unterstützte CPU-, Mainboard-, Chipsatz-, VRM- und Lüfterdaten; `smartmontools` SMART-Daten für HDD, SSD und unterstützte NVMe-Geräte.

## 2. Sensoren erkennen
```bash
sensors-detect
```
Folge dem Assistenten und aktiviere die für deine Hardware passenden Module. Werden Einträge für `/etc/modules` angeboten, stelle sicher, dass die benötigten Module für Neustarts gespeichert werden.

## 3. Prüfen
```bash
sensors
```
Bei Intel-Systemen mit `coretemp` kann bei Bedarf getestet werden:
```bash
modprobe coretemp
sensors
```
`coretemp` nicht auf Systemen erzwingen, die einen anderen Treiber verwenden.

## 4. Sidecar installieren
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```

```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API (User Mode)
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always
RestartSec=10s
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=full

[Install]
WantedBy=default.target
EOF
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. Sidecar prüfen
```bash
systemctl status pve-sensors.service
```
Öffne anschließend `http://DEINE_PROXMOX_IP:9000/sensors`. Eine JSON-Antwort bestätigt, dass der Sidecar reagiert.

## 6. Verhalten bei Sidecar-Ausfall
V5 behält nach Möglichkeit die letzten gültigen Hardwarewerte. **Sidecar Status** zeigt pro PVE-Knoten den Zustand von Memory, Mounts, Sensors und SMART als `ok`, `degraded`, `error` oder `unknown`.

Weiter: [02. Proxmox-Benutzer und Berechtigungen](02-proxmox-config.md)
