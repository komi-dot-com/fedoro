# FEDORO OS - Installation & Deployment Guide

## 1. System Requirements

### Minimum Requirements:
- **Processor**: 64-bit x86 dual-core CPU (2.0 GHz or higher).
- **Memory (RAM)**: 4 GB RAM.
- **Storage**: 25 GB free disk space (SSD recommended).
- **Graphics**: GPU with OpenGL 3.2+ or Vulkan support (Intel HD 4000+, AMD GCN 1.0+, NVIDIA Kepler+).
- **Firmware**: UEFI (Secure Boot supported via Fedora shim).

### Recommended Requirements:
- **Processor**: 4-core Intel Core i5/AMD Ryzen 5 or better.
- **Memory (RAM)**: 8 GB+ RAM.
- **Storage**: 50 GB+ NVMe SSD.
- **Display**: 1080p, 2K, or 4K with HiDPI support.

---

## 2. Preparing the Installation Media

### Using Fedora Media Writer (Recommended for Windows / macOS / Linux):
1. Download Fedora Media Writer or use the installed version.
2. Select **Custom Image** and navigate to your `Fedoro-OS-Live.iso`.
3. Choose your USB Flash drive (minimum 8 GB capacity).
4. Click **Write**.

### Using Command Line (`dd` on Linux / macOS):
```bash
sudo dd if=Fedoro-OS-Live.iso of=/dev/sdX bs=4M status=progress oflag=sync
```
*(Replace `/dev/sdX` with the target block device of your flash drive)*.

---

## 3. Booting into Fedoro Live Session

1. Insert the bootable USB into your target computer.
2. Power on the machine and access the BIOS/UEFI boot menu (typically `F12`, `F11`, `F10`, or `Del`).
3. Select the UEFI boot option corresponding to your flash drive.
4. In the GRUB boot menu, select **Start Fedoro OS Live (Wayland & Hyprland)**.
5. The system will automatically log in to the Live User session and launch Hyprland.

---

## 4. First Boot & Onboarding

Upon launching into the Fedoro desktop:
- **Fedoro Welcome** appears automatically on the first session.
- Review initial configuration options:
  - Toggle **Dark Mode** or **Light Mode**.
  - Configure **Display Scaling** if using a HiDPI / 4K monitor.
  - Review the **Shortcuts Cheat Sheet** (`Super + Space` for app search, `Super + Return` for terminal).
  - Click **Enable Flathub** to activate universal application downloads.
- Launch **Fedoro Store** (`Super + S`) to install your daily drivers (Firefox, VS Code, Discord, Spotify).
