# 3D Görsel Varlık Kataloğu

Bu depo, web paneli ve satış/demo dokümanları için kod tabanlı SVG 3D görseller içerir. SVG seçimi; küçük dosya boyutu, versiyon kontrolü, erişilebilirlik ve hızlı düzenleme avantajı sağlar.

| Asset | Yol | Kullanım |
| --- | --- | --- |
| B2B ekosistem haritası | `api/static/assets/3d/b2b-ecosystem.svg` | ERP, portal, WMS, finans, LLM ve dashboard sunumu. |
| El terminali | `api/static/assets/3d/handheld-terminal.svg` | WMS, barkod, sayım ve toplama akışı. |
| Depo ağı | `api/static/assets/3d/warehouse-network.svg` | Merkez depo, şube ve kargo akışı. |

## Şema

Görsel varlık metadata sözleşmesi `schemas/visual_asset_schema.json` dosyasındadır. Üretimde bu kayıtlar PIM/CDN veya CMS tarafında saklanabilir.
