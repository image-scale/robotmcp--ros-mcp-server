"""Smoke tests for ros_mcp package — no ROS/Docker required."""
import pytest


class TestImports:
    def test_import_ros_mcp(self):
        import ros_mcp  # noqa: F401

    def test_import_utils_response(self):
        from ros_mcp.utils import response  # noqa: F401

    def test_import_utils_config_utils(self):
        from ros_mcp.utils import config_utils  # noqa: F401

    def test_import_utils_network_utils(self):
        from ros_mcp.utils import network_utils  # noqa: F401

    def test_import_utils_websocket(self):
        from ros_mcp.utils.websocket import WebSocketManager  # noqa: F401

    def test_import_utils_rosapi_types(self):
        from ros_mcp.utils.rosapi_types import detect_rosapi_types  # noqa: F401

    def test_import_tools(self):
        from ros_mcp.tools import register_all_tools  # noqa: F401

    def test_import_resources(self):
        from ros_mcp.resources import register_all_resources  # noqa: F401


class TestResponseHelpers:
    def test_check_response_none(self):
        from ros_mcp.utils.response import _check_response
        result = _check_response(None)
        assert result is not None
        assert "error" in result

    def test_check_response_empty_dict(self):
        from ros_mcp.utils.response import _check_response
        result = _check_response({})
        assert result is not None
        assert "error" in result

    def test_check_response_success(self):
        from ros_mcp.utils.response import _check_response
        result = _check_response({"result": True, "values": {"data": 42}})
        assert result is None

    def test_check_response_failure(self):
        from ros_mcp.utils.response import _check_response
        result = _check_response({"result": False, "values": {"message": "oops"}})
        assert result is not None
        assert "error" in result

    def test_safe_get_values_valid(self):
        from ros_mcp.utils.response import _safe_get_values
        result = _safe_get_values({"values": {"key": "val"}})
        assert result == {"key": "val"}

    def test_safe_get_values_missing(self):
        from ros_mcp.utils.response import _safe_get_values
        result = _safe_get_values({"no_values": True})
        assert result is None

    def test_safe_get_values_none_input(self):
        from ros_mcp.utils.response import _safe_get_values
        result = _safe_get_values(None)
        assert result is None

    def test_extract_error_with_message(self):
        from ros_mcp.utils.response import _extract_error
        result = _extract_error({"values": {"message": "something went wrong"}})
        assert result == "something went wrong"

    def test_extract_error_no_response(self):
        from ros_mcp.utils.response import _extract_error
        result = _extract_error(None)
        assert result == "No response"


class TestConfigUtils:
    def test_get_robots_list(self):
        from ros_mcp.utils.config_utils import get_verified_robots_list_util
        result = get_verified_robots_list_util()
        assert "robot_specifications" in result
        assert isinstance(result["robot_specifications"], list)
        assert result["count"] > 0

    def test_get_robots_list_contains_expected(self):
        from ros_mcp.utils.config_utils import get_verified_robots_list_util
        result = get_verified_robots_list_util()
        assert "local_rosbridge" in result["robot_specifications"]

    def test_load_robot_config_valid(self):
        from ros_mcp.utils.config_utils import get_verified_robot_spec_util
        result = get_verified_robot_spec_util("local_rosbridge")
        assert "local_rosbridge" in result
        assert "type" in result["local_rosbridge"]
        assert "prompts" in result["local_rosbridge"]

    def test_load_robot_config_not_found(self):
        from ros_mcp.utils.config_utils import load_robot_config
        with pytest.raises(FileNotFoundError):
            load_robot_config("nonexistent_robot", "/tmp")


class TestNetworkUtils:
    def test_resolve_dns_ip_address(self):
        from ros_mcp.utils.network_utils import _resolve_dns
        success, resolved, error = _resolve_dns("127.0.0.1")
        assert success is True
        assert resolved == "127.0.0.1"
        assert error is None

    def test_resolve_dns_localhost(self):
        from ros_mcp.utils.network_utils import _resolve_dns
        success, resolved, error = _resolve_dns("localhost")
        assert success is True
        assert resolved is not None

    def test_resolve_dns_invalid(self):
        from ros_mcp.utils.network_utils import _resolve_dns
        success, resolved, error = _resolve_dns("this.host.does.not.exist.invalid")
        assert success is False
        assert error is not None


class TestWebSocketManager:
    def test_websocket_manager_creation(self):
        from ros_mcp.utils.websocket import WebSocketManager
        ws = WebSocketManager("127.0.0.1", 9090, default_timeout=1.0)
        assert ws is not None
