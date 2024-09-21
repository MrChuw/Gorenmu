# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from bot.translations import EnDecorators
from twitchio.ext.commands import Bucket
from textwrap import dedent
from bot.translations.en.extras.response import CommandExemples, Admonitions


class PtBrDecorators(EnDecorators):

    template_part1 = dedent("""
    # {command_title}

    ## Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.

    """).lstrip('\n')  # NOQA

    template_part2 = dedent("""
    {description}

    {aliases}

    """).lstrip('\n')  # NOQA

    template_part3 = "## As formas de utilizar este comando são:\n\n"

    alias_template = dedent("""
    ## Todos os aliases disponíveis para {command_title} são:
        - {aliases}\n
    """).lstrip('\n')  # NOQA

    command_template = dedent("""
    ```text
        user: {prefix}{command_name} {args}

        bot: Usuário, {response}
    ```\n
    """).lstrip('\n')  # NOQA

    admonition_template = dedent("""
    !!! {type} "{title}"

        {message}\n
    """).lstrip('\n')  # NOQA

    @staticmethod
    def get_bucket_type(bucket):
        bucket_type = "geral"
        if bucket == Bucket.default:
            bucket_type = "dont know"

        if bucket == Bucket.channel:
            bucket_type = "todos os usuários no canal"

        if bucket == Bucket.member:
            bucket_type = "usuário por canal"

        if bucket == Bucket.user:
            bucket_type = "usuário independente do canal"

        if bucket == Bucket.subscriber:
            bucket_type = "subscriber"

        if bucket == Bucket.mod:
            bucket_type = "moderação"
        return bucket_type

    class Admin(EnDecorators.Admin):
        class Nada(EnDecorators.Admin.Nada):
            helper = "Este comando é utilizado para testes."
            usage = "Para usar: {}nada <texto>"
            description = "Este comando é utilizado para testes."
            extras = ""
            commands = False
            admonitions = False

        class Reload(EnDecorators.Admin.Reload):
            helper = "Recarrega os comandos."
            usage = "Para usar: {}reload"
            description = ("Este comando é utilizado para recarregar todos os comandos do bot. "
                           "Caso algum tenha sido atualizado e não precisa de um reinício completo.")
            extras = ""
            commands = CommandExemples([{'args': "", 'response': "Os comandos foram recarregados com sucesso."}])
            admonitions = False

        class Restart(EnDecorators.Admin.Restart):
            helper = "Reinicia o bot."
            usage = "Para usar: {}restart"
            description = "Reinicia o bot."
            extras = ""
            commands = CommandExemples([{'args': "", 'response': ""}])
            admonitions = False

    class Others(EnDecorators.Others):
        class Pipe(EnDecorators.Others.Pipe):
            helper = "Pipe não é realmente um comando. Para mais informações, visite o site."
            usage = "Pipe não é realmente um comando. Para mais informações, visite o site."
            description = "Pipe não é realmente um comando. Para mais informações, visite o site."
            extras = ""
            commands = False
            admonitions = False
            template = dedent("""
                    # {command_title}

                    # Isto não é realmente um comando.

                    !!! warning "Cooldown!"

                        O cooldown do pipe será igual ao cooldown dos comandos utilizados.

                    O Pipe é representado pelo caractere "|" (barra vertical), que serve para encaminhar a saída de um comando para outro.

                    ## Como usar pipe:

                    ```text
                    user: {prefix}exemplo_de_comando_1 <opções do comando> | exemplo_de_comando_2 
                    ou 
                    user: {prefix}exemplo_de_comando_1 <opções do comando> | exemplo_de_comando_2 <opções do comando 2> {output} <resto das opções do comando 2>
                    ```

                    ## O passo a passo do bot será:
                     - Executar o `exemplo_de_comando_1` com `<opções do comando>` caso tenha alguma.
                     - Em seguida, ele executará o `exemplo_de_comando_2` com a resposta do comando `exemplo_de_comando_1` adicionada como argumento.
                       - Se você utilizar `{output}`, ele colocará a resposta de `exemplo_de_comando_1` na posição especificada.

                    """)  # NOQA

    class Afk(EnDecorators.Afk):
        class Afk(EnDecorators.Afk.Afk):
            helper = "Comando para entrar em um status."
            usage = "Como usar: {}Afk <mensagem>"
            description = "Este comando define seu status como AFK."
            extras = ""
            commands = CommandExemples([
                {'args': "", 'response': "você ficou ausente: 🏃 ⌨️"},
                {
                    'args': "Texto que você quer deixar para quando voltar ou que as pessoas verão ao usar o "
                            "{prefix}isafk.",
                    'response': "você ficou ausente: 🏃 ⌨️ e deixou uma nota com: Texto que você quer deixar para "
                                "quando voltar ou que as pessoas verão ao usar o {prefix}isafk."
                },
            ])
            admonitions = Admonitions([
                {
                    "admonition_type": "warning",
                    "title": "Tamanho Máximo!",
                    "message": "A mensagem não pode ter mais que 450 caracteres; caso seja maior, retornará um erro."
                },
            ])

        class IsAfk(EnDecorators.Afk.IsAfk):
            helper = "Digite o comando e o nome do usuário para saber se ele está AFK"
            usage = "Para usar: {}IsAfk <nome do usuário>"
            description = "Este comando define se um usuário está AFK ou não."
            extras = ""
            commands = CommandExemples([
                    {'args': "user2", 'response': "@user2 não está afk."},
                    {'args': "user3", 'response': "@user3 está afk."},
                    {'args': "user4", 'response': "@user4 está afk e deixou um bilhete: <mensagem>"},
            ])
            admonitions = False

        class RAfk(EnDecorators.Afk.RAfk):
            helper = "Retorna a ficar AFK"
            usage = "Para usar: {}rafk"
            description = "Este comando é usado para retornar a ficar AFK."
            extras = ""
            commands = CommandExemples([
                {'args': "", 'response': "@user2 você continuou Afk: 🏃 ⌨️"},
                {'args': "<mensagem>", 'response': "@user2 você continuou Afk: 🏃 ⌨️ e deixou um nota: <mensagem>"},
            ])
            admonitions = Admonitions([
                {
                    "admonition_type": "warning",
                    "title": "Tempo Máximo!",
                    "message": "Do momento que você mandar uma mensagem no chat, você têm 2 minutos para retornar ao "
                               "status de Afk."
                },
            ])

    class Alias(EnDecorators.Alias):
        helper = "Comando usado para gerenciar os alias."
        usage = "Para usar: {}alias add|check|copy|describe|edit|link|remove|rename <opções>"
        description = dedent("""
        Este comando gerencia alias personalizados para comandos. Com ele, você pode:
        
         - Adicionar um novo alias para um comando existente.
         - Verificar ou listar alias existentes.
         - Copiar alias de outro usuário.
         - Descrever um alias com uma descrição personalizada.
         - Editar um alias existente, atualizando o comando associado.
         - Linkar um alias para outro alias ou criar um alias baseado em um alias existente.
         - Remover um alias.
         - Renomear um alias.
    
        Use o comando seguido de uma ação (add, check, copy, describe, edit, link, remove, rename) para realizar a tarefa desejada.
        """)  # NOQA
        extras = ""
        template = dedent("""
        # {command_title}
        
        ## Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.
        
        !!! warning "Restrições para os nomes dos aliases!"
        
            - Devem ter entre 2 e 30 caracteres.
            - Podem conter letras, números, traços, subtraços e uma ampla variedade de caracteres Unicode, incluindo emojis.
        
        !!! warning "Cooldown para os aliases criados!"
        
            Ao criar um alias, o cooldown do alias será o cooldown dos comandos utilizados no alias. Portanto, se um comando pode ser usado 1x a cada 5 segundos e outro 3x a cada 10 segundos, o cooldown do alias será 1x a cada 5 segundos.
        
        {description}
        
        ## Como criar um alias:
         - O exemplo a seguir faz uso de [pipe](pipe.md) para passar a resposta de um comando para outro.
        
        ```text
        user: {prefix}{command_name} add nome_legal choice 1234 123456 | count
        
        bot: Usuário, seu alias "nome_legal" foi criado com sucesso.
        ```
        
        Com o exemplo acima, criamos um alias chamado `nome_legal`. O alias invocará o comando `choice` com os argumentos "1234" e "123456", e o resultado do `choice` será enviado para o comando `count`.
        
        ## Para usar o alias:
        
        ```text
        user: {prefix}{prefix}nome_legal
        
        bot: Usuário, há um total de 4 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
        ou
        bot: Usuário, há um total de 6 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
        ```
        
        Para usar o alias, basta usar `{prefix}{prefix}` e o nome do alias ({prefix} é o prefixo padrão do bot; se o prefixo do chat for diferente, basta repetir o prefixo 2 (duas) vezes e então o nome do alias).
        
        ## Como verificar um alias:
        
        ```text
        user: {prefix}{command_name} check nome_legal 
        
        bot: Usuário, o alias "nome_legal" tem os argumentos: choice 1234 123456 | count || Link: <url>
        ```
        
        ## Como copiar um alias:
        
        ```text
        user: {prefix}{command_name} copy <nome do usuário> nome_legal 
        
        bot: Usuário, alias "nome_legal" copiado com sucesso.
        ```
        
        Para copiar um alias, você só precisa do nome do usuário e do nome do alias.
        
        ## Como adicionar uma descrição a um alias:
        
        ```text
        user: {prefix}{command_name} description nome_legal <nova descrição>
        
        bot: Usuário, a descrição do alias "nome_legal" foi atualizada com sucesso.
        ```
        
        ## Como editar o comando/argumentos de um alias:
        
        ```text
        user: {prefix}{command_name} edit nome_legal choice 123 1234 12345 | count
        
        bot: Usuário, o alias "nome_legal" foi editado com sucesso.
        ```
        
        No exemplo acima, a edição do comando foi nos argumentos, mudando de `1234 123456` para `123 1234 12345`. Para atualizar, você deve enviar o comando completo e mudar apenas a parte que deseja atualizar.
        
        ## Como linkar um alias:
        
        ```text
        user: {prefix}{command_name} link <usuário> nome_legal
        
        bot: Usuário, alias vinculado com sucesso. Quando o original mudar, o seu também mudará.
        ```
        
        Também é possível criar um link e mudar o nome do alias.
        
        ```text
        user: {prefix}{command_name} link <usuário> nome_legal outro_nome_legal
        
        bot: Usuário, alias vinculado com sucesso, com um nome personalizado "outro_nome_legal". Quando o original mudar, o seu também mudará.
        ```
        
        E caso seja um link para um link:
        
        ```text
        user: {prefix}{command_name} link <usuário> nome_legal
        
        bot: Usuário, você tentou criar um link a partir de um alias já vinculado (alias nome_legal por <usuário>), então usei o original como seu modelo. Quando o original mudar, o seu também mudará.
        ```
        
        ## Para remover um alias:
        
        ```text
        user: {prefix}{command_name} remove nome_legal
        
        bot: Usuário, seu alias "nome_legal" foi removido com sucesso.
        ```
        
        Ao deletar um alias, os links para este alias continuarão existindo e funcionando.
        
        ## Para renomear um alias:
        
        ```text
        user: {prefix}{command_name} rename nome_legal outro_nome_legal
        
        bot: Usuário, seu alias "nome_legal" foi renomeado com sucesso para "outro_nome_legal".
        ```
        
        # Uso avançado do alias:
        
        ## Primeiro, vamos criar um alias:
        
        ```text
        user: {prefix}{command_name} add uso_avancado choice 1234 123456 | count {0}
        
        bot: Usuário, seu alias "uso_avancado" foi criado com sucesso.
        ```
        
        ## A forma de utilizar este tipo de alias:
        
        ```text
        user: {prefix}{prefix}uso_avancado texto
        
        bot: Há um total de 10 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
        ```
        
        A resposta normal do comando seria: `Há um total de 4 caracteres. etc` ou `Há um total de 6 caracteres. etc`, pois o `choice` escolheria entre `1234` ou `123456` e então o `count` retornaria a quantidade de caracteres.
        
        Mas, devido à adição do `{0}` depois do count, ele irá pegar o conteúdo do que foi enviado ao invocar o alias e substituirá o `{0}`.
        
        # Outras opções ao criar o alias são:
         - `{output}`: ele colocará o output do último comando na posição de `{output}`.
         - `{channel}`: ele substituirá pelo nome do canal atual.
         - `{user}`: ele substituirá pelo seu nick na Twitch.
         - `{0}`, `{1}`, `{2}` etc., podendo também utilizar `{3+}`, que irá pegar todo texto que foi enviado ao invocar o alias e substituir.
        
        ## Um exemplo mostrando todos seria:
        
        ```text
        user: {prefix}{command_name} add uso_avancado2 choice 1234 123456 | count {0} {channel} {output} {user} {1+}
        
        bot: Usuário, seu alias "uso_avancado2" foi criado com sucesso.
        ```
        
        Vamos imaginar que você utilizou o comando desta forma: `{prefix}{prefix}uso_avancado2 algo_aqui e no final`:
        
        ## O passo a passo do bot será:
         - Substituir o `{0}` por `algo_aqui`.
         - Substituir o `{1+}` por `e no final`.
         - Substituir o `{channel}` pelo canal ao qual a mensagem foi enviada, exemplo: `gorenmu`.
         - Substituir o `{user}` pelo seu nick, exemplo: `xXNickOriginalXx`.
         - Enviar o resultado `choice 1234 123456 | count algo_aqui gorenmu {output} xXNickOriginalXx e no final` para ser processado pelo pipe.
        
        ## Ao chegar no pipe, ele irá:
         - Processar a primeira parte: `choice 1234 123456` (como exemplo, vamos dizer que `choice` escolheu `1234`).
         - Processar a segunda parte: `count algo_aqui gorenmu {output} xXNickOriginalXx e no final`; ao processar a segunda parte, ele vai substituir `{output}` por `1234`.
         - Então, o comando que será enviado para o count será `count algo_aqui gorenmu 1234 xXNickOriginalXx e no final`. 
         - E a resposta será `Há um total de 50 caracteres. Dentre eles, 1 são pontuações, 4 são letras maiúsculas e 0 são caracteres especiais.`
        
        """) # NOQA

    class Chance(EnDecorators.Chance):
        helper = "Retorna uma percentagem aleatória."
        usage = "Para usar: {}chance"
        description = "Este comando gera e retorna uma porcentagem aleatória, representando uma chance entre 0% e 100%."
        extras = ""
        commands = CommandExemples([{"args": "", "response": "34%"},])
        admonitions = False

    class Choice(EnDecorators.Choice):
        helper = "Escolhe uma opção das opções passadas pelo usuário"
        usage = "Para usar: {}choice <opção1> ou <opção2>"
        description = "Escolhe uma opção das opções passadas pelo usuário."
        extras = ""
        commands = CommandExemples([
                {"args": "dado ou casa ou moeda", "response": "casa"},
                {"args": "dado casa moeda", "response": "dado"},
                {"args": "dado, casa, moeda", "response": "moeda"},
            ])
        admonitions = False

    class Count(EnDecorators.Count):
        helper = "Conta a quantidade de símbolos em um texto ou em uma URL."
        usage = "Como usar: {}count <texto> ou type:url <quantas URLs quiser>"
        description = ("Este comando pode contar o número de caracteres, letras maiúsculas, pontuações e "
                       "caracteres especiais em um texto ou no conteúdo de uma URL. Se você fornecer um link "
                       "e a tag `type:url`, o comando acessa o conteúdo da página e faz a contagem com base no que "
                       "foi encontrado. E ele guardara o conteúdo da página em cache pôr 30 minutos (trinta minutos).")
        extras = ""
        commands = CommandExemples([
                        {
                            "args": " algum texto legal! com alguns 😄 personagens, espaciais!",
                            "response": "Há um total de 55 caracteres. Dentre eles, 3 são pontuações, 0 são letras "
                                        "maiúsculas e 1 são caracteres especiais."
                        },
                        {
                            "args": "https://example.com/",
                            "response": "Há um total de 20 caracteres. Dentre eles, 5 são pontuações, 0 são letras "
                                        "maiúsculas e 0 são caracteres especiais."
                        },
                        {
                            "args": "type:url https://example.com/ ",
                            "response": "Há um total de 1257 caracteres. Dentre eles, 188 são pontuações, 21 são "
                                        "letras maiúsculas e 0 são caracteres especiais."
                        },
                        {
                            "args": "type:url  https://example.com/ https://example.org/",
                            "response": "Há um total de 2514 caracteres. Dentre eles, 376 são pontuações, 42 são "
                                        "letras maiúsculas e 0 são caracteres especiais."
                        },
                    ])
        admonitions = False

    class HyperTranslate(EnDecorators.HyperTranslate):
        helper = "Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que o usuário pedir."
        usage = "Para usar: <prefixo>hypertranslate <quantidade de vezes> <texto>"
        description = ("Comando baseado no [ravbug](https://www.ravbug.com/hypertranslate/) que serve para traduzir "
                       "um texto em idiomas aleatórios dependendo da quantidade de vezes que o usuário pedir.")
        extras = ""
        commands = CommandExemples([{"args": "10 teste","response": "<algum texto aleatório.>"}])
        admonitions = False

    class NSFW(EnDecorators.NSFW):
        class Imgur(EnDecorators.NSFW.Imgur):
            helper = "Envia um link aleatório do Imgur. (Pode ser NSFW)"
            usage = "Para usar: {}imgur ou {}imgur7 <quantidade>"
            description = ("Este comando gera links aleatórios do Imgur com 5 caracteres, que são de 2014 para trás, e "
                           "usando imgur7 para links de 2014 até o presente.")
            extras = ""
            commands = CommandExemples([
                            {
                                "args": "<quantidade de imagens>",
                                "response": "<link para a imagem ou link para um site com todas as imagens>"
                            },
                            {
                                "args": "7 <quantidade de imagens>",
                                "response": "<link para a imagem ou link para um site com todas as imagens>"
                            },
                        ])
            admonitions = False

        class ImgurRepeated(EnDecorators.NSFW.ImgurRepeated):
            helper = "Verifica a quantidade de imagens do Imgur repetidas."
            usage = "Para usar: {}imgur_repeated"
            description = ("Este comando é simples, ele conta todas as imagens que "
                           "já foram geradas pelo [imgur](imgur.md).")
            extras = ""
            commands = CommandExemples([
                            {
                                "args": "",
                                "response": "Quantidade total de imagens repetidas: <Quantidade de imagens repetidas> "
                                            "|| Imagens: <Link para as imagens>"
                            },
                        ])
            admonitions = False

        class Boru(EnDecorators.NSFW.Boru):
            # Este comando não vai ser adicionado ao site
            helper = "Envia um ou mais links aleatórios de uma lista de boorus."
            usage = "Para usar: {}booru <quantidade>"
            description = "Envia um ou mais links aleatórios de uma lista de boorus."

            # helper = "Envia um ou mais links aleatório de um site de booru específico."
            # usage = "Para usar: {}sfbo <tags1> <tags2> <tags3> --<quantidade opcional>"
            # description = "Envia um ou mais links aleatório de um site de booru específico."

    class RandomColor(EnDecorators.RandomColor):
        helper = "Envia uma cor aleatória."
        usage = "Para usar: {}random_color"
        description = "Este comando responde com o código HEX de uma cor aleatória e o link para uma imagem da cor."
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "",
                            "response": "#<HEX> <Nome da cor> <Link da imagem da cor>"
                        },
                    ])
        admonitions = False

    class Reverse(EnDecorators.Reverse):
        helper = "Reverte um texto."
        usage = "Para usar: {}reverse <texto>"
        description = "Este comando reverte o texto enviado."
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "o texto enviado.",
                            "response": ".odaivne otxet o"
                        },
                    ])
        admonitions = False

    class RandomLine(EnDecorators.RandomLine):
        helper = "Pega uma mensagem aleatória do canal ou do usuário no canal."
        usage = ("para usar: `{0}rl channel:<nome do canal>` ou `{0}rl user:<nome do usuário>` ou `{0}rl` ou "
                 "`{0}rl channel:<nome do canal>` user:<nome do usuário>`")
        description = "Este comando seleciona uma mensagem aleatória dependendo das opções passadas."
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "argumento",
                            "response": "resposta"
                        },
                    ])
        admonitions = Admonitions([
                        {
                            "admonition_type": "warning",
                            "title": "blablabla",
                            "message": "blablabla"
                        },
                    ])
        template = dedent("""
        # {command_title}

        # Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.

        {description}
        
        ## Todos os aliases disponíveis para {command_name} são:
            - {aliases}

        ## As formas de utilizar este comando são:

        ```text
        user: {prefix}{command_name}

        bot: Usuário, <ele irá enviar uma mensagem aleatória do chat atual>
        ```

        ```text
        user: {prefix}{command_name} user:<nome do usuário>

        bot: Usuário, <ele irá enviar uma mensagem aleatória do usuário através de todos os canais>
        ```

        ```text
        user: {prefix}{command_name} channel:<nome do canal>

        bot: Usuário, <ele irá enviar uma mensagem aleatória de um canal específico>
        ```

        ```text
        user: {prefix}{command_name} channel:<nome do canal> user:<nome do usuário>

        bot: Usuário, <ele irá enviar uma mensagem aleatória de um usuário em um canal específico>
        ```
        """)  # NOQA

    class Scp(EnDecorators.Scp):
        helper = "Envia um SCP aleatório."
        usage = "Para usar: {}scp <quantidade>"
        description = ("Este comando utiliza o random do [SCP](https://scp-wiki.wikidot.com) para gerar links "
                       "aleatórios do SCP.")
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "argumento",
                            "response": "resposta"
                        },
                    ])
        admonitions = Admonitions([
                        {
                            "admonition_type": "warning",
                            "title": "blablabla",
                            "message": "blablabla"
                        },
                    ])
        template = dedent("""
        # {command_title}

        # Este comando pode ser usado {rate}x seguidas, com um cooldown de {per} por {cooldown_type}.

        {description}

        ## Todos os aliases disponíveis para {command_name} são:
            - {aliases}

        ## As formas de utilizar este comando são:

        ```text
        usuário: {prefix}{command_name}

        bot: Usuário, <link aleatório para o SCP>
        ```

        ```text
        usuário: {prefix}{command_name} 5

        bot: Usuário, <links aleatórios para o SCP>
        ```
        """)  # NOQA

    class UpSideDown(EnDecorators.UpSideDown):
        helper = "Coloca o texto de cabeça para baixo."
        usage = "Para usar: {}upsidedown <texto>"
        description = "Este comando inverte e coloca o texto enviado de cabeça para baixo."
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "argumento",
                            "response": "resposta"
                        },
                    ])
        admonitions = Admonitions([
                        {
                            "admonition_type": "warning",
                            "title": "blablabla",
                            "message": "blablabla"
                        },
                    ])
        template = dedent("""
        # {command_title}

        # Este comando pode ser usado {rate} vezes seguidas, com um cooldown de {per} por {cooldown_type}.

        {description}

        ## Todos os aliases disponíveis para {command_name} são:
            - {aliases}

        ## As formas de utilizar este comando são:

        ```text
        usuário: {prefix}{command_name} testes

        bot: Usuário, sǝʇsǝʇ
        ```
        """)  # NOQA

    class Wikihow(EnDecorators.Wikihow):
        helper = "Envia um link do wikihow aleatório."
        usage = "Para usar: {}wikihow <quantidade>"
        description = ("Este comando utiliza o random do [Wikihow](https://pt.wikihow.com) para gerar links "
                       "aleatórios.")
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "argumento",
                            "response": "resposta"
                        },
                    ])
        admonitions = Admonitions([
                        {
                            "admonition_type": "warning",
                            "title": "blablabla",
                            "message": "blablabla"
                        },
                    ])
        template = dedent("""
        # {command_title}
        
        # Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.
        
        {description}
        
        ## As formas de utilizar este comando são:

        ```text
        usuário: {prefix}{command_name}

        bot: Usuário, <link aleatório para o wikihow>
        ```

        ```text
        usuário: {prefix}{command_name} 5

        bot: Usuário, <links aleatórios para o wikihow>
        ```
        """)  # NOQA

    class Wikipedia(EnDecorators.Wikipedia):
        helper = "Envia um link da wikipedia aleatório."
        usage = "Para usar: {}wikipedia"
        description = ("Este comando utiliza o random do [Wikipedia](https://pt.Wikipedia.com) para gerar links "
                       "aleatórios.")
        extras = ""
        commands = CommandExemples([
                        {
                            "args": "argumento",
                            "response": "resposta"
                        },
                    ])
        admonitions = Admonitions([
                        {
                            "admonition_type": "warning",
                            "title": "blablabla",
                            "message": "blablabla"
                        },
                    ])
        template = dedent("""
        # {command_title}
        
        # Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.
        
        {description}
        
        ## As formas de utilizar este comando são:

        ```text
        usuário: {prefix}{command_name}

        bot: Usuário, <link aleatório para o Wikipedia>
        ```
        """)  # NOQA

    class Annotations(EnDecorators.Annotations):
        helper = "Cria anotações permanentes para o usuário."
        usage = "Para usar: {}note add/check/delete"
        description = "Este comando serve para criar anotações permanentes."
        extras = ""
        commands = CommandExemples([
                {
                    "args": "add Uma anotação de algo que eu quero poder checar para sempre.",
                    "response": "Anotação criada com sucesso. 📝 (ID: <id da anotação>)"
                }, {
                    "args": "add title:\"título para facilitar lembrar o conteúdo\" Uma anotação de algo que eu quero "
                            "poder checar para sempre.",
                    "response": "Anotação criada com sucesso. 📝 (ID: <id da anotação>)"
                }, {
                    "args": "check",
                    "response": "Suas anotações são as de ID: <título se tiver [id]>"
                }, {
                    "args": "check <id>",
                    "response": "<Conteúdo da anotação.>"
                }, {
                    "args": "delete <id>",
                    "response": "Sua anotação de ID <id> foi deletada com sucesso. 🗑"
                }])
        admonitions = Admonitions([
                {
                    "admonition_type": "warning",
                    "position": "bottom",
                    "title": "Tamanho Máximo para o 'add'!",
                    "message": "A mensagem não pode ter mais que 450 caracteres; caso seja maior, retornará um erro."
                }, {
                    "admonition_type": "warning",
                    "position": "bottom",
                    "title": "Tamanho Máximo para o Título do 'add'!",
                    "message": "O título não pode ter mais que 32 caracteres; caso seja maior, retornará um erro."
                }, {
                    "admonition_type": "tip",
                    "position": "top",
                    "title": "Anotações e Alias",
                    "message": "Use alias e anotações juntos para criar comandos personalizados. "
                               "Por exemplo, com +alias add bolos note check <id>, você poderá usar ++bolos para que o "
                               "bot envie automaticamente o conteúdo da anotação, sem precisar usar o comando completo "
                               "note check <id>."
                }])

    class Lottery(EnDecorators.Lottery):
        helper = "Usado para criar ou verificar apostas."
        usage = "Para usar: {}aposta <números que você quer apostar>"
        description = ("Este comando é usado para criar ou consultar apostas. Elas devem ser feitas utilizando números "
                       "entre 1 e 60, com até 6 números por aposta, no valor de 5 cookies "
                       "(apostas com mais de 6 números são permitidas, mas é mais caro).")
        extras = ""
        commands = CommandExemples([
                {
                    "args": "create 1, 2, 3, 4, 5, 6",
                    "response": "A aposta foi criada com os números [1, 2, 3, 4, 5, 6] e o valor de 5 cookies. (ID: 1)"
                }, {
                    "args": "create random",
                    "response": "A aposta foi criada com os números [números aleatórios entre 1 e 60] e o valor de "
                                "5 cookies. (ID: <id>)"
                }, {
                    "args": "check", "response": "Suas apostas atuais são: [IDs], com o valor total de <Total>."
                }, {
                    "args": "check <ID>",
                    "response": "Aposta com os números: [1, 2, 3, 4, 5, 6] no valor de 5, criada há <Tempo>."
                }, {
                    "args": "check old",
                    "response": "Suas apostas passadas são: <IDs>, com o valor total de <Total>."
                }, {
                    "args": "check new",
                    "response": "Suas apostas atuais são: <IDs>, com o valor total de <Total>."
                }, {
                    "args": "check",
                    "response": "Todas as suas apostas são: <IDs>, com o valor total de <Total>."
                }])
        admonitions = Admonitions([
                {
                    "admonition_type": "info",
                    "position": "bottom",
                    "title": "Desabilitar Notificações.",
                    "message": "Para desabilitar as notificações de loteria no seu canal, você pode usar "
                               "\"[disable](disable.md) lottery notice\"."
                }
        ])

    class Safebooru(EnDecorators.Safebooru):
        helper = "Comando utilizado para gerar imagens aleatórias do Safebooru."
        usage = "Para usar: {}safebooru <quantidade> <tags>"
        description = ("Este comando é utilizado para gerar imagens aleatórias do Safebooru "
                       "e encurtá-las para conveniência.")
        extras = ""
        commands = CommandExemples([
                {
                    'args': "",
                    'response': "Original: <URL> || "
                                "Preview: <URL>"
                },
                {
                    'args': "3",
                    'response': "Original: <URL> || "
                                "Preview: <URL>"
                                "Original: <URL> || "
                                "Preview: <URL>"
                                "Original: <URL> || "
                                "Preview: <URL>"
                },
                {
                    'args': "some_tag",
                    'response': "Original: <URL> || "
                                "Preview: <URL>"
                },
        ])
        admonitions = Admonitions([
                {
                    "admonition_type": "warning",
                    "title": "Tags!",
                    "message": "Para tags que contêm espaços, substitua o espaço por \"_\"."
                }
        ])


    decorators = {
            'pipe': Others.Pipe,
            'afk': Afk,
            'alias': Alias,
            'chance': Chance,
            'choice': Choice,
            'count': Count,
            'hypertranslate': HyperTranslate,
            'randomcolor': RandomColor,
            'reverse': Reverse,
            'randomline': RandomLine,
            'rscp': Scp,
            'upsidedown': UpSideDown,
            'wikihow': Wikihow,
            'annotations': Annotations,
            'lottery': Lottery,


            'NSFW': {
                    'imgur': NSFW.Imgur,
                    'imgur_repeated': NSFW.ImgurRepeated,
            },
            'Dev': {
                    'nada': Admin.Nada,
                    'reload': Admin.Reload,
                    'restart': Admin.Restart,
            }
    }

    class Cookies(EnDecorators.Cookies):
        class Cookie(EnDecorators.Cookies.Cookie):
            helper = "coma um cookie e receba uma frase da sorte."
            usage = "Para usar: {}cookie <quantidade|1>"
            description = "coma um cookie e receba uma frase da sorte."

        class CookieCount(EnDecorators.Cookies.CookieCount):
            helper = "presenteie alguém com seu cookie diário"
            usage = "Para usar: {}gift <nome_do_usuário>"
            description = "presenteie alguém com seu cookie diário"

        class Gift(EnDecorators.Cookies.Gift):
            helper = "aposte seu cookie diário para ter a chance de ganhar outros"
            usage = (
                    "Para usar: {}slotmachine <all pode ser usado para apostar todos os cookies não resgatados rapidamente>")
            description = "aposte seu cookie diário para ter a chance de ganhar outros"

        class SlotMachine(EnDecorators.Cookies.SlotMachine):
            pass

        class Stock(EnDecorators.Cookies.Stock):
            helper = "estoque o seu cookie diário."
            usage = "Para usar: {}stock <all pode ser usado para stockar todos os cookies não resgatados rapidamente>"
            description = "estoque o seu cookie diário."

        class Top(EnDecorators.Cookies.Top):
            helper = "veja quais são os maiores comedores ou doadores de cookies"
            usage = "Para usar: {}top ou passes uma das opções stocked | streak | consumed | donated | received | total"
            description = "veja quais são os maiores comedores ou doadores de cookies"

    class Copy(EnDecorators.Copy):
        class Copy(EnDecorators.Copy.Copy):
            helper = "criar ou consultar uma copypasta."
            usage = "Para usar: {}copy <id da copypasta> ou <prefixo>copy <copypasta>"
            description = "criar ou consultar uma copypasta."

        class DeleteCopy(EnDecorators.Copy.DeleteCopy):
            helper = "deleta uma copypasta."
            usage = "Para usar: {}delcopy <delete> <copy_id da copypasta>"
            description = "deleta uma copypasta."

        class RandomCopy(EnDecorators.Copy.RandomCopy):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class Dungeons(EnDecorators.Dungeons):
        class DungeonLevel(EnDecorators.Dungeons.DungeonLevel):
            helper = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."
            usage = "Para usar: {}level <nome do usuário| author>."
            description = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."

        class DungeonRank(EnDecorators.Dungeons.DungeonRank):
            helper = "saiba quais são os melhores jogadores da dungeon."
            usage = "Para usar: {}dungeonrank win | lose | winrate | warrior | mage | ranger"
            description = ""

        class DungeonEnter(EnDecorators.Dungeons.DungeonEnter):
            helper = ""
            usage = "Para usar: {}"
            description = ""

        class DungeonFast(EnDecorators.Dungeons.DungeonFast):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class General(EnDecorators.General):
        class BotInfo(EnDecorators.General.BotInfo):
            helper = "Veja as principais informações sobre o bot."
            usage = "Para usar: {0}botinfo ou {0}site ou {0}uptime"
            description = "Veja informações o bot, site, uptime."

        class Bug(EnDecorators.General.Bug):
            helper = "reporte um bug que está ocorrendo no Bot."
            usage = "Para usar: {}bug <mensagem>"
            description = "reporte um bug que está ocorrendo no Bot."

        class Channels(EnDecorators.General.Channels):
            helper = "Manda todos os canais conectados"
            usage = "Para usar: {}channels"
            description = "Manda todos os canais conectados"

        class Color(EnDecorators.General.Color):
            helper = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."
            usage = "Para usar: {}color <nick|hex>"
            description = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."

        class Dict(EnDecorators.General.Dict):
            helper = "Pesquisa a palavra no www.dicio.com.br"
            usage = "Para usar: {}dicio <palavra>"
            description = "Pesquisa a palavra no www.dicio.com.br"

        class Echo(EnDecorators.General.Echo):
            helper = "Retorna a mensagem enviada."
            usage = "Para usar: {}echo <mensagem>"
            description = "Retorna a mensagem enviada."

        class Help(EnDecorators.General.Help):
            helper = "Envia informações sobre os comandos."
            usage = "Para usar: {}help <nome_do_comando>"
            description = "Envia informações sobre os comandos."

        class Join(EnDecorators.General.Join):
            helper = "Comando para entrar no seu canal."
            usage = "Para usar: {}join"
            description = "Comando para entrar no seu canal."

        class LastSeen(EnDecorators.General.LastSeen):
            helper = "Mostra o último canal que o usuário usou."
            usage = "Para usar: {}lastseen <nome do usuário>"
            description = "Mostra o último canal que o usuário usou."

        class Leave(EnDecorators.General.Leave):
            helper = "Comando para sair do seu canal."
            usage = "Para usar: {}sair <seu nick>"
            description = "Comando para sair do seu canal."

        class Nicks(EnDecorators.General.Nicks):
            helper = "Histórico de nicks de um usuário."
            usage = "Para usar: {}nicks <nick do usuário>"
            description = "Histórico de nicks de um usuário."

        class Ping(EnDecorators.General.Ping):
            helper = "Verifica alguns status do bot."
            usage = "Para usar: {}ping"
            description = "Verifica alguns status do bot."

        class PopOut(EnDecorators.General.PopOut):
            helper = "Envia o link para o chat em popout de algum canal."
            usage = "Para usar: {}popout <nick do usuário>"
            description = "Envia o link para o chat em popout de algum canal."

        class Preview(EnDecorators.General.Preview):
            helper = "Envia um print do que está acontecendo na live."
            usage = "Para usar: {}preview <nick do usuário>"
            description = "Envia um print do que está acontecendo na live."

        class Spam(EnDecorators.General.Spam):
            helper = "Spam puro e simples. +spam 'quantidade' <mensagem>"
            usage = "Para usar: {}"
            description = "Spam puro e simples. +spam 'quantidade' <mensagem>"

        class Suggest(EnDecorators.General.Suggest):
            helper = "faça uma sugestão de recurso para o bot."
            usage = "Para usar: {}suggest <mensagem>"
            description = "faça uma sugestão de recurso para o bot."

    class Infos(EnDecorators.Infos):
        class AccountAge(EnDecorators.Infos.AccountAge):
            helper = "Mostra a idade da conta de um usuário."
            usage = "Para usar: {}accountage <nome do usuário>"
            description = "Mostra a idade da conta de um usuário."

        class Avatar(EnDecorators.Infos.Avatar):
            helper = "Mostra o avatar de um usuário."
            usage = "Para usar: {}avatar <nome do usuário>"
            description = "Mostra o avatar de um usuário."

        class FirstFollow(EnDecorators.Infos.FirstFollow):
            helper = "Mostra o primeiro seguidor da conta."
            usage = "Para usar: {}firstfollow <nome do usuário>"
            description = "Mostra o primeiro seguidor da conta."

        class FollowAge(EnDecorators.Infos.FollowAge):
            helper = "Mostra o tempo de follow da conta"
            usage = "Para usar: {}followage <nome do usuário> <nome do canal>"
            description = "Mostra o tempo de follow da conta"

        class Live(EnDecorators.Infos.Live):
            helper = "Mostra as informações de uma live."
            usage = "Para usar: {}live <nome do canal>"
            description = "Mostra as informações de uma live."

        class Title(EnDecorators.Infos.Title):
            helper = "Retorna apenas o título de uma stream."
            usage = "Para usar: {}title <nome do usuário>"
            description = "Retorna apenas o título de uma stream."

    class Interactive(EnDecorators.Interactive):
        class Fight(EnDecorators.Interactive.Fight):
            helper = "Desafie alguém para lutar."
            usage = "Para usar: {}fight <usuário>"
            description = "Desafie alguém para lutar."

        class Hug(EnDecorators.Interactive.Hug):
            helper = "Dê um abraço em alguém do chat."
            usage = "Para usar: {}hug <usuário>"
            description = "Dê um abraço em alguém do chat."

        class Kiss(EnDecorators.Interactive.Kiss):
            helper = "Dê um beijinho em alguém do chat."
            usage = "Para usar: {}kiss <usuário>"
            description = "Dê um beijinho em alguém do chat."

        class Love(EnDecorators.Interactive.Love):
            helper = "Veja quanto de amor existe entre o ship de duas pessoas."
            usage = "Para usar: {}love <usuário 1> <usuário 2>"
            description = "Veja quanto de amor existe entre o ship de duas pessoas."

        class Pat(EnDecorators.Interactive.Pat):
            helper = "Faça carinho em alguém do chat."
            usage = "Para usar: {}pat <usuário>"
            description = "Faça carinho em alguém do chat."

        class Penis(EnDecorators.Interactive.Penis):
            helper = "é... é isso mesmo."
            usage = "Para usar: {}penis <usuário>"
            description = "é... é isso mesmo."

        class Slap(EnDecorators.Interactive.Slap):
            helper = "Dê um tapa em alguém do chat."
            usage = "Para usar: {}slap <usuário>"
            description = "Dê um tapa em alguém do chat."

        class Tuck(EnDecorators.Interactive.Tuck):
            helper = "Coloque alguém do chat na cama para dormir"
            usage = "Para usar: {}tuck <usuário>"
            description = "Coloque alguém do chat na cama para dormir"

    class Markov(EnDecorators.Markov):  # TODO: atualizar o site. ou atualizar automaticamente com os docs.
        class Markov(EnDecorators.Markov.Markov):
            helper = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"
            usage = "Para usar: {}Markov"
            description = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"

    class Marry(EnDecorators.Marry):
        class Marry(EnDecorators.Marry.Marry):
            helper = "Case-se e seja feliz para sempre, mas isso custará cookies."
            usage = "Para usar: {}marry <usuário>"
            description = "Case-se e seja feliz para sempre, mas isso custará cookies."

        class Divorce(EnDecorators.Marry.Divorce):
            helper = "Divorcie-se da pessoa com quem você é casada."
            usage = "Para usar: {}divorce <usuário>"
            description = "Divorcie-se da pessoa com quem você é casada."

        class MarryAge(EnDecorators.Marry.MarryAge):
            helper = "Saiba há quanto tempo algum usuário está casado."
            usage = "Para usar: {}ma <usuário>"
            description = "Saiba há quanto tempo algum usuário está casado."

    class Pet(EnDecorators.Pet):
        class Pet(EnDecorators.Pet.Pet):
            helper = "Veja os pets de alguém."
            usage = "Para usar: {}pet <usuário>"
            description = "Veja os pets de alguém."

        class PetList(EnDecorators.Pet.PetList):
            helper = "Veja os pets disponíveis para adquirir no dia."
            usage = "Para usar: {}petlist"
            description = "Veja os pets disponíveis para adquirir no dia."

        class PetName(EnDecorators.Pet.PetName):
            helper = "Dê um nome para o seu pet."
            usage = "Para usar: {}petname <nome do pet>"
            description = "Dê um nome para o seu pet."

        class PetPat(EnDecorators.Pet.PetPat):
            helper = "Faça carinho nos seus pets."
            usage = "Para usar: {}petpat <nome do pat>"
            description = "Faça carinho nos seus pets."

        class PetSell(EnDecorators.Pet.PetSell):
            helper = "Devolva um pet em troca de parte da quantia que gastou."
            usage = "Para usar: {}"
            description = "Devolva um pet em troca de parte da quantia que gastou."

    class Profile(EnDecorators.Profile):
        class Mention(EnDecorators.Profile.Mention):
            helper = "Reativa as menções nos comandos."
            usage = "Para usar: {}mention"
            description = "Reativa as menções nos comandos."

        class NickName(EnDecorators.Profile.NickName):
            helper = "Mude o seu apelido."
            usage = "Para usar: {}nickname <apelido>"
            description = "Mude o seu apelido."

        class SaveCity(EnDecorators.Profile.SaveCity):
            helper = "Digite o comando e o nome da cidade que deseja salvar."
            usage = "Para usar: {}savecity <cidade>"
            description = "Digite o comando e o nome da cidade que deseja salvar."

        class SaveColor(EnDecorators.Profile.SaveColor):
            helper = "Salva um cor pra mais tarde."
            usage = "Para usar: {}savecolor <hex>"
            description = "Salva um cor pra mais tarde."

        class UnMention(EnDecorators.Profile.UnMention):
            helper = "Desativa as menções nos comandos."
            usage = "Para usar: {}unmention"
            description = "Desativa as menções nos comandos."

    class Reminder(EnDecorators.Reminder):
        class Remind(EnDecorators.Reminder.Remind):
            helper = ('Digite remind pessoa (ou me para você), é a "mensagem", e sera lembrado na proxima vez que '
                      "digitar no chat.")
            usage = "Para usar: {}remind <pessoa> in <tempo> <mensagem>"
            description = ('Digite remind pessoa (ou me para você), é a "mensagem", '
                           "e sera lembrado na proxima vez que digitar no chat.")

        class Reminds(EnDecorators.Reminder.Reminds):
            helper = "Mostra os lembretes que você tem."
            usage = "Para usar: {}reminds"
            description = "Mostra os lembretes que você tem."

    class Settings(EnDecorators.Settings):
        class BanWord(EnDecorators.Settings.BanWord):
            helper = "Usado para banir palavras que eu não possa dizer."
            usage = "Para usar: {}banword <termo>"
            description = "Usado para banir palavras que eu não possa dizer."

        class Disable(EnDecorators.Settings.Disable):
            helper = "Usado para desativar comandos."
            usage = "Para usar: {}disable <comando>"
            description = "Usado para desativar comandos."

        class Enable(EnDecorators.Settings.Enable):
            helper = "Usado para reativar comandos desativados."
            usage = "Para usar: {}enable <comando>"
            description = "Usado para reativar comandos desativados."

        class Prefix(EnDecorators.Settings.Prefix):
            helper = "Usado para mudar o prefixo do canal."
            usage = "Para usar: {}prefixo <prefixo>"
            description = "Usado para mudar o prefixo do canal."

        class Start(EnDecorators.Settings.Start):
            helper = "Usado para ligar o bot no canal."
            usage = "Para usar: {}start"
            description = "Usado para ligar o bot no canal."

        class Stop(EnDecorators.Settings.Stop):
            helper = "Usado para desligar o bot no canal."
            usage = "Para usar: {}stop"
            description = "Usado para desligar o bot no canal."

        class UnBanWord(EnDecorators.Settings.UnBanWord):
            helper = "Usado para desbanir palavras que eu não possa diz"
            usage = "Para usar: {}unbanword <termo>"
            description = "Usado para desbanir palavras que eu não possa diz"

    class Tools(EnDecorators.Tools):
        class Math(EnDecorators.Tools.Math):
            helper = "Digite o comando e uma operação matemática para eu resolvê-la."
            usage = "Para usar: {}math <expressão matemática>"
            description = "Digite o comando e uma operação matemática para eu resolvê-la."

        class Shorten(EnDecorators.Tools.Shorten):
            helper = "Encurta links usando o meu serviço de encurtar links."
            usage = "Para usar: {}shorten <links>"
            description = "Encurta links usando o meu serviço de encurtar links."

        class Time(EnDecorators.Tools.Time):
            helper = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                      "etc. Podendo converter para o passado ou para o futuro.")
            usage = "Para usar: {}tempo <formato para transformar ex: h> <formato que vai a ser transformando ex: 50h>"
            description = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                           "etc. Podendo converter para o passado ou para o futuro.")

        class UserId(EnDecorators.Tools.UserId):
            helper = "Pega o user_id de um usuario ou o usuario pelo user_id."
            usage = "Para usar: {}userid <user_id> ou <prefixo>userid <nome do usuário>"
            description = "Pega o user_id de um usuario ou o usuario pelo user_id."

        class Weather(EnDecorators.Tools.Weather):
            helper = "Digite o comando e uma cidade para obter a previsão do tempo."
            usage = "Para usar: {}weather <localização>"
            description = "Digite o comando e uma cidade para obter a previsão do tempo."

    class Tower(EnDecorators.Tower):
        class EnterTower(EnDecorators.Tower.EnterTower):
            helper = "Tenta avançar no seu caminho ao topo da torre."
            usage = "Para usar: {}entertower"
            description = "Tenta avançar no seu caminho ao topo da torre."

        class FastTower(EnDecorators.Tower.FastTower):
            helper = "Opção para limpar um andar da torre de maneira rápida."
            usage = "Para usar: {}fasttower"
            description = "Opção para limpar um andar da torre de maneira rápida."

        class TowerLevel(EnDecorators.Tower.TowerLevel):
            helper = "Mostra o nível atual da torre."
            usage = "Para usar: {}towerlevel"
            description = "Mostra o nível atual da torre."



    class AdminOld(EnDecorators.AdminOld):
        class AddUser(EnDecorators.AdminOld.AddUser):
            helper = "Adiciona um usuário"
            usage = "Para usar: {}add_user <nome do usuário>"
            description = "Este comando adiciona um usuário no banco de dados."

        class AddBot(EnDecorators.AdminOld.AddBot):
            helper = "Adiciona um bot"
            usage = "Para usar: {}addbot <nick do bot>"
            description = ("Usado para retirar os bots de serem comutados pelo Markov de canais. (ja que "
                           "não tem nenhuma forma de eu filtrar o bot sem ter que excluir ele totalmente da tabela.)")

        class AllChannels(EnDecorators.AdminOld.AllChannels):
            helper = "Mostra todos os canais que o bot está."
            usage = "Para usar: {}all_channels"
            description = "Mostra todos os canais que o bot está."

        class Announce(EnDecorators.AdminOld.Announce):
            helper = "Anuncia em todos os canais ou em um canal especifico."
            usage = "Para usar: {}anunciar <all ou nome do canal> <conteudo>"
            description = "Anuncia em todos os canais ou em um canal especifico."

        class ApiBot(EnDecorators.AdminOld.ApiBot):
            helper = "Adiciona bots de uma api que eu achei por ai."
            usage = "Para usar: {}apibot"
            description = "Adiciona bots de uma api que eu achei por ai."

        class ChannelLog(EnDecorators.AdminOld.ChannelLog):
            helper = "Faz o bot entrar em um canal para dar log nas mensagens."
            usage = "Para usar: {}channel_log <nome do canal> <entrar ou sair>"
            description = "Faz o bot entrar em um canal para dar log nas mensagens."

        class CookieGive(EnDecorators.AdminOld.CookieGive):
            helper = "Permite alguém que têm role de developer dar cookies para alguém."
            usage = "Para usar: {}cookie_give <nome do usuário> <quantidade>"
            description = "Permite alguém que têm role de developer dar cookies para alguém."

        class CountUser(EnDecorators.AdminOld.CountUser):
            helper = "Conta quantos usuários tem no banco de dados."
            usage = "Para usar: {}count_user"
            description = "Conta quantos usuários tem no banco de dados."

        class DBGrep(EnDecorators.AdminOld.DBGrep):
            helper = "Pegá as infos de um usuário ou canal."
            usage = "Para usar: {}dbgrep <texto>"
            description = "Pegá as infos de um usuário ou canal."

        class DelFromDB(EnDecorators.AdminOld.DelFromDB):
            helper = "Deleta um usuário ou todos os usuários de um canal."
            usage = "Para usar: {}del_from_db <user ou users_canal> <nome do usuário>"
            description = "Deleta um usuário ou todos os usuários de um canal."

        class DisableNSFW(EnDecorators.AdminOld.DisableNSFW):
            helper = "Desabilita o NSFW em todos os canais."
            usage = "Para usar: {}disable_nsfw"
            description = "Desabilita o NSFW em todos os canais."

        class LotteryStart(EnDecorators.AdminOld.LotteryStart):
            helper = "Inicia um sorteio."
            usage = "Para usar: {}lottery_start <tempo ate o final da loteria> <quantidade que a casa vai colocar>"
            description = "Inicia um sorteio."



        class RGit(EnDecorators.AdminOld.RGit):
            helper = "Puxa do git."
            usage = "Para usar: {}rgit"
            description = "Puxa do git."
