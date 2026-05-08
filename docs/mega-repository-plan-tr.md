# ProB2B Dev Kod Deposu Planı

Bu plan, depoyu tek bir MVP'den büyük ölçekli ürün ailesine çevirmek için modül sınırlarını, servisleri ve paketleri tanımlar.

## Yeni Modül Alanları

1. `api/b2b_ecosystem.py`: Cari, ürün, fiyat, sipariş, rezervasyon, ERP job ve audit çekirdeği.
2. `api/enterprise_suite.py`: ACL, workflow kararları, ödeme planı, kargo, iade, bildirim, arama indeksi ve KPI snapshot katmanı.
3. `api/quick_order.py`: Excel/CSV hızlı sipariş parsing altyapısı.
4. `cli/prob2b.py`: Blueprint, CSV teklif ve fixture export komut satırı aracı.
5. `schemas/`: Order, customer ve quick-order veri sözleşmeleri.
6. `openapi/`: Harici ekipler için API sözleşmesi.
7. `observability/`: Prometheus scrape ve Grafana dashboard taslakları.
8. `deploy/saas/k8s/`: Deployment, service, ingress ve autoscaling taslakları.

## Ürünleşme Yol Haritası

| Faz | Hedef | Çıktı |
| --- | --- | --- |
| Faz 1 | Modüler monolit | FastAPI, domain store, test, docs, Docker |
| Faz 2 | Worker ayrışması | ERP/EDI job worker, notification worker, search indexer |
| Faz 3 | Veri platformu | PostgreSQL, Redis, OpenSearch, object storage, BI mart |
| Faz 4 | Çok kiracılı SaaS | Tenant izolasyonu, billing, rate limit, HPA, ingress, audit retention |
| Faz 5 | Global marketplace | Supplier portal, dropship, cross-border tax, multi-currency, SLA engine |

## Geliştirici Komutları

```bash
python -m cli.prob2b blueprint
python -m cli.prob2b quote-csv examples/quick_order.csv --customer-id CARI-99 --branch-id ANKARA-SUBE
python -m cli.prob2b export-fixtures
pytest -q
```
