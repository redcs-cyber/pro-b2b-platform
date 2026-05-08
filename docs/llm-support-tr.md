# LLM Destek Katmanı

ProB2B LLM desteği doğrudan dış modele çağrı yapmaz; önce güvenli bir **görev planı** üretir. Bu sayede KVKK/PII maskeleme, insan onayı, ERP/finans doğrulaması ve tool erişimleri merkezi olarak yönetilir.

## Desteklenen Sağlayıcı Rotaları

| Rota | Kullanım | Not |
| --- | --- | --- |
| `local-rules` | Deterministik offline yanıt ve test | Varsayılan, dış çağrı yok. |
| `ollama-local` | Yerel ağda LLM | `OLLAMA_URL` ile ayarlanır. |
| `openai-compatible` | Tool destekli LLM | `OPENAI_BASE_URL` ile uyumlu endpoint. |
| `azure-openai` | Kurumsal tenant | `AZURE_OPENAI_ENDPOINT` ile ayarlanır. |
| `offline-review-queue` | İnsan onayı gerekli işler | Compliance ve SQL rapor gibi riskli işler. |

## Görev Tipleri

- `support_reply`: bayi destek yanıtı.
- `quote_summary`: teklif/iskonto/KDV açıklaması.
- `compliance_gap`: sertifika ve go-live eksik analizi.
- `product_copy`: PIM ürün açıklaması.
- `sql_report`: BI rapor taslağı.
- `integration_debug`: ERP/EDI mapper ve kuyruk analizi.

## API

```bash
curl http://127.0.0.1:8000/b2b/llm/capabilities
curl -X POST http://127.0.0.1:8000/b2b/llm/tasks/plan \
  -H "Content-Type: application/json" \
  -d '{"task_type":"quote_summary","prompt":"CARI-99 teklifini bayi dilinde açıkla","context":{"requires_tools":true}}'
```

Görev planı çıktı olarak provider route, system prompt, guardrail, tool listesi ve beklenen JSON output schema döndürür.
