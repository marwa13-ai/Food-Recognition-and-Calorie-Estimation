## Food Recognition and Calorie Estimation

Application web interactive développée avec **PyTorch** et **Streamlit** permettant d'identifier un plat à partir d'une photo (sur les **101 classes du dataset Food-101**), d'estimer ses apports nutritionnels sur une portion standard, de calculer un objectif calorique journalier personnalisé et d'offrir des conseils repas détaillés.

---

##  Ce qui a déjà été réalisé

* **Entraînement du modèle de vision par ordinateur**
  * Architecture **ResNet-50** fine-tunée sur **Food-101** (101 classes alimentaires).
  * Migration de l'entraînement du CPU local vers **Google Colab avec GPU T4**, atteignant **83,50 % de précision** sur le jeu de test après 5 époques.
  * Sauvegarde des poids entraînés dans `model-food.pth` (~95 Mo) et publication via **GitHub Releases** afin de garder le dépôt Git léger tout en permettant le téléchargement automatique du modèle lorsque nécessaire.

* **Logique nutritionnelle & calcul d'objectifs (`nutrition.py`)**
  * Calcul du besoin calorique journalier à partir du profil utilisateur (taille, poids, âge, sexe, niveau d'activité) et de l'objectif choisi (*Perdre du poids*, *Juste savoir* ou *Masse musculaire*).
  * Estimation des macronutriments (glucides, protéines, lipides et répartition en % des calories), fibres et sucres sur une **portion standard** (adaptée aux repas pris à l'extérieur ou au restaurant).
  * Conseils pratiques et structurés expliquant **quoi manger avec le plat** et **comment équilibrer le repas suivant**.

* **Interface « Calorie Tracker » & suivi (`app.py`)**
  * Barre latérale dédiée au profil, à l'objectif calorique quotidien, à la jauge de progression et au journal des repas de la session.
  * Cartes visuelles pour afficher le plat reconnu, l'indice de confiance, les macronutriments et l'ajout en un clic au journal du jour.
  * Gestion sécurisée du chargement de `model-food.pth` avec repli propre vers un mode démonstration si les poids ne sont pas chargés sur l'environnement.

---

##  Stack technique

* **Langage & Deep Learning :** Python, PyTorch, Torchvision (`ResNet-50`), Pillow
* **Interface web :** Streamlit
* **Entraînement & déploiement :** Google Colab (T4 GPU), Git / GitHub (Releases), Streamlit Community Cloud

---

##  Structure du projet

```text
projet-food-ia/
├── app.py           # Interface Streamlit, inférence ResNet-50 et suivi journalier
├── nutrition.py     # Base nutritionnelle, calcul des besoins caloriques et conseils
├── .gitignore       # Exclusion des fichiers volumineux (ex. model-food.pth) et caches
└── README.md        # Documentation du projet

```

---

##  Lancer l'application en local

1. **Cloner le dépôt et se placer dans le dossier du projet :**
```bash
git clone [https://github.com/marwa13-ai/Food-Recognition-and-Calorie-Estimation.git](https://github.com/marwa13-ai/Food-Recognition-and-Calorie-Estimation.git)
cd Food-Recognition-and-Calorie-Estimation

```


2. **Installer les dépendances :**
```bash
pip install streamlit torch torchvision pillow

```


3. **Placer le fichier `model-food.pth` à la racine du projet (s'il n'est pas déjà présent).**
4. **Démarrer l'application :**
```bash
streamlit run app.py

```
---

##  Prochaines améliorations envisagées

* Enrichir `NUTRITION_DB` dans `nutrition.py` avec davantage de plats du quotidien et de spécialités locales.
* Ajouter l'exportation ou la sauvegarde persistante du journal de repas.
* Poursuivre l'expérimentation sur l'entraînement et l'évaluation du modèle.

```

```
