import flet as ft
from ui import theme

class SimpleCalcView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.display = ft.TextField(
            value="0",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=True,
            text_size=30,
            text_style=ft.TextStyle(weight="bold"),
            border_radius=15,
            bgcolor=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_300
        )
        
        self.expression = ""

        # Calculator Grid
        buttons = [
            ["C", "DEL", "/", "*"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["0", ".", " "]
        ]
        
        btn_rows = []
        for row in buttons:
            row_controls = []
            for btn_text in row:
                if btn_text == " ": continue
                
                is_op = btn_text in ["/", "*", "-", "+", "="]
                is_clear = btn_text in ["C", "DEL"]
                
                color = ft.Colors.BLUE_500 if is_op else (ft.Colors.RED_400 if is_clear else theme.PRIMARY_COLOR)
                bg = ft.Colors.BLUE_50 if is_op else (ft.Colors.RED_50 if is_clear else ft.Colors.GREY_50)
                
                btn = ft.Container(
                    content=ft.Text(btn_text, size=20, weight="bold", color=color),
                    width=65,
                    height=65,
                    bgcolor=bg,
                    border_radius=15,
                    alignment=ft.Alignment(0, 0),
                    ink=True,
                    on_click=lambda e, t=btn_text: self.on_click(t)
                )
                
                if btn_text == "0":
                    btn.width = 145 # Double width
                    
                row_controls.append(btn)
            btn_rows.append(ft.Row(row_controls, alignment=ft.MainAxisAlignment.CENTER, spacing=15))

        self.content = ft.Column([
            ft.Container(height=40),
            ft.Row([
                ft.Icon(ft.Icons.CALCULATE, color=theme.PRIMARY_COLOR, size=30),
                ft.Text("Calculatrice", size=24, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=30),
            ft.Row([self.display], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            ft.Column(btn_rows, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def on_click(self, text):
        if text == "C":
            self.expression = ""
        elif text == "DEL":
            self.expression = self.expression[:-1]
        elif text == "=":
            try:
                # Basic safety check for eval
                safe_expr = self.expression.replace("*", "*").replace("/", "/")
                self.expression = str(eval(safe_expr, {"__builtins__": None}, {}))
            except:
                self.expression = "Error"
        else:
            if self.expression == "Error": self.expression = ""
            self.expression += text
            
        self.display.value = self.expression if self.expression else "0"
        self.update()
