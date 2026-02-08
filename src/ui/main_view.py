import flet as ft
from ui.components.drug_card import DrugCard
from ui.components.search_bar import SearchBar
from ui.components.calculator_view import CalculatorView
from ui.components.simple_calc_view import SimpleCalcView
from ui.dialogs.drug_details import show_details_dialog
from core.database import search_drugs, get_favorites, get_history, is_favorite
from ui import theme

from ui.views.home_view import HomeView

def create_main_view(page):
    # --- Navigation Logic ---
    def navigate_to(nav_tag):
        if nav_tag == "search":
            page.navigation_bar.selected_index = 1
            update_tab_content(1)
        elif nav_tag == "calc_gfr":
            page.navigation_bar.selected_index = 4
            update_tab_content(4)
            calculator_tab_content.set_category("gfr")
        elif nav_tag in ["calc_electro", "calc_hemato"]:
            page.navigation_bar.selected_index = 4
            update_tab_content(4)
            calculator_tab_content.set_category("electrolytes")
        elif nav_tag == "simple_calc":
            page.navigation_bar.selected_index = 5
            update_tab_content(5)
        page.update()

    # --- Views ---
    home_tab_content = HomeView(on_navigate=navigate_to)

    # --- Search Tab Content ---
    results_list = ft.ListView(expand=True, spacing=10)
    
    def on_drug_click(drug_id):
        def on_close_callback():
            refresh_favorites()
            refresh_history()
        show_details_dialog(page, drug_id, on_close=on_close_callback)

    def update_results(query):
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
                    results_list.controls.append(
                        DrugCard(drug, on_drug_click)
                    )
        page.update()

    def clear_search(e):
        search_field.value = ""
        results_list.controls.clear()
        page.update()

    search_field = SearchBar(
        on_change=lambda e: update_results(e.control.value),
        on_clear=clear_search
    )

    search_tab_content = ft.Column([
        ft.Container(search_field, padding=ft.Padding(0, 20, 0, 10)),
        results_list,
    ], expand=True)

    # --- Favorites Tab Content ---
    favorites_list = ft.ListView(expand=True, spacing=10)

    def refresh_favorites():
        vals = get_favorites()
        favorites_list.controls.clear()
        if not vals:
            favorites_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.FAVORITE_BORDER, size=50, color=ft.Colors.GREY_400),
                        ft.Text("No favorites yet", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0),
                    padding=20,
                    opacity=0.5
                )
            )
        else:
            for drug in vals:
                favorites_list.controls.append(
                    DrugCard(drug, on_drug_click, is_favorite=True)
                )
        if page: page.update()

    favorites_tab_content = ft.Column([
        ft.Container(height=20), # Spacer
        favorites_list
    ], expand=True)

    # --- History Tab Content ---
    history_list = ft.ListView(expand=True, spacing=10)

    def refresh_history():
        vals = get_history()
        history_list.controls.clear()
        if not vals:
            history_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.HISTORY, size=50, color=ft.Colors.GREY_400),
                        ft.Text("Pas d'historique récent", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0),
                    padding=20,
                    opacity=0.5
                )
            )
        else:
            for drug in vals:
                history_list.controls.append(
                    DrugCard(drug, on_drug_click, is_favorite=is_favorite(drug['id']))
                )
        if page: page.update()

    history_tab_content = ft.Column([
        ft.Container(height=20), # Spacer
        history_list
    ], expand=True)


    # --- Calculator Tab Content ---
    calculator_tab_content = CalculatorView()
    simple_calc_content = SimpleCalcView()

    # --- Layout & Tab Handling ---
    
    # Area where tab content will be displayed
    content_area = ft.Container(expand=True)
    content_area.content = home_tab_content # Default is Home

    def update_tab_content(index):
        if index == 0:
            content_area.content = home_tab_content
        elif index == 1:
            content_area.content = search_tab_content
        elif index == 2:
            refresh_favorites()
            content_area.content = favorites_tab_content
        elif index == 3:
            refresh_history()
            content_area.content = history_tab_content
        elif index == 4:
            content_area.content = calculator_tab_content
        elif index == 5:
            content_area.content = simple_calc_content
        content_area.update()
        page.update()

    # Use NavigationBar (Bottom)
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Accueil"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Recherche"),
            ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Favoris"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Historique"),
            ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label="Médical"),
            ft.NavigationBarDestination(icon=ft.Icons.CALCULATE, label="Calcul"),
        ],
        selected_index=0
    )
    page.navigation_bar.on_change = lambda e: update_tab_content(e.control.selected_index)
    page.update()

    return content_area
