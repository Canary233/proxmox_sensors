# 🔌 Paso 3: Configuración en Home Assistant — PVE, PBS y CLUSTER

Esta guía explica cómo instalar **Proxmox Extended Sensors V5** y añadir conexiones PVE, PBS o CLUSTER a Home Assistant.

---

## 1. Instalar mediante HACS

[![Abre tu instancia de Home Assistant y Proxmox Extended Sensors en HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors está incluido en el repositorio predeterminado de HACS. No necesitas añadir ningún repositorio personalizado.**

1. Abre **HACS → Integraciones**.
2. Busca **Proxmox Extended Sensors**.
3. Descárgalo.
4. Reinicia Home Assistant.

---

## 2. Añadir la integración

Después de reiniciar Home Assistant:

1. Ve a **Ajustes → Dispositivos y servicios**.
2. Pulsa **Añadir integración**.
3. Busca **Proxmox Extended Sensors**.

La primera pantalla de configuración solicita:

- Host
- Tipo de servidor

Los tipos disponibles son:

- **PVE** — Proxmox Virtual Environment
- **PBS** — Proxmox Backup Server
- **CLUSTER** — vista del clúster Proxmox

---

## 3. Host

Introduce la dirección IP o el nombre de host del servidor, por ejemplo:

```text
192.168.1.50
```

o:

```text
pve.example.local
```

La integración gestiona internamente el esquema de conexión, por lo que normalmente debes introducir únicamente el valor de host solicitado por el formulario.

---

## 4. Autenticación

### PVE

V5 admite:

- Usuario + contraseña
- API Token

### PBS

El flujo de configuración actual de V5 utiliza **autenticación mediante API Token** para PBS.

### CLUSTER

CLUSTER utiliza su propio flujo de configuración y las credenciales configuradas para el acceso al clúster.

---

## 5. Campos del API Token

Cuando selecciones autenticación mediante token, introduce:

- **User** → usuario completo y realm, por ejemplo `homeassistant@pve`
- **Token ID** → solo el nombre del token, por ejemplo `ha-token`
- **Token Secret** → el secret generado

No introduzcas la cadena completa combinada del token en el campo Token ID.

---

## 6. Selección de nodo y recursos PVE

Después de validar una conexión PVE, la integración descubre los recursos Proxmox disponibles y continúa con su flujo de selección de nodos y recursos.

Dependiendo del entorno, puedes configurar la monitorización de recursos como:

- nodos
- VMs
- contenedores LXC
- storages
- información de hardware

V5 utiliza una identidad de VM/LXC a nivel de clúster, por lo que las entidades de guest pueden seguir las migraciones entre nodos conservando su identidad en Home Assistant.

---

## 7. Configuración PBS

Una conexión PBS crea su propia entrada de configuración en Home Assistant.

V5 asigna una identidad persistente al servidor PBS para que puedan coexistir varias instancias sin mezclar acciones de mantenimiento ni estados de datastore.

La monitorización PBS puede incluir:

- uso del datastore
- información de backups
- deduplicación
- estado de tareas
- GC
- Prune
- Verify
- Sync cuando existe un Sync Job

---

## 8. Configuración CLUSTER

El tipo de servidor CLUSTER se utiliza para entidades globales del clúster como:

- quórum y estado de nodos
- CPU y RAM agregadas
- número de VM y CT
- información de almacenamiento del clúster
- tareas fallidas
- salud de backups
- estado de replicación PVE

---

## 9. Dashboard dinámico de Proxmox opcional

V5 incluye un generador de dashboards opcional para PVE, PBS y CLUSTER.

### Requisitos

- Proxmox Extended Sensors V5
- Card Mod

### Instalación

1. Instala **Card Mod** desde HACS.
2. Añade este recurso Lovelace como **Módulo JavaScript**:

   ```text
   /proxmox_sensors/proxmox-dashboard.js
   ```

3. Recarga el navegador.
4. Crea un nuevo dashboard y elige la estrategia de comunidad **Proxmox Extended Sensors**.
5. Selecciona uno de los tipos ofrecidos para tu instalación: **PVE**, **PBS** o **CLUSTER**.

El dashboard seguirá siendo gestionado por la estrategia hasta que elijas **Tomar el control (Take Control)**. Después podrás editarlo como cualquier dashboard Lovelace normal.

---

## 10. Servicios PBS gestionados

En servicios PBS alojados o multi-tenant, el proveedor puede restringir la información de hardware o de bajo nivel del nodo.

Esto no indica necesariamente un error de la integración. Las entidades disponibles dependen de lo que el proveedor exponga mediante tu cuenta PBS y sus permisos de API.

---

## ✔ Conclusión

Tu conexión PVE, PBS y/o CLUSTER debería estar ya disponible en Home Assistant.

Siguiente: [04. Preguntas frecuentes y solución de problemas](04-faq.md)
