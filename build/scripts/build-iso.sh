#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Master ISO Build Entrypoint
# Supports both native host execution (with root/sudo) and containerized builds.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

USE_CONTAINER=true
DRY_RUN=false

for arg in "$@"; do
    case "$arg" in
        --host)
            USE_CONTAINER=false
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --help|-h)
            echo "Usage: $0 [--host] [--dry-run]"
            echo "  --host     : Run build directly on host using local livemedia-creator (requires root)"
            echo "  --dry-run  : Validate configurations and dependencies without starting full build"
            exit 0
            ;;
    esac
done

if [ "$USE_CONTAINER" = true ]; then
    echo "Delegating to containerized build runner (Podman)..."
    if [ "$DRY_RUN" = true ]; then
        exec "$SCRIPT_DIR/run-container-build.sh" --dry-run
    else
        exec "$SCRIPT_DIR/run-container-build.sh"
    fi
else
    if [ "$EUID" -ne 0 ]; then
        echo "Error: Host build requires root privileges for loopback device mounting."
        echo "Run with sudo or use the default containerized build: ./build/scripts/build-iso.sh"
        exit 1
    fi

    echo "Running native host build..."
    "$SCRIPT_DIR/check-deps.sh"
    python3 "$SCRIPT_DIR/flatten_ks.py" \
        "$ROOT_DIR/build/kickstart/fedoro-live-hyprland.ks" \
        "$ROOT_DIR/build/kickstart/fedoro-live-hyprland-flat.ks"

    if [ "$DRY_RUN" = true ]; then
        echo "Host dry-run successful."
        exit 0
    fi

    livemedia-creator \
        --ks="$ROOT_DIR/build/kickstart/fedoro-live-hyprland-flat.ks" \
        --no-virt \
        --resultdir="$ROOT_DIR/build/output" \
        --project="Fedoro OS" \
        --releasever=41 \
        --volid="FEDORO_LIVE"

    "$SCRIPT_DIR/verify-checksums.sh" "$ROOT_DIR/build/output"
fi
