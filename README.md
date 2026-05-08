# ProB2B Platform

ProB2B Platform, paylaşılan ProB2B/Jarvis kurulum paketinden taşınan örnek Python servisleri, Jarvis asistan modülleri, telemetri paneli ve Windows kurulum betiklerini içerir.

## İçerik

- `api/`: FastAPI tabanlı sağlık ve telemetri servisleri.
- `core/`: Platform çekirdek başlatıcısı.
- `jarvis/`: IRONMAN/GOODMOOD odaklı çoklu sağlayıcı asistan paketi.
- `scripts/`: Windows kurulum, çalıştırma ve GitHub'a push betikleri.
- `tests/`: Temel birim testleri.
- `docs/automotive-ecosystem-tr.md`: Otomotiv yedek parça ekosistemi, API uçları ve el terminali akışı.
- `docs/enterprise-b2b-ecosystem-tr.md`: Tailor-made B2B ERP/CRM/PIM/finans/lojistik/BI mimarisi ve dosya haritası.
- `schemas/`, `integrations/`, `migrations/`, `deploy/`: Sipariş şeması, ERP/EDI örnekleri, veri tabanı migrasyonu ve SaaS/on-prem dağıtım taslakları.
- `api/enterprise_suite.py`, `api/quick_order.py`, `api/compliance.py`, `cli/`, `openapi/`, `observability/`: Workflow, ACL, kargo/iade/bildirim, hızlı sipariş, sertifika/müfredat readiness, CLI, API sözleşmesi ve izlenebilirlik katmanı.

## Otomotiv Yedek Parça Ekosistemi

Platform; parça kataloğu, OEM/araç uyumluluk araması, çok lokasyonlu stok, sipariş yönetimi ve barkodlu el terminali görev kuyruğunun yanında ERP, EDI, CRM, PIM, finans, lojistik, BI, güvenlik, audit, SaaS ve on-prem dağıtım taslakları için genişletilmiş tailor-made B2B çekirdeği sunar. API başladıktan sonra panelden canlı özeti görmek için `http://127.0.0.1:8000`, Swagger için `http://127.0.0.1:8000/docs` adresini açın. Ayrıntılı otomotiv akışı için `docs/automotive-ecosystem-tr.md`, uçtan uca B2B mimarisi için `docs/enterprise-b2b-ecosystem-tr.md`, dev depo yol haritası için `docs/mega-repository-plan-tr.md`, sertifika/müfredat go-live matrisi için `docs/compliance-certification-roadmap-tr.md` dosyasına bakın.

## Hızlı Başlangıç

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

API başladıktan sonra `http://127.0.0.1:8000` adresini açabilirsiniz.
