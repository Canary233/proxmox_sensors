# 🌡️ Paso 1: Configuración de sensores de hardware y Sidecar

Esta guía prepara un nodo Proxmox VE para que **Proxmox Extended Sensors V5** pueda leer información de hardware que no está disponible a través de la API estándar de Proxmox.

El sidecar de hardware se utiliza para obtener datos como temperaturas, información de memoria, discos montados y detalles SMART. V5 también expone una entidad de diagnóstico **Sidecar Status** para que Home Assistant pueda informar del estado de estos endpoints.

---

## 1. Instalar los paquetes necesarios

Instala las utilidades de hardware y SMART en el host Proxmox:

```bash
apt update && apt install lm-sensors smartmontools -y
```

- **lm-sensors** → CPU, placa base, chipset, VRM, ventiladores y otros sensores compatibles
- **smartmontools** → información SMART de HDD, SSD y dispositivos NVMe compatibles

---

## 2. Detectar los sensores de hardware

Ejecuta:

```bash
sensors-detect
```

Sigue el asistente y habilita los módulos adecuados para tu hardware.

> [!CAUTION]
> Al finalizar `sensors-detect`, lee atentamente la pregunta. Si te pide guardar los módulos detectados en `/etc/modules`, asegúrate de guardar los necesarios para que también se carguen después de reiniciar.

---

## 3. Verificar `lm-sensors`

Ejecuta:

```bash
sensors
```

Deberías ver los sensores expuestos por tu hardware y los controladores del kernel.

Si tu sistema Intel utiliza `coretemp` y no se ha cargado automáticamente, puedes probarlo con:

```bash
modprobe coretemp
sensors
```

No fuerces `coretemp` en sistemas que utilicen otro controlador de sensores de hardware.

---

## 4. Instalar el sidecar Proxmox Sensors

La API estándar de Proxmox no expone toda la información de hardware utilizada por la integración, por lo que V5 utiliza el servicio sidecar del proyecto.

Descarga el script:

```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```

Crea el servicio systemd:

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
```

Actívalo e inícialo:

```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

---

## 5. Verificar el sidecar

Comprueba el servicio:

```bash
systemctl status pve-sensors.service
```

Después abre:

```text
http://IP_DE_TU_PROXMOX:9000/sensors
```

Si el endpoint devuelve datos JSON, el sidecar está respondiendo correctamente.

---

## 6. Qué hace V5 si falla el sidecar

Un fallo temporal del sidecar no provoca que desaparezcan inmediatamente todas las entidades de hardware que anteriormente tenían datos válidos.

V5 conserva, cuando es posible, los últimos datos de hardware válidos y expone un sensor **Sidecar Status** por cada nodo PVE con el estado de:

- Memoria
- Montajes
- Sensores
- SMART

Los estados habituales de Sidecar Status son:

- `ok`
- `degraded`
- `error`
- `unknown`

---

## ✔ Conclusión

Cuando `lm-sensors`, el soporte SMART y `pve-sensors.service` estén funcionando, Home Assistant podrá obtener la información adicional de hardware compatible con tu host Proxmox.

Siguiente: [02. Usuario y permisos de Proxmox](02-proxmox-config.md)
