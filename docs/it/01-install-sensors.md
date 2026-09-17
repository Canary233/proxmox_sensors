# 🌡️ Passo 1: Sensori hardware e Sidecar

Questa guida prepara un nodo Proxmox VE per i dati hardware non esposti dalla normale API Proxmox. V5 usa il sidecar per temperature, memoria, mount e SMART e aggiunge **Sidecar Status**.

## 1. Installa i pacchetti
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Rileva i sensori
```bash
sensors-detect
```
Segui la procedura e abilita i moduli adatti all'hardware. Se viene proposto di salvarli in `/etc/modules`, assicurati che quelli necessari siano persistenti dopo il riavvio.

## 3. Verifica
```bash
sensors
```
Su Intel con `coretemp`, se necessario:
```bash
modprobe coretemp
sensors
```
Non forzare `coretemp` su sistemi che usano un driver diverso.

## 4. Installa il sidecar
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

## 5. Verifica il sidecar
Esegui `systemctl status pve-sensors.service` e apri `http://IP_DEL_TUO_PROXMOX:9000/sensors`. Una risposta JSON conferma il funzionamento.

## 6. Guasto del sidecar
V5 conserva quando possibile gli ultimi valori hardware validi. **Sidecar Status** mostra Memory, Mounts, Sensors e SMART come `ok`, `degraded`, `error` o `unknown`.

Avanti: [02. Utente e permessi Proxmox](02-proxmox-config.md)
