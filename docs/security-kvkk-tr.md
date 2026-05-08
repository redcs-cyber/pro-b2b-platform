# Güvenlik, KVKK ve Yetkilendirme Standardı

## Kimlik ve Erişim

- Rollere dayalı erişim: `super_admin`, `dealer_admin`, `buyer`, `approver`, `finance`, `sales_rep`, `warehouse`, `support`.
- Kritik aksiyonlar: fiyat değişikliği, limit onayı, ödeme, iade ve ERP aktarımı audit trail'e yazılır.
- 2FA, IP allowlist ve cihaz güven ilişkisi SaaS ve on-prem kurulumlarda zorunlu kabul edilir.

## KVKK

- `kvkk_consent` müşteri kaydında tutulur.
- Retention varsayılanı `.env.example` içindeki `KVKK_RETENTION_DAYS` ile yönetilir.
- Kişisel veri export/delete talepleri ayrı audit olayı üretmelidir.

## Güvenlik Başlıkları

On-prem Nginx örneği `X-Frame-Options`, `X-Content-Type-Options` ve `Referrer-Policy` başlıklarını uygular. Production ortamda CSP, HSTS ve WAF kuralları eklenmelidir.
