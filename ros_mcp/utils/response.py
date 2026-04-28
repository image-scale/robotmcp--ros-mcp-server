"""Response utilities for ROS MCP Server."""


def _check_response(response):
    """Check if a rosbridge response indicates success."""
    raise NotImplementedError


def _safe_get_values(response):
    """Safely extract values from response."""
    raise NotImplementedError


def _extract_error(response):
    """Extract error message from response."""
    raise NotImplementedError
