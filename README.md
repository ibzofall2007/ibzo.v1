# ⚡ ibzo

**ibzo** est une application ultra-légère et rapide pour partager instantanément des fichiers en réseau local (LAN). Lancez l'application, scannez le QR code généré directement dans votre terminal avec votre smartphone, et transférez des fichiers de plusieurs Giga-octets sans aucune compression !

## ✨ Fonctionnalités
- 🚀 **Vitesse maximale :** Pas de serveurs tiers, les transferts se font à la vitesse maximale de votre réseau Wi-Fi/Filaire local.
- 📦 **Streaming Chunks (1 Mo) :** Écrit et lit par morceaux de 1 Mo pour ne jamais saturer la mémoire RAM, idéal pour les fichiers immenses (films, archives, ISO).
- 📱 **Génération de QR Code :** Affichage d'un QR code directement dans le terminal pour s'y connecter instantanément depuis un mobile.
- 🎨 **Interface moderne :** Design épuré, sombre, responsive, avec barre de progression de transfert en temps réel.

## 🛠️ Installation et Lancement

### 1. Prérequis
Assurez-vous d'avoir installé **Python 3.8+**.

### 2. Cloner le projet
```bash
git clone https://github.com
cd ibzo
```

### 3. Installer les dépendances
```bash
pip install flask segno
```

### 4. Lancer l'application
```bash
python app.py
```
Ouvrez ensuite l'URL indiquée ou scannez le QR code.

## 🗺️ Feuille de route / Ce qu'il manque (Roadmap Open Source)
Avis aux contributeurs ! Voici les fonctionnalités prévues ou manquantes que vous pouvez ajouter via des *Pull Requests* :
- [ ] **Sécurité :** Ajouter une option de mot de passe ou un code PIN généré pour sécuriser les transferts.
- [ ] **Gestion Multi-fichiers :** Permettre l'envoi simultané (par lots) de plusieurs fichiers via l'interface graphique (actuellement traité un par un dans le script JS).
- [ ] **Bouton Supprimer :** Pouvoir supprimer un fichier depuis l'interface web.
- [ ] **Clean Code :** Séparer le code HTML/CSS dans un dossier `templates/` dédié au lieu d'une variable string dans `app.py`.

## 📄 Licence
Ce projet est sous licence **MIT** – libre d'utilisation, de modification et de distribution.
