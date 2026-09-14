$ErrorActionPreference = 'Stop'
$Repo = 'https://github.com/deiompackaging-netizen/claude.git'
$Root = Join-Path $env:USERPROFILE 'DEIOM-CEO-MONEY-ENGINE'
$AgentDir = Join-Path $Root 'pc_agent'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host 'Git is required. Install Git for Windows, then run this script again.'
  exit 1
}

if (-not (Test-Path (Join-Path $Root '.git'))) {
  git clone $Repo $Root
} else {
  Set-Location $Root
  git pull --ff-only origin main
}

$Worker = Join-Path $Root 'pc_agent\worker.ps1'
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Worker`""
$Trigger1 = New-ScheduledTaskTrigger -AtStartup
$Trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 30)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'DEIOM CEO Money Engine' -Action $Action -Trigger @($Trigger1,$Trigger2) -Principal $Principal -Force

Write-Host 'DEIOM CEO Money Engine installed.'
Write-Host 'It will run at startup and every 30 minutes while the Windows account is available.'
Write-Host "Logs: $Root\logs\worker.log"
