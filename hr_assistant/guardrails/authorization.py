import json
from pathlib import Path


EMPLOYEE_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "employees"
    / "employees.json"
)


def is_employee_authorized(employee_id: str) -> bool:
    """
    Check whether the authenticated user exists
    in the employee database.
    """

    if not employee_id:
        return False

    with open(EMPLOYEE_FILE, "r", encoding="utf-8") as file:
        employees = json.load(file)

    return any(
        employee["employee_id"].lower() == employee_id.lower()
        for employee in employees
    )