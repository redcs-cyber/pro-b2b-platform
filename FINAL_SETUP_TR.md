# ProB2B/Jarvis Final Kurulum

## 1) Ortam

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Çalıştırma

```powershell
python run.py
```

## 3) Jarvis Local/Hybrid

```powershell
cd jarvis
python -m jarvis.main --mode local --visual --ironman
python -m jarvis.main --mode hybrid --visual --ironman
```

## 4) Paketleme

```powershell
pyinstaller run.py --onefile --name Jarvis
```

Çıktı: `dist/Jarvis.exe`

## 5) GitHub'a Push (PowerShell)

GitHub'da boş bir repo oluşturduktan sonra repo URL'sini aşağıdaki komuta verin:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/push_to_github.ps1 -RepoUrl "https://github.com/KULLANICI_ADI/REPO_ADI.git" -Branch main -CommitMessage "Initial ProB2B/Jarvis setup"
```

Betik `.gitignore` güvenli varsayılanlarını tamamlar, `origin` remote'unu ayarlar, değişiklik varsa commit oluşturur ve seçilen branch'i GitHub'a pushlar.

## 6) GitHub Actions Artifact

Push sonrası: **Actions > build > Artifacts > Jarvis**

## 7) Sorun Giderme

- `ModuleNotFoundError`: `pip install -r requirements.txt`
- `dashboard boş`: `jarvis/telemetry/events.jsonl` oluştuğunu kontrol et
- `ollama timeout`: `OLLAMA_URL` ve model adını `.env` içinde doğrula
