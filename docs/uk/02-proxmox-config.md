# 🔐 Крок 2: Користувач і дозволи Proxmox

За можливості використовуйте окремий обліковий запис Home Assistant замість `root`. Потрібні дозволи залежать від функцій: моніторинг, керування guest, backup або обслуговування PBS.

## 1. Автентифікація
**PVE:** користувач + пароль або API Token; для окремого облікового запису рекомендовано token.

**PBS:** поточний V5 flow використовує API Token з User, Token ID і Token Secret.

## 2. Створити користувача
PVE: **Datacenter → Permissions → Users**, наприклад `homeassistant@pve`. Для PBS створіть окремого користувача з правильним realm; PVE і PBS мають різні системи автентифікації.

## 3. Дозволи
Для повного набору функцій документація проєкту традиційно використовує **PVEAdmin** на `/` для PVE і **Administrator** на `/` для PBS. Це широкі ролі. З обмеженими ролями перевірте керування VM/CT, backup, cluster/tasks, storage, реплікацію PVE та PBS GC/Prune/Verify/Sync.

## 4. API Token
PVE: **Datacenter → Permissions → API Tokens**. Створіть, наприклад, `ha-token` і одразу збережіть secret. При **Privilege Separation** token може потребувати додаткових явних дозволів.

## 5. Значення Home Assistant
- **User:** повний користувач + realm (`homeassistant@pve`)
- **Token ID:** лише ім'я token (`ha-token`)
- **Token Secret:** згенерований secret

Далі: [03. Налаштування Home Assistant](03-login-pve-pbs.md)
