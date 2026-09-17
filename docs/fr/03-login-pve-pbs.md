# 🔌 Étape 3 : Home Assistant — PVE, PBS et CLUSTER

## 1. HACS
[![Ouvrir dans HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

L'intégration est dans le dépôt HACS par défaut : aucun dépôt personnalisé. Recherchez **Proxmox Extended Sensors** dans **HACS → Intégrations**, téléchargez-le puis redémarrez Home Assistant.

## 2. Ajouter l'intégration
**Paramètres → Appareils et services → Ajouter une intégration → Proxmox Extended Sensors**.

Types : **PVE**, **PBS**, **CLUSTER**.

## 3. Hôte et authentification
Saisissez l'IP ou le nom d'hôte. PVE accepte utilisateur/mot de passe ou API Token. PBS utilise le token dans le flux V5 actuel. Pour un token : User complet avec realm, Token ID = nom du token uniquement, puis Token Secret.

## 4. PVE
Après connexion, l'intégration découvre nœuds et ressources (VM, LXC, storages, matériel). L'identité cluster-wide de V5 permet aux entités VM/LXC de suivre les migrations.

## 5. PBS
Chaque PBS possède sa propre entrée de configuration et une identité persistante. Les données peuvent inclure datastore, sauvegardes, déduplication, tâches, GC, Prune, Verify et Sync si un Sync Job existe.

## 6. CLUSTER
Expose notamment quorum, nœuds, CPU/RAM agrégés, nombre de VM/CT, stockage cluster, tâches échouées, santé des sauvegardes et réplication PVE.

## 7. Dashboard optionnel
Installer Card Mod, ajouter `/proxmox_sensors/proxmox-dashboard.js` comme Module JavaScript, recharger le navigateur puis créer un dashboard avec la stratégie **Proxmox Extended Sensors**. Choisir PVE/PBS/CLUSTER. **Take Control** permet ensuite de l'éditer normalement.

## 8. PBS hébergé
Un fournisseur PBS géré peut limiter les données matérielles/bas niveau. Les entités disponibles dépendent de l'accès API et des permissions.

Suivant : [04. FAQ](04-faq.md)
