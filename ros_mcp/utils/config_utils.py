"""Configuration utilities for ROS MCP Server."""


def get_verified_robots_list_util():
    """Get list of available robot specifications."""
    raise NotImplementedError


def get_verified_robot_spec_util(robot_name):
    """Get a specific robot specification."""
    raise NotImplementedError


def load_robot_config(robot_name, path):
    """Load robot configuration from a specific path."""
    raise NotImplementedError
