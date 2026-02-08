import flet as ft
import sys
import os

# Ajoute le dossier src au chemin de recherche de Python
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Importe la fonction main de ton application
from app import main

if __name__ == "__main__":
    ft.app(target=main)
