import flet as ft
from ui import theme

class HomeView(ft.Container):
    def __init__(self, on_navigate):
        super().__init__()
        self.on_navigate = on_navigate
        self.expand = True
        self.padding = 0
        self.margin = 0
        self.bgcolor = "#F8FAFB" # Ultra clean off-white
        
        # 1. Soft Medical Background Highlights
        self.bg_highlights = ft.Stack([
            ft.Container(
                expand=True,
                gradient=ft.RadialGradient(
                    center=ft.Alignment(0.7, -0.6),
                    radius=1.2,
                    colors=[ft.Colors.with_opacity(0.4, "#E3F2FD"), ft.Colors.TRANSPARENT]
                )
            ),
            ft.Container(
                expand=True,
                gradient=ft.RadialGradient(
                    center=ft.Alignment(-0.8, 0.4),
                    radius=1.0,
                    colors=[ft.Colors.with_opacity(0.3, "#E0F2F1"), ft.Colors.TRANSPARENT]
                )
            ),
        ], expand=True)

        # 2. Main Grid
        grid_content = ft.Column([
            ft.Container(height=40),
            ft.Text("NephroGuide", size=32, weight=ft.FontWeight.W_900, color=theme.PRIMARY_COLOR),
            ft.Text("Assistant Clinique de Néphrologie", size=14, color=ft.Colors.BLUE_GREY_400),
            ft.Container(height=40),
            
            ft.Row([
                self._create_glass_card("Recherche", "Dosage & Adaptation", ft.Icons.SEARCH, "search", "#2196F3"),
                self._create_glass_card("Rein (DFG)", "Estimation de la fonction", ft.Icons.ANALYTICS, "calc_gfr", "#9C27B0"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=25),
            
            ft.Row([
                self._create_glass_card("Formules", "Électrolytes & Fer", ft.Icons.WATER_DROP, "calc_electro", "#00BCD4"),
                self._create_glass_card("Calculatrice", "Outil Arithmétique", ft.Icons.CALCULATE, "simple_calc", "#4CAF50"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=25),
            
            ft.Container(expand=True),
            
            # Footer
            ft.Column([
                ft.Text("Based on The Renal Drug Handbook (2018)", color=ft.Colors.BLUE_GREY_300, size=11),
                ft.Text("Adapted by MEYAZ", weight="bold", color=theme.PRIMARY_COLOR, size=13),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        self.content = ft.Stack([
            self.bg_highlights,
            ft.Container(content=grid_content, padding=30, expand=True)
        ], expand=True)

    def _create_glass_card(self, title, subtitle, icon, nav_tag, accent_color):
        container = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=35, color=accent_color),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.05, accent_color),
                    border_radius=18,
                ),
                ft.Column([
                    ft.Text(title, weight="bold", size=17, color=theme.TEXT_COLOR_PRIMARY),
                    ft.Text(subtitle, size=11, color=ft.Colors.BLUE_GREY_400, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            width=175, height=190,
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), # Frosted white
            border_radius=28,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            blur=ft.Blur(12, 12, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(
                blur_radius=25,
                spread_radius=-8,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 12)
            ),
            ink=True,
            on_click=lambda e: self.on_navigate(nav_tag),
            padding=15
        )
        return container
