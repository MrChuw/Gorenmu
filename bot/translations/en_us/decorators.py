# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from twitchio.ext.commands import Bucket

if TYPE_CHECKING:
    from bot.ext.commands import Context


class BaseDecorator:
    helper: str
    usage: str
    description: str
    dynamic_description: dict[str, str]


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


class EnUsDecorators:
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

    class IDE:
        class TypeChecking(BaseDecorator, BaseClass):
            pass

    class Afk(BaseClass):
        class Afk(BaseDecorator, BaseClass):
            helper = "Command to set your status."
            usage = "How to use: {}Afk <message>"
            description = "This command sets your status to AFK."
            dynamic_description = {
                    "title_part1": "This command can be used",
                    "title_part2": "again after the cooldown of",
                    "title_part3": "for",
                    "usage_title": "Usages:",
                    "response_afk": "User, you went AFK: 🏃 ⌨️",
                    "usage_title_content": "Using with text.",
                    "usage_content": "Text you want to leave for when you return or that people will see when they use {}isafk.",
                    "usage_response_afk_with_content": "User, you went AFK: 🏃 ⌨️ and left a note with: "
            }

        class IsAfk(BaseDecorator, BaseClass):
            helper = "Type the command and the username to check if they are AFK."
            usage = "To use: {}IsAfk <username>"
            description = "This command checks if a user is AFK or not."

        class RAfk(BaseDecorator, BaseClass):
            helper = "Return to AFK status."
            usage = "To use: {}rafk"
            description = "This command is used to return to AFK status."

    class Alias(BaseDecorator, BaseClass):
        helper = "Command used to manage aliases."
        usage = "To use: {}alias add|check|copy|describe|edit|link|remove|rename <options>"
        description = "Command used to manage aliases."

    class Chance(BaseDecorator, BaseClass):
        helper = "Returns a random percentage."
        usage = "To use: {}chance"
        description = "Returns a random percentage."

    class Choice(BaseDecorator, BaseClass):
        helper = "Chooses an option from the options provided by the user."
        usage = "To use: {}choice <option1> or <option2>"
        description = "Chooses an option from the options provided by the user."

    class Count(BaseDecorator, BaseClass):
        helper = "Counts the number of symbols in a text or a URL."
        usage = "To use: {}count <text> or type:url <as many URLs as you want>"
        description = "Counts the number of symbols in a text."

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



    class Admin(BaseClass):
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

        class Nada(BaseDecorator, BaseClass):
            helper = "Nada."
            usage = "Para usar: {}nada asfasfasfasfasdfasf"
            description = "Nada."

        class Reload(BaseDecorator, BaseClass):
            helper = "Recarrega os comandos."
            usage = "Para usar: {}reload"
            description = "Recarrega os comandos."

        class Restart(BaseDecorator, BaseClass):
            helper = "Reinicia o bot."
            usage = "Para usar: {}restart"
            description = "Reinicia o bot."

        class RGit(BaseDecorator, BaseClass):
            helper = "Puxa do git."
            usage = "Para usar: {}rgit"
            description = "Puxa do git."
