# 🌡️ Étape 1 : Capteurs matériels et Sidecar

Cette procédure prépare un nœud Proxmox VE pour les données matérielles non exposées par l'API Proxmox standard. V5 utilise le sidecar pour les températures, la mémoire, les montages et SMART, et expose **Sidecar Status**.

## 1. Installer les paquets
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Détecter les capteurs
```bash
sensors-detect
```
Suivez l'assistant et activez les modules adaptés au matériel. Si l'assistant propose d'ajouter les modules à `/etc/modules`, enregistrez ceux nécessaires au redémarrage.

## 3. Vérifier
```bash
sensors
```
Pour un système Intel utilisant `coretemp`, si nécessaire :
```bash
modprobe coretemp
sensors
```
Ne forcez pas `coretemp` sur un système utilisant un autre pilote.

## 4. Installer le sidecar
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

## 5. Vérifier le sidecar
`systemctl status pve-sensors.service`, puis ouvrir `http://IP_DE_VOTRE_PROXMOX:9000/sensors`. Une réponse JSON confirme son fonctionnement.

## 6. En cas de panne
V5 conserve si possible les dernières valeurs matérielles valides. **Sidecar Status** indique l'état de Memory, Mounts, Sensors et SMART : `ok`, `degraded`, `error` ou `unknown`.

Suivant : [02. Utilisateur et permissions Proxmox](02-proxmox-config.md)
