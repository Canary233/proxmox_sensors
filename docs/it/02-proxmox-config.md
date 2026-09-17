# 🔐 Passo 2: Utente e permessi Proxmox

Usa preferibilmente un account Home Assistant dedicato invece di `root`. I permessi necessari dipendono dalle funzioni: solo monitoraggio, controllo guest, backup o manutenzione PBS.

## 1. Autenticazione
**PVE:** utente + password oppure API Token. Per un account dedicato è consigliato il token.

**PBS:** il flusso V5 attuale usa API Token con User, Token ID e Token Secret.

## 2. Crea l'utente
In PVE: **Datacenter → Permissions → Users**, ad esempio `homeassistant@pve`. In PBS crea separatamente l'utente con il realm corretto: PVE e PBS hanno sistemi di autenticazione distinti.

## 3. Permessi
Per tutte le funzioni la documentazione ha tradizionalmente usato **PVEAdmin** su `/` per PVE e **Administrator** su `/` per PBS. Sono ruoli ampi. Con ruoli più restrittivi verifica controllo VM/CT, backup, cluster/task, storage, replica PVE e GC/Prune/Verify/Sync PBS.

## 4. API Token
In PVE: **Datacenter → Permissions → API Tokens**. Crea ad esempio `ha-token` e salva subito il secret. Con **Privilege Separation** il token può richiedere permessi espliciti oltre a quelli dell'utente.

## 5. Valori Home Assistant
- **User:** utente completo con realm (`homeassistant@pve`)
- **Token ID:** solo nome token (`ha-token`)
- **Token Secret:** secret generato

Avanti: [03. Configurazione Home Assistant](03-login-pve-pbs.md)
