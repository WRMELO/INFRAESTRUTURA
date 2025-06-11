# 🧠 Automação de IP por Rede Wi-Fi — Projeto Wilson
**Versão:** 1.0  
**Gerado em:** 02/06/2025 14:33:34

---

## 🎯 Objetivo

Automatizar a configuração da interface de rede Wi-Fi em um notebook com Windows 11, de forma que:

- Ao conectar-se à rede **WRMELOCLARO**, seja atribuído automaticamente o IP fixo `192.168.0.50`.
- Ao conectar-se a **qualquer outra rede**, ou permanecer desconectado, o IP volte a ser atribuído automaticamente via DHCP.

---

## 🧱 Estrutura Implementada

### 📁 Diretório dos scripts
Todos os scripts foram salvos em:

```
C:\ScriptsRede
```

---

### 📜 Script 1 — `fixar_ip_em_casa.ps1`

**Função:** Quando conectado à rede `WRMELOCLARO`, aplica IP fixo e DNS customizado.

```powershell
$targetSSID = "WRMELOCLARO"
$timeout = 60
$elapsed = 0
$interfaceName = $null
$ssidAtivo = $null

Write-Output "🔄 Aguardando rede Wi-Fi '$targetSSID' ficar disponível..."

while ($elapsed -lt $timeout) {
    $wifiInfo = netsh wlan show interfaces
    $lines = $wifiInfo -split "`n"

    foreach ($line in $lines) {
        if ($line -match "^\s*Nome\s*:\s*(.+)$") {
            $interfaceName = $Matches[1].Trim()
        }
        if ($line -match "^\s*SSID\s*:\s*(.+)$") {
            $ssidAtivo = $Matches[1].Trim()
        }
    }

    if ($interfaceName -and ($ssidAtivo -eq $targetSSID)) {
        break
    }

    Start-Sleep -Seconds 2
    $elapsed += 2
}

if ($interfaceName -and ($ssidAtivo -eq $targetSSID)) {
    Write-Output "✅ Conectado à rede '$ssidAtivo' via interface '$interfaceName'"

    netsh interface ip set address name="$interfaceName" static 192.168.0.50 255.255.255.0 192.168.0.1
    Start-Sleep -Seconds 5
    netsh interface ip set dns name="$interfaceName" static 8.8.8.8
    netsh interface ip add dns name="$interfaceName" 8.8.4.4 index=2

    Write-Output "✅ IP fixo e DNS aplicados com sucesso."
}
else {
    Write-Output "❌ Falha: SSID '$targetSSID' não detectado após $timeout segundos."
    Write-Output "🧪 Último SSID detectado: $ssidAtivo"
}
```

---

### 📜 Script 2 — `voltar_para_dhcp.ps1`

**Função:** Retorna a interface de rede para DHCP quando conectado a uma rede **diferente** de `WRMELOCLARO` ou quando estiver **desconectado**.

```powershell
$targetSSID = "WRMELOCLARO"
$timeout = 60
$elapsed = 0
$interfaceName = $null
$ssidAtivo = $null

Write-Output "🔄 Verificando rede Wi-Fi atual para decidir se deve voltar ao DHCP..."

while ($elapsed -lt $timeout) {
    $wifiInfo = netsh wlan show interfaces
    $lines = $wifiInfo -split "`n"

    foreach ($line in $lines) {
        if ($line -match "^\s*Nome\s*:\s*(.+)$") {
            $interfaceName = $Matches[1].Trim()
        }
        if ($line -match "^\s*SSID\s*:\s*(.+)$") {
            $ssidAtivo = $Matches[1].Trim()
        }
    }

    if ($interfaceName) { break }

    Start-Sleep -Seconds 2
    $elapsed += 2
}

if ($interfaceName -and (($ssidAtivo -ne $targetSSID) -or (-not $ssidAtivo))) {
    Write-Output "📡 SSID atual: '$ssidAtivo'. Retornando interface '$interfaceName' para DHCP..."

    netsh interface ip set address name="$interfaceName" dhcp
    netsh interface ip set dns name="$interfaceName" dhcp

    Write-Output "✅ Interface '$interfaceName' reconfigurada para DHCP."
}
elseif ($interfaceName -and ($ssidAtivo -eq $targetSSID)) {
    Write-Output "⏸️ SSID atual é '$ssidAtivo' (igual ao alvo). Nada será alterado — IP fixo mantido."
}
else {
    Write-Output "❌ Falha: interface de rede não detectada após $timeout segundos."
}
```

---

## 🔁 Integração com Agendador de Tarefas (Task Scheduler)

- Tarefa: `Fixar IP em casa (WRMELOCLARO)`
  - Disparo: **Ao fazer logon**
  - Ação: Executa `fixar_ip_em_casa.ps1`

- Tarefa: `Voltar para DHCP (fora de WRMELOCLARO)`
  - Disparo: **Ao fazer logon**
  - Ação: Executa `voltar_para_dhcp.ps1`

Ambas configuradas para rodar com privilégios de administrador.

---

## ✅ Resultados Esperados

| Situação                            | Resultado                                   |
|------------------------------------|---------------------------------------------|
| Conectado à `WRMELOCLARO`          | IP fixo `192.168.0.50` e DNS customizado    |
| Conectado a outra rede Wi-Fi       | Retorna automaticamente ao modo DHCP        |
| Sem Wi-Fi conectada                | Também volta ao DHCP (interface liberada)   |

---

## ✍️ Observações Finais

- Scripts funcionam mesmo com nomes diferentes de interface (`Wi-Fi`, `Wi-Fi 2`, etc).
- Os scripts são tolerantes a erros e silenciosos se o contexto não for compatível.
- A lógica pode ser facilmente adaptada a novos SSIDs, bastando mudar o valor de `$targetSSID`.

---

