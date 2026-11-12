from fastapi import APIRouter
from app.api.v1 import (
    health, agent, transactions, trustguard, revenue, audit, auth, customers,
    notifications, demo, demo_dashboard,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(agent.router)
api_router.include_router(transactions.router)
api_router.include_router(trustguard.router)
api_router.include_router(revenue.router)
api_router.include_router(audit.router)
api_router.include_router(auth.router)
api_router.include_router(customers.router)
api_router.include_router(notifications.router)
api_router.include_router(demo.router)
api_router.include_router(demo_dashboard.router)
