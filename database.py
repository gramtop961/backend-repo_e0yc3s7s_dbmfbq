import os
from typing import Any, Dict, List, Optional
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client = None


def _get_motor_client():
    global _client
    if _client is None:
        try:
            from motor.motor_asyncio import AsyncIOMotorClient  # lazy import to avoid startup crash if motor missing
        except Exception as e:
            raise RuntimeError(f"Motor not available: {e}")
        _client = AsyncIOMotorClient(DATABASE_URL)
    return _client


def db():
    return _get_motor_client()[DATABASE_NAME]


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    data = {**data, "created_at": now, "updated_at": now}
    res = await db()[collection_name].insert_one(data)
    data["_id"] = str(res.inserted_id)
    return data


async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 20) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    cursor = db()[collection_name].find(filter_dict or {}).limit(limit)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # stringify ObjectId
        items.append(doc)
    return items
