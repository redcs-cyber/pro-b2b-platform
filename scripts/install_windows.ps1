$ErrorActionPreference = "Stop"
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
Write-Host "ProB2B/Jarvis kurulumu tamamlandı." -ForegroundColor Green
