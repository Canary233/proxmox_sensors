# 🔐 Stap 2: Proxmox-gebruiker en rechten

Gebruik bij voorkeur een speciaal Home Assistant-account in plaats van `root`. Rechten hangen af van monitoring, guest-control, backups en PBS-onderhoud.

## 1. Authenticatie
**PVE:** gebruiker + wachtwoord of API Token; token aanbevolen voor een speciaal account.

**PBS:** de huidige V5-flow gebruikt API Token met User, Token ID en Token Secret.

## 2. Gebruiker maken
PVE: **Datacenter → Permissions → Users**, bijvoorbeeld `homeassistant@pve`. Maak voor PBS apart een gebruiker met het juiste realm; PVE en PBS zijn gescheiden authenticatiesystemen.

## 3. Rechten
Voor volledige functionaliteit gebruikt de projectdocumentatie traditioneel **PVEAdmin** op `/` voor PVE en **Administrator** op `/` voor PBS. Dit zijn brede rollen. Test bij beperktere rollen VM/CT-control, backups, cluster/taken, storage, PVE-replicatie en PBS GC/Prune/Verify/Sync.

## 4. API Token
PVE: **Datacenter → Permissions → API Tokens**. Maak bijvoorbeeld `ha-token` en bewaar het secret direct. Met **Privilege Separation** kan de token extra expliciete rechten nodig hebben.

## 5. Home Assistant-waarden
- **User:** volledige gebruiker + realm (`homeassistant@pve`)
- **Token ID:** alleen tokennaam (`ha-token`)
- **Token Secret:** gegenereerd secret

Volgende: [03. Home Assistant-configuratie](03-login-pve-pbs.md)
