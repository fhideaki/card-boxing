from effects import *

# Tudo o que é estático (cartas, partes, etc) vai ficar armazenado aqui.
card_list = [
    
    # Criando as cartas de ação básicas.
    {
        "id": 1,
        "category": "card",
        "name": "Simple Guard", 
        "class": "guard", 
        "type": "neutral", 
        "description": "Simple Guard. Protects against Attack from opponent.It still can be Clinched",
        "effect": None
    },
    {   
        "id": 2,
        "category": "card",
        "name": "Simple Attack", 
        "class":"attack", 
        "type":"neutral", 
        "description": "Simple Attack. Does damage even if the opponent Attacks or Clinches. It can be blocked by Simple Guard.",
        "effect": None
    },
    {
        "id": 3,
        "category": "card",
        "name": "Clinch", 
        "class": "clinch", 
        "type": "neutral", 
        "description": "Clinch, holds the opponent fighter. Vulnerable to opponents attacks. Strong against opponents guards.",
        "effect": ClinchEffect
    },

        # Criando as cartas de ação especializadas
    {
        "id": 4,
        "category": "card",
        "name": "Strong Attack", 
        "class": "attack", 
        "type": "neutral", 
        "description": "Strong Attack. If the opponent clinches, it does double damage. Does regular damage against Simple Guard.",
        "effect": DoubleDamageEffect
    },
    {
        "id": 5, 
        "category": "card",
        "name": "Special Guard", 
        "class": "guard", 
        "type": "neutral", 
        "description": "Special Guard. Blocks completely any attack. Invulnerable to clinches.",
        "effect": InvincibleEffect
    }
]

# Lista de partes disponíveis para escolha
parts_list = [
    {
        "id": 1,
        "category": "part",
        "part_name": "Iron Head", 
        "slot": "head",
        "type": "iron",
        "description": "A solid Iron head made from pieces found in the scrapyard. If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 2, 
            "strength": 0,
            "agility": -2,
            "HP": 2 
            }, 
            "special_card": {
                "id": 6, 
                "category": "card", 
                "name": "Iron Guard",
                "class": "guard", 
                "type": "iron", 
                "description": "The Iron Guard is so strong that it returns some damage to the oponent if they choose to attack.",
                "effect": StopHittingYourselfEffect
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 2,
        "category": "part",
        "part_name": "Blazing Arm", 
        "slot": "right_arm", 
        "type": "fire",
        "description": "A regular fighter arm bathed in a flammable substance and lit on fire. It increases the damage output but the fire also harms the user.",
        "modifiers": {
            "constitution": -2, 
            "strength": 2,
            "agility": 2,
            "HP": -2 
            }, 
            "special_card": {
                "id": 7, 
                "category": "card",
                "name": "Fiery Punch",
                "class": "attack", 
                "type": "fire", 
                "description": "Attack that leaves the opponent with a burn. If it lands, the opponent loses one slot of his hand for the end of the round.",
                "effect": WhiteHotFirePunchEffect
            },
        "resistances": [],
        "weaknesses": ["water"]
    },
    {
        "id": 3,
        "category": "part",
        "part_name": "Rubber Arm", 
        "slot": "left_arm",
        "type": "rubber",
        "description": "A rubber arm that is very flexible and helps holding the opponent. But it is not that powerful.",
        "modifiers": {
            "constitution": 1, 
            "strength": -1,
            "agility": 3,
            "HP": 0 
            }, 
            "special_card": {
                "id": 8, 
                "category": "card",
                "name": "Rubber Attack",
                "class": "attack", 
                "type": "rubber", 
                "description": "Hits weakly and automatically clinches if it lands.",
                "effect": OmniclinchEffect
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    },
    {
        "id": 4,
        "category": "part",
        "part_name": "Iron Body", 
        "slot": "body",
        "type": "iron",
        "description": "A body part made of iron. Very heavy and durable. If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 6, 
            "strength": 0,
            "agility": -6,
            "HP": 4 
            },            
            "special_card": {
                "id": None, 
                "category": None,
                "name": None,
                "class": None, 
                "type": None, 
                "description": None,
                "effect": None
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 5,
        "category": "part",
        "part_name": "Rubber Body", 
        "slot": "body", 
        "type": "rubber",
        "description": "A body made of very flexible rubber. It is very effective withstanding attacks without losing agility. If the fighter gets a full set of rubber parts, it unlocks a new special card.",
        "modifiers": {
            "constitution": 2, 
            "strength": -1,
            "agility": 2,
            "HP": 0 
            },            
            "special_card": {
                "id": None, 
                "category": None,
                "name": None,
                "class": None, 
                "type": None, 
                "description": None,
                "effect": None,
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    },
    {
        "id": 6,
        "category": "part",
        "part_name": "Iron Leg", 
        "slot": "right_leg", 
        "type": "iron",
        "description": "Looks like a very thick nail, but who can tell? If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 3, 
            "strength": 0,
            "agility": -2,
            "HP": 2 
            },            
            "special_card": {
                "id": None, 
                "category": None,
                "name": None,
                "class": None, 
                "type": None, 
                "description": None,
                "effect": None,
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 7,
        "category": "part",
        "part_name": "Rubber Leg", 
        "slot": "left_leg", 
        "type": "rubber",
        "description": "A leg made of very flexible rubber. It increases agility but sacrifices power. If the fighter gets a full set of rubber parts, it unlocks a new special card.",
        "modifiers": {
            "constitution": 1, 
            "strength": -2,
            "agility": 3,
            "HP": 0 
            },            
            "special_card": {
                "id": None, 
                "category": None,
                "name": None,
                "class": None, 
                "type": None, 
                "description": None,
                "effect": None,
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    }
]

# Matriz de conflitos
conflicts_table = {
    ('attack', 'guard'): {'winner':'p2','winning_class':'guard'}, 
    ('guard', 'attack'): {'winner':'p1','winning_class':'guard'}, 
    ('attack', 'clinch'): {'winner':'p1','winning_class':'attack'},
    ('clinch', 'attack'): {'winner':'p2','winning_class':'attack'},
    ('attack', 'attack'): {'winner':'tie','winning_class':'attack'},
    ('clinch', 'guard'): {'winner':'p1','winning_class':'clinch'},
    ('guard', 'clinch'): {'winner':'p2','winning_class':'clinch'},
    ('clinch', 'clinch'): {'winner':'tie','winning_class':'clinch'},
    ('guard', 'guard'): {'winner':'tie','winning_class':'none'},
}

# Matriz de resistências. Chave - Ataque, Valor - Resistência.
resistances_matrix = {
    "iron": ["water"],
    "rubber": ["fire"],
    "fire": ["water"],
    "neutral":["rubber", "iron"]
}

# Matriz de fraquezas. Chave - Ataque, Valor - Elemento com fraqueza aquele ataque.
weaknesses_matrix = {
    "iron": ["rubber"],
    "rubber": [],
    "fire": ["iron", "rubber"],
    "water": ["fire"],
    "neutral": []
}