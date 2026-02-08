import flet as ft
import re
from ui.theme import (
    PRIMARY_COLOR, 
    PRIMARY_LIGHT,
    SURFACE_COLOR, 
    TEXT_COLOR_PRIMARY, 
    WARNING_TEXT_COLOR,
    BORDER_RADIUS,
    CARD_ELEVATION
)

class DrugCard(ft.Card):
    def __init__(self, drug, on_click, is_favorite=False):
        super().__init__()
        self.drug = drug
        
        # Design Tweaks
        self.elevation = CARD_ELEVATION
        self.color = SURFACE_COLOR
        self.shadow_color = ft.Colors.BLACK12 # Subtle shadow
        # ft.Card doesn't have border_radius in some versions, but Container does. 
        # Actually Card usually wraps Container.
        
        # We replace standard Card content with a styled Container
        
        trailing_icon = None
        if is_favorite:
            trailing_icon = ft.Icon(ft.Icons.STAR_ROUNDED, color="#FFC107", size=24) # Gold Star
        else:
             # Add a subtle arrow to indicate action
            trailing_icon = ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=ft.Colors.GREY_400)

        # Main Content
        self.content = ft.Container(
            content=ft.Row([
                # Leading Icon with background
                ft.Container(
                    content=ft.Icon(ft.Icons.MEDICATION_LIQUID_ROUNDED, color="white", size=24),
                    bgcolor=PRIMARY_COLOR,
                    padding=10,
                    border_radius=10,
                ),
                ft.VerticalDivider(width=10, color="transparent"),
                
                # Title
                ft.Text(
                    re.sub(r'\s+\d+$', '', drug["name"]), # Clean Name
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_COLOR_PRIMARY,
                    expand=True
                ),
                
                # Trailing Action
                trailing_icon
            ], alignment=ft.MainAxisAlignment.START),
            
            padding=15,
            border_radius=BORDER_RADIUS,
            ink=True, # Ripple effect
        )
        self.content.on_click = lambda e: on_click(drug["id"])

