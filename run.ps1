# ==============================================================================
#  RiskTwin - Единый диспетчер запуска микросервисов
#  Поддерживаемые команды:
#    .\run.ps1 start    - Запустить все микросервисы
#    .\run.ps1 stop     - Остановить все сервисы и освободить порты
#    .\run.ps1 restart  - Перезапустить всю экосистему
#    .\run.ps1 status   - Проверить статус доступности портов
# ==============================================================================

param (
    [Parameter(Position = 0)]
    [ValidateSet("start", "stop", "restart", "status")]
    [string]$Action = "start"
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"
$Root = $PSScriptRoot

$PORTS = [ordered]@{
    "ML Engine (PyTorch gRPC)" = 50051
    "Agent World (Python API)" = 8001
    "Core Backend (.NET 9)"    = 5000
    "Web UI (Next.js)"         = 3000
}

function Show-Banner {
    Write-Host ""
    Write-Host "   ==============================================================" -ForegroundColor DarkCyan
    Write-Host "     ____  _     _     _____          _                          " -ForegroundColor Cyan
    Write-Host "    |  _ \(_)___| | __|_   _|_      _(_)_ __                     " -ForegroundColor Cyan
    Write-Host "    | |_) | / __| |/ /  | | \ \ /\ / / | '_ \                    " -ForegroundColor Cyan
    Write-Host "    |  _ <| \__ \   <   | |  \ V  V /| | | | |                   " -ForegroundColor Cyan
    Write-Host "    |_| \_\_|___/_|\_\  |_|   \_/\_/ |_|_| |_|                   " -ForegroundColor Cyan
    Write-Host "     Кредитный цифровой двойник • Диспетчер микросервисов        " -ForegroundColor White
    Write-Host "   ==============================================================" -ForegroundColor DarkCyan
    Write-Host ""
}

function Kill-Port {
    param([int]$Port, [string]$Name)
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($connections) {
        $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($procId in $pids) {
            if ($procId -gt 0) {
                try {
                    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                    Write-Host "   [-] Порт $Port ($Name) освобожден (PID $procId)" -ForegroundColor Yellow
                } catch {}
            }
        }
    }
}

function Stop-AllServices {
    Write-Host "[1/2] Остановка сервисов..." -ForegroundColor Yellow
    foreach ($k in $PORTS.Keys) {
        Kill-Port -Port $PORTS[$k] -Name $k
    }

    # Завершаем фоновые процессы dotnet и node если они привязаны к RiskTwin
    Get-Process dotnet, node, uv -ErrorAction SilentlyContinue | Where-Object {
        $_.Path -like "*RiskTwin*"
    } | Stop-Process -Force -ErrorAction SilentlyContinue

    Start-Sleep -Seconds 1
    Write-Host "   [OK] Сервисы остановлены." -ForegroundColor Green
    Write-Host ""
}

function Check-ServicePort {
    param([int]$Port)
    $conn = Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    return $conn
}

function Show-Status {
    Write-Host "--- Статус микросервисов ---" -ForegroundColor White
    foreach ($k in $PORTS.Keys) {
        $port = $PORTS[$k]
        $isAlive = Check-ServicePort -Port $port
        if ($isAlive) {
            Write-Host "   [ONLINE]  $($k.PadRight(26)) : порт $port" -ForegroundColor Green
        } else {
            Write-Host "   [OFFLINE] $($k.PadRight(26)) : порт $port" -ForegroundColor Red
        }
    }
    Write-Host ""
}

function Start-AllServices {
    Write-Host "[1/3] Проверка и освобождение портов..." -ForegroundColor Yellow
    foreach ($k in $PORTS.Keys) {
        Kill-Port -Port $PORTS[$k] -Name $k
    }
    Start-Sleep -Seconds 1

    Write-Host "[2/3] Запуск микросервисов..." -ForegroundColor Cyan

    # 1. ML Engine (gRPC :50051)
    Write-Host "   --> Запуск ML Engine (PyTorch gRPC)..." -ForegroundColor Gray
    Start-Process powershell -WorkingDirectory "$Root\src\ml-engine" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'RiskTwin [1] ML Engine (:50051)'; uv run main.py"

    Start-Sleep -Seconds 2

    # 2. Agent World (FastAPI :8001)
    Write-Host "   --> Запуск Agent World (10 RL-агентов)..." -ForegroundColor Gray
    Start-Process powershell -WorkingDirectory "$Root\src\agent-world" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'RiskTwin [2] Agent World (:8001)'; uv run main.py"

    Start-Sleep -Seconds 2

    # 3. Core Backend (.NET 9 :5000)
    Write-Host "   --> Запуск Core Backend (.NET 9 WebApi)..." -ForegroundColor Gray
    Start-Process powershell -WorkingDirectory "$Root\src\core-backend\RiskTwin.WebApi" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'RiskTwin [3] Core Backend (:5000)'; dotnet run --urls 'http://localhost:5000'"

    Start-Sleep -Seconds 2

    # 4. Web Frontend (Next.js :3000)
    Write-Host "   --> Запуск Web Frontend (Next.js)..." -ForegroundColor Gray
    Start-Process powershell -WorkingDirectory "$Root\src\web" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle = 'RiskTwin [4] Web Frontend (:3000)'; npm run dev"

    Write-Host "[3/3] Ожидание инициализации (5 сек)..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5

    Show-Status

    Write-Host "   [+] Открытие браузера: http://localhost:3000" -ForegroundColor Cyan
    Start-Process "http://localhost:3000"

    Write-Host ""
    Write-Host "   Остановить все сервисы:  .\run.ps1 stop" -ForegroundColor Green
    Write-Host "   Перезапустить сервисы:   .\run.ps1 restart" -ForegroundColor Green
    Write-Host ""
}

# Точка входа
Show-Banner

switch ($Action) {
    "start" {
        Start-AllServices
    }
    "stop" {
        Stop-AllServices
        Show-Status
    }
    "restart" {
        Write-Host "--- ПЕРЕЗАПУСК ПРИЛОЖЕНИЯ ---" -ForegroundColor Cyan
        Stop-AllServices
        Start-Sleep -Seconds 2
        Start-AllServices
    }
    "status" {
        Show-Status
    }
}
