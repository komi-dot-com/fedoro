#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Kickstart Integration Test
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Testing Kickstart Processing and Semantic Validation ==="

OUTPUT_FLAT="$ROOT_DIR/build/kickstart/test-flat.ks"

python3 "$ROOT_DIR/build/scripts/flatten_ks.py" \
    "$ROOT_DIR/build/kickstart/fedoro-live-hyprland.ks" \
    "$OUTPUT_FLAT"

echo "Checking essential kickstart directives in flattened file..."

grep -q "selinux --enforcing" "$OUTPUT_FLAT" || { echo "Missing selinux directive"; exit 1; }
grep -q "hyprland" "$OUTPUT_FLAT" || { echo "Missing hyprland package"; exit 1; }
grep -q "waybar" "$OUTPUT_FLAT" || { echo "Missing waybar package"; exit 1; }
grep -q "flatpak" "$OUTPUT_FLAT" || { echo "Missing flatpak package"; exit 1; }
grep -q "pipewire" "$OUTPUT_FLAT" || { echo "Missing pipewire package"; exit 1; }
grep -q "liveuser" "$OUTPUT_FLAT" || { echo "Missing liveuser setup"; exit 1; }

rm -f "$OUTPUT_FLAT"
echo "✓ Kickstart integration test PASSED!"
