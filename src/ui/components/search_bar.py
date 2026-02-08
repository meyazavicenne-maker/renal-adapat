import flet as ft

class SearchBar(ft.TextField):
    def __init__(self, on_change, on_clear):
        super().__init__()
        self.hint_text = "Search drug name (e.g. Amoxicillin)..."
        self.prefix_icon = ft.Icons.SEARCH
        self.suffix = ft.IconButton(ft.Icons.CLEAR)
        self.suffix.on_click = on_clear
        self.border_radius = 20
        self.filled = True
        self.expand = True
        self.on_change = on_change
