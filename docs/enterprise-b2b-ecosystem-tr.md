# Tailor-Made Kurumsal B2B Ekosistemi

Bu doküman, sistemi yalnızca otomotiv yedek parça MVP'si olmaktan çıkarıp **ERP + CRM + PIM + finans + lojistik + BI + güvenlik + SaaS/on-prem dağıtım** katmanlarını kapsayan özel yazılım mimarisine taşır.

## Katmanlar

1. **Identity / ACL / KVKK:** Bayi, alt bayi, plasiyer, satın almacı, onaycı, finans ve admin rolleri; 2FA; audit trail.
2. **ERP Köprüsü:** LOGO, SAP, Netsis, Mikro veya özel ERP için REST/SOAP adaptörleri, mapper dosyaları ve kuyruklu job modeli.
3. **EDI:** X12 850 sipariş, X12 810 fatura, EDIFACT ORDERS/INVOIC dosya alışverişi; AS2 veya SFTP taşıma.
4. **PIM:** Teknik katalog, PDF, 3D çizim, montaj kılavuzu, medya/CDN ve ürün attribute sözlüğü.
5. **Fiyat Motoru:** Cari net fiyat, bayi grubu iskontosu, hacim iskontosu, kampanya, para birimi ve vade etkisi.
6. **Bayi Portalı:** Hızlı sipariş, Excel/CSV yükleme, özel fiyat, stok görünürlüğü, onay limitleri.
7. **Finans:** Cari ekstre, açık fatura, vade yaşlandırma, sanal POS, açık hesap, çek/senet ve kredi limit kontrolü.
8. **WMS / El Terminali:** Stok rezervasyon, mal kabul, toplama, sayım, transfer ve sevkiyat doğrulama.
9. **Lojistik:** CreateShipment, GetTrackingStatus, parsiyel sevkiyat ve teslimat kanıtı.
10. **BI / Observability:** Bayi performansı, stok turnover, satış hunisi, anomaly/fraud sinyalleri, log/metric/trace.
11. **Dağıtım:** SaaS için Kubernetes; on-prem için Docker Compose + Nginx + backup scriptleri.
12. **Enterprise Suite:** ACL policy, workflow karar motoru, ödeme planı, kargo, iade, bildirim, arama indeksi ve KPI snapshot.
13. **Compliance / Müfredat:** KVKK, ISO 27001, OWASP ASVS, PCI DSS, e-belge, iş sürekliliği ve eğitim çıktısı readiness matrisi.

## Kritik Dosya Haritası

| Dosya | Görev |
| --- | --- |
| `api/b2b_ecosystem.py` | Tailor-made B2B domain store, fiyat motoru, rezervasyon, ERP job ve audit çekirdeği. |
| `schemas/order_schema.json` | Sipariş JSON Schema sözleşmesi. |
| `migrations/001_b2b_core.sql` | Cari, ürün, fiyat kuralı, rezervasyon ve audit tabloları. |
| `integrations/erp/erp_field_mapping.json` | ERP alan adlarını B2B alanlarına dönüştüren mapper. |
| `integrations/erp/product_sync.xml` | ERP ürün senkronizasyon örneği. |
| `integrations/erp/stock_update.json` | Anlık stok güncelleme örneği. |
| `integrations/erp/price_list.json` | Fiyat ve iskonto kuralı örneği. |
| `integrations/erp/order_export.csv` | ERP sipariş fişi dışa aktarım örneği. |
| `integrations/edi/x12_850_purchase_order.txt` | EDI X12 850 satın alma siparişi örneği. |
| `.env.example` | JWT, encryption, ERP, EDI, ödeme ve KVKK ortam değişkenleri. |
| `deploy/Dockerfile` | API container imajı. |
| `deploy/onprem/docker-compose.yml` | On-prem PostgreSQL, Redis, API ve Nginx ayağa kaldırma taslağı. |
| `deploy/onprem/scripts/backup_postgres.sh` | Günlük/saatlik cron ile çalıştırılabilecek PostgreSQL yedek betiği. |
| `deploy/saas/k8s/prob2b-api-deployment.yaml` | SaaS Kubernetes deployment/service taslağı. |
| `deploy/saas/k8s/prob2b-api-hpa.yaml` | Trafik artışında otomatik yatay ölçekleme taslağı. |
| `deploy/saas/k8s/prob2b-api-ingress.yaml` | TLS ve ingress yönlendirme taslağı. |
| `openapi/prob2b.openapi.yaml` | Harici ekipler ve entegrasyonlar için API sözleşmesi. |
| `observability/prometheus/prometheus.yml` | Prometheus scrape yapılandırması. |
| `observability/grafana/prob2b-overview-dashboard.json` | Grafana dashboard taslağı. |
| `cli/prob2b.py` | Blueprint, CSV teklif ve fixture export CLI aracı. |
| `api/compliance.py` | Sertifika, go-live ve müfredat readiness domain katmanı. |
| `docs/compliance-certification-roadmap-tr.md` | Sertifika/müfredat uygunluk ve eksik aksiyon matrisi. |
| `schemas/compliance_control_schema.json` | Sertifika kontrol kaydı JSON schema sözleşmesi. |

## API Uçları

| Amaç | Metot | Yol |
| --- | --- | --- |
| Platform blueprint | `GET` | `/b2b/platform/blueprint` |
| Cari hiyerarşi | `GET` | `/b2b/customers/tree?root_customer_id=CARI-99` |
| Teklif/fiyat hesaplama | `POST` | `/b2b/quote` |
| Sipariş oluşturma | `POST` | `/b2b/orders` |
| ERP/EDI paketleri | `GET` | `/b2b/integrations/packets` |
| Audit trail | `GET` | `/b2b/audit` |
| Enterprise feature catalog | `GET` | `/b2b/enterprise/features` |
| Workflow karar motoru | `POST` | `/b2b/enterprise/workflow/decide` |
| CSV hızlı sipariş parse | `POST` | `/b2b/quick-order/parse` |
| Kargo oluşturma | `POST` | `/b2b/shipments` |
| İade oluşturma | `POST` | `/b2b/returns` |
| Arama indeksi | `GET` | `/b2b/search/index` |
| KPI snapshot | `GET` | `/b2b/analytics/snapshot` |
| Compliance readiness | `GET` | `/b2b/compliance/readiness` |
| Sertifika matrisi | `GET` | `/b2b/compliance/certifications` |
| Müfredat haritası | `GET` | `/b2b/compliance/curriculum` |
| Eksik go-live aksiyonları | `GET` | `/b2b/compliance/missing-actions` |

## Örnek Teklif

```bash
curl -X POST http://127.0.0.1:8000/b2b/quote \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CARI-99",
    "branch_id": "ANKARA-SUBE",
    "payment_method": "open_account",
    "shipping_address_id": "ADDR-01",
    "lines": [{"sku": "PROD-X", "quantity": 100}],
    "notes": "Acil teslimat"
  }'
```

Bu istek cari net fiyatı, gold bayi iskontosunu, hacim iskontosunu, KDV'yi, kredi limitini ve onay workflow'unu tek cevapta hesaplar.
