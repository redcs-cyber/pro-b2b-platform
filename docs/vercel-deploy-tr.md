# ProB2B Vercel Yayın Rehberi

Bu dosya, projeyi **başlatma kısmından finale kadar** Vercel'e profesyonel şekilde taşımak için BT mühendisi runbook'udur. Bu repo Vercel'e hazırdır; gerçek yayın için Vercel hesabı, proje bağlantısı ve ortam değişkenleri gerekir.

## 1. Ön Kontrol

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python scripts/vercel_deploy_check.py
```

## 2. Vercel CLI Kurulumu

```bash
npm i -g vercel
vercel login
```

## 3. Projeyi Vercel'e Bağla

```bash
vercel link
```

Komut tamamlanınca `.vercel/project.json` lokal makinede oluşur. Bu dosya repoya commit edilmemelidir.

## 4. Production Ortam Değişkenleri

Vercel Dashboard veya CLI ile aşağıdaki değişkenleri girin:

| Değişken | Açıklama |
| --- | --- |
| `PROB2B_MODE=vercel` | Vercel çalışma modu. |
| `PYTHONPATH=.` | `api.*` modül importları için gereklidir. |
| `JWT_SECRET` | Production güçlü secret. |
| `ENCRYPTION_KEY` | 32 byte veya KMS tabanlı anahtar. |
| `ERP_ADAPTER` | LOGO/SAP/NETSIS/MIKRO/CUSTOM adapter seçimi. |
| `OLLAMA_URL`, `OPENAI_BASE_URL`, `AZURE_OPENAI_ENDPOINT` | LLM rota ayarları; kullanılmayan boş bırakılabilir. |

## 5. Build ve Deploy

Manuel:

```bash
vercel pull --yes --environment=production
vercel build --prod
vercel deploy --prebuilt --prod
```

Script ile:

```bash
export VERCEL_ORG_ID="..."
export VERCEL_PROJECT_ID="..."
scripts/deploy_vercel.sh
```

## 6. Yayın Sonrası Kabul Testleri

Aşağıdaki URL'lerde 200 yanıtı beklenir:

```bash
curl https://<proje>.vercel.app/health
curl https://<proje>.vercel.app/b2b/platform/blueprint
curl https://<proje>.vercel.app/b2b/llm/capabilities
curl https://<proje>.vercel.app/b2b/compliance/readiness
```

Dashboard için:

```text
https://<proje>.vercel.app/
```

## 7. Final Kontrol Listesi

- [ ] `pytest -q` yeşil.
- [ ] `python scripts/vercel_deploy_check.py` yeşil.
- [ ] Vercel env değişkenleri production'a girildi.
- [ ] Dashboard 3D görselleri yüklüyor.
- [ ] `/b2b/platform/blueprint` data files içinde `vercel` deploy path'i görünüyor.
- [ ] `/b2b/compliance/readiness` go-live gap'lerini doğru gösteriyor.
- [ ] Log ve analytics kontrol edildi.

## Not

Bu çalışma canlı Vercel hesabına erişim olmadığı ortamda deploy'u gerçekleştirmez; deploy edilebilir dosyaları, script'i, config'i ve kabul testlerini hazırlar.
