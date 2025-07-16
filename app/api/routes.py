from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.mcp import MCPOrchestrator
from typing import Any

router = APIRouter()

class KVIn(BaseModel):
    key: str
    value: Any

class KVOut(BaseModel):
    status: str
    key: str

@router.post("/kv", response_model=KVOut)
async def post_kv(kv: KVIn):
    orchestrator = MCPOrchestrator()
    task = {"key": kv.key, "value": kv.value}
    res = await orchestrator.run(["kv_store"], task)
    if res.get("status") != "success":
        raise HTTPException(status_code=500, detail=res.get("message"))
    return res
