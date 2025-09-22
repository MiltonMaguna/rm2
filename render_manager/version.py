# --------------------------------------------------------------------------------------------
# 05/2022 - 1.0.0 - Dev
# --------------------------------------------------------------------------------------------
import os

# qt ui file
ui_file = os.path.join(os.path.dirname(__file__), "ui", "main.ui")


__author__ = "Maximiliano Rocamora"

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

version = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

app_name = "RenderManager - Test"
__qt__ = f"Arcane:Qt_{app_name}_ui"
