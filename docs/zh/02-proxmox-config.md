# 🔐 第 2 步：Proxmox 用户与权限

尽可能使用专用 Home Assistant 账户，而不是 `root`。所需权限取决于功能：仅监控、guest 控制、备份或 PBS 维护。

## 1. 身份验证
**PVE：** 用户名 + 密码或 API Token；专用账户推荐使用 token。

**PBS：** 当前 V5 配置流程使用 API Token，需要 User、Token ID 和 Token Secret。

## 2. 创建用户
PVE：**Datacenter → Permissions → Users**，例如 `homeassistant@pve`。PBS 需要单独创建用户并使用正确 realm；PVE 与 PBS 是独立的身份验证系统。

## 3. 权限
对于完整功能，项目文档传统上使用 PVE 的 `/` 路径 **PVEAdmin** 角色，以及 PBS 的 `/` 路径 **Administrator** 角色。这些权限较广。如果使用限制更严格的角色，请测试 VM/CT 控制、备份、cluster/tasks、storage、PVE 复制以及 PBS GC/Prune/Verify/Sync。

## 4. API Token
PVE：**Datacenter → Permissions → API Tokens**。例如创建 `ha-token` 并立即安全保存 secret。启用 **Privilege Separation** 时，token 可能需要额外的显式权限。

## 5. Home Assistant 字段
- **User：** 完整用户和 realm，例如 `homeassistant@pve`
- **Token ID：** 仅 token 名称，例如 `ha-token`
- **Token Secret：** 生成的 secret

下一步：[03. Home Assistant 配置](03-login-pve-pbs.md)
