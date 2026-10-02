# from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from hr_assistant.prompt.instruction import HR_ASSISTANT_INSTRUCTION
from hr_assistant.core.config import settings
from hr_assistant.core.logging import setup_logging
from hr_assistant.tools.employee_db_tool import (
    get_employee_details,
    )
from hr_assistant.tools.rag_tool import search_hr_policies
from hr_assistant.callbacks.authorization_callback import authorize_employee

root_agent = Agent(
    model=LiteLlm(model=settings.MODEL,
                  api_base=settings.OLLAMA_HOST,),
    name="hr_assistant",
    description=(
        "An AI assistant that can answer questions about the HR system. "
    ),
    instruction=HR_ASSISTANT_INSTRUCTION,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=False,
            thinking_budget=1024,
        )
    ),
    tools=[get_employee_details, search_hr_policies],
    before_agent_callback=authorize_employee,
)
