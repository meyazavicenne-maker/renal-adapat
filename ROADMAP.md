# ROADMAP: Projet Renal Drug Handbook

Bonjour ! Voici la stratégie pour transformer votre livre "énorme" en une application fluide et rapide.

## 1. Le Défi de la Donnée ("Le Livre Énorme")
C'est la partie la plus critique. Pour éviter de copier-coller 1000 pages à la main, nous avons besoin d'automatisaton.
*   **Si vous avez le PDF** : Je peux créer un "robot" (script Python) qui lit le PDF, détecte le nom des médicaments et extrait les tableaux d'adaptation rénale pour les mettre dans une base de données.
*   **Si c'est papier** : Il faudra scanner ou utiliser une app OCR, mais c'est plus long.

## 2. La Solution Technique (Mobile + Windows)
Pour avoir une application sur Windows **ET** Mobile sans tout coder deux fois, je vous propose d'utiliser **Flet** (Python).
*   **Avantages** : C'est du Python (que votre environnement semble privilégier), c'est moderne (Material Design 3), et ça s'exporte sur Android/iOS et Windows.

## 3. Architecture de l'App
1.  **Moteur de Recherche** : Une barre de recherche centrale. Vous tapez "Amox...", ça filtre instantanément.
2.  **Base de Données Locale** : Tout est stocké dans l'app (`SQLite`). Pas besoin d'internet. Rapide comme l'éclair.
3.  **Fiche Pratique** : Une vue claire avec :
    *   Posologie standard.
    *   Adaptation GFR > 50 / 10-50 / < 10.
    *   Dialyse / CRRT.

## Prochaine Étape Immédiate
Avez-vous le fichier numérique du livre (PDF) ?
- **OUI** : Copiez-le dans ce dossier (`RENAL ADAPAT`). Je l'analyserai pour extraire les données.
- **NON** : On devra construire une structure vide et vous devrez peut-être remplir au fur et à mesure, ou trouver une source numérique.

En attendant, je vais préparer le "squelette" de l'application pour que vous puissiez voir à quoi ça ressemble.
