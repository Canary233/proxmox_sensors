# 🌡️ Шаг 1: Аппаратные датчики и Sidecar

Руководство подготавливает узел Proxmox VE к чтению аппаратных данных, которых нет в стандартном API Proxmox. V5 использует sidecar для температур, памяти, mounts и SMART и добавляет **Sidecar Status**.

## 1. Установить пакеты
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Обнаружить датчики
```bash
sensors-detect
```
Следуйте мастеру и включите подходящие модули. Если предлагается запись в `/etc/modules`, сохраните необходимые модули для загрузки после перезапуска.

## 3. Проверить
```bash
sensors
```
Для Intel с `coretemp`, если требуется:
```bash
modprobe coretemp
sensors
```
Не используйте `coretemp` принудительно на системах с другим драйвером.

## 4. Установить sidecar
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```
Создайте systemd-службу для `/usr/bin/python3 /usr/local/bin/pve-sensors-api.py` с автоматическим перезапуском, затем:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. Проверить sidecar
`systemctl status pve-sensors.service`, затем `http://IP_PROXMOX:9000/sensors`. JSON-ответ подтверждает работу.

## 6. При сбое
V5 по возможности сохраняет последние корректные аппаратные значения. **Sidecar Status** показывает Memory, Mounts, Sensors и SMART как `ok`, `degraded`, `error` или `unknown`.

Далее: [02. Пользователь и права Proxmox](02-proxmox-config.md)
