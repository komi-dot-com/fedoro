# ==============================================================================
# FEDORO OS - Master Live ISO Kickstart
# Target: Fedora 41 x86_64 Live Hyprland Edition
# ==============================================================================

# Include Base and Package Manifests
# --- Begin %include fedoro-base.ks ---
# ==============================================================================
# FEDORO OS - Base System Kickstart
# Foundation: Fedora 41 x86_64 Base
# ==============================================================================

# System Authorization and Security
authselect select sssd with-mkhomedir --force
selinux --enforcing
firewall --enabled --service=mdns,ssh

# Keyboard and Localization
keyboard us
lang en_US.UTF-8
timezone UTC --utc

# Network Configuration
network --bootproto=dhcp --device=link --activate --onboot=on

# Root and System Accounts (Live environment disables root password)
rootpw --lock

# System Services
services --enabled=NetworkManager,systemd-resolved,sssd,bluetooth,pipewire,wireplumber

# Disk Partitioning for Live Media creation
zerombr
clearpart --all --initlabel
part / --size=12288 --fstype=ext4 --label=fedoro-root

# Bootloader
bootloader --location=none
# --- End %include fedoro-base.ks ---
# --- Begin %include fedoro-packages.ks ---
# ==============================================================================
# FEDORO OS - Package Manifest Kickstart
# Curated packages for Hyprland, Wayland, PipeWire, and Flatpak
# ==============================================================================

%packages
# Core Linux Kernel and Initramfs for Live media
@core
kernel
kernel-modules
kernel-modules-extra
dracut-live
grub2-efi-x64
grub2-pc
shim-x64
efibootmgr
systemd-udev

# Hardware Acceleration & GPU Graphics Stack
mesa-dri-drivers
mesa-vulkan-drivers
vulkan-loader
libva
libva-utils
pciutils
usbutils

# Wayland Compositor & Hyprland Ecosystem
hyprland
hyprpaper
hypridle
hyprlock
xdg-desktop-portal-hyprland
xdg-desktop-portal-gtk
polkit-gnome

# Desktop Shell Utilities
waybar
rofi-wayland
swaync
wl-clipboard
cliphist
grim
slurp
jq
brightnessctl
playerctl

# Audio & Media Stack (PipeWire)
pipewire
pipewire-pulseaudio
pipewire-alsa
wireplumber
pavucontrol-qt

# Networking & Connectivity
NetworkManager
NetworkManager-wifi
network-manager-applet
bluez
bluez-tools
blueman

# Universal Applications & Flatpak
flatpak
xdg-user-dirs
xdg-utils

# Default Terminal and File Management
ptyxis
nautilus
gvfs
gvfs-smb
tar
unzip
p7zip

# Desktop Runtime & Python Adwaita Support for Fedoro Apps
python3
python3-gobject
gtk4
libadwaita

# Typography & Modern Font Rendering
inter-fonts
fontawesome-fonts-all
google-noto-sans-fonts
google-noto-color-emoji-fonts
fira-code-fonts

# System Administration & Diagnostics
fastfetch
htop
curl
wget
git

# Exclude unnecessary heavy legacy packages
-@gnome-desktop
-gnome-shell
-mutter
-gdm
%end
# --- End %include fedoro-packages.ks ---

# Repository Definitions
url --mirrorlist="https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-41&arch=x86_64"
repo --name="fedora" --mirrorlist="https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-41&arch=x86_64"
repo --name="updates" --mirrorlist="https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f41&arch=x86_64"

# Live Image Configuration & User Setup


%post
echo ">>> Starting Fedoro OS Live Post-Installation Setup..."

# 1. Create liveuser for live ISO session
useradd -m -c "Fedoro Live User" -G wheel liveuser
passwd -d liveuser > /dev/null

# Allow passwordless sudo for liveuser in live environment
echo "liveuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/liveuser
chmod 0440 /etc/sudoers.d/liveuser

# 2. Configure System Branding
cat << 'EOF' > /etc/os-release
NAME="Fedoro OS"
VERSION="41 (Wayland Edition)"
ID=fedoro
ID_LIKE="fedora"
VERSION_ID=41
PRETTY_NAME="Fedoro OS 41 (Wayland Edition)"
ANSI_COLOR="0;38;2;0;210;255"
LOGO=fedoro-logo-icon
CPE_NAME="cpe:/o:fedoro:fedoro:41"
DEFAULT_HOSTNAME="fedoro"
HOME_URL="https://github.com/fedoro-os/fedoro"
VARIANT="Wayland Hyprland Edition"
VARIANT_ID=hyprland
EOF

# 3. Setup Fedoro Desktop Skeleton Directory
mkdir -p /etc/skel/.config/hypr
mkdir -p /etc/skel/.config/waybar
mkdir -p /etc/skel/.config/rofi
mkdir -p /etc/skel/.config/swaync
mkdir -p /etc/skel/.config/gtk-3.0
mkdir -p /etc/skel/.config/gtk-4.0
mkdir -p /usr/share/backgrounds/fedoro
mkdir -p /usr/share/fedoro

# Create systemd autologin directly to Hyprland for liveuser
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat << 'EOF' > /etc/systemd/system/getty@tty1.service.d/autologin.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin liveuser --noclear %I $TERM
EOF

# Autostart Hyprland on TTY1 login
cat << 'EOF' >> /etc/skel/.bash_profile
if [ -z "$WAYLAND_DISPLAY" ] && [ "$XDG_VTNR" -eq 1 ]; then
    exec Hyprland
fi
EOF

# Copy skeleton to liveuser home
cp -r /etc/skel/. /home/liveuser/
chown -R liveuser:liveuser /home/liveuser

# 4. Flathub setup configuration
mkdir -p /etc/flatpak/remotes.d
cat << 'EOF' > /etc/flatpak/remotes.d/flathub.flatpakrepo
[Flatpak Repo]
Title=Flathub
Url=https://dl.flathub.org/repo/
Homepage=https://flathub.org/
Comment=Central repository of Flatpak applications
Description=Central repository of Flatpak applications
Icon=https://dl.flathub.org/repo/logo.svg
GPGKey=mQINBFl3mUEBEAC1FO4...
EOF

# 5. Enable Core Daemons
systemctl enable NetworkManager.service
systemctl enable bluetooth.service
systemctl set-default graphical.target

echo ">>> Fedoro OS Live Post-Installation Complete."
%end
