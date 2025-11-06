from flask import Flask, Response
import ssl
import socket
import datetime
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

DOMAINS = [
    "google.com",
    "amazon.com",
    "github.com",
    "your-new-domain.com",
    "ibm.com",
    "127.0.0.1",
    "expired.badssl.com"
]

# Prometheus metrics
cert_expiry_days = Gauge("ssl_cert_expiry_days", "Days until SSL certificate expires", ["domain"])
cert_valid = Gauge("ssl_cert_valid", "Whether SSL certificate is valid (1=valid, 0=invalid)", ["domain"])

def check_cert(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (expiry_date - datetime.datetime.utcnow()).days
                cert_expiry_days.labels(domain=domain).set(days_left)
                cert_valid.labels(domain=domain).set(1 if days_left > 0 else 0)
    except Exception:
        cert_expiry_days.labels(domain=domain).set(-1)
        cert_valid.labels(domain=domain).set(0)

@app.route("/metrics")
def metrics():
    for domain in DOMAINS:
        check_cert(domain)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)