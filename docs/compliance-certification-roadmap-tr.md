# Müfredat, Sertifika ve Go-Live Uygunluk Yol Haritası

Kısa cevap: **Kod deposu müfredat ve sertifika hazırlık omurgasını içeriyor; fakat üretim ortamı için sertifikalar “tamamlandı” sayılamaz.** ISO, PCI, KVKK/e-belge ve penetrasyon testi gibi başlıklar dış denetim, hukuk/finans onayı ve gerçek ortam kanıtı ister.

## Zorunlu Go-Live Sertifika / Uygunluk Matrisi

| Kod | Kapsam | Durum | Neden gerekli? | Kanıt dosyaları | Eksik kalan üretim işi |
| --- | --- | --- | --- | --- | --- |
| KVKK-GDPR | Kişisel veri, açık rıza, saklama/imha | Devam ediyor | Cari, kullanıcı, audit, ödeme ve lojistik verileri kişisel veri içerebilir. | `docs/security-kvkk-tr.md`, `.env.example`, `migrations/001_b2b_core.sql` | Veri envanteri, aydınlatma metni, veri işleyen sözleşmeleri, imha job'ı |
| ISO-27001 | Bilgi güvenliği yönetim sistemi | Dış denetim gerekli | Kurumsal B2B müşteriler güvenlik yönetim sistemi kanıtı ister. | `docs/security-kvkk-tr.md`, `docs/runbook-tr.md`, `observability/prometheus/prometheus.yml` | ISMS kapsamı, risk planı, SoA, iç denetim, akredite denetim |
| OWASP-ASVS-L2 | Web/API güvenlik doğrulaması | Devam ediyor | API, bayi portalı, quick order ve ödeme akışları güvenlik testine ihtiyaç duyar. | `openapi/prob2b.openapi.yaml`, `tests/` | Auth/session/access-control testleri, SAST/DAST, pentest bulguları |
| PCI-DSS-4.0.1 | Kartlı ödeme güvenliği | Planlandı | Sanal POS kullanılacaksa kart verisi kapsamı belirlenmeli. | `.env.example`, `docs/enterprise-b2b-ecosystem-tr.md` | Hosted/tokenized ödeme kararı, SAQ tipi, ödeme sağlayıcı AOC |
| E-INVOICE-TR | e-Fatura/e-Arşiv/e-İrsaliye | Devam ediyor | Türkiye B2B finans operasyonunda ERP/e-belge kabul testleri gerekir. | `integrations/erp/*` | Özel entegratör testleri, iptal/iade/irsaliye senaryoları |
| ISO-22301 | İş sürekliliği | Devam ediyor | SaaS/on-prem kesinti, yedek ve geri dönüş tatbikatı gerekir. | `deploy/onprem/scripts/backup_postgres.sh`, `docs/runbook-tr.md` | RPO/RTO onayı, restore testi, kesinti tatbikatı |

## Müfredat Uygunluğu

| Modül | Seviye | Öğrenim çıktısı | Depo kanıtı | Ölçme |
| --- | --- | --- | --- | --- |
| B2B-101 | Temel | Cari hiyerarşi, teklif, sipariş ve stok rezervasyonu | `api/b2b_ecosystem.py` | CARI-99 siparişi oluşturma |
| SEC-201 | Orta | KVKK, ASVS, audit ve güvenli API | `api/compliance.py`, `docs/security-kvkk-tr.md` | Endpoint güvenlik checklist'i |
| ERP-EDI-301 | İleri | ERP mapper, EDI, e-belge kabul testi | `integrations/erp/`, `integrations/edi/` | Sipariş export eşleme ödevi |
| DEVOPS-301 | İleri | Docker, Kubernetes, observability, RPO/RTO | `deploy/`, `observability/` | Kesinti runbook'u hazırlama |
| ARCH-401 | Uzman | Modüler monolitten worker/mikroservise evrim | `docs/mega-repository-plan-tr.md`, `docs/adr/` | Worker ayrışma tasarımı |

## Tamamlanma Kriteri

1. `GET /b2b/compliance/readiness` go-live için `go_live_ready=true` dönmeli.
2. Zorunlu tüm track'ler `evidence_ready` veya dış denetim tamamlandı durumuna çekilmeli.
3. KVKK ve e-belge için hukuk/finans kabul imzası alınmalı.
4. ISO 27001 ve gerekiyorsa PCI DSS için akredite denetim kanıtları arşivlenmeli.
5. Pentest ve SAST/DAST kritik/yüksek bulguları kapatılmalı.

## Sonuç

Bu repo artık “hangi müfredat ve sertifika eksik?” sorusunu teknik olarak izleyebilir. Ancak **sertifika yerine geçmez**; üretime çıkış için dış denetim, gerçek entegrasyon kabul testleri ve şirket içi politika/onay süreçleri zorunludur.
