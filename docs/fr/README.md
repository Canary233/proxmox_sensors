# 📚 Proxmox Extended Sensors V5 — Documentation

Cette documentation couvre l'installation, la préparation de Proxmox, l'authentification, la configuration de Home Assistant, la surveillance matérielle et le dépannage de **Proxmox Extended Sensors V5**.

## Guides
- 🌡️ [01. Capteurs matériels et Sidecar](01-install-sensors.md)
- 🔐 [02. Utilisateur et permissions Proxmox](02-proxmox-config.md)
- 🔌 [03. Configuration Home Assistant — PVE, PBS et CLUSTER](03-login-pve-pbs.md)
- ❓ [04. FAQ et dépannage](04-faq.md)

[⬅ Retour au README principal](../../README.md)

---

## 🚀 Nouveautés de V5

### 🔄 Identité VM/LXC résistante aux migrations
Les entités VM et LXC sont suivies à l'échelle du cluster. Lors d'une migration, `unique_id`, `entity_id`, historique, statistiques, dashboards, automatisations et contrôles du guest sont conçus pour rester inchangés.

### 🛡️ Résilience aux pannes partielles
Les données PVE, PBS et CLUSTER sont actualisées par sections indépendantes. Une panne temporaire d'une partie de l'API n'oblige pas les autres données à disparaître et les dernières valeurs valides sont conservées lorsque c'est possible.

### 🔁 Réplication PVE native
V5 ajoute l'état global de réplication et des entités par job pour la **Durée**, la **Dernière réplication** et la **Prochaine réplication**. L'identité du job reste stable après migration du guest.

### 🗄️ Maintenance PBS

Les actions de maintenance PBS comprennent :

- Garbage Collection (GC)
- Prune
- Verify
- Sync

**Prune, Verify et Sync exécutent les Jobs configurés dans PBS. Garbage Collection (GC) s'exécute directement sur le datastore.**

Les actions lancées depuis Home Assistant sont corrélées à l'UPID exact de la tâche PBS, ce qui permet de suivre leur état réel du début jusqu'à la fin.

### 🧩 Multi-PBS, ❤️ Sidecar Status et 📊 pourcentages
Plusieurs PBS conservent des identités persistantes. Sidecar Status résume Memory, Mounts, Sensors et SMART par nœud PVE. V5 ajoute les pourcentages mémoire CT, disque CT et mémoire VM. Le pourcentage disque VM n'est pas exposé faute de métrique suffisamment fiable.

---

## 🎨 Dashboard Proxmox dynamique
V5 propose un dashboard Lovelace optionnel pour **PVE, PBS et CLUSTER**, généré à partir des ressources réellement présentes.

### Prérequis
- Proxmox Extended Sensors V5
- [Card Mod](https://github.com/thomasloven/lovelace-card-mod)

### Installation
1. Installer Card Mod via HACS.
2. Ajouter `/proxmox_sensors/proxmox-dashboard.js` comme **Module JavaScript** Lovelace.
3. Recharger le navigateur.
4. Créer un dashboard avec la stratégie communautaire **Proxmox Extended Sensors**.
5. Choisir **PVE**, **PBS** ou **CLUSTER** parmi les types proposés.

Avec **Take Control**, le dashboard devient personnalisable comme un dashboard Lovelace normal. Il reste entièrement optionnel.

---

## 🌐 Surveillance, sauvegardes et PBS
Selon les données disponibles, V5 peut exposer nœuds, quorum, CPU/RAM/charge/I/O wait, RX/TX, KSM, storages, montages, disques physiques, SMART, températures, VM, LXC, tâches échouées, santé des sauvegardes et réplication PVE.

Les services `create_vzdump_backup` et `backup_all` utilisent l'exécution native des sauvegardes Proxmox. PBS inclut utilisation du datastore, sauvegardes, déduplication, tâches et maintenance, avec corrélation des actions aux tâches PBS réelles.

---

## 🧩 Installation
### Via HACS — recommandé
[![Ouvrir Proxmox Extended Sensors dans HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Javisen&repository=proxmox_sensors&category=integration)

**Proxmox Extended Sensors est inclus dans le dépôt HACS par défaut. Aucun dépôt personnalisé n'est nécessaire.**

1. Ouvrir **HACS → Intégrations**.
2. Rechercher **Proxmox Extended Sensors** et le télécharger.
3. Redémarrer Home Assistant.
4. Aller dans **Paramètres → Appareils et services → Ajouter une intégration** et rechercher l'intégration.

Installation manuelle : copier dans `/config/custom_components/proxmox_sensors`, puis redémarrer Home Assistant.

---

## 🧩 Environnements pris en charge
Le projet prend en charge les installations modernes de Proxmox VE, Proxmox Backup Server et Home Assistant. Les versions minimales exactes devront être vérifiées dans les notes de version avant publication.

---
<p align="center"><i>Maintained by Javisen — MIT License</i></p>
