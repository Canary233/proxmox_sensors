# 📚 Proxmox Extended Sensors V5 — Documentación

Esta documentación cubre la instalación, preparación de Proxmox, autenticación, configuración de Home Assistant, monitorización de hardware y solución de problemas de **Proxmox Extended Sensors V5**.

## Guías

- 🌡️ [01. Configuración de sensores de hardware](01-install-sensors.md)
- 🔐 [02. Usuario y permisos de Proxmox](02-proxmox-config.md)
- 🔌 [03. Configuración en Home Assistant — PVE, PBS y CLUSTER](03-login-pve-pbs.md)
- ❓ [04. Preguntas frecuentes y solución de problemas](04-faq.md)

[⬅ Volver al README principal](../../README.md)

---

## 🚀 Novedades de V5

V5 mantiene las funciones de monitorización y control de versiones anteriores e introduce una arquitectura más resistente y una identidad estable de las entidades durante operaciones reales de Proxmox.

### 🔄 Identidad de VM y LXC resistente a migraciones

Las entidades de VM y LXC se identifican a nivel de clúster. Cuando un guest migra entre nodos Proxmox, Home Assistant mantiene la misma identidad lógica en lugar de crear entidades nuevas.

Esto está diseñado para conservar:

- `unique_id`
- `entity_id`
- historial y estadísticas
- dashboards
- automatizaciones
- controles del guest

### 🛡️ Resistencia a fallos parciales

Los datos de PVE, PBS y CLUSTER se actualizan en secciones independientes. Si una parte de la API falla temporalmente, los datos no relacionados pueden seguir actualizándose y, cuando es posible, se conservan los últimos valores válidos de la sección afectada.

### 🔁 Monitorización nativa de replicación PVE

V5 añade estado global de replicación a nivel de clúster y entidades por job como:

- Duración
- Última replicación
- Próxima replicación

La identidad del job de replicación permanece estable aunque el guest migre a otro nodo.

### 🗄️ Monitorización ampliada del mantenimiento PBS

Las acciones de mantenimiento PBS incluyen:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify y Sync ejecutan los Jobs configurados en PBS. Garbage Collection (GC) se ejecuta directamente sobre el datastore.**

Las acciones iniciadas desde Home Assistant se correlacionan con el UPID exacto de la tarea PBS, permitiendo seguir su estado real desde el inicio hasta su finalización.

### 🧩 Identidad multi-PBS

Pueden coexistir varios servidores PBS sin mezclar estados de mantenimiento ni acciones de datastore. V5 asigna identidades persistentes a los servidores PBS y los mantiene aislados dentro de Home Assistant.

### ❤️ Sidecar Status

Cada nodo PVE expone un sensor de diagnóstico **Sidecar Status** que resume el estado de los endpoints del sidecar utilizados para:

- Memoria
- Montajes
- Sensores
- SMART

### 📊 Nuevos sensores porcentuales

V5 añade:

- Porcentaje de memoria de CT
- Porcentaje de disco de CT
- Porcentaje de memoria de VM

El porcentaje de disco de VM no se expone porque actualmente no existe una métrica de origen suficientemente fiable.

---

## 🎨 Dashboard dinámico de Proxmox

V5 incluye un sistema opcional de dashboards Lovelace para **PVE, PBS y CLUSTER**.

El dashboard se genera a partir de las entidades y recursos realmente disponibles en tu instalación de Home Assistant, por lo que no se ofrecen dashboards vacíos para tipos de servidor que no estén presentes.

### Requisitos

- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Instalación del dashboard

1. Instala **Card Mod** desde HACS si todavía no lo tienes.
2. Añade este recurso Lovelace como **Módulo JavaScript**:

   ```text
   /proxmox_sensors/proxmox-dashboard.js
   ```

3. Recarga el navegador.
4. Crea un nuevo dashboard y selecciona la estrategia de comunidad **Proxmox Extended Sensors**.
5. Elige uno de los tipos disponibles para tu instalación: **PVE**, **PBS** o **CLUSTER**.

El dashboard seguirá siendo gestionado por la estrategia hasta que utilices la opción **Tomar el control (Take Control)** de Home Assistant. Después podrás editarlo como cualquier dashboard Lovelace normal.

> El dashboard es opcional. La integración funciona normalmente sin instalarlo.

---

## 🌐 Monitorización PVE y CLUSTER

Dependiendo del tipo de servidor configurado y de los datos disponibles, la integración puede exponer información de:

- nodos Proxmox
- salud y quórum del clúster
- CPU, RAM, carga e I/O wait
- red RX/TX
- KSM
- storages y discos montados
- discos físicos y SMART
- temperaturas de hardware
- máquinas virtuales
- contenedores LXC
- tareas fallidas
- jobs de backup y salud de backups
- replicación PVE

---

## 🖥️ Máquinas virtuales y contenedores

Los dispositivos VM y LXC pueden exponer estado, uptime, CPU, memoria, tráfico de red y otra información del guest disponible a través de Proxmox.

V5 también controla el estado esperado de arranque (`onboot`) y mantiene estable la identidad del guest durante las migraciones entre nodos.

Los controles de guest se exponen como entidades de botón de Home Assistant cuando la acción correspondiente está disponible.

---

## 💾 Servicios de backup

La integración proporciona servicios de Home Assistant para realizar backups de guests de Proxmox VE.

### `create_vzdump_backup`

- Admite uno o varios IDs de guest.
- Utiliza la ejecución nativa de backups de Proxmox.
- Admite destinos de almacenamiento local, de red y PBS disponibles para PVE.

### `backup_all`

- Realiza backup de los guests seleccionados de un nodo.
- Admite concurrencia y retardos configurables.
- Puede utilizarse desde automatizaciones de Home Assistant.

---

## 🗄️ Proxmox Backup Server

La monitorización PBS incluye uso del datastore, información de backups, datos de deduplicación, estado de tareas e información de mantenimiento expuesta por la API de PBS.

V5 mejora el seguimiento del mantenimiento correlacionando las acciones con sus tareas PBS reales en lugar de considerar que una petición POST aceptada equivale a una tarea finalizada.

---

## 🧩 Instalación

### Mediante HACS — recomendado

[![Abre tu instancia de Home Assistant y Proxmox Extended Sensors en HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors está incluido en el repositorio predeterminado de HACS. No es necesario añadir un repositorio personalizado.**

1. Abre **HACS → Integraciones**.
2. Busca **Proxmox Extended Sensors**.
3. Descarga la integración.
4. Reinicia Home Assistant.
5. Ve a **Ajustes → Dispositivos y servicios → Añadir integración**.
6. Busca **Proxmox Extended Sensors**.

Continúa con [03. Configuración en Home Assistant — PVE, PBS y CLUSTER](03-login-pve-pbs.md).

### Instalación manual

Copia la integración en:

```text
/config/custom_components/proxmox_sensors
```

Después reinicia Home Assistant y añade la integración desde **Ajustes → Dispositivos y servicios**.

---

## 🧩 Entornos compatibles

El proyecto es compatible con instalaciones modernas de Proxmox VE, Proxmox Backup Server y Home Assistant. Las versiones mínimas exactas deberán comprobarse con las notas de la versión actual antes de la publicación.

---

## 🤝 Contribuciones y comunidad

Puedes abrir issues y pull requests en el repositorio oficial:

https://github.com/Javisen/proxmox_sensors

Si la integración te resulta útil, considera dejar una ⭐ en GitHub.

---

<p align="center"><i>Mantenido por Javisen — Licencia MIT</i></p>
