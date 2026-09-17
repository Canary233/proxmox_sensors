# 🔐 Step 2: Proxmox User and Permission Configuration

For Home Assistant to communicate with Proxmox, use a dedicated account instead of the root account whenever possible.

The exact permissions you grant should match the features you intend to use. Monitoring-only access can be more restrictive, while guest control, backups and PBS maintenance actions require broader privileges.

---

## 1. PVE and PBS authentication

### 🖥️ Proxmox VE (PVE)

V5 supports:

- Username + password
- API Token

API Token authentication is recommended for a dedicated Home Assistant account.

### 🗄️ Proxmox Backup Server (PBS)

The current V5 configuration flow uses **API Token authentication for PBS**.

The setup form requires:

- User
- Token ID
- Token Secret

---

## 2. Create a dedicated user

Create a dedicated Home Assistant user on the Proxmox server you are configuring.

For PVE, this is normally done from:

**Datacenter → Permissions → Users**

A typical example is:

```text
homeassistant@pve
```

For PBS, create the corresponding user in PBS and use the correct PBS realm for that account.

> Do not assume that a PVE user automatically exists on PBS. PVE and PBS are separate authentication systems.

---

## 3. Assign permissions

The integration can expose monitoring, control, backup and maintenance features, so the required privilege set depends on what you want Home Assistant to do.

For a full-feature PVE installation, the existing documentation has traditionally used a dedicated user with the **PVEAdmin** role at `/`.

For a full-feature PBS installation, the existing documentation has traditionally used a dedicated user with the **Administrator** role at `/`.

These are broad roles. If you intentionally build a more restrictive role, test all functions you plan to use, especially:

- VM and CT control
- backup services
- cluster and task visibility
- storage information
- PVE replication information
- PBS GC, Prune, Verify and Sync actions

V5 can detect when the connection has minimum access but lacks some optional endpoints and may mark the connection as having limited permissions.

---

## 4. Create an API Token

For PVE, go to:

**Datacenter → Permissions → API Tokens**

Select the dedicated user and create a token, for example:

```text
ha-token
```

When the token is created, save the secret immediately.

> [!WARNING]
> The token secret is sensitive. Store it securely and do not publish it in screenshots, logs or issues.

### Privilege Separation

If you want the token to inherit the permissions of its parent user, configure **Privilege Separation** accordingly in Proxmox.

A token with privilege separation enabled can require explicit token permissions in addition to the user permissions. If those permissions are missing, some integration features can fail with permission errors.

---

## 5. Values required by Home Assistant

When using token authentication, V5 expects:

- **User** → complete user including realm, for example `homeassistant@pve`
- **Token ID** → token name only, for example `ha-token`
- **Token Secret** → the generated secret

Do not enter the combined Proxmox API-token string in the Token ID field.

---

## ✔ Conclusion

You should now have:

- a dedicated PVE and/or PBS user
- the permissions required for the features you need
- an API Token and secret

Next: [03. Home Assistant Setup — PVE, PBS and CLUSTER](03-login-pve-pbs.md)
