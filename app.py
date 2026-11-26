import os
import urllib.request
from PIL import Image
import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from nutrition import calculer_besoin_calorique, get_nutritional_info

# Remplace cette URL par le lien direct exact vers model-food.pth dans ta GitHub Release
MODEL_URL = "https://github.com/marwa13-ai/Food-Recognition-and-Calorie-Estimation/releases/download/v1.0-model/model-food.pth"
MODEL_PATH = "model-food.pth"

st.set_page_config(
    page_title="CalorieLens — Nutri & Food AI",
    page_icon="🥗",
    layout="wide"
)

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
        margin-top: 1rem;
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
    .advice-step {
        color: #1f2937;
        font-size: 0.96rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
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


def ensure_model_downloaded():
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 1_000_000:
        return True, "OK"
    if not MODEL_URL or "TON_USER" in MODEL_URL or "TON_REPO" in MODEL_URL:
        return False, "MODEL_URL non configurée"
    try:
        req = urllib.request.Request(MODEL_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as resp, open(MODEL_PATH, "wb") as out:
            out.write(resp.read())
        size = os.path.getsize(MODEL_PATH) if os.path.exists(MODEL_PATH) else 0
        if size <= 1_000_000:
            if os.path.exists(MODEL_PATH):
                os.remove(MODEL_PATH)
            return False, f"Fichier incomplet ({size} octets) — vérifie MODEL_URL"
        return True, "OK"
    except Exception as e:
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return False, f"Échec téléchargement : {e}"


@st.cache_resource
def load_model():
    ok, msg = ensure_model_downloaded()
    if not ok:
        return None, msg

    model = models.resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(CLASSES_FOOD101))

    try:
        state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
        model.load_state_dict(state_dict)
        model.eval()
        return model, "OK"
    except Exception as e:
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return None, f"Échec torch.load : {e}"


if "journal" not in st.session_state:
    st.session_state.journal = []

# Barre latérale gauche : Profil, Objectif & Journal
with st.sidebar:
    st.header("👤 Ton profil & objectif")
    taille_cm = st.number_input("Taille (cm)", min_value=120, max_value=230, value=168, step=1)
    poids_kg = st.number_input("Poids (kg)", min_value=35.0, max_value=220.0, value=65.0, step=0.5)
    age = st.number_input("Âge", min_value=14, max_value=100, value=22, step=1)
    sexe = st.selectbox("Sexe biologique", ["Femme", "Homme"])
    activite = st.selectbox(
        "Niveau d'activité",
        [
            "Sédentaire (peu ou pas d'exercice)",
            "Légèrement actif (1–3j/semaine)",
            "Modérément actif (3–5j/semaine)",
            "Très actif (6–7j/semaine)",
        ],
        index=1
    )
    objectif = st.radio(
        "Ton but",
        ["Perdre du poids", "Juste savoir", "Masse musculaire"],
        index=1
    )

    objectif_kcal = calculer_besoin_calorique(poids_kg, taille_cm, age, sexe, activite, objectif)
    st.metric(" Calories conseillées / jour", f"{objectif_kcal} kcal")

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
        for repas in st.session_state.journal:
            st.write(f"• **{repas['nom']}** — {repas['calories']} kcal")
        if st.button("Vider le journal"):
            st.session_state.journal = []
            st.rerun()

# Zone principale droite
st.markdown("""
<div class="main-header">
    <h1>🥗 CalorieLens AI</h1>
    <p>Reconnaissance de plat, calories sur portion standard et conseils repas</p>
</div>
""", unsafe_allow_html=True)

model, model_status = load_model()
if model is None:
    st.caption(f"Mode démonstration actif ({model_status}).")

uploaded_file = st.file_uploader(" Prends ou importe la photo de ton plat", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Photo du plat", use_container_width=True)

    if st.button("Analyser le repas", type="primary", use_container_width=True):
        with st.spinner("Analyse de l'image en cours..."):
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
            }

if "derniere_analyse" in st.session_state:
    analyse = st.session_state.derniere_analyse
    info = get_nutritional_info(analyse["plat_cle"])

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f'<span class="badge">{info["categorie"]}</span>', unsafe_allow_html=True)
    st.markdown(f"##  {info['nom_fr']}")
    st.caption(f"Confiance IA : **{analyse['confiance']}** • Basé sur une **portion standard estimée (~{info['portion_g']} g)**")
    st.write(info["description"])

    st.markdown(
        f'<div class="kcal-big">{info["calories"]} <span style="font-size:1rem;font-weight:500;color:#6b7280;">kcal (portion standard)</span></div>',
        unsafe_allow_html=True
    )
    st.caption(f"Soit ~{round(info['calories'] / max(objectif_kcal, 1) * 100)}% de ton objectif de {objectif_kcal} kcal ({objectif})")

    st.markdown("####  Macronutriments")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="macro-box"><div class="macro-val">{info["glucides"]} g</div><div class="macro-lbl">Glucides ({info["pct_glucides"]}% kcal)</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f'<div class="macro-box"><div class="macro-val">{info["proteines"]} g</div><div class="macro-lbl">Protéines ({info["pct_proteines"]}% kcal)</div></div>',
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f'<div class="macro-box"><div class="macro-val">{info["lipides"]} g</div><div class="macro-lbl">Lipides ({info["pct_lipides"]}% kcal)</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("####  Détails complémentaires")
    d1, d2 = st.columns(2)
    d1.metric("Fibres", f"{info['fibres']} g")
    d2.metric("Sucres", f"{info['sucres']} g")

    st.markdown("####  Quoi manger avec / ensuite ?")
    st.markdown(
        f'<p class="advice-step"><strong>1. Avec ce plat :</strong> {info["avec"]}</p>'
        f'<p class="advice-step"><strong>2. Au repas suivant (ensuite) :</strong> {info["ensuite"]}</p>',
        unsafe_allow_html=True
    )

    if st.button(" Ajouter cette portion au journal du jour", use_container_width=True):
        st.session_state.journal.append({
            "nom": info["nom_fr"],
            "calories": info["calories"]
        })
        st.toast(f"{info['nom_fr']} ajouté au journal !")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)