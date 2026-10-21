#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Power Menu Script
# ==============================================================================

theme="$HOME/.config/rofi/powermenu.rasi"
if [ ! -f "$theme" ]; then
    theme="/etc/skel/.config/rofi/powermenu.rasi"
fi

lock="󰌾  Lock Screen"
suspend="󰒲  Suspend"
logout="󰍃  Log Out"
reboot="󰜉  Reboot"
shutdown="⏻  Shut Down"

options="$lock\n$suspend\n$logout\n$reboot\n$shutdown"

chosen="$(echo -e "$options" | rofi -dmenu -i -theme "$theme" -p "Power")"

case "$chosen" in
    *"Lock"*)
        hyprlock || loginctl lock-session
        ;;
    *"Suspend"*)
        systemctl suspend
        ;;
    *"Log Out"*)
        hyprctl dispatch exit || loginctl terminate-user "$USER"
        ;;
    *"Reboot"*)
        systemctl reboot
        ;;
    *"Shut Down"*)
        systemctl poweroff
        ;;
esac
