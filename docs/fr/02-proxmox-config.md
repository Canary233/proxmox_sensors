# 🔐 Étape 2 : Utilisateur et permissions Proxmox

Utilisez de préférence un compte Home Assistant dédié plutôt que `root`. Les permissions dépendent des fonctions utilisées : surveillance seule, contrôle des guests, sauvegardes ou maintenance PBS.

## 1. Authentification
**PVE :** utilisateur + mot de passe ou API Token. Un token est recommandé pour un compte dédié.

**PBS :** le flux V5 actuel utilise un API Token avec User, Token ID et Token Secret.

## 2. Créer l'utilisateur
Dans PVE : **Datacenter → Permissions → Users**, par exemple `homeassistant@pve`. Créez séparément l'utilisateur PBS avec le realm approprié : PVE et PBS sont des systèmes d'authentification distincts.

## 3. Permissions
Pour toutes les fonctions, la documentation du projet utilise traditionnellement **PVEAdmin** sur `/` pour PVE et **Administrator** sur `/` pour PBS. Ce sont des rôles larges. Avec un rôle restreint, testez contrôle VM/CT, sauvegardes, cluster/tâches, stockage, réplication PVE et GC/Prune/Verify/Sync PBS.

## 4. API Token
Dans PVE : **Datacenter → Permissions → API Tokens**. Créez par exemple `ha-token` et conservez immédiatement le secret. Avec **Privilege Separation**, le token peut nécessiter des permissions explicites en plus de celles de l'utilisateur.

## 5. Valeurs Home Assistant
- **User** : utilisateur complet + realm (`homeassistant@pve`)
- **Token ID** : nom du token uniquement (`ha-token`)
- **Token Secret** : secret généré

Suivant : [03. Configuration Home Assistant](03-login-pve-pbs.md)
