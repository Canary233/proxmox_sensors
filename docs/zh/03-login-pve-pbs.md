# 🔌 第 3 步：Home Assistant — PVE、PBS 和 CLUSTER

## 1. HACS
[![在 HACS 中打开。](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

集成已包含在默认 HACS 仓库中，无需 custom repository。在 **HACS → Integrations** 搜索 **Proxmox Extended Sensors**，下载后重启 Home Assistant。

## 2. 添加集成
**Settings → Devices & Services → Add Integration → Proxmox Extended Sensors**。类型：**PVE**、**PBS**、**CLUSTER**。

## 3. Host 与身份验证
输入 IP 或 hostname。PVE 支持用户/密码或 API Token；PBS 在当前 V5 流程中使用 API Token。Token 登录时填写完整 User+realm、仅 token 名称作为 Token ID，以及 Token Secret。

## 4. PVE
连接后会发现节点以及 VM、LXC、storages、hardware 等资源。V5 的 cluster-wide 身份让 VM/LXC 实体能够跟随迁移并保持 Home Assistant 身份。

## 5. PBS
每个 PBS 有独立 config entry 和持久身份。可包括 datastore、备份、去重、tasks、GC、Prune、Verify，以及存在 Sync Job 时的 Sync。

## 6. CLUSTER
包括 quorum、节点状态、聚合 CPU/RAM、VM/CT 数量、cluster storage、failed tasks、backup health 和 PVE replication。

## 7. 可选 Dashboard
安装 Card Mod，将 `/proxmox_sensors/proxmox-dashboard.js` 添加为 JavaScript Module，重新加载浏览器，并使用 **Proxmox Extended Sensors** community strategy 创建 dashboard。选择 PVE/PBS/CLUSTER。使用 **Take Control** 后可正常编辑 Lovelace。

## 8. 托管 PBS
托管服务商可能限制 hardware 或低级数据。可用实体取决于 API 访问和权限。

下一步：[04. FAQ](04-faq.md)
