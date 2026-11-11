# Base de données nutritionnelle pour les plats (valeurs estimées pour 100g)

NUTRITION_DATABASE = {
    "apple_pie": {
        "calories": 237,
        "proteines": "2.4 g",
        "glucides": "34.0 g",
        "lipides": "10.0 g",
        "conseil": "Ce plat est riche en sucre et en lipides (pâtisserie). À consommer de manière occasionnelle."
    },
    "caesar_salad": {
        "calories": 150,
        "proteines": "8.0 g",
        "glucides": "5.0 g",
        "lipides": "11.0 g",
        "conseil": "Bon apport en protéines si elle contient du poulet. Attention toutefois à la sauce riche en graisses."
    },
    "pizza": {
        "calories": 266,
        "proteines": "11.0 g",
        "glucides": "33.0 g",
        "lipides": "10.0 g",
        "conseil": "Plat dense en glucides et en graisses saturées. Accompagne-le d'une grande salade verte pour l'équilibrer."
    },
    "sushi": {
        "calories": 143,
        "proteines": "5.0 g",
        "glucides": "25.0 g",
        "lipides": "2.0 g",
        "conseil": "Excellent choix ! Riche en protéines (poisson) et faible en graisses. Veille à limiter la sauce soja salée."
    },
    "hamburger": {
        "calories": 295,
        "proteines": "14.0 g",
        "glucides": "24.0 g",
        "lipides": "15.0 g",
        "conseil": "Riche en calories et en lipides. Pour équilibrer la journée, évite les boissons sucrées avec et privilégie des légumes au repas suivant."
    }
    # Tu pourras ajouter d'autres plats du dataset Food-101 au fur et à mesure ici !
}

def get_nutritional_info(food_name):
    """
    Récupère les informations nutritionnelles d'un plat.
    Si le plat n'est pas dans le dictionnaire, retourne des valeurs par défaut.
    """
    food_name = food_name.lower().strip()
    if food_name in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[food_name]
    else:
        # Valeur par défaut si le plat n'est pas encore répertorié
        return {
            "calories": 200,
            "proteines": "5.0 g",
            "glucides": "20.0 g",
            "lipides": "8.0 g",
            "conseil": "Aliment détecté. Pense à varier tes sources de nutriments pour un repas équilibré."
        }