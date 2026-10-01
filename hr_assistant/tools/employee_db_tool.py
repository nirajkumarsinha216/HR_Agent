import json
from pathlib import Path

from hr_assistant.core.exceptions import (
    EmployeeNotFoundError,
    ToolExecutionError,
)


EMPLOYEE_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "employees"
    / "employees.json"
)


def get_employee_details(employee_id: str) -> dict:
    """
    Retrieve employee information using employee ID.

    Args:
        employee_id: Unique employee identifier.

    Returns:
        Employee information.
    """

    try:
        with open(EMPLOYEE_FILE, "r", encoding="utf-8") as file:
            employees = json.load(file)

        for employee in employees:

            if employee["employee_id"].lower() == employee_id.lower():

                return {
                    "status": "success",
                    "employee": employee
                }

        raise EmployeeNotFoundError(
            f"Employee {employee_id} was not found."
        )

    except EmployeeNotFoundError:
        raise

    except Exception as exc:
        raise ToolExecutionError(
            f"Failed to retrieve employee information: {exc}"
        ) from exc