 # Food Recognition and Calorie Estimation via Deep Vision

Application web intelligente basée sur la vision par ordinateur et le Deep Learning permettant d'identifier des plats à partir d'une image, d'analyser leurs composants nutritionnels (macronutriments) et d'estimer les calories pour le suivi diététique.
```
```
## Fonctionnalités Principales
* **Classification d'images par Deep Learning :** Reconnaissance automatique de plats grâce à un modèle de type CNN entraîné sur le dataset *Food-101*.
* **Estimation Nutritionnelle :** Affichage détaillé des calories, protéines, glucides et lipides (pour 100g).
* **Équilibre des Repas :** Suggestions et conseils diététiques dynamiques pour compenser ou équilibrer les apports du plat détecté.
* **Interface Web Interactive :** Application fluide et ergonomique développée avec **Streamlit**.
```
```

##  Stack Technique
* **Langage :** Python
* **Deep Learning :** PyTorch, Torchvision (ResNet / Transfer Learning)
* **Interface Web :** Streamlit
* **Traitement d'images :** Pillow, OpenCV
```

```
## Structure du Projet
```text
projet-food-ia/
├── app.py                # Interface web de l'application (Streamlit)
├── train.py              # Script d'entraînement du modèle de Deep Learning
├── nutrition.py          # Base de données des calories et macronutriments
├── model-food.pth        # Poids du modèle entraîné
├── food-101.zip          # Fichier archive du dataset (ignoré ou stocké localement)
├── .gitignore            # Configuration des fichiers ignorés par Git
└── README.md             # Documentation du projet

```

---

##  Installation et Lancement en Local

1. **Cloner le dépôt :**
```bash
git clone [https://github.com/marwa13-ai/Food-Recognition-and-Calorie-Estimation.git](https://github.com/marwa13-ai/Food-Recognition-and-Calorie-Estimation.git)
cd Food-Recognition-and-Calorie-Estimation

```


2. **Installer les dépendances requises :**
```bash
pip install torch torchvision streamlit pillow opencv-python scikit-learn

```


3. **Lancer l'application web Streamlit :**
```bash
streamlit run app.py

```



---

##  Entraînement du Modèle

Pour entraîner le modèle de Deep Learning à partir du dataset Food-101 :

```bash
python train.py

```

```

```
