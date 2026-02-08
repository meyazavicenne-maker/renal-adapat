import flet as ft
from data import search_drugs, get_drug_details
import theme
from parser import parse_drug_dosages
import re

def main(page: ft.Page):
    page.title = "Renal Drug Handbook"
    page.theme = theme.get_theme()
    page.bgcolor = theme.BACKGROUND_COLOR
    page.padding = 20
    page.window_width = 450
    page.window_height = 850
    
    # --- State ---
    current_search = ""

    # --- UI Components ---
    
    def get_renal_dose_display(drug):
        rows = parse_drug_dosages(drug)
        if not rows:
             return ft.Text(drug["dose_renal_impairment"] or "Not specified", style=theme.body_style())
             
        # Create DataTable
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Clairance/Mode", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Dosage", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row["category"], weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(row["recommendation"])),
                    ]
                ) for row in rows
            ],
            width=float("inf"),
            column_spacing=10,
        )

    def get_details_content(drug):
        """Creates the content for the details dialog"""
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Clinical Use", style=theme.subheader_style()),
                        ft.Text(drug["clinical_use"] or "Not specified", style=theme.body_style()),
                    ]),
                    padding=10,
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Dose (Normal Renal Function)", style=theme.subheader_style()),
                        ft.Text(drug["dose_normal"] or "Not specified", style=theme.body_style()),
                    ]),
                    padding=10,
                ),
                
                # Highlighted Renal Dose Section
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.WARNING_ROUNDED, color=theme.WARNING_TEXT_COLOR),
                            ft.Text("Dose in Renal Impairment", style=theme.subheader_style()),
                        ]),
                        # Table logic
                        get_renal_dose_display(drug)
                    ]),
                    bgcolor=theme.WARNING_COLOR,
                    border_radius=10,
                    padding=15,
                    # Fix: Use Margin.symmetric
                    margin=ft.Margin.symmetric(vertical=10),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def show_details(drug_id):
        print(f"Opening details for {drug_id}")
        drug = get_drug_details(drug_id)
        if not drug:
            print("Drug not found!")
            return
            
        dlg = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.MEDICAL_SERVICES, color=theme.PRIMARY_COLOR),
                ft.Text(re.sub(r'\s+\d+$', '', drug["name"]), expand=True, size=18, weight=ft.FontWeight.BOLD),
            ]),
            content=ft.Container(
                content=get_details_content(drug),
                width=500, # Increased width
                height=700, # Increased height to avoid truncation
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(dlg))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Robust Dialog Opening: Add to overlay
        print("Adding dialog to overlay...")
        page.overlay.append(dlg)
        dlg.open = True
        page.update()
        print("Dialog updated.")

    def close_dialog(dlg):
        print("Close button clicked.")
        dlg.open = False
        page.update()
        if dlg in page.overlay:
             page.overlay.remove(dlg)
        page.update()

    results_list = ft.ListView(expand=True, spacing=10)

    def search_action(query):
        nonlocal current_search
        current_search = query
        results_list.controls.clear()
        
        if len(query) > 1:
            drugs = search_drugs(query)
            if not drugs:
                 results_list.controls.append(
                    ft.Container(
                        content=ft.Text("No results found", italic=True, color=ft.Colors.GREY_500),
                        alignment=ft.Alignment(0, 0),
                        padding=20
                    )
                )
            else:
                for drug in drugs:
                    # Card-based result item
                    results_list.controls.append(
                        ft.Card(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.MEDICATION, color=theme.PRIMARY_COLOR),
                                title=ft.Text(re.sub(r'\s+\d+$', '', drug["name"]), weight=ft.FontWeight.W_500),
                                # Page number removed as requested
                                # subtitle=ft.Text(f"Page {drug.get('page_number', '?')}", size=12, italic=True),
                                on_click=lambda e, d=drug["id"]: show_details(d),
                            ),
                            elevation=2,
                        )
                    )
        page.update()

    search_field = ft.TextField(
        hint_text="Search drug name (e.g. Amoxicillin)...",
        prefix_icon=ft.Icons.SEARCH,
        suffix=ft.IconButton(ft.Icons.CLEAR, on_click=lambda e: clear_search()),
        border_radius=20,
        filled=True,
        expand=True,
        on_change=lambda e: search_action(e.control.value)
    )
    
    def clear_search():
        search_field.value = ""
        results_list.controls.clear()
        page.update()

    # --- Header ---
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LOCAL_HOSPITAL, size=40, color=ft.Colors.WHITE),
                ft.Text("Renal Drug Handbook", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Rapid Dosage Adjustment Guide", color=ft.Colors.WHITE70, italic=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=theme.PRIMARY_COLOR,
        padding=20,
        # Fix: Use BorderRadius directly (top_left, top_right, bottom_left, bottom_right)
        border_radius=ft.BorderRadius(0, 0, 20, 20),
    )

    # --- Main Layout ---
    page.add(
        header,
        # Fix: Use Padding directly (left, top, right, bottom)
        ft.Container(search_field, padding=ft.Padding(0, 20, 0, 10)),
        results_list,
    )

if __name__ == "__main__":
    ft.app(main)
