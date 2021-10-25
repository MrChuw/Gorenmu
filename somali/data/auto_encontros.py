import random
import pprint
# from somali.data.variaveis_encontros import *
# from variaveis_encontros import *
# from escolhas import *
# from coisas import *

import random

def gerar_encontros(dungeon: int = None):
    player_entrar = (
        'Ao entrar você avista,',
        'Enquanto corria você avista',
        'Enquanto caminhava você avista,',
        'Você avista ao entrar,',
        'Ao chegar no andar você avista,',
        'Apos passar pela porta você avista,',
        'Enquanto observava os a redores você avista,',
        )

    entrar = random.choice(player_entrar)

    objetos = (
        'a tv',
        'o sofá',
        'a mesa',
        'a cama',
        'a porta',
        'a caixa',
        'a árvore',
        'a cadeira',
        # 'o arbusto',
        'o armario',
        )

    monstros = (
        'a Fada',
        'o Lobo',
        'o Rato',
        'o Gato',
        'o Mico',
        'o Sapo',
        'o Coxo',
        'o Skum',
        'o Leão',
        'o Warg',
        'a Naga',
        'o Fado',
        'o Ente',
        'o Orel',
        'o Amok',
        'a Águia',
        'o Gambá',
        'o Zumbi',
        'a Hiena',
        'o Trobo',
        'o Duplo',
        'o Grick',
        'o Grifo',
        'a Múmia',
        'o Troll',
        'a Lâmia',
        'o Chuul',
        'o Bodak',
        'o Probo',
        'o Muhir',
        'o Balor',
        'o Fúria',
        'o Dragão',
        'o Texugo',
        'o Camelo',
        'o Gorila',
        'o Javali',
        'o Sátiro',
        'o Kitalu',
        'o Lívido',
        'a Sombra',
        'o Ankheg',
        'a Dríade',
        'o Guruan',
        'o Maziel',
        'o Otyugh',
        'o Uktril',
        'o Mantor',
        'o Mímico',
        'o Wyvern',
        'a Baleia',
        'a Medusa',
        'o Falcão',
        'o Goblin',
        'a Súcubo',
        'o Mamute',
        'o Morgue',
        'o Kimazu',
        'o Parcus',
        'o Kraken',
        'o Avimak',
        'o Revyug',
        'o Pileus',
        'a Harpia',
        'a Harpia',
        'o Abolete',
        'o Bugbear',
        'o Carcaju',
        'o Lacedon',
        'a Galhada',
        'a Gárgula',
        'o Igddryl',
        'o Alfgeld',
        'o Inumano',
        'o Afogado',
        'o Bulette',
        'a Quimera',
        'o Veridak',
        'o Erynies',
        'a Górgona',
        'o Aboleth',
        'a Banshee',
        'o Reishid',
        'o Kthurik',
        'o Athrokk',
        'o Buramok',
        'o Nesside',
        'o Theriak',
        'o Trevall',
        'o Cachorro',
        'o Carniçal',
        'o Centauro',
        'o Golfinho',
        'o Sahuagin',
        'o Diabrete',
        'o Leopardo',
        'o Orc Xamã',
        'o Barghest',
        'o Carvarel',
        'a Cocatriz',
        'o Girallon',
        'a Aparição',
        'o Aucharai',
        'o Eiradaan',
        'o Fantasma',
        'o Hurobakk',
        'o Mortalha',
        'a Fera-Mãe',
        'o Múltiplo',
        'o Varukiri',
        'o Marilith',
        'o Rakshasa',
        'a Megapeia',
        'o Magnetus',
        'o Thumroll',
        'o Lobisomem',
        'o Tentacute',
        'o Hobgoblin',
        'o Lobisomem',
        'o Crocodilo',
        'o Kill\'bone',
        'o Orc Negro',
        'o Deinonico',
        'o Unicórnio',
        'o Basilisco',
        'a Cobra-Rei',
        'o Orc Chefe',
        'o Ganchador',
        'o Geraktril',
        'o Incubador',
        'a Mantícora',
        'o Rhayrivel',
        'o Escavador',
        'o Jhumariel',
        'o Rhayphozz',
        'o Margharon',
        'o Thuwarokk',
        'o Tarrasque',
        'o Orc Comum',
        'o Trog Comum',
        'o Homem-Leão',
        'o Ogro Comum',
        'o Urso Negro',
        'o Hipossauro',
        'o Canceronte',
        'o Homem-Rato',
        'o Androdraco',
        'a Gosma Ocre',
        'o Tendrículo',
        'o Kobold Rei',
        'o Catoplebas',
        'o Mathrushka',
        'o Numolliach',
        'a Cobra Naja',
        'o Elfo-do-mar',
        'o Gnoll Comum',
        'a Nagah Comum',
        'o Homem-Hiena',
        'o Cão Abissal',
        'a Fera-Cactus',
        'a Fada-Dragão',
        'o Urso Marrom',
        'o Zumbi Verde',
        'o Gênio do Ar',
        'o Urso-Coruja',
        'o Pudim Negro',
        'o Triceratops',
        'o Aracnarcano',
        'o Anjo-do-Mar',
        'o Nayansilvel',
        'o Rato Gigante',
        'o Sprite Comum',
        'o Kobold Chefe',
        'o Pterodáctilo',
        'o Velociraptor',
        'o Kobold Herói',
        'o Ogro Capanga',
        'o Gigante Leão',
        'o Kobold Comum',
        'a Bruxa do Mar',
        'o Esmaga-Ossos',
        'o Elasmossauro',
        'a Sombra Maior',
        'o Honto-no-Oni',
        'o Tiranossauro',
        'o Gênio da Luz',
        'o Gigante Urso',
        'o Djinni Nobre',
        'o Pássaro Roca',
        'a Fera do Caos',
        'o Gigante Real',
        'a Cobra Jiboia',
        'a Cobra Sucuri',
        'a Asa-Assassina',
        'o Cão de Guarda',
        'o Cogumelo Anão',
        'o Homem-Morcego',
        'o Limo Cinzento',
        'o Tubarão-Touro',
        'a Apiapi Zangão',
        'a Ameba Gigante',
        'o Armadilefante',
        'o Homem Vegetal',
        'o Gênio da Água',
        'o Gênio do Fogo',
        'o Polvo Gigante',
        'o Couatl da Luz',
        'o Braquiossauro',
        'o Golem de Lama',
        'o Verme Púrpura',
        'o Sala da Morte',
        'o Homem-Lagarto',
        'o Homem-Lagarto',
        'o Espada Voadora',
        'a Aranha Gigante',
        'o Cavalo-Marinho',
        'a Coruja Gigante',
        'o Homem-Serpente',
        'o Ogro Esqueleto',
        'o Trog Saqueador',
        'o Cão do Inferno',
        'o Gigante Búfalo',
        'o Cipó Assassino',
        'o Gênio da Terra',
        'o Limo Sangrento',
        'a Nagah Guardião',
        'o Tubarão Branco',
        'a Cobra Cascavel',
        'o Golem de Areia',
        'o Golem de Carne',
        'a Massa Cinzenta',
        'o Rei dos Túneis',
        'o Árvore-Matilha',
        'o Centauro Chefe',
        'a Nagah Cultista',
        'o Golem de Pedra',
        'o Golem de Ferro',
        'o Cemitério Vivo',
        'o Bandido Humano',
        'o Gigante Máximo',
        'o Apiapi Operária',
        'o Pônei de Guerra',
        'o Homem-Crocodilo',
        'o Besouro Gigante',
        'o Cubo Gelatinoso',
        'o Tigre-de-Hynnin',
        'o Horror Blindado',
        'o Golem de Bronze',
        'o Basilisco Maior',
        'o Gigante do Gelo',
        'o Gigante Mutante',
        'o Gigante do Fogo',
        'o Besouro do Óleo',
        'o Inumano General',
        'a Naga das Trevas',
        'o Armadura Voadora',
        'o Humano Esqueleto',
        'o Lagarto Elétrico',
        'o Búfalo de Guerra',
        'o Cavalo de Guerra',
        'o Monstro Ferrugem',
        'o Soldado Mecânico',
        'o Vardak Abençoado',
        'o Wyvern Esqueleto',
        'o Esqueleto-Enxame',
        'o Xamã de Harraakh',
        'o Carrasco de Lena',
        'o Guerreiro da Luz',
        'o Gigante da Pedra',
        'o Gênio das Trevas',
        'o Serpente Marinha',
        'o Gigante Bicéfalo',
        'o Pônei de Montaria',
        'o Enxame de Kobolds',
        'o Lobo-das-Cavernas',
        'o Campeão Batráquio',
        'o Corcel das Trevas',
        'o Crocodilo Marinho',
        'o Caçador Invisível',
        'o Ancião das Rochas',
        'o Dançarino da Água',
        'o Dragão Azul Jovem',
        'o Gigante Crocodilo',
        'o Golem de Espelhos',
        'o Couatl das Trevas',
        'o Gog’magogue Jovem',
        'o Horror das Trevas',
        'o Senhor das Múmias',
        'o Andarilho Noturno',
        'o Espírito da Terra',
        'o Cavalo de Montaria',
        'o Vardak Trabalhador',
        'a Espada-da-Floresta',
        'o Mastim das Sombras',
        'o Cocatriz-Imperador',
        'o Elefante da Savana',
        'o Dragão Negro Jovem',
        'o Dragão Verde Jovem',
        'o Sprite Encantadora',
        'a Orquídea Carnívora',
        'o Dragão Azul Adulto',
        'o Gog’magogue Adulto',
        'o Rastejante Noturno',
        'o Gog’magogue Ancião',
        'o Dragão Azul Ancião',
        'o Homem-Peixe Soldado',
        'o Lagarto Perseguidor',
        'o Pirata do Mar Negro',
        'o Dragão Azul Filhote',
        'o Homem-Peixe Caçador',
        'o Homem-Peixe Clérigo',
        'o Dragão Branco Jovem',
        'o Gigante das Colinas',
        'o Homem-Peixe Capitão',
        'a Pirâmide Gelatinosa',
        'o Dragão Verde Adulto',
        'o Dragão Negro Adulto',
        'o Dragão Verde Ancião',
        'o Dragão Negro Ancião',
        'o Objeto Animado Médio',
        'o Dragão Negro Filhote',
        'o Dragão Verde Filhote',
        'o Garanhão de Namalkah',
        'o Cogumelo Anão Druida',
        'o Guerreiro de Chifres',
        'o Dragão Marinho Jovem',
        'o Dragão Branco Adulto',
        'a Hidra de Dez Cabeças',
        'o Caranguejo de Guerra',
        'o Dragão Branco Ancião',
        'o Colossos de Igasehra',
        'o Dragão Branco Filhote',
        'a Hidra de Duas Cabeças',
        'o Ogro das Sanguinárias',
        'o Dragão Vermelho Jovem',
        'o Dragão Marinho Adulto',
        'o Dragão Azul Venerável',
        'o Dragão Marinho Ancião',
        'o Dragão Marinho Filhote',
        'o Kobold Filho do Dragão',
        'o Elemental do Ar Enorme',
        'a Hidra de Cinco Cabeças',
        'o Elemental do Ar Ancião',
        'o Dragão Vermelho Adulto',
        'o Dragão Verde Venerável',
        'o Dragão Negro Venerável',
        'o Dragão Vermelho Ancião',
        'o Guarda de Cidade Humano',
        'o Orc Comum (Bestiário 2)',
        'o Elemental do Ar Pequeno',
        'o Elemental da Água Médio',
        'o Cogumelo Anão Sentinela',
        'o Dragão Vermelho Filhote',
        'o Gnoll Líder de Alcateia',
        'o Elemental da Luz Enorme',
        'o Elemental da Luz Ancião',
        'o Dragão Branco Venerável',
        'o Elemental da Luz Pequeno',
        'o Pirata do Rio dos Deuses',
        'o Elemental da Terra Médio',
        'o Guardião de Folhas Médio',
        'o Elemental da Água Enorme',
        'o Elemental do Fogo Enorme',
        'o Gnoll Caçador de Cabeças',
        'o Cão de Guerra Rhayrachay',
        'o Elemental da Água Ancião',
        'o Elemental do Fogo Ancião',
        'o Dragão Marinho Venerável',
        'o Elemental do Fogo Pequeno',
        'o Sargento da Guarda Humano',
        'o Guardião de Folhas Grande',
        'o Elemental da Terra Enorme',
        'o Elemental da Terra Ancião',
        'o Dragão Vermelho Venerável',
        'o Elemental das Trevas Médio',
        'o Paraelemental da Lama Médio',
        'o Paraelemental do Gelo Médio',
        'o Urso-das-Cavernas Esqueleto',
        'o Elemental das Trevas Enorme',
        'o Elemental das Trevas Ancião',
        )

    moedas = random.choices(('ouro', 'prata', 'cobre'), weights=(0.20, 0.45, 0.50))

    quantidade_moedas = random.randint(2, 25)

    moedas = f'{quantidade_moedas} {moedas[0]}' 

    encontro = random.choices(["objetos", "monstros"], weights=(0.30, 0.70))
    # encontro = ['monstros']

    if encontro == ['monstros']:
        encontro_escolhido1 = random.choice(monstros)
    else:
        encontro_escolhido1 = random.choice(objetos)


    if encontro_escolhido1[0] == 'a':
        encontro_escolhido = encontro_escolhido1.replace('a', 'uma', 1)
    else:
        encontro_escolhido = encontro_escolhido1.replace('o', 'um', 1)

    opções_monstros = {
        'opção': 'montar uma armadilha',
        'win':  f'Você prepara uma armadilha simples e {encontro_escolhido1} tropeça dando a oportunidade perfeita para você, matá-lo rapidamente.',
        'lose': f'Você prepara uma armadilha simples, mas {encontro_escolhido1} percebe entrando em alerta e eventualmente fugindo.'
        },{
        'opção': 'atacar',
        'win':  f'Você corre em direção d{encontro_escolhido1}, e em um golpe de sorte, você acerta a sua cabeça o matando-o.',
        'lose': f'Você corre em sua direção, {encontro_escolhido1} sabendo de sua presença lança um ataque. Lhe deixa inconsciente.'
        },{
        'opção': 'emboscar',
        'win':  f'Você corre para uma árvore proxima, e espera pascientemente {encontro_escolhido1} se aproximar então você pula enfiando sua adaga em sua cabeça.',
        'lose': f'Você corre para uma árvore proxima, e espera pascientemente {encontro_escolhido1} se aproximar so que ele nunca aparece.'
        },{
        'opção': 'fugir',
        'win': f'Você corre em direção a saída e consegue passar sem ser percebido.',
        'lose': f'Você corre em direção a saída e no meio do caminho trupica e faz muito barulho, tendo que recuar.'
        },{
        'opção': 'emboscar',
        'win': f'Você prepara uma armadilha simples e {encontro_escolhido1} trupica dando a oportunidade perfeita para você, matá-lo rapidamente.',
        'lose': f'Você prepara uma armadilha simples, mas {encontro_escolhido1} percebe entrando em alerta e eventualmente fugindo.'
        },{
        'opção': 'tentar atacar de frente',
        'win': f'Você corre em direção do {encontro_escolhido1} sem pensar muito nas consequências de suas ações, e em um golpe de sorte, acerta a sua cabeça o matando.',
        'lose': f'Você corre em sua direção, {encontro_escolhido1} sabendo de sua presença lança um ataque. Que por sorte não lhe mata, mas lhe deixa inconsciente.'
        }

    opções_objetos = {
        'opção': 'ignorar',
        'win':  f'Apos passar pel{encontro_escolhido1}, você escuta um som de click então {encontro_escolhido1} explode em chamas.',
        'lose': f'Apos passar pel{encontro_escolhido1}, você escuta um grito dizendo "Estou rico" ao tentar encontrar onde {encontro_escolhido1} estava você se perde.'
        },{
        'opção': 'examinar',
        'win':  f'Ao se aproximar você nota um feitiço de disfarce n{encontro_escolhido1}, apos cutucar o feitiço um pouco ele se desfaz revelando uma sacola com {moedas}',
        'lose': f'Ao se aproximar você nota um feitiço de disfarce n{encontro_escolhido1}, apos cutucar o feitiço um pouco ele explode destruindo {encontro_escolhido1} e lhe queimando.'
        },{
        'opção': 'destruir',
        'win':  f'Você atira uma bola de fogo n{encontro_escolhido1}, fazendo ele sumir misteriosamente e deixando um mapa da zona onde ele estava.',
        'lose': f'Você atira uma bola de fogo n{encontro_escolhido1}, fazendo ele sumir misteriosamente e de repente você esta de volta no inicio da zona.'
        },

    if encontro == ['monstros']:
        opção1, opção2, opção3 = random.choice(opções_monstros), random.choice(opções_monstros), random.choice(opções_monstros)
    else:
        opção1, opção2, opção3 = random.choice(opções_objetos), random.choice(opções_objetos), random.choice(opções_objetos)

    while opção1['win'] == opção2['win'] or opção1['win'] == opção3['win']:
        if encontro == ['monstros']:
            opção1 = random.choice(opções_monstros)
        else:
            opção1 = random.choice(opções_objetos)

    while opção2['win'] == opção1['win'] or opção2['win'] == opção3['win']:
        if encontro == ['monstros']:
            opção2 = random.choice(opções_monstros)
        else:
            opção2 = random.choice(opções_objetos)

    while opção3['win'] == opção1['win'] or opção3['win'] == opção2['win']:
        if encontro == ['monstros']:
            opção3 = random.choice(opções_monstros)
        else:
            opção3 = random.choice(opções_objetos)

    encontro_final = {
                    'quote':   f"{entrar} {encontro_escolhido}, \"et 1\" para {opção1['opção']}, \"et 2\" para {opção2['opção']} ou \"et 3\" para {opção3['opção']}.",
                    '1': {
                        'win': f"{opção1['win']}",
                        'lose':f"{opção1['lose']}"
                    },
                    '2':{
                        'win': f"{opção2['win']}",
                        'lose':f"{opção2['lose']}"
                    },
                    '3':{
                        'win': f"{opção3['win']}",
                        'lose':f"{opção3['lose']}"
                    },
                    },{
                    'quote':   f"{entrar} {encontro_escolhido}, \"et 1\" para {opção1['opção']}, \"et 2\" para {opção2['opção']} ou \"et 3\" para {opção3['opção']}.",
                    '1': {
                        'win': f"{opção1['win']}",
                        'lose':f"{opção1['lose']}"
                    },
                    '2':{
                        'win': f"{opção2['win']}",
                        'lose':f"{opção2['lose']}"
                    },
                    '3':{
                        'win': f"{opção3['win']}",
                        'lose':f"{opção3['lose']}"
                    },
                    },{
                    "quote": f"Você avista a figura de homem misterioso a distância, \"et 1\" para gritar a fim de chamar a sua atenção, \"et 2\" para se aproximar ou \"et 3\" para atacá-lo.",
                    "1": {
                        "win": f"Sem se virar ele joga uma moeda de ouro nos seus pés, com medo por não ter o visto arremessar você se distancia.",
                        "lose": f"Sem se virar ele joga uma moeda de ouro acertando a sua cabeça, fazendo com que você fique desmaiado por algum tempo."
                    },
                    "2": {
                        "win": f"Ao se aproximar sua visão começa a ficar turva, forcando você a coçar os olhos, ao tirar a mão nota que o homem, sumiu e restou apenas uma moeda de ouro no chão.",
                        "lose": f"Ao se aproximar sua visão começa a ficar turva, ao um ponto onde você não é mais capaz de enxergar, esse efeito dura por algumas horas, e enquanto isso você anda perdido pelo andar."
                    },
                    "3": {
                        "win": f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, você examina os restos e encontra uma bolsa de ouro em frente aos ossos.",
                        "lose": f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, ao examinar os restos, você é picado por uma aranha e fica com o dedo inchado."
                    },
                    },

    dungeon = int(dungeon) if dungeon else random.randint(0, len(encontro_final) - 1)
    return encontro_final[dungeon], dungeon


# encontro_final = encontros()
# print(encontro_final[0]['quote'],"\n")
# print(encontro_final[0]['1']['win'] ,"\n")
# print(encontro_final[0]['1']['lose'],"\n")
# print(encontro_final[0]['2']['win'] ,"\n")
# print(encontro_final[0]['2']['lose'],"\n")
# print(encontro_final[0]['3']['win'] ,"\n")
# print(encontro_final[0]['3']['lose'],"\n")


"""def gerar_encontros(dungeon: int = None):

    quotes_e_opções_solo = {
        'quote': f'{player_ao_entrada} {monstro}, \"et 1\" para fugir, \"et 2\" para emboscar ou \"et 3\" para tentar enfrentar.',
        '1': {
            'win': f'Você corre em direção a saída e consegue passar sem ser percebido.',
            'lose': f'Você corre em direção a saída e no meio do caminho trupica e faz muito barulho, tendo que recuar..'
        },
        '2': {
            'win': f'Você prepara uma armadilha simples e {monstro_escolhido} trupica dando a oportunidade perfeita para você, matá-lo rapidamente.',
            'lose': f'Você prepara uma armadilha simples, mas {monstro_escolhido} percebe entrando em alerta e eventualmente fugindo.'
        },
        '3': {
            'win': f'Você corre em direção do {monstro_escolhido} sem pensar muito nas consequências de suas ações, e em um golpe de sorte, acerta a sua cabeça o matando.',
            'lose': f'Você corre em sua direção, {monstro_escolhido} sabendo de sua presença lança um ataque. Que por sorte não lhe mata, mas lhe deixa inconsciente.'
        }
    }, {
        'quote': f'{player_ao_entrada} {monstro}, \"et 1\" para fugir, \"et 2\" para emboscar ou \"et 3\" para enfrentar.',
        '1': {
            'win': f'Você corre em direção a saída e consegue passar sem ser percebido.',
            'lose': f'Você corre em direção a saída e no meio do caminho trupica e faz muito barulho, tendo que recuar..'
        },
        '2': {
            'win': f'Você prepara uma armadilha simples e o {monstro_escolhido} tropeça dando a oportunidade perfeita para você, matá-lo rapidamente.',
            'lose': f'Você prepara uma armadilha simples, mas o {monstro_escolhido} percebe entrando em alerta e eventualmente fugindo.'
        },
        '3': {
            'win': f'Você corre em direção do {monstro_escolhido} sem pensar muito nas consequências de suas ações, e em um golpe de sorte, acerta a sua cabeça o matando.',
            'lose': f'Você corre em sua direção, {monstro_escolhido} sabendo de sua presença lança um ataque. Que por sorte não lhe mata, mas lhe deixa inconsciente.'
        }
    }, {
        'quote': f'Você encontra {quote_objeto}, \"et 1\" para {quote_objeto_opcao1}, \"et 2\" para {quote_objeto_opcao2} ou \"et 3\" para {quote_objeto_opcao3}.',
        '1': {
            'win': f'Você vai em direção {objeto}, {win_opcao1}' ,
            'lose':f'Você vai em direção {objeto}, {lose_opcao1}',
        },
        '2': {
            'win': f'Você vai em direção {objeto}, {win_opcao2}' ,
            'lose':f'Você vai em direção {objeto}, {lose_opcao2}',
        },
        '3': {
            'win': f'Você vai em direção {objeto_escolhido} e {win_opcao3}' ,
            'lose':f'Você vai em direção {objeto_escolhido} e {lose_opcao3}',
        }
    },

    quotes_e_opções_grupo = {
        'quote': f'{player_ao_entrada} {monstro},\"et 1\" para fugir, \"et 2\" para emboscar o grupo ou \"et 3\" para tentar enfrentar.',
        '1': {
            'win': f'Você consegue correr através de grupo enquanto eles estavam distraídos com a vegetação ao redor 🌳.',
            'lose': f'Enquanto tentava se esgueirar através do acampamento do grupo de {monstro_escolhido}, você acaba sendo avistado, e decide recuar.'
        },
        '2': {
            'win': f'Você espera ate que o grupo de {monstro_escolhido} se aproxime de um pequeno vale, você pula em cima dos dois que estavam mais atrás, conseguindo matá-los e fugir.',
            'lose': f'Você espera ate que o grupo de {monstro_escolhido} se aproxime de um pequeno vale, você erra, caindo um pouco atrás deles, e quando percebe já esta apanhando, ate perder a consciência.'
        },
        '3': {
            'win': f'Você corre em direção a eles, conseguindo derrubar um desprevenido, e ferindo oque estava ao seu lado, apos muita luta, você decide se afastar, e acaba encontrando a saída.',
            'lose': f'Você corre em direção a eles, conseguindo derrubar um desprevenido, mas acaba levando uma no meio dos olhos e desmaia, por sorte, talvez eles não lhe mataram enquanto estava desmaiado.'
        }
    }, {
        'quote': f'{player_ao_entrada} {monstro},\"et 1\" para fugir, \"et 2\" para emboscar o grupo ou \"et 3\" para tentar enfrentar.',
        '1': {
            'win': f'Você consegue correr através de grupo enquanto eles estavam distraídos com a vegetação ao redor 🌳.',
            'lose': f'Enquanto tentava se esgueirar através do acampamento do grupo de {monstro_escolhido}, você acaba sendo avistado, e decide recuar.'
        },
        '2': {
            'win': f'Você espera ate que o grupo de {monstro_escolhido} se aproxime de um pequeno vale, você pula em cima dos dois que estavam mais atrás, conseguindo matá-los e fugir.',
            'lose': f'Você espera ate que o grupo de {monstro_escolhido} se aproxime de um pequeno vale, você erra, caindo um pouco atrás deles, e quando percebe já esta apanhando, ate perder a consciência.'
        },
        '3': {
            'win': f'Você corre em direção a eles, conseguindo derrubar um desprevenido, e ferindo oque estava ao seu lado, apos muita luta, você decide se afastar, e acaba encontrando a saída.',
            'lose': f'Você corre em direção a eles, conseguindo derrubar um desprevenido, mas acaba levando uma no meio dos olhos e desmaia, por sorte, talvez eles não lhe mataram enquanto estava desmaiado.'
        }
    },

    if escolha_g_s == ['solo']:
        quote_etc_escolha = random.choice(quotes_e_opções_solo)
    else:
        quote_etc_escolha = random.choice(quotes_e_opções_grupo)

    encontro = {
        "quote": f'{quote_etc_escolha["quote"]}',
        "1": {
            "win": f"{quote_etc_escolha['1']['win']}",
            "lose": f"{quote_etc_escolha['1']['lose']}"
        },  # o 1 seria a opcao mais facil de se resolver
        "2": {
            "win": f"{quote_etc_escolha['2']['win']}",
            "lose": f"{quote_etc_escolha['2']['lose']}"
        },  # o 2 seria a opcao um pouco mais dificil de se resolver
        "3": {
            "win": f"{quote_etc_escolha['3']['win']}",
            "lose": f"{quote_etc_escolha['3']['lose']}"
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
    }, {
        "quote": f'{quote_etc_escolha["quote"]}',
        "1": {
            "win": f"{quote_etc_escolha['1']['win']}",
            "lose": f"{quote_etc_escolha['1']['lose']}"
        },  # o 1 seria a opcao mais facil de se resolver
        "2": {
            "win": f"{quote_etc_escolha['2']['win']}",
            "lose": f"{quote_etc_escolha['2']['lose']}"
        },  # o 2 seria a opcao um pouco mais dificil de se resolver
        "3": {
            "win": f"{quote_etc_escolha['3']['win']}",
            "lose": f"{quote_etc_escolha['3']['lose']}"
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
    }, {
        "quote": f"Você avista a figura de homem misterioso a distância, \"et 1\" para gritar a fim de chamar a sua atenção, \"et 2\" para se aproximar ou \"et 3\" para atacá-lo.",
        "1": {
            "win": f"Sem se virar ele joga uma moeda de ouro nos seus pés, com medo por não ter o visto arremessar você se distancia.",
            "lose": f"Sem se virar ele joga uma moeda de ouro acertando a sua cabeça, fazendo com que você fique desmaiado por algum tempo."
        },  # o 1 seria a opcao mais facil de se resolver
        "2": {
            "win": f"Ao se aproximar sua visão começa a ficar turva, forcando você a coçar os olhos, ao tirar a mão nota que o homem, sumiu e restou apenas uma moeda de ouro no chão.",
            "lose": f"Ao se aproximar sua visão começa a ficar turva, ao um ponto onde você não é mais capaz de enxergar, esse efeito dura por algumas horas, e enquanto isso você anda perdido pelo andar."
        },  # o 2 seria a opcao um pouco mais dificil de se resolver
        "3": {
            "win": f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, você examina os restos e encontra uma bolsa de ouro em frente aos ossos.",
            "lose": f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, ao examinar os restos, você é picado por uma aranha e fica com o dedo inchado."
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
    },

    dungeon = int(dungeon) if dungeon else random.randint(0, len(encontro) - 1)
    return encontro[dungeon], dungeon


    # count = 0
    encontru = gerar_encontros()
    # while count < 1:
        # encontru = gerar_encontros()
        # print(f"{encontru[0]['quote']}", '\n')
        # count += 1
    # print(f'{encontru[0]["1"]}','\n')
    # print(f'{encontru[0]["1"]["win"]}', '\n')
    # print(f'{encontru[0]["1"]["lose"]}', '\n')
    # # print(f'{encontru[0]["2"]}','\n')
    # print(f'{encontru[0]["2"]["win"]}', '\n')
    # print(f'{encontru[0]["2"]["lose"]}', '\n')
    # # print(f'{encontru[0]["3"]}','\n')
    # print(f'{encontru[0]["3"]["win"]}', '\n')
    # print(f'{encontru[0]["3"]["lose"]}', '\n')



        {
        'quote': f'{player_ao_entrada} {}/{monstro}, \"et 1\" para "opção", \"et 2\" para "opção" ou \"et 3\" para "opção".', 
        '1': {
            'win': f'texto 1 win',
            'lose':f'texto 1 lose'
        }, 
        '2': {
            'win': f'texto 2 win',
            'lose':f'texto 2 lose'
        }, 
        '3': {
            'win': f'texto 3 win',
            'lose':f'texto 3 lose'
        }
        },

"""