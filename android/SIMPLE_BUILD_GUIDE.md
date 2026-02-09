# Guide Simple : Build APK via GitHub Actions

## ✅ Pourquoi cette méthode ?

- **Pas besoin d'Android Studio**
- **Pas besoin de Java**
- **Pas de configuration locale**
- Build dans le cloud (gratuit)

---

## 📝 Étapes (5 minutes)

### 1. Push le code sur GitHub

```powershell
cd "C:\Users\Ham6\Desktop\Apps\RENAL ADAPAT"

# Ajoute tous les fichiers Android
git add android/
git add .github/workflows/build-android.yml

# Commit
git commit -m "Add Android native app"

# Push
git push
```

### 2. Déclenche le build

1. Va sur GitHub : https://github.com/TON_USERNAME/RENAL-ADAPAT
2. Clique sur **Actions**
3. Clique sur **Build Android APK** (à gauche)
4. Clique sur **Run workflow** (bouton vert à droite)
5. Clique sur **Run workflow** (confirmer)

### 3. Attends le build (~5 min)

- Tu verras la progression en temps réel
- Quand c'est vert ✅, c'est terminé

### 4. Télécharge l'APK

1. Clique sur le workflow terminé
2. En bas, section **Artifacts**
3. Clique sur **app-debug** pour télécharger
4. Dézippe le fichier → tu as ton APK !

---

## 📱 Installer l'APK

1. Copie `app-debug.apk` sur ton téléphone
2. Ouvre-le depuis l'app Fichiers
3. Installe (autorise les sources inconnues si demandé)

---

**C'est tout ! Pas besoin d'Android Studio.** 🎉
