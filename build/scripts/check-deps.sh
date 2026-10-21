#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Build Dependency & System Pre-flight Checker
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
CYAN="\033[36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}=== FEDORO OS: System Dependency & Pre-Flight Check ===${RESET}"
echo ""

ERRORS=0
WARNINGS=0

check_cmd() {
    local cmd="$1"
    local desc="$2"
    local required="$3"

    if command -v "$cmd" >/dev/null 2>&1; then
        echo -e "  [${GREEN}✓${RESET}] $desc ($cmd): Found at $(command -v "$cmd")"
    else
        if [ "$required" = "true" ]; then
            echo -e "  [${RED}✗${RESET}] $desc ($cmd): ${RED}NOT FOUND (Required)${RESET}"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "  [${YELLOW}!${RESET}] $desc ($cmd): ${YELLOW}Not found (Optional/Containerized)${RESET}"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

echo -e "${BOLD}1. Host Development Tools:${RESET}"
check_cmd python3 "Python 3 Interpreter" true
check_cmd dnf5 "DNF5 Package Manager" false
check_cmd dnf "DNF Package Manager" false
check_cmd podman "Podman Container Engine (for rootless ISO builds)" true
check_cmd qemu-system-x86_64 "QEMU x86_64 Virtual Machine" true
check_cmd magick "ImageMagick (Asset processing)" false

echo ""
echo -e "${BOLD}2. Python Libraries:${RESET}"
python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1'); from gi.repository import Gtk, Adw" 2>/dev/null && \
    echo -e "  [${GREEN}✓${RESET}] PyGObject GTK4 & Libadwaita: Available" || \
    { echo -e "  [${RED}✗${RESET}] PyGObject GTK4 / Libadwaita: Missing"; ERRORS=$((ERRORS + 1)); }

python3 -c "import pykickstart" 2>/dev/null && \
    echo -e "  [${GREEN}✓${RESET}] pykickstart Library: Available" || \
    { echo -e "  [${YELLOW}!${RESET}] pykickstart Library: Missing (Install python3-pykickstart)"; WARNINGS=$((WARNINGS + 1)); }

echo ""
echo -e "${BOLD}3. System Resources:${RESET}"
# Check free disk space in current directory
FREE_KB=$(df -k . | awk 'NR==2 {print $4}')
FREE_GB=$((FREE_KB / 1024 / 1024))

if [ "$FREE_GB" -ge 15 ]; then
    echo -e "  [${GREEN}✓${RESET}] Available Disk Space: ${FREE_GB} GB (Requirement: 15+ GB for ISO build)"
else
    echo -e "  [${RED}✗${RESET}] Available Disk Space: ${FREE_GB} GB (Low! At least 15 GB recommended)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check RAM
TOTAL_MEM_MB=$(free -m | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM_MB" -ge 4000 ]; then
    echo -e "  [${GREEN}✓${RESET}] System Memory (RAM): ${TOTAL_MEM_MB} MB"
else
    echo -e "  [${YELLOW}!${RESET}] System Memory (RAM): ${TOTAL_MEM_MB} MB (Low! 4GB+ recommended)"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo -e "${BOLD}=== Summary ===${RESET}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All required tools and environments are ready for Fedoro OS development & build!${RESET}"
    exit 0
else
    echo -e "${RED}Total Errors: $ERRORS, Warnings: $WARNINGS. Please resolve missing requirements.${RESET}"
    exit 1
fi
