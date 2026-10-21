#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - QEMU Virtual Machine Test Runner
# Boots the Fedoro ISO in QEMU with UEFI, VirtIO graphics, audio, and network.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

ISO_PATH="${1:-}"

if [ -z "$ISO_PATH" ]; then
    # Look for most recent ISO in build/output
    ISO_PATH=$(find "$ROOT_DIR/build/output" -name "*.iso" 2>/dev/null | head -n 1 || true)
fi

if [ -z "$ISO_PATH" ] || [ ! -f "$ISO_PATH" ]; then
    echo "Usage: $0 [path/to/fedoro-live.iso]"
    echo "Error: No ISO image specified or found in build/output/."
    exit 1
fi

echo "======================================================================"
echo "  FEDORO OS - QEMU Test Environment"
echo "  ISO Target : $ISO_PATH"
echo "  Memory     : 4096 MB"
echo "  CPU Cores  : 4 Cores (Host Passthrough / KVM)"
echo "  Display    : VirtIO GPU (Wayland accelerated)"
echo "======================================================================"

# Determine KVM acceleration availability
KVM_FLAG=""
if [ -w /dev/kvm ]; then
    echo "[INFO] Hardware KVM acceleration enabled."
    KVM_FLAG="-enable-kvm -cpu host"
else
    echo "[WARN] /dev/kvm not accessible. Running in emulation mode (slower)."
    KVM_FLAG="-cpu max"
fi

# Locate OVMF UEFI firmware if available
OVMF_FLAG=""
for ovmf in \
    /usr/share/edk2/ovmf/OVMF_CODE.fd \
    /usr/share/OVMF/OVMF_CODE.fd \
    /usr/share/edk2-ovmf/x64/OVMF_CODE.fd; do
    if [ -f "$ovmf" ]; then
        OVMF_FLAG="-bios $ovmf"
        echo "[INFO] UEFI Firmware found: $ovmf"
        break
    fi
done

qemu-system-x86_64 \
    $KVM_FLAG \
    $OVMF_FLAG \
    -m 4096 \
    -smp 4 \
    -vga virtio \
    -display gtk,gl=on \
    -device virtio-net-pci,netdev=net0 \
    -netdev user,id=net0 \
    -device intel-hda \
    -device hda-duplex \
    -boot d \
    -cdrom "$ISO_PATH"
