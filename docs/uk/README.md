# 📚 Proxmox Extended Sensors V5 — Документація

Документація охоплює встановлення, підготовку Proxmox, автентифікацію, налаштування Home Assistant, моніторинг обладнання та усунення несправностей **Proxmox Extended Sensors V5**.

## Посібники
- 🌡️ [01. Апаратні датчики та Sidecar](01-install-sensors.md)
- 🔐 [02. Користувач і дозволи Proxmox](02-proxmox-config.md)
- 🔌 [03. Налаштування Home Assistant — PVE, PBS і CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ та усунення несправностей](04-faq.md)

[⬅ Назад до основного README](../../README.md)

---

## 🚀 Що нового у V5

### 🔄 Стабільна ідентичність VM/LXC під час міграції
VM і LXC відстежуються на рівні кластера. Під час міграції V5 розроблена для збереження `unique_id`, `entity_id`, історії, статистики, dashboards, автоматизацій і керування guest.

### 🛡️ Стійкість до часткових збоїв
PVE, PBS і CLUSTER оновлюються незалежними секціями. Тимчасовий збій однієї частини API не повинен стирати непов'язані дані; останні коректні значення за можливості зберігаються.

### 🔁 Нативний моніторинг реплікації PVE
V5 додає глобальний стан реплікації та сутності для кожного job: **Тривалість**, **Остання реплікація**, **Наступна реплікація**. Ідентичність job залишається стабільною після міграції guest.

### 🗄️ Обслуговування PBS

Дії обслуговування PBS включають:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify і Sync виконують Jobs, налаштовані в PBS. Garbage Collection (GC) виконується безпосередньо для datastore.**

Дії, запущені з Home Assistant, зіставляються з точним UPID завдання PBS, що дає змогу відстежувати їх фактичний стан від запуску до завершення.

### 🧩 Multi-PBS, ❤️ Sidecar Status і 📊 відсотки
Кілька PBS мають постійні ідентичності. Sidecar Status узагальнює Memory, Mounts, Sensors і SMART для кожного PVE-вузла. V5 додає відсоток пам'яті CT, диска CT і пам'яті VM. Відсоток диска VM не надається через відсутність достатньо надійної метрики.

---

## 🎨 Динамічний Proxmox Dashboard
V5 містить необов'язковий Lovelace dashboard для **PVE, PBS і CLUSTER**, сформований із реально доступних ресурсів.

### Вимоги
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Встановлення
1. Встановити Card Mod через HACS.
2. Додати `/proxmox_sensors/proxmox-dashboard.js` як Lovelace **JavaScript Module**.
3. Перезавантажити браузер.
4. Створити dashboard зі стратегією спільноти **Proxmox Extended Sensors**.
5. Обрати **PVE**, **PBS** або **CLUSTER** із доступних типів.

Після **Take Control** dashboard можна редагувати як звичайний Lovelace. Він повністю необов'язковий.

---

## 🌐 Моніторинг, backup і PBS
Залежно від доступних даних V5 може показувати вузли, quorum, CPU/RAM/load/I/O wait, RX/TX, KSM, storages, mounts, фізичні диски, SMART, температури, VM, LXC, failed tasks, стан backup і реплікацію PVE.

Сервіси `create_vzdump_backup` і `backup_all` використовують нативний механізм backup Proxmox. PBS включає datastore, backup, дедуплікацію, tasks і обслуговування з прив'язкою дій до реальних PBS tasks.

---

## 🧩 Встановлення
### Через HACS — рекомендовано
[![Відкрити Proxmox Extended Sensors у HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors входить до стандартного репозиторію HACS. Власний репозиторій не потрібен.**

1. Відкрити **HACS → Інтеграції**.
2. Знайти **Proxmox Extended Sensors** і завантажити.
3. Перезапустити Home Assistant.
4. Відкрити **Налаштування → Пристрої та служби → Додати інтеграцію** та знайти інтеграцію.

Вручну: скопіювати до `/config/custom_components/proxmox_sensors` і перезапустити Home Assistant.

---

## 🧩 Підтримувані середовища
Проєкт підтримує сучасні інсталяції Proxmox VE, Proxmox Backup Server і Home Assistant. Точні мінімальні версії слід перевірити за актуальними release notes перед публікацією.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
