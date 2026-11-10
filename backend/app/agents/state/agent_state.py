from typing import TypedDict, Any

class AgentState(TypedDict, total=False):
    run_id: str
    case_id: str
    user_message: str
    customer_id: str | None
    merchant_id: str | None
    transaction_ref: str | None

    intent: str
    entities: dict[str, Any]
    txn_data: dict[str, Any] | None
    diagnosis: str
    knowledge_evidence: list[str]
    selected_action: str
    action_args: dict[str, Any]

    risk_level: str
    risk_score: int
    risk_reasons: list[str]
    duplicate_blocked: bool

    needs_approval: bool
    approval_id: str | None
    approval_required_reason: str | None

    tool_calls: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]

    verification: dict[str, Any]
    final_response: str
    status: str
    step_index: int
