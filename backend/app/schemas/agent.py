from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


def to_camel(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AgentRunRequest(CamelModel):
    message: str = Field(..., min_length=2)
    customer_id: str | None = None
    merchant_id: str | None = None
    transaction_ref: str | None = None


class AgentStep(CamelModel):
    step: int
    name: str
    status: str
    detail: str | None = None
    evidence: dict | None = None


class ToolCallOut(CamelModel):
    id: str
    name: str
    args: dict
    result: dict | None = None
    status: str
    error: str | None = None


class AgentRunOut(CamelModel):
    run_id: str
    case_id: str
    status: str
    intent: str | None = None
    root_cause: str | None = None
    selected_action: str | None = None
    risk_level: str | None = None
    steps: list[AgentStep] = Field(default_factory=list)
    tool_calls: list[ToolCallOut] = Field(default_factory=list)
    final_response: str | None = None
    knowledge_evidence: list[str] = Field(default_factory=list)
    verified: bool = False
    created_at: datetime
    updated_at: datetime
