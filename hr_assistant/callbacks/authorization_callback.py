from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from hr_assistant.guardrails.authorization import (
    is_employee_authorized,
)


def authorize_employee(
    callback_context: CallbackContext,
) -> types.Content | None:

    employee_id = callback_context.user_id

    if not employee_id:
        return types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="Access denied. Employee identity could not be verified."
                )
            ],
        )

    authorized = is_employee_authorized(employee_id)

    if not authorized:
        return types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="Access denied. Your employee identity is not authorized to use this application."
                )
            ],
        )

    # Store verified identity in session state
    callback_context.state["employee_id"] = employee_id
    callback_context.state["authorized"] = True

    return None