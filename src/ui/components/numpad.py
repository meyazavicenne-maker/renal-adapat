import flet as ft
from ui import theme

class Numpad(ft.Container):
    def __init__(self, on_keypress):
        super().__init__()
        self.on_keypress = on_keypress
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = ft.BorderRadius(20, 20, 0, 0)
        self.shadow = ft.BoxShadow(
            blur_radius=10,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, -2)
        )
        self.padding = 20
        self.visible = False
        self.extra_keys = [] # To be set dynamically
        
        self.rows_container = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        hide_btn = ft.Container(
            content=ft.Icon(ft.Icons.KEYBOARD_HIDE, color=ft.Colors.GREY_500),
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(0, 0, 0, 10),
        )
        hide_btn.on_click = lambda e: self.toggle(False)
            
        self.content = ft.Column([
            hide_btn,
            self.rows_container
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.render_keys()

    def set_extra_keys(self, keys):
        self.extra_keys = keys
        self.render_keys()
        self.update()

    def render_keys(self):
        # Base keys
        base_keys = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            [".", "0", "BACK"],
        ]
        
        # If we have extra keys, we add them as a column or row
        # For simplicity, let's add them as a trailing column if present
        all_rows = []
        for i, row in enumerate(base_keys):
            row_controls = []
            for key in row:
                row_controls.append(self.create_key_btn(key))
            
            # Add extra key if available for this row
            if i < len(self.extra_keys):
                row_controls.append(self.create_key_btn(self.extra_keys[i], is_extra=True))
            
            all_rows.append(ft.Row(row_controls, alignment=ft.MainAxisAlignment.SPACE_EVENLY))
        
        self.rows_container.controls = all_rows

    def create_key_btn(self, key, is_extra=False):
        is_back = key == "BACK"
        bg = ft.Colors.GREY_100 if not is_extra else ft.Colors.BLUE_50
        text_color = theme.PRIMARY_COLOR if not is_extra else ft.Colors.BLUE_700
        
        btn = ft.Container(
            content=ft.Text(
                key if not is_back else "", 
                size=22, 
                weight=ft.FontWeight.BOLD,
                color=text_color
            ),
            width=60, 
            height=60,
            bgcolor=bg,
            border_radius=30,
            alignment=ft.Alignment(0, 0),
            ink=True,
        )
        btn.on_click = lambda e, k=key: self.handle_click(k)
        
        if is_back:
            btn.content = ft.Icon(ft.Icons.BACKSPACE_OUTLINED, color=theme.PRIMARY_COLOR)
            btn.bgcolor = ft.Colors.RED_50
        
        return btn

    def handle_click(self, key):
        if self.on_keypress:
            self.on_keypress(key)

    def toggle(self, visible):
        self.visible = visible
        self.update()
