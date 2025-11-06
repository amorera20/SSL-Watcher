# SSL-Cert-Watcher
This project provides an SSL monitoring solution built with Flask, Prometheus, Alertmanager, Grafana, and Kubernetes. It periodically checks configured domains, exposes Prometheus‑style metrics, visualizes status in Grafana, and triggers alerts in Slack to ensure that SSL certificates are valid, are close to expiration, or have expired.

## 📦 Features
- Monitors SSL certificate validity and expiration dates
- Exports metrics to Prometheus
- Visualizes data in Grafana dashboards
- Sends alerts to Slack when certificates are invalid or near expiration

## 🏗 Architecture
- Flask App: periodically checks a list of domains and exposes status.
- Prometheus: scrapes /metrics every 1 hour.
- Grafana: visualizes valid certificates and expiring days.
- Alertmanager: alerts on expired certificates and integration with Slack.
- Kubernetes: orchestrates deployment via cert-watcher-deployment.yaml, cert-watcher-service.yaml, etc.

## 🛠 Requirements
- Python 3.8+
- Prometheus
- Alertmanager
- Grafana
- Kubernetes with Minikube (recommended for local testing)
- Slack Webhook URL

## 📂 Project Structure

CERT-WATCHER
.
├──app
│   ├── cert_watcher.py
│   ├── requirements.txt
├── Dockerfile
├── k8s
│   ├── cert-watcher-deployment.yaml
│   ├── cert-watcher-service.yaml
├── monitoring
│   └── alertmanager
│       └── alertmanager-configmap.yaml
|       ├── alertmanager-deployment.yaml
|       ├── alertmanager-service.yaml
|       ├── alertmanager.yml
|   └── grafana
│       └── grafana-deployment.yaml
|       ├── grafana-service.yaml
|   └── prometheus
│       └── alert_rules.yml
|       ├── prometheus-configmap.yaml
|       ├── prometheus-deployment.yaml
|       ├── prometheus-service.yaml
|       ├── prometheus.yml
├── LICENSE.md
├── ssl_dashboard_grafana.json
└── README.md

## 🚀 Installation Steps

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ssl-monitoring
cd ssl-monitoring
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Deploy Prometheus and Alertmanager
Apply the Kubernetes manifests:
```bash
kubectl apply -f prometheus-deployment.yaml
kubectl apply -f alertmanager-deployment.yaml
```

### 4. Deploy Grafana
```bash
kubectl apply -f grafana-deployment.yaml
kubectl apply -f grafana-service.yaml
```
Access Grafana:
```bash
minikube service grafana
```

### 5. Configure Grafana
- Add Prometheus as a data source
- Import the dashboard from `ssl_dashboard_grafana.json`

### 6. Configure Alertmanager
Edit `alertmanager.yml` and set your Slack webhook URL:
```yaml
api_url: '$(SLACK_WEBHOOK)'
```

### 7. Simulate Alerts
Run the checker with an expired domain:
```bash
python ssl_checker.py --domain expired.badssl.com
```

### 8. Port-forward Alertmanager
```bash
kubectl port-forward svc/alertmanager 9093:9093
```

## 🔍 Observability
- Import ssl_dashboard_grafana.json into Grafana.
  - Navigate to your Grafana UI (http://localhost:3000).
  - Go to Dashboards > New Dashboard > Import.
  - Click "Upload JSON file" and select ssl_dashboard_grafana.json from your project directory.
  - Ensure you select Prometheus as the data source when prompted.
    
- Visualizes:
  - SSL valid certificates
  - SSL invalid or expired certificates

## 📸 Screenshots
- Metrics
- Prometheus target UP
- Alertmanager alerts
- Pods running
- Grafana connection with Prometheus
- Grafana dashboard showing SSL certificates data
- Slack alert message for expiring certificate

## 📂 Notes
This repository is part of a practical and final project training series developed for the SRE Academy.
It is optimized for environments like Minikube but can be adapted to other Kubernetes setups.

---
