# ❓ FAQ — Proxmox Extended Sensors V5

Esta página recoge las preguntas más habituales de configuración y solución de problemas de **Proxmox Extended Sensors V5**.

---

## 🔐 Problemas de conexión

### No puedo conectar

Comprueba primero lo básico: que Proxmox sea accesible desde Home Assistant, usuario y realm, token y Token Secret, permisos API y configuración SSL. Para configurar el token, consulta [02. Usuario y permisos de Proxmox](02-proxmox-config.md).

### Obtengo `Permission denied`

Normalmente significa que las credenciales son válidas, pero la cuenta o el token no pueden acceder a uno o varios endpoints necesarios. Comprueba permisos del usuario padre, permisos del token / Privilege Separation y permisos asignados en la ruta necesaria.

---

## 🌡️ Hardware y Sidecar

### No aparecen las temperaturas

Comprueba `sensors`, después `systemctl status pve-sensors.service` y finalmente `http://IP_DE_TU_PROXMOX:9000/sensors`. Consulta [01. Configuración de sensores de hardware y Sidecar](01-install-sensors.md).

### ¿Qué significa `Sidecar Status`?

V5 expone un sensor de diagnóstico Sidecar Status por nodo PVE que resume Memoria, Montajes, Sensores y SMART (`ok`, `degraded`, `error`, `unknown`). Cuando es posible, V5 conserva los últimos valores válidos durante un fallo del sidecar.

### Faltan algunos sensores SMART o de temperatura

La integración solo puede exponer los valores disponibles a través del hardware, controladores, `lm-sensors`, herramientas SMART y sidecar. Puede ser normal que falten métricas según el hardware o la virtualización.

---

## 🖥️ Máquinas virtuales y contenedores LXC

### ¿Qué ocurre cuando una VM o CT migra a otro nodo?

V5 utiliza una identidad de guest a nivel de clúster para conservar `unique_id`, `entity_id`, historial, estadísticas, automatizaciones y dashboards. Inmediatamente después de una migración, el dispositivo del nodo de origen puede permanecer temporalmente vacío mientras termina la reconciliación.

### ¿Por qué no existe un sensor de porcentaje de disco de VM?

V5 no lo expone porque los datos disponibles de Proxmox no proporcionan una métrica suficientemente fiable. El porcentaje de disco de CT sí está disponible cuando existen los datos necesarios.

---

## 🔁 Replicación PVE

### ¿Dónde aparece la información de replicación?

V5 expone estado a nivel de clúster y entidades por job asociadas al guest: Duración, Última replicación y Próxima replicación. La identidad del job se basa en el job de Proxmox, no en el nodo físico.

### ¿Un error de API significa automáticamente que la replicación ha fallado?

No. V5 mantiene separados el inventario de replicación y la información de ejecución. Un fallo temporal de API/runtime no se interpreta automáticamente como un fallo real del job.

---

## 🗄️ Proxmox Backup Server

### ¿Qué acciones de mantenimiento PBS son compatibles?

V5 admite Garbage Collection (GC), Prune, Verify y Sync.

> **Cambio de seguridad en V5:** a diferencia de V4.x, **Prune, Verify y Sync ya no se ejecutan como operaciones directas construidas por la integración**. V5 ejecuta el **Job correspondiente previamente configurado por el administrador en PBS**. Así la operación queda bajo las políticas de PBS y, especialmente en Prune, se respetan las reglas de retención configuradas que determinan qué backups pueden eliminarse.

**GC se mantiene intencionadamente como acción directa sobre el datastore.** Garbage Collection recupera espacio no referenciado y resulta útil para automatizaciones de Home Assistant, por ejemplo cuando queda poco espacio libre en la unidad de backups.

Las acciones iniciadas desde Home Assistant se siguen mediante el UPID de la tarea PBS para conocer su resultado real.

### ¿Por qué Prune, Verify o Sync devuelve un error?

Cada acción necesita que exista en PBS su Job correspondiente. Antes de utilizarla desde Home Assistant debes configurar el **Prune Job, Verify Job o Sync Job** apropiado en Proxmox Backup Server.

Si no existe un Job compatible, **la integración devuelve un error y no intenta realizar la operación directamente como alternativa**. Es un comportamiento de seguridad intencionado, no un fallo de la integración.

### ¿Por qué no está disponible Sync?

Sync necesita un Sync Job configurado en PBS. Si no existe, la integración no tiene ningún job que ejecutar y mostrará un error en lugar de intentar una operación alternativa.

### ¿Puedo añadir más de un servidor PBS?

Sí. V5 asigna identidades PBS persistentes para que acciones, datastores y estados de mantenimiento permanezcan asociados a la instancia correcta.

### Un PBS alojado o gestionado muestra menos entidades

Los proveedores pueden restringir información de hardware o de nivel de nodo. Las entidades disponibles dependen del acceso API y de los permisos expuestos a tu cuenta.

---

## 🛡️ Fallos parciales y conservación de valores

Un valor anterior durante un problema de API puede ser intencionado. V5 actualiza secciones de forma independiente y conserva cuando es posible los últimos datos válidos hasta recuperar datos nuevos.

---

## 🎨 Dashboard dinámico de Proxmox

El dashboard es opcional. Necesita V5, Card Mod y `/proxmox_sensors/proxmox-dashboard.js`. Con **Tomar el control (Take Control)** puede personalizarse como cualquier Lovelace normal.

---

## 🔄 Actualizaciones y rendimiento

La integración utiliza actualizaciones asíncronas coordinadas y concurrencia controlada. No te bases en un intervalo fijo antiguo de versiones anteriores.

---

## 🧾 Antes de abrir un issue

Comprueba conectividad, credenciales, token, permisos, reinicio de Home Assistant, sidecar si afecta al hardware y logs. **Si el problema es Prune, Verify o Sync, comprueba también que exista y esté correctamente configurado el Job PBS correspondiente.**

Elimina contraseñas, Token Secrets y otras credenciales de capturas y logs.

---

## Limitaciones conocidas

- El porcentaje de disco de VM no se expone porque no existe una métrica suficientemente fiable.
- Los entornos PBS alojados pueden exponer menos información.
- Los datos de hardware dependen del host, controladores y sidecar.
- Tras una migración VM/LXC, el dispositivo del nodo de origen puede permanecer temporalmente vacío.

---

[⬅ Volver a la documentación V5](README.md)
