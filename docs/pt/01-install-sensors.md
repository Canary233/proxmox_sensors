# 🌡️ Passo 1: Sensores de hardware e Sidecar

Este guia prepara um nó Proxmox VE para dados de hardware que não são expostos pela API Proxmox padrão. V5 usa o sidecar para temperaturas, memória, mounts e SMART e adiciona **Sidecar Status**.

## 1. Instalar pacotes
```bash
apt update && apt install lm-sensors smartmontools -y
```

## 2. Detetar sensores
```bash
sensors-detect
```
Siga o assistente e ative os módulos adequados. Se for proposta a gravação em `/etc/modules`, assegure que os módulos necessários persistem após reiniciar.

## 3. Verificar
```bash
sensors
```
Em Intel com `coretemp`, se necessário:
```bash
modprobe coretemp
sensors
```
Não force `coretemp` em sistemas que usam outro driver.

## 4. Instalar sidecar
```bash
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py
chmod +x /usr/local/bin/pve-sensors-api.py
```
Crie o serviço systemd para executar `/usr/bin/python3 /usr/local/bin/pve-sensors-api.py` com reinício automático e depois:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors.service
```

## 5. Verificar sidecar
Execute `systemctl status pve-sensors.service` e abra `http://IP_DO_SEU_PROXMOX:9000/sensors`. Uma resposta JSON confirma o funcionamento.

## 6. Em caso de falha
V5 preserva, quando possível, os últimos valores de hardware válidos. **Sidecar Status** mostra Memory, Mounts, Sensors e SMART como `ok`, `degraded`, `error` ou `unknown`.

Seguinte: [02. Utilizador e permissões Proxmox](02-proxmox-config.md)
