NUTRITION_DB = {
    "beignets": {
        "nom_fr": "Beignets",
        "categorie": "Pâtisserie / Frit",
        "portion_g": 90,
        "calories_100g": 389,
        "proteines_100g": 5.4,
        "glucides_100g": 45.2,
        "lipides_100g": 20.8,
        "fibres_100g": 1.5,
        "sucres_100g": 14.0,
        "description": "Pâte levée frite dorée et moelleuse, souvent sucrée.",
        "quoi_manger": "Évite de les manger seuls le ventre vide (pic de sucre). Accompagne-les d'une boisson non sucrée (café, thé, eau) et, au repas suivant, privilégie des légumes verts + une bonne source de protéines (œufs, poulet, poisson, légumineuses) pour rééquilibrer."
    },
    "apple_pie": {
        "nom_fr": "Tarte aux pommes",
        "categorie": "Dessert / Pâtisserie",
        "portion_g": 140,
        "calories_100g": 237,
        "proteines_100g": 2.4,
        "glucides_100g": 33.9,
        "lipides_100g": 10.6,
        "fibres_100g": 1.6,
        "sucres_100g": 15.5,
        "description": "Part de tarte aux pommes dorée avec pâte et garniture aux fruits.",
        "quoi_manger": "Si tu la prends en dessert ou au goûter, garde une part normale sans boule de glace ni crème. Au repas suivant, mise sur une assiette riche en protéines maigres et fibres (salade composée, légumes cuits, viandes blanches ou poissons)."
    },
    "pizza": {
        "nom_fr": "Pizza",
        "categorie": "Plat principal",
        "portion_g": 220,
        "calories_100g": 266,
        "proteines_100g": 11.0,
        "glucides_100g": 33.0,
        "lipides_100g": 10.0,
        "fibres_100g": 2.3,
        "sucres_100g": 3.6,
        "description": "Portion de pizza (pâte, sauce tomate, fromage et garniture).",
        "quoi_manger": "Au restaurant, commande une salade verte ou des crudités en entrée pour apporter des fibres et calmer la faim plus vite. Choisis des garnitures riches en protéines (poulet, thon, champignons, légumes) plutôt que trop de charcuterie grasse."
    },
    "hamburger": {
        "nom_fr": "Hamburger",
        "categorie": "Plat complet",
        "portion_g": 240,
        "calories_100g": 295,
        "proteines_100g": 17.0,
        "glucides_100g": 24.0,
        "lipides_100g": 14.0,
        "fibres_100g": 1.8,
        "sucres_100g": 4.2,
        "description": "Burger complet avec pain, steak/protéine, fromage et garniture.",
        "quoi_manger": "Pour un repas équilibré au restaurant, accompagne le burger de légumes ou d'une petite salade plutôt que de grandes frites, et évite les sodas sucrés (préfère de l'eau ou une boisson zéro)."
    },
    "sushi": {
        "nom_fr": "Sushi",
        "categorie": "Poisson & Riz",
        "portion_g": 220,
        "calories_100g": 150,
        "proteines_100g": 5.8,
        "glucides_100g": 27.5,
        "lipides_100g": 1.6,
        "fibres_100g": 1.2,
        "sucres_100g": 4.5,
        "description": "Assortiment de sushis (riz assaisonné, poisson, nori).",
        "quoi_manger": "Complète avec une soupe miso, une salade de chou ou d'algues (wakame) et des edamame pour ajouter des fibres et des protéines. Dose la sauce soja pour limiter l'excès de sel."
    },
    "ramen": {
        "nom_fr": "Ramen",
        "categorie": "Soupe & Nouilles",
        "portion_g": 450,
        "calories_100g": 115,
        "proteines_100g": 5.2,
        "glucides_100g": 14.5,
        "lipides_100g": 4.1,
        "fibres_100g": 1.4,
        "sucres_100g": 1.2,
        "description": "Bol de nouilles en bouillon avec garnitures (œuf, viande, légumes).",
        "quoi_manger": "Mange d'abord les légumes, l'œuf et la viande/protéine, puis les nouilles, et laisse une partie du bouillon au fond du bol si tu veux limiter le sodium et les graisses."
    },
    "caesar_salad": {
        "nom_fr": "Salade César",
        "categorie": "Salade & Protéines",
        "portion_g": 260,
        "calories_100g": 180,
        "proteines_100g": 8.5,
        "glucides_100g": 7.0,
        "lipides_100g": 13.0,
        "fibres_100g": 2.4,
        "sucres_100g": 1.8,
        "description": "Salade romaine, croûtons, parmesan et sauce César.",
        "quoi_manger": "Ajoute du poulet grillé, du saumon ou des œufs durs si tu veux plus de protéines et de satiété, et demande la sauce à part pour ajuster la quantité."
    },
    "waffles": {
        "nom_fr": "Gaufres",
        "categorie": "Petit-déjeuner / Dessert",
        "portion_g": 120,
        "calories_100g": 291,
        "proteines_100g": 7.9,
        "glucides_100g": 33.0,
        "lipides_100g": 14.1,
        "fibres_100g": 1.7,
        "sucres_100g": 8.5,
        "description": "Gaufre dorée cuite au gaufrier.",
        "quoi_manger": "Associe-la à des fruits frais (fraises, banane, myrtilles) ou un yaourt grec / fromage blanc pour apporter des protéines et limiter l'excès de sucre."
    }
}


def calculer_besoin_calorique(poids_kg: float, taille_cm: float, age: int, sexe: str, activite: str, objectif: str) -> int:
    # Formule de Mifflin-St Jeor
    if sexe == "Femme":
        bmr = 10 * poids_kg + 6.25 * taille_cm - 5 * age - 161
    else:
        bmr = 10 * poids_kg + 6.25 * taille_cm - 5 * age + 5

    facteurs_activite = {
        "Sédentaire (peu ou pas d'exercice)": 1.2,
        "Légèrement actif (1–3j/semaine)": 1.375,
        "Modérément actif (3–5j/semaine)": 1.55,
        "Très actif (6–7j/semaine)": 1.725,
    }
    tdee = bmr * facteurs_activite.get(activite, 1.375)

    if objectif == "Perdre du poids":
        cible = tdee - 400
    elif objectif == "Masse musculaire":
        cible = tdee + 300
    else:  # Juste savoir / Maintien
        cible = tdee

    return max(1200, int(round(cible / 10.0) * 10))


def get_nutritional_info(dish_key: str) -> dict:
    key = dish_key.lower().strip().replace(" ", "_")
    base = NUTRITION_DB.get(key)

    if base is None:
        nom_propre = key.replace("_", " ").title()
        base = {
            "nom_fr": nom_propre,
            "categorie": "Plat Food-101",
            "portion_g": 180,
            "calories_100g": 220,
            "proteines_100g": 9.0,
            "glucides_100g": 24.0,
            "lipides_100g": 9.5,
            "fibres_100g": 2.0,
            "sucres_100g": 4.0,
            "description": f"Plat identifié comme {nom_propre}. Estimation calculée sur une portion standard.",
            "quoi_manger": "Pour équilibrer ce plat : accompagne-le d'une portion de légumes riches en fibres, assure-toi d'avoir une source de protéines (viande, poisson, œufs, légumineuses) et garde une hydratation régulière."
        }

    grammes = base["portion_g"]
    factor = grammes / 100.0

    calories = round(base["calories_100g"] * factor)
    proteines = round(base["proteines_100g"] * factor, 1)
    glucides = round(base["glucides_100g"] * factor, 1)
    lipides = round(base["lipides_100g"] * factor, 1)
    fibres = round(base["fibres_100g"] * factor, 1)
    sucres = round(base["sucres_100g"] * factor, 1)

    kcal_p = proteines * 4.0
    kcal_g = glucides * 4.0
    kcal_l = lipides * 9.0
    total_macro_kcal = max(kcal_p + kcal_g + kcal_l, 1.0)

    return {
        "nom_fr": base["nom_fr"],
        "categorie": base["categorie"],
        "portion_g": grammes,
        "description": base["description"],
        "quoi_manger": base["quoi_manger"],
        "calories": calories,
        "proteines": proteines,
        "glucides": glucides,
        "lipides": lipides,
        "fibres": fibres,
        "sucres": sucres,
        "pct_proteines": round((kcal_p / total_macro_kcal) * 100),
        "pct_glucides": round((kcal_g / total_macro_kcal) * 100),
        "pct_lipides": round((kcal_l / total_macro_kcal) * 100),
    }