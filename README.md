# 🚀 DevOps CI/CD Pipeline
A **production-grade CI/CD pipeline** built from scratch — covering everything from application development to containerization, Kubernetes deployment, and full pipeline automation using GitHub Actions.

> Every commit to `main` automatically lints the code, runs tests, builds a Docker image, pushes it to DockerHub, and deploys to a Kubernetes cluster — with zero manual steps.

---

## 📌 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pipeline Stages](#-pipeline-stages)
- [Getting Started](#-getting-started)
- [Running Locally](#-running-locally)
- [Docker](#-docker)
- [Kubernetes](#-kubernetes)
- [GitHub Actions](#-github-actions)
- [API Endpoints](#-api-endpoints)
- [Key Results](#-key-results)
- [Author](#-author)

---

## 🎯 What This Project Does

Most teams write code and manually deploy it — which is slow, error-prone, and inconsistent. This project solves that with a fully automated pipeline.

**The flow is simple:**
1. A developer pushes code to GitHub
2. GitHub Actions automatically kicks off the pipeline
3. The code is linted and tested — if anything fails, the pipeline stops
4. A Docker image is built and pushed to DockerHub
5. The app is deployed to a Kubernetes cluster automatically
6. Kubernetes health checks confirm the app is live

No manual deployments. No "it worked on my machine." Just consistent, reliable delivery.

---

## 🏗️ Architecture

```
  Developer
     │
     │  git push
     ▼
┌─────────────────────────────────────────────────────┐
│                  GitHub Repository                  │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │           GitHub Actions (CI/CD)            │   │
│  │                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │  🔍 Lint │→ │ 🧪 Test  │→ │🐳 Build  │  │   │
│  │  │  flake8  │  │  pytest  │  │  & Push  │  │   │
│  │  └──────────┘  └──────────┘  └────┬─────┘  │   │
│  │                                   │         │   │
│  └───────────────────────────────────┼─────────┘   │
└──────────────────────────────────────┼─────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    DockerHub     │
                              │  hanuhoney/      │
                              │  devops-cicd-    │
                              │  pipeline:latest │
                              └────────┬─────────┘
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │   Kubernetes Cluster     │
                        │                          │
                        │  ┌─────────┐ ┌────────┐  │
                        │  │  Pod 1  │ │  Pod 2 │  │
                        │  │  Flask  │ │  Flask │  │
                        │  │  App    │ │  App   │  │
                        │  └─────────┘ └────────┘  │
                        │        ▲                  │
                        │  ┌─────┴──────┐           │
                        │  │  Service   │           │
                        │  │ (NodePort) │           │
                        │  └───────────┘           │
                        │        ▲                  │
                        │  ┌─────┴──────┐           │
                        │  │    HPA     │ ← scales  │
                        │  │ min:2 max:5│   on load │
                        │  └───────────┘           │
                        └──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Tool | Purpose |
|---|---|---|
| **Application** | Python + Flask | REST API with health endpoints |
| **Testing** | pytest + pytest-cov | Unit tests with 90% coverage |
| **Linting** | flake8 | Code quality enforcement |
| **Containerization** | Docker (multi-stage) | Lightweight production image (~50MB) |
| **Production Server** | Gunicorn | WSGI server (replaces Flask dev server) |
| **Orchestration** | Kubernetes | Container scheduling and management |
| **Autoscaling** | HPA | Auto-scale pods on CPU load |
| **CI/CD** | GitHub Actions | Automated pipeline on every push |
| **Image Registry** | DockerHub | Stores and serves Docker images |
| **Local K8s** | Minikube | Kubernetes cluster on local machine |

---

## 📁 Project Structure

```
devops-cicd-pipeline/
│
├── app/
│   ├── app.py              # Flask application (4 endpoints)
│   ├── requirements.txt    # Python dependencies
│   └── test_app.py         # Unit tests (6 tests, 90% coverage)
│
├── k8s/
│   ├── deployment.yaml     # 2-replica deployment with health probes
│   ├── service.yaml        # NodePort service (exposes the app)
│   └── hpa.yaml            # Auto-scales 2→5 pods at 70% CPU
│
├── .github/
│   └── workflows/
│       ├── ci.yml          # Lint → Test → Build → Push
│       └── cd.yml          # Deploy to Kubernetes
│
├── Dockerfile              # Multi-stage build (builder + final)
├── .dockerignore           # Keeps image lean
└── README.md               # This file
```

---

## ⚙️ Pipeline Stages

### CI Pipeline (`ci.yml`) — runs on every push

```
Push to GitHub
      │
      ▼
┌─────────────┐
│ 🔍 Stage 1  │  Lint
│  flake8     │  Checks code style and formatting
│             │  Fails fast if code quality is poor
└──────┬──────┘
       │ (only if lint passes)
       ▼
┌─────────────┐
│ 🧪 Stage 2  │  Test
│  pytest     │  Runs 6 unit tests
│             │  Coverage must be ≥ 80% or pipeline fails
└──────┬──────┘
       │ (only if tests pass + only on main branch)
       ▼
┌─────────────┐
│ 🐳 Stage 3  │  Build & Push
│  Docker     │  Builds multi-stage image
│             │  Pushes 2 tags to DockerHub:
│             │  → hanuhoney/devops-cicd-pipeline:latest
│             │  → hanuhoney/devops-cicd-pipeline:<git-sha>
└─────────────┘
```

### CD Pipeline (`cd.yml`) — runs after CI succeeds on main

```
CI Pipeline Completed Successfully
              │
              ▼
┌──────────────────────────┐
│ 🚀 Deploy to Kubernetes  │
│                          │
│  1. Spin up kind cluster │  ← Fresh K8s cluster in GitHub Actions
│  2. Pull from DockerHub  │  ← Uses image built by CI
│  3. kubectl apply -f k8s/│  ← Deploys all manifests
│  4. Rollout status check │  ← Waits for pods to be Ready
│  5. Health verification  │  ← Curls /health and /ready
│  6. Show pod status      │  ← Final confirmation
└──────────────────────────┘
```

**Why two separate pipelines?** CI runs on every push (including PRs). CD only runs when CI passes on `main`. This ensures nothing broken ever reaches deployment.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have these installed before starting:

| Tool | Check Command | Install |
|---|---|---|
| Python 3.9+ | `python3 --version` | [python.org](https://python.org) |
| Docker Desktop | `docker --version` | [docker.com](https://docker.com) |
| Minikube | `minikube version` | `brew install minikube` |
| kubectl | `kubectl version` | `brew install kubectl` |
| Git | `git --version` | Pre-installed on Mac |

### Clone the repository

```bash
git clone https://github.com/HanuHoney/devops-cicd-pipeline.git
cd devops-cicd-pipeline
```

---

## 💻 Running Locally

### Install dependencies

```bash
cd app
python3 -m pip install -r requirements.txt
```

### Run tests

```bash
python3 -m pytest test_app.py -v --cov=app --cov-report=term-missing
```

Expected output:
```
test_app.py::test_home_returns_200            PASSED
test_app.py::test_home_returns_json           PASSED
test_app.py::test_health_endpoint             PASSED
test_app.py::test_ready_endpoint              PASSED
test_app.py::test_info_endpoint               PASSED
test_app.py::test_unknown_route_returns_404   PASSED

6 passed — Coverage: 90%
```

### Run the app

```bash
python3 app.py
```

Open your browser → `http://localhost:8080/health`

---

## 🐳 Docker

### What makes this Dockerfile special — Multi-stage build

A regular Dockerfile would result in a ~400MB image because it includes build tools, pip cache, and unnecessary system packages. This project uses a **multi-stage build** to keep it lean.

```
Stage 1 (Builder):   Install all dependencies
                           ↓
Stage 2 (Final):     Copy ONLY the installed packages
                     + Run as non-root user (security)
                     + Use Gunicorn (production server)

Result: ~50MB image instead of ~400MB
```

### Build the image

```bash
docker build -t devops-cicd-pipeline:v1.0.0 .
```

### Run the container

```bash
docker run -p 9090:8080 devops-cicd-pipeline:v1.0.0
```

Open browser → `http://localhost:9090/health`

You'll see Gunicorn start 2 workers:
```
[INFO] Starting gunicorn 22.0.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Booting worker with pid: 7
[INFO] Booting worker with pid: 8
```

### Why Gunicorn and not Flask's built-in server?

Flask's dev server is single-threaded and not safe for production. Gunicorn runs multiple worker processes, handles concurrent requests, and is battle-tested in production environments.

---

## ☸️ Kubernetes

Kubernetes runs your app across multiple containers (called Pods) and automatically restarts them if they crash. Think of it as a smart manager for your Docker containers.

### Start Minikube (local Kubernetes cluster)

```bash
minikube start --driver=docker
```

### Load the Docker image into Minikube

```bash
minikube image load devops-cicd-pipeline:v1.0.0
```

### Deploy everything

```bash
kubectl apply -f k8s/
```

This creates 3 resources:

| Resource | File | What it does |
|---|---|---|
| Deployment | `deployment.yaml` | Runs 2 copies of the app with health checks |
| Service | `service.yaml` | Exposes the app on a stable URL |
| HPA | `hpa.yaml` | Auto-scales from 2 to 5 pods if CPU > 70% |

### Check pod status

```bash
kubectl get pods
```

```
NAME                                    READY   STATUS    RESTARTS   AGE
devops-cicd-pipeline-7758fcb88b-g7xm7   1/1     Running   0          90s
devops-cicd-pipeline-7758fcb88b-lqd4p   1/1     Running   0          90s
```

Both pods `1/1 Running` means Kubernetes verified your app is healthy via the `/health` endpoint before marking them ready.

### Access the app

```bash
minikube service devops-cicd-pipeline-svc --url
```

This gives you a URL like `http://127.0.0.1:49925`. Open `/health` on that URL.

### Understanding the Kubernetes manifests

**`deployment.yaml`** — Key features:
- `replicas: 2` → Always runs 2 instances for availability
- `maxUnavailable: 0` → Zero-downtime rolling updates
- `livenessProbe` → Kubernetes restarts the pod if `/health` fails
- `readinessProbe` → Traffic only sent when `/ready` returns 200
- `resources.limits` → Prevents one pod from using too much CPU/memory

**`hpa.yaml`** — Autoscaling:
- Watches CPU usage across all pods
- Scales up when average CPU > 70%
- Scales down when load decreases
- Never goes below 2 or above 5 pods

---

## 🔁 GitHub Actions

### Setting up secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → add:

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub Access Token (from Account Settings → Security) |

### Watching the pipeline run

After pushing to `main`:
1. Go to your repo on GitHub
2. Click the **Actions** tab
3. You'll see both pipelines running live

Each stage must pass before the next starts. If tests fail, the Docker image never gets built. If CI fails, deployment never happens.

---

## 🌐 API Endpoints

| Endpoint | Method | Description | Response |
|---|---|---|---|
| `/` | GET | Home — app info | `{"message": "...", "version": "1.0.0", "environment": "production"}` |
| `/health` | GET | Liveness probe | `{"status": "healthy", "version": "1.0.0"}` |
| `/ready` | GET | Readiness probe | `{"status": "ready", "environment": "production"}` |
| `/api/info` | GET | App metadata | `{"app": "devops-cicd-pipeline", "maintainer": "Hanu Priya", ...}` |

**Why `/health` and `/ready` separately?**

- `/health` (liveness) → "Is the app running?" — if this fails, Kubernetes restarts the pod
- `/ready` (readiness) → "Is the app ready for traffic?" — if this fails, traffic is rerouted away without restarting

This separation prevents restarts during slow startup while still keeping unhealthy pods out of rotation.

---

## 📊 Key Results

| Metric | Result |
|---|---|
| Test coverage | 90% |
| Docker image size | ~50MB (multi-stage vs ~400MB single-stage) |
| Pipeline execution | ~4 minutes end-to-end |
| Deployment strategy | Zero-downtime rolling update |
| Pod replicas | 2 always running, scales to 5 under load |
| Gunicorn workers | 2 per pod |

---

## 👩‍💻 Author

**Hanu Priya Nagineni**
DevOps & Cloud Engineer | AWS | Kubernetes | Terraform | GitHub Actions

- 🔗 [LinkedIn](https://linkedin.com/in/hanu-priya)
- 🐙 [GitHub](https://github.com/HanuHoney)
- 📧 hanu.nagineni@gmail.com
