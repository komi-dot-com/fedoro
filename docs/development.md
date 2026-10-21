# FEDORO OS - Developer & Maintainer Guide

## 1. Development Workspace Structure

The project repository is structured cleanly into functional layers:

```
fedoro/
├── README.md                      # Project overview and roadmap
├── LICENSE                        # GNU General Public License v3.0
├── docs/                          # Technical and user guides
├── build/
│   ├── kickstart/                 # Base, package manifest, and live kickstarts
│   ├── scripts/                   # Automated build, check, and test scripts
│   └── output/                    # Target directory for generated ISO images
├── desktop/
│   ├── hypr/                      # Hyprland modular configuration files
│   ├── waybar/                    # Status bar config and CSS styling
│   ├── launcher/                  # Rofi launcher and power menu scripts
│   ├── notifications/             # SwayNC & Mako notification configs
│   └── themes/                    # GTK and Qt theme presets
├── branding/
│   ├── wallpapers/                # Vector SVG & rendered PNG 4K wallpapers
│   ├── icons/                     # Vector SVG & PNG logos and icons
│   └── os-release                 # /etc/os-release branding specification
├── applications/
│   ├── welcome/                   # Fedoro Welcome GTK4/Adwaita onboarding app
│   ├── settings/                  # Fedoro Settings desktop preferences app
│   └── store/                     # Fedoro Store Flatpak package center
└── tests/                         # Automated syntax, config, and unit tests
```

---

## 2. Running Local Unit & Integration Tests

Fedoro OS includes an automated pre-flight testing pipeline:

```bash
# 1. Test shell scripts and Python syntax
./tests/test_syntax.sh

# 2. Validate desktop configurations (JSON, JSONC, Hyprland modules)
./tests/test_desktop_configs.sh

# 3. Test Kickstart resolution and directives
./tests/test_kickstart.sh

# 4. Run application test suite (headless GTK4 / Libadwaita verification)
python3 -m unittest tests/test_applications.py
```

---

## 3. Building the Live ISO

### Prerequisites:
- Podman (for containerized rootless builds) or Fedora root access.
- At least 15 GB free disk space.
- Internet connectivity to pull Fedora base repositories and packages.

### Dry-Run Validation:
To validate kickstarts, package lists, and build scripts without starting a long compilation:
```bash
./build/scripts/build-iso.sh --dry-run
```

### Full ISO Build (Containerized via Podman):
```bash
./build/scripts/build-iso.sh
```

### Full ISO Build (Directly on Fedora Host with root):
```bash
sudo ./build/scripts/build-iso.sh --host
```

The resulting ISO will be placed in `build/output/` alongside generated SHA256 and SHA512 checksum files.

---

## 4. Testing the ISO with QEMU

Run the virtual machine test harness:
```bash
./build/scripts/test-iso-qemu.sh [path/to/fedoro-live.iso]
```
The test script launches QEMU with UEFI (OVMF firmware), 4 GB RAM, 4 CPU cores, and hardware-accelerated VirtIO graphics.
