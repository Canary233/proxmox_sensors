# 🔌 Крок 3: Home Assistant — PVE, PBS і CLUSTER

## 1. HACS
[![Відкрити в HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

Інтеграція є у стандартному репозиторії HACS; custom repository не потрібен. Знайдіть **Proxmox Extended Sensors** у **HACS → Інтеграції**, завантажте й перезапустіть Home Assistant.

## 2. Додати інтеграцію
**Налаштування → Пристрої та служби → Додати інтеграцію → Proxmox Extended Sensors**. Типи: **PVE**, **PBS**, **CLUSTER**.

## 3. Host та автентифікація
Введіть IP або hostname. PVE підтримує user/password або API Token; PBS у поточному V5 використовує API Token. Для token введіть повний User з realm, лише ім'я token як Token ID і Token Secret.

## 4. PVE
Після підключення інтеграція виявляє вузли та ресурси: VM, LXC, storages і hardware. Cluster-wide ідентичність V5 дозволяє VM/LXC сутностям слідувати за міграціями.

## 5. PBS
Кожен PBS має окремий config entry і постійну ідентичність. Можливі datastore, backup, дедуплікація, tasks, GC, Prune, Verify і Sync за наявності Sync Job.

## 6. CLUSTER
Включає quorum, вузли, агреговані CPU/RAM, кількість VM/CT, cluster storage, failed tasks, backup health і PVE replication.

## 7. Необов'язковий dashboard
Встановіть Card Mod, додайте `/proxmox_sensors/proxmox-dashboard.js` як JavaScript Module, перезавантажте браузер і створіть dashboard зі стратегією **Proxmox Extended Sensors**. Оберіть PVE/PBS/CLUSTER. **Take Control** дозволяє звичайне редагування Lovelace.

## 8. Managed PBS
Провайдер може обмежувати hardware або low-level дані. Доступні сутності залежать від API-доступу та дозволів.

Далі: [04. FAQ](04-faq.md)
