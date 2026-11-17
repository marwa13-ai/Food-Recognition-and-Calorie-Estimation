import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from nutrition import get_nutritional_info
import os

# Configuration de la page
st.set_page_config(
    page_title="Food Recognition & Calorie Estimation",
    page_icon="🍔",
    layout="centered"
)

st.title("🍔 Food Recognition & Calorie Estimation")
st.markdown("Application intelligente de vision par ordinateur pour le **suivi diététique** et le **fitness**.")

# 1. Chargement du modèle entraîné avec PyTorch
@st.cache_resource
def load_model():
    # Crée l'architecture ResNet-50
    model = models.resnet50(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 101) # 101 classes pour Food-101
    
    # Charge les poids que tu viens d'entraîner
    if os.path.exists("model-food.pth"):
        device = torch.device("cpu") # Utilise le CPU par défaut pour l'interface web
        model.load_state_dict(torch.load("model-food.pth", map_location=device))
        model.eval()
        return model
    else:
        return None

model = load_model()

# Liste des 101 classes du dataset Food-101 (principales classes ou classes de base)
# Pour faire simple, voici quelques classes principales du dataset Food-101
CLASSES_FOOD101 = [
    "apple_pie", "baby_back_ribs", "baklava", "beef_carpaccio", "beef_tartare", 
    "beet_salad", "beignets", "bibimbap", "bread_pudding", "breakfast_burrito", 
    "bruschetta", "caesar_salad", "cannoli", "caprese_salad", "carrot_cake", 
    "ceviche", "cheesecake", "cheese_plate", "chicken_curry", "chicken_quesadilla", 
    "chicken_wings", "chocolate_cake", "chocolate_mousse", "churros", "clam_chowder", 
    "club_sandwich", "crab_cakes", "creme_brulee", "croque_madame", "cup_cakes", 
    "deviled_eggs", "donuts", "dumplings", "edamame", "eggs_benedict", 
    "escargots", "falafel", "filet_mignon", "fish_and_chips", "foie_gras", 
    "french_fries", "french_onion_soup", "french_toast", "fried_calamari", "fried_rice", 
    "garlic_bread", "gnocchi", "greek_salad", "grilled_cheese_sandwich", "grilled_salmon", 
    "guacamole", "gyoza", "hamburger", "hot_dog", "huevos_rancheros", 
    "hummus", "ice_cream", "lasagna", "lobster_bisque", "lobster_roll_sandwich", 
    "macaroni_and_cheese", "macarons", "miso_soup", "mussels", "nachos", 
    "omelette", "onion_rings", "oysters", "pad_thai", "paella", 
    "pancakes", "panna_cotta", "peking_duck", "pho", "pizza", 
    "pork_chop", "poutine", "prime_rib", "pulled_pork_sandwich", "ramen", 
    "ravioli", "red_velvet_cake", "risotto", "samosa", "sashimi", 
    "scallops", "seaweed_salad", "shrimp_and_grits", "spaghetti_bolognese", "spaghetti_carbonara", 
    "spring_rolls", "steak", "strawberry_shortcake", "sushi", "tacos", 
    "takoyaki", "tiramisu", "tuna_tartare", "waffles"
]

# Transformations de l'image téléchargée
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 2. Zone de téléchargement de l'image sur le site
uploaded_file = st.file_uploader("Choisissez une image de plat (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Plat téléchargé', use_column_width=True)
    
    if st.button("Lancer l'analyse intelligente"):
        if model is None:
            st.error("⚠️ Le fichier du modèle 'model-food.pth' est introuvable. Assure-toi qu'il est bien à la racine du projet.")
        else:
            with st.spinner("Analyse du plat en cours par ton modèle PyTorch..."):
                # Prétraitement de l'image
                input_tensor = transform(image).unsqueeze(0)
                
                # Prédiction avec le modèle
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                    confidence, predicted_idx = torch.max(probabilities, 0)
                
                # Récupération du nom du plat prédit
                class_idx = predicted_idx.item()
                if class_idx < len(CLASSES_FOOD101):
                    plat_detecte = CLASSES_FOOD101[class_idx]
                else:
                    plat_detecte = "pizza" # Valeur de secours
                
                confiance_pct = f"{confidence.item() * 100:.1f}%"
                
                # Récupération des infos nutritionnelles
                info = get_nutritional_info(plat_detecte)
                
                # --- AFFICHAGE DES RÉSULTATS ---
                st.success("Analyse réussie !")
                
                st.markdown(f"### 🏷️ Résultat de la reconnaissance :")
                st.write(f"- **Aliment identifié :** `{plat_detecte.replace('_', ' ').capitalize()}`")
                st.write(f"- **Indice de confiance :** {confiance_pct}")
                
                # Affichage des macronutriments
                st.markdown("#### 📊 Composition nutritionnelle (pour 100g) :")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Calories", f"{info['calories']} kcal")
                col2.metric("Protéines", info['proteines'])
                col3.metric("Glucides", info['glucides'])
                col4.metric("Lipides", info['lipides'])
                
                # Conseil diététique
                st.markdown("#### 🥗 Conseil pour un repas équilibré :")
                st.info(info['conseil'])

st.markdown("---")
st.markdown("<p style='text-align: center;'>Projet IA - Reconnaissance d'Aliments & Estimation Calorique 🚀</p>", unsafe_allow_html=True)