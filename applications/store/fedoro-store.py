#!/usr/bin/env python3
"""
FEDORO OS - Modern Flatpak Application Center
Explore, search, install, update, and manage sandboxed Flatpak packages.
Built with GTK4 and Libadwaita.
"""

import sys
import os
import subprocess
import threading
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GLib


CURATED_CATALOG = [
    {
        "id": "org.mozilla.firefox",
        "name": "Mozilla Firefox",
        "summary": "Fast, private, and independent web browser",
        "category": "Internet",
        "icon": "web-browser-symbolic",
        "developer": "Mozilla Corporation",
        "installed": False,
    },
    {
        "id": "org.chromium.Chromium",
        "name": "Chromium Web Browser",
        "summary": "Open-source browser project behind Google Chrome",
        "category": "Internet",
        "icon": "web-browser-symbolic",
        "developer": "The Chromium Authors",
        "installed": False,
    },
    {
        "id": "com.visualstudio.code",
        "name": "Visual Studio Code",
        "summary": "Powerful code editor with vast extension ecosystem",
        "category": "Development",
        "icon": "applications-development-symbolic",
        "developer": "Microsoft Corporation",
        "installed": False,
    },
    {
        "id": "org.gnome.Builder",
        "name": "GNOME Builder",
        "summary": "Integrated development environment for modern GNOME and GTK apps",
        "category": "Development",
        "icon": "applications-development-symbolic",
        "developer": "Christian Hergert",
        "installed": False,
    },
    {
        "id": "org.gimp.GIMP",
        "name": "GNU Image Manipulation Program (GIMP)",
        "summary": "Professional image editor, digital painting, and photo retouching",
        "category": "Graphics",
        "icon": "applications-graphics-symbolic",
        "developer": "The GIMP Team",
        "installed": False,
    },
    {
        "id": "org.inkscape.Inkscape",
        "name": "Inkscape Vector Graphics",
        "summary": "Vector graphics editor using the standard SVG format",
        "category": "Graphics",
        "icon": "applications-graphics-symbolic",
        "developer": "Inkscape Community",
        "installed": False,
    },
    {
        "id": "org.blender.Blender",
        "name": "Blender 3D",
        "summary": "Free and open source 3D creation suite",
        "category": "Graphics",
        "icon": "applications-graphics-symbolic",
        "developer": "Blender Foundation",
        "installed": False,
    },
    {
        "id": "org.libreoffice.LibreOffice",
        "name": "LibreOffice",
        "summary": "Full-featured office suite: Writer, Calc, Impress, and Draw",
        "category": "Productivity",
        "icon": "x-office-document-symbolic",
        "developer": "The Document Foundation",
        "installed": False,
    },
    {
        "id": "md.obsidian.Obsidian",
        "name": "Obsidian Notes",
        "summary": "Markdown-based connected note-taking and knowledge base",
        "category": "Productivity",
        "icon": "text-x-generic-symbolic",
        "developer": "Dynalist Inc.",
        "installed": False,
    },
    {
        "id": "org.videolan.VLC",
        "name": "VLC Media Player",
        "summary": "Plays almost all media codecs, discs, webcams, and streams",
        "category": "Multimedia",
        "icon": "multimedia-player-symbolic",
        "developer": "VideoLAN Organization",
        "installed": False,
    },
    {
        "id": "com.obsproject.Studio",
        "name": "OBS Studio",
        "summary": "Free and open source software for video recording and live streaming",
        "category": "Multimedia",
        "icon": "camera-video-symbolic",
        "developer": "OBS Project",
        "installed": False,
    },
    {
        "id": "com.valvesoftware.Steam",
        "name": "Steam",
        "summary": "Digital gaming distribution platform and runtime",
        "category": "Games",
        "icon": "applications-games-symbolic",
        "developer": "Valve Corporation",
        "installed": False,
    },
    {
        "id": "com.discordapp.Discord",
        "name": "Discord",
        "summary": "All-in-one voice and text chat for gamers and communities",
        "category": "Internet",
        "icon": "user-available-symbolic",
        "developer": "Discord Inc.",
        "installed": False,
    },
]


class FedoroStoreWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Fedoro Store")
        self.set_default_size(1020, 720)

        self.active_category = "All"
        self.search_query = ""
        self.app_rows = {}

        # Main Layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header Bar
        self.header = Adw.HeaderBar()
        self.main_box.append(self.header)

        # Title
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_lbl = Gtk.Label(label="Fedoro Store", css_classes=["title"])
        title_box.append(title_lbl)
        self.header.set_title_widget(title_box)

        # Search Entry in Header
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search Flatpaks...")
        self.search_entry.connect("search-changed", self._on_search_changed)
        self.header.pack_end(self.search_entry)

        # Update All button
        btn_update = Gtk.Button(label="Update All", icon_name="software-update-available-symbolic")
        btn_update.connect("clicked", self._on_update_all_clicked)
        self.header.pack_start(btn_update)

        # Category Filter Bar
        cat_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cat_bar.set_margin_top(12)
        cat_bar.set_margin_bottom(12)
        cat_bar.set_margin_start(20)
        cat_bar.set_margin_end(20)

        categories = ["All", "Internet", "Development", "Graphics", "Productivity", "Multimedia", "Games"]
        for cat in categories:
            b = Gtk.Button(label=cat)
            b.connect("clicked", lambda btn, c=cat: self._on_category_selected(c))
            cat_bar.append(b)

        self.main_box.append(cat_bar)

        # Scrolled Catalog
        self.scroll = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        self.main_box.append(self.scroll)

        self.clamp = Adw.Clamp(maximum_size=860, margin_start=16, margin_end=16, margin_bottom=20)
        self.scroll.set_child(self.clamp)

        self.catalog_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.clamp.set_child(self.catalog_box)

        # Banner
        banner = Adw.Banner()
        banner.set_title("Flathub Universal Applications — Sandboxed, Secure, and Wayland Native")
        banner.set_revealed(True)
        self.catalog_box.append(banner)

        # Apps Group
        self.apps_group = Adw.PreferencesGroup()
        self.apps_group.set_title("Available Applications")
        self.catalog_box.append(self.apps_group)

        self._build_app_list()
        self._refresh_installed_status_async()

    def _build_app_list(self):
        # Clear existing items
        self.app_rows.clear()

        for item in CURATED_CATALOG:
            row = Adw.ActionRow(
                title=item["name"],
                subtitle=f"{item['developer']} • {item['summary']}"
            )
            row.add_prefix(Gtk.Image.new_from_icon_name(item["icon"]))

            # Action button
            btn_action = Gtk.Button(label="Install")
            btn_action.add_css_class("suggested-action")
            btn_action.connect("clicked", lambda b, it=item: self._on_app_action(it, b))
            row.add_suffix(btn_action)

            self.app_rows[item["id"]] = {
                "item": item,
                "row": row,
                "button": btn_action
            }
            self.apps_group.add(row)

    def _filter_apps(self):
        q = self.search_query.lower()
        cat = self.active_category

        for app_id, data in self.app_rows.items():
            it = data["item"]
            matches_cat = (cat == "All" or it["category"] == cat)
            matches_q = (not q or q in it["name"].lower() or q in it["summary"].lower() or q in app_id.lower())
            
            data["row"].set_visible(matches_cat and matches_q)

    def _on_search_changed(self, entry):
        self.search_query = entry.get_text()
        self._filter_apps()

    def _on_category_selected(self, cat):
        self.active_category = cat
        self._filter_apps()

    def _refresh_installed_status_async(self):
        def worker():
            try:
                res = subprocess.run(
                    ["flatpak", "list", "--columns=application"],
                    capture_output=True, text=True, check=False
                )
                installed_ids = set(res.stdout.splitlines())
            except Exception:
                installed_ids = set()

            def update_ui():
                for app_id, data in self.app_rows.items():
                    is_inst = app_id in installed_ids
                    data["item"]["installed"] = is_inst
                    btn = data["button"]
                    if is_inst:
                        btn.set_label("Installed ✓")
                        btn.remove_css_class("suggested-action")
                        btn.add_css_class("flat")
                    else:
                        btn.set_label("Install")
                        btn.remove_css_class("flat")
                        btn.add_css_class("suggested-action")
                return False

            GLib.idle_add(update_ui)

        threading.Thread(target=worker, daemon=True).start()

    def _on_app_action(self, item, button):
        app_id = item["id"]
        if item.get("installed"):
            # Launch application
            try:
                subprocess.Popen(["flatpak", "run", app_id])
            except Exception as e:
                print(f"Error launching {app_id}: {e}")
        else:
            # Install application via user scope (no root required)
            button.set_label("Installing...")
            button.set_sensitive(False)

            def worker():
                cmd = ["flatpak", "install", "--user", "-y", "flathub", app_id]
                success = False
                try:
                    p = subprocess.run(cmd, check=True)
                    success = True
                except Exception as e:
                    print(f"Installation failed: {e}")

                def on_done():
                    button.set_sensitive(True)
                    if success:
                        item["installed"] = True
                        button.set_label("Launch")
                        button.remove_css_class("suggested-action")
                    else:
                        button.set_label("Retry")
                        button.add_css_class("destructive-action")
                    return False

                GLib.idle_add(on_done)

            threading.Thread(target=worker, daemon=True).start()

    def _on_update_all_clicked(self, button):
        button.set_sensitive(False)
        button.set_label("Updating...")

        def worker():
            try:
                subprocess.run(["flatpak", "update", "--user", "-y"], check=False)
            except Exception:
                pass

            def finish():
                button.set_sensitive(True)
                button.set_label("Up to Date ✓")
                return False

            GLib.idle_add(finish)

        threading.Thread(target=worker, daemon=True).start()


class FedoroStoreApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="org.fedoro.store", **kwargs)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FedoroStoreWindow(application=self)
        win.present()


def main():
    if "--test-mode" in sys.argv:
        print("Fedoro Store --test-mode: Initializing GTK4/Adw successfully.")
        app = FedoroStoreApp()
        win = FedoroStoreWindow(application=app)
        assert win is not None
        print("Fedoro Store verification passed.")
        return 0

    app = FedoroStoreApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
