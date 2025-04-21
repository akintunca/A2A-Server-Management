from fastapi import FastAPI

from config import settings
from routers import root_router, agent_router

app = FastAPI(**settings.app_settings.kwargs())

app.include_router(router=root_router, tags=["Root"])
app.include_router(router=agent_router, prefix="/api/v1/agent", tags=["Agent"])
