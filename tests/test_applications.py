#!/usr/bin/env python3
"""
FEDORO OS - Automated Test Suite for Custom System Applications
Tests instantiation, views, catalog, and data structures of Fedoro Welcome, Settings, and Store.
"""

import unittest
import sys
import os

# Add paths to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "applications/welcome"))
sys.path.insert(0, os.path.join(BASE_DIR, "applications/settings"))
sys.path.insert(0, os.path.join(BASE_DIR, "applications/store"))

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

welcome_mod = __import__("fedoro-welcome")
settings_mod = __import__("fedoro-settings")
store_mod = __import__("fedoro-store")


class TestFedoroApplications(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize GTK in headless mode
        Gtk.init()
        Adw.init()

    def test_fedoro_welcome_instantiation(self):
        app = welcome_mod.FedoroWelcomeApp()
        win = welcome_mod.FedoroWelcomeWindow(application=app)
        self.assertIsNotNone(win)
        self.assertEqual(win.get_title(), "Welcome to Fedoro OS")
        self.assertIsNotNone(win.view_stack)
        # Check pages
        pages = ["overview", "setup", "apps", "shortcuts", "community"]
        for p in pages:
            child = win.view_stack.get_child_by_name(p)
            self.assertIsNotNone(child, f"Page {p} not found in view_stack")

    def test_fedoro_settings_instantiation(self):
        app = settings_mod.FedoroSettingsApp()
        win = settings_mod.FedoroSettingsWindow(application=app, target_page="display")
        self.assertIsNotNone(win)
        self.assertEqual(win.get_title(), "Fedoro Settings")
        pages = ["appearance", "display", "shortcuts", "about"]
        for p in pages:
            child = win.view_stack.get_child_by_name(p)
            self.assertIsNotNone(child, f"Page {p} not found in view_stack")

    def test_fedoro_store_catalog(self):
        catalog = store_mod.CURATED_CATALOG
        self.assertGreater(len(catalog), 5)
        categories = {item["category"] for item in catalog}
        self.assertIn("Development", categories)
        self.assertIn("Productivity", categories)
        self.assertIn("Internet", categories)

        app = store_mod.FedoroStoreApp()
        win = store_mod.FedoroStoreWindow(application=app)
        self.assertIsNotNone(win)
        self.assertEqual(win.get_title(), "Fedoro Store")
        self.assertGreater(len(win.app_rows), 5)


if __name__ == "__main__":
    unittest.main()
