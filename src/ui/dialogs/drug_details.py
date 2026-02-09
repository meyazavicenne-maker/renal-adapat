import flet as ft
import re
from core.database import get_drug_details, toggle_favorite, is_favorite, add_to_history, update_drug
from core.parser import parse_drug_dosages
from ui import theme

def partition_rows(rows):
    renal_rows = []
    replacement_rows = []
    warnings = []
    interactions = []
    others = []
    
    dialysis_keys = ["APD/CAPD", "HD", "HDF/High flux", "CAV/VVHD"]
    
    for row in rows:
        cat = row["category"]
        cat_upper = cat.upper()
        
        # Priority 1: Warnings and Interactions
        if "WARNING" in cat_upper:
            warnings.append(row)
        elif "INTERACTION" in cat_upper:
            interactions.append(row)
        elif any(k in cat_upper for k in ["IMPORTANT", "NOTE", "COMMENT", "INFO", "ADMIN", "CLINICAL", "OTHER"]):
            others.append(row)
        elif any(k.upper() == cat_upper for k in dialysis_keys):
            replacement_rows.append(row)
        else:
            # GFR ranges usually
            renal_rows.append(row)
            
    return renal_rows, replacement_rows, warnings, interactions, others

def build_dose_table(rows, fallback_text):
    if not rows:
         return ft.Text(fallback_text or "Not specified", style=theme.body_style())
         
    # Use a Column of Rows instead of DataTable for better wrapping
    display_rows = []
    
    # Header
    display_rows.append(
        ft.Row([
            ft.Text("Clairance/Mode", weight=ft.FontWeight.BOLD, size=15, width=150, color=theme.PRIMARY_COLOR),
            ft.Text("Dosage", weight=ft.FontWeight.BOLD, size=15, expand=True, color=theme.PRIMARY_COLOR),
        ])
    )
    display_rows.append(ft.Divider(height=1, color=ft.Colors.GREY_400))
    
    for row in rows:
        display_rows.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(row["category"], weight=ft.FontWeight.W_500, size=14, width=150),
                    ft.Text(row["recommendation"], size=14, expand=True, selectable=True), # Larger text for readability
                ], vertical_alignment=ft.CrossAxisAlignment.START),
                padding=ft.Padding(0, 8, 0, 8)  # Increased padding for easier tapping
            )
        )
        display_rows.append(ft.Divider(height=0.5, color=ft.Colors.GREY_200))

    return ft.Column(display_rows, spacing=2)

def build_info_block(title, rows, bg_color, text_color=theme.PRIMARY_COLOR, icon=None):
    if not rows:
        return None
        
    content_rows = []
    for row in rows:
        cat = row['category']
        # If the category is generic (Note, Interaction) or matches the block title, hide it
        # Otherwise keep it to show specific labels like "Important" or "CAV/VVHD"
        cleaned_cat = cat.strip().rstrip(':').upper()
        cleaned_title = title.strip().upper()
        
        is_generic = cleaned_cat in ["NOTE", "COMMENT", "INFO", "INTERACTION", "INTERACTIONS"]
        is_redundant = cleaned_title.startswith(cleaned_cat) or cleaned_cat.startswith(cleaned_title.rstrip('S'))
        
        prefix = ""
        if not is_generic and not is_redundant:
            prefix = f"{cat}: "
            
        content_rows.append(ft.Text(f"{prefix}{row['recommendation']}", style=theme.body_style()))
        
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(icon, color=text_color) if icon else ft.Container(),
                ft.Text(title, style=theme.subheader_style(), color=text_color),
            ]),
            ft.Column(content_rows, spacing=5)
        ]),
        bgcolor=bg_color,
        border_radius=10,
        padding=15,
        margin=ft.Margin.symmetric(vertical=5),
    )

def build_renal_content(drug):
    rows = parse_drug_dosages(drug)
    renal_rows, replacement_rows, warnings, interactions, others = partition_rows(rows)
    
    controls = []
    
    # 1. Renal Impairment (Orange)
    controls.append(
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.WARNING_ROUNDED, color=theme.WARNING_TEXT_COLOR),
                    ft.Text("Dose in Renal Impairment", style=theme.subheader_style()),
                ]),
                build_dose_table(renal_rows, drug["dose_renal_impairment"])
            ]),
            bgcolor=theme.WARNING_COLOR,
            border_radius=10,
            padding=15,
            margin=ft.Margin.symmetric(vertical=10),
        )
    )

    # 1b. Replacement Therapy (Light Blue)
    if replacement_rows:
        controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.RECYCLING_ROUNDED, color=ft.Colors.BLUE_900),
                        ft.Text("Dose in Replacement Therapy", style=theme.subheader_style()),
                    ]),
                    build_dose_table(replacement_rows, drug["dose_replacement"])
                ]),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                padding=15,
                margin=ft.Margin.symmetric(vertical=10),
            )
        )
    
    # 2. Warnings (Red)
    if warnings:
        controls.append(build_info_block("Avertissements", warnings, ft.Colors.RED_50, ft.Colors.RED_900, ft.Icons.WARNING_AMBER_ROUNDED))
        
    # 3. Interactions (Blue/Purple)
    if interactions:
        controls.append(build_info_block("Interactions", interactions, ft.Colors.BLUE_50, ft.Colors.BLUE_900, ft.Icons.CHAT_BUBBLE_OUTLINE))
        
    # 4. Others (Grey/Yellow)
    if others:
         controls.append(build_info_block("Notes", others, ft.Colors.AMBER_50, ft.Colors.AMBER_900, ft.Icons.NOTE_ROUNDED))
         
    return controls

def show_details_dialog(page, drug_id, on_close=None):
    print(f"Opening details for {drug_id}")
    
    # Load initial data
    # We use a mutable container for the drug data to handle updates
    drug_data = {"drug": get_drug_details(drug_id)}
    
    if not drug_data["drug"]:
        print("Drug not found!")
        return
    
    # Log to history
    add_to_history(drug_id)
    
    # Main content container - responsive sizing
    dialog_width = min(600, page.width * 0.95) if page.width else 500  # 95% of screen width, max 600px
    dialog_height = min(700, page.height * 0.85) if page.height else 600  # 85% of screen height, max 700px
    content_container = ft.Container(width=dialog_width, height=dialog_height)
    
    # --- State Management ---
    
    def refresh_view():
        drug = drug_data["drug"]
        
        # View Mode Content
        view_content = ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Clinical Use", style=theme.subheader_style()),
                        ft.Text(drug["clinical_use"] or "Not specified", style=theme.body_style(), selectable=True),
                    ]),
                    padding=10,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Dose (Normal Renal Function)", style=theme.subheader_style()),
                        ft.Text(drug["dose_normal"] or "Not specified", style=theme.body_style(), selectable=True),
                    ]),
                    padding=10,
                ),
                
                # Highlighted Renal Dose Section and Extra Info
                *build_renal_content(drug),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        content_container.content = view_content
        update_actions(is_editing=False)
        content_container.update()

    def enable_edit_mode(e):
        drug = drug_data["drug"]
        
        # Create input fields
        clinical_use_field = ft.TextField(
            label="Clinical Use", 
            value=drug["clinical_use"], 
            multiline=True,
            min_lines=2
        )
        normal_dose_field = ft.TextField(
            label="Dose (Normal)", 
            value=drug["dose_normal"], 
            multiline=True, 
            min_lines=2
        )
        renal_dose_field = ft.TextField(
            label="Dose (Renal Impairment)", 
            value=drug["dose_renal_impairment"], 
            multiline=True, 
            min_lines=5,
            text_size=14
        )
        
        def save_changes(e):
            updates = {
                "clinical_use": clinical_use_field.value,
                "dose_normal": normal_dose_field.value,
                "dose_renal_impairment": renal_dose_field.value
            }
            if update_drug(drug_id, updates):
                # Update local data
                drug_data["drug"].update(updates)
                page.snack_bar = ft.SnackBar(ft.Text("Modifications enregistrées !"), bgcolor="green")
                page.snack_bar.open = True
                page.update()
                refresh_view()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Erreur lors de la sauvegarde"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        # Edit Mode Content
        edit_content = ft.Column([
            ft.Text("Mode Correcteur", style=theme.header_style()),
            ft.Text("Modifiez les données brutes ci-dessous. Le tableau sera régénéré automatiquement.", size=12, italic=True),
            ft.Divider(),
            clinical_use_field,
            normal_dose_field,
            renal_dose_field,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

        content_container.content = edit_content
        
        # Update actions for Edit Mode
        save_btn = ft.ElevatedButton("Enregistrer", icon=ft.Icons.SAVE, bgcolor=theme.PRIMARY_COLOR, color="white")
        save_btn.on_click = save_changes
        cancel_btn = ft.TextButton("Annuler")
        cancel_btn.on_click = lambda e: refresh_view()
        
        dlg.actions = [save_btn, cancel_btn]
        page.update()

    # --- Actions ---
    
    # Favorite Icon
    is_fav = is_favorite(drug_id)
    fav_icon = ft.IconButton(
        icon=ft.Icons.STAR_ROUNDED if is_fav else ft.Icons.STAR_BORDER_ROUNDED,
        icon_color=ft.Colors.AMBER if is_fav else ft.Colors.GREY,
        tooltip="Favori"
    )

    def toggle_fav_action(e):
        new_state = toggle_favorite(drug_id)
        fav_icon.icon = ft.Icons.STAR_ROUNDED if new_state else ft.Icons.STAR_BORDER_ROUNDED
        fav_icon.icon_color = ft.Colors.AMBER if new_state else ft.Colors.GREY
        fav_icon.update()
        
    fav_icon.on_click = toggle_fav_action
    
    # Edit Icon
    edit_icon = ft.IconButton(
        icon=ft.Icons.EDIT_ROUNDED,
        tooltip="Corriger la fiche",
        icon_color=theme.PRIMARY_COLOR
    )
    edit_icon.on_click = enable_edit_mode

    def handle_close(e):
        dlg.open = False
        page.update()
        if on_close:
            on_close()

    close_button = ft.TextButton("Fermer")
    close_button.on_click = handle_close

    def update_actions(is_editing):
        if is_editing:
            # Done inside enable_edit_mode usually, but if needed here
            pass 
        else:
            dlg.actions = [
                ft.Row([fav_icon, edit_icon]), # Left actions
                close_button # Right action
            ]
            dlg.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            if page: page.update()

    # --- Dialog Initialization ---

    dlg = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.MEDICAL_SERVICES_ROUNDED, color=theme.PRIMARY_COLOR),
            ft.Text(re.sub(r'\s+\d+$', '', drug_data["drug"]["name"]), expand=True, size=20, weight=ft.FontWeight.BOLD),
        ]),
        content=content_container,
        actions=[], # Set by update_actions
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    dlg.on_dismiss = lambda e: on_close() if on_close else None
    
    page.overlay.append(dlg)
    dlg.open = True
    
    # Initial Render
    refresh_view()
    page.update()
