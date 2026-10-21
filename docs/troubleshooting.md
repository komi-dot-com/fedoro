# FEDORO OS - Hardware & Runtime Troubleshooting

## 1. NVIDIA Dedicated GPU Configuration

Fedoro OS uses Wayland natively. While modern NVIDIA drivers (555+ and 560+) provide robust Wayland support via explicit sync, ensure the following parameters are active if experiencing stutter or black screens:

### Kernel Parameters (`/etc/default/grub`):
```ini
GRUB_CMDLINE_LINUX="... rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1 nvidia-drm.fbdev=1"
```
Rebuild GRUB:
```bash
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
```

### Hyprland Environment Variables (`desktop/hypr/hyprland.conf`):
```ini
env = LIBVA_DRIVER_NAME,nvidia
env = __GLX_VENDOR_LIBRARY_NAME,nvidia
env = NVD_BACKEND,direct
```

---

## 2. PipeWire Audio Routing & Microphones

If audio devices are not detected:
1. Check WirePlumber daemon status:
   ```bash
   systemctl --user status wireplumber pipewire
   ```
2. Verify audio sinks and sources:
   ```bash
   wpctl status
   ```
3. Set default output device:
   ```bash
   wpctl set-default <ID>
   ```

---

## 3. Screen Sharing & WebRTC (Discord / Zoom / Chrome)

Fedoro OS ships with `xdg-desktop-portal-hyprland`. If browser or app screen sharing prompts do not appear:
1. Ensure both portals are running in user session:
   ```bash
   systemctl --user status xdg-desktop-portal
   systemctl --user status xdg-desktop-portal-hyprland
   ```
2. In Firefox or Chromium, ensure Wayland flags are enabled:
   - Firefox: `MOZ_ENABLE_WAYLAND=1` (Default in Fedoro OS).
   - Chromium / Chrome: Flag `Preferred Ozone platform` set to `Wayland`.

---

## 4. Fractional Scaling & Blurry XWayland Applications

If legacy X11 applications appear blurry under fractional scaling:
In `desktop/hypr/monitors.conf`:
```ini
xwayland {
    force_zero_scaling = true
}
```
This forces XWayland clients to render at 1x scale and rely on their internal scaling, preserving crisp text and graphics.
