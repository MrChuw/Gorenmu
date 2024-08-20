# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from bot.translations import EnUsDecorators

if TYPE_CHECKING:
    from bot.ext.commands import Context



class PtBrDecorators(EnUsDecorators):
    class Afk(EnUsDecorators.Afk):
        class Afk(EnUsDecorators.Afk.Afk):
            helper = "Comando para entrar em um Status."
            usage = "Para usar: {}Afk <mensagem>"
            description = "Este comando define seu status como AFK."

        class IsAfk(EnUsDecorators.Afk.IsAfk):
            helper = "Digite o comando e o nome do usuário para saber se ele está AFK"
            usage = "Para usar: {}IsAfk <nome do usuário>"
            description = "Este comando define se um usuário está AFK ou não."

        class RAfk(EnUsDecorators.Afk.RAfk):
                helper = "Retorna a ficar AFK"
                usage = "Para usar: {}rafk"
                description = "Este comando é usado para retornar a ficar AFK."

    class Alias(EnUsDecorators.Alias):
        helper = "Comando usado para gerenciar os alias."
        usage = "Para usar: {}alias add|check|copy|describe|edit|link|remove|rename <opções>"
        description = "Comando usado para gerenciar os alias."

    class Chance(EnUsDecorators.Chance):
        helper = "Retorna uma percentagem aleatória."
        usage = "Para usar: {}chance"
        description = "Retorna uma percentagem aleatória."



    class Choice(EnUsDecorators.Choice):
        helper = "Escolhe uma opção das opções passadas pelo usuário"
        usage = "Para usar: {}choice <opção1> ou <opção2>"
        description = "Escolhe uma opção das opções passadas pelo usuário."

    class Count(EnUsDecorators.Count):
        helper = "Conta a quantidade de símbolos em um texto."
        usage = "Para usar: {}count <texto>"
        description = "Conta a quantidade de símbolos em um texto."

    class HyperTranslate(EnUsDecorators.HyperTranslate):
        helper = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer que "
                  "ele seja traduzido.")
        usage = "para usar: <prefixo>hypertranslate <quantidade de vezes que vai ser traduzido/número> <texto>"
        description = ("Traduz um texto para idiomas aleatórios dependendo da quantidade de vezes que você quer "
                       "que ele seja traduzido.")

    class Imgur(EnUsDecorators.Imgur):
        helper = "Envia um link aleatorio do imgur. (Pode vir NSFW)"
        usage = "para usar: <prefixo>imgur <quantidade>"
        description = "Envio um link aleatorio do imgur. (Pode vir NSFW)"

    class Imgur7(EnUsDecorators.Imgur7):
        helper = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                  "(Pode vir NSFW)")
        usage = "para usar: <prefixo>imgur <quantidade>"
        description = ("Envia um link aleatorio do imgur com 7 caracteres, e isso pode levar entre 5 minutos e 1h. "
                       "(Pode vir NSFW)")

    class ImgurRepeated(EnUsDecorators.ImgurRepeated):
        helper = "Verifica a quantidade de imgurs repetidos."
        usage = "Para usar: {}imgur_repetidos"
        description = "Verifica a quantidade de imgurs repetidos."

    class RandomColor(EnUsDecorators.RandomColor):
        helper = "Envia uma cor aleatória."
        usage = "Para usar: {}random_color"
        description = "Envia uma cor aleatória."

    class Reverse(EnUsDecorators.Reverse):
        helper = "Reverte um texto."
        usage = "Para usar: {}reverse <texto>"
        description = "Reverte um texto."

    class RandomLine(EnUsDecorators.RandomLine):
        helper = "Pega uma mensagem aleatória do canal ou do usuário no canal."
        usage = "para usar: `{0}rl --canal:<nome do canal>` ou `{0}rl --user:<nome do usuario>` ou `{0}rl`"
        description = "Pega uma mensagem aleatória do canal ou do usuário no canal."

    class Scp(EnUsDecorators.Scp):
        helper = "Envia um scp aleatório."
        usage = "Para usar: {}scp <quantidade>"
        description = "Envia um scp aleatório."

    class UpSideDown(EnUsDecorators.UpSideDown):
        helper = "Coloca o texto de cabeça para baixo."
        usage = "Para usar: {}upsidedown <texto>"
        description = "Coloca o texto de cabeça para baixo."

    class Wikihow(EnUsDecorators.Wikihow):
        helper = "Envia um link do wikihow aleatório."
        usage = "Para usar: {}wikihow <quantidade>"
        description = "Envia um link do wikihow aleatório."

    class Wikipedia(EnUsDecorators.Wikipedia):
            helper = "Envia um link da wikipedia aleatório."
            usage = "Para usar: {}wikipedia <quantidade>"
            description = "Envia um link da wikipedia aleatório."

    class Annotations(EnUsDecorators.Annotations):
        class Annotation(EnUsDecorators.Annotations.Annotation):
            helper = "Cria anotações permanentes para o usuário."
            usage = "Para usar: {}anotacao <anotação>"
            description = "Cria anotações permanentes para o usuário."

        class Annotations(EnUsDecorators.Annotations.Annotation):
            helper = "Lista anotações do usuário. Da mais recente para a mais antiga."
            usage = "Para usar: {}anotacoes"
            description = "Lista anotações do usuário. Da mais recente para a mais antiga."

    class Lottery(EnUsDecorators.Lottery):
        class Bet(EnUsDecorators.Lottery.Bet):
            helper = "use <prefixo>aposta <números que vc quer apostar>"
            usage = "Para usar: {}aposta <números que vc quer apostar>"
            description = "use <prefixo>aposta <números que vc quer apostar>"

        class Lottery(EnUsDecorators.Lottery.Lottery):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class NSFW(EnUsDecorators.NSFW):  # TODO: Fazer de novo.
        class Boru(EnUsDecorators.NSFW.Boru):
            helper = "Envia um ou mais links aleatório de uma lista de boorus."
            usage = "Para usar: {}booru <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais link aleatório de uma lista de boorus."

        class AllBoorus(EnUsDecorators.NSFW.AllBoorus):
            helper = "Envia um ou mais links aleatório de um site de booru específico."
            usage = "Para usar: {}sfbo <tags1> <tags2> <tags3> --<quantidade opcional>"
            description = "Envia um ou mais links aleatório de um site de booru específico."

    class Cookies(EnUsDecorators.Cookies):
        class Cookie(EnUsDecorators.Cookies.Cookie):
            helper = "coma um cookie e receba uma frase da sorte."
            usage = "Para usar: {}cookie <quantidade|1>"
            description = "coma um cookie e receba uma frase da sorte."

        class CookieCount(EnUsDecorators.Cookies.CookieCount):
            helper = "presenteie alguém com seu cookie diário"
            usage = "Para usar: {}gift <nome_do_usuário>"
            description = "presenteie alguém com seu cookie diário"

        class Gift(EnUsDecorators.Cookies.Gift):
            helper = "aposte seu cookie diário para ter a chance de ganhar outros"
            usage = (
                    "Para usar: {}slotmachine <all pode ser usado para apostar todos os cookies não resgatados rapidamente>")
            description = "aposte seu cookie diário para ter a chance de ganhar outros"

        class SlotMachine(EnUsDecorators.Cookies.SlotMachine):
            pass

        class Stock(EnUsDecorators.Cookies.Stock):
            helper = "estoque o seu cookie diário."
            usage = "Para usar: {}stock <all pode ser usado para stockar todos os cookies não resgatados rapidamente>"
            description = "estoque o seu cookie diário."

        class Top(EnUsDecorators.Cookies.Top):
            helper = "veja quais são os maiores comedores ou doadores de cookies"
            usage = "Para usar: {}top ou passes uma das opções stocked | streak | consumed | donated | received | total"
            description = "veja quais são os maiores comedores ou doadores de cookies"

    class Copy(EnUsDecorators.Copy):
        class Copy(EnUsDecorators.Copy.Copy):
            helper = "criar ou consultar uma copypasta."
            usage = "Para usar: {}copy <id da copypasta> ou <prefixo>copy <copypasta>"
            description = "criar ou consultar uma copypasta."

        class DeleteCopy(EnUsDecorators.Copy.DeleteCopy):
            helper = "deleta uma copypasta."
            usage = "Para usar: {}delcopy <delete> <copy_id da copypasta>"
            description = "deleta uma copypasta."

        class RandomCopy(EnUsDecorators.Copy.RandomCopy):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class Dungeons(EnUsDecorators.Dungeons):
        class DungeonLevel(EnUsDecorators.Dungeons.DungeonLevel):
            helper = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."
            usage = "Para usar: {}level <nome do usuário| author>."
            description = "veja qual o seu level (ou de alguém) e outras estatísticas da dungeon."

        class DungeonRank(EnUsDecorators.Dungeons.DungeonRank):
            helper = "saiba quais são os melhores jogadores da dungeon."
            usage = "Para usar: {}dungeonrank win | lose | winrate | warrior | mage | ranger"
            description = ""

        class DungeonEnter(EnUsDecorators.Dungeons.DungeonEnter):
            helper = ""
            usage = "Para usar: {}"
            description = ""

        class DungeonFast(EnUsDecorators.Dungeons.DungeonFast):
            helper = ""
            usage = "Para usar: {}"
            description = ""

    class General(EnUsDecorators.General):
        class BotInfo(EnUsDecorators.General.BotInfo):
            helper = "Veja as principais informações sobre o bot."
            usage = "Para usar: {0}botinfo ou {0}site ou {0}uptime"
            description = "Veja informações o bot, site, uptime."

        class Bug(EnUsDecorators.General.Bug):
            helper = "reporte um bug que está ocorrendo no Bot."
            usage = "Para usar: {}bug <mensagem>"
            description = "reporte um bug que está ocorrendo no Bot."

        class Channels(EnUsDecorators.General.Channels):
            helper = "Manda todos os canais conectados"
            usage = "Para usar: {}channels"
            description = "Manda todos os canais conectados"

        class Color(EnUsDecorators.General.Color):
            helper = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."
            usage = "Para usar: {}color <nick|hex>"
            description = "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick."

        class Dict(EnUsDecorators.General.Dict):
            helper = "Pesquisa a palavra no www.dicio.com.br"
            usage = "Para usar: {}dicio <palavra>"
            description = "Pesquisa a palavra no www.dicio.com.br"

        class Echo(EnUsDecorators.General.Echo):
            helper = "Retorna a mensagem enviada."
            usage = "Para usar: {}echo <mensagem>"
            description = "Retorna a mensagem enviada."

        class Help(EnUsDecorators.General.Help):
            helper = "Envia informações sobre os comandos."
            usage = "Para usar: {}help <nome_do_comando>"
            description = "Envia informações sobre os comandos."

        class Join(EnUsDecorators.General.Join):
            helper = "Comando para entrar no seu canal."
            usage = "Para usar: {}join"
            description = "Comando para entrar no seu canal."

        class LastSeen(EnUsDecorators.General.LastSeen):
            helper = "Mostra o último canal que o usuário usou."
            usage = "Para usar: {}lastseen <nome do usuário>"
            description = "Mostra o último canal que o usuário usou."

        class Leave(EnUsDecorators.General.Leave):
            helper = "Comando para sair do seu canal."
            usage = "Para usar: {}sair <seu nick>"
            description = "Comando para sair do seu canal."

        class Nicks(EnUsDecorators.General.Nicks):
            helper = "Histórico de nicks de um usuário."
            usage = "Para usar: {}nicks <nick do usuário>"
            description = "Histórico de nicks de um usuário."

        class Ping(EnUsDecorators.General.Ping):
            helper = "Verifica alguns status do bot."
            usage = "Para usar: {}ping"
            description = "Verifica alguns status do bot."

        class PopOut(EnUsDecorators.General.PopOut):
            helper = "Envia o link para o chat em popout de algum canal."
            usage = "Para usar: {}popout <nick do usuário>"
            description = "Envia o link para o chat em popout de algum canal."

        class Preview(EnUsDecorators.General.Preview):
            helper = "Envia um print do que está acontecendo na live."
            usage = "Para usar: {}preview <nick do usuário>"
            description = "Envia um print do que está acontecendo na live."

        class Spam(EnUsDecorators.General.Spam):
            helper = "Spam puro e simples. +spam 'quantidade' <mensagem>"
            usage = "Para usar: {}"
            description = "Spam puro e simples. +spam 'quantidade' <mensagem>"

        class Suggest(EnUsDecorators.General.Suggest):
            helper = "faça uma sugestão de recurso para o bot."
            usage = "Para usar: {}suggest <mensagem>"
            description = "faça uma sugestão de recurso para o bot."

    class Infos(EnUsDecorators.Infos):
        class AccountAge(EnUsDecorators.Infos.AccountAge):
            helper = "Mostra a idade da conta de um usuário."
            usage = "Para usar: {}accountage <nome do usuário>"
            description = "Mostra a idade da conta de um usuário."

        class Avatar(EnUsDecorators.Infos.Avatar):
            helper = "Mostra o avatar de um usuário."
            usage = "Para usar: {}avatar <nome do usuário>"
            description = "Mostra o avatar de um usuário."

        class FirstFollow(EnUsDecorators.Infos.FirstFollow):
            helper = "Mostra o primeiro seguidor da conta."
            usage = "Para usar: {}firstfollow <nome do usuário>"
            description = "Mostra o primeiro seguidor da conta."

        class FollowAge(EnUsDecorators.Infos.FollowAge):
            helper = "Mostra o tempo de follow da conta"
            usage = "Para usar: {}followage <nome do usuário> <nome do canal>"
            description = "Mostra o tempo de follow da conta"

        class Live(EnUsDecorators.Infos.Live):
            helper = "Mostra as informações de uma live."
            usage = "Para usar: {}live <nome do canal>"
            description = "Mostra as informações de uma live."

        class Title(EnUsDecorators.Infos.Title):
            helper = "Retorna apenas o título de uma stream."
            usage = "Para usar: {}title <nome do usuário>"
            description = "Retorna apenas o título de uma stream."

    class Interactive(EnUsDecorators.Interactive):
        class Fight(EnUsDecorators.Interactive.Fight):
            helper = "Desafie alguém para lutar."
            usage = "Para usar: {}fight <usuário>"
            description = "Desafie alguém para lutar."

        class Hug(EnUsDecorators.Interactive.Hug):
            helper = "Dê um abraço em alguém do chat."
            usage = "Para usar: {}hug <usuário>"
            description = "Dê um abraço em alguém do chat."

        class Kiss(EnUsDecorators.Interactive.Kiss):
            helper = "Dê um beijinho em alguém do chat."
            usage = "Para usar: {}kiss <usuário>"
            description = "Dê um beijinho em alguém do chat."

        class Love(EnUsDecorators.Interactive.Love):
            helper = "Veja quanto de amor existe entre o ship de duas pessoas."
            usage = "Para usar: {}love <usuário 1> <usuário 2>"
            description = "Veja quanto de amor existe entre o ship de duas pessoas."

        class Pat(EnUsDecorators.Interactive.Pat):
            helper = "Faça carinho em alguém do chat."
            usage = "Para usar: {}pat <usuário>"
            description = "Faça carinho em alguém do chat."

        class Penis(EnUsDecorators.Interactive.Penis):
            helper = "é... é isso mesmo."
            usage = "Para usar: {}penis <usuário>"
            description = "é... é isso mesmo."

        class Slap(EnUsDecorators.Interactive.Slap):
            helper = "Dê um tapa em alguém do chat."
            usage = "Para usar: {}slap <usuário>"
            description = "Dê um tapa em alguém do chat."

        class Tuck(EnUsDecorators.Interactive.Tuck):
            helper = "Coloque alguém do chat na cama para dormir"
            usage = "Para usar: {}tuck <usuário>"
            description = "Coloque alguém do chat na cama para dormir"

    class Markov(EnUsDecorators.Markov):  # TODO: atualizar o site. ou atualizar automaticamente com os docs.
        class Markov(EnUsDecorators.Markov.Markov):
            helper = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"
            usage = "Para usar: {}Markov"
            description = "Por favor visite o site para mais informações: https://gorenmu.vercel.app/docs/Markov/markov"

    class Marry(EnUsDecorators.Marry):
        class Marry(EnUsDecorators.Marry.Marry):
            helper = "Case-se e seja feliz para sempre, mas isso custará cookies."
            usage = "Para usar: {}marry <usuário>"
            description = "Case-se e seja feliz para sempre, mas isso custará cookies."

        class Divorce(EnUsDecorators.Marry.Divorce):
            helper = "Divorcie-se da pessoa com quem você é casada."
            usage = "Para usar: {}divorce <usuário>"
            description = "Divorcie-se da pessoa com quem você é casada."

        class MarryAge(EnUsDecorators.Marry.MarryAge):
            helper = "Saiba há quanto tempo algum usuário está casado."
            usage = "Para usar: {}ma <usuário>"
            description = "Saiba há quanto tempo algum usuário está casado."

    class Pet(EnUsDecorators.Pet):
        class Pet(EnUsDecorators.Pet.Pet):
            helper = "Veja os pets de alguém."
            usage = "Para usar: {}pet <usuário>"
            description = "Veja os pets de alguém."

        class PetList(EnUsDecorators.Pet.PetList):
            helper = "Veja os pets disponíveis para adquirir no dia."
            usage = "Para usar: {}petlist"
            description = "Veja os pets disponíveis para adquirir no dia."

        class PetName(EnUsDecorators.Pet.PetName):
            helper = "Dê um nome para o seu pet."
            usage = "Para usar: {}petname <nome do pet>"
            description = "Dê um nome para o seu pet."

        class PetPat(EnUsDecorators.Pet.PetPat):
            helper = "Faça carinho nos seus pets."
            usage = "Para usar: {}petpat <nome do pat>"
            description = "Faça carinho nos seus pets."

        class PetSell(EnUsDecorators.Pet.PetSell):
            helper = "Devolva um pet em troca de parte da quantia que gastou."
            usage = "Para usar: {}"
            description = "Devolva um pet em troca de parte da quantia que gastou."

    class Profile(EnUsDecorators.Profile):
        class Mention(EnUsDecorators.Profile.Mention):
            helper = "Reativa as menções nos comandos."
            usage = "Para usar: {}mention"
            description = "Reativa as menções nos comandos."

        class NickName(EnUsDecorators.Profile.NickName):
            helper = "Mude o seu apelido."
            usage = "Para usar: {}nickname <apelido>"
            description = "Mude o seu apelido."

        class SaveCity(EnUsDecorators.Profile.SaveCity):
            helper = "Digite o comando e o nome da cidade que deseja salvar."
            usage = "Para usar: {}savecity <cidade>"
            description = "Digite o comando e o nome da cidade que deseja salvar."

        class SaveColor(EnUsDecorators.Profile.SaveColor):
            helper = "Salva um cor pra mais tarde."
            usage = "Para usar: {}savecolor <hex>"
            description = "Salva um cor pra mais tarde."

        class UnMention(EnUsDecorators.Profile.UnMention):
            helper = "Desativa as menções nos comandos."
            usage = "Para usar: {}unmention"
            description = "Desativa as menções nos comandos."

    class Reminder(EnUsDecorators.Reminder):
        class Remind(EnUsDecorators.Reminder.Remind):
            helper = ('Digite remind pessoa (ou me para você), é a "mensagem", e sera lembrado na proxima vez que '
                      "digitar no chat.")
            usage = "Para usar: {}remind <pessoa> in <tempo> <mensagem>"
            description = ('Digite remind pessoa (ou me para você), é a "mensagem", '
                           "e sera lembrado na proxima vez que digitar no chat.")

        class Reminds(EnUsDecorators.Reminder.Reminds):
            helper = "Mostra os lembretes que você tem."
            usage = "Para usar: {}reminds"
            description = "Mostra os lembretes que você tem."

    class Settings(EnUsDecorators.Settings):
        class BanWord(EnUsDecorators.Settings.BanWord):
            helper = "Usado para banir palavras que eu não possa dizer."
            usage = "Para usar: {}banword <termo>"
            description = "Usado para banir palavras que eu não possa dizer."

        class Disable(EnUsDecorators.Settings.Disable):
            helper = "Usado para desativar comandos."
            usage = "Para usar: {}disable <comando>"
            description = "Usado para desativar comandos."

        class Enable(EnUsDecorators.Settings.Enable):
            helper = "Usado para reativar comandos desativados."
            usage = "Para usar: {}enable <comando>"
            description = "Usado para reativar comandos desativados."

        class Prefix(EnUsDecorators.Settings.Prefix):
            helper = "Usado para mudar o prefixo do canal."
            usage = "Para usar: {}prefixo <prefixo>"
            description = "Usado para mudar o prefixo do canal."

        class Start(EnUsDecorators.Settings.Start):
            helper = "Usado para ligar o bot no canal."
            usage = "Para usar: {}start"
            description = "Usado para ligar o bot no canal."

        class Stop(EnUsDecorators.Settings.Stop):
            helper = "Usado para desligar o bot no canal."
            usage = "Para usar: {}stop"
            description = "Usado para desligar o bot no canal."

        class UnBanWord(EnUsDecorators.Settings.UnBanWord):
            helper = "Usado para desbanir palavras que eu não possa diz"
            usage = "Para usar: {}unbanword <termo>"
            description = "Usado para desbanir palavras que eu não possa diz"

    class Tools(EnUsDecorators.Tools):
        class Math(EnUsDecorators.Tools.Math):
            helper = "Digite o comando e uma operação matemática para eu resolvê-la."
            usage = "Para usar: {}math <expressão matemática>"
            description = "Digite o comando e uma operação matemática para eu resolvê-la."

        class Shorten(EnUsDecorators.Tools.Shorten):
            helper = "Encurta links usando o meu serviço de encurtar links."
            usage = "Para usar: {}shorten <links>"
            description = "Encurta links usando o meu serviço de encurtar links."

        class Time(EnUsDecorators.Tools.Time):
            helper = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                      "etc. Podendo converter para o passado ou para o futuro.")
            usage = "Para usar: {}tempo <formato para transformar ex: h> <formato que vai a ser transformando ex: 50h>"
            description = ("Converte unidades de tempo para outras unidades, exemplo dias em horas, segundos em dias, "
                           "etc. Podendo converter para o passado ou para o futuro.")

        class UserId(EnUsDecorators.Tools.UserId):
            helper = "Pega o user_id de um usuario ou o usuario pelo user_id."
            usage = "Para usar: {}userid <user_id> ou <prefixo>userid <nome do usuário>"
            description = "Pega o user_id de um usuario ou o usuario pelo user_id."

        class Weather(EnUsDecorators.Tools.Weather):
            helper = "Digite o comando e uma cidade para obter a previsão do tempo."
            usage = "Para usar: {}weather <localização>"
            description = "Digite o comando e uma cidade para obter a previsão do tempo."

    class Tower(EnUsDecorators.Tower):
        class EnterTower(EnUsDecorators.Tower.EnterTower):
            helper = "Tenta avançar no seu caminho ao topo da torre."
            usage = "Para usar: {}entertower"
            description = "Tenta avançar no seu caminho ao topo da torre."

        class FastTower(EnUsDecorators.Tower.FastTower):
            helper = "Opção para limpar um andar da torre de maneira rápida."
            usage = "Para usar: {}fasttower"
            description = "Opção para limpar um andar da torre de maneira rápida."

        class TowerLevel(EnUsDecorators.Tower.TowerLevel):
            helper = "Mostra o nível atual da torre."
            usage = "Para usar: {}towerlevel"
            description = "Mostra o nível atual da torre."



    class Admin(EnUsDecorators.Admin):
        class AddUser(EnUsDecorators.Admin.AddUser):
            helper = "Adiciona um usuário"
            usage = "Para usar: {}add_user <nome do usuário>"
            description = "Este comando adiciona um usuário no banco de dados."

        class AddBot(EnUsDecorators.Admin.AddBot):
            helper = "Adiciona um bot"
            usage = "Para usar: {}addbot <nick do bot>"
            description = ("Usado para retirar os bots de serem comutados pelo Markov de canais. (ja que "
                           "não tem nenhuma forma de eu filtrar o bot sem ter que excluir ele totalmente da tabela.)")

        class AllChannels(EnUsDecorators.Admin.AllChannels):
            helper = "Mostra todos os canais que o bot está."
            usage = "Para usar: {}all_channels"
            description = "Mostra todos os canais que o bot está."

        class Announce(EnUsDecorators.Admin.Announce):
            helper = "Anuncia em todos os canais ou em um canal especifico."
            usage = "Para usar: {}anunciar <all ou nome do canal> <conteudo>"
            description = "Anuncia em todos os canais ou em um canal especifico."

        class ApiBot(EnUsDecorators.Admin.ApiBot):
            helper = "Adiciona bots de uma api que eu achei por ai."
            usage = "Para usar: {}apibot"
            description = "Adiciona bots de uma api que eu achei por ai."

        class ChannelLog(EnUsDecorators.Admin.ChannelLog):
            helper = "Faz o bot entrar em um canal para dar log nas mensagens."
            usage = "Para usar: {}channel_log <nome do canal> <entrar ou sair>"
            description = "Faz o bot entrar em um canal para dar log nas mensagens."

        class CookieGive(EnUsDecorators.Admin.CookieGive):
            helper = "Permite alguém que têm role de developer dar cookies para alguém."
            usage = "Para usar: {}cookie_give <nome do usuário> <quantidade>"
            description = "Permite alguém que têm role de developer dar cookies para alguém."

        class CountUser(EnUsDecorators.Admin.CountUser):
            helper = "Conta quantos usuários tem no banco de dados."
            usage = "Para usar: {}count_user"
            description = "Conta quantos usuários tem no banco de dados."

        class DBGrep(EnUsDecorators.Admin.DBGrep):
            helper = "Pegá as infos de um usuário ou canal."
            usage = "Para usar: {}dbgrep <texto>"
            description = "Pegá as infos de um usuário ou canal."

        class DelFromDB(EnUsDecorators.Admin.DelFromDB):
            helper = "Deleta um usuário ou todos os usuários de um canal."
            usage = "Para usar: {}del_from_db <user ou users_canal> <nome do usuário>"
            description = "Deleta um usuário ou todos os usuários de um canal."

        class DisableNSFW(EnUsDecorators.Admin.DisableNSFW):
            helper = "Desabilita o NSFW em todos os canais."
            usage = "Para usar: {}disable_nsfw"
            description = "Desabilita o NSFW em todos os canais."

        class LotteryStart(EnUsDecorators.Admin.LotteryStart):
            helper = "Inicia um sorteio."
            usage = "Para usar: {}lottery_start <tempo ate o final da loteria> <quantidade que a casa vai colocar>"
            description = "Inicia um sorteio."

        class Nada(EnUsDecorators.Admin.Nada):
            helper = "Nada."
            usage = "Para usar: {}nada <texto>"
            description = "Nada."

        class Reload(EnUsDecorators.Admin.Reload):
            helper = "Recarrega os comandos."
            usage = "Para usar: {}reload"
            description = "Recarrega os comandos."

        class Restart(EnUsDecorators.Admin.Restart):
            helper = "Reinicia o bot."
            usage = "Para usar: {}restart"
            description = "Reinicia o bot."

        class RGit(EnUsDecorators.Admin.RGit):
            helper = "Puxa do git."
            usage = "Para usar: {}rgit"
            description = "Puxa do git."
