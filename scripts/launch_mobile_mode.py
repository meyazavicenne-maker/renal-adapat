import flet as ft
import sys
import os

# Add src to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import main

def mobile_main(page: ft.Page):
    # Force mobile dimensions (iPhone 14-ish)
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False # Enforce the constraint
    
    # Run the standard main function
    main(page)

if __name__ == "__main__":
    print("Launching in Mobile Mode (390x844)...")
    ft.run(mobile_main)
