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
