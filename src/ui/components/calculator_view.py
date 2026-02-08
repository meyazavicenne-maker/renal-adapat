import flet as ft
import math
from core.formulas import (
    convert_creat_to_mgdl, 
    calculate_cockcroft_gault, 
    calculate_mdrd, 
    calculate_ckd_epi, 
    calculate_schwartz,
    calculate_corrected_sodium,
    calculate_water_deficit,
    calculate_anion_gap,
    calculate_ktv_daugirdas,
    calculate_corrected_calcium,
    calculate_iron_deficit
)
from ui.components.numpad import Numpad
from ui import theme

class CalculatorView(ft.Container):
    def set_category(self, category_key):
        # Programmatic category switch
        self.category_dropdown.value = category_key
        # Trigger update
        self.on_category_change(None)

    def __init__(self):
        super().__init__()
        print("DEBUG: CalculatorView RELOADED with COLORS!")
        self.expand = True
        self.bgcolor = ft.Colors.WHITE
        self.border_radius = ft.BorderRadius(20, 20, 0, 0)
        
        # State
        self.active_input = None
        self.numpad = Numpad(self.on_numpad_press)

        # --- Selectors ---
        self.category_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("gfr", "Fonction Rénale (DFG)"),
                ft.dropdown.Option("electrolytes", "Électrolytes & Métabolisme"),
                ft.dropdown.Option("hematology", "Thérapeutique & Fer"),
            ],
            value="gfr",
            label="Catégorie",
            expand=True
        )
        self.category_dropdown.on_change = self.on_category_change

        # Container to hold the dynamic dropdown
        self.formula_container = ft.Container() # Replaces static dropdown usage

        # --- Input Creation Helper with Icons & Colors ---
        def create_numeric_input(label, suffix="", ref_name=None, icon=None, active_color=None): # NO DEFAULT
             if not active_color: active_color = "#9E9E9E" # Fallback Grey if missed
             
             # The actual text field
             tf = ft.TextField(
                 suffix=ft.Text(suffix, size=12, color="grey") if suffix else None,
                 expand=True, 
                 read_only=False,
                 value="",
                 text_align=ft.TextAlign.RIGHT,
                 border=ft.InputBorder.NONE,
                 height=40,
                 text_style=ft.TextStyle(size=18, weight="bold", color=theme.TEXT_COLOR_PRIMARY)
             )
             
             if ref_name: setattr(self, ref_name, tf)
             
             print(f"DEBUG: creating input '{label}' with active_color={active_color}")
             
             # The Card Container
             card = ft.Container(
                 content=ft.Row([
                     ft.Container(
                         content=ft.Icon(icon, color=active_color, size=24) if icon else None,
                         padding=ft.Padding(0, 0, 15, 0)
                     ),
                     ft.Text(label, size=14, color=theme.TEXT_COLOR_SECONDARY, expand=True, weight="w500"),
                     ft.Container(tf, width=120)
                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                 padding=ft.Padding(15, 8, 15, 8),
                 bgcolor=ft.Colors.with_opacity(0.05, active_color), 
                 border_radius=12,
                 border=ft.border.only(left=ft.BorderSide(4, active_color)),
                 shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
                 ink=True
             )
             card.on_click = lambda _: self.activate_input(tf)
             return card

        # GFR / Common - HEX PURPLE
        self.creat_input = create_numeric_input("Creatinine", "mg/L", "creat_input_field", ft.Icons.SCIENCE, "#9C27B0")
        
        self.creat_unit = ft.Dropdown(
            options=[ft.dropdown.Option("mg/L"), ft.dropdown.Option("mg/dL"), ft.dropdown.Option("µmol/L")],
            value="mg/L", width=80, text_size=12, border=ft.InputBorder.NONE
        )
        self.creat_unit.on_change = self.on_creat_unit_change
        
        creat_row_content = ft.Container(
                 content=ft.Row([
                     ft.Container(
                         content=ft.Icon(ft.Icons.SCIENCE, color="#9C27B0", size=24), # HEX
                         padding=ft.Padding(0, 0, 15, 0)
                     ),
                     ft.Text("Creatinine", size=14, color=theme.TEXT_COLOR_SECONDARY, expand=True, weight="w500"),
                     ft.Row([
                        ft.Container(self.creat_input_field, width=80),
                        ft.Container(self.creat_unit, width=80) 
                     ], spacing=0)
                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                 padding=ft.Padding(15, 8, 5, 8),
                 bgcolor=ft.Colors.with_opacity(0.05, "#9C27B0"),
                 border_radius=12,
                 border=ft.border.only(left=ft.BorderSide(4, "#9C27B0")),
                 shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
                 ink=True,
                 on_click=lambda _: self.activate_input(self.creat_input_field)
        )

        # HEX COLORS: Orange, BlueGrey, Green
        self.age_input = create_numeric_input("Age", "years", "age_input_field", ft.Icons.CALENDAR_TODAY, "#FF9800")
        self.weight_input = create_numeric_input("Weight", "kg", "weight_input_field", ft.Icons.MONITOR_WEIGHT, "#607D8B")
        self.height_input = create_numeric_input("Height", "cm", "height_input_field", ft.Icons.HEIGHT, "#4CAF50")
        
        self.sex_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="M", label="Male", active_color="#3F51B5"), 
                ft.Radio(value="F", label="Female", active_color="#3F51B5")
            ], alignment="center"),
            value="M"
        )
        sex_card = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON, color="#3F51B5", size=24), # HEX INDIGO
                ft.Container(width=10),
                ft.Text("Sex", size=14, color=theme.TEXT_COLOR_SECONDARY),
                ft.Container(content=self.sex_radio, expand=True, alignment=ft.Alignment(1.0, 0.0))
            ]),
            padding=ft.Padding(15, 8, 15, 8), bgcolor=ft.Colors.WHITE, border_radius=12,
            border=ft.border.only(left=ft.BorderSide(4, "#3F51B5")),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
            ink=True,
            on_click=lambda _: self.activate_input(None)
        )

        self.race_switch = ft.Switch(label="Black (Afro-Am.)", value=False, active_color="#795548")
        race_card = ft.Container(
            content=ft.Row([
                 ft.Icon(ft.Icons.PUBLIC, color="#795548", size=24), # HEX BROWN
                 ft.Container(width=10),
                 ft.Container(content=self.race_switch, expand=True)
            ]),
            padding=ft.Padding(15, 8, 15, 8), bgcolor=ft.Colors.WHITE, border_radius=12,
            border=ft.border.only(left=ft.BorderSide(4, "#795548")),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
            ink=True
        )
        
        # Electrolytes - HEX COLORS (Blue, Cyan, LightBlue, Pink)
        self.na_input = create_numeric_input("Sodium (Na+)", "mEq/L", "na_input_field", ft.Icons.WATER_DROP, "#2196F3")
        self.cl_input = create_numeric_input("Chloride (Cl-)", "mEq/L", "cl_input_field", ft.Icons.SCIENCE, "#00BCD4")
        self.hco3_input = create_numeric_input("Bicarbonate", "mEq/L", "hco3_input_field", ft.Icons.AIR, "#03A9F4")
        self.k_input = create_numeric_input("Potassium (K+)", "mEq/L", "k_input_field", ft.Icons.OPACITY, "#4CAF50")
        self.glucose_input_field = ft.TextField(
             expand=True, read_only=False, value="", text_align=ft.TextAlign.RIGHT,
             border=ft.InputBorder.NONE, height=40,
             text_style=ft.TextStyle(size=18, weight="bold", color=theme.TEXT_COLOR_PRIMARY)
        )
        self.glucose_unit = ft.Dropdown(
            options=[ft.dropdown.Option("mg/dL"), ft.dropdown.Option("g/L")],
            value="g/L", width=80, text_size=12, border=ft.InputBorder.NONE
        )
        
        glucose_row_content = ft.Container(
                 content=ft.Row([
                     ft.Container(
                         content=ft.Icon(ft.Icons.CAKE, color="#E91E63", size=24),
                         padding=ft.Padding(0, 0, 15, 0)
                     ),
                     ft.Text("Glucose", size=14, color=theme.TEXT_COLOR_SECONDARY, expand=True, weight="w500"),
                     ft.Row([
                        ft.Container(self.glucose_input_field, width=80),
                        ft.Container(self.glucose_unit, width=80) 
                     ], spacing=0)
                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                 padding=ft.Padding(15, 8, 5, 8),
                 bgcolor=ft.Colors.with_opacity(0.05, "#E91E63"),
                 border_radius=12,
                 border=ft.border.only(left=ft.BorderSide(4, "#E91E63")),
                 shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 4)),
                 ink=True,
                 on_click=lambda _: self.activate_input(self.glucose_input_field)
        )
        
        # Dialysis - HEX COLORS (Red, Red900, Blue400, Amber)
        self.pre_bun = create_numeric_input("Pre-dialysis BUN", "g/L", "pre_bun_field", ft.Icons.BLOODTYPE, "#F44336")
        self.post_bun = create_numeric_input("Post-dialysis BUN", "g/L", "post_bun_field", ft.Icons.BLOODTYPE, "#B71C1C")
        self.uf_vol = create_numeric_input("UF Volume", "L", "uf_vol_field", ft.Icons.WATER, "#42A5F5")
        self.dial_hours = create_numeric_input("Duration", "h", "dial_hours_field", ft.Icons.TIMER, "#FFC107")
        
        # Hematology - HEX COLORS (Red Accent, Green Accent)
        self.actual_hb = create_numeric_input("Hb Actuelle", "g/dL", "actual_hb_field", ft.Icons.BLOODTYPE, "#D32F2F")
        self.target_hb = create_numeric_input("Hb Cible", "g/dL", "target_hb_field", ft.Icons.TRACK_CHANGES, "#388E3C")
        
        # Simple Calculator Input
        self.math_input = create_numeric_input("Calcul", "Expression", "math_input_field", ft.Icons.CALCULATE, "#673AB7")
        
        # New: Calcium & Albumin
        self.ca_input = create_numeric_input("Calcium total", "mg/L", "ca_input_field", ft.Icons.OPACITY, "#9FA8DA")
        self.ca_unit = ft.Dropdown(
            options=[ft.dropdown.Option("mg/L"), ft.dropdown.Option("mg/dL"), ft.dropdown.Option("mmol/L")],
            value="mg/L", width=80, text_size=12, border=ft.InputBorder.NONE
        )
        self.alb_input = create_numeric_input("Albumine", "g/L", "alb_input_field", ft.Icons.EGG, "#81C784")

        # Layout containers for visibility
        self.input_containers = {
            "creat": creat_row_content,
            "age": self.age_input,
            "sex": sex_card,
            "weight": self.weight_input,
            "height": self.height_input,
            "race": race_card,
            "na": self.na_input,
            "cl_hco3_k": ft.Column([self.cl_input, self.hco3_input, self.k_input], spacing=15),
            "dialysis_ext": ft.Column([self.uf_vol, self.dial_hours], spacing=15),
            "glucose": glucose_row_content,
            "ca_alb": ft.Column([
                ft.Row([self.ca_input, self.ca_unit]),
                self.alb_input
            ], spacing=15),
            "hb": ft.Column([self.actual_hb, self.target_hb], spacing=15),
            "math": self.math_input,
        }

        # --- Formula & Explanation Labels ---
        self.formula_display = ft.Container(
            content=ft.Text("", size=13, color="#757575", italic=True),
            padding=ft.Padding(10, 0, 10, 10)
        )
        self.explanation_display = ft.Container(
            content=ft.Column(spacing=5),
            visible=False,
            padding=20,
            bgcolor="#F5F5F5",
            border_radius=10
        )

        # Status for debugging (hidden by default)
        self.status_text = ft.Text("", size=12, italic=True, color="grey", visible=False)
        self.results_column = ft.Column(spacing=15)
        
        self.calculate_button = ft.ElevatedButton(
            "CALCULATE", icon=ft.Icons.CALCULATE, 
            style=ft.ButtonStyle(
                bgcolor=theme.PRIMARY_COLOR, 
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=15,
                elevation=5
            ),
            width=280 # Wider for mobile
        )
        self.calculate_button.on_click = self.calculate
        
        # We wrap inputs in a Column we can reference easily
        self.inputs_list = ft.Column(list(self.input_containers.values()), spacing=20) # More spacing
        
        # Initial Status
        self.header_text = ft.Text("Fonction Rénale (DFG)", style=theme.header_style(), size=24)
        
        form_content = ft.Column(
            [
                # Styled Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.MEDICAL_SERVICES, color=theme.PRIMARY_COLOR, size=30),
                        self.header_text
                    ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.Padding(0, 10, 0, 10)
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                # Stylish Formula Selection Container
                ft.Container(
                    content=ft.Column([
                        ft.Text("Choix de la Formule", size=12, color=theme.PRIMARY_COLOR, weight="bold"),
                        self.formula_container # Holds the dynamic radio selector
                    ]),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, theme.PRIMARY_COLOR), offset=ft.Offset(0, 4))
                ),
                
                self.formula_display,
                self.status_text,
                ft.Divider(height=25, color=ft.Colors.TRANSPARENT),
                
                self.inputs_list,
                
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                ft.Container(self.calculate_button, alignment=ft.Alignment(0, 0)),
                ft.Divider(height=20),
                
                # Results Section
                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.ANALYTICS, color=theme.SECONDARY_COLOR), ft.Text("Résultats", weight=ft.FontWeight.BOLD, size=20, color=theme.TEXT_COLOR_PRIMARY)]),
                        ft.Divider(height=10),
                        self.results_column,
                        ft.Divider(height=10),
                        self.explanation_display
                    ]),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    border=ft.border.all(1, ft.Colors.GREY_100),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 5))
                ),
                
                ft.Container(height=120) # Space for scrolling/Numpad
            ],
            scroll=ft.ScrollMode.AUTO, # Allow scrolling if content is long
        )

        # Numpad Container (Overlay)
        self.numpad_container = ft.Container(
            content=self.numpad, 
            bottom=0, left=0, right=0,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
            border_radius=ft.BorderRadius(25, 25, 0, 0),
            padding=ft.Padding(0, 20, 0, 0),
            visible=False # Hidden by default
        )

        self.content = ft.Stack([
            ft.Container(form_content, padding=25), # More padding
            self.numpad_container
        ])
        
        # Initial State (No calls to self.update here)
        self.init_dropdown_options()
        self.update_ui_state()

    def init_dropdown_options(self):
        # Default options for 'gfr'
        opts = [
            ft.dropdown.Option("ckd_epi", "CKD-EPI (2009)"),
            ft.dropdown.Option("mdrd", "MDRD (4-var)"),
            ft.dropdown.Option("cockcroft", "Cockcroft-Gault"),
            ft.dropdown.Option("schwartz", "Schwartz (Pediatric)"),
            ft.dropdown.Option("all", "Comparison (All)"),
        ]
        self.create_formula_selector(opts)

    def activate_input(self, tf):
        # Clear previous selection styling
        for container in self.input_containers.values():
            if isinstance(container, ft.Container):
                 container.bgcolor = ft.Colors.WHITE
            elif isinstance(container, ft.Column):
                 for child in container.controls:
                     if isinstance(child, ft.Container): child.bgcolor = ft.Colors.WHITE

        self.active_input = tf
        
        # Update numpad keys based on tool
        form = self.formula_selector.value
        if form == "simple_calc":
            self.numpad.set_extra_keys(["+", "-", "*", "/"])
        else:
            self.numpad.set_extra_keys([])
            
        if not tf: 
            self.numpad_container.visible = False
            if self.page: self.update()
            return

        # Highlight current selection
        # We find which container holds this tf
        for name, container in self.input_containers.items():
            found = False
            if isinstance(container, ft.Container) and (container.content == tf or (isinstance(container.content, ft.Row) and tf in container.content.controls)):
                found = True
            elif isinstance(container, ft.Column):
                for child in container.controls:
                    if isinstance(child, ft.Container) and (child.content == tf or (isinstance(child.content, ft.Row) and tf in child.content.controls)):
                        child.bgcolor = ft.Colors.BLUE_50
                        break
            
            if found:
                container.bgcolor = ft.Colors.BLUE_50
                break

        # Show numpad
        self.numpad_container.visible = True
        self.numpad.visible = True
        try:
            if self.page:
                 self.numpad_container.update()
                 self.update() # Refresh colors
        except:
            pass

    def on_numpad_press(self, key):
        if not self.active_input: return
        curr = self.active_input.value or ""
        if key == "BACK": self.active_input.value = curr[:-1]
        elif key == ".":
            if "." not in curr: self.active_input.value = curr + key
        elif key in ["+", "-", "*", "/"]:
            # Simple math support
            self.active_input.value = curr + key
        else: self.active_input.value = curr + key
        self.active_input.update()

    def on_creat_unit_change(self, e):
        # Update logic handled by view
        pass 

    def on_category_change(self, e):
        cat = self.category_dropdown.value
        if cat == "gfr":
            opts = [
                ft.dropdown.Option("ckd_epi", "CKD-EPI (2009)"),
                ft.dropdown.Option("mdrd", "MDRD (4-var)"),
                ft.dropdown.Option("cockcroft", "Cockcroft-Gault"),
                ft.dropdown.Option("schwartz", "Schwartz (Pédiatrique)"),
                ft.dropdown.Option("all", "Comparaison Multi-formules"),
            ]
        elif cat == "electrolytes":
            opts = [
                ft.dropdown.Option("corrected_na", "Sodium Corrigé (Glucose)"),
                ft.dropdown.Option("corrected_ca", "Calcémie Corrigée (Albu)"),
                ft.dropdown.Option("water_deficit", "Déficit en Eau Libre"),
                ft.dropdown.Option("anion_gap", "Trou Anionique"),
                ft.dropdown.Option("ganzoni", "Déficit en Fer (Ganzoni)"),
            ]
        
        # DYNAMIC RECREATION (RadioGroup Edition)
        self.create_formula_selector(opts)
        
        self.update_ui_state()
        
        header_labels = {
            "gfr": "Fonction Rénale (DFG)",
            "electrolytes": "Formules cliniques"
        }
        self.header_text.value = header_labels.get(cat, "Calculateurs")
        
        try:
            if self.page:
                self.formula_container.update() 
                self.category_dropdown.update()
                self.header_text.update()
                self.update() 
        except:
            pass
            
    def create_formula_selector(self, options):
        # Create RadioGroup for robustness (instead of Dropdown)
        radios = [
            ft.Radio(
                value=opt.key, 
                label=opt.text, 
                active_color=theme.PRIMARY_COLOR
            ) for opt in options
        ]
        
        self.formula_selector = ft.RadioGroup(
            content=ft.Column(radios, spacing=0),
            value=options[0].key,
            on_change=self.on_formula_change
        )
        
        # Place in container
        self.formula_container.content = self.formula_selector

    def on_formula_change(self, e):
        new_val = self.formula_selector.value
        print(f"DEBUG: on_formula_change EVENT FIRED. Internal={new_val}")
        
        self.update_ui_state()
        try:
            if self.page:
                self.update()
        except:
            pass

    def update_ui_state(self):
        cat = self.category_dropdown.value
        form = self.formula_selector.value
        
        print(f"DEBUG: REBUILDING UI for cat={cat} form={form}")

        # Determine which containers should be visible
        visible_keys = []
        
        if cat == "gfr":
            if form == "all":
                visible_keys.extend(["creat", "age", "sex", "weight", "height", "race"])
            elif form in ["ckd_epi", "mdrd"]:
                 visible_keys.extend(["creat", "age", "sex", "race"])
            elif form == "schwartz": 
                visible_keys.extend(["creat", "height"])
            elif form == "cockcroft": 
                visible_keys.extend(["creat", "age", "sex", "weight"])
            elif form == "ktv":
                visible_keys.extend(["dialysis_ext", "weight"])
                
        elif cat == "electrolytes":
            if form == "corrected_ca":
                visible_keys.append("ca_alb")
            elif form == "ganzoni":
                visible_keys.extend(["weight", "hb"])
            else:
                visible_keys.append("na")
                if form == "corrected_na": 
                    visible_keys.append("glucose")
                elif form == "water_deficit": 
                    visible_keys.extend(["weight", "age", "sex"])
                elif form == "anion_gap": 
                    visible_keys.append("cl_hco3_k")
                elif form == "simple_calc":
                    visible_keys.append("math")
            
            # cat == 'dialysis' block removed as form 'ktv' is now under 'gfr'

        print(f"DEBUG: Selected Keys: {visible_keys}")

        # 1. CLEAR existing controls
        self.inputs_list.controls.clear()
        
        # 2. REBUILD list with ONLY required content
        # Also force visible=True/height=None just in case they were smashed before
        for k in visible_keys:
            if k in self.input_containers:
                container = self.input_containers[k]
                container.visible = True
                container.height = None
                container.opacity = 1
                
                # Restore children recursively
                if isinstance(container, ft.Column):
                    for child in container.controls:
                        child.visible = True
                        child.height = None
                        child.opacity = 1
                        
                self.inputs_list.controls.append(container)
        
        # 3. Update Formula Display
        formulas = {
            "ckd_epi": "141 * min(Cr/k, 1)^α * max(Cr/k, 1)^-1.209 * 0.993^Age [* 1.018 si F] [* 1.159 si Noir]",
            "mdrd": "175 * (Cr)^-1.154 * (Age)^-0.203 [* 0.742 si F] [* 1.212 si Noir]",
            "cockcroft": "((140 - Age) * Poids) / (72 * Cr) [* 0.85 si F]",
            "schwartz": "0.413 * Taille / Cr",
            "ktv": "-ln(R - 0.008*t) + (4 - 3.5*R) * (UF/Poids)",
            "corrected_na": "Na + 0.016 * (Glucose - 100)",
            "corrected_ca": "Ca + 0.8 * (40 - Albumine)",
            "water_deficit": "Eau Totale * ((Na / 140) - 1)",
            "anion_gap": "(Na + K) - (Cl + HCO3)",
            "ganzoni": "Poids * (Hb Cible - Hb Act) * 2.4 + Réserves",
            "all": "Comparaison multi-formules (CKD-EPI, MDRD, Cockcroft, Schwartz)"
        }
        self.formula_display.content.value = f"Formule: {formulas.get(form, '')}"
        
        try:
            if self.page:
                self.update() # FORCE FULL UPDATE
        except:
            pass

    def calculate(self, e):
        # Hide numpad on calculate
        self.numpad_container.visible = False
        try:
            if self.page: self.numpad_container.update() 
        except: pass

        try:
            val = lambda tf: float(tf.value.replace(',', '.')) if tf.value else 0.0
            results = []
            
            cat = self.category_dropdown.value
            form = self.formula_selector.value
            
            if cat == "gfr":
                cr = val(self.creat_input_field) # Use field ref
                unit = self.creat_unit.value
                if cr <= 0: return self.show_error("Creatinine required.")
                cr_mgdl = convert_creat_to_mgdl(cr, unit)
                age = val(self.age_input_field)
                sex = self.sex_radio.value
                weight = val(self.weight_input_field)
                height = val(self.height_input_field)
                race = self.race_switch.value
                
                if form in ["all", "ckd_epi"] and age > 0:
                    results.append(self.create_res("CKD-EPI", calculate_ckd_epi(age, cr_mgdl, sex, race), "mL/min/1.73m²"))
                if form in ["all", "mdrd"] and age > 0:
                    results.append(self.create_res("MDRD", calculate_mdrd(age, cr_mgdl, sex, race), "mL/min/1.73m²"))
                if form in ["all", "cockcroft"] and age > 0 and weight > 0:
                    results.append(self.create_res("Cockcroft-Gault", calculate_cockcroft_gault(age, weight, cr_mgdl, sex), "mL/min"))
                if form in ["all", "schwartz"] and height > 0:
                    results.append(self.create_res("Schwartz", calculate_schwartz(height, cr_mgdl), "mL/min/1.73m²"))
            
                if form == "ktv":
                    pre, post = val(self.pre_bun_field), val(self.post_bun_field)
                    w, uf, h = val(self.weight_input_field), val(self.uf_vol_field), val(self.dial_hours_field)
                    if pre <= 0 or w <= 0: return self.show_error("Data missing.")
                    results.append(self.create_res("spKt/V (Daugirdas)", calculate_ktv_daugirdas(pre, post, w, uf, h), ""))
            
            elif cat == "electrolytes":
                na = val(self.na_input_field)
                if na <= 0: return self.show_error("Sodium required.")
                if form == "corrected_na":
                    glancing = val(self.glucose_input_field)
                    if self.glucose_unit.value == "g/L": 
                        glancing *= 100 # g/L to mg/dL: 1 g/L = 100 mg/dL
                    results.append(self.create_res("Corrected Na", calculate_corrected_sodium(na, glancing), "mEq/L"))
                elif form == "corrected_ca":
                    # Calcium measured
                    ca_raw = val(self.ca_input_field)
                    if self.ca_unit.value == "mg/dL": ca_raw *= 10
                    elif self.ca_unit.value == "mmol/L": ca_raw *= 40 # 1 mmol/L = 40 mg/L
                    
                    alb = val(self.alb_input_field)
                    if ca_raw <= 0 or alb <= 0: return self.show_error("Data missing.")
                    
                    res_mgl = calculate_corrected_calcium(ca_raw, alb)
                    results.append(self.create_res("Calcémie Corrigée", res_mgl, "mg/L"))
                    results.append(self.create_res("Calcémie Corrigée", res_mgl/10.0, "mg/dL"))
                    results.append(self.create_res("Calcémie Corrigée", res_mgl/40.0, "mmol/L"))
                    group = 'adult' if age < 65 else 'elderly'
                    results.append(self.create_res("Water Deficit", calculate_water_deficit(w, na, sex, group), "L"))
                elif form == "anion_gap":
                    ag = calculate_anion_gap(na, val(self.k_input_field), val(self.cl_input_field), val(self.hco3_input_field))
                    results.append(self.create_res("Trou Anionique", ag, "mEq/L"))
                elif form == "ganzoni":
                    w = val(self.weight_input_field)
                    h_act = val(self.actual_hb_field)
                    h_tgt = val(self.target_hb_field)
                    
                    if w <= 0 or h_act <= 0 or h_tgt <= 0:
                        return self.show_error("Données manquantes (Poids, Hb).")
                    
                    deficit = calculate_iron_deficit(w, h_act, h_tgt, is_adult=(w > 35))
                    ampoules = math.ceil(deficit / 100)
                    
                    results.append(self.create_res("Déficit Total en Fer", deficit, "mg"))
                    results.append(self.create_res("Nombre d'ampoules (Venofer 100mg)", ampoules, "amp"))

            # Update Explanations
            explanations = {
                "gfr": "Normes (KDIGO) :\n• G1 : ≥ 90 (Nomal)\n• G2 : 60-89 (Baisse légère)\n• G3a : 45-59 (Baisse modérée)\n• G3b : 30-44 (Baisse sévère)\n• G4 : 15-29 (Insuffisance sévère)\n• G5 : < 15 (Défaillance rénale)\n*DFG < 60 pendant > 3 mois = Maladie Rénale Chronique.*",
                "ckd_epi": "Formule de référence actuelle (KDIGO 2012). Plus précise pour les DFG > 60 mL/min.",
                "mdrd": "Historiquement utilisée, peut sous-estimer le DFG chez les sujets sains.",
                "cockcroft": "Estime la Clairance de la Créatinine (non normalisée). Utilisée pour l'adaptation posologique de nombreux médicaments.",
                "schwartz": "Utilisée exclusivement en pédiatrie (< 18 ans). K=0.413.",
                "corrected_na": "Norme Na : 135-145 mmol/L.\nCorrection obligatoire en cas d'hyperglycémie car le glucose attire l'eau hors des cellules (dilution).",
                "corrected_ca": "Norme Ca : 2.2-2.6 mmol/L (88-104 mg/L).\nL'hypoalbuminémie fausse la calcémie totale. La forme active est le calcium ionisé.",
                "water_deficit": "Calcule le volume d'eau libre à administrer pour ramener la natrémie à 140 mEq/L.\nA corriger lentement (< 10-12 mmol/L par 24h) pour éviter l'oedème cérébral.",
                "anion_gap": "Norme : 12 ± 2 mEq/L.\nAcidose à TA élevé = ajout d'acide exogenous ou endogène (Cétose, Lactates, Toxiques, IR).\nAcidose à TA normal = perte digestive ou rénale de Bicarbonates.",
                "ganzoni": "Cible Hb : 13-15 g/dL (Sujet sain), 10-12 g/dL (MRC).\nRéserves en fer : 500mg (si poids > 35kg). Chaque ampoule de Venofer contient 100mg de fer élémentaire."
            }
            
            exp_key = form if form in explanations else (cat if cat in explanations else None)
            if exp_key:
                self.explanation_display.content.controls = [
                    ft.Text("Note Clinique:", size=12, weight="bold", color=theme.PRIMARY_COLOR),
                    ft.Text(explanations[exp_key], size=12, color=theme.TEXT_COLOR_SECONDARY)
                ]
                self.explanation_display.visible = True
            else:
                self.explanation_display.visible = False

            self.results_column.controls = results if results else [ft.Text("Missing data / Invalid input.", color="red")]
            self.results_column.update()
            
        except Exception as err:
            self.show_error(f"Error: {str(err)}")
    
    def create_res(self, title, value, unit):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.PRIMARY_COLOR, size=24),
                    ft.Column([
                        ft.Text(title, weight="bold", size=15, color=theme.TEXT_COLOR_PRIMARY),
                        ft.Text(unit, size=13, color=theme.TEXT_COLOR_SECONDARY)
                    ], spacing=2)
                ]),
                ft.Text(f"{value:.1f}" if value else "N/A", size=24, weight="bold", color=theme.PRIMARY_COLOR),
            ], alignment="spaceBetween"), 
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            border=ft.border.all(1, theme.PRIMARY_LIGHT),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.08, theme.PRIMARY_COLOR), offset=ft.Offset(0, 4)),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, 0.0),
                end=ft.Alignment(1.0, 0.0),
                colors=[ft.Colors.WHITE, ft.Colors.with_opacity(0.05, theme.PRIMARY_LIGHT)],
            )
        )

    def show_error(self, message):
        self.results_column.controls = [ft.Text(message, color="red")]
        self.results_column.update()
