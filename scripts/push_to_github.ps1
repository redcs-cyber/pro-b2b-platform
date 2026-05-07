Param(
  [Parameter(Mandatory = $true)]
  [string]$RepoUrl,

  [string]$Branch = "main",
  [string]$CommitMessage = "Publish project to GitHub"
)

$ErrorActionPreference = "Stop"

function Write-Step {
  Param([string]$Message)
  Write-Host "==> $Message" -ForegroundColor Cyan
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Git bulunamadi. Once Git for Windows kurun: https://git-scm.com/download/win"
}

Write-Step "Git deposu kontrol ediliyor"
if (-not (Test-Path ".git")) {
  git init | Out-Host
}

Write-Step ".gitignore guvenli varsayilanlarla hazirlaniyor"
$ignoreEntries = @(
  ".venv/",
  "venv/",
  "__pycache__/",
  "*.py[cod]",
  ".pytest_cache/",
  "dist/",
  "build/",
  "*.spec",
  "*.log",
  ".env",
  "jarvis/.env",
  "jarvis/mcp_servers.json",
  ".DS_Store"
)

if (-not (Test-Path ".gitignore")) {
  New-Item -ItemType File -Path ".gitignore" | Out-Null
}

$currentIgnore = Get-Content ".gitignore" -ErrorAction SilentlyContinue
foreach ($entry in $ignoreEntries) {
  if ($currentIgnore -notcontains $entry) {
    Add-Content -Path ".gitignore" -Value $entry
  }
}

Write-Step "Remote origin ayarlaniyor"
$existingOrigin = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0 -and $existingOrigin) {
  git remote set-url origin $RepoUrl | Out-Host
} else {
  git remote add origin $RepoUrl | Out-Host
}

Write-Step "Dosyalar stage ediliyor"
git add . | Out-Host

$stagedChanges = git diff --cached --name-only
if ($stagedChanges) {
  Write-Step "Commit olusturuluyor"
  git commit -m $CommitMessage | Out-Host
} else {
  Write-Host "Commit edilecek yeni degisiklik yok; mevcut commit pushlanacak." -ForegroundColor Yellow
}

Write-Step "Branch $Branch olarak ayarlaniyor"
git branch -M $Branch | Out-Host

Write-Step "GitHub'a pushlaniyor"
git push -u origin $Branch | Out-Host

Write-Host "Tamamlandi. Repo: $RepoUrl" -ForegroundColor Green
