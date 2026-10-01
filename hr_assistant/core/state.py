from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:

    employee_id: str | None = None

    user_query: str | None = None

    language: str = "English"

    intent: str | None = None

    plan: list[dict[str, Any]] = field(default_factory=list)

    tool_results: dict[str, Any] = field(default_factory=dict)

    final_response: str | None = None

    escalation_required: bool = False

    hr_case_id: str | None = None