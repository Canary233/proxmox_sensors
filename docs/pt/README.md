# 📚 Proxmox Extended Sensors V5 — Documentação

Esta documentação cobre instalação, preparação do Proxmox, autenticação, configuração do Home Assistant, monitorização de hardware e resolução de problemas do **Proxmox Extended Sensors V5**.

## Guias
- 🌡️ [01. Sensores de hardware e Sidecar](01-install-sensors.md)
- 🔐 [02. Utilizador e permissões Proxmox](02-proxmox-config.md)
- 🔌 [03. Configuração Home Assistant — PVE, PBS e CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ e resolução de problemas](04-faq.md)

[⬅ Voltar ao README principal](../../README.md)

---

## 🚀 Novidades da V5

### 🔄 Identidade VM/LXC resistente a migrações
As entidades VM e LXC são acompanhadas ao nível do cluster. Durante uma migração, V5 foi concebida para preservar `unique_id`, `entity_id`, histórico, estatísticas, dashboards, automações e controlos do guest.

### 🛡️ Resistência a falhas parciais
Os dados PVE, PBS e CLUSTER são atualizados em secções independentes. Uma falha temporária numa área da API não precisa de apagar dados não relacionados e, quando possível, são preservados os últimos valores válidos.

### 🔁 Monitorização nativa da replicação PVE
V5 adiciona estado global de replicação e entidades por job para **Duração**, **Última replicação** e **Próxima replicação**. A identidade do job permanece estável após a migração do guest.

### 🗄️ Manutenção PBS

As ações de manutenção PBS incluem:

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify e Sync executam os Jobs configurados no PBS. Garbage Collection (GC) é executado diretamente no datastore.**

As ações iniciadas no Home Assistant são correlacionadas com o UPID exato da tarefa PBS, permitindo acompanhar o seu estado real desde o início até à conclusão.

### 🧩 Multi-PBS, ❤️ Sidecar Status e 📊 percentagens
Vários PBS mantêm identidades persistentes. Sidecar Status resume Memory, Mounts, Sensors e SMART por nó PVE. V5 adiciona percentagem de memória CT, disco CT e memória VM. A percentagem de disco VM não é exposta por falta de uma métrica suficientemente fiável.

---

## 🎨 Dashboard Proxmox dinâmico
V5 inclui um dashboard Lovelace opcional para **PVE, PBS e CLUSTER**, gerado a partir dos recursos realmente disponíveis.

### Requisitos
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Instalação
1. Instalar Card Mod via HACS.
2. Adicionar `/proxmox_sensors/proxmox-dashboard.js` como **Módulo JavaScript** Lovelace.
3. Recarregar o navegador.
4. Criar um dashboard com a estratégia comunitária **Proxmox Extended Sensors**.
5. Escolher **PVE**, **PBS** ou **CLUSTER** entre os tipos disponíveis.

Com **Take Control**, o dashboard pode ser editado como um Lovelace normal. É completamente opcional.

---

## 🌐 Monitorização, backups e PBS
Conforme os dados disponíveis, V5 pode expor nós, quorum, CPU/RAM/load/I/O wait, RX/TX, KSM, storages, mounts, discos físicos, SMART, temperaturas, VMs, LXC, tarefas falhadas, saúde dos backups e replicação PVE.

Os serviços `create_vzdump_backup` e `backup_all` utilizam a execução nativa de backups do Proxmox. PBS inclui utilização de datastore, backups, deduplicação, tarefas e manutenção, correlacionando ações com as tarefas PBS reais.

---

## 🧩 Instalação
### Via HACS — recomendado
[![Abrir Proxmox Extended Sensors no HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors está incluído no repositório HACS predefinido. Não é necessário adicionar um repositório personalizado.**

1. Abrir **HACS → Integrações**.
2. Procurar **Proxmox Extended Sensors** e descarregar.
3. Reiniciar Home Assistant.
4. Ir a **Definições → Dispositivos e serviços → Adicionar integração** e procurar a integração.

Instalação manual: copiar para `/config/custom_components/proxmox_sensors` e reiniciar Home Assistant.

---

## 🧩 Ambientes suportados
O projeto suporta instalações modernas de Proxmox VE, Proxmox Backup Server e Home Assistant. As versões mínimas exatas devem ser confirmadas nas notas de versão antes da publicação.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
