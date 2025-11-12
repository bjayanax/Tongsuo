#!/bin/bash
# Wrapper script for fetch_openssl_issues.py
# This script provides a convenient way to call the Python script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/fetch_openssl_issues.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found" >&2
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH" >&2
    exit 1
fi

# Execute the Python script with all arguments
exec python3 "$PYTHON_SCRIPT" "$@"
