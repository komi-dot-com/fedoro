#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Artifact Checksum Generator and Validator
# Generates and validates SHA256 and SHA512 hashes for release ISOs.
# ==============================================================================

set -euo pipefail

TARGET_DIR="${1:-./build/output}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Warning: Target directory $TARGET_DIR does not exist."
    exit 0
fi

cd "$TARGET_DIR"

ISOS=(*.iso)
if [ ! -e "${ISOS[0]}" ]; then
    echo "No ISO images found in $TARGET_DIR yet."
    exit 0
fi

echo "======================================================================"
echo "  FEDORO OS - Generating Checksums for ISO Images"
echo "======================================================================"

for iso in "${ISOS[@]}"; do
    echo "Processing image: $iso"
    
    echo "  Generating SHA-256..."
    sha256sum "$iso" > "${iso}.sha256"
    cat "${iso}.sha256"

    echo "  Generating SHA-512..."
    sha512sum "$iso" > "${iso}.sha512"
    
    echo "  Verifying generated SHA-256..."
    sha256sum -c "${iso}.sha256"
    
    echo "✓ Checksum verification passed for $iso"
done
