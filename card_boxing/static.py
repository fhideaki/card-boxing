# Tudo o que é estático (cartas, partes, etc) vai ficar armazenado aqui.
card_list = [
    
    # Criando as cartas de ação básicas.
    {
        "id": 1,
        "category": "CARD",
        "name": "Simple Guard", 
        "class": "GUARD", 
        "type": "neutral", 
        "description": "Simple Guard. Protects against Attack from opponent.It still can be Clinched", 
        "meta": {
            "atk": 0,
            "def": 1, 
            "cli": 0}
    },
    {   
        "id": 2,
        "category": "CARD",
        "name": "Simple Attack", 
        "class":"ATTACK", 
        "type":"neutral", 
        "description": "Simple Attack. Does damage even if the opponent Attacks or Clinches. It can be blocked by Simple Guard.", 
        "meta": {
            "atk": 1, 
            "def": 0, 
            "cli": 0}
    },
    {
        "id": 3,
        "category": "CARD",
        "name": "Clinch", 
        "class": "CLINCH", 
        "type": "neutral", 
        "description": "Clinch, holds the opponent fighter. Vulnerable to opponents attacks. Strong against opponents guards.", 
        "meta":{
            "atk": 0, 
            "def": 0, 
            "cli": 1}
    },

        # Criando as cartas de ação especializadas
    {
        "id": 4,
        "category": "CARD",
        "name": "Strong Attack", 
        "class": "ATTACK", 
        "type": "neutral", 
        "description": "Strong Attack. If the opponent clinches, it does double damage. Does regular damage against Simple Guard.", 
        "meta":{
            "atk": 2, 
            "def": 0, 
            "cli": 0}
    },
    {
        "id": 5, 
        "category": "CARD",
        "name": "Special Guard", 
        "class": "GUARD", 
        "type": "neutral", 
        "description": "Special Guard. Blocks completely any attack. Invulnerable to clinches.", 
        "meta": {
            "atk": 0, 
            "def": 2, 
            "cli": 2}
    }
]

# Lista de partes disponíveis para escolha
parts_list = [
    {
        "id": 1,
        "category": "PART",
        "part_name": "Iron Head", 
        "slot": "HEAD", 
        "description": "A solid Iron head made from pieces found in the scrapyard. If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 2, 
            "strength": 0,
            "agility": -2,
            "HP": 2 
            }, 
            "special_card": {
                "id": 6, 
                "category": "CARD", 
                "name": "Iron Guard",
                "class": "GUARD", 
                "type": "iron", 
                "description": "The Iron Guard is so strong that it returns some damage to the oponent if they choose to attack.", 
                "meta": {
                    "atk": 1, 
                    "def": 1, 
                    "cli": 0
                }
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 2,
        "category": "PART",
        "part_name": "Blazing Arm", 
        "slot": "ARM", 
        "description": "A regular fighter arm bathed in a flammable substance and lit on fire. It increases the damage output but the fire also harms the user.",
        "modifiers": {
            "constitution": -2, 
            "strength": 2,
            "agility": 2,
            "HP": -2 
            }, 
            "special_card": {
                "id": 7, 
                "category": "CARD",
                "name": "Fiery Punch",
                "class": "ATTACK", 
                "type": "fire", 
                "description": "Attack that leaves the opponent with a burn. If it lands, the opponent loses one slot of his hand for the end of the round.", 
                "meta": {
                    "atk": 1, 
                    "def": 1, 
                    "cli": 0
                }
            },
        "resistances": [],
        "weaknesses": ["water"]
    },
    {
        "id": 3,
        "category": "PART",
        "part_name": "Rubber Arm", 
        "slot": "ARM", 
        "description": "A rubber arm that is very flexible and helps holding the opponent. But it is not that powerful.",
        "modifiers": {
            "constitution": 1, 
            "strength": -1,
            "agility": 3,
            "HP": 0 
            }, 
            "special_card": {
                "id": 8, 
                "category": "CARD",
                "name": "Rubber Attack",
                "class": "ATTACK", 
                "type": "rubber", 
                "description": "Hits weakly and automatically clinches if it lands.", 
                "meta": {
                    "atk": 1, 
                    "def": 0, 
                    "cli": 0
                }
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    },
    {
        "id": 4,
        "category": "PART",
        "part_name": "Iron Body", 
        "slot": "BODY",
        "description": "A body part made of iron. Very heavy and durable. If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 6, 
            "strength": 0,
            "agility": -6,
            "HP": 4 
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 5,
        "category": "PART",
        "part_name": "Rubber Body", 
        "slot": "BODY", 
        "description": "A body made of very flexible rubber. It is very effective withstanding attacks without losing agility. If the fighter gets a full set of rubber parts, it unlocks a new special card.",
        "modifiers": {
            "constitution": 2, 
            "strength": -1,
            "agility": 2,
            "HP": 0 
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    },
    {
        "id": 6,
        "category": "PART",
        "part_name": "Iron Leg", 
        "slot": "LEG", 
        "description": "Looks like a very thick nail, but who can tell? If the fighter gets a full set of iron parts, it gets an extra bonus.",
        "modifiers": {
            "constitution": 3, 
            "strength": 0,
            "agility": -2,
            "HP": 2 
            },
        "resistances": ["water", "neutral"],
        "weaknesses": ["fire"]
    },
    {
        "id": 7,
        "category": "PART",
        "part_name": "Rubber Leg", 
        "slot": "LEG", 
        "description": "A leg made of very flexible rubber. It increases agility but sacrifices power. If the fighter gets a full set of rubber parts, it unlocks a new special card.",
        "modifiers": {
            "constitution": 1, 
            "strength": -2,
            "agility": 3,
            "HP": 0 
            },
        "resistances": ["iron"],
        "weaknesses": ["fire"]
    }
]

# Matriz de conflitos
conflicts = {
    "ATTACK": {
        "GUARD": "GUARD",
        "CLINCH": "ATTACK",
        "ATTACK": "BOTH"
    },
    "GUARD": {
        "ATTACK": "GUARD",
        "CLINCH": "CLINCH",
        "GUARD": "BOTH"
    },
    "CLINCH": {
        "GUARD": "CLINCH",
        "ATTACK": "ATTACK",
        "CLINCH": "BOTH"
    }
}