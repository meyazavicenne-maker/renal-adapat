import flet as ft
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_view import create_main_view
from ui import theme

def main(page: ft.Page):
    # Original page setup
    page.title = "Renal Drug Handbook"
    page.theme = theme.get_theme()
    page.theme_mode = ft.ThemeMode.LIGHT  # Force light mode, ignore system dark mode
    page.bgcolor = theme.BACKGROUND_COLOR
    page.padding = 0 # main_view handles padding mostly
    
    # Create the original main view
    content_area = create_main_view(page)
    
    page.add(content_area)
    page.update()

if __name__ == "__main__":
    # Desktop mode (more stable)
    ft.run(main)



