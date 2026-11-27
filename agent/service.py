import os
from typing import Literal
from pydantic import BaseModel, Field
from agent.prompt import MAX_TOOL_STEPS, MODEL_ID

class TriageResponse(BaseModel):
    category: Literal["billing", "technical", "account"]
    summary: str = Field(min_length=5, max_length=240)
    tools_used: list[str]

def lookup_account(user_id: str) -> dict[str, str]:
    return {"user_id": user_id, "tier": "pro", "status": "active"}

def run_agent(user_id: str, message: str) -> TriageResponse:
    steps = 0
    tools_used: list[str] = []

    if steps < MAX_TOOL_STEPS:
        _ = lookup_account(user_id)
        tools_used.append("lookup_account")
        steps += 1

    if os.getenv("USE_MOCK_LLM", "true").lower() == "true":
        lowered = message.lower()
        if "invoice" in lowered or "charge" in lowered or "refund" in lowered:
            category: Literal["billing", "technical", "account"] = "billing"
        elif "login" in lowered or "password" in lowered or "mfa" in lowered:
            category = "account"
        else:
            category = "technical"

        return TriageResponse(
            category=category,
            summary=f"[{MODEL_ID}] Triaged request for {user_id}: {message[:120]}",
            tools_used=tools_used,
        )

    raise NotImplementedError("Set USE_MOCK_LLM=true or connect your LLM client.")
