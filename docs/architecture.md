# FEDORO OS - Operating System Architecture Specification

## 1. Executive Summary

**FEDORO OS** is a modern, high-performance Linux distribution combining the rock-solid base of **Fedora Linux**, the tearing-free responsiveness of **Wayland**, the fluidity of the **Hyprland** dynamic tiling compositor, and the security and flexibility of **Flatpak** sandboxed applications.

Unlike traditional desktop distributions that mix system utilities and graphical applications in a unified RPM namespace, Fedoro OS establishes a clear architectural boundary:
- **Base System**: Managed strictly via RPM & DNF5 with SELinux enforcing.
- **Desktop Layer**: Wayland-native compositor, status bar, notification daemon, and custom Libadwaita control suite.
- **Application Layer**: Universal desktop applications delivered predominantly via Flatpak and Flathub.

```
+-----------------------------------------------------------------------+
|                    Application Layer (Flatpak / Flathub)               |
|      Firefox | VS Code | LibreOffice | Obsidian | VLC | Discord       |
+-----------------------------------------------------------------------+
|                    Fedoro Desktop Suite (GTK4 / Libadwaita)           |
|      Fedoro Welcome    |    Fedoro Settings    |    Fedoro Store      |
+-----------------------------------------------------------------------+
|                    Desktop Layer (Wayland Native)                     |
|  Hyprland Compositor | Waybar | Rofi-Wayland | SwayNC | Hyprlock/Idle |
|  XDG Desktop Portal (xdg-desktop-portal-hyprland + gtk)               |
+-----------------------------------------------------------------------+
|                    Plumbing Stack (systemd & Daemons)                 |
|  PipeWire & WirePlumber | NetworkManager | Polkit | BlueZ | Dracut    |
+-----------------------------------------------------------------------+
|                    Graphics Stack                                      |
|  Linux Kernel (DRM/KMS) | Mesa (Vulkan / OpenGL) | Wayland Protocols  |
+-----------------------------------------------------------------------+
|                    Base System (Fedora Core)                          |
|  Fedora Linux 41+ | RPM / DNF5 | SELinux (Enforcing) | systemd        |
+-----------------------------------------------------------------------+
```

---

## 2. Layer-by-Layer Architectural Breakdown

### Layer 1: Base System
- **Distribution Base**: Fedora Linux 41+ (x86_64).
- **Init & Service Manager**: `systemd` v256+ with modern unit sandboxing (`DynamicUser`, `ProtectSystem`, `ProtectHome`).
- **Package Management**: DNF5 / RPM for core system packages, kernel updates, and hardware drivers.
- **Security Engine**: SELinux in **Enforcing** mode. Fedoro OS preserves standard Fedora SELinux policies without disabling or weakening label restrictions.

### Layer 2: Graphics & Display Stack
- **Display Protocol**: Pure Wayland. XWayland is available on demand with zero fractional scaling distortion (`force_zero_scaling = true`).
- **Graphics Drivers**: Mesa DRI and Vulkan drivers (`mesa-dri-drivers`, `mesa-vulkan-drivers`).
- **NVIDIA Support**: Automated kernel module loading through standard RPM Fusion kmod-nvidia packages with DRM modeset enabled (`nvidia-drm.modeset=1`).

### Layer 3: Compositor & Desktop Environment
- **Compositor**: Hyprland (wlroots-based modern dynamic tiling compositor).
- **Status Bar**: Waybar with custom glassmorphism styling, real-time hardware telemetry, volume/network controls, and application launcher button.
- **Application Launcher**: Rofi-Wayland with fuzzy application search and custom power management dialog.
- **Notification Daemon**: SwayNotificationCenter (SwayNC) providing an integrated notification tray, quick settings toggles, and volume/brightness sliders.
- **Screen Lock & Idle**: `hypridle` and `hyprlock` integrated with systemd session locking.
- **Portals**: `xdg-desktop-portal-hyprland` paired with `xdg-desktop-portal-gtk` for native file choosers, screen sharing (PipeWire screen-cast), and token management.

### Layer 4: Audio and Multimedia
- **Audio Server**: PipeWire with WirePlumber session manager.
- **Compatibility**: Drop-in replacements for PulseAudio (`pipewire-pulseaudio`) and ALSA (`pipewire-alsa`).
- **Control**: `pavucontrol-qt` and WirePlumber CLI (`wpctl`).

### Layer 5: Fedoro Custom Applications
- **Fedoro Welcome** (`fedoro-welcome`): Built with GTK4 and Libadwaita. Welcomes new users, offers first-boot customization (dark/light theme, display scale), keybindings cheat sheet, and one-click Flathub initialization.
- **Fedoro Settings** (`fedoro-settings`): Centralized hub for theme toggling, blur adjustment, wallpaper selection, HiDPI scale factor configuration, and hardware overview.
- **Fedoro Store** (`fedoro-store`): Clean graphical store for browsing, installing, and updating sandboxed Flatpak packages.

---

## 3. Security Architecture

1. **SELinux Enforcement**: Never placed in Permissive or Disabled modes in production kickstart recipes.
2. **Privilege Separation**: Core desktop components run strictly as an unprivileged user (`liveuser` or standard user). Root execution is gated via Polkit (`polkit-gnome`).
3. **Application Sandboxing**: By prioritizing Flatpak, user applications cannot read or alter system binaries in `/usr`, protecting the system from tampering.
4. **Reproducible ISO Pipeline**: Kickstart configurations are declarative, flattened, and validated via `pykickstart` before invocation.
