# 📚 Proxmox Extended Sensors V5 — Документация

Документация описывает установку, подготовку Proxmox, аутентификацию, настройку Home Assistant, мониторинг оборудования и устранение неполадок **Proxmox Extended Sensors V5**.

## Руководства
- 🌡️ [01. Аппаратные датчики и Sidecar](01-install-sensors.md)
- 🔐 [02. Пользователь и права Proxmox](02-proxmox-config.md)
- 🔌 [03. Настройка Home Assistant — PVE, PBS и CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ и устранение неполадок](04-faq.md)

[⬅ Вернуться к основному README](../../README.md)

---

## 🚀 Что нового в V5

### 🔄 Устойчивая к миграциям идентичность VM/LXC
VM и LXC отслеживаются на уровне кластера. При миграции V5 сохраняет `unique_id`, `entity_id`, историю, статистику, dashboards, автоматизации и управление guest.

### 🛡️ Устойчивость к частичным сбоям
Данные PVE, PBS и CLUSTER обновляются независимыми секциями. Временный сбой одной части API не должен стирать несвязанные данные; последние корректные значения по возможности сохраняются.

### 🔁 Нативный мониторинг репликации PVE
V5 добавляет общий статус репликации и сущности для каждого job: **Длительность**, **Последняя репликация**, **Следующая репликация**. Идентичность job остаётся стабильной после миграции guest.

### 🗄️ Обслуживание PBS

Действия обслуживания PBS включают:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify и Sync выполняют Jobs, настроенные в PBS. Garbage Collection (GC) выполняется непосредственно для datastore.**

Действия, запущенные из Home Assistant, сопоставляются с точным UPID задачи PBS, что позволяет отслеживать их фактическое состояние от запуска до завершения.

### 🧩 Multi-PBS, ❤️ Sidecar Status и 📊 проценты
Несколько PBS получают постоянные идентификаторы. Sidecar Status суммирует Memory, Mounts, Sensors и SMART для каждого PVE-узла. V5 добавляет проценты памяти CT, диска CT и памяти VM. Процент диска VM не предоставляется из-за отсутствия достаточно надёжной метрики.

---

## 🎨 Динамический Proxmox Dashboard
V5 включает необязательный Lovelace dashboard для **PVE, PBS и CLUSTER**, формируемый из реально доступных ресурсов.

### Требования
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Установка
1. Установить Card Mod через HACS.
2. Добавить `/proxmox_sensors/proxmox-dashboard.js` как Lovelace **JavaScript Module**.
3. Перезагрузить браузер.
4. Создать dashboard со стратегией сообщества **Proxmox Extended Sensors**.
5. Выбрать **PVE**, **PBS** или **CLUSTER** из доступных вариантов.

После **Take Control** dashboard можно редактировать как обычный Lovelace. Он полностью необязателен.

---

## 🌐 Мониторинг, backup и PBS
В зависимости от доступных данных V5 может показывать узлы, quorum, CPU/RAM/load/I/O wait, RX/TX, KSM, storages, mounts, физические диски, SMART, температуры, VM, LXC, failed tasks, состояние backup и репликацию PVE.

Сервисы `create_vzdump_backup` и `backup_all` используют нативный механизм backup Proxmox. PBS включает datastore, backup, дедупликацию, задачи и обслуживание с привязкой действий к реальным PBS-задачам.

---

## 🧩 Установка
### Через HACS — рекомендуется
[![Открыть Proxmox Extended Sensors в HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors включён в стандартный репозиторий HACS. Пользовательский репозиторий не требуется.**

1. Открыть **HACS → Интеграции**.
2. Найти **Proxmox Extended Sensors** и скачать.
3. Перезапустить Home Assistant.
4. Открыть **Настройки → Устройства и службы → Добавить интеграцию** и найти интеграцию.

Вручную: скопировать в `/config/custom_components/proxmox_sensors` и перезапустить Home Assistant.

---

## 🧩 Поддерживаемые среды
Проект поддерживает современные установки Proxmox VE, Proxmox Backup Server и Home Assistant. Точные минимальные версии следует сверить с актуальными release notes перед публикацией.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
