# 🔌 Passo 3: Home Assistant — PVE, PBS e CLUSTER

## 1. HACS
[![Abrir no HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

A integração está no repositório HACS predefinido; não é necessário repositório personalizado. Procure **Proxmox Extended Sensors** em **HACS → Integrações**, descarregue e reinicie Home Assistant.

## 2. Adicionar integração
**Definições → Dispositivos e serviços → Adicionar integração → Proxmox Extended Sensors**. Tipos: **PVE**, **PBS**, **CLUSTER**.

## 3. Host e autenticação
Introduza IP ou hostname. PVE suporta utilizador/palavra-passe ou API Token; PBS usa API Token no fluxo V5 atual. Com token: User completo com realm, apenas nome do token como Token ID e Token Secret.

## 4. PVE
Após ligar, a integração descobre nós e recursos como VMs, LXC, storages e hardware. A identidade cluster-wide de V5 permite às entidades VM/LXC seguir migrações.

## 5. PBS
Cada PBS tem uma config entry própria e identidade persistente. Pode incluir datastore, backups, deduplicação, tarefas, GC, Prune, Verify e Sync quando existe Sync Job.

## 6. CLUSTER
Inclui quorum, nós, CPU/RAM agregados, contagens VM/CT, storage do cluster, tarefas falhadas, saúde de backups e replicação PVE.

## 7. Dashboard opcional
Instale Card Mod, adicione `/proxmox_sensors/proxmox-dashboard.js` como Módulo JavaScript, recarregue o navegador e crie um dashboard com a estratégia **Proxmox Extended Sensors**. Escolha PVE/PBS/CLUSTER. **Take Control** permite depois editar normalmente.

## 8. PBS gerido
Fornecedores PBS podem limitar dados de hardware ou baixo nível. As entidades disponíveis dependem do acesso API e permissões.

Seguinte: [04. FAQ](04-faq.md)
