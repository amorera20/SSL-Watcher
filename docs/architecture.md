
# System Architecture

This SSL certificate monitoring system is composed of the following components:

- **Python App**: Periodically checks SSL certificate status and exposes metrics.
- **Prometheus**: Scrapes metrics from the Python app.
- **Alertmanager**: Receives alerts from Prometheus and forwards them to Slack.
- **Grafana**: Visualizes SSL metrics using dashboards.
- **Slack**: Receives notifications when alerts are triggered.

All components are deployed in a Kubernetes cluster using Minikube.
