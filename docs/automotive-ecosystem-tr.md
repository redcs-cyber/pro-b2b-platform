# Otomotiv Yedek Parça Ekosistemi

Bu proje artık ProB2B/Jarvis temelinin üzerine kurulmuş bir otomotiv yedek parça MVP çekirdeği içerir. Amaç; B2B parça satışı, depo operasyonu, servis/müşteri siparişleri ve el terminali görevlerini tek API ve panel altında toplamaktır.

## Modüller

1. **Parça kataloğu:** SKU, marka, kategori, OEM numarası ve araç uyumluluk bilgisi.
2. **Uyumluluk araması:** Parça adı, SKU, marka, OEM veya araç modeli ile arama.
3. **Çok lokasyonlu stok:** Merkez depo, mağaza, servis ve saha aracı stokları.
4. **Sipariş yönetimi:** B2B portal, telefon, pazaryeri veya el terminali kanalı ile sipariş.
5. **El terminali kuyruğu:** Sayım, mal kabul, sipariş toplama, raf transferi ve teslimat görevleri.
6. **Operasyon paneli:** Dashboard üzerinden ekosistem durumu ve örnek terminal iş akışları.

## API Uçları

| Amaç | Metot | Yol |
| --- | --- | --- |
| Ekosistem özeti | `GET` | `/automotive/overview` |
| Parça ara/listele | `GET` | `/automotive/parts?q=fren&vehicle=bmw` |
| Parça ekle | `POST` | `/automotive/parts` |
| Stok listesi | `GET` | `/automotive/inventory` |
| Stok güncelle | `PUT` | `/automotive/inventory/{sku}` |
| Sipariş oluştur | `POST` | `/automotive/orders` |
| Siparişleri listele | `GET` | `/automotive/orders` |
| El terminali görevi oluştur | `POST` | `/automotive/terminal/tasks` |
| Terminal görevlerini listele | `GET` | `/automotive/terminal/tasks?terminal_id=HT-01` |
| Terminal görev durumu | `PATCH` | `/automotive/terminal/tasks/{task_id}/done` |

## El Terminali İş Akışı

1. Operatör Android el terminalinde veya PWA ekranda `terminal_id` ile oturum açar.
2. `/automotive/terminal/tasks?terminal_id=HT-01` ile açık görevler çekilir.
3. Barkod/OEM/SKU okutulur ve görevdeki SKU ile eşleştirilir.
4. Toplanan veya sayılan miktar doğrulanır.
5. Görev `in_progress`, sonra `done` durumuna alınır.
6. Sipariş, depo ve telemetri kayıtları aynı platformda izlenir.

## Örnek Sipariş

```bash
curl -X POST http://127.0.0.1:8000/automotive/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Ankara Oto Servis",
    "channel": "b2b_portal",
    "lines": [{"sku": "FRN-BLK-001", "quantity": 2}]
  }'
```

Sipariş oluşturulduğunda sistem otomatik olarak `HT-01` için bir **toplama** görevi açar.
