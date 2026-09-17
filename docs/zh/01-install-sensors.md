# 🌡️ 第 1 步：硬件传感器与 Sidecar

本指南用于准备 Proxmox VE 节点，以读取标准 Proxmox API 未提供的硬件数据。V5 使用 sidecar 获取温度、内存、mount 和 SMART 数据，并提供 **Sidecar Status**。

## 1. 安装软件包
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. 检测传感器
```bash
sensors-detect
```
按照向导启用适合硬件的模块。如果提示写入 `/etc/modules`，请确保所需模块在重启后仍会加载。

## 3. 验证
```bash
sensors
```
Intel 系统使用 `coretemp` 时，如有需要：
```bash
modprobe coretemp
sensors
```
不要在使用其他驱动的系统上强制加载 `coretemp`。

## 4. 安装 sidecar
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```
创建 systemd 服务运行 `/usr/bin/python3 /usr/local/bin/pve-sensors-api.py` 并启用自动重启，然后：
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. 验证 sidecar
运行 `systemctl status pve-sensors.service`，然后打开 `http://你的_PROXMOX_IP:9000/sensors`。返回 JSON 表示 sidecar 正常响应。

## 6. Sidecar 故障时
V5 会尽可能保留最后一次有效硬件值。**Sidecar Status** 将 Memory、Mounts、Sensors 和 SMART 显示为 `ok`、`degraded`、`error` 或 `unknown`。

下一步：[02. Proxmox 用户与权限](02-proxmox-config.md)
