"""Configuration utilities for ROS MCP Server."""
import os
from pathlib import Path

import yaml


def _get_robot_specifications_path():
    """Get the path to the robot_specifications directory."""
    # Get the package root directory (parent of ros_mcp)
    package_root = Path(__file__).parent.parent.parent
    return package_root / "robot_specifications"


def get_verified_robots_list_util():
    """Get list of available robot specifications.

    Returns:
        A dict with "robot_specifications" list and "count".
    """
    specs_path = _get_robot_specifications_path()
    robot_specs = []

    if specs_path.exists():
        for yaml_file in specs_path.glob("*.yaml"):
            # Use the filename without extension as the robot name
            robot_name = yaml_file.stem
            robot_specs.append(robot_name)

    return {
        "robot_specifications": sorted(robot_specs),
        "count": len(robot_specs),
    }


def get_verified_robot_spec_util(robot_name):
    """Get a specific robot specification.

    Args:
        robot_name: The name of the robot to load.

    Returns:
        A dict with robot_name as key containing the robot config.
    """
    specs_path = _get_robot_specifications_path()
    yaml_path = specs_path / f"{robot_name}.yaml"

    if not yaml_path.exists():
        raise FileNotFoundError(f"Robot specification not found: {robot_name}")

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def load_robot_config(robot_name, path):
    """Load robot configuration from a specific path.

    Args:
        robot_name: The name of the robot configuration file.
        path: The directory path to load from.

    Returns:
        The loaded configuration dict.

    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
    """
    config_path = Path(path) / f"{robot_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Robot configuration not found: {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
