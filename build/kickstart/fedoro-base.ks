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
