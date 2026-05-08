# ProB2B Profesyonel Başlatma → Final Runbook

## A. Geliştirici Başlangıcı

1. Repo çekilir.
2. Python venv açılır.
3. `pip install -r requirements.txt` çalıştırılır.
4. `pytest -q` ile domain kuralları doğrulanır.
5. `python run.py` ile lokal API başlatılır.

## B. Teknik Kabul

| Kontrol | Komut | Beklenen |
| --- | --- | --- |
| Self check | `python tools/self_check.py` | `Self check passed` |
| Test | `pytest -q` | Tüm testler yeşil |
| Vercel hazırlık | `python scripts/vercel_deploy_check.py` | `Vercel deploy check passed` |
| Şema/görsel validasyon | JSON/SVG parse | Hata yok |

## C. Fonksiyonel Kabul

- B2B teklif ve sipariş oluşturma.
- Atomik stok rezervasyon rollback testi.
- El terminali görev kuyruğu.
- LLM görev planlama ve guardrail kontrolü.
- Compliance readiness ve eksik go-live aksiyonları.
- 3D SVG dashboard görselleri.

## D. Final Yayın

1. Vercel project link.
2. Production env girişi.
3. `vercel build --prod`.
4. `vercel deploy --prebuilt --prod`.
5. `/health`, `/b2b/platform/blueprint`, `/b2b/llm/capabilities`, `/b2b/compliance/readiness` smoke test.
6. Sürüm etiketi ve release notu.

## E. Operasyon Devri

- `docs/runbook-tr.md` operasyon ekibine teslim edilir.
- `docs/security-kvkk-tr.md` hukuk/security ekibine teslim edilir.
- `docs/compliance-certification-roadmap-tr.md` yönetim ve denetim ekibine teslim edilir.
- Vercel dashboard erişimleri least-privilege prensibiyle verilir.
