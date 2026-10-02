from hr_assistant.rag.retriever import search_policies


def search_hr_policies(query: str) -> dict:
    """
    Search official LALA Company HR policies.

    Use this tool for questions about:
    - leave
    - benefits
    - HR policies
    - attendance
    - payroll policies
    - employee procedures
    - company rules
    """

    results = search_policies(query=query, top_k=5)

    if not results:
        return {
            "status": "no_results",
            "message": "No relevant HR policy information was found."
        }

    return {
        "status": "success",
        "results": results
    }