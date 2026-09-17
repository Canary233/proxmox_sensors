# 🌡️ Stap 1: Hardwaresensoren en Sidecar

Deze handleiding bereidt een Proxmox VE-node voor op hardwaredata die niet via de standaard Proxmox-API beschikbaar is. V5 gebruikt de sidecar voor temperaturen, geheugen, mounts en SMART en voegt **Sidecar Status** toe.

## 1. Pakketten installeren
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Sensoren detecteren
```bash
sensors-detect
```
Volg de wizard en activeer passende modules. Als `/etc/modules` wordt aangeboden, zorg dat benodigde modules na reboot blijven laden.

## 3. Controleren
```bash
sensors
```
Voor Intel met `coretemp`, indien nodig:
```bash
modprobe coretemp
sensors
```
Forceer `coretemp` niet op systemen met een andere driver.

## 4. Sidecar installeren
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```
Maak `/etc/systemd/system/pve-sensors.service` met `ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py`, `Restart=always`, `RestartSec=10s`, `NoNewPrivileges=yes`, `PrivateTmp=yes` en `ProtectSystem=full`, en activeer daarna:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. Controleren
`systemctl status pve-sensors.service` en daarna `http://JOUW_PROXMOX_IP:9000/sensors`. JSON bevestigt dat de sidecar reageert.

## 6. Bij storing
V5 bewaart waar mogelijk de laatste geldige hardwarewaarden. **Sidecar Status** toont Memory, Mounts, Sensors en SMART als `ok`, `degraded`, `error` of `unknown`.

Volgende: [02. Proxmox-gebruiker en rechten](02-proxmox-config.md)
