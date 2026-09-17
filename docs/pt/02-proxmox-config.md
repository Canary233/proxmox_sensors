# 🔐 Passo 2: Utilizador e permissões Proxmox

Use preferencialmente uma conta dedicada ao Home Assistant em vez de `root`. As permissões dependem das funções: monitorização, controlo de guests, backups ou manutenção PBS.

## 1. Autenticação
**PVE:** utilizador + palavra-passe ou API Token; token recomendado para uma conta dedicada.

**PBS:** o fluxo V5 atual usa API Token com User, Token ID e Token Secret.

## 2. Criar utilizador
Em PVE: **Datacenter → Permissions → Users**, por exemplo `homeassistant@pve`. Em PBS crie separadamente o utilizador com o realm correto; PVE e PBS têm sistemas de autenticação distintos.

## 3. Permissões
Para todas as funções, a documentação do projeto tem usado tradicionalmente **PVEAdmin** em `/` para PVE e **Administrator** em `/` para PBS. São funções amplas. Com permissões mais restritas, teste controlo VM/CT, backups, cluster/tarefas, storage, replicação PVE e PBS GC/Prune/Verify/Sync.

## 4. API Token
Em PVE: **Datacenter → Permissions → API Tokens**. Crie, por exemplo, `ha-token` e guarde imediatamente o secret. Com **Privilege Separation**, o token pode precisar de permissões explícitas adicionais.

## 5. Valores Home Assistant
- **User:** utilizador completo + realm (`homeassistant@pve`)
- **Token ID:** apenas o nome do token (`ha-token`)
- **Token Secret:** secret gerado

Seguinte: [03. Configuração Home Assistant](03-login-pve-pbs.md)
