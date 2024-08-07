# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from twitchio.ext.commands import Command, Context as TwitchioContext

if TYPE_CHECKING:
    from bot.ext.commands import Context


class BaseDecorator:
    helper: str
    usage: str
    description: str


class EnUsDecorators:
    @staticmethod
    def get_decorator(source: Context | Command, ctx: Context) -> BaseDecorator | None:
        decorators = None
        if isinstance(source, TwitchioContext):
            decorators = source.command.decorators
        elif isinstance(source, Command):
            decorators = source.decorators

        for classe in dir(EnUsDecorators):
            for attr_name in dir(getattr(EnUsDecorators, classe)):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(getattr(EnUsDecorators, classe), attr_name)
                if isinstance(decorators, attr):
                    decorator_class = getattr(
                        ctx.bot.TranslationManager.get_decorator(ctx.user.language or "pt-br"),
                        classe,
                        None,
                    )
                    if decorator_class:
                        decorator_class = getattr(decorator_class, attr_name)
                        return decorator_class()
        return None

    @staticmethod
    def get_helper(source: Context | Command, ctx: Context, prefix: str) -> str:
        return EnUsDecorators.get_decorator(source, ctx).helper.format(prefix)

    @staticmethod
    def get_usage(source: Context | Command, ctx: Context) -> str:
        return EnUsDecorators.get_decorator(source, ctx).usage.format(ctx.prefix)

    @staticmethod
    def get_description(source: Context | Command, ctx: Context) -> str:
        return EnUsDecorators.get_decorator(source, ctx).description

    class IDE:
        class TypeChecking(BaseDecorator):
            pass
    
    class Activity:
        class Afk(BaseDecorator):
            helper = "Comando para entrar em um Status."
            usage = "Para usar: {}Afk <mensagem>"
            description = "Este comando define seu status como AFK."

        class IsAfk(BaseDecorator):
            helper = "Digite o comando e o nome do usuário para saber se ele está AFK"
            usage = "Para usar: {}IsAfk <nome do usuário>"
            description = "Este comando define se um usuário está AFK ou não."

        class RAfk(BaseDecorator):
            helper = "Retorna a ficar AFK"
            usage = "Para usar: {}rafk"
            description = "Este comando é usado para retornar a ficar AFK."

    class Admin:
        class AddUser(BaseDecorator):
            helper = "Adiciona um usuário"
            usage = "Para usar: {}add_user <nome do usuário>"
            description = "Este comando adiciona um usuário no banco de dados."

        class AddBot(BaseDecorator):
            helper = "Adiciona um bot"
            usage = "Para usar: {}addbot <nick do bot>"
            description = ("Usado para retirar os bots de serem comutados pelo Markov de canais. (ja que "
                           "não tem nenhuma forma de eu filtrar o bot sem ter que excluir ele totalmente da tabela.)")

        class AllChannels(BaseDecorator):
            helper = "Mostra todos os canais que o bot está."
            usage = "Para usar: {}all_channels"
            description = "Mostra todos os canais que o bot está."

        class Announce(BaseDecorator):
            helper = "Anuncia em todos os canais ou em um canal especifico."
            usage = "Para usar: {}anunciar <all ou nome do canal> <conteudo>"
            description = "Anuncia em todos os canais ou em um canal especifico."

        class ApiBot(BaseDecorator):
            helper = "Adiciona bots de uma api que eu achei por ai."
            usage = "Para usar: {}apibot"
            description = "Adiciona bots de uma api que eu achei por ai."

        class ChannelLog(BaseDecorator):
            helper = "Faz o bot entrar em um canal para dar log nas mensagens."
            usage = "Para usar: {}channel_log <nome do canal> <entrar ou sair>"
            description = "Faz o bot entrar em um canal para dar log nas mensagens."

        class CookieGive(BaseDecorator):
            helper = "Permite alguém que têm role de developer dar cookies para alguém."
            usage = "Para usar: {}cookie_give <nome do usuário> <quantidade>"
            description = "Permite alguém que têm role de developer dar cookies para alguém."

        class CountUser(BaseDecorator):
            helper = "Conta quantos usuários tem no banco de dados."
            usage = "Para usar: {}count_user"
            description = "Conta quantos usuários tem no banco de dados."

        class DBGrep(BaseDecorator):
            helper = "Pegá as infos de um usuário ou canal."
            usage = "Para usar: {}dbgrep <texto>"
            description = "Pegá as infos de um usuário ou canal."

        class DelFromDB(BaseDecorator):
            helper = "Deleta um usuário ou todos os usuários de um canal."
            usage = "Para usar: {}del_from_db <user ou users_canal> <nome do usuário>"
            description = "Deleta um usuário ou todos os usuários de um canal."

        class DisableNSFW(BaseDecorator):
            helper = "Desabilita o NSFW em todos os canais."
            usage = "Para usar: {}disable_nsfw"
            description = "Desabilita o NSFW em todos os canais."

        class LotteryStart(BaseDecorator):
            helper = "Inicia um sorteio."
            usage = "Para usar: {}lottery_start <tempo ate o final da loteria> <quantidade que a casa vai colocar>"
            description = "Inicia um sorteio."

        class Nada(BaseDecorator):
            helper = "Nada."
            usage = "Para usar: {}nada"
            description = "Nada."

        class Reload(BaseDecorator):
            helper = "Recarrega os comandos."
            usage = "Para usar: {}reload"
            description = "Recarrega os comandos."

        class Restart(BaseDecorator):
            helper = "Reinicia o bot."
            usage = "Para usar: {}restart"
            description = "Reinicia o bot."

        class RGit(BaseDecorator):
            helper = "Puxa do git."
            usage = "Para usar: {}rgit"
            description = "Puxa do git."

    class Random:
        class Chance(BaseDecorator):
            helper = "Chance."
            usage = "Para usar: {}chance"
            description = "Chance."

        class Choice(BaseDecorator):
            helper = "Escolhe uma opção das opções passadas pelo usuário"
            usage = "Para usar: {}choice <opção1> ou <opção2>"
            description = "Escolhe uma opção das opções passadas pelo usuário."

        class Count(BaseDecorator):
            helper = "Conta a quantidade de símbolos em um texto."
            usage = "Para usar: {}count <texto>"
            description = "Conta a quantidade de símbolos em um texto."

        class HyperTranslate(BaseDecorator):
            helper = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer que "
                      "ele seja traduzido.")
            usage = "para usar: <prefixo>hypertranslate <quantidade de vezes que vai ser traduzido/número> <texto>"
            description = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer "
                           "que ele seja traduzido.")

        class Imgur(BaseDecorator):
            helper = "Envia um link aleatorio do imgur. (Pode vir NSFW)"
            usage = "para usar: <prefixo>imgur <quantidade>"
            description = "Envio um link aleatorio do imgur. (Pode vir NSFW)"

        class Imgur7(BaseDecorator):
            helper = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                      "(Pode vir NSFW)")
            usage = "para usar: <prefixo>imgur <quantidade>"
            description = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                           "(Pode vir NSFW)")

        class ImgurRepeated(BaseDecorator):
            helper = "Verifica a quantidade de imgurs repetidos."
            usage = "Para usar: {}imgur_repetidos"
            description = "Verifica a quantidade de imgurs repetidos."

        class RandomColor(BaseDecorator):
            helper = "Envia uma cor aleatória."
            usage = "Para usar: {}random_color"
            description = "Envia uma cor aleatória."

        class Reverse(BaseDecorator):
            helper = "Reverte um texto."
            usage = "Para usar: {}reverse <texto>"
            description = "Reverte um texto."

        class RandomLine(BaseDecorator):
            helper = "Pega uma mensagem aleatória do canal ou do usuário no canal."
            usage = "para usar: `{0}rl --canal:<nome do canal>` ou `{0}rl --user:<nome do usuario>` ou `{0}rl`"
            description = "Pega uma mensagem aleatória do canal ou do usuário no canal."

        class Scp(BaseDecorator):
            helper = "Envia um scp aleatório."
            usage = "Para usar: {}scp <quantidade>"
            description = "Envia um scp aleatório."

        class UpSideDown(BaseDecorator):
            helper = "Coloca o texto de cabeça para baixo."
            usage = "Para usar: {}upsidedown <texto>"
            description = "Coloca o texto de cabeça para baixo."

        class Wikihow(BaseDecorator):
            helper = "Envia um link do wikihow aleatório."
            usage = "Para usar: {}wikihow <quantidade>"
            description = "Envia um link do wikihow aleatório."

        class Wikipedia(BaseDecorator):
            helper = "Envia um link da wikipedia aleatório."
            usage = "Para usar: {}wikipedia <quantidade>"
            description = "Envia um link da wikipedia aleatório."

    class Annotations:
        class Annotation(BaseDecorator):
            helper = "Cria anotações permanentes para o usuário."
            usage = "Para usar: {}anotacao <anotação>"
            description = "Cria anotações permanentes para o usuário."

        class Annotations(BaseDecorator):
            helper = "Lista anotações do usuário. Da mais recente para a mais antiga."
            usage = "Para usar: {}anotacoes"
            description = "Lista anotações do usuário. Da mais recente para a mais antiga."

    class Lottery:
        class Bet(BaseDecorator):
            helper = "use <prefixo>aposta <números que vc quer apostar>"
            usage = "Para usar: {}aposta <números que vc quer apostar>"
            description = "use <prefixo>aposta <números que vc quer apostar>"

        class Lottery(BaseDecorator):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class NSFW:  # TODO: Fazer de novo.
        class Boru(BaseDecorator):
            helper = "Envia um ou mais links aleatório de uma lista de boorus."
            usage = "Para usar: {}booru <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais link aleatório de uma lista de boorus."

        class AllBoorus(BaseDecorator):
            helper = "Envia um ou mais links aleatório de um site de booru específico."
            usage = "Para usar: {}sfbo <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais links aleatório de um site de booru específico."

    class Cookies:
        class Cookie(BaseDecorator):
            helper = "coma um cookie e receba uma frase da sorte."
            usage = "Para usar: {}cookie <quantidade|1>"
            description = "coma um cookie e receba uma frase da sorte."

        class CookieCount(BaseDecorator):
            helper = "presenteie alguém com seu cookie diário"
            usage = "Para usar: {}gift <nome_do_usuário>"
            description = "presenteie alguém com seu cookie diário"

        class Gift(BaseDecorator):
            helper = "aposte seu cookie diário para ter a chance de ganhar outros"
            usage = (
                    "Para usar: {}slotmachine <all pode ser usado para apostar todos os cookies não resgatados rapidamente>")
            description = "aposte seu cookie diário para ter a chance de ganhar outros"

        class SlotMachine(BaseDecorator):
            pass

        class Stock(BaseDecorator):
            helper = "estoque o seu cookie diário."
            usage = "Para usar: {}stock <all pode ser usado para stockar todos os cookies não resgatados rapidamente>"
            description = "estoque o seu cookie diário."

        class Top(BaseDecorator):
            helper = "veja quais são os maiores comedores ou doadores de cookies"
            usage = "Para usar: {}top ou passes uma das opções stocked | streak | consumed | donated | received | total"
            description = "veja quais são os maiores comedores ou doadores de cookies"

    class Copy:
        class Copy(BaseDecorator):
            helper = "criar ou consultar uma copypasta."
            usage = "Para usar: {}copy <id da copypasta> ou <prefixo>copy <copypasta>"
            description = "criar ou consultar uma copypasta."

        class DeleteCopy(BaseDecorator):
            helper = "deleta uma copypasta."
            usage = "Para usar: {}delcopy <delete> <copy_id da copypasta>"
            description = "deleta uma copypasta."

        class RandomCopy(BaseDecorator):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class Dungeons:
        class DungeonLevel(BaseDecorator):
            helper = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."
            usage = "Para usar: {}level <nome do usuário| author>."
            description = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."

        class DungeonRank(BaseDecorator):
            helper = "saiba quais são os melhores jogadores da dungeon."
            usage = "Para usar: {}dungeonrank win | lose | winrate | warrior | mage | ranger"
            description = ""

        class DungeonEnter(BaseDecorator):
            helper = ""
            usage = "Para usar: {}"
            description = ""

        class DungeonFast(BaseDecorator):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class General:
        class BotInfo(BaseDecorator):
            helper = "Veja as principais informações sobre o bot."
            usage = "Para usar: {0}botinfo ou {0}site ou {0}uptime"
            description = "Veja informações o bot, site, uptime."

        class Bug(BaseDecorator):
            helper = "reporte um bug que está ocorrendo no Bot."
            usage = "Para usar: {}bug <mensagem>"
            description = "reporte um bug que está ocorrendo no Bot."

        class Channels(BaseDecorator):
            helper = "Manda todos os canais conectados"
            usage = "Para usar: {}channels"
            description = "Manda todos os canais conectados"

        class Color(BaseDecorator):
            helper = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."
            usage = "Para usar: {}color <nick|hex>"
            description = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."

        class Dict(BaseDecorator):
            helper = "Pesquisa a palavra no www.dicio.com.br"
            usage = "Para usar: {}dicio <palavra>"
            description = "Pesquisa a palavra no www.dicio.com.br"

        class Echo(BaseDecorator):
            helper = "Retorna a mensagem enviada."
            usage = "Para usar: {}echo <mensagem>"
            description = "Retorna a mensagem enviada."

        class Help(BaseDecorator):
            helper = "Envia informações sobre os comandos."
            usage = "Para usar: {}help <nome_do_comando>"
            description = "Envia informações sobre os comandos."

        class Join(BaseDecorator):
            helper = "Comando para entrar no seu canal."
            usage = "Para usar: {}join"
            description = "Comando para entrar no seu canal."

        class LastSeen(BaseDecorator):
            helper = "Mostra o último canal que o usuário usou."
            usage = "Para usar: {}lastseen <nome do usuário>"
            description = "Mostra o último canal que o usuário usou."

        class Leave(BaseDecorator):
            helper = "Comando para sair do seu canal."
            usage = "Para usar: {}sair <seu nick>"
            description = "Comando para sair do seu canal."

        class Nicks(BaseDecorator):
            helper = "Histórico de nicks de um usuário."
            usage = "Para usar: {}nicks <nick do usuário>"
            description = "Histórico de nicks de um usuário."

        class Ping(BaseDecorator):
            helper = "Verifica alguns status do bot."
            usage = "Para usar: {}ping"
            description = "Verifica alguns status do bot."

        class PopOut(BaseDecorator):
            helper = "Envia o link para o chat em popout de algum canal."
            usage = "Para usar: {}popout <nick do usuário>"
            description = "Envia o link para o chat em popout de algum canal."

        class Preview(BaseDecorator):
            helper = "Envia um print do que está acontecendo na live."
            usage = "Para usar: {}preview <nick do usuário>"
            description = "Envia um print do que está acontecendo na live."

        class Spam(BaseDecorator):
            helper = "Spam puro e simples. +spam 'quantidade' <mensagem>"
            usage = "Para usar: {}"
            description = "Spam puro e simples. +spam 'quantidade' <mensagem>"

        class Suggest(BaseDecorator):
            helper = "faça uma sugestão de recurso para o bot."
            usage = "Para usar: {}suggest <mensagem>"
            description = "faça uma sugestão de recurso para o bot."

    class Infos:
        class AccountAge(BaseDecorator):
            helper = "Mostra a idade da conta de um usuário."
            usage = "Para usar: {}accountage <nome do usuário>"
            description = "Mostra a idade da conta de um usuário."

        class Avatar(BaseDecorator):
            helper = "Mostra o avatar de um usuário."
            usage = "Para usar: {}avatar <nome do usuário>"
            description = "Mostra o avatar de um usuário."

        class FirstFollow(BaseDecorator):
            helper = "Mostra o primeiro seguidor da conta."
            usage = "Para usar: {}firstfollow <nome do usuário>"
            description = "Mostra o primeiro seguidor da conta."

        class FollowAge(BaseDecorator):
            helper = "Mostra o tempo de follow da conta"
            usage = "Para usar: {}followage <nome do usuário> <nome do canal>"
            description = "Mostra o tempo de follow da conta"

        class Live(BaseDecorator):
            helper = "Mostra as informações de uma live."
            usage = "Para usar: {}live <nome do canal>"
            description = "Mostra as informações de uma live."

        class Title(BaseDecorator):
            helper = "Retorna apenas o título de uma stream."
            usage = "Para usar: {}title <nome do usuário>"
            description = "Retorna apenas o título de uma stream."

    class Interactive:
        class Fight(BaseDecorator):
            helper = "Desafie alguém para lutar."
            usage = "Para usar: {}fight <usuário>"
            description = "Desafie alguém para lutar."

        class Hug(BaseDecorator):
            helper = "Dê um abraço em alguém do chat."
            usage = "Para usar: {}hug <usuário>"
            description = "Dê um abraço em alguém do chat."

        class Kiss(BaseDecorator):
            helper = "Dê um beijinho em alguém do chat."
            usage = "Para usar: {}kiss <usuário>"
            description = "Dê um beijinho em alguém do chat."

        class Love(BaseDecorator):
            helper = "Veja quanto de amor existe entre o ship de duas pessoas."
            usage = "Para usar: {}love <usuário 1> <usuário 2>"
            description = "Veja quanto de amor existe entre o ship de duas pessoas."

        class Pat(BaseDecorator):
            helper = "Faça carinho em alguém do chat."
            usage = "Para usar: {}pat <usuário>"
            description = "Faça carinho em alguém do chat."

        class Penis(BaseDecorator):
            helper = "é... é isso mesmo."
            usage = "Para usar: {}penis <usuário>"
            description = "é... é isso mesmo."

        class Slap(BaseDecorator):
            helper = "Dê um tapa em alguém do chat."
            usage = "Para usar: {}slap <usuário>"
            description = "Dê um tapa em alguém do chat."

        class Tuck(BaseDecorator):
            helper = "Coloque alguém do chat na cama para dormir"
            usage = "Para usar: {}tuck <usuário>"
            description = "Coloque alguém do chat na cama para dormir"

    class Markov:  # TODO: atualizar o site. ou atualizar automaticamente com os docs.
        class Markov(BaseDecorator):
            helper = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"
            usage = "Para usar: {}Markov"
            description = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"

    class Marry:
        class Marry(BaseDecorator):
            helper = "Case-se e seja feliz para sempre, mas isso custará cookies."
            usage = "Para usar: {}marry <usuário>"
            description = "Case-se e seja feliz para sempre, mas isso custará cookies."

        class Divorce(BaseDecorator):
            helper = "Divorcie-se da pessoa com quem você é casada."
            usage = "Para usar: {}divorce <usuário>"
            description = "Divorcie-se da pessoa com quem você é casada."

        class MarryAge(BaseDecorator):
            helper = "Saiba há quanto tempo algum usuário está casado."
            usage = "Para usar: {}ma <usuário>"
            description = "Saiba há quanto tempo algum usuário está casado."

    class Pet:
        class Pet(BaseDecorator):
            helper = "Veja os pets de alguém."
            usage = "Para usar: {}pet <usuário>"
            description = "Veja os pets de alguém."

        class PetList(BaseDecorator):
            helper = "Veja os pets disponíveis para adquirir no dia."
            usage = "Para usar: {}petlist"
            description = "Veja os pets disponíveis para adquirir no dia."

        class PetName(BaseDecorator):
            helper = "Dê um nome para o seu pet."
            usage = "Para usar: {}petname <nome do pet>"
            description = "Dê um nome para o seu pet."

        class PetPat(BaseDecorator):
            helper = "Faça carinho nos seus pets."
            usage = "Para usar: {}petpat <nome do pat>"
            description = "Faça carinho nos seus pets."

        class PetSell(BaseDecorator):
            helper = "Devolva um pet em troca de parte da quantia que gastou."
            usage = "Para usar: {}"
            description = "Devolva um pet em troca de parte da quantia que gastou."

    class Profile:
        class Mention(BaseDecorator):
            helper = "Reativa as menções nos comandos."
            usage = "Para usar: {}mention"
            description = "Reativa as menções nos comandos."

        class NickName(BaseDecorator):
            helper = "Mude o seu apelido."
            usage = "Para usar: {}nickname <apelido>"
            description = "Mude o seu apelido."

        class SaveCity(BaseDecorator):
            helper = "Digite o comando e o nome da cidade que deseja salvar."
            usage = "Para usar: {}savecity <cidade>"
            description = "Digite o comando e o nome da cidade que deseja salvar."

        class SaveColor(BaseDecorator):
            helper = "Salva um cor pra mais tarde."
            usage = "Para usar: {}savecolor <hex>"
            description = "Salva um cor pra mais tarde."

        class UnMention(BaseDecorator):
            helper = "Desativa as menções nos comandos."
            usage = "Para usar: {}unmention"
            description = "Desativa as menções nos comandos."

    class Reminder:
        class Remind(BaseDecorator):
            helper = ('Digite remind pessoa (ou me para você), é a "mensagem", e sera lembrado na proxima vez que '
                      "digitar no chat.")
            usage = "Para usar: {}remind <pessoa> in <tempo> <mensagem>"
            description = ('Digite remind pessoa (ou me para você), é a "mensagem", '
                           "e sera lembrado na proxima vez que digitar no chat.")

        class Reminds(BaseDecorator):
            helper = "Mostra os lembretes que você tem."
            usage = "Para usar: {}reminds"
            description = "Mostra os lembretes que você tem."

    class Settings:
        class BanWord(BaseDecorator):
            helper = "Usado para banir palavras que eu não possa dizer."
            usage = "Para usar: {}banword <termo>"
            description = "Usado para banir palavras que eu não possa dizer."

        class Disable(BaseDecorator):
            helper = "Usado para desativar comandos."
            usage = "Para usar: {}disable <comando>"
            description = "Usado para desativar comandos."

        class Enable(BaseDecorator):
            helper = "Usado para reativar comandos desativados."
            usage = "Para usar: {}enable <comando>"
            description = "Usado para reativar comandos desativados."

        class Prefix(BaseDecorator):
            helper = "Usado para mudar o prefixo do canal."
            usage = "Para usar: {}prefixo <prefixo>"
            description = "Usado para mudar o prefixo do canal."

        class Start(BaseDecorator):
            helper = "Usado para ligar o bot no canal."
            usage = "Para usar: {}start"
            description = "Usado para ligar o bot no canal."

        class Stop(BaseDecorator):
            helper = "Usado para desligar o bot no canal."
            usage = "Para usar: {}stop"
            description = "Usado para desligar o bot no canal."

        class UnBanWord(BaseDecorator):
            helper = "Usado para desbanir palavras que eu não possa diz"
            usage = "Para usar: {}unbanword <termo>"
            description = "Usado para desbanir palavras que eu não possa diz"

    class Tools:
        class Math(BaseDecorator):
            helper = "Digite o comando e uma operação matemática para eu resolvê-la."
            usage = "Para usar: {}math <expressão matemática>"
            description = "Digite o comando e uma operação matemática para eu resolvê-la."

        class Shorten(BaseDecorator):
            helper = "Encurta links usando o meu serviço de encurtar links."
            usage = "Para usar: {}shorten <links>"
            description = "Encurta links usando o meu serviço de encurtar links."

        class Time(BaseDecorator):
            helper = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                      "etc. Podendo converter para o passado ou para o futuro.")
            usage = "Para usar: {}tempo <formato para transformar ex: h> <formato que vai a ser transformando ex: 50h>"
            description = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                           "etc. Podendo converter para o passado ou para o futuro.")

        class UserId(BaseDecorator):
            helper = "Pega o user_id de um usuario ou o usuario pelo user_id."
            usage = "Para usar: {}userid <user_id> ou <prefixo>userid <nome do usuário>"
            description = "Pega o user_id de um usuario ou o usuario pelo user_id."

        class Weather(BaseDecorator):
            helper = "Digite o comando e uma cidade para obter a previsão do tempo."
            usage = "Para usar: {}weather <localização>"
            description = "Digite o comando e uma cidade para obter a previsão do tempo."

    class Tower:
        class EnterTower(BaseDecorator):
            helper = "Tenta avançar no seu caminho ao topo da torre."
            usage = "Para usar: {}entertower"
            description = "Tenta avançar no seu caminho ao topo da torre."

        class FastTower(BaseDecorator):
            helper = "Opção para limpar um andar da torre de maneira rápida."
            usage = "Para usar: {}fasttower"
            description = "Opção para limpar um andar da torre de maneira rápida."

        class TowerLevel(BaseDecorator):
            helper = "Mostra o nível atual da torre."
            usage = "Para usar: {}towerlevel"
            description = "Mostra o nível atual da torre."
