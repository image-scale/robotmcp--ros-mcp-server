#!/bin/bash
set -eo pipefail

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export CI=true

cd /workspace/ros-mcp-server

rm -rf .pytest_cache

pytest -p no:cacheprovider \
    -v --tb=short \
    --ignore=tests/integration \
    --ignore=tests/installation \
    tests/

