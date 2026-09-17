# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 Connexion
Vérifiez accessibilité, utilisateur/realm, token actif, secret, permissions API et SSL. `Permission denied` indique généralement des permissions insuffisantes.

## 🌡️ Matériel et Sidecar
Si les températures manquent : `sensors`, `systemctl status pve-sensors.service`, puis `http://IP_PROXMOX:9000/sensors`.

**Sidecar Status** résume Memory, Mounts, Sensors et SMART (`ok`, `degraded`, `error`, `unknown`). V5 conserve si possible les dernières valeurs valides.

## 🖥️ Migration VM/LXC
V5 utilise une identité à l'échelle du cluster afin de conserver `unique_id`, `entity_id`, historique, statistiques, automatisations et dashboards. Le device du nœud source peut rester brièvement vide pendant la réconciliation.

Pas de pourcentage disque VM faute de métrique fiable ; le pourcentage disque CT est disponible lorsque les données existent.

## 🔁 Réplication PVE
État cluster + durée, dernière et prochaine réplication par job. Une erreur API/runtime temporaire n'est pas automatiquement considérée comme un échec réel du job.

## 🗄️ PBS
V5 prend en charge GC, Prune, Verify et Sync.

> **Changement de sécurité V5 :** contrairement à V4.x, **Prune, Verify et Sync ne sont plus exécutés comme des opérations directes construites par l'intégration**. V5 lance le **Job correspondant déjà configuré dans PBS**. Les politiques PBS restent ainsi responsables de l'opération, notamment les règles de rétention du Prune Job qui déterminent les sauvegardes pouvant être supprimées.

**GC reste volontairement une action directe sur le datastore.** Garbage Collection récupère l'espace non référencé et reste donc utile dans les automatisations Home Assistant lorsque l'espace de sauvegarde devient faible.

Prune, Verify et Sync nécessitent respectivement un **Prune Job, Verify Job ou Sync Job** configuré dans PBS. Si le Job requis n'existe pas, **l'intégration renvoie une erreur et n'effectue aucune opération directe de remplacement**. C'est un comportement de sécurité intentionnel, pas un dysfonctionnement.

Les actions HA sont suivies via l'UPID PBS jusqu'au résultat réel. Plusieurs PBS conservent des identités persistantes.

## 🛡️ Pannes partielles
Une ancienne valeur pendant un problème API peut être intentionnelle : V5 conserve les dernières données valides jusqu'au retour de données fraîches.

## 🎨 Dashboard
Optionnel. Nécessite V5, Card Mod et `/proxmox_sensors/proxmox-dashboard.js`. **Take Control** permet ensuite la personnalisation.

## 🧾 Avant d'ouvrir une issue
Vérifiez connexion, identifiants, token, permissions, redémarrage HA, sidecar si nécessaire et logs. Pour une erreur Prune/Verify/Sync, vérifiez aussi que le Job PBS correspondant existe et est correctement configuré. Retirez mots de passe et Token Secrets des captures/logs.

## Limitations connues
- pas de pourcentage disque VM
- PBS géré potentiellement plus limité
- matériel dépend du host, pilotes et sidecar
- device source temporairement vide possible après migration

[⬅ Retour à la documentation V5](README.md)
