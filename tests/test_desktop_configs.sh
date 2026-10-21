#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Desktop Configuration Validator
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Testing Desktop Configuration Validity ==="

# 1. Test SwayNC JSON configuration
echo -n "Validating SwayNC config.json ... "
python3 -c "import json; json.load(open('$ROOT_DIR/desktop/notifications/swaync/config.json'))"
echo "OK"

# 2. Test Waybar JSONC configuration (stripping // comments)
echo -n "Validating Waybar config.jsonc ... "
python3 -c "
import re, json
content = open('$ROOT_DIR/desktop/waybar/config.jsonc').read()
clean_json = re.sub(r'//.*', '', content)
json.loads(clean_json)
"
echo "OK"

# 3. Test Hyprland config files existence and structure
echo "Verifying Hyprland modular configuration files..."
HYPR_FILES=(
    "hyprland.conf"
    "monitors.conf"
    "autostart.conf"
    "input.conf"
    "lookfeel.conf"
    "keybindings.conf"
    "rules.conf"
    "hypridle.conf"
    "hyprlock.conf"
    "hyprpaper.conf"
)

for f in "${HYPR_FILES[@]}"; do
    target="$ROOT_DIR/desktop/hypr/$f"
    if [ -f "$target" ]; then
        echo "  [✓] Found: desktop/hypr/$f"
    else
        echo "  [✗] Missing: desktop/hypr/$f"
        exit 1
    fi
done

# 4. Check Rofi configs
echo "Verifying Rofi themes..."
for f in "config.rasi" "powermenu.rasi"; do
    target="$ROOT_DIR/desktop/launcher/rofi/$f"
    if [ -f "$target" ]; then
        echo "  [✓] Found: desktop/launcher/rofi/$f"
    else
        echo "  [✗] Missing: desktop/launcher/rofi/$f"
        exit 1
    fi
done

echo ""
echo "✓ All Desktop Configuration validations PASSED!"
