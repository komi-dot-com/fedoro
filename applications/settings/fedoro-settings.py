#!/usr/bin/env python3
"""
FEDORO OS - System Settings & Desktop Customization Center
Built with GTK4 and Libadwaita for modern Wayland desktop management.
"""

import sys
import os
import subprocess
import shutil
import platform
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib


class FedoroSettingsWindow(Adw.ApplicationWindow):
    def __init__(self, *args, target_page=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Fedoro Settings")
        self.set_default_size(920, 680)

        # Main Layout: Navigation View / View Stack with ViewSwitcher
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header bar
        self.header = Adw.HeaderBar()
        self.header.set_show_title(False)
        self.main_box.append(self.header)

        # View Stack & Switcher
        self.view_stack = Adw.ViewStack()
        
        switcher = Adw.ViewSwitcherTitle()
        switcher.set_stack(self.view_stack)
        switcher.set_title("Fedoro Settings")
        self.header.set_title_widget(switcher)

        # Add Settings Pages
        self._add_appearance_page()
        self._add_display_page()
        self._add_shortcuts_page()
        self._add_system_info_page()

        self.main_box.append(self.view_stack)

        if target_page:
            self.view_stack.set_visible_child_name(target_page)

    def _add_appearance_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp(maximum_size=720, margin_top=20, margin_bottom=20)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        clamp.set_child(box)

        # Color Theme Group
        theme_group = Adw.PreferencesGroup()
        theme_group.set_title("Desktop Style and Color Scheme")

        dark_row = Adw.ActionRow(
            title="Dark Mode",
            subtitle="Deep navy and cyan glassmorphism palette"
        )
        self.dark_switch = Gtk.Switch()
        self.dark_switch.set_active(True)
        self.dark_switch.set_valign(Gtk.Align.CENTER)
        self.dark_switch.connect("state-set", self._on_dark_switch_toggled)
        dark_row.add_suffix(self.dark_switch)
        theme_group.add(dark_row)

        blur_row = Adw.ActionRow(
            title="Window Blur and Transparency",
            subtitle="Enable hardware-accelerated background blur in Hyprland"
        )
        self.blur_switch = Gtk.Switch()
        self.blur_switch.set_active(True)
        self.blur_switch.set_valign(Gtk.Align.CENTER)
        self.blur_switch.connect("state-set", self._on_blur_switch_toggled)
        blur_row.add_suffix(self.blur_switch)
        theme_group.add(blur_row)

        box.append(theme_group)

        # Wallpapers Group
        wall_group = Adw.PreferencesGroup()
        wall_group.set_title("Wallpaper")
        wall_group.set_description("Select your desktop background.")

        wall_row = Adw.ActionRow(title="Active Wallpaper")
        
        btn_dark_wall = Gtk.Button(label="Default Dark")
        btn_dark_wall.connect("clicked", lambda b: self._set_wallpaper("fedoro-default-dark.png"))
        
        btn_light_wall = Gtk.Button(label="Default Light")
        btn_light_wall.connect("clicked", lambda b: self._set_wallpaper("fedoro-default-light.png"))

        btn_custom = Gtk.Button(label="Browse File...")
        btn_custom.connect("clicked", self._browse_custom_wallpaper)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.append(btn_dark_wall)
        btn_box.append(btn_light_wall)
        btn_box.append(btn_custom)
        wall_row.add_suffix(btn_box)
        wall_group.add(wall_row)

        box.append(wall_group)

        self.view_stack.add_titled_with_icon(
            scroll, "appearance", "Appearance", "preferences-desktop-theme-symbolic"
        )

    def _add_display_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp(maximum_size=720, margin_top=20, margin_bottom=20)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Displays and HiDPI Scaling")
        group.set_description("Configure resolution, refresh rate and fractional scaling.")

        # Scale selector
        scale_row = Adw.ComboRow()
        scale_row.set_title("Display Scale")
        scale_row.set_subtitle("Adjust UI sizing for 2K/4K high-density monitors")
        
        scale_model = Gtk.StringList.new([
            "100% (Standard / 1.0x)",
            "125% (Fractional / 1.25x)",
            "150% (Recommended for 4K / 1.5x)",
            "175% (Fractional / 1.75x)",
            "200% (HiDPI Retina / 2.0x)"
        ])
        scale_row.set_model(scale_model)
        scale_row.set_selected(0)
        scale_row.connect("notify::selected", self._on_scale_selected)
        group.add(scale_row)

        # Refresh rate preference
        vrr_row = Adw.ActionRow(
            title="Variable Refresh Rate (VRR / FreeSync)",
            subtitle="Reduce screen tearing and stutter in compatible monitors"
        )
        vrr_switch = Gtk.Switch(active=True, valign=Gtk.Align.CENTER)
        vrr_switch.connect("state-set", self._on_vrr_toggled)
        vrr_row.add_suffix(vrr_switch)
        group.add(vrr_row)

        # Multi-monitor setup guidance
        info_row = Adw.ActionRow(
            title="Multi-Monitor Layout",
            subtitle="Configured via ~/.config/hypr/monitors.conf"
        )
        btn_edit_mon = Gtk.Button(label="Open Config")
        btn_edit_mon.connect("clicked", self._open_monitors_conf)
        info_row.add_suffix(btn_edit_mon)
        group.add(info_row)

        box.append(group)

        self.view_stack.add_titled_with_icon(
            scroll, "display", "Display", "video-display-symbolic"
        )

    def _add_shortcuts_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp(maximum_size=720, margin_top=20, margin_bottom=20)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Keyboard Shortcuts and Window Rules")
        group.set_description("View and customize Hyprland desktop bindings.")

        edit_row = Adw.ActionRow(
            title="Keybindings Configuration File",
            subtitle="Stored in ~/.config/hypr/keybindings.conf"
        )
        btn_edit = Gtk.Button(label="Edit Keybindings")
        btn_edit.connect("clicked", self._open_keybindings_conf)
        edit_row.add_suffix(btn_edit)
        group.add(edit_row)

        # Searchable list of common bindings
        shortcuts_list = [
            ("Super + Space", "Rofi Application Launcher"),
            ("Super + Return", "Default Terminal Emulator"),
            ("Super + E", "File Manager (Nautilus)"),
            ("Super + B", "Web Browser (Firefox)"),
            ("Super + I", "Fedoro Settings"),
            ("Super + S", "Fedoro App Store"),
            ("Super + Q", "Close Window"),
            ("Super + F", "Fullscreen Toggle"),
            ("Super + V", "Floating Window Toggle"),
            ("Super + L", "Lock Screen"),
            ("Super + Shift + S", "Interactive Screenshot"),
            ("Super + Esc", "Power / Session Menu"),
        ]

        for key, desc in shortcuts_list:
            r = Adw.ActionRow(title=desc)
            l = Gtk.Label(label=key)
            l.add_css_class("heading")
            l.add_css_class("accent")
            r.add_suffix(l)
            group.add(r)

        box.append(group)

        self.view_stack.add_titled_with_icon(
            scroll, "shortcuts", "Shortcuts", "input-keyboard-symbolic"
        )

    def _add_system_info_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp(maximum_size=720, margin_top=20, margin_bottom=20)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        clamp.set_child(box)

        # OS Details Group
        os_group = Adw.PreferencesGroup()
        os_group.set_title("System Specifications and Versions")

        row_os = Adw.ActionRow(title="Operating System", subtitle="Fedoro OS 41 (Wayland Edition)")
        row_os.add_prefix(Gtk.Image.new_from_icon_name("system-software-install-symbolic"))
        os_group.add(row_os)

        row_base = Adw.ActionRow(title="Base Distribution", subtitle="Fedora Linux (RPM / DNF5 Base)")
        os_group.add(row_base)

        row_wm = Adw.ActionRow(title="Window Manager / Compositor", subtitle="Hyprland (Wayland Native)")
        os_group.add(row_wm)

        kernel_str = platform.uname().release
        row_kernel = Adw.ActionRow(title="Linux Kernel", subtitle=kernel_str)
        os_group.add(row_kernel)

        row_sec = Adw.ActionRow(title="Security Architecture", subtitle="SELinux (Enforcing)")
        os_group.add(row_sec)

        arch_str = platform.machine()
        row_arch = Adw.ActionRow(title="Architecture", subtitle=arch_str)
        os_group.add(row_arch)

        # Hardware summary
        try:
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            mem_gib = mem_bytes / (1024 ** 3)
            row_mem = Adw.ActionRow(title="Installed Memory (RAM)", subtitle=f"{mem_gib:.1f} GiB")
            os_group.add(row_mem)
        except Exception:
            pass

        box.append(os_group)

        self.view_stack.add_titled_with_icon(
            scroll, "about", "About", "help-about-symbolic"
        )

    def _on_dark_switch_toggled(self, switch, state):
        style_manager = Adw.StyleManager.get_default()
        if state:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

    def _on_blur_switch_toggled(self, switch, state):
        val = 1 if state else 0
        try:
            subprocess.run(["hyprctl", "keyword", "decoration:blur:enabled", str(val)], check=False)
        except Exception:
            pass

    def _set_wallpaper(self, filename):
        path = os.path.join("/usr/share/backgrounds/fedoro", filename)
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../branding/wallpapers", filename)
        
        try:
            subprocess.run(["hyprctl", "hyprpaper", "wallpaper", f",{path}"], check=False)
            subprocess.run(["swaybg", "-i", path, "-m", "fill"], check=False)
        except Exception:
            pass

    def _browse_custom_wallpaper(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Wallpaper Image")
        dialog.open(self, None, self._on_wallpaper_selected)

    def _on_wallpaper_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                path = file.get_path()
                subprocess.run(["hyprctl", "hyprpaper", "wallpaper", f",{path}"], check=False)
        except Exception:
            pass

    def _on_scale_selected(self, combo, param):
        idx = combo.get_selected()
        scales = ["1.0", "1.25", "1.5", "1.75", "2.0"]
        scale_val = scales[idx]
        try:
            # Dynamically set scale for all active outputs
            subprocess.run(["hyprctl", "keyword", "monitor", f",preferred,auto,{scale_val}"], check=False)
        except Exception:
            pass

    def _on_vrr_toggled(self, switch, state):
        val = 1 if state else 0
        try:
            subprocess.run(["hyprctl", "keyword", "misc:vrr", str(val)], check=False)
        except Exception:
            pass

    def _open_monitors_conf(self, button):
        path = os.path.expanduser("~/.config/hypr/monitors.conf")
        self._open_file(path)

    def _open_keybindings_conf(self, button):
        path = os.path.expanduser("~/.config/hypr/keybindings.conf")
        self._open_file(path)

    def _open_file(self, path):
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("# Fedoro custom configuration\n")
        subprocess.Popen(["xdg-open", path])


class FedoroSettingsApp(Adw.Application):
    def __init__(self, target_page=None, **kwargs):
        super().__init__(application_id="org.fedoro.settings", **kwargs)
        self.target_page = target_page

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FedoroSettingsWindow(application=self, target_page=self.target_page)
        win.present()


def main():
    target_page = None
    if "--page" in sys.argv:
        try:
            idx = sys.argv.index("--page")
            target_page = sys.argv[idx + 1]
        except (IndexError, ValueError):
            pass

    if "--test-mode" in sys.argv:
        print("Fedoro Settings --test-mode: Initializing GTK4/Adw successfully.")
        app = FedoroSettingsApp()
        win = FedoroSettingsWindow(application=app, target_page=target_page)
        assert win is not None
        print("Fedoro Settings verification passed.")
        return 0

    app = FedoroSettingsApp(target_page=target_page)
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
