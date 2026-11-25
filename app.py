import os
from PIL import Image
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from nutrition import get_nutritional_info

st.set_page_config(
    page_title="CalorieLens — Nutri & Food AI",
    page_icon="🥗",
    layout="centered"
)

# Style CSS moderne inspiré des applications de suivi nutritionnel
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.2rem;
    }
    .main-header h1 {
        color: white !important;
        font-size: 1.8rem !important;
        margin: 0 0 0.3rem 0 !important;
    }
    .main-header p {
        margin: 0;
        opacity: 0.95;
        font-size: 0.95rem;
    }
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .kcal-big {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.1;
    }
    .macro-box {
        background-color: #f9fafb;
        border: 1px solid #f3f4f6;
        border-radius: 12px;
        padding: 0.75rem;
        text-align: center;
    }
    .macro-val {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
    }
    .macro-lbl {
        font-size: 0.8rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

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

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@st.cache_resource
def load_model():
    model = models.resnet50(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(CLASSES_FOOD101))

    if os.path.exists("model-food.pth") and os.path.getsize("model-food.pth") > 1000:
        try:
            device = torch.device("cpu")
            state_dict = torch.load("model-food.pth", map_location=device)
            model.load_state_dict(state_dict)
            model.eval()
            return model
        except Exception:
            return None
    return None

if "journal" not in st.session_state:
    st.session_state.journal = []

# Barre latérale : objectif journalier & journal des repas
with st.sidebar:
    st.header(" Objectif du jour")
    objectif_kcal = st.number_input("Objectif calorique (kcal)", min_value=1000, max_value=5000, value=2000, step=50)

    total_mange = sum(item["calories"] for item in st.session_state.journal)
    restant = objectif_kcal - total_mange
    progression = min(total_mange / max(objectif_kcal, 1), 1.0)

    st.progress(progression)
    st.write(f"**Consommé :** {total_mange} kcal")
    st.write(f"**Restant :** {restant} kcal" if restant >= 0 else f"**Dépassement :** {abs(restant)} kcal")

    st.divider()
    st.subheader(" Journal du jour")
    if not st.session_state.journal:
        st.caption("Aucun repas ajouté pour l'instant.")
    else:
        for idx, repas in enumerate(st.session_state.journal):
            st.write(f"• **{repas['nom']}** ({repas['grammes']}g) — {repas['calories']} kcal")
        if st.button("Vider le journal"):
            st.session_state.journal = []
            st.rerun()

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1> CalorieLens AI</h1>
    <p>Scan de plat, estimation calorique selon la portion et suivi nutritionnel quotidien</p>
</div>
""", unsafe_allow_html=True)

model = load_model()
if model is None:
    st.info("ℹ Mode démonstration actif (`model-food.pth` absent sur cet environnement : simulation sur *beignets* activée).")

uploaded_file = st.file_uploader(" Prends ou importe la photo de ton plat", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Aperçu du repas", use_column_width=True)

    grammes = st.slider(" Poids estimé de ta portion (en grammes)", min_value=30, max_value=800, value=150, step=10)

    if st.button("Analyser le repas", type="primary", use_container_width=True):
        with st.spinner("Analyse visuelle et calcul nutritionnel..."):
            if model is not None:
                input_tensor = transform(image).unsqueeze(0)
                with torch.no_grad():
                    outputs = model(input_tensor)
                    probs = torch.nn.functional.softmax(outputs[0], dim=0)
                    conf, pred_idx = torch.max(probs, 0)
                plat_cle = CLASSES_FOOD101[pred_idx.item()]
                confiance_pct = f"{conf.item() * 100:.1f}%"
            else:
                plat_cle = "beignets"
                confiance_pct = "96.4%"

            st.session_state.derniere_analyse = {
                "plat_cle": plat_cle,
                "confiance": confiance_pct,
                "grammes": grammes
            }

if "derniere_analyse" in st.session_state:
    analyse = st.session_state.derniere_analyse
    info = get_nutritional_info(analyse["plat_cle"], grams=grammes)

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f'<span class="badge">{info["categorie"]}</span>', unsafe_allow_html=True)
    st.markdown(f"##  {info['nom_fr']}")
    st.caption(f"Confiance IA : **{analyse['confiance']}** • Portion : **{info['grammes']} g** (portion type conseillée : ~{info['portion_type_g']} g)")
    st.write(info["description"])

    st.markdown(f'<div class="kcal-big">{info["calories"]} <span style="font-size:1rem;font-weight:500;color:#6b7280;">kcal</span></div>', unsafe_allow_html=True)
    st.caption(f"Soit ~{round(info['calories'] / max(objectif_kcal, 1) * 100)}% de ton objectif de {objectif_kcal} kcal")

    st.markdown("####  Macronutriments")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="macro-box"><div class="macro-val">{info["glucides"]} g</div><div class="macro-lbl">Glucides ({info["pct_glucides"]}% kcal)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="macro-box"><div class="macro-val">{info["proteines"]} g</div><div class="macro-lbl">Protéines ({info["pct_proteines"]}% kcal)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="macro-box"><div class="macro-val">{info["lipides"]} g</div><div class="macro-lbl">Lipides ({info["pct_lipides"]}% kcal)</div></div>', unsafe_allow_html=True)

    st.markdown("####  Détails complémentaires")
    d1, d2 = st.columns(2)
    d1.metric("Fibres", f"{info['fibres']} g")
    d2.metric("Sucres", f"{info['sucres']} g")

    st.markdown("####  Conseil nutritionnel")
    st.success(info["conseil"])

    if st.button("➕ Ajouter ce repas au journal du jour", use_container_width=True):
        st.session_state.journal.append({
            "nom": info["nom_fr"],
            "grammes": info["grammes"],
            "calories": info["calories"]
        })
        st.toast(f"{info['nom_fr']} ({info['grammes']}g) ajouté au journal !")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)