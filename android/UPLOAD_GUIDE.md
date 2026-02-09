# Guide Ultra Simple : Build APK sans Git ni Android Studio

## 🎯 Méthode : Upload direct sur GitHub

### Étape 1 : Créer un fichier ZIP

1. Ouvre l'explorateur Windows
2. Va dans `C:\Users\Ham6\Desktop\Apps\RENAL ADAPAT`
3. Sélectionne le dossier **`android`**
4. Clic droit → **Envoyer vers → Dossier compressé**
5. Renomme le ZIP en `android.zip`

### Étape 2 : Upload sur GitHub

1. Va sur ton repo GitHub : https://github.com/TON_USERNAME/RENAL-ADAPAT
2. Clique sur **Add file** → **Upload files**
3. Glisse-dépose `android.zip` (ou clique pour sélectionner)
4. Attends l'upload
5. En bas, écris : "Add Android native app"
6. Clique sur **Commit changes**

### Étape 3 : Extraire le ZIP sur GitHub

1. Sur GitHub, clique sur `android.zip`
2. Clique sur les **3 points** → **Download**
3. Dézippe localement
4. Re-upload le contenu du dossier `android/` directement (pas le ZIP)

**OU MIEUX : Utilise GitHub Desktop**

---

## 🚀 Alternative : GitHub Desktop (Recommandé)

### Installation

1. Télécharge : https://desktop.github.com/
2. Installe GitHub Desktop
3. Connecte-toi avec ton compte GitHub

### Utilisation

1. **File → Add Local Repository**
2. Sélectionne `C:\Users\Ham6\Desktop\Apps\RENAL ADAPAT`
3. Coche tous les fichiers dans `android/`
4. En bas à gauche, écris : "Add Android native app"
5. Clique sur **Commit to main**
6. Clique sur **Push origin** (en haut)

---

## ⚡ Après le push

1. Va sur GitHub → **Actions**
2. Le workflow **Build Android APK** démarre automatiquement
3. Attends 5 minutes
4. Télécharge l'APK dans **Artifacts**

---

**Quelle méthode préfères-tu ?**
- GitHub Desktop (plus simple)
- Upload manuel sur GitHub
