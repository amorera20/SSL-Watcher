
# Alert Flow

The alert flow for SSL certificate expiration is as follows:

1. **Python App** exports metrics:
   - `ssl_cert_expiry_days{domain="example.com"}`
   - `ssl_cert_valid{domain="example.com"}`

2. **Prometheus** evaluates alert rules:
   ```
   alert: SSLCertificateExpiringSoon
   expr: ssl_cert_expiry_days < 10
   for: 1m
   ```

3. **Alertmanager** receives the alert and routes it to Slack using a webhook.

4. **Slack** displays the alert message in the configured channel.
