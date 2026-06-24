# Employee Directory API

A REST API built with FastAPI and PostgreSQL, containerised with Docker, and deployed on Google Kubernetes Engine (GKE) as part of a Kubernetes multi-tier deployment assignment.

---

## Links

| Resource | URL |
|----------|-----|
| GitHub Repository | https://github.com/ashishpanzade/employee-api.git |
| Docker Hub Image | https://hub.docker.com/r/ashishpanz/employee-api/tags |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 with connection pooling |
| Server | Uvicorn |
| Containerisation | Docker + Docker Compose |
| Registry | Docker Hub |
| Orchestration | Kubernetes (GKE Autopilot) |
| Cloud | Google Cloud Platform (us-central1) |

---

## Project Structure

```
k8s-employee-api/
├── api/
│   ├── main.py                          # App entry point, health route, router registration
│   ├── routers/
│   │   └── employees.py                 # HTTP layer — routes, status codes, HTTP exceptions
│   ├── services/
│   │   └── employee_service.py          # Orchestration layer — business logic
│   ├── repositories/
│   │   └── employee_repository.py       # Data access layer — all DB queries
│   ├── models/
│   │   └── employee.py                  # SQLAlchemy ORM model (persistence)
│   ├── schemas/
│   │   └── employee.py                  # Pydantic request/response schemas
│   └── db/
│       ├── database.py                  # PostgreSQL connection + session management
│       └── seed.py                      # Seeds 8 employee records on first startup
├── k8s/
│   ├── db-secret.yaml                   # PostgreSQL password (K8s Secret)
│   ├── db-configmap.yaml                # PostgreSQL DB name and user (ConfigMap)
│   ├── db-pvc.yaml                      # 1Gi persistent disk for PostgreSQL data
│   ├── db-deployment.yaml               # PostgreSQL pod (1 replica)
│   ├── db-service.yaml                  # ClusterIP Service — internal only
│   ├── api-configmap.yaml               # DB host, port, name, user for API
│   ├── api-deployment.yaml              # API pods (4 replicas)
│   ├── api-service.yaml                 # NodePort Service with NEG + BackendConfig
│   ├── api-backendconfig.yaml           # GKE health check config (/health path)
│   ├── hpa.yaml                         # HorizontalPodAutoscaler (4-8 replicas, 50% CPU)
│   └── ingress.yaml                     # GCE Ingress — exposes API externally
├── Dockerfile
├── docker-compose.yml                   # Local development stack
├── requirements.txt
└── .env.example
```

### Layer Responsibilities

| Layer | Folder | Responsibility |
|-------|--------|---------------|
| HTTP | `routers/` | Routes, status codes, HTTPException |
| Orchestration | `services/` | Business logic, coordinates repositories |
| Data Access | `repositories/` | All `db.query()` calls, no business logic |
| Persistence Model | `models/` | SQLAlchemy ORM table definitions |
| API Contract | `schemas/` | Pydantic request/response shapes |
| Infrastructure | `db/` | Connection pool, session lifecycle, seeding |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness check for Kubernetes probes |
| GET | `/employees` | List all employees |
| GET | `/employees/{id}` | Get single employee by ID (404 if not found) |
| POST | `/employees` | Create a new employee (returns 201) |

### Sample Response — `GET /employees/1`

```json
{
  "id": 1,
  "name": "Rohit Sharma",
  "department": "Engineering",
  "role": "Backend Engineer",
  "salary": "95000.00",
  "city": "Mumbai",
  "joined_on": "2021-03-15"
}
```

### Sample Request — `POST /employees`

```json
{
  "name": "Rahul Singh",
  "department": "Engineering",
  "role": "SRE",
  "salary": 92000,
  "city": "Pune",
  "joined_on": "2024-01-15"
}
```

---

## Kubernetes Architecture

```
Internet
   │
   ▼
GCP HTTP Load Balancer (Ingress)
   │
   ▼
api-service (NodePort)
   │
   ├──► api pod 1 (ashishpanz/employee-api:v1)
   ├──► api pod 2 (ashishpanz/employee-api:v1)
   ├──► api pod 3 (ashishpanz/employee-api:v1)     ← HPA manages 4-8 pods
   └──► api pod 4 (ashishpanz/employee-api:v1)
              │
              │  DB_HOST=postgres-service (K8s DNS, no pod IPs)
              ▼
        postgres-service (ClusterIP — internal only)
              │
              ▼
        postgres pod (postgres:15)
              │
              ▼
        PVC → GCP Persistent Disk (1Gi) ← data survives pod restarts
```

---

## Kubernetes Requirements Coverage

| Requirement | Implementation |
|-------------|---------------|
| API exposed externally | GCE Ingress |
| API pods = 4 | `replicas: 4` in api-deployment.yaml |
| Rolling updates | `strategy: RollingUpdate` (K8s default) |
| API ConfigMap | api-configmap.yaml (DB_HOST, DB_PORT, DB_NAME, DB_USER) |
| API Secrets | postgres-secret (DB_PASSWORD) |
| DB internal only | ClusterIP Service, no external exposure |
| DB pods = 1 | `replicas: 1` in db-deployment.yaml |
| DB persistent storage | PVC backed by GCP Persistent Disk |
| DB ConfigMap | db-configmap.yaml (POSTGRES_DB, POSTGRES_USER) |
| DB Secrets | postgres-secret (POSTGRES_PASSWORD) |
| No pod IPs | All comms via Service DNS names |
| HPA | api-hpa: 4-8 replicas at 50% CPU threshold |

---

## FinOps Considerations

### Resource Requests and Limits

| Container | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|------------|-----------|----------------|--------------|
| API | 250m | 500m | 256Mi | 512Mi |
| PostgreSQL | 250m | 500m | 256Mi | 512Mi |

### Three Cost Optimisation Opportunities

1. **GKE Autopilot over Standard** — Pay per pod request, not per idle node. Zero cost when nothing is deployed.

2. **HPA scale-down** — At low traffic HPA maintains minimum 4 pods. Under zero load it would scale to `minReplicas`. No manual intervention needed to save cost overnight or on weekends.

3. **Right-sized requests** — API uses 250m CPU request (not 1000m). PostgreSQL at 256Mi memory (not 1Gi). Each over-provisioned millicores/MiB directly increases billing in Autopilot.

---

## Running Locally

```bash
git clone https://github.com/ashishpanzade/employee-api.git
cd k8s-employee-api
docker compose up --build
```

Test:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/employees
```

Swagger UI: http://localhost:8000/docs

---

## Docker Images

```bash
docker pull ashishpanz/employee-api:v1
```
