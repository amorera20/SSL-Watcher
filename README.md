# SSL-Cert-Watcher
This project provides an SSL monitoring solution built with Flask, Prometheus, Alertmanager, Grafana, and Kubernetes. It periodically checks configured domains, exposes Prometheus‑style metrics, visualizes status in Grafana, and triggers alerts in Slack to ensure that SSL certificates are valid, close to expiration, or have expired.

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
- Colima
- Docker
- Minikube
- Kubectl
- Prometheus
- Alertmanager
- Grafana
- Slack Webhook URL

## 📂 Project Structure

CERT-WATCHER
```
├── app
│   └── cert_watcher.py
│   ├── requirements.txt
├── Dockerfile
├── k8s
│   └── cert-watcher-deployment.yaml
│   ├── cert-watcher-service.yaml
├── monitoring
│   └── alertmanager
│       └── alertmanager.yml
|       ├── alertmanager-deployment.yaml
|       ├── alertmanager-configmap.yaml
|       ├── alertmanager-service.yaml
|   └── grafana
│       └── grafana-deployment.yaml
|       ├── grafana-service.yaml
|   └── prometheus
│       └── alert_rules.yml
|       ├── prometheus-configmap.yaml
|       ├── prometheus-deployment.yaml
|       ├── prometheus-service.yaml
|       ├── prometheus.yml
├── LICENSE
├── ssl_dashboard_grafana.json
└── README.md
```

## 🚀 Installation Steps (This project is optimized for macOS environments)

### 1. Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

### 2. Install Required Tools
```bash
brew install python
brew install colima
brew install docker
brew install minikube
brew install kubectl
```

### 3. Verification
```bash
python3 --version
docker --version
minikube version
kubectl version --client
```

### 4. Start Colima, build a local image, and check for the created image.
```bash
colima start --cpu 4 --memory 6 --disk 60
docker version
docker build -t cert-watcher:latest .
docker images | grep cert-watcher
```

### 5. Start Minikube
```bash
minikube start
kubectl get nodes
```

### 6. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 7. Install Prometheus + Grafana (kube-prometheus-stack)
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

### 8. Deploy Prometheus and Alertmanager
Apply manifests:
```bash
kubectl apply -f monitoring/prometheus/
kubectl apply -f monitoring/alertmanager/
```
### 9. Port-forward Alertmanager
```bash
kubectl port-forward svc/alertmanager 9093:9093
```

### 10. Create ConfigMap
```bash
kubectl create configmap prometheus-config \
  --from-file=prometheus.yml \
  --from-file=alert_rules.yml
```

### 11. Configure Alertmanager
Edit `alertmanager.yml` and set your Slack webhook URL:
```yaml
api_url: '$(SLACK_WEBHOOK)'
```
```bash
kubectl apply -f monitoring/alertmanager/alertmanager.yml
```

### 12. Deploy Grafana
```bash
kubectl apply -f monitoring/grafana/grafana-deployment.yaml
kubectl apply -f monitoring/grafana/grafana-service.yaml
```

### 13. Check Pods
```bash
kubectl get pods
```

### 14. Check Services
```bash
kubectl get svc
```

### 15. Check Prometheus target & metrics
- Port-forward Prometheus and open UI:
```bash
# find Prometheus service name
kubectl get svc
# port-forward (common service name below; if different, use the actual name from svc list)
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```
- Open in browser: http://localhost:9090
• Go to Status → Targets and look for cert-watcher target. Status should be UP.
• Query metrics: ssl_cert_days_left in Prometheus Graph → Execute.

### 16. Configure Grafana
- Check Grafana pod and service status
```bash
kubectl get pods -l app=grafana
kubectl get svc grafana
```
- Enter Grafana dashboard
```bash
kubectl port-forward svc/grafana 3000:3000
```
- In your browser, go to:
```bash
http://localhost:3000
```
## 🔍 Observability
- Import ssl_dashboard_grafana.json into Grafana.
  - Navigate to your Grafana UI (http://localhost:3000).
  - Go to Dashboards > New Dashboard > Import.
  - Click "Upload JSON file" and select ssl_dashboard_grafana.json from your project directory.
  - Ensure you select Prometheus as the data source when prompted.
  - In the URL write:
```bash
http://prometheus:9090
```
- Click on Save & Test

- Visualizes:
  - SSL valid certificates
  - SSL invalid or expired certificates

### 17. Simulate Alerts
Run the checker with an expired domain:
```bash
python ssl_checker.py --domain expired.badssl.com
```

### 18. Verify in Prometheus
- Port forwarding:
```bash
kubectl port-forward svc/prometheus 9090:9090
```
- Access Prometheus:
```bash
http:localhost:9090
```
- Query the metrics:
```bash
ssl_cert_expiry_days
ssl_cert_valid
```
- Confirm that the values reflect the alert status (for example, days < 10 or validity = 0).

### 19. Verify in Alertmanager
- Port forwarding:
```bash
kubectl port-forward svc/alertmanager 9093:9093
```
- Access Alertmanager:
```bash
http:localhost:9093
```
- Check that the alert is active and that it has the label severity: warning.

### 20. Verify in Slack
- Make sure you have correctly configured the Slack Webhook in Alertmanager:
```bash
receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
        channel: '#slack-channel'
        title: '{{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'
```
- Verify that the message reaches the Slack channel.
    
## 📸 Screenshots
This folder contains screenshots that validate the project’s functionality.
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
