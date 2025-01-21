from fastapi import APIRouter
from app.settings import check_redis_health

router = APIRouter()

@router.get("/redis-health")
def redis_health():
    if check_redis_health():
        return {"status": "Redis is connected!"}
    return {"status": "Failed to connect to Redis!"}
