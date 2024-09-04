# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from twitchio.ext.commands import Bucket
from textwrap import dedent

if TYPE_CHECKING:
    from bot.ext.commands import Context


class BaseDecorator:
    helper: str
    usage: str
    description: str
    template: str


class BaseClass:
    @classmethod
    def get_decorator(cls, ctx: Context) -> BaseDecorator | None:
        if "usage" in dir(cls):
            return cls  # NOQA
        decorator = ctx.command.decorators[ctx.user.language]
        for classe in dir(decorator):
            invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
            if invoke_by == classe.lower():
                return getattr(decorator, classe)


    @classmethod
    def get_helper(cls, ctx: Context) -> str:
        return cls.get_decorator(ctx).helper.format(ctx.prefix)

    @classmethod
    def get_usage(cls, ctx: Context) -> str:
        return cls.get_decorator(ctx).usage.format(ctx.prefix)

    @classmethod
    def get_dynamic_description(cls, ctx: Context | BaseDecorator):
        return cls.get_decorator(ctx).dynamic_description

    @classmethod
    def get_description(cls, ctx: Context | BaseDecorator) -> str:
        return cls.get_decorator(ctx).description


class EnDecorators:
    @staticmethod
    def get_bucket_type(bucket):
        bucket_type = "geral"
        if bucket == Bucket.default:
            bucket_type = "all user in all channels"

        if bucket == Bucket.channel:
            bucket_type = "all user per channel"

        if bucket == Bucket.member:
            bucket_type = "member"

        if bucket == Bucket.user:
            bucket_type = "user"

        if bucket == Bucket.subscriber:
            bucket_type = "subscriber"

        if bucket == Bucket.mod:
            bucket_type = "mod"
        return bucket_type

    class TypeChecking(BaseDecorator, BaseClass):
        pass

    class Admin(BaseClass):
        class Nada(BaseDecorator, BaseClass):
            helper = "This command is used for testing."
            usage = "How to use: {}nada <text>"
            description = "This command is used for testing."
            extras = ""
            template = dedent("""
            # {command_title}
            
            # This command can be used {rate} times in succession, with a cooldown of {per} per {cooldown_type}.
            
            {description}
               
            ## The way to use this command are always changing.
            
            """)  # NOQA

        class Reload(BaseDecorator, BaseClass):
            helper = "Reloads the commands."
            usage = "How to use: {}reload"
            description = ("This command is used to reload all bot commands. "
                           "If any have been updated and don't require a full restart.")
            extras = ""
            template = dedent("""
            # {command_title}
        
            # This command can be used {rate} times in succession, with a cooldown of {per} per {cooldown_type}.
        
            {description}
        
            ## The way to use this command is:
        
            Just the command:
            ```text
            user: {prefix}{command_name}
        
            bot: User, the commands have been successfully reloaded.
            ```
            """)  # NOQA

    class Others(BaseClass):
        class Pipe(BaseDecorator, BaseClass):
            helper = "Pipe is not really a command. For more information, visit the website."
            usage = "Pipe is not really a command. For more information, visit the website."
            description = "Pipe is not really a command. For more information, visit the website."
            extras = ""
            template = dedent("""
                    # {command_title}

                    # This is not really a command.

                    !!! warning "Cooldown!"

                        The cooldown for the pipe will be the same as the cooldown of the commands used.

                    The Pipe is represented by the character "|" (vertical bar), and it is used to forward the output of one command to another.

                    ## How to use pipe:

                    ```text
                    user: {prefix}example_command_1 <command options> | example_command_2 
                    or 
                    user: {prefix}example_command_1 <command options> | example_command_2 <command 2 options> {output} <remaining command 2 options>
                    ```

                    ## The bot's step-by-step will be:
                     - Execute `example_command_1` with `<command options>` if any.
                     - Then it will execute `example_command_2` with the response from `example_command_1` added as an argument.
                       - If you use `{output}`, it will place the response from `example_command_1` in the specified position.

                    """)  # NOQA

    class Afk(BaseClass):
        class Afk(BaseDecorator, BaseClass):
            helper = "Command to set your status."
            usage = "How to use: {}Afk <message>"
            description = "This command sets your status to AFK."
            extras = ""
            template: str = dedent("""
            # {command_title}

            ## This command can be used {rate}x times in succession, with a cooldown of {per} per {cooldown_type}.
            
            {description}
            
            ## All the alias available for AFK are:
                - {aliases}
            
            ## The ways to use this command are:
            Only the command:
            ```text
            user: {prefix}{command_name}
    
            bot: User, you went AFK: 🏃 ⌨️
            ```
            Command with a message:
            ```text
            user: {prefix}{command_name} Text you want to leave for when you return or that people will see when they use {prefix}isafk.
    
            bot: User, you went AFK: 🏃 ⌨️ and left a note with: Text you want to leave for when you return or that people will see when they use {prefix}isafk.
            ```
            !!! warning "Maximum length!"

                The message could not be longer than 450 characters, if it is longer, an error will be returned.
            """)  # NOQA

        class IsAfk(BaseDecorator, BaseClass):
            helper = "Type the command and the user's name to see if they are AFK."
            usage = "How to use: {}IsAfk <username>"
            description = "This command checks if a user is AFK or not."
            extras = ""
            template = dedent("""
            # {command_title}
        
            ## This command can be used {rate} times in succession, with a cooldown of {per} per {cooldown_type}.
            
            {description}
            
            ## The ways to use this command are:
            
            ```text
            user: {prefix}{command_name} user2
        
            bot: User, @user2 is not AFK.
            ```

            ```text
            user: {prefix}{command_name} user3
        
            bot: User, @user3 is AFK.
            ```

            ```text
            user: {prefix}{command_name} user4
        
            bot: User, @user4 is AFK and left a note: <message>
            ```
            """)  # NOQA

        class RAfk(BaseDecorator, BaseClass):
            helper = "Return to AFK status."
            usage = "To use: {}rafk"
            description = "This command is used to return to AFK status."
            extras = ""
            template = dedent("""
            # {command_title}
            
            ## This command can be used {rate} times in succession, with a cooldown of {per} per {cooldown_type}.
            
            {description}
            
            ## All available aliases for {command_name} are:
                - {aliases}
            
            ## The ways to use this command are:
            
            Just the command:
            ```text
            user: {prefix}{command_name}
            
            bot: User, @user2 you remained AFK: 🏃 ⌨️
            ```
        
            Command with a message:
            ```text
            user: {prefix}{command_name} <message>
            
            bot: User, @user2 you remained AFK: 🏃 ⌨️ and left a note: <message>
            ```
            
            !!! warning "Maximum Length!"
            
                From the moment you send a message in the chat, you have 2 minutes to return to AFK status. 
            """)  # NOQA

    class Alias(BaseDecorator, BaseClass):
        helper = "Command used to manage aliases."
        usage = "To use: {}alias add|check|copy|describe|edit|link|remove|rename <options>"
        description = dedent("""
        This command manages custom aliases for commands. With it, you can:

         - Add a new alias for an existing command.
         - Check or list existing aliases.
         - Copy aliases from another user.
         - Describe an alias with a custom description.
         - Edit an existing alias, updating the associated command.
         - Link an alias to another alias or create an alias based on an existing alias.
         - Remove an alias.
         - Rename an alias.
        
        Use the command followed by an action (add, check, copy, describe, edit, link, remove, rename) to perform the desired task.
        """)  # NOQA # TODO: Fazer o templeta do alias
        extras = ""
        template = dedent("""
        # {command_title}
    
        # This command can be used {rate} times in succession, with a cooldown of {per} per {cooldown_type}.
    
        !!! warning "Restrictions for alias names!"
    
            - Must be between 2 and 30 characters long.
            - Can contain letters, numbers, dashes, underscores, and a wide range of Unicode characters, including emojis.
    
        !!! warning "Cooldown for created aliases!"
    
            When creating an alias, the alias cooldown will be the cooldown of the commands used in the alias. Therefore, if one command can be used 1x every 5 seconds and another 3x every 10 seconds, the alias cooldown will be 1x every 5 seconds.
    
        {description}
    
        ## How to create an alias:
         - The following example uses [pipe](pipe.md) to pass the response of one command to another.
    
        ```text
        user: {prefix}{command_name} add cool_name choice 1234 123456 | count
    
        bot: User, your alias "cool_name" has been successfully created.
        ```
    
        In the example above, we created an alias named `cool_name`. The alias will invoke the `choice` command with the arguments "1234" and "123456", and the result from `choice` will be sent to the `count` command.
    
        ## To use the alias:
    
        ```text
        user: {prefix}{prefix}cool_name
    
        bot: User, there is a total of 4 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
        or
        bot: User, there is a total of 6 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
        ```
    
        To use the alias, just use `{prefix}{prefix}` followed by the alias name ({prefix} is the bot's default prefix; if the chat prefix is different, simply repeat it 2 (two) times and then the alias name).
    
        ## How to check an alias:
    
        ```text
        user: {prefix}{command_name} check cool_name 
    
        bot: User, the alias "cool_name" has the arguments: choice 1234 123456 | count || Link: <url>
        ```
    
        ## How to copy an alias:
    
        ```text
        user: {prefix}{command_name} copy <username> cool_name 
    
        bot: User, alias "cool_name" copied successfully.
        ```
    
        To copy an alias, you only need the username and the alias name.
    
        ## How to add a description to an alias:
    
        ```text
        user: {prefix}{command_name} description cool_name <new description>
    
        bot: User, the description for alias "cool_name" has been successfully updated.
        ```
    
        ## How to edit the command/arguments of an alias:
    
        ```text
        user: {prefix}{command_name} edit cool_name choice 123 1234 12345 | count
    
        bot: User, the alias "cool_name" has been successfully edited.
        ```
    
        In the example above, the command was edited by changing the arguments from `1234 123456` to `123 1234 12345`. To update, you need to send the full command and only change the part you want to update.
    
        ## How to link an alias:
    
        ```text
        user: {prefix}{command_name} link <user> cool_name
    
        bot: User, alias linked successfully. When the original changes, yours will also change.
        ```
    
        It is also possible to create a link and change the alias name.
    
        ```text
        user: {prefix}{command_name} link <user> cool_name new_cool_name
    
        bot: User, alias linked successfully, with a custom name "new_cool_name". When the original changes, yours will also change.
        ```
    
        And if it is a link to a link:
    
        ```text
        user: {prefix}{command_name} link <user> cool_name
    
        bot: User, you attempted to create a link from an already linked alias (alias cool_name by <user>), so I used the original as your model. When the original changes, yours will also change.
        ```
    
        ## To remove an alias:
    
        ```text
        user: {prefix}{command_name} remove cool_name
    
        bot: User, your alias "cool_name" has been successfully removed.
        ```
    
        When deleting an alias, the links to this alias will continue to exist and function.
    
        ## To rename an alias:
    
        ```text
        user: {prefix}{command_name} rename cool_name new_cool_name
    
        bot: User, your alias "cool_name" has been successfully renamed to "new_cool_name".
        ```
        
        # Advanced alias usage:
        
        ## First, let's create an alias:
        
        ```text
        user: {prefix}{command_name} add advanced_usage choice 1234 123456 | count {0}
        
        bot: User, your alias "advanced_usage" has been successfully created.
        ```
        
        # How to use this type of alias:
        
        ```text
        user: {prefix}{prefix}advanced_usage text
        
        bot: There are a total of 10 characters. Among them, 0 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
        ```
        
        The normal response of the command would be: `There are a total of 4 characters. etc` or `There are a total of 6 characters. etc`, as `choice` would select between `1234` or `123456`, and then count would return the number of characters.
        
        But, due to the addition of `{0}` after count, it will take the content of what was sent when invoking the alias and replace `{0}`.
        
        # Other options when creating the alias are:
         - `{output}`: it will place the output of the last command at the `{output}` position.
         - `{channel}`: it will replace with the name of the current channel.
         - `{user}`: it will replace with your Twitch username.
         - `{0}`, `{1}`, `{2}` etc., you can also use `{3+}`, which will take all text sent when invoking the alias and replace.
        
        ## An example showing all would be:
        
        ```text
        user: {prefix}{command_name} add advanced_usage2 choice 1234 123456 | count {0} {channel} {output} {user} {1+}
        
        bot: User, your alias "advanced_usage2" has been successfully created.
        ```
        
        Let's imagine you used the command like this: `{prefix}{prefix}advanced_usage2 something_here and in the end`:
        
        ## The bot's step-by-step process will be:
         - Replace `{0}` with `something_here`.
         - Replace `{1+}` with `and in the end`.
         - Replace `{channel}` with the channel to which the message was sent, for example, `gorenmu`.
         - Replace `{user}` with your username, for example, `xXNickOriginalXx`.
         - Send the result `choice 1234 123456 | count something_here gorenmu {output} xXNickOriginalXx` and in the end to be processed by the pipe.
        
        ## When it reaches the pipe, it will:
         - Process the first part: `choice 1234 123456` (as an example, let's say choice selected `1234`).
         - Process the second part: `count something_here gorenmu {output} xXNickOriginalXx and in the end`; when processing the second part, it will replace `{output}` with `1234`.
         - Then, the command that will be sent to count will be `count something_here gorenmu 1234 xXNickOriginalXx and in the end.`
         - And the response will be `There are a total of 50 characters. Among them, 1 is punctuation, 4 are uppercase letters, and 0 are special characters.` 
         """) # NOQA


    class Chance(BaseDecorator, BaseClass):
        helper = "Returns a random percentage."
        usage = "To use: {}chance"
        description = ("This command generates and returns a random percentage, "
                       "representing a chance between 0% and 100%.")
        extras = ""
        template: str = dedent("""
        # {command_title}
        
        ## This command can be used {rate}x times in succession, with a cooldown of {per} per {cooldown_type}.
        
        {description}
        
        ## All the alias available for AFK are:
            - {aliases}
        
        ## The ways to use this command are:

        ```text
        user: {prefix}{command_name}
        
        bot: User, 34%
        """)  # NOQA

    class Choice(BaseDecorator, BaseClass):
        helper = "Chooses an option from the options provided by the user."
        usage = "To use: {}choice <option1> or <option2>"
        description = "Chooses an option from the options provided by the user."
        extras = ""
        template: str = dedent("""
        # {command_title}
        
        ## This command can be used {rate}x times in succession, with a cooldown of {per} per {cooldown_type}.
        
        {description}
        
        ## All the alias available for AFK are:
            - {aliases}
        
        ## The ways to use this command are:
        
        ```text
        user: {prefix}{command_name} dice or house or coin
        
        bot: User, house
        ```
        ```text
        user: {prefix}{command_name} dice house coin
        
        bot: User, dice
        ```
        ```text
        user: {prefix}{command_name} dice, house, coin
        
        bot: User, coin
        ```
        """)  # NOQA

    class Count(BaseDecorator, BaseClass):
        helper = "Counts the number of symbols in a text or a URL."
        usage = "To use: {}count <text> or type:url <as many URLs as you want>"
        description = ("This command can count the number of characters, uppercase letters, punctuation marks, "
                       "and special characters in a text or the content of a URL. "
                       "If you provide a link and the tag `type:url`, the command fetches the page's "
                       "content and performs the count based on what it finds. "
                       "And it will cache the page content for 30 minutes (thirty minutes).")
        extras = ""
        template: str = dedent("""
        # {command_title}
        
        ## This command can be used {rate}x times in succession, with a cooldown of {per} per {cooldown_type}.
        
        {description}
        
        ## The ways to use this command are:
        ```text
        user: {prefix}{command_name} some nice text! with some 😄 caracteres, spacial!
        
        bot: User, There is a total of 48 characters. Of these, 3 are punctuation marks, 0 are uppercase letters, and 1 are special characters.
        ```
        ```text
        user: {prefix}{command_name} https://example.com/
        
        bot: User, There is a total of 20 characters. Of these, 5 are punctuation marks, 0 are uppercase letters, and 0 are special characters.
        ```
        This command can also be used to calculate the number of characters in the content of one or more links:
        
        ```text
        user: {prefix}{command_name} type:url https://example.com/
        
        bot: User, There is a total of 1257 characters. Of these, 188 are punctuation marks, 21 are uppercase letters, and 0 are special characters.
        ```
        ```text
        user: {prefix}{command_name} type:url https://example.com/ https://example.org/
        
        bot: User, There is a total of 2514 characters. Of these, 376 are punctuation marks, 42 are uppercase letters, and 0 are special characters.
        ```
        """)  # NOQA

    decorators = {
            'afk': Afk,
            'isafk': Afk,
            'rafk': Afk,
            'alias': Alias,
            'chance': Chance,
            'choice': Choice,
            'count': Count,

            'nada': Admin.Nada,
            'reload': Admin.Reload,
            'pipe': Others.Pipe,
    }

    class HyperTranslate(BaseDecorator, BaseClass):
        helper = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer que "
                  "ele seja traduzido.")
        usage = "para usar: <prefixo>hypertranslate <quantidade de vezes que vai ser traduzido/número> <texto>"
        description = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer "
                       "que ele seja traduzido.")

    class Imgur(BaseDecorator, BaseClass):
        helper = "Envia um link aleatorio do imgur. (Pode vir NSFW)"
        usage = "para usar: <prefixo>imgur <quantidade>"
        description = "Envio um link aleatorio do imgur. (Pode vir NSFW)"

    class Imgur7(BaseDecorator, BaseClass):
        helper = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                  "(Pode vir NSFW)")
        usage = "para usar: <prefixo>imgur <quantidade>"
        description = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                       "(Pode vir NSFW)")

    class ImgurRepeated(BaseDecorator, BaseClass):
        helper = "Verifica a quantidade de imgurs repetidos."
        usage = "Para usar: {}imgur_repetidos"
        description = "Verifica a quantidade de imgurs repetidos."

    class RandomColor(BaseDecorator, BaseClass):
        helper = "Envia uma cor aleatória."
        usage = "Para usar: {}random_color"
        description = "Envia uma cor aleatória."

    class Reverse(BaseDecorator, BaseClass):
        helper = "Reverte um texto."
        usage = "Para usar: {}reverse <texto>"
        description = "Reverte um texto."

    class RandomLine(BaseDecorator, BaseClass):
        helper = "Pega uma mensagem aleatória do canal ou do usuário no canal."
        usage = "para usar: `{0}rl --canal:<nome do canal>` ou `{0}rl --user:<nome do usuario>` ou `{0}rl`"
        description = "Pega uma mensagem aleatória do canal ou do usuário no canal."

    class Scp(BaseDecorator, BaseClass):
        helper = "Envia um scp aleatório."
        usage = "Para usar: {}scp <quantidade>"
        description = "Envia um scp aleatório."

    class UpSideDown(BaseDecorator, BaseClass):
        helper = "Coloca o texto de cabeça para baixo."
        usage = "Para usar: {}upsidedown <texto>"
        description = "Coloca o texto de cabeça para baixo."

    class Wikihow(BaseDecorator, BaseClass):
        helper = "Envia um link do wikihow aleatório."
        usage = "Para usar: {}wikihow <quantidade>"
        description = "Envia um link do wikihow aleatório."

    class Wikipedia(BaseDecorator, BaseClass):
            helper = "Envia um link da wikipedia aleatório."
            usage = "Para usar: {}wikipedia <quantidade>"
            description = "Envia um link da wikipedia aleatório."

    class Annotations(BaseClass):
        class Annotation(BaseDecorator, BaseClass):
            helper = "Cria anotações permanentes para o usuário."
            usage = "Para usar: {}anotacao <anotação>"
            description = "Cria anotações permanentes para o usuário."

        class Annotations(BaseDecorator, BaseClass):
            helper = "Lista anotações do usuário. Da mais recente para a mais antiga."
            usage = "Para usar: {}anotacoes"
            description = "Lista anotações do usuário. Da mais recente para a mais antiga."

    class Lottery(BaseClass):
        class Bet(BaseDecorator, BaseClass):
            helper = "use <prefixo>aposta <números que vc quer apostar>"
            usage = "Para usar: {}aposta <números que vc quer apostar>"
            description = "use <prefixo>aposta <números que vc quer apostar>"

        class Lottery(BaseDecorator, BaseClass):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class NSFW(BaseClass):  # TODO: Fazer de novo.
        class Boru(BaseDecorator, BaseClass):
            helper = "Envia um ou mais links aleatório de uma lista de boorus."
            usage = "Para usar: {}booru <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais link aleatório de uma lista de boorus."

        class AllBoorus(BaseDecorator, BaseClass):
            helper = "Envia um ou mais links aleatório de um site de booru específico."
            usage = "Para usar: {}sfbo <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais links aleatório de um site de booru específico."

    class Cookies(BaseClass):
        class Cookie(BaseDecorator, BaseClass):
            helper = "coma um cookie e receba uma frase da sorte."
            usage = "Para usar: {}cookie <quantidade|1>"
            description = "coma um cookie e receba uma frase da sorte."

        class CookieCount(BaseDecorator, BaseClass):
            helper = "presenteie alguém com seu cookie diário"
            usage = "Para usar: {}gift <nome_do_usuário>"
            description = "presenteie alguém com seu cookie diário"

        class Gift(BaseDecorator, BaseClass):
            helper = "aposte seu cookie diário para ter a chance de ganhar outros"
            usage = (
                    "Para usar: {}slotmachine <all pode ser usado para apostar todos os cookies não resgatados rapidamente>")
            description = "aposte seu cookie diário para ter a chance de ganhar outros"

        class SlotMachine(BaseDecorator, BaseClass):
            pass

        class Stock(BaseDecorator, BaseClass):
            helper = "estoque o seu cookie diário."
            usage = "Para usar: {}stock <all pode ser usado para stockar todos os cookies não resgatados rapidamente>"
            description = "estoque o seu cookie diário."

        class Top(BaseDecorator, BaseClass):
            helper = "veja quais são os maiores comedores ou doadores de cookies"
            usage = "Para usar: {}top ou passes uma das opções stocked | streak | consumed | donated | received | total"
            description = "veja quais são os maiores comedores ou doadores de cookies"

    class Copy(BaseClass):
        class Copy(BaseDecorator, BaseClass):
            helper = "criar ou consultar uma copypasta."
            usage = "Para usar: {}copy <id da copypasta> ou <prefixo>copy <copypasta>"
            description = "criar ou consultar uma copypasta."

        class DeleteCopy(BaseDecorator, BaseClass):
            helper = "deleta uma copypasta."
            usage = "Para usar: {}delcopy <delete> <copy_id da copypasta>"
            description = "deleta uma copypasta."

        class RandomCopy(BaseDecorator, BaseClass):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class Dungeons(BaseClass):
        class DungeonLevel(BaseDecorator, BaseClass):
            helper = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."
            usage = "Para usar: {}level <nome do usuário| author>."
            description = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."

        class DungeonRank(BaseDecorator, BaseClass):
            helper = "saiba quais são os melhores jogadores da dungeon."
            usage = "Para usar: {}dungeonrank win | lose | winrate | warrior | mage | ranger"
            description = ""

        class DungeonEnter(BaseDecorator, BaseClass):
            helper = ""
            usage = "Para usar: {}"
            description = ""

        class DungeonFast(BaseDecorator, BaseClass):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class General(BaseClass):
        class BotInfo(BaseDecorator, BaseClass):
            helper = "Veja as principais informações sobre o bot."
            usage = "Para usar: {0}botinfo ou {0}site ou {0}uptime"
            description = "Veja informações o bot, site, uptime."

        class Bug(BaseDecorator, BaseClass):
            helper = "reporte um bug que está ocorrendo no Bot."
            usage = "Para usar: {}bug <mensagem>"
            description = "reporte um bug que está ocorrendo no Bot."

        class Channels(BaseDecorator, BaseClass):
            helper = "Manda todos os canais conectados"
            usage = "Para usar: {}channels"
            description = "Manda todos os canais conectados"

        class Color(BaseDecorator, BaseClass):
            helper = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."
            usage = "Para usar: {}color <nick|hex>"
            description = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."

        class Dict(BaseDecorator, BaseClass):
            helper = "Pesquisa a palavra no www.dicio.com.br"
            usage = "Para usar: {}dicio <palavra>"
            description = "Pesquisa a palavra no www.dicio.com.br"

        class Echo(BaseDecorator, BaseClass):
            helper = "Retorna a mensagem enviada."
            usage = "Para usar: {}echo <mensagem>"
            description = "Retorna a mensagem enviada."

        class Help(BaseDecorator, BaseClass):
            helper = "Envia informações sobre os comandos."
            usage = "Para usar: {}help <nome_do_comando>"
            description = "Envia informações sobre os comandos."

        class Join(BaseDecorator, BaseClass):
            helper = "Comando para entrar no seu canal."
            usage = "Para usar: {}join"
            description = "Comando para entrar no seu canal."

        class LastSeen(BaseDecorator, BaseClass):
            helper = "Mostra o último canal que o usuário usou."
            usage = "Para usar: {}lastseen <nome do usuário>"
            description = "Mostra o último canal que o usuário usou."

        class Leave(BaseDecorator, BaseClass):
            helper = "Comando para sair do seu canal."
            usage = "Para usar: {}sair <seu nick>"
            description = "Comando para sair do seu canal."

        class Nicks(BaseDecorator, BaseClass):
            helper = "Histórico de nicks de um usuário."
            usage = "Para usar: {}nicks <nick do usuário>"
            description = "Histórico de nicks de um usuário."

        class Ping(BaseDecorator, BaseClass):
            helper = "Verifica alguns status do bot."
            usage = "Para usar: {}ping"
            description = "Verifica alguns status do bot."

        class PopOut(BaseDecorator, BaseClass):
            helper = "Envia o link para o chat em popout de algum canal."
            usage = "Para usar: {}popout <nick do usuário>"
            description = "Envia o link para o chat em popout de algum canal."

        class Preview(BaseDecorator, BaseClass):
            helper = "Envia um print do que está acontecendo na live."
            usage = "Para usar: {}preview <nick do usuário>"
            description = "Envia um print do que está acontecendo na live."

        class Spam(BaseDecorator, BaseClass):
            helper = "Spam puro e simples. +spam 'quantidade' <mensagem>"
            usage = "Para usar: {}"
            description = "Spam puro e simples. +spam 'quantidade' <mensagem>"

        class Suggest(BaseDecorator, BaseClass):
            helper = "faça uma sugestão de recurso para o bot."
            usage = "Para usar: {}suggest <mensagem>"
            description = "faça uma sugestão de recurso para o bot."

    class Infos(BaseClass):
        class AccountAge(BaseDecorator, BaseClass):
            helper = "Mostra a idade da conta de um usuário."
            usage = "Para usar: {}accountage <nome do usuário>"
            description = "Mostra a idade da conta de um usuário."

        class Avatar(BaseDecorator, BaseClass):
            helper = "Mostra o avatar de um usuário."
            usage = "Para usar: {}avatar <nome do usuário>"
            description = "Mostra o avatar de um usuário."

        class FirstFollow(BaseDecorator, BaseClass):
            helper = "Mostra o primeiro seguidor da conta."
            usage = "Para usar: {}firstfollow <nome do usuário>"
            description = "Mostra o primeiro seguidor da conta."

        class FollowAge(BaseDecorator, BaseClass):
            helper = "Mostra o tempo de follow da conta"
            usage = "Para usar: {}followage <nome do usuário> <nome do canal>"
            description = "Mostra o tempo de follow da conta"

        class Live(BaseDecorator, BaseClass):
            helper = "Mostra as informações de uma live."
            usage = "Para usar: {}live <nome do canal>"
            description = "Mostra as informações de uma live."

        class Title(BaseDecorator, BaseClass):
            helper = "Retorna apenas o título de uma stream."
            usage = "Para usar: {}title <nome do usuário>"
            description = "Retorna apenas o título de uma stream."

    class Interactive(BaseClass):
        class Fight(BaseDecorator, BaseClass):
            helper = "Desafie alguém para lutar."
            usage = "Para usar: {}fight <usuário>"
            description = "Desafie alguém para lutar."

        class Hug(BaseDecorator, BaseClass):
            helper = "Dê um abraço em alguém do chat."
            usage = "Para usar: {}hug <usuário>"
            description = "Dê um abraço em alguém do chat."

        class Kiss(BaseDecorator, BaseClass):
            helper = "Dê um beijinho em alguém do chat."
            usage = "Para usar: {}kiss <usuário>"
            description = "Dê um beijinho em alguém do chat."

        class Love(BaseDecorator, BaseClass):
            helper = "Veja quanto de amor existe entre o ship de duas pessoas."
            usage = "Para usar: {}love <usuário 1> <usuário 2>"
            description = "Veja quanto de amor existe entre o ship de duas pessoas."

        class Pat(BaseDecorator, BaseClass):
            helper = "Faça carinho em alguém do chat."
            usage = "Para usar: {}pat <usuário>"
            description = "Faça carinho em alguém do chat."

        class Penis(BaseDecorator, BaseClass):
            helper = "é... é isso mesmo."
            usage = "Para usar: {}penis <usuário>"
            description = "é... é isso mesmo."

        class Slap(BaseDecorator, BaseClass):
            helper = "Dê um tapa em alguém do chat."
            usage = "Para usar: {}slap <usuário>"
            description = "Dê um tapa em alguém do chat."

        class Tuck(BaseDecorator, BaseClass):
            helper = "Coloque alguém do chat na cama para dormir"
            usage = "Para usar: {}tuck <usuário>"
            description = "Coloque alguém do chat na cama para dormir"

    class Markov(BaseClass):  # TODO: atualizar o site. ou atualizar automaticamente com os docs.
        class Markov(BaseDecorator, BaseClass):
            helper = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"
            usage = "Para usar: {}Markov"
            description = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"

    class Marry(BaseClass):
        class Marry(BaseDecorator, BaseClass):
            helper = "Case-se e seja feliz para sempre, mas isso custará cookies."
            usage = "Para usar: {}marry <usuário>"
            description = "Case-se e seja feliz para sempre, mas isso custará cookies."

        class Divorce(BaseDecorator, BaseClass):
            helper = "Divorcie-se da pessoa com quem você é casada."
            usage = "Para usar: {}divorce <usuário>"
            description = "Divorcie-se da pessoa com quem você é casada."

        class MarryAge(BaseDecorator, BaseClass):
            helper = "Saiba há quanto tempo algum usuário está casado."
            usage = "Para usar: {}ma <usuário>"
            description = "Saiba há quanto tempo algum usuário está casado."

    class Pet(BaseClass):
        class Pet(BaseDecorator, BaseClass):
            helper = "Veja os pets de alguém."
            usage = "Para usar: {}pet <usuário>"
            description = "Veja os pets de alguém."

        class PetList(BaseDecorator, BaseClass):
            helper = "Veja os pets disponíveis para adquirir no dia."
            usage = "Para usar: {}petlist"
            description = "Veja os pets disponíveis para adquirir no dia."

        class PetName(BaseDecorator, BaseClass):
            helper = "Dê um nome para o seu pet."
            usage = "Para usar: {}petname <nome do pet>"
            description = "Dê um nome para o seu pet."

        class PetPat(BaseDecorator, BaseClass):
            helper = "Faça carinho nos seus pets."
            usage = "Para usar: {}petpat <nome do pat>"
            description = "Faça carinho nos seus pets."

        class PetSell(BaseDecorator, BaseClass):
            helper = "Devolva um pet em troca de parte da quantia que gastou."
            usage = "Para usar: {}"
            description = "Devolva um pet em troca de parte da quantia que gastou."

    class Profile(BaseClass):
        class Mention(BaseDecorator, BaseClass):
            helper = "Reativa as menções nos comandos."
            usage = "Para usar: {}mention"
            description = "Reativa as menções nos comandos."

        class NickName(BaseDecorator, BaseClass):
            helper = "Mude o seu apelido."
            usage = "Para usar: {}nickname <apelido>"
            description = "Mude o seu apelido."

        class SaveCity(BaseDecorator, BaseClass):
            helper = "Digite o comando e o nome da cidade que deseja salvar."
            usage = "Para usar: {}savecity <cidade>"
            description = "Digite o comando e o nome da cidade que deseja salvar."

        class SaveColor(BaseDecorator, BaseClass):
            helper = "Salva um cor pra mais tarde."
            usage = "Para usar: {}savecolor <hex>"
            description = "Salva um cor pra mais tarde."

        class UnMention(BaseDecorator, BaseClass):
            helper = "Desativa as menções nos comandos."
            usage = "Para usar: {}unmention"
            description = "Desativa as menções nos comandos."

    class Reminder(BaseClass):
        class Remind(BaseDecorator, BaseClass):
            helper = ('Digite remind pessoa (ou me para você), é a "mensagem", e sera lembrado na proxima vez que '
                      "digitar no chat.")
            usage = "Para usar: {}remind <pessoa> in <tempo> <mensagem>"
            description = ('Digite remind pessoa (ou me para você), é a "mensagem", '
                           "e sera lembrado na proxima vez que digitar no chat.")

        class Reminds(BaseDecorator, BaseClass):
            helper = "Mostra os lembretes que você tem."
            usage = "Para usar: {}reminds"
            description = "Mostra os lembretes que você tem."

    class Settings(BaseClass):
        class BanWord(BaseDecorator, BaseClass):
            helper = "Usado para banir palavras que eu não possa dizer."
            usage = "Para usar: {}banword <termo>"
            description = "Usado para banir palavras que eu não possa dizer."

        class Disable(BaseDecorator, BaseClass):
            helper = "Usado para desativar comandos."
            usage = "Para usar: {}disable <comando>"
            description = "Usado para desativar comandos."

        class Enable(BaseDecorator, BaseClass):
            helper = "Usado para reativar comandos desativados."
            usage = "Para usar: {}enable <comando>"
            description = "Usado para reativar comandos desativados."

        class Prefix(BaseDecorator, BaseClass):
            helper = "Usado para mudar o prefixo do canal."
            usage = "Para usar: {}prefixo <prefixo>"
            description = "Usado para mudar o prefixo do canal."

        class Start(BaseDecorator, BaseClass):
            helper = "Usado para ligar o bot no canal."
            usage = "Para usar: {}start"
            description = "Usado para ligar o bot no canal."

        class Stop(BaseDecorator, BaseClass):
            helper = "Usado para desligar o bot no canal."
            usage = "Para usar: {}stop"
            description = "Usado para desligar o bot no canal."

        class UnBanWord(BaseDecorator, BaseClass):
            helper = "Usado para desbanir palavras que eu não possa diz"
            usage = "Para usar: {}unbanword <termo>"
            description = "Usado para desbanir palavras que eu não possa diz"

    class Tools(BaseClass):
        class Math(BaseDecorator, BaseClass):
            helper = "Digite o comando e uma operação matemática para eu resolvê-la."
            usage = "Para usar: {}math <expressão matemática>"
            description = "Digite o comando e uma operação matemática para eu resolvê-la."

        class Shorten(BaseDecorator, BaseClass):
            helper = "Encurta links usando o meu serviço de encurtar links."
            usage = "Para usar: {}shorten <links>"
            description = "Encurta links usando o meu serviço de encurtar links."

        class Time(BaseDecorator, BaseClass):
            helper = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                      "etc. Podendo converter para o passado ou para o futuro.")
            usage = "Para usar: {}tempo <formato para transformar ex: h> <formato que vai a ser transformando ex: 50h>"
            description = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                           "etc. Podendo converter para o passado ou para o futuro.")

        class UserId(BaseDecorator, BaseClass):
            helper = "Pega o user_id de um usuario ou o usuario pelo user_id."
            usage = "Para usar: {}userid <user_id> ou <prefixo>userid <nome do usuário>"
            description = "Pega o user_id de um usuario ou o usuario pelo user_id."

        class Weather(BaseDecorator, BaseClass):
            helper = "Digite o comando e uma cidade para obter a previsão do tempo."
            usage = "Para usar: {}weather <localização>"
            description = "Digite o comando e uma cidade para obter a previsão do tempo."

    class Tower(BaseClass):
        class EnterTower(BaseDecorator, BaseClass):
            helper = "Tenta avançar no seu caminho ao topo da torre."
            usage = "Para usar: {}entertower"
            description = "Tenta avançar no seu caminho ao topo da torre."

        class FastTower(BaseDecorator, BaseClass):
            helper = "Opção para limpar um andar da torre de maneira rápida."
            usage = "Para usar: {}fasttower"
            description = "Opção para limpar um andar da torre de maneira rápida."

        class TowerLevel(BaseDecorator, BaseClass):
            helper = "Mostra o nível atual da torre."
            usage = "Para usar: {}towerlevel"
            description = "Mostra o nível atual da torre."



    class AdminOld(BaseClass):
        class AddUser(BaseDecorator, BaseClass):
            helper = "Adiciona um usuário"
            usage = "Para usar: {}add_user <nome do usuário>"
            description = "Este comando adiciona um usuário no banco de dados."

        class AddBot(BaseDecorator, BaseClass):
            helper = "Adiciona um bot"
            usage = "Para usar: {}addbot <nick do bot>"
            description = ("Usado para retirar os bots de serem comutados pelo Markov de canais. (ja que "
                           "não tem nenhuma forma de eu filtrar o bot sem ter que excluir ele totalmente da tabela.)")

        class AllChannels(BaseDecorator, BaseClass):
            helper = "Mostra todos os canais que o bot está."
            usage = "Para usar: {}all_channels"
            description = "Mostra todos os canais que o bot está."

        class Announce(BaseDecorator, BaseClass):
            helper = "Anuncia em todos os canais ou em um canal especifico."
            usage = "Para usar: {}anunciar <all ou nome do canal> <conteudo>"
            description = "Anuncia em todos os canais ou em um canal especifico."

        class ApiBot(BaseDecorator, BaseClass):
            helper = "Adiciona bots de uma api que eu achei por ai."
            usage = "Para usar: {}apibot"
            description = "Adiciona bots de uma api que eu achei por ai."

        class ChannelLog(BaseDecorator, BaseClass):
            helper = "Faz o bot entrar em um canal para dar log nas mensagens."
            usage = "Para usar: {}channel_log <nome do canal> <entrar ou sair>"
            description = "Faz o bot entrar em um canal para dar log nas mensagens."

        class CookieGive(BaseDecorator, BaseClass):
            helper = "Permite alguém que têm role de developer dar cookies para alguém."
            usage = "Para usar: {}cookie_give <nome do usuário> <quantidade>"
            description = "Permite alguém que têm role de developer dar cookies para alguém."

        class CountUser(BaseDecorator, BaseClass):
            helper = "Conta quantos usuários tem no banco de dados."
            usage = "Para usar: {}count_user"
            description = "Conta quantos usuários tem no banco de dados."

        class DBGrep(BaseDecorator, BaseClass):
            helper = "Pegá as infos de um usuário ou canal."
            usage = "Para usar: {}dbgrep <texto>"
            description = "Pegá as infos de um usuário ou canal."

        class DelFromDB(BaseDecorator, BaseClass):
            helper = "Deleta um usuário ou todos os usuários de um canal."
            usage = "Para usar: {}del_from_db <user ou users_canal> <nome do usuário>"
            description = "Deleta um usuário ou todos os usuários de um canal."

        class DisableNSFW(BaseDecorator, BaseClass):
            helper = "Desabilita o NSFW em todos os canais."
            usage = "Para usar: {}disable_nsfw"
            description = "Desabilita o NSFW em todos os canais."

        class LotteryStart(BaseDecorator, BaseClass):
            helper = "Inicia um sorteio."
            usage = "Para usar: {}lottery_start <tempo ate o final da loteria> <quantidade que a casa vai colocar>"
            description = "Inicia um sorteio."

        class Restart(BaseDecorator, BaseClass):
            helper = "Reinicia o bot."
            usage = "Para usar: {}restart"
            description = "Reinicia o bot."

        class RGit(BaseDecorator, BaseClass):
            helper = "Puxa do git."
            usage = "Para usar: {}rgit"
            description = "Puxa do git."
