# ==============================================================================
# FEDORO OS - Master Live ISO Kickstart
# Target: Fedora 41 x86_64 Live Hyprland Edition
# ==============================================================================

# Include Base and Package Manifests
%include fedoro-base.ks
%include fedoro-packages.ks

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
