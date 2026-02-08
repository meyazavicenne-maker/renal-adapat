import flet as ft

# Modern Medical Palette
PRIMARY_COLOR = "#37474F"      
PRIMARY_LIGHT = "#4DB6AC"      
SECONDARY_COLOR = "#00BCD4"    
BACKGROUND_COLOR = "#F4F7F6"   
SURFACE_COLOR = "#FFFFFF"      

# Bento / Modern UI Tokens
BENTO_MESH_COLORS = ["#1A237E", "#311B92", "#006064"] # Deep Navy, Deep Purple, Deep Teal
GLASS_BG = "rgba(255, 255, 255, 0.15)"
GLASS_BORDER = "rgba(255, 255, 255, 0.3)"

TEXT_COLOR_PRIMARY = "#263238" # Blue-Grey 900
TEXT_COLOR_SECONDARY = "#546E7A" # Blue-Grey 600

WARNING_COLOR = "#FFF8E1"      # Soft Amber background
WARNING_BORDER = "#FFC107"     # Amber border
WARNING_TEXT_COLOR = "#7F6000" # Dark Amber text

# Typography & Spacing
BORDER_RADIUS = 12
CARD_ELEVATION = 4

def get_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            secondary=SECONDARY_COLOR,
            surface=SURFACE_COLOR,
            on_primary="white",
            on_secondary="white",
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.CUPERTINO
        ),
        use_material3=False # Disable to prevent aggressive color overrides on icons
    )

def header_style():
    return ft.TextStyle(
        size=22, 
        weight=ft.FontWeight.W_700, 
        color=PRIMARY_COLOR,
        font_family="Roboto"
    )

def subheader_style():
    return ft.TextStyle(
        size=16, 
        weight=ft.FontWeight.W_600, 
        color=TEXT_COLOR_PRIMARY
    )

def body_style():
    return ft.TextStyle(
        size=15, 
        color=TEXT_COLOR_PRIMARY,
        height=1.4 # Better readability
    )

def caption_style():
    return ft.TextStyle(
        size=13, 
        color=TEXT_COLOR_SECONDARY,
        italic=True
    )
