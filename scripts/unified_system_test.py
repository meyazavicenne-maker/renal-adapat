import sys
import os
import math
import flet as ft

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.formulas import (
    calculate_ckd_epi, calculate_mdrd, calculate_cockcroft_gault, calculate_schwartz,
    calculate_corrected_sodium, calculate_corrected_calcium, calculate_water_deficit,
    calculate_anion_gap, calculate_iron_deficit
)
from core.database import search_drugs
from app import main

def run_automated_tests():
    print("--- Demarrage des tests automatises (Module par Module) ---")
    
    # --- 1. TEST FORMULES DFG ---
    print("\n[DFG] Verification des calculs...")
    # CKD-EPI: Age 60, Cr 1.0, Male, Non-black -> ~94.1
    res = calculate_ckd_epi(60, 1.0, 'M', False)
    print(f"  CKD-EPI: {res:.2f} mL/min (Attendu: ~94)")
    
    # --- 2. TEST ELECTROLYTES ---
    print("\n[Electrolytes] Verification des calculs...")
    # Sodium Corrige: Na 130, Glucose 300 -> 133.2
    res = calculate_corrected_sodium(130, 300)
    print(f"  Sodium Corrige: {res:.1f} (Attendu: 133.2)")
    
    # Calcium Corrige: Ca 80 (mg/L), Alb 30 (g/L) -> 80 + 0.8*(40-30) = 88
    res = calculate_corrected_calcium(80, 30)
    print(f"  Calcium Corrige: {res:.1f} mg/L (Attendu: 88)")

    # --- 3. TEST DEFICIT EN FER (GANZONI) ---
    print("\n[Fer] Verification de la formule de Ganzoni...")
    # Poids 70, Hb 10, Cible 14, Adulte -> [70 * (14-10) * 2.4] + 500 = 672 + 500 = 1172mg
    res = calculate_iron_deficit(70, 10, 14, is_adult=True)
    print(f"  Deficit en Fer: {res:.0f} mg (Attendu: 1172)")

    # --- 4. TEST BASE DE DONNEES ---
    print("\n[Base de Donnees] Verification de la recherche...")
    drugs = search_drugs("Abacavir")
    if drugs:
        print(f"  Recherche 'Abacavir': OK ({len(drugs)} resultat(s))")
    else:
        print("  !!! ERREUR: Aucun resultat pour Abacavir")

    print("\nTests automatises termines avec succes.")

def mobile_launcher(page: ft.Page):
    # Dimensions iPhone 14
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = True 
    
    print("\nLancement de l'interface en mode MOBILE (390x844)")
    print("Verifiez la visibilite des menus et des resultats de calcul.")
    
    main(page)

if __name__ == "__main__":
    run_automated_tests()
    print("\n--- TEST VISUEL (MOBILE) ---")
    ft.app(target=mobile_launcher)
