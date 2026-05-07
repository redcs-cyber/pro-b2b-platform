# ProB2B Platform

ProB2B Platform, paylaşılan ProB2B/Jarvis kurulum paketinden taşınan örnek Python servisleri, Jarvis asistan modülleri, telemetri paneli ve Windows kurulum betiklerini içerir.

## İçerik

- `api/`: FastAPI tabanlı sağlık ve telemetri servisleri.
- `core/`: Platform çekirdek başlatıcısı.
- `jarvis/`: IRONMAN/GOODMOOD odaklı çoklu sağlayıcı asistan paketi.
- `scripts/`: Windows kurulum, çalıştırma ve GitHub'a push betikleri.
- `tests/`: Temel birim testleri.

## Hızlı Başlangıç

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

API başladıktan sonra `http://127.0.0.1:8000` adresini açabilirsiniz.
