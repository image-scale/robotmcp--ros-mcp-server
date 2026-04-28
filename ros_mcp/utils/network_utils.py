"""Network utilities for ROS MCP Server."""
import socket


def _resolve_dns(hostname):
    """Resolve DNS for a hostname.

    Args:
        hostname: The hostname or IP address to resolve.

    Returns:
        A tuple of (success: bool, resolved_ip: str or None, error: str or None).
    """
    # Check if it's already an IP address
    try:
        socket.inet_aton(hostname)
        # It's a valid IP address, return as-is
        return (True, hostname, None)
    except socket.error:
        pass

    # Try to resolve the hostname
    try:
        resolved_ip = socket.gethostbyname(hostname)
        return (True, resolved_ip, None)
    except socket.gaierror as e:
        return (False, None, str(e))
    except Exception as e:
        return (False, None, str(e))
