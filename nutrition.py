NUTRITION_DB = {
    "beignets": {
        "nom_fr": "Beignets",
        "categorie": "Pâtisserie / Frit",
        "portion_type_g": 90,
        "calories_100g": 389,
        "proteines_100g": 5.4,
        "glucides_100g": 45.2,
        "lipides_100g": 20.8,
        "fibres_100g": 1.5,
        "sucres_100g": 14.0,
        "description": "Pâte levée frite dorée et moelleuse, généralement saupoudrée de sucre glace.",
        "conseil": "Riche en glucides simples et en lipides de friture. À consommer occasionnellement, idéalement accompagné d'un café/thé sans sucre ou d'une source de protéines/fibres au repas suivant."
    },
    "apple_pie": {
        "nom_fr": "Tarte aux pommes",
        "categorie": "Dessert / Pâtisserie",
        "portion_type_g": 140,
        "calories_100g": 237,
        "proteines_100g": 2.4,
        "glucides_100g": 33.9,
        "lipides_100g": 10.6,
        "fibres_100g": 1.6,
        "sucres_100g": 15.5,
        "description": "Pâte feuilletée ou brisée garnie de pommes fondantes, souvent relevée à la cannelle.",
        "conseil": "Apport énergétique modéré à élevé surtout issu de la pâte et des sucres. Privilégie une part raisonnable et évite d'ajouter de la glace ou de la crème."
    },
    "pizza": {
        "nom_fr": "Pizza",
        "categorie": "Plat principal",
        "portion_type_g": 180,
        "calories_100g": 266,
        "proteines_100g": 11.0,
        "glucides_100g": 33.0,
        "lipides_100g": 10.0,
        "fibres_100g": 2.3,
        "sucres_100g": 3.6,
        "description": "Pâte à pain garnie de sauce tomate, fromage et ingrédients variés.",
        "conseil": "Associe-la à une grande salade verte ou des légumes grillés pour augmenter les fibres et la satiété sans alourdir l'apport calorique."
    },
    "hamburger": {
        "nom_fr": "Hamburger",
        "categorie": "Fast-food / Plat complet",
        "portion_type_g": 220,
        "calories_100g": 295,
        "proteines_100g": 17.0,
        "glucides_100g": 24.0,
        "lipides_100g": 14.0,
        "fibres_100g": 1.8,
        "sucres_100g": 4.2,
        "description": "Pain burger, steak haché, fromage, crudités et sauce.",
        "conseil": "Bonne source de protéines, mais surveille la sauce et l'accompagnement : préfère des légumes ou une petite portion plutôt que des frites."
    },
    "sushi": {
        "nom_fr": "Sushi",
        "categorie": "Poisson & Riz",
        "portion_type_g": 200,
        "calories_100g": 150,
        "proteines_100g": 5.8,
        "glucides_100g": 27.5,
        "lipides_100g": 1.6,
        "fibres_100g": 1.2,
        "sucres_100g": 4.5,
        "description": "Riz vinaigré accompagné de poisson cru ou cuit, algue nori et légumes.",
        "conseil": "Léger en lipides mais riche en riz blanc : ajoute une soupe miso ou une salade de chou/algues et dose la sauce soja (riche en sodium)."
    },
    "ramen": {
        "nom_fr": "Ramen",
        "categorie": "Soupe & Nouilles",
        "portion_type_g": 450,
        "calories_100g": 115,
        "proteines_100g": 5.2,
        "glucides_100g": 14.5,
        "lipides_100g": 4.1,
        "fibres_100g": 1.4,
        "sucres_100g": 1.2,
        "description": "Nouilles de blé dans un bouillon savoureux avec œuf, viande ou légumes.",
        "conseil": "Le bouillon concentre beaucoup de sel et parfois de graisses : garde les protéines et les légumes, et laisse une partie du bouillon au fond du bol."
    },
    "caesar_salad": {
        "nom_fr": "Salade César",
        "categorie": "Salade / Entrée ou plat léger",
        "portion_type_g": 250,
        "calories_100g": 180,
        "proteines_100g": 8.5,
        "glucides_100g": 7.0,
        "lipides_100g": 13.0,
        "fibres_100g": 2.4,
        "sucres_100g": 1.8,
        "description": "Laitue romaine, croûtons, parmesan et sauce crémeuse (souvent avec poulet).",
        "conseil": "Très intéressant si tu ajoutes du poulet grillé pour les protéines, mais demande la sauce à part pour maîtriser les lipides."
    },
    "waffles": {
        "nom_fr": "Gaufres",
        "categorie": "Petit-déjeuner / Pâtisserie",
        "portion_type_g": 110,
        "calories_100g": 291,
        "proteines_100g": 7.9,
        "glucides_100g": 33.0,
        "lipides_100g": 14.1,
        "fibres_100g": 1.7,
        "sucres_100g": 8.5,
        "description": "Pâte cuite dans un gaufrier à alvéoles caractéristiques, croustillante dehors et moelleuse dedans.",
        "conseil": "Équilibre avec des fruits frais ou un yaourt grec nature plutôt que beaucoup de pâte à tartiner ou de sirop très sucré."
    }
}

def get_nutritional_info(dish_key: str, grams: float = 100.0) -> dict:
    key = dish_key.lower().strip().replace(" ", "_")
    base = NUTRITION_DB.get(key)

    if base is None:
        nom_propre = key.replace("_", " ").title()
        base = {
            "nom_fr": nom_propre,
            "categorie": "Plat Food-101",
            "portion_type_g": 150,
            "calories_100g": 220,
            "proteines_100g": 9.0,
            "glucides_100g": 24.0,
            "lipides_100g": 9.5,
            "fibres_100g": 2.0,
            "sucres_100g": 4.0,
            "description": f"Plat identifié comme {nom_propre}. Les valeurs ci-dessous sont une estimation générique pour {int(grams)} g.",
            "conseil": "Associe ce plat à des légumes riches en fibres et une source de protéines maigres pour maintenir une bonne satiété."
        }

    factor = max(grams, 0.0) / 100.0

    calories = round(base["calories_100g"] * factor)
    proteines = round(base["proteines_100g"] * factor, 1)
    glucides = round(base["glucides_100g"] * factor, 1)
    lipides = round(base["lipides_100g"] * factor, 1)
    fibres = round(base["fibres_100g"] * factor, 1)
    sucres = round(base["sucres_100g"] * factor, 1)

    # Estimation de la répartition calorique (%) : Protéines 4 kcal/g, Glucides 4 kcal/g, Lipides 9 kcal/g
    kcal_p = proteines * 4.0
    kcal_g = glucides * 4.0
    kcal_l = lipides * 9.0
    total_macro_kcal = max(kcal_p + kcal_g + kcal_l, 1.0)

    return {
        "nom_fr": base["nom_fr"],
        "categorie": base["categorie"],
        "portion_type_g": base["portion_type_g"],
        "grammes": int(grams),
        "description": base["description"],
        "conseil": base["conseil"],
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