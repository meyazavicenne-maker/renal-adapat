import flet as ft
from ui import theme

def create_header():
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LOCAL_HOSPITAL, size=40, color=ft.Colors.WHITE),
                ft.Text("NephroGuide", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Rapid Dosage Adjustment Guide", color=ft.Colors.WHITE70, italic=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=theme.PRIMARY_COLOR,
        padding=20,
        border_radius=ft.BorderRadius(0, 0, 20, 20),
    )
