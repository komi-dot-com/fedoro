#!/usr/bin/env bash
# ==============================================================================
# FEDORO OS - Screenshot Utility Script
# Uses grim + slurp + wl-copy + notify-send
# ==============================================================================

DIR="$HOME/Pictures/Screenshots"
mkdir -p "$DIR"
FILENAME="$DIR/Fedoro_$(date +'%Y-%m-%d_%H-%M-%S').png"

case "$1" in
    area)
        GEOM=$(slurp)
        if [ -n "$GEOM" ]; then
            grim -g "$GEOM" "$FILENAME"
            wl-copy < "$FILENAME"
            notify-send "Fedoro Screenshot" "Area saved to $FILENAME & copied to clipboard" -i "$FILENAME"
        fi
        ;;
    full)
        sleep 0.5
        grim "$FILENAME"
        wl-copy < "$FILENAME"
        notify-send "Fedoro Screenshot" "Fullscreen saved to $FILENAME & copied to clipboard" -i "$FILENAME"
        ;;
    window)
        GEOM=$(hyprctl activewindow -j | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"')
        if [ -n "$GEOM" ]; then
            grim -g "$GEOM" "$FILENAME"
            wl-copy < "$FILENAME"
            notify-send "Fedoro Screenshot" "Window saved to $FILENAME & copied to clipboard" -i "$FILENAME"
        fi
        ;;
    *)
        echo "Usage: $0 {area|full|window}"
        exit 1
        ;;
esac
