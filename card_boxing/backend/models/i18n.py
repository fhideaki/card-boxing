# Traduções de exibição (PT-BR) para os nomes/descrições das cartas.
# Usadas apenas para o texto mostrado ao jogador (log e tela de batalha) -
# o valor interno em inglês (card['name']) continua sendo o usado pela lógica
# do motor (turn.py compara contra esses literais em inglês) e não é alterado aqui.

CARD_NAME_PT = {
    'Simple Guard': 'Guarda Simples',
    'Simple Attack': 'Ataque Simples',
    'Clinch': 'Clinch',
    'Strong Attack': 'Ataque Forte',
    'Special Guard': 'Guarda Especial',
    'Iron Guard': 'Guarda de Ferro',
    'Fiery Punch': 'Soco Flamejante',
    'Rubber Attack': 'Ataque de Borracha',
}

CARD_DESCRIPTION_PT = {
    'Simple Guard': 'Protege contra ataques do oponente. Ainda pode ser agarrada (Clinch).',
    'Simple Attack': 'Causa dano mesmo se o oponente atacar ou agarrar. Pode ser bloqueado pela Guarda Simples.',
    'Clinch': 'Agarra o oponente. Vulnerável a ataques. Forte contra guardas do oponente.',
    'Strong Attack': 'Se o oponente agarrar, causa dano dobrado. Dano normal contra a Guarda Simples.',
    'Special Guard': 'Torna o usuário invulnerável a qualquer ataque ou agarrão.',
    'Iron Guard': 'Tão resistente que devolve parte do dano ao oponente se ele escolher atacar.',
    'Fiery Punch': 'Deixa o oponente queimado: se acertar, ele perde 1 espaço de mão até o fim do round.',
    'Rubber Attack': 'Acerta fraco, mas agarra automaticamente o oponente se conectar.',
}


def nome_carta_pt(nome_en):
    return CARD_NAME_PT.get(nome_en, nome_en)
