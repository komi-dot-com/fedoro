#!/usr/bin/env python3
"""
FEDORO OS - Welcome & First Boot Setup Application
Built with GTK4 and Libadwaita for modern Wayland desktop experience.
"""

import sys
import os
import subprocess
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib


class FedoroWelcomeWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Welcome to Fedoro OS")
        self.set_default_size(860, 620)

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
        switcher.set_title("Welcome to Fedoro OS")
        switcher.set_subtitle("Wayland & Hyprland Edition")
        self.header.set_title_widget(switcher)

        # Add Pages
        self._add_overview_page()
        self._add_setup_page()
        self._add_apps_page()
        self._add_shortcuts_page()
        self._add_community_page()

        # Bottom Action Bar
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        bottom_bar.set_margin_top(8)
        bottom_bar.set_margin_bottom(12)
        bottom_bar.set_margin_start(16)
        bottom_bar.set_margin_end(16)

        self.autostart_check = Gtk.CheckButton(label="Show this welcome dialog on startup")
        self.autostart_check.set_active(True)
        self.autostart_check.connect("toggled", self._on_autostart_toggled)
        bottom_bar.append(self.autostart_check)

        spacer = Gtk.Box(hexpand=True)
        bottom_bar.append(spacer)

        btn_close = Gtk.Button(label="Get Started")
        btn_close.add_css_class("suggested-action")
        btn_close.connect("clicked", lambda b: self.close())
        bottom_bar.append(btn_close)

        self.main_box.append(self.view_stack)
        self.main_box.append(bottom_bar)

    def _add_overview_page(self):
        page = Adw.StatusPage()
        page.set_icon_name("system-software-install-symbolic")
        page.set_title("Welcome to Fedoro OS")
        page.set_description(
            "A modern, high-performance Linux distribution crafted with Fedora, Wayland, "
            "Hyprland, and the Flatpak universal application ecosystem."
        )

        clamp = Adw.Clamp()
        clamp.set_maximum_size(680)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        clamp.set_child(box)

        # Feature highlights group
        group = Adw.PreferencesGroup()
        group.set_title("Core Architecture and Highlights")

        row1 = Adw.ActionRow(
            title="Wayland Native and Hyprland",
            subtitle="Tear-free rendering, fluid animations, dynamic tiling, and multi-monitor scaling."
        )
        row1.add_prefix(Gtk.Image.new_from_icon_name("video-display-symbolic"))
        group.add(row1)

        row2 = Adw.ActionRow(
            title="Fedora RPM and DNF5 Base",
            subtitle="Rock-solid system packages, latest Linux kernel, and SELinux security enforced."
        )
        row2.add_prefix(Gtk.Image.new_from_icon_name("security-high-symbolic"))
        group.add(row2)

        row3 = Adw.ActionRow(
            title="Flatpak Sandboxed Applications",
            subtitle="Clean separation between core OS and desktop applications with Flathub integration."
        )
        row3.add_prefix(Gtk.Image.new_from_icon_name("software-properties-symbolic"))
        group.add(row3)

        box.append(group)
        page.set_child(clamp)

        self.view_stack.add_titled_with_icon(
            page, "overview", "Overview", "help-about-symbolic"
        )

    def _add_setup_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(680)
        clamp.set_margin_top(16)
        clamp.set_margin_bottom(16)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Initial Desktop Setup")
        group.set_description("Customize your experience with essential settings.")

        # Theme mode toggle
        theme_row = Adw.ActionRow(
            title="Theme Appearance",
            subtitle="Switch between Dark and Light visual styles"
        )
        btn_dark = Gtk.Button(label="Dark Mode")
        btn_dark.connect("clicked", lambda b: self._set_theme(dark=True))
        btn_light = Gtk.Button(label="Light Mode")
        btn_light.connect("clicked", lambda b: self._set_theme(dark=False))
        
        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        theme_box.append(btn_dark)
        theme_box.append(btn_light)
        theme_row.add_suffix(theme_box)
        group.add(theme_row)

        # Display & Scaling
        disp_row = Adw.ActionRow(
            title="Display and Scaling (HiDPI)",
            subtitle="Configure resolution, refresh rates, and scaling"
        )
        btn_disp = Gtk.Button(label="Display Settings")
        btn_disp.connect("clicked", lambda b: subprocess.Popen(["fedoro-settings", "--page", "display"]))
        disp_row.add_suffix(btn_disp)
        group.add(disp_row)

        # Network Settings
        net_row = Adw.ActionRow(
            title="Network and Wi-Fi",
            subtitle="Connect to wireless networks and configure VPNs"
        )
        btn_net = Gtk.Button(label="Network Setup")
        btn_net.connect("clicked", lambda b: subprocess.Popen(["nm-connection-editor"]))
        net_row.add_suffix(btn_net)
        group.add(net_row)

        # Audio Configuration
        snd_row = Adw.ActionRow(
            title="Audio Volume and Routing",
            subtitle="PipeWire and WirePlumber audio settings"
        )
        btn_snd = Gtk.Button(label="Audio Control")
        btn_snd.connect("clicked", lambda b: subprocess.Popen(["pavucontrol"]))
        snd_row.add_suffix(btn_snd)
        group.add(snd_row)

        box.append(group)

        self.view_stack.add_titled_with_icon(
            scroll, "setup", "Setup", "preferences-system-symbolic"
        )

    def _add_apps_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(680)
        clamp.set_margin_top(16)
        clamp.set_margin_bottom(16)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Flatpak and Software Repositories")
        group.set_description("Enable Flathub to access thousands of sandboxed applications.")

        # Flathub Enable
        flathub_row = Adw.ActionRow(
            title="Flathub Repository",
            subtitle="Universal repository for browsers, office suites, dev tools, and games"
        )
        self.btn_flathub = Gtk.Button(label="Enable Flathub")
        self.btn_flathub.add_css_class("suggested-action")
        self.btn_flathub.connect("clicked", self._enable_flathub)
        flathub_row.add_suffix(self.btn_flathub)
        group.add(flathub_row)

        # Launch Fedoro Store
        store_row = Adw.ActionRow(
            title="Fedoro App Store",
            subtitle="Browse and install software graphically"
        )
        btn_store = Gtk.Button(label="Open Store")
        btn_store.connect("clicked", lambda b: subprocess.Popen(["fedoro-store"]))
        store_row.add_suffix(btn_store)
        group.add(store_row)

        box.append(group)

        # Recommended Apps
        rec_group = Adw.PreferencesGroup()
        rec_group.set_title("Popular Curated Applications")

        apps = [
            ("Firefox Browser", "org.mozilla.firefox", "Fast and privacy-first web browser"),
            ("Visual Studio Code", "com.visualstudio.code", "Code editor and developer environment"),
            ("LibreOffice", "org.libreoffice.LibreOffice", "Complete office productivity suite"),
            ("VLC Media Player", "org.videolan.VLC", "Universal multimedia player"),
        ]

        for name, app_id, desc in apps:
            row = Adw.ActionRow(title=name, subtitle=desc)
            btn = Gtk.Button(label="Install")
            btn.connect("clicked", lambda b, aid=app_id: self._install_app(aid, b))
            row.add_suffix(btn)
            rec_group.add(row)

        box.append(rec_group)

        self.view_stack.add_titled_with_icon(
            scroll, "apps", "Apps", "software-properties-symbolic"
        )

    def _add_shortcuts_page(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        clamp = Adw.Clamp()
        clamp.set_maximum_size(680)
        clamp.set_margin_top(16)
        clamp.set_margin_bottom(16)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Hyprland Essential Shortcuts")
        group.set_description("Super key is typically the Windows key.")

        shortcuts = [
            ("Super + Space", "Open Application Launcher (Rofi)"),
            ("Super + Return", "Launch Terminal"),
            ("Super + E", "Open File Manager"),
            ("Super + B", "Open Web Browser"),
            ("Super + Q", "Close Focused Window"),
            ("Super + F", "Toggle Fullscreen"),
            ("Super + V", "Toggle Floating Window"),
            ("Super + L", "Lock Screen (Hyprlock)"),
            ("Super + Shift + S", "Screenshot Selection (Copy to clipboard)"),
            ("Super + 1..9", "Switch to Workspace 1 through 9"),
            ("Super + Shift + 1..9", "Move Active Window to Workspace"),
            ("Super + Escape", "Open System Power Menu"),
        ]

        for key, desc in shortcuts:
            row = Adw.ActionRow(title=desc)
            badge = Gtk.Label(label=key)
            badge.add_css_class("heading")
            badge.add_css_class("accent")
            row.add_suffix(badge)
            group.add(row)

        box.append(group)

        self.view_stack.add_titled_with_icon(
            scroll, "shortcuts", "Shortcuts", "input-keyboard-symbolic"
        )

    def _add_community_page(self):
        page = Adw.StatusPage()
        page.set_icon_name("dialog-information-symbolic")
        page.set_title("Documentation and Resources")
        page.set_description(
            "Access official Fedoro OS guides, report issues, and contribute to the project."
        )

        clamp = Adw.Clamp()
        clamp.set_maximum_size(680)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        clamp.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Online Resources")

        r1 = Adw.ActionRow(title="User Documentation and Architecture Guide")
        btn1 = Gtk.Button(label="Open Docs")
        btn1.connect("clicked", lambda b: Gio.AppInfo.launch_default_for_uri("https://github.com/fedoro-os/fedoro/tree/main/docs", None))
        r1.add_suffix(btn1)
        group.add(r1)

        r2 = Adw.ActionRow(title="Issue Tracker and Bug Reports")
        btn2 = Gtk.Button(label="Report Bug")
        btn2.connect("clicked", lambda b: Gio.AppInfo.launch_default_for_uri("https://github.com/fedoro-os/fedoro/issues", None))
        r2.add_suffix(btn2)
        group.add(r2)

        box.append(group)
        page.set_child(clamp)

        self.view_stack.add_titled_with_icon(
            page, "community", "Resources", "network-workgroup-symbolic"
        )

    def _set_theme(self, dark=True):
        style_manager = Adw.StyleManager.get_default()
        if dark:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

    def _enable_flathub(self, button):
        cmd = [
            "flatpak", "remote-add", "--if-not-exists", "flathub",
            "https://dl.flathub.org/repo/flathub.flatpakrepo"
        ]
        try:
            subprocess.run(cmd, check=True)
            button.set_label("Flathub Enabled ✓")
            button.set_sensitive(False)
        except Exception as e:
            button.set_label(f"Failed: {e}")

    def _install_app(self, app_id, button):
        button.set_sensitive(False)
        button.set_label("Installing...")
        cmd = ["flatpak", "install", "-y", "flathub", app_id]
        try:
            subprocess.Popen(cmd)
            button.set_label("Started")
        except Exception as e:
            button.set_label("Error")

    def _on_autostart_toggled(self, button):
        config_dir = os.path.expanduser("~/.config/fedoro")
        os.makedirs(config_dir, exist_ok=True)
        flag_file = os.path.join(config_dir, ".welcome_shown")
        if not button.get_active():
            with open(flag_file, "w") as f:
                f.write("1\n")
        else:
            if os.path.exists(flag_file):
                os.remove(flag_file)


class FedoroWelcomeApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="org.fedoro.welcome", **kwargs)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FedoroWelcomeWindow(application=self)
        win.present()


def main():
    if "--test-mode" in sys.argv:
        print("Fedoro Welcome --test-mode: Initializing GTK4/Adw successfully.")
        app = FedoroWelcomeApp()
        # Verify instantiation without opening blocking event loop
        win = FedoroWelcomeWindow(application=app)
        assert win is not None
        print("Fedoro Welcome verification passed.")
        return 0

    app = FedoroWelcomeApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
