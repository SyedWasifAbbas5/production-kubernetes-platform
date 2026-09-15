# Production Kubernetes Platform

A production-style Kubernetes deployment platform built with Docker, Kubernetes, NGINX Ingress, Metrics Server and Horizontal Pod Autoscaling.

This project demonstrates how to containerize, deploy, expose, monitor and automatically scale a Flask application on Kubernetes.

## Architecture

```text
                    Client
                      |
                      v
              +----------------+
              | NGINX Ingress  |
              +----------------+
                      |
                      v
             +-------------------+
             | Kubernetes Service|
             +-------------------+
                      |
              +-------+-------+
              |               |
              v               v
          +-------+       +-------+
          | Pod 1 |       | Pod 2 |
          | Flask |       | Flask |
          |  API  |       |  API  |
          +-------+       +-------+
```

### Monitoring & Autoscaling

```text
             Pods
              |
              v
       Metrics Server
              |
              v
             HPA
              |
              v
       Scale Deployment
          2 -> 5 replicas
```

## Technologies

* Python / Flask
* Docker
* Kubernetes
* kind
* NGINX Ingress Controller
* Metrics Server
* Horizontal Pod Autoscaler
* ConfigMaps
* Kubernetes Secrets
* NetworkPolicy
* Bash
* GitHub Codespaces

## Application

The Flask API provides:

* `/` - Application information
* `/health` - Health endpoint
* `/ready` - Readiness endpoint
* `/api/v1/status` - Application status
* `/api/v1/info` - Runtime information

## Docker

The application uses:

* `python:3.12-slim`
* Gunicorn
* Non-root UID/GID `10001`
* Container healthcheck
* Python bytecode disabled
* Production-style resource configuration

### Build

```bash
docker build -t production-kubernetes-platform:1.0.0 .
```

### Run Locally

```bash
docker run --rm -p 8080:8080 production-kubernetes-platform:1.0.0
```

### Test

```bash
curl http://localhost:8080/health
```

## Kubernetes Deployment

The application is deployed into the `production-platform` namespace.

### Apply Resources

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/network-policy.yaml
```

### Check Deployment

```bash
kubectl get all -n production-platform
```

## Production Features

### Rolling Updates

The Deployment uses a RollingUpdate strategy:

```yaml
strategy:
  type: RollingUpdate
```

Configuration:

```text
maxUnavailable: 0
maxSurge: 1
```

This allows new pods to become available before old pods are removed.

### Health Probes

The application uses:

* Startup probe
* Readiness probe
* Liveness probe

Endpoints:

```text
/health
/ready
```

### Resource Management

Each container has CPU and memory requests and limits:

```text
CPU request:     100m
CPU limit:       500m
Memory request:  128Mi
Memory limit:    256Mi
```

### Horizontal Pod Autoscaling

The HPA is configured for:

```text
Minimum replicas: 2
Maximum replicas: 5
CPU target:       70%
Memory target:    80%
```

The HPA was successfully tested by generating CPU load inside the Kubernetes workload.

During testing:

```text
2 replicas -> 4 replicas
```

After the load stopped, the HPA returned to the configured minimum after the stabilization period.

Check HPA:

```bash
kubectl get hpa -n production-platform
```

### Security

The containers run as a non-root numeric UID.

Security controls include:

* `runAsNonRoot`
* `seccompProfile: RuntimeDefault`
* `allowPrivilegeEscalation: false`
* All Linux capabilities dropped

### Configuration

Application configuration is provided through a ConfigMap.

Sensitive configuration is represented through a Kubernetes Secret.

The repository contains demonstration values only. Production credentials should be supplied through a secure secrets-management solution.

### Network Policy

A Kubernetes NetworkPolicy manifest is included to demonstrate application ingress and egress restrictions.

Enforcement depends on the Kubernetes networking implementation/CNI used by the cluster.

## Ingress

The application is exposed through the NGINX Ingress Controller.

Host:

```text
production-platform.local
```

The Ingress was successfully tested through a local port-forward.

### Port Forward

```bash
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80
```

Then:

```bash
curl -H "Host: production-platform.local" \
  http://127.0.0.1:8080/health
```

The request successfully followed:

```text
Client
  -> NGINX Ingress
  -> Kubernetes Service
  -> Flask Pod
```

## Monitoring

Metrics Server is installed and used by the HPA.

### Node Metrics

```bash
kubectl top nodes
```

### Application Metrics

```bash
kubectl top pods -n production-platform
```

## Troubleshooting

Useful commands:

```bash
kubectl get pods -n production-platform
kubectl describe pod <pod-name> -n production-platform
kubectl logs <pod-name> -n production-platform
kubectl get events -n production-platform --sort-by=.lastTimestamp
kubectl get hpa -n production-platform
kubectl top pods -n production-platform
```

Documentation:

* `docs/troubleshooting.md`
* `docs/deployment.md`
* `docs/security.md`

## Validation Results

The following components were successfully tested in GitHub Codespaces:

| Component                  | Result |
| -------------------------- | ------ |
| Flask application          | Passed |
| Docker build               | Passed |
| Docker container           | Passed |
| Kubernetes deployment      | Passed |
| Kubernetes service         | Passed |
| Health probes              | Passed |
| Metrics Server             | Passed |
| HPA                        | Passed |
| HPA scale-up test          | Passed |
| NGINX Ingress              | Passed |
| End-to-end Ingress routing | Passed |

## Environment

Primary development environment:

```text
GitHub Codespaces
kind Kubernetes cluster
Kubernetes v1.34
```
The Kubernetes manifests can be adapted for a managed Kubernetes environment such as Amazon EKS.

## Project Goals

* Containerization
* Kubernetes workload management
* Production deployment strategies
* Health monitoring
* Autoscaling
* Ingress routing
* Resource management
* Kubernetes security
* Troubleshooting
* Infrastructure configuration

## Author

**Syed Wasif Abbas**
