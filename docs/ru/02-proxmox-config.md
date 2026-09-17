# 🔐 Шаг 2: Пользователь и права Proxmox

По возможности используйте отдельную учётную запись Home Assistant вместо `root`. Необходимые права зависят от функций: мониторинг, управление guest, backup или обслуживание PBS.

## 1. Аутентификация
**PVE:** пользователь + пароль или API Token; для отдельной учётной записи рекомендуется token.

**PBS:** текущий поток V5 использует API Token с User, Token ID и Token Secret.

## 2. Создать пользователя
PVE: **Datacenter → Permissions → Users**, например `homeassistant@pve`. Для PBS создайте отдельного пользователя с правильным realm; PVE и PBS используют разные системы аутентификации.

## 3. Права
Для полного набора функций документация проекта традиционно использует **PVEAdmin** на `/` для PVE и **Administrator** на `/` для PBS. Это широкие роли. При ограниченных ролях проверьте управление VM/CT, backup, cluster/tasks, storage, репликацию PVE и PBS GC/Prune/Verify/Sync.

## 4. API Token
PVE: **Datacenter → Permissions → API Tokens**. Создайте, например, `ha-token` и сразу сохраните secret. При **Privilege Separation** token может требовать дополнительных явных прав.

## 5. Значения Home Assistant
- **User:** полный пользователь + realm (`homeassistant@pve`)
- **Token ID:** только имя token (`ha-token`)
- **Token Secret:** сгенерированный secret

Далее: [03. Настройка Home Assistant](03-login-pve-pbs.md)
