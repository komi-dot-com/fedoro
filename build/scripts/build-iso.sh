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
    if [ "$DRY_RUN" = false ] && [ "$EUID" -ne 0 ]; then
        if podman info --format '{{.Host.Security.Rootless}}' 2>/dev/null | grep -q "true"; then
            echo "======================================================================"
            echo " [LỖI QUYỀN HỆ THỐNG - ROOTLESS CONTAINER DETECTED]"
            echo "======================================================================"
            echo "Quy trình tạo Live ISO (livemedia-creator) bắt buộc phải phân vùng và"
            echo "gắn kết thiết bị loopback kernel (/dev/loop*)."
            echo "Nhân Linux (Linux Kernel) chặn quyền mount loopback trong rootless Podman."
            echo ""
            echo ">> BẠN CẦN CHẠY VỚI QUYỀN 'sudo' THEO 1 TRONG 2 CÁCH SAU:"
            echo ""
            echo "Cách 1: Build trực tiếp trên máy Fedora của bạn (Nhanh và ổn định nhất):"
            echo "    1. Cài đặt lorax:  sudo dnf install -y lorax"
            echo "    2. Chạy lệnh:       sudo ./build/scripts/build-iso.sh --host"
            echo ""
            echo "Cách 2: Build trong container với quyền root (để có quyền /dev/loop):"
            echo "    Chạy lệnh:          sudo ./build/scripts/build-iso.sh"
            echo "======================================================================"
            exit 1
        fi
    fi

    echo "Delegating to containerized build runner (Podman)..."
    if [ "$DRY_RUN" = true ]; then
        exec "$SCRIPT_DIR/run-container-build.sh" --dry-run
    else
        exec "$SCRIPT_DIR/run-container-build.sh"
    fi
else
    if [ "$EUID" -ne 0 ]; then
        echo "======================================================================"
        echo " Error: Host build requires root privileges for loopback device mounting."
        echo " Please run: sudo ./build/scripts/build-iso.sh --host"
        echo "======================================================================"
        exit 1
    fi

    if ! command -v livemedia-creator >/dev/null 2>&1; then
        echo "======================================================================"
        echo " Error: 'livemedia-creator' is not installed on the host system."
        echo " Please install lorax first by running:"
        echo "     sudo dnf install -y lorax"
        echo " Then re-run: sudo ./build/scripts/build-iso.sh --host"
        echo "======================================================================"
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
