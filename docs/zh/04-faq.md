# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 连接
检查可访问性、user/realm、token、secret、API 权限和 SSL。`Permission denied` 通常表示权限不足。

## 🌡️ 硬件与 Sidecar
缺少温度时：运行 `sensors`、`systemctl status pve-sensors.service`，然后访问 `http://PROXMOX_IP:9000/sensors`。

**Sidecar Status** 汇总 Memory、Mounts、Sensors 和 SMART（`ok`、`degraded`、`error`、`unknown`）。V5 尽可能保留最后有效值。

## 🖥️ VM/LXC 迁移
V5 使用 cluster-wide 身份以保留 `unique_id`、`entity_id`、历史、统计、自动化和 dashboards。协调完成前，源节点 device 可能暂时为空。

由于没有足够可靠的指标，不提供 VM 磁盘百分比；有数据时可提供 CT 磁盘百分比。

## 🔁 PVE 复制
提供集群状态以及每个 job 的持续时间、上次和下次复制。临时 API/runtime 错误不会自动视为真实复制失败。

## 🗄️ PBS
V5 支持 GC、Prune、Verify 和 Sync。

> **V5 安全性变更：**与 V4.x 不同，**Prune、Verify 和 Sync 不再由集成自行构造并直接执行维护操作**。V5 会运行管理员预先在 PBS 中配置的对应 **Job**。这样操作始终遵循 PBS 的策略，尤其是 Prune Job 的保留规则，由 PBS 决定哪些备份可以删除。

**GC 有意保留为 datastore 的直接操作。** Garbage Collection 用于回收不再被引用的空间，因此非常适合在备份存储空间不足时通过 Home Assistant 自动化触发。

Prune、Verify 和 Sync 分别要求 PBS 中存在对应的 **Prune Job、Verify Job 或 Sync Job**。如果所需 Job 不存在，**集成会返回错误，并且不会退回到直接执行的替代操作**。这是有意的安全设计，并非集成故障。

HA 发起的操作通过 PBS UPID 跟踪到实际结果。多个 PBS 使用持久身份。

## 🛡️ 局部故障
API 出现问题时仍显示旧值可能是预期行为：V5 会保留最后一次有效数据，直到新的数据恢复。

## 🎨 Dashboard
可选。需要 V5、Card Mod 和 `/proxmox_sensors/proxmox-dashboard.js`。使用 **Take Control** 后可自定义。

## 🧾 提交 issue 前
检查连接、credentials、token、权限、HA 重启、必要时检查 sidecar 和 logs。如果 Prune/Verify/Sync 报错，还应确认对应的 PBS Job 已存在且配置正确。请从截图/log 中删除密码和 Token Secret。

## 已知限制
- 不提供 VM 磁盘百分比
- 托管 PBS 可能提供更少数据
- 硬件数据取决于 host/drivers/sidecar
- VM/LXC 迁移后源 device 可能暂时为空

[⬅ 返回 V5 文档](README.md)
