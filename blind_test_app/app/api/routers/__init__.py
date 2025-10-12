from fastapi import APIRouter
from app.api.routers import (
    auth, 
    users, 
    models, 
    tests, 
    questions, 
    input_pools, 
    answer_logs
)

# Main API router
api_router = APIRouter()

# Entity-based routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(input_pools.router, prefix="/input-pools", tags=["input-pools"])
api_router.include_router(answer_logs.router, prefix="/answer-logs", tags=["answer-logs"])
