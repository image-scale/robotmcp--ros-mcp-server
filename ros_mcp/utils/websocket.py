"""WebSocket manager for ROS MCP Server."""
import json
import threading
import time
import uuid

import websocket


class WebSocketManager:
    """Manage WebSocket connections to rosbridge."""

    def __init__(self, ip, port, default_timeout=5.0):
        """Initialize WebSocket manager.

        Args:
            ip: The IP address of the rosbridge server.
            port: The port number of the rosbridge server.
            default_timeout: Default timeout for operations in seconds.
        """
        self.ip = ip
        self.port = port
        self.default_timeout = default_timeout
        self.ws = None
        self._responses = {}
        self._lock = threading.Lock()
        self._connected = False

    def _get_ws_url(self):
        """Get the WebSocket URL."""
        return f"ws://{self.ip}:{self.port}"

    def connect(self):
        """Connect to the rosbridge server."""
        url = self._get_ws_url()
        try:
            self.ws = websocket.create_connection(url, timeout=self.default_timeout)
            self._connected = True
            return True
        except Exception as e:
            self._connected = False
            raise e

    def disconnect(self):
        """Disconnect from the rosbridge server."""
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            finally:
                self.ws = None
                self._connected = False

    def is_connected(self):
        """Check if connected to rosbridge."""
        return self._connected and self.ws is not None

    def send_message(self, message, timeout=None):
        """Send a message and wait for response.

        Args:
            message: The message dict to send.
            timeout: Timeout in seconds (uses default if None).

        Returns:
            The response dict or None.
        """
        if timeout is None:
            timeout = self.default_timeout

        if not self.is_connected():
            return None

        # Add an ID if not present
        if "id" not in message:
            message["id"] = str(uuid.uuid4())

        msg_id = message["id"]

        try:
            self.ws.send(json.dumps(message))
            self.ws.settimeout(timeout)
            response = self.ws.recv()
            return json.loads(response)
        except Exception:
            return None

    def call_service(self, service_name, args=None, timeout=None):
        """Call a ROS service.

        Args:
            service_name: The name of the service.
            args: The service arguments.
            timeout: Timeout in seconds.

        Returns:
            The service response or None.
        """
        message = {
            "op": "call_service",
            "service": service_name,
            "args": args or {},
        }
        return self.send_message(message, timeout)
