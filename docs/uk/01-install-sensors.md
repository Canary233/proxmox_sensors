# 🌡️ Крок 1: Апаратні датчики та Sidecar

Посібник готує вузол Proxmox VE до апаратних даних, яких немає у стандартному API Proxmox. V5 використовує sidecar для температур, пам'яті, mounts і SMART та додає **Sidecar Status**.

## 1. Встановити пакети
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Виявити датчики
```bash
sensors-detect
```
Дотримуйтесь майстра та активуйте відповідні модулі. Якщо пропонується запис до `/etc/modules`, збережіть необхідні модулі для завантаження після перезапуску.

## 3. Перевірити
```bash
sensors
```
Для Intel із `coretemp`, якщо потрібно:
```bash
modprobe coretemp
sensors
```
Не використовуйте `coretemp` примусово на системах з іншим драйвером.

## 4. Встановити sidecar
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```
Створіть systemd-сервіс для `/usr/bin/python3 /usr/local/bin/pve-sensors-api.py` з автоматичним перезапуском, потім:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. Перевірити sidecar
`systemctl status pve-sensors.service`, потім `http://IP_PROXMOX:9000/sensors`. JSON-відповідь підтверджує роботу.

## 6. При збої
V5 за можливості зберігає останні коректні апаратні значення. **Sidecar Status** показує Memory, Mounts, Sensors і SMART як `ok`, `degraded`, `error` або `unknown`.

Далі: [02. Користувач і дозволи Proxmox](02-proxmox-config.md)
