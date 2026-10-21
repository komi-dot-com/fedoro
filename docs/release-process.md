# FEDORO OS - Quality Assurance & Release Process

## 1. Release Cadence & Versioning

Fedoro OS follows semantic versioning aligned with Fedora upstream stable releases:
- **Major.Minor.Patch**: e.g., `41.1.0`
  - `41`: Fedora platform version base.
  - `1`: Fedoro desktop environment revision.
  - `0`: Hotfix / security release update.

---

## 2. Release Candidate Pre-Flight Checklist

Before tagging and publishing a release:

- [ ] **Dependency Audit**:
  - Run `./build/scripts/check-deps.sh`.
  - Verify zero unmet package dependencies in `build/kickstart/fedoro-packages.ks`.
- [ ] **Syntactic & Static Analysis**:
  - Run `./tests/test_syntax.sh` (Shell scripts & Python).
  - Run `./tests/test_desktop_configs.sh` (JSON, JSONC, Hyprland modules).
- [ ] **Application Unit Testing**:
  - Run `python3 -m unittest tests/test_applications.py`.
- [ ] **Kickstart Semantic Validation**:
  - Run `python3 build/scripts/flatten_ks.py build/kickstart/fedoro-live-hyprland.ks build/kickstart/fedoro-live-hyprland-flat.ks`.
  - Verify with `tests/test_kickstart.sh`.
- [ ] **Clean Build**:
  - Run `./build/scripts/build-iso.sh`.
- [ ] **Artifact Verification**:
  - Generate and verify SHA256 / SHA512 hashes using `./build/scripts/verify-checksums.sh`.
- [ ] **VM Smoke Testing (QEMU)**:
  - Boot image with `./build/scripts/test-iso-qemu.sh`.
  - Verify autologin into Hyprland.
  - Verify Waybar status bar loading and modules (CPU, RAM, audio, clock).
  - Verify Rofi launcher (`Super + Space`).
  - Verify Fedoro Welcome startup dialog.
  - Test Flatpak installation of sample application.
  - Verify clean system reboot and shutdown.
