"""Response utilities for ROS MCP Server."""


def _check_response(response):
    """Check if a rosbridge response indicates success.

    Args:
        response: The response dict from rosbridge.

    Returns:
        None if success, or a dict with "error" key if there's an issue.
    """
    if response is None:
        return {"error": "No response received"}

    if not response:
        return {"error": "Empty response received"}

    # Check if result key exists and is True
    if response.get("result") is True:
        return None

    # Response indicates failure
    error_msg = _extract_error(response)
    return {"error": error_msg}


def _safe_get_values(response):
    """Safely extract values from response.

    Args:
        response: The response dict from rosbridge.

    Returns:
        The values dict if present, None otherwise.
    """
    if response is None:
        return None

    return response.get("values")


def _extract_error(response):
    """Extract error message from response.

    Args:
        response: The response dict from rosbridge.

    Returns:
        The error message string.
    """
    if response is None:
        return "No response"

    values = _safe_get_values(response)
    if values and "message" in values:
        return values["message"]

    return "Unknown error"
