# 🔌 Шаг 3: Home Assistant — PVE, PBS и CLUSTER

## 1. HACS
[![Открыть в HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

Интеграция находится в стандартном репозитории HACS; custom repository не нужен. Найдите **Proxmox Extended Sensors** в **HACS → Интеграции**, скачайте и перезапустите Home Assistant.

## 2. Добавить интеграцию
**Настройки → Устройства и службы → Добавить интеграцию → Proxmox Extended Sensors**. Типы: **PVE**, **PBS**, **CLUSTER**.

## 3. Host и аутентификация
Введите IP или hostname. PVE поддерживает user/password или API Token; PBS в текущем V5 использует API Token. Для token укажите полный User с realm, только имя token как Token ID и Token Secret.

## 4. PVE
После подключения обнаруживаются узлы и ресурсы: VM, LXC, storages, hardware. Cluster-wide идентичность V5 позволяет сущностям VM/LXC следовать за миграциями.

## 5. PBS
Каждый PBS имеет отдельную config entry и постоянную идентичность. Доступны datastore, backup, дедупликация, tasks, GC, Prune, Verify и Sync при наличии Sync Job.

## 6. CLUSTER
Включает quorum, узлы, агрегированные CPU/RAM, количество VM/CT, cluster storage, failed tasks, backup health и PVE replication.

## 7. Необязательный dashboard
Установите Card Mod, добавьте `/proxmox_sensors/proxmox-dashboard.js` как JavaScript Module, перезагрузите браузер и создайте dashboard со стратегией **Proxmox Extended Sensors**. Выберите PVE/PBS/CLUSTER. **Take Control** позволяет обычное редактирование Lovelace.

## 8. Managed PBS
Провайдер может ограничивать аппаратные и низкоуровневые данные. Доступные сущности зависят от API-доступа и прав.

Далее: [04. FAQ](04-faq.md)
