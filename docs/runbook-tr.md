# Operasyon Runbook

## Günlük Kontroller

1. `/health` ile API sağlık kontrolü.
2. `/b2b/analytics/snapshot` ile sipariş, GMV, rezervasyon ve bekleyen finans onayları.
3. `/b2b/integrations/packets` ile ERP/EDI kuyruğu.
4. `deploy/onprem/scripts/backup_postgres.sh` yedek çıktıları.

## Olay Müdahalesi

- ERP kuyruğu birikirse integration worker durumu ve ERP adapter kimlik bilgileri kontrol edilir.
- Stok rezervasyon uyuşmazlığında branch/warehouse stokları ERP `stock_update.json` sözleşmesiyle tekrar senkronize edilir.
- Ödeme veya iade problemi için audit trail, payment plan ve notification queue birlikte incelenir.
