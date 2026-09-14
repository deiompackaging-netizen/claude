$ErrorActionPreference = 'Stop'
$Repo = 'https://github.com/deiompackaging-netizen/claude.git'
$Root = Join-Path $env:USERPROFILE 'DEIOM-CEO-MONEY-ENGINE'
$LogDir = Join-Path $Root 'logs'
New-Item -ItemType Directory -Force -Path $Root,$LogDir | Out-Null

function Log($m) {
  $line = "$(Get-Date -Format s) $m"
  Add-Content -Path (Join-Path $LogDir 'worker.log') -Value $line
  Write-Host $line
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Log 'Git is not installed. Worker stopped.'; exit 1 }

if (-not (Test-Path (Join-Path $Root '.git'))) {
  Log 'Cloning CEO engine repository.'
  git clone $Repo $Root | Out-Null
} else {
  Set-Location $Root
  git pull --ff-only origin main | Out-Null
}

Set-Location $Root

# Safe, deterministic local work. Heavy AI/video jobs stay in cloud services.
$jobs = @(
  @{ Name='money-engine'; Command='python scripts/money_engine.py' },
  @{ Name='tests'; Command='python -m pytest -q' }
)

foreach ($job in $jobs) {
  Log "Starting $($job.Name)"
  try {
    cmd /c $job.Command 2>&1 | Tee-Object -FilePath (Join-Path $LogDir "$($job.Name).log")
    Log "Finished $($job.Name)"
  } catch {
    Log "Job failed: $($job.Name): $($_.Exception.Message)"
  }
}

Log 'CEO PC worker completed its scheduled pass.'
