# 🔐 Paso 2: Configuración de usuario y permisos de Proxmox

Para que Home Assistant se comunique con Proxmox, utiliza siempre que sea posible una cuenta dedicada en lugar del usuario root.

Los permisos exactos deben corresponder a las funciones que quieras utilizar. Un acceso únicamente de monitorización puede ser más restrictivo, mientras que el control de guests, los backups y las acciones de mantenimiento PBS requieren privilegios más amplios.

---

## 1. Autenticación PVE y PBS

### 🖥️ Proxmox VE (PVE)

V5 admite:

- Usuario + contraseña
- API Token

Para una cuenta dedicada a Home Assistant se recomienda utilizar API Token.

### 🗄️ Proxmox Backup Server (PBS)

El flujo de configuración actual de V5 utiliza **autenticación mediante API Token para PBS**.

El formulario solicita:

- Usuario
- Token ID
- Token Secret

---

## 2. Crear un usuario dedicado

Crea un usuario específico para Home Assistant en el servidor Proxmox que estés configurando.

En PVE normalmente se realiza desde:

**Datacenter → Permissions → Users**

Un ejemplo habitual es:

```text
homeassistant@pve
```

Para PBS, crea el usuario correspondiente en PBS y utiliza el realm correcto de esa cuenta.

> No des por hecho que un usuario de PVE existe automáticamente en PBS. PVE y PBS utilizan sistemas de autenticación independientes.

---

## 3. Asignar permisos

La integración puede ofrecer monitorización, control, backups y acciones de mantenimiento, por lo que el conjunto de privilegios necesario depende de lo que quieras permitir desde Home Assistant.

Para una instalación PVE con todas las funciones, la documentación del proyecto ha utilizado tradicionalmente un usuario dedicado con el rol **PVEAdmin** en `/`.

Para una instalación PBS con todas las funciones, la documentación ha utilizado tradicionalmente un usuario dedicado con el rol **Administrator** en `/`.

Son roles amplios. Si decides crear un rol más restrictivo, comprueba todas las funciones que quieras utilizar, especialmente:

- control de VM y CT
- servicios de backup
- visibilidad del clúster y de las tareas
- información de almacenamiento
- información de replicación PVE
- acciones PBS de GC, Prune, Verify y Sync

V5 puede detectar que una conexión dispone del acceso mínimo pero carece de algunos endpoints opcionales y marcarla como conexión con permisos limitados.

---

## 4. Crear un API Token

En PVE, ve a:

**Datacenter → Permissions → API Tokens**

Selecciona el usuario dedicado y crea un token, por ejemplo:

```text
ha-token
```

Guarda el secret en cuanto se cree el token.

> [!WARNING]
> El secret del token es información sensible. Guárdalo de forma segura y no lo publiques en capturas, logs o issues.

### Privilege Separation

Si quieres que el token herede los permisos de su usuario padre, configura **Privilege Separation** de forma adecuada en Proxmox.

Con Privilege Separation activado, el token puede necesitar permisos explícitos adicionales a los del usuario. Si faltan, algunas funciones de la integración pueden producir errores de permisos.

---

## 5. Valores requeridos por Home Assistant

Al utilizar autenticación mediante token, V5 espera:

- **User** → usuario completo incluyendo realm, por ejemplo `homeassistant@pve`
- **Token ID** → solo el nombre del token, por ejemplo `ha-token`
- **Token Secret** → el secret generado

No introduzcas la cadena completa combinada del API Token de Proxmox en el campo Token ID.

---

## ✔ Conclusión

Ahora deberías tener:

- un usuario dedicado PVE y/o PBS
- los permisos necesarios para las funciones que quieras utilizar
- un API Token y su secret

Siguiente: [03. Configuración en Home Assistant — PVE, PBS y CLUSTER](03-login-pve-pbs.md)
