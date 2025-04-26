from fastapi import APIRouter

router = APIRouter(prefix="/api/dashboard")

@router.get("/status")
async def get_status():
    # Dummy data - replace with real DB call later
    return {
        "status": "online",
        "node_count": 4,
        "last_updated": "2023-11-15T10:00:00Z"
    }

@router.get("/node_status")
async def get_node_status():

    return