
# Grafana Visualization

The Grafana dashboard includes the following panels:

- **Bar Chart**: Shows remaining days before SSL certificate expiration per domain.
- **Status Panel**: Indicates whether the certificate is valid.
- **Table Panel**: Summarizes all domains with their expiration days and validity.

Metrics used:
- `ssl_cert_expiry_days`
- `ssl_cert_valid`

The dashboard is imported using a JSON file and connected to Prometheus as the data source.
