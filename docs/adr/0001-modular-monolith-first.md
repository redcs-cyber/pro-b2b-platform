# ADR-0001: Önce Modüler Monolit

## Karar

ProB2B, ilk fazda tek FastAPI uygulaması içinde modüler domain dosyalarıyla ilerler. ERP/EDI, notification, search ve analytics worker'ları daha sonra ayrı servis olarak çıkarılır.

## Gerekçe

- İş kuralları hızlı değişirken tek repo test hızını artırır.
- Domain sınırları dosya/modül bazında netleştirilir.
- SaaS ve on-prem kurulumlar aynı çekirdeği paylaşır.

## Sonuç

`api/b2b_ecosystem.py`, `api/enterprise_suite.py` ve `api/quick_order.py` ayrı domain modülleri olarak tutulur; veri sözleşmeleri `schemas/` ve `openapi/` altında versiyonlanır.
