# ❓ FAQ — Proxmox Extended Sensors V5

## 🔐 Verbinding
Controleer bereikbaarheid, user/realm, actieve token, secret, API-rechten en SSL. `Permission denied` betekent vaak onvoldoende rechten.

## 🌡️ Hardware en Sidecar
Bij ontbrekende temperaturen: `sensors`, `systemctl status pve-sensors.service`, daarna `http://PROXMOX_IP:9000/sensors`.

**Sidecar Status** vat Memory, Mounts, Sensors en SMART samen (`ok`, `degraded`, `error`, `unknown`). V5 bewaart waar mogelijk laatste geldige waarden.

## 🖥️ VM/LXC-migratie
V5 gebruikt clusterbrede identiteit om `unique_id`, `entity_id`, geschiedenis, statistieken, automatiseringen en dashboards te behouden. Het bron-node-device kan tijdens reconciliation tijdelijk leeg zijn.

Geen VM-schijfpercentage wegens onvoldoende betrouwbare metriek; CT-schijfpercentage is beschikbaar wanneer data bestaat.

## 🔁 PVE-replicatie
Clusterstatus plus duur, laatste en volgende replicatie per job. Een tijdelijke API/runtime-fout betekent niet automatisch een echte replicatiefout.

## 🗄️ PBS
V5 ondersteunt GC, Prune, Verify en Sync.

> **V5-veiligheidswijziging:** anders dan in V4.x worden **Prune, Verify en Sync niet meer uitgevoerd als directe onderhoudsacties die door de integratie zelf worden opgebouwd**. V5 start de bijbehorende, vooraf in PBS geconfigureerde **Job**. Daardoor blijven de PBS-beleidsregels leidend, vooral de retentieregels van een Prune Job die bepalen welke backups verwijderd mogen worden.

**GC blijft bewust een directe datastore-actie.** Garbage Collection maakt niet-gerefereerde ruimte vrij en is daarom nuttig voor Home Assistant-automatiseringen wanneer de backupruimte laag wordt.

Prune, Verify en Sync vereisen respectievelijk een geconfigureerde **Prune Job, Verify Job of Sync Job** in PBS. Ontbreekt de benodigde Job, dan **geeft de integratie een fout en voert zij geen directe alternatieve operatie uit**. Dit is bewust veiligheidsgedrag, geen storing.

HA-acties worden via UPID tot het werkelijke resultaat gevolgd. Meerdere PBS-servers hebben persistente identiteiten.

## 🛡️ Gedeeltelijke storingen
Een oude waarde tijdens een API-probleem kan bewust zijn: V5 bewaart laatste geldige sectiedata tot verse data terugkeert.

## 🎨 Dashboard
Optioneel. Vereist V5, Card Mod en `/proxmox_sensors/proxmox-dashboard.js`. **Take Control** maakt aanpassing mogelijk.

## 🧾 Voor een issue
Controleer verbinding, credentials, token, rechten, HA-herstart, sidecar indien relevant en logs. Controleer bij Prune/Verify/Sync-fouten ook of de bijbehorende PBS Job bestaat en correct is geconfigureerd. Verwijder wachtwoorden en Token Secrets uit screenshots/logs.

## Bekende beperkingen
- geen VM-schijfpercentage
- managed PBS kan minder data bieden
- hardware hangt af van host/drivers/sidecar
- brondevice kan na migratie tijdelijk leeg zijn

[⬅ Terug naar V5-documentatie](README.md)
