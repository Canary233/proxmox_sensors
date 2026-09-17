# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 Ligação
Verifique acessibilidade, user/realm, token ativo, secret, permissões API e SSL. `Permission denied` costuma indicar permissões insuficientes.

## 🌡️ Hardware e Sidecar
Se faltarem temperaturas: `sensors`, `systemctl status pve-sensors.service`, depois `http://IP_PROXMOX:9000/sensors`.

**Sidecar Status** resume Memory, Mounts, Sensors e SMART (`ok`, `degraded`, `error`, `unknown`). V5 preserva quando possível os últimos valores válidos.

## 🖥️ Migração VM/LXC
V5 usa identidade ao nível do cluster para preservar `unique_id`, `entity_id`, histórico, estatísticas, automações e dashboards. O device do nó de origem pode ficar temporariamente vazio durante a reconciliação.

Não há percentagem de disco VM por falta de métrica fiável; disco CT está disponível quando existem dados.

## 🔁 Replicação PVE
Estado do cluster mais duração, última e próxima replicação por job. Um erro temporário API/runtime não significa automaticamente falha real da replicação.

## 🗄️ PBS
V5 suporta GC, Prune, Verify e Sync.

> **Alteração de segurança no V5:** ao contrário do V4.x, **Prune, Verify e Sync já não são executados como operações diretas construídas pela integração**. O V5 executa o **Job correspondente previamente configurado no PBS**. Assim, as políticas do PBS continuam a controlar a operação, especialmente as regras de retenção do Prune Job que determinam quais backups podem ser removidos.

**GC continua intencionalmente como ação direta no datastore.** Garbage Collection recupera espaço não referenciado e é útil em automações do Home Assistant quando o armazenamento de backups está com pouco espaço livre.

Prune, Verify e Sync exigem, respetivamente, um **Prune Job, Verify Job ou Sync Job** configurado no PBS. Se o Job necessário não existir, **a integração devolve um erro e não executa uma operação direta alternativa**. É um comportamento de segurança intencional, não uma falha.

As ações HA são seguidas por UPID até ao resultado real. Vários PBS têm identidades persistentes.

## 🛡️ Falhas parciais
Um valor anterior durante problema API pode ser intencional: V5 preserva os últimos dados válidos até regressarem dados novos.

## 🎨 Dashboard
Opcional. Requer V5, Card Mod e `/proxmox_sensors/proxmox-dashboard.js`. **Take Control** permite personalização.

## 🧾 Antes de abrir uma issue
Verifique ligação, credenciais, token, permissões, reinício HA, sidecar quando aplicável e logs. Para erros de Prune/Verify/Sync, confirme também que o Job PBS correspondente existe e está corretamente configurado. Remova palavras-passe e Token Secrets de capturas/logs.

## Limitações conhecidas
- sem percentagem de disco VM
- PBS gerido pode expor menos dados
- hardware depende de host/drivers/sidecar
- device de origem pode ficar temporariamente vazio após migração

[⬅ Voltar à documentação V5](README.md)
