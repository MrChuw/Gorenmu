from somali.data import Monster
import random


def encontos():
    monstro = Monster()
    encontro ={
        "quote": f"Enquanto andava você avista um grupo de {monstro.name}, \"et 1\" para tentar assustá-los, \"et 2\" para tentar atrair um para longe deles ou \"et 3\" para tentar lutar contra todos.",
        "1": {
            "win": f"Então você corre na direção dos {monstro.name} balançando os braços e gritando, e de alguma forma os assustou.",
            "lose":f"Você corre na direção dos {monstro.name} balançando os braços e gritando, quando eles notam que é apenas um $player_classe$, eles decidem atacar, e você temendo pela sua vida foge o mais rapido que pode"
        },
        "2":{
            "win": f"Aproximando sorrateiramente  do {monstro.name} que estava distante do restante, você consegue atrair ele com sucesso e derrotalo apos uma luta dificil.",
            "lose":f"Aproximando sorrateiramente do {monstro.name} que estava distante do restante, você ao tentar atrair ele acaba chamando do grupo, e presando pela sua vida, decide correr antes que os outros se aproximem."
        },
        "3":{
            "win": f"Enquanto corria em direção dos {monstro.name}, sem nenhum motivo aparente eles começam a lutar entre si, se aproveitando do caos, você consegue matar alguns e correr sem muitos danos.",
            "lose":f"Enquanto corria em direção dos {monstro.name}, eles notam você se aproximando, e te perseguem pelas próximas horas."
        }
        },{
        "quote": f"Você avista a figura de homem misterioso a distância, \"et 1\" para gritar a fim de chamar a sua atenção, \"et 2\" para se aproximar ou \"et 3\" para atacá-lo.",
        "1": {
            "win": f"Sem se virar ele joga uma moeda de ouro nos seus pés, com medo por não ter o visto arremessar você se distancia.",
            "lose":f"Sem se virar ele joga uma moeda de ouro acertando a sua cabeça, fazendo com que você fique desmaiado por algum tempo."
        }, # o 1 seria a opcao mais facil de se resolver
        "2":{
            "win": f"Ao se aproximar sua visão começa a ficar turva, forcando você a coçar os olhos, ao tirar a mão nota que o homem, sumiu e restou apenas uma moeda de ouro no chão.",
            "lose":f"Ao se aproximar sua visão começa a ficar turva, ao um ponto onde você não é mais capaz de enxergar, esse efeito dura por algumas horas, e enquanto isso você anda perdido pelo andar."
        }, # o 2 seria a opcao um pouco mais dificil de se resolver
        "3":{
            "win": f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, você examina os restos e encontra uma bolsa de ouro em frente aos ossos.",
            "lose":f"Ao atacar, a figura se desfaz revelando apenas ossos velhos e tão frágeis quanto gravetos, ao examinar os restos, você é picado por uma aranha e fica com o dedo inchado."
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
        },{
        "quote": f"Em um dos cantos do andar, você avista uma árvore e percebe a presença de um fruto, \"et 1\" para recolher 1 fruto, \"et 2\" para coletar 2 frutos ou \"et 3\" para coletar o máximo possível.",
        "1": {
            "win": f"Você se aproxima da árvore e pega um de seus frutos, ao provar e sente revigorado e pronto para continuar a aventura.",
            "lose":f"Você se aproxima da árvore e pega um de seus frutos, ao provar nota um gosto estranho, olhando para o fruto vê que ele, na verdade, estava estragado."
        }, # o 1 seria a opcao mais facil de se resolver
        "2":{
            "win": f"Você se aproxima da árvore e recolhe um fruto, mas ao tenta puxar o segundo, ele resiste a se soltar, apos pegá-los, você prova um e guarda o outro para mais tarde.",
            "lose":f"Você se aproxima da árvore e recolhe um fruto, mas ao tenta puxar o segundo, ele resiste tentando colocar mais força, você acaba cortando a mão e desiste."
        }, # o 2 seria a opcao um pouco mais dificil de se resolver
        "3":{
            "win": f"Você chuta a árvore com toda a sua força, derrubando vários frutos, apos encher a sua bolsa você vai embora como se nada tivesse acontecido.",
            "lose":f"Você chuta a árvore com toda a sua força, e nada acontece ao olhar para cima nota que a árvore esta pronta para atacar mesmo correndo o máximo que você pode, ainda é atingido na perna e tem que repousar por um dia."
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
        },{
        "quote": f"Ao entrar nesta zona você vê uma caixa no meio da sala, \"et 1\" para se aproximar cautelosamente da caixa, \"et 2\" para cutucar a caixa com um graveto ou \"et 3\" para chutar a caixa.",    
        "1": {
            "win": f"Ao chegar na caixa, você levanta a tampa e vê um bolo comido, você tira uma fatia e vai embora",
            "lose":f"Ao chegar na caixa, você levanta a tampa e vê um bolo cheio de rato, com medo de ficar doente você se afasta."
        }, # o 1 seria a opcao mais facil de se resolver
        "2":{
            "win": f"Você cutuca a caixa… nada acontece, vendo que não tem resposta, você decide colocar a caixa na bolsa e levar, sem verificar o seu conteúdo. ",
            "lose":f"Você cutuca a caixa… então uma ninhada de ratos furiosos saem de dentro da caixa e começam a lhe perseguir"
        }, # o 2 seria a opcao um pouco mais dificil de se resolver
        "3":{
            "win": f"Você chuta a caixa, revelando seu conteúdo, algumas poções de vida e mana, que agora estão quebradas, mas, no fundo da caixa, colada, uma poção de vida grande.",
            "lose":f"Você chuta a caixa, revelando seu conteúdo, algumas poções de vida e mana, que agora estão todas quebradas."
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
        },{
        "quote": f"Você encontra um {monstro.name} gravemente ferido, \"et 1\" para saquear as redondezas, \"et 2\" para saquear os corpos perto do {monstro.name} ou \"et 3\" para finalizá-lo e examinar a área com mais calma.",    
        "1": {
            "win": f"Ao revirar as caixas e sacos ao redor do local de batalha, você encontra um saco de moedas de prata contendo {random.randint(1, 50)} moedas e algumas adagas.",
            "lose":f"Ao revirar as caixas e sacos ao redor do local de batalha, você encontra apenas espadas e arcos quebrados."
        }, # o 1 seria a opcao mais facil de se resolver
        "2":{
            "win": f"Ao saquear os corpos você encontra {random.randint(1, 100)} moedas de prata, e algumas poções de vida.",
            "lose":f"Ao se aproximar do corpo de um guerreiro, em seu último suspiro ele aguarra sua mão, e enquanto alucina pede desculpas por não conseguir voltar para casa."
        }, # o 2 seria a opcao um pouco mais dificil de se resolver
        "3":{
            "win": f"Ao finalizar o {monstro.name}, você nota algumas flechas encantadas, ao longe é notasse um homem encostado em uma parede, ao examiná-lo você nota um colar com algumas coisas escritas, ao não entender você guarda.",
            "lose":f"Ao se aproximar, em seu último suspiro o {monstro.name}, infringe um ataque quase letal em sua barriga, apos gastar algumas poções você consegue se recuperar o suficiente para recuar."
        }  # o 3 seria a opcao mais muito mais dificil de se resolver
        },
    return encontro
'''
{
    "quote": f"'Encontro {monstro.name} Ou algo mais.' , \"et 1\" para 'Opcao 1', \"et 2\" para 'Opcao 2' ou \"et 3\" para 'Opcao 3'.",
    "1": {
        "win": f"Teste1",
        "lose":f"Teste2"
    }, # o 1 seria a opcao mais facil de se resolver
    "2":{
        "win": f"Teste3",
        "lose":f"Teste4"
    }, # o 2 seria a opcao um pouco mais dificil de se resolver
    "3":{
        "win": f"Teste5",
        "lose":f"Teste6"
    }  # o 3 seria a opcao mais muito mais dificil de se resolver
    },
'''