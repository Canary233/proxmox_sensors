# 📚 Proxmox Extended Sensors V5 — 文档

本文档介绍 **Proxmox Extended Sensors V5** 的安装、Proxmox 准备、身份验证、Home Assistant 配置、硬件监控和故障排除。

## 指南
- 🌡️ [01. 硬件传感器与 Sidecar](01-install-sensors.md)
- 🔐 [02. Proxmox 用户与权限](02-proxmox-config.md)
- 🔌 [03. Home Assistant 配置 — PVE、PBS 和 CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ 与故障排除](04-faq.md)

[⬅ 返回主 README](../../README.md)

---

## 🚀 V5 新功能

### 🔄 可安全迁移的 VM/LXC 身份
VM 和 LXC 实体以集群范围进行跟踪。Guest 在 Proxmox 节点间迁移时，V5 旨在保留 `unique_id`、`entity_id`、历史记录、统计信息、dashboard、自动化和 guest 控制。

### 🛡️ 局部故障容错
PVE、PBS 和 CLUSTER 数据按独立部分刷新。某个 API 区域暂时失败时，无关数据仍可继续更新，并尽可能保留受影响部分最后一次有效值。

### 🔁 原生 PVE 复制监控
V5 增加集群级复制状态以及每个 job 的 **持续时间**、**上次复制** 和 **下次复制** 实体。Guest 迁移后 job 身份保持稳定。

### 🗄️ PBS 维护

PBS 维护操作包括：

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune、Verify 和 Sync 执行 PBS 中配置的 Jobs。Garbage Collection (GC) 直接在 datastore 上执行。**

从 Home Assistant 启动的操作会与 PBS 任务的精确 UPID 关联，从而可以跟踪其从开始到完成的真实状态。

### 🧩 Multi-PBS、❤️ Sidecar Status 与 📊 百分比
多个 PBS 服务器使用持久身份。Sidecar Status 汇总每个 PVE 节点的 Memory、Mounts、Sensors 和 SMART 状态。V5 增加 CT 内存百分比、CT 磁盘百分比和 VM 内存百分比。由于缺少足够可靠的数据源，不提供 VM 磁盘百分比。

---

## 🎨 动态 Proxmox Dashboard
V5 提供可选的 **PVE、PBS 和 CLUSTER** Lovelace dashboard，并根据 Home Assistant 中实际存在的资源生成。

### 要求
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### 安装
1. 通过 HACS 安装 Card Mod。
2. 将 `/proxmox_sensors/proxmox-dashboard.js` 添加为 Lovelace **JavaScript Module**。
3. 重新加载浏览器。
4. 创建 dashboard，并选择 **Proxmox Extended Sensors** community strategy。
5. 从可用类型中选择 **PVE**、**PBS** 或 **CLUSTER**。

使用 **Take Control** 后，可以像普通 Lovelace dashboard 一样编辑。Dashboard 完全可选。

---

## 🌐 监控、备份与 PBS
根据可用数据，V5 可显示节点、quorum、CPU/RAM/load/I/O wait、RX/TX、KSM、storages、mounts、物理磁盘、SMART、温度、VM、LXC、失败任务、备份健康状态和 PVE 复制。

`create_vzdump_backup` 和 `backup_all` 使用 Proxmox 原生备份机制。PBS 监控包括 datastore 使用情况、备份、去重、任务和维护，并将操作与真实 PBS 任务关联。

---

## 🧩 安装
### 通过 HACS — 推荐
[![在 HACS 中打开 Proxmox Extended Sensors。](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors 已包含在默认 HACS 仓库中，无需添加自定义仓库。**

1. 打开 **HACS → Integrations**。
2. 搜索 **Proxmox Extended Sensors** 并下载。
3. 重启 Home Assistant。
4. 前往 **Settings → Devices & Services → Add Integration** 并搜索该集成。

手动安装：复制到 `/config/custom_components/proxmox_sensors`，然后重启 Home Assistant。

---

## 🧩 支持的环境
项目支持现代 Proxmox VE、Proxmox Backup Server 和 Home Assistant 环境。发布前应根据当前 release notes 确认准确的最低版本要求。

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
