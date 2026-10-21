#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Containerized ISO Build Runner (Podman)
# Runs the live ISO build inside a clean, isolated Fedora environment.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

OUTPUT_DIR="$ROOT_DIR/build/output"
mkdir -p "$OUTPUT_DIR"

DRY_RUN=false
for arg in "$@"; do
    if [ "$arg" == "--dry-run" ]; then
        DRY_RUN=true
    fi
done

echo "======================================================================"
echo "  FEDORO OS - Containerized Build Pipeline"
echo "  Target Architecture : x86_64"
echo "  Base Distribution   : Fedora 41 (Lorax / livemedia-creator)"
echo "  Output Directory    : $OUTPUT_DIR"
echo "  Dry Run Mode        : $DRY_RUN"
echo "======================================================================"

# Step 1: Pre-flight check
"$SCRIPT_DIR/check-deps.sh"

# Step 2: Flatten & Validate Kickstart
echo ""
echo "[Step 2/4] Flattening and validating kickstart specification..."
python3 "$SCRIPT_DIR/flatten_ks.py" \
    "$ROOT_DIR/build/kickstart/fedoro-live-hyprland.ks" \
    "$ROOT_DIR/build/kickstart/fedoro-live-hyprland-flat.ks"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "======================================================================"
    echo " [DRY-RUN COMPLETE] Kickstart and configuration validation successful."
    echo " To perform a full ISO compilation, run without --dry-run."
    echo "======================================================================"
    exit 0
fi

# Step 3: Containerized livemedia-creator Execution
echo ""
echo "[Step 3/4] Launching isolated Podman build container..."

CONTAINER_IMG="registry.fedoraproject.org/fedora:41"

podman run --rm --privileged \
    -v "$ROOT_DIR:/workspace:Z" \
    -w /workspace \
    "$CONTAINER_IMG" bash -c '
        set -euo pipefail
        echo ">>> Inside Fedoro Build Container <<<"
        echo "Updating package caches and installing build tools..."
        dnf -y --setopt=install_weak_deps=False install lorax pykickstart
        
        echo "Preparing build output directory..."
        mkdir -p /workspace/build/output
        
        echo "Executing livemedia-creator for Fedoro OS..."
        livemedia-creator \
            --ks=/workspace/build/kickstart/fedoro-live-hyprland-flat.ks \
            --no-virt \
            --resultdir=/workspace/build/output \
            --project="Fedoro OS" \
            --releasever=41 \
            --volid="FEDORO_LIVE"
'

# Step 4: Verify checksums if an ISO exists
echo ""
echo "[Step 4/4] Verifying generated release artifacts..."
"$SCRIPT_DIR/verify-checksums.sh" "$OUTPUT_DIR"
