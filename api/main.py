from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.db.seed import seed
from api.routers import employees as employees_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs once at startup to create table and load initial data
    seed()
    yield


app = FastAPI(
    title="Employee Directory API",
    description="""
A simple employee directory service built as part of a Kubernetes multi-tier deployment.
The service connects to a PostgreSQL database running in the same cluster and exposes employee records over REST.
- **API tier** - this service (FastAPI + Python)
- **Database tier** - PostgreSQL with persistent storage
""",
    version="2.0.0",
    lifespan=lifespan,
    contact={
        "name": "Ashish Panzade",
        "email": "ashish.panzade@gmail.com",
    },
)


@app.get("/health", tags=["Health"], summary="Health check")
def health_check():
    """
    Basic liveness check used by Kubernetes probes.
    Returns 200 OK if the service is up. No DB call here intentionally.
    don't want K8s to kill the pod just because the DB is slow.
    """
    return {"status": "ok", "version": "2.0.0"}


app.include_router(employees_router.router)
