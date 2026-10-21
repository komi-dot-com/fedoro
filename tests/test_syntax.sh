#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Shell and Python Syntax Test Suite
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Testing Bash Scripts Syntax ==="
find "$ROOT_DIR" -type f -name "*.sh" -print0 | while IFS= read -r -d '' f; do
    echo -n "Checking $f ... "
    bash -n "$f"
    echo "OK"
done

echo ""
echo "=== Testing Python Scripts Syntax ==="
find "$ROOT_DIR" -type f -name "*.py" -print0 | while IFS= read -r -d '' f; do
    echo -n "Compiling $f ... "
    python3 -m py_compile "$f"
    echo "OK"
done

echo ""
echo "✓ All Shell and Python syntax tests PASSED!"
