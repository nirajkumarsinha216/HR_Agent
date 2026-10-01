class EmployeeAgentError(Exception):
    """Base exception for HR Agent."""


class EmployeeNotFoundError(EmployeeAgentError):
    """Employee was not found."""


class UnauthorizedAccessError(EmployeeAgentError):
    """Employee is not authorized to access this information."""


class ToolExecutionError(EmployeeAgentError):
    """Tool execution failed."""


class RAGRetrievalError(EmployeeAgentError):
    """RAG retrieval failed."""


class HRCaseCreationError(EmployeeAgentError):
    """HR case creation failed."""