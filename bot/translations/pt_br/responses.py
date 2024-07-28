from __future__ import annotations

from typing import Any, TYPE_CHECKING

from bot.translations.base import BaseTranslations, Response
from bot.translations.pt_br.extras.weather import WeatherTools
from bot.translations.pt_br.extras.pets import from_list_to_pet_list, pets, PetsDict
from bot.translations.pt_br.extras.games import fight_option
from bot.translations.pt_br.extras.dungeon import dungeon_rank_dict
from bot.translations.pt_br.extras.activity import Activity as ActivityExtras

if TYPE_CHECKING:
    from ext.commands import Context


# TODO: Colocar o pipeble false nos comandos que não podem ir para o pipe.
# TODO: adicionar um fallback para o idioma padrão caso não tenha a tradução.


class PtBrTranslations:
    class Activity(BaseTranslations.Activity):
        afks: dict[str, ActivityExtras.Status] = ActivityExtras.afks

        class Afk(BaseTranslations.Activity.Afk):
            message_too_long: Response = Response(
                {"success": False, "response": "Esta mensagem é muito longa.", "is_response": False}
            )
            afk_response: Response = Response({"success": True, "response": "{}: {}", "is_response": False})
            afk_content_response: Response = Response(
                {"success": True, "response": "{}: {} e deixou uma nota com: {}", "is_response": False}
            )

        class IsAfk(BaseTranslations.Activity.IsAfk):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sempre estou aqui... observando.", "is_response": False}
            )
            author_nick: Response = Response(
                {"success": False, "response": "você não está trabalhando... obviamente", "is_response": False}
            )
            never_seen: Response = Response(
                {"success": False, "response": "não lembro de ja ter visto nenhum {}.", "is_response": False}
            )
            is_afk: Response = Response({"success": False, "response": "@{} {}: {}", "is_response": False})
            is_afk_content: Response = Response(
                {"success": False, "response": "@{} {} e deixou um bilhete: {}", "is_response": False}
            )
            is_not_afk: Response = Response({"success": False, "response": "@{} não está Afk.", "is_response": False})

        class RAfk(BaseTranslations.Activity.RAfk):
            time_expired: Response = Response(
                {"success": False, "response": "O tempo para voltar já passou.", "is_response": False}
            )
            is_afk: Response = Response({"success": False, "response": "{}: {}", "is_response": False})
            is_afk_content: Response = Response(
                {"success": False, "response": "{} {} e deixou um bilhete: {}", "is_response": False}
            )
            is_not_afk: Response = Response({"success": False, "response": "voce não está afk.", "is_response": False})

        class AfkListeners(BaseTranslations.Activity.AfkListeners):
            is_afk: Response = Response({"success": False, "response": "{}: {} (ficou {} {})", "is_response": False})
            is_afk_content: Response = Response(
                {"success": False, "response": "{} {} e deixou um bilhete: {} (ficou {} {})", "is_response": False}
            )

    class Admin(BaseTranslations.Admin):
        class AddUser(BaseTranslations.Admin.AddUser):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}.", "is_response": False}
            )
            user_response: Response = Response(
                {
                    "success": False,
                    "response": "as infos de {} foram adicionadas.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class AddBot(BaseTranslations.Admin.AddBot):
            user_not_found: Response = Response(
                {"success": False, "response": "eu ainda não vi esse bot em nenhum chat.", "is_response": False}
            )
            user_already_added: Response = Response(
                {"success": False, "response": "o bot {} ja esta registrado.", "is_response": False}
            )
            user_added: Response = Response(
                {"success": True, "response": "o bot {} foi adicionado aos bots.", "is_response": False}
            )

        class AllChannels(BaseTranslations.Admin.AllChannels):
            channels: Response = Response(
                {"success": False, "response": "aqui a lista de todos os canais que eu estou: {}", "is_response": False}
            )

        class Announce(BaseTranslations.Admin.Announce):
            success: Response = Response(
                {"success": False, "response": "O comando foi executado com sucesso.", "is_response": False}
            )

        class ApiBot(BaseTranslations.Admin.ApiBot):
            added_with_success: Response = Response(
                {
                    "success": False,
                    "response": "O comando foi executado com sucesso. Com {} bots adicionados.",
                    "is_response": False,
                }
            )

        class ChannelLog(BaseTranslations.Admin.ChannelLog):
            channel_already_added: Response = Response(
                {"success": False, "response": "Ja estou no canal {}.", "is_response": False}
            )
            channel_added: Response = Response(
                {"success": True, "response": "Entrei no canal {}.", "is_response": False}
            )

        class CookieGive(BaseTranslations.Admin.CookieGive):
            cookie_given: Response = Response(
                {"success": True, "response": "você deu {} para {}.", "is_response": False}
            )

        class CountUser(BaseTranslations.Admin.CountUser):
            user_quantity: Response = Response(
                {"success": True, "response": "têm {} usuários no banco de dados.", "is_response": False}
            )

        class DBGrep(BaseTranslations.Admin.DBGrep):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}.", "is_response": False}
            )
            user_info: Response = Response(
                {
                    "success": False,
                    "response": "aqui as infos do usuário: {}.",
                    "response_list": [],
                    "is_response": False,
                }
            )
            channel_info: Response = Response(
                {"success": False, "response": "aqui as infos do canal: {}.", "response_list": [], "is_response": False}
            )

        class DelFromDB(BaseTranslations.Admin.DelFromDB):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nome {}.", "is_response": False}
            )
            user_deleted: Response = Response(
                {"success": True, "response": "o usuário {} foi deletado do banco de dados.", "is_response": False}
            )
            users_deleted: Response = Response(
                {
                    "success": True,
                    "response": "foi deletado {} usuários do canal {}.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class DisableNSFW(BaseTranslations.Admin.DisableNSFW):
            commands_disabled: Response = Response(
                {"success": True, "response": "NSFW foi desabilitado em {} canais.", "is_response": False}
            )

        class LotteryStart(BaseTranslations.Admin.LotteryStart):
            pass  # TODO: Fazer quando refizer o loterica_start

        class Nada(BaseTranslations.Admin.Nada):
            nada: Response = Response(
                {"success": True, "response": "O comando foi executado com sucesso.", "is_response": False}
            )

        class Reload(BaseTranslations.Admin.Reload):
            commands_reloaded: Response = Response(
                {"success": True, "response": "Os comandos foram recarregados com sucesso.", "is_response": False}
            )

        class Restart(BaseTranslations.Admin.Restart):
            success: Response = Response(
                {"success": True, "response": "O bot foi reiniciado com sucesso.", "is_response": False}
            )
            unexpected_error: Response = Response(
                {"success": False, "response": "Houve um erro ao reiniciar o bot: {}", "is_response": False}
            )

        class RGit(BaseTranslations.Admin.RGit):
            git_pulled: Response = Response(
                {"success": True, "response": "O comando foi executado com sucesso.", "is_response": False}
            )

    class Random(BaseTranslations.Random):
        class Chance(BaseTranslations.Random.Chance):
            random_percentage: Response = Response({"success": False, "response": "{:.2f}%.", "is_response": False})

        class Choice(BaseTranslations.Random.Choice):
            chosen_option: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Count(BaseTranslations.Random.Count):
            character_count: Response = Response(
                {
                    "success": False,
                    "response": "Com um total de {} caracteres. Onde {} são caracteres especiais.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class HyperTranslate(BaseTranslations.Random.HyperTranslate):
            quantity_error: Response = Response(
                {
                    "success": False,
                    "response": "Você deve informar a quantidade de vezes que vai ser traduzido. Como exemplo: "
                    "`{}hypertranslate 10 <texto>`",
                    "is_response": False,
                }
            )
            starter_string: str = "Estou traduzindo o texto..."
            api_error: Response = Response(
                {"success": False, "response": "Ocorreu um erro com a api de tradução.", "is_response": False}
            )
            unexpected_error: Response = Response(
                {"success": False, "response": "Não foi possível traduzir o texto.", "is_response": False}
            )
            translation: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Imgur(BaseTranslations.Random.Imgur):
            links: Response = Response({"success": False, "response": "", "response_list": [], "is_response": False})
            timeout: Response = Response(
                {
                    "success": False,
                    "response": "100 segundos se passaram e eu não consegui gerar, espera um pouco e tente novamente.",
                    "is_response": False,
                }
            )

        class Imgur7(BaseTranslations.Random.Imgur7):
            links: Response = Response({"success": False, "response": "", "response_list": [], "is_response": False})
            timeout: Response = Response(
                {
                    "success": False,
                    "response": "100 segundos se passaram e eu não consegui gerar, espera um pouco e tente novamente.",
                    "is_response": False,
                }
            )

        class ImgurRepeated(BaseTranslations.Random.ImgurRepeated):
            links_repeated: Response = Response(
                {
                    "success": False,
                    "response": "Quantidade total de imagens repetidas: {}",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class RandomColor(BaseTranslations.Random.RandomColor):
            response: Response = Response(
                {
                    "success": False,
                    "response": "aqui está uma cor aleatória: #{} https://goo.gl/search?%23{}",
                    "is_response": False,
                }
            )

            response_url: Response = Response(
                {"success": False, "response": "{} é {}. https://goo.gl/search?%23{} {}", "is_response": False}
            )

        class Reverse(BaseTranslations.Random.Reverse):
            reversed_string: Response = Response({"success": False, "response": "{}", "is_response": False})

        class RandomLine(BaseTranslations.Random.RandomLine):
            channel_not_found: Response = Response(
                {
                    "success": False,
                    "response": "Não achei nenhum canal com nome {} no banco de dados.",
                    "is_response": False,
                }
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "Não achei nenhum usuário com nome {} no banco de dados.",
                    "is_response": False,
                }
            )
            no_message_found: Response = Response(
                {"success": False, "response": "Não foi possível encontrar uma mensagem.", "is_response": False}
            )
            no_option_found: Response = Response(
                {
                    "success": False,
                    "response": "informe se você que uma mensagem de um canal ou de um usuario no canal. Exemplo: "
                    "`{0}rl <nome do canal>` ou `{0}rl <nome do usuario>` ou `{0}rl <nome do canal> "
                    "<nome do usuário>`",
                    "is_response": False,
                }
            )
            random_line: Response = Response(
                {"success": False, "response": "{} (enviada há {} por {} )", "is_response": False}
            )

        class Scp(BaseTranslations.Random.Scp):
            links: Response = Response({"success": False, "response": "{}", "is_response": False})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente.", "is_response": False}
            )

        class UpSideDown(BaseTranslations.Random.UpSideDown):
            upsidedown: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Wikihow(BaseTranslations.Random.Wikihow):
            links: Response = Response({"success": False, "response": "{}", "is_response": False})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente.", "is_response": False}
            )

        class Wikipedia(BaseTranslations.Random.Wikihow):
            links: Response = Response({"success": False, "response": "{}", "is_response": False})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente.", "is_response": False}
            )

    class Annotations(BaseTranslations.Annotations):
        class Annotation(BaseTranslations.Annotations.Annotation):
            no_content_provided: Response = Response(
                {
                    "success": False,
                    "response": "Você deve informar algo para eu criar uma anotação.",
                    "is_response": False,
                }
            )
            too_much_annotations: Response = Response(
                {
                    "success": False,
                    "response": "já existem 100 anotações, não é possível criar mais.",
                    "is_response": False,
                }
            )
            too_much_characters: Response = Response(
                {"success": False, "response": "A anotação deve ter no máximo 450 caracteres.", "is_response": False}
            )
            annotation_created: Response = Response(
                {"success": False, "response": "Anotação criada com sucesso.  📝 (ID: {})", "is_response": False}
            )

        class Annotations(BaseTranslations.Annotations.Annotations):
            annotation_content: Response = Response(
                {"success": False, "response": "sua anotação de id {} é: {}", "is_response": False}
            )
            not_permitted: Response = Response(
                {
                    "success": False,
                    "response": "a anotação de ID {} não pertence a você ou não existe.",
                    "is_response": False,
                }
            )
            deleted: Response = Response(
                {
                    "success": False,
                    "response": "sua anotação de ID {} foi deletada com sucesso. 🗑",
                    "is_response": False,
                }
            )
            no_annotations_with_id: Response = Response(
                {"success": False, "response": "você não possui nenhuma anotação com esse ID", "is_response": False}
            )
            no_id_provided: Response = Response(
                {
                    "success": False,
                    "response": "você deve passar o ID da anotação que quer deletar",
                    "is_response": False,
                }
            )
            all_annotations: Response = Response(
                {"success": False, "response": "suas anotações são os de ID: {}", "is_response": False}
            )
            no_annotations: Response = Response(
                {"success": False, "response": "você não tem anotações.", "is_response": False}
            )

    class Lottery(BaseTranslations.Lottery):
        class Bet(BaseTranslations.Lottery.Bet):
            lottery_lock: Response = Response(
                {
                    "success": False,
                    "response": "desculpe a lotérica esta fechada enquanto os resultados estão sendo computado.",
                    "is_response": False,
                }
            )
            not_enough_cookies: Response = Response(
                {
                    "success": False,
                    "response": "você não tem cookies suficientes para fazer uma aposta.",
                    "is_response": False,
                }
            )
            five_numbers_bet: Response = Response(
                {
                    "success": False,
                    "response": "a aposta foi criada com os números {} com o valor de 5 cookies.",
                    "is_response": False,
                }
            )
            more_than_five_numbers_bet: Response = Response(
                {
                    "success": False,
                    "response": "a aposta foi criada com os números {} com o valor de {} cookies.",
                    "is_response": False,
                }
            )
            too_much_numbers: Response = Response(
                {"success": False, "response": "você não pode apostar mais que 15 números.", "is_response": False}
            )
            only_numbers: Response = Response(
                {"success": False, "response": "envie apenas números de 1 a 60.", "is_response": False}
            )
            duplicate_numbers: Response = Response(
                {"success": False, "response": "por favor escolha números não repetidos.", "is_response": False}
            )
            minimum_bet: Response = Response(
                {"success": False, "response": "por favor escolha no mínimo 3 números.", "is_response": False}
            )

        class Lottery(BaseTranslations.Lottery.Lottery):
            lottery_lock: Response = Response(
                {
                    "success": False,
                    "response": "desculpe a lotérica esta fechada enquanto os resultados estão sendo computado.",
                    "is_response": False,
                }
            )
            timeout: Response = Response(
                {
                    "success": False,
                    "response": "você demorou muito tempo para escolher uma opção.",
                    "is_response": False,
                }
            )
            not_enough_cookies: Response = Response(
                {
                    "success": False,
                    "response": "você não tem cookies suficientes para fazer uma aposta.",
                    "is_response": False,
                }
            )

            five_numbers_bet: Response = Response(
                {
                    "success": False,
                    "response": "a aposta foi criada com os números {} com o valor de 5 cookies.",
                    "is_response": False,
                }
            )

            more_than_five_numbers_bet: Response = Response(
                {
                    "success": False,
                    "response": "a aposta foi criada com os números {} com o valor de {} cookies.",
                    "is_response": False,
                }
            )
            too_much_numbers: Response = Response(
                {"success": False, "response": "você não pode apostar mais que 15 números.", "is_response": False}
            )

            only_numbers: Response = Response(
                {"success": False, "response": "envie apenas números de 1 a 60.", "is_response": False}
            )
            duplicate_numbers: Response = Response(
                {"success": False, "response": "por favor escolha números não repetidos.", "is_response": False}
            )
            minimum_bet: Response = Response(
                {"success": False, "response": "por favor escolha no mínimo 3 números.", "is_response": False}
            )

    class NSFW(BaseTranslations.NSFW):
        class Boru(BaseTranslations.NSFW.Boru):
            pls_wait = "por favor espera um pouco, estou gerando os links."
            unexpected_error: Response = Response({"success": False, "response": "{}", "is_response": False})
            success: Response = Response({"success": False, "response": "", "is_response": False})

        class AllBoorus(BaseTranslations.NSFW.AllBoorus):
            pls_wait = "por favor espera um pouco, estou gerando os links."
            unexpected_error: Response = Response({"success": False, "response": "{}", "is_response": False})
            too_much_tags: Response = Response(
                {
                    "success": False,
                    "response": "Quantidade de tags ultrapassou o limite permitido de {}.",
                    "is_response": False,
                }
            )
            success: Response = Response({"success": False, "response": "", "is_response": False})

    class Cookies(BaseTranslations.Cookies):
        cookie_lines: list[str] = None

        def cookie_file(self):
            with open("cookies.txt", "r", encoding="utf-8") as file:
                cookie_lines = file.readlines()
            return cookie_lines

        class Cookie(BaseTranslations.Cookies.Cookie):
            not_eat: Response = Response(
                {"success": False, "response": "você não comeu nada, uau!", "is_response": False}
            )
            negative_eat: Response = Response(
                {
                    "success": False,
                    "response": "para comer {} cookies, você primeiro deve saber reverter a entropia.",
                    "is_response": False,
                }
            )
            multiple_eat: Response = Response(
                {"success": False, "response": "você comeu {} cookies de uma só vez. 🥠", "is_response": False}
            )
            eat: Response = Response({"success": False, "response": "", "is_response": False})
            not_enough_cookies: Response = Response(
                {
                    "success": False,
                    "response": "você so pode poder comer {}, para comer {} vai ter que esperar mais {} de dias "
                    "guardando o cookie diário. (não usar stock ou cookie)",
                    "is_response": False,
                }
            )
            daily_limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "você já usou seu cookie diário, a próxima fornada sai a meia noite! ⌛",
                    "is_response": False,
                }
            )

        class CookieCount(BaseTranslations.Cookies.CookieCount):
            bot_nick: Response = Response(
                {
                    "success": False,
                    "response": "eu tenho cookies infinitos, e distribuo uma fração deles para vocês.",
                    "is_response": False,
                }
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "usuário {} ainda não foi registra e não usou nenhum comando de cookie.",
                    "is_response": False,
                }
            )
            cookie: Response = Response({"success": False, "response": "", "is_response": False})
            no_cookie: Response = Response(
                {"success": False, "response": "{} ainda não comeu nenhum cookie", "is_response": False}
            )

            @staticmethod
            def format_cookie(self: Response, ctx: Context, *args: Any, **kwargs: Any):
                self.ctx = ctx
                success = kwargs.pop("success", True)
                response_list = kwargs.pop("response_list", None)
                handle = kwargs.pop("handle", None)
                self.is_response = True

                mention = kwargs.pop("mention", None)
                cookie = kwargs.pop("cookie")

                # Definir valores em response_obj se fornecidos
                if success is not None:
                    self.success = success
                if response_list is not None:
                    self.response_list = response_list
                if handle is not None:
                    self.handle = handle

                comidos = f"já comeu {cookie.consumed} cookies 🥠," if cookie.consumed > 0 else ""
                stocked = f"tem {round(cookie.stocked)} estocados," if cookie.stocked > 0 else ""
                received = f"foi presenteado com {cookie.received}," if cookie.received > 0 else ""
                donated = f"presenteou {cookie.donated}," if cookie.donated > 0 else ""
                unclaimed = (
                    f"e tem um total de {ctx.bot.CookieTools.seed - cookie.daily} não resgatados."
                    if ctx.bot.CookieTools.seed - cookie.daily > 0
                    else ""
                )
                total = f"e teve um total de cookies de {cookie.total} cookies que ja passaram na conta."
                response = f"{mention} {comidos} {stocked} {received} {donated} {unclaimed} {total}"

                self.response_string = response
                return self

        class Gift(BaseTranslations.Cookies.Gift):
            invalid_amount: Response = Response(
                {
                    "success": False,
                    "response": "mande uma quantidade valida para doação e não {}.",
                    "is_response": False,
                }
            )
            bot_nick: Response = Response(
                {"success": False, "response": "eu não quero seu cookie.", "is_response": False}
            )
            user_himself: Response = Response(
                {"success": False, "response": "você tentou presenteou você mesmo, uau!", "is_response": False}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            multiple_gift: Response = Response(
                {"success": False, "response": "você presenteou @{} com {} cookie(s) 🎁", "is_response": False}
            )
            gift: Response = Response(
                {
                    "success": False,
                    "response": "você so pode poder presentear {}, para presentear {} vai ter que esperar mais {} de "
                    "dias guardando o cookie diário. (não usar stock, cookie ou give)",
                    "is_response": False,
                }
            )
            daily_limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "você já usou seu cookie diário, a próxima fornada sai a meia noite! ⌛",
                    "is_response": False,
                }
            )

        class SlotMachine(BaseTranslations.Cookies.SlotMachine):
            daily_limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "você já usou seu cookie diário, a próxima fornada sai a meia noite! ⌛",
                    "is_response": False,
                }
            )
            invalid_amount: Response = Response(
                {
                    "success": False,
                    "response": "você esta tentando apostar {} mais so tem {} cookies não resgatados.",
                    "is_response": False,
                }
            )
            daily_win: Response = Response(
                {
                    "success": False,
                    "response": "[{}] você usou seu cookie diário e ganhou {} cookies!",
                    "is_response": False,
                }
            )
            daily_single_loss: Response = Response(
                {
                    "success": False,
                    "response": "[{''.join(fruits)}] você perdeu seu cookie diário...",
                    "is_response": False,
                }
            )
            not_daily_multiple_loss: Response = Response(
                {
                    "success": False,
                    "response": "[{}] você usou seu cookie diário não resgatado e ganhou {} cookies!",
                    "is_response": False,
                }
            )
            not_daily_single_loss: Response = Response(
                {
                    "success": False,
                    "response": "[{}] você perdeu seu cookie diário não resgatado...",
                    "is_response": False,
                }
            )
            not_daily_multiple_win: Response = Response(
                {
                    "success": False,
                    "response": "você usou {} cookies diários não resgatados e ganhou {} cookies das seguintes "
                    "apostas: {}",
                    "is_response": False,
                }
            )
            not_daily_lost_everything: Response = Response(
                {
                    "success": False,
                    "response": "você usou {} cookies diários e perdeu tudo PoroSad",
                    "is_response": False,
                }
            )

        class Stock(BaseTranslations.Cookies.Stock):
            invalid_number: Response = Response(
                {
                    "success": False,
                    "response": "envie um número inteiro para o que deseja guardar e não {amount}.",
                    "is_response": False,
                }
            )
            single_stock: Response = Response(
                {"success": False, "response": "você estocou seu cookie diário 🍪", "is_response": False}
            )
            invalid_amount: Response = Response(
                {
                    "success": False,
                    "response": "envie uma quantidade entre nada para apostar so um e {} e não {}.",
                    "is_response": False,
                }
            )
            invalid_quantity: Response = Response(
                {
                    "success": False,
                    "response": "você esta tentando apostar {} mais so tem {} cookies não resgatados.",
                    "is_response": False,
                }
            )
            old_stock: Response = Response(
                {"success": False, "response": "você estocou seu cookie diário não resgatado 🍪", "is_response": False}
            )
            multiple_old_stock: Response = Response(
                {
                    "success": False,
                    "response": "você estocou seus {amount} cookies diários não resgatados 🍪",
                    "is_response": False,
                }
            )
            daily_limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "você já usou seu cookie diário, a próxima fornada sai a meia noite! ⌛",
                    "is_response": False,
                }
            )

        class Top(BaseTranslations.Cookies.Top):
            ranks: Response = Response({"success": False, "response": "os ranks são: {}", "is_response": False})
            top10_ish: Response = Response(
                {
                    "success": False,
                    "response": "top {} {}: {} || Você está na posição {}º do ranking com {}.",
                    "is_response": False,
                }
            )

    class Copy(BaseTranslations.Copy):
        class Copy(BaseTranslations.Copy.Copy):
            success: Response = Response({"success": False, "response": "o id da copypasta {}", "is_response": False})
            copy: Response = Response({"success": False, "response": "{}", "is_response": False})
            wrong_id: Response = Response(
                {"success": False, "response": "não existe copypasta com esse id.", "is_response": False}
            )

        class DeleteCopy(BaseTranslations.Copy.DeleteCopy):
            deleted: Response = Response(
                {"success": False, "response": "a copypasta de id {} foi deletada.", "is_response": False}
            )
            not_owner: Response = Response(
                {"success": False, "response": "você precisa ser o criador da copy para apagar.", "is_response": False}
            )
            error: Response = Response(
                {"success": False, "response": "envie {}delcopy delete {} para deletar.", "is_response": False}
            )

        class RandomCopy(BaseTranslations.Copy.RandomCopy):
            success: Response = Response({"success": False, "response": "{}", "is_response": False})

    class Dungeons(BaseTranslations.Dungeons):
        dungeonrank_dict = dungeon_rank_dict

        class DungeonLevel(BaseTranslations.Dungeons.DungeonLevel):
            bot_nick: Response = Response(
                {"success": False, "response": "eu apenas crio as dungeons...", "is_response": False}
            )
            no_class_chosen: Response = Response(
                {"success": False, "response": "{} ainda não escolheu a nova classe", "is_response": False}
            )
            player_status: Response = Response(
                {
                    "success": False,
                    "response": "{} é {} ({}, {} XP) com {} dungeons ({} vitórias, {} derrotas, {:.2f}% winrate) ♦",
                    "is_response": False,
                }
            )
            player_not_found: Response = Response(
                {"success": False, "response": "{} ainda não entrou em nenhuma dungeon", "is_response": False}
            )

        class DungeonRank(BaseTranslations.Dungeons.DungeonRank):
            winrate: Response = Response(
                {
                    "success": False,
                    "response": "top {} {}: {} || você é o {}º no ranking com {:.2f}% {}.",
                    "is_response": False,
                }
            )
            player_rank = "|| Você está na posição {}º no ranking com {} {}."
            normal: Response = Response({"success": False, "response": "top {} {}: {} {}", "is_response": False})

        class DungeonEnter(BaseTranslations.Dungeons.DungeonEnter):
            class_rank_up: Response = Response({"success": False, "response": "agora você é {}", "is_response": False})
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            dungeon_result: Response = Response({"success": False, "response": "{}", "is_response": False})
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar em outra dungeon ⌛", "is_response": False}
            )
            class_choice: Response = Response(
                {"success": False, "response": "você escolheu {}! {}", "is_response": False}
            )
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class DungeonFast(BaseTranslations.Dungeons.DungeonFast):
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, digite '{}ed' e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar em outra dungeon ⌛", "is_response": False}
            )
            dungeon_result: Response = Response({"success": False, "response": "{}", "is_response": False})
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

    class General(BaseTranslations.General):
        class BotInfo(BaseTranslations.General.BotInfo):
            info: Response = Response(
                {
                    "success": False,
                    "response": "estou conectado à {} canais, com {} comandos, "
                    '"feito" por @{} em Python (Twitchio). '
                    "Site do boto: {}",
                    "is_response": False,
                }
            )
            site: Response = Response({"success": False, "response": "{}", "is_response": False})
            uptime: Response = Response({"success": False, "response": "eu acordei há {}", "is_response": False})

        class Bug(BaseTranslations.General.Bug):
            bug_id: Response = Response(
                {"success": False, "response": "seu bug foi reportado 🐛 (ID {})", "is_response": False}
            )

        class Channels(BaseTranslations.General.Channels):
            quantity: Response = Response(
                {"success": False, "response": "estou conectado em {quantidade} canais.", "is_response": False}
            )
            names: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Color(BaseTranslations.General.Color):
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "eu não encontrei ninguém com o nick de {} e isso também não é uma cor valida.",
                    "is_response": False,
                }
            )
            unexpected_error: Response = Response(
                {
                    "success": False,
                    "response": "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick. "
                    "Ex: {}cor ff00ff ou {}cor {}",
                    "is_response": False,
                }
            )
            user_has_no_color = "o usuário {} não tem nenhuma cor salva."
            user_color = "{} cor salva"
            author_color = "sua cor salva é"
            response: Response = Response({"success": False, "response": "{}", "is_response": False})
            response_link: Response = Response(
                {"success": False, "response": "{} é {}. https://goo.gl/search?%23{} {}", "is_response": False}
            )

        class Dict(BaseTranslations.General.Dict):
            word_not_found: Response = Response(
                {"success": False, "response": "não encontrei a palavra {} no www.dicio.com.br", "is_response": False}
            )
            word: Response = Response(
                {"success": False, "response": "A palavra '{}' existe em {}", "is_response": False}
            )

        class Echo(BaseTranslations.General.Echo):
            echo: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Help(BaseTranslations.General.Help):
            command_site: Response = Response(
                {
                    "success": False,
                    "response": "veja todos os comandos: https://gorenmu.vercel.app/docs/intro",
                    "is_response": False,
                }
            )
            command: Response = Response(
                {"success": False, "response": "{}{}: {} | Comando no site: {}", "is_response": False}
            )
            command_aliases: Response = Response(
                {"success": False, "response": "{}{} ({}): {} | Comando no site: {}", "is_response": False}
            )

        class Join(BaseTranslations.General.Join):
            join_message = (
                "Opa. Fui convidado a me instalar aqui, caso queira saber meus comandos entre em "
                '" {} " ou mande {}help. Se o bot cair manda whisper ou mensagem no '
                "chat do {} ."
            )
            already_in_channel_disabled: Response = Response(
                {
                    "success": False,
                    "response": "Eu nunca sai do canal {} e vc pôde me ativar novamente usando {}start !",
                    "is_response": False,
                }
            )
            joined: Response = Response(
                {"success": False, "response": "Entrei no canal com sucesso!", "is_response": False}
            )
            already_in_channel: Response = Response(
                {"success": False, "response": "Ja estou no canal {}!", "is_response": False}
            )

        class LastSeen(BaseTranslations.General.LastSeen):
            bot_nick: Response = Response(
                {"success": False, "response": "eu estou em todos os lugares, a todo momento...", "is_response": False}
            )
            author: Response = Response(
                {"success": False, "response": "você foi visto pela última vez aqui ☝️", "is_response": False}
            )
            author_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{name} ainda não foi registrado (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            not_authorized: Response = Response(
                {"success": False, "response": "esse usuário optou por não permitir mencioná-lo", "is_response": False}
            )
            last_seen: Response = Response(
                {"success": False, "response": "@{} foi visto em @{} pela última vez: {} (há {})", "is_response": False}
            )

        class Leave(BaseTranslations.General.Leave):
            not_in_channel: Response = Response(
                {"success": False, "response": "Eu não estou no seu canal {}!", "is_response": False}
            )
            left: Response = Response({"success": False, "response": "{} removido com sucesso!", "is_response": False})

        class Nicks(BaseTranslations.General.Nicks):
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "não encontrei ninguem com nome de {} no meu banco de dados.",
                    "is_response": False,
                }
            )
            nicks: Response = Response({"success": False, "response": "{}", "is_response": False})
            last_nick: Response = Response({"success": False, "response": "{} → {}", "is_response": False})
            no_nick: Response = Response(
                {"success": False, "response": "nenhuma mudança de nick registrada ainda.", "is_response": False}
            )

        class Ping(BaseTranslations.General.Ping):
            ping: Response = Response(
                {"success": False, "response": "{} || RAM usada {} pelo python || {}", "is_response": False}
            )

        class PopOut(BaseTranslations.General.PopOut):
            url: Response = Response(
                {"success": False, "response": "https://www.twitch.tv/popout/{}/chat?popout=", "is_response": False}
            )

        class Preview(BaseTranslations.General.Preview):
            no_stream: Response = Response(
                {"success": False, "response": "este usuário não esta em live.", "is_response": False}
            )
            response: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Spam(BaseTranslations.General.Spam):
            content_not_valid: Response = Response(
                {"success": False, "response": "Por favor, digite um conteúdo para o spam.", "is_response": False}
            )
            number_not_valid: Response = Response(
                {"success": False, "response": "'{}' não é um número.", "is_response": False}
            )
            response: Response = Response({"success": False, "response": "", "is_response": False})

        class Suggest(BaseTranslations.General.Suggest):
            suggest_id: Response = Response(
                {"success": False, "response": "sua sugestão foi anotada 📝 (ID {})", "is_response": False}
            )

    class Infos(BaseTranslations.Infos):
        class AccountAge(BaseTranslations.Infos.AccountAge):
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um usuário inválido.", "is_response": False}
            )
            birthday_year: Response = Response(
                {"success": False, "response": "hoje completa {} ano que {} criou a conta 🎂", "is_response": False}
            )
            birthday_years: Response = Response(
                {"success": False, "response": "hoje completa {} anos que {} criou a conta 🎂", "is_response": False}
            )
            age: Response = Response(
                {"success": False, "response": "{} criou a conta em {} (há {})", "is_response": False}
            )

        class Avatar(BaseTranslations.Infos.Avatar):
            user_not_found: Response = Response(
                {"success": False, "response": "minha foto de perfil: {} || {}", "is_response": False}
            )
            author_avatar: Response = Response(
                {"success": False, "response": "Usuário {} não exites.", "is_response": False}
            )
            bot_avatar: Response = Response(
                {"success": False, "response": "sua foto de perfil: {} || {}", "is_response": False}
            )
            nick_avatar: Response = Response(
                {"success": False, "response": "foto de perfil de @{}: {} || {}", "is_response": False}
            )

        class FirstFollow(BaseTranslations.Infos.FirstFollow):
            first_and_follow: Response = Response(
                {
                    "success": False,
                    "response": "{} seguiu primeiro @{} e foi seguido primeiro por @{}",
                    "is_response": False,
                }
            )
            not_first_but_followed: Response = Response(
                {
                    "success": False,
                    "response": "{} não segue ninguém e foi seguido primeiro por @{}",
                    "is_response": False,
                }
            )
            follow_but_not_followed: Response = Response(
                {
                    "success": False,
                    "response": "{} seguiu primeiro @{} e não é seguido por ninguém",
                    "is_response": False,
                }
            )
            alone: Response = Response(
                {"success": False, "response": "{} não segue e não é seguido por ninguém", "is_response": False}
            )

        class FollowAge(BaseTranslations.Infos.FollowAge):
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um usuário inválido.", "is_response": False}
            )
            follow_yourself: Response = Response(
                {"success": False, "response": "{} não pode se seguir.", "is_response": False}
            )
            not_followed: Response = Response({"success": False, "response": "{} não segue {}", "is_response": False})
            follow: Response = Response(
                {"success": False, "response": "{} seguiu {} em {} (há {})", "is_response": False}
            )

        class Live(BaseTranslations.Infos.Live):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sou um bot, não um streamer", "is_response": False}
            )
            user_not_found: Response = Response(
                {"success": False, "response": "@{channel} é um canal inválido", "is_response": False}
            )
            channel_offline: Response = Response(
                {"success": False, "response": "@{channel} está offline", "is_response": False}
            )
            stream: Response = Response(
                {
                    "success": False,
                    "response": "{} está streamando {} para {} viewers: {} (há {})",
                    "is_response": False,
                }
            )
            stream_with_print: Response = Response(
                {
                    "success": False,
                    "response": "{} está streamando {} para {} viewers: {} (há {}) || Print {}",
                    "is_response": False,
                }
            )

        class Title(BaseTranslations.Infos.Title):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sou um bot, não um streamer.", "is_response": False}
            )
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um canal inválido", "is_response": False}
            )
            no_title_game: Response = Response(
                {"success": False, "response": "@{} não têm nem título e nem jogo configurado.", "is_response": False}
            )
            no_title: Response = Response({"success": False, "response": "{} 🎮 {}", "is_response": False})
            title_no_game: Response = Response({"success": False, "response": "{} 📑 {}", "is_response": False})
            full_title: Response = Response({"success": False, "response": "{} 📑 {} | 🎮 {}", "is_response": False})

    class Interactive(BaseTranslations.Interactive):
        class Fight(BaseTranslations.Interactive.Fight):
            options: list[str] = fight_option
            bot_nick: Response = Response(
                {"success": False, "response": "você nunca conseguiria me derrotar...", "is_response": False}
            )
            internal_fight: Response = Response(
                {"success": False, "response": "você iniciou uma luta interna...", "is_response": False}
            )
            already_fight: Response = Response(
                {"success": False, "response": "@{} já está sendo desafiado por @{}!", "is_response": False}
            )
            result: Response = Response({"success": False, "response": "{}", "is_response": False})
            refused: Response = Response(
                {"success": False, "response": "@{} recusou o desafio contra @{} LUL", "is_response": False}
            )
            timeout: Response = Response(
                {"success": False, "response": "@{} não respondeu ao seu desafio a tempo", "is_response": False}
            )

        class Hug(BaseTranslations.Interactive.Hug):
            bot: Response = Response({"success": False, "response": "🤗", "is_response": False})
            yourself: Response = Response(
                {"success": False, "response": "você tentou se abraçar...", "is_response": False}
            )
            hug: Response = Response({"success": False, "response": "você abraçou @{} 🤗", "is_response": False})

        class Kiss(BaseTranslations.Interactive.Kiss):
            bot: Response = Response({"success": False, "response": "😳", "is_response": False})
            yourself: Response = Response(
                {"success": False, "response": "você tentou se beijar...", "is_response": False}
            )
            kiss: Response = Response(
                {"success": False, "response": "você deu um beijinho em @{} 😚", "is_response": False}
            )

        class Love(BaseTranslations.Interactive.Love):
            yourself: Response = Response(
                {"success": False, "response": "uma pessoa não pode ser shipada com ela mesma...", "is_response": False}
            )
            ship: Response = Response(
                {"success": False, "response": "@{} & @{}: {} com {}% de amor {}", "is_response": False}
            )

        class Pat(BaseTranslations.Interactive.Pat):
            bot: Response = Response({"success": False, "response": "😊", "is_response": False})
            yourself: Response = Response(
                {"success": False, "response": "você tentou fazer cafuné em si mesmo...", "is_response": False}
            )
            pat: Response = Response({"success": False, "response": "você fez cafuné em @{} 😊", "is_response": False})

        class Penis(BaseTranslations.Interactive.Penis):
            bot: Response = Response({"success": False, "response": "eu só tenho pen drive.", "is_response": False})
            penis: Response = Response({"success": False, "response": "{} tem {}cm {}", "is_response": False})

        class Slap(BaseTranslations.Interactive.Slap):
            bot: Response = Response({"success": False, "response": "vai bater na mãe 😠.", "is_response": False})
            yourself: Response = Response(
                {"success": False, "response": "você se deu um tapa... 😕.", "is_response": False}
            )
            slap: Response = Response(
                {"success": False, "response": "você deu um tapa em @{} 👋", "is_response": False}
            )

        class Tuck(BaseTranslations.Interactive.Tuck):
            bot: Response = Response({"success": False, "response": "eu não posso dormir agora.", "is_response": False})
            yourself: Response = Response(
                {"success": False, "response": "você foi para a cama 🛏", "is_response": False}
            )
            tuck: Response = Response(
                {"success": False, "response": "você colocou @{} na cama 🙂👉🛏", "is_response": False}
            )

    class Markov(BaseTranslations.Markov):
        class Markov(BaseTranslations.Markov.Markov):
            channel_not_found: Response = Response(
                {"success": False, "response": "@canal não encontrado no meu banco de dados.", "is_response": False}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} usuário não encontrado no meu banco de dados.",
                    "is_response": False,
                }
            )
            no_start: Response = Response(
                {
                    "success": False,
                    "response": "não encontrei nenhuma mensagem com o inicio {} para iniciar a geração",
                    "is_response": False,
                }
            )
            markov_generated: Response = Response({"success": False, "response": "{}", "is_response": False})

    class Marry(BaseTranslations.Marry):
        class Marry(BaseTranslations.Marry.Marry):
            bot: Response = Response(
                {
                    "success": False,
                    "response": "não fui programado para fazer parte de um relacionamento.",
                    "is_response": False,
                }
            )
            yourself: Response = Response(
                {"success": False, "response": "você não pode se casar com você mesmo...", "is_response": False}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            proposal_already_in_progress: Response = Response(
                {
                    "success": False,
                    "response": "antes você precisa responder ao pedido de @{}! Digite 'yes' ou 'no",
                    "is_response": False,
                }
            )
            someone_arrived_first: Response = Response(
                {
                    "success": False,
                    "response": "@{} chegou primeiro e já fez uma proposta à mão de @{}",
                    "is_response": False,
                }
            )
            already_married: Response = Response(
                {"success": False, "response": "vocês dois já são casados... não se lembra?", "is_response": False}
            )
            author_limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "você já está casado(a) com {} pessoas não é o suficiente?",
                    "is_response": False,
                }
            )
            limit_reached: Response = Response(
                {
                    "success": False,
                    "response": "@{} já está com o {} pessoas, não há espaço para mais um...",
                    "is_response": False,
                }
            )
            not_enough_cookies: Response = Response(
                {
                    "success": False,
                    "response": "para pagar a aliança e todo o casório, você deve juntar mais {} cookies.",
                    "is_response": False,
                }
            )

            proposal_message: str = (
                "você pediu a mão de @{}, o usuário deve digitar 'yes' ou 'no' / 'sim' ou 'não', 💐💍"
            )

            not_enough_cookies2: Response = Response(
                {
                    "success": False,
                    "response": "parece que @{} gastou todos os cookies que eram pra aliança... "
                    "o casamento precisou ser cancelado",
                    "is_response": False,
                }
            )
            proposal_accept: Response = Response(
                {
                    "success": False,
                    "response": "{}, você aceitou o pedido de @{}, felicidades para o casal! 🎉💞",
                    "is_response": False,
                }
            )
            no_proposal: Response = Response(
                {"success": False, "response": "{}, não há nenhum pedido de casamento para você.", "is_response": False}
            )

            proposal_denied: Response = Response(
                {"success": False, "response": "{}, você recusou o pedido de casamento de @{} 💔", "is_response": False}
            )

            timeout: Response = Response(
                {
                    "success": False,
                    "response": "o tempo para pensar acabou, caso descidão se casar de novo use o comando novamente.",
                    "is_response": False,
                }
            )

        class Divorce(BaseTranslations.Marry.Divorce):
            bot: Response = Response(
                {"success": False, "response": "eu nunca estaria casado com você.", "is_response": False}
            )
            yourself: Response = Response(
                {"success": False, "response": "você não pode se livrar de você mesmo.", "is_response": False}
            )
            not_married: Response = Response(
                {"success": False, "response": "você não está casado com ninguém.", "is_response": False}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            divorce: Response = Response(
                {
                    "success": False,
                    "response": "então, é isso... da próxima vez, case-se com alguém "
                    "que realmente te ame, e não qualquer pessoa por aí",
                    "is_response": False,
                }
            )
            wrong_person: Response = Response(
                {
                    "success": False,
                    "response": "você não sabe nem o nome da pessoa com quem está casado?",
                    "is_response": False,
                }
            )

        class MarryAge(BaseTranslations.Marry.MarryAge):
            bot: Response = Response(
                {"success": False, "response": "nunca me casarei com ninguém.", "is_response": False}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            not_married: Response = Response(
                {"success": False, "response": "{} não esta casado com ninguém.", "is_response": False}
            )
            married: str = "@{} está casado com @{} há {}"
            divorced: str = "@{} está separado de @{} há {} e quem pediu o divórcio foi @{}"
            response: Response = Response({"success": False, "response": "", "is_response": False})

    class Pet(BaseTranslations.Pet):
        PetsDict: PetsDict = pets
        FromListToPetList = from_list_to_pet_list

        class Pet(BaseTranslations.Pet.Pet):
            bot: Response = Response(
                {
                    "success": False,
                    "response": "eu tenho todos os pets, e ofereço alguns pra vocês",
                    "is_response": False,
                }
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            mention_denied: Response = Response(
                {"success": False, "response": "@{} optou por não permitir ser mencionado.", "is_response": False}
            )
            pets: Response = Response({"success": False, "response": "{} possui {}", "is_response": False})
            no_pets: Response = Response(
                {
                    "success": False,
                    "response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    "is_response": False,
                }
            )
            user_no_pets: Response = Response(
                {"success": False, "response": "{} não possui nenhum pet.", "is_response": False}
            )

        class PetBuy(BaseTranslations.Pet.PetBuy):
            no_cookies: Response = Response(
                {
                    "success": False,
                    "response": "comece a estocar cookies para adquirir um pet ({}stock)",
                    "is_response": False,
                }
            )
            not_enough_cookies: Response = Response(
                {"success": False, "response": "estoque {} cookies para adquirir {}", "is_response": False}
            )
            name_too_large: str = (
                "vamos maneirar no tamanho do nome, " "tente novamente desta vez com um nome menor que 32 caracteres."
            )
            timeout: Response = Response(
                {"success": False, "response": "o tempo para comprar acabou tente novamente.", "is_response": False}
            )
            timeout_response: Response = Response(
                {"success": False, "response": "você demorou de mais para responder.", "is_response": False}
            )
            what_name: str = "qual nome você gostaria de da-lo?"
            are_you_sure: str = "tem certeza que deja nomear de {}? (yes ou no)"
            pet_name: str = "o seu pet sera nomeado {}"
            pet_buy: Response = Response(
                {"success": False, "response": "você adquiriu {} {} por {} cookies.", "is_response": False}
            )
            no_options: Response = Response(
                {"success": False, "response": "escolha um dos pets disponíveis hoje ({}petlist)", "is_response": False}
            )

        class PetList(BaseTranslations.Pet.PetList):
            pet_list: Response = Response(
                {"success": False, "response": "pets disponíveis (adquira com {}petbuy): {}", "is_response": False}
            )

        class PetName(BaseTranslations.Pet.PetName):
            no_pets: Response = Response(
                {"success": False, "response": "Você não tem pets para dar nome.", "is_response": False}
            )
            what_pet_to_name: str = (
                "qual dos pets você quer nomear: {}? " "(mande o número do pet que você gostaria de mudar.)"
            )
            timeout: Response = Response(
                {"success": False, "response": "você demorou de mais para responder.", "is_response": False}
            )
            what_name: str = "qual nome você quer dar para {}?"
            new_name: Response = Response(
                {"success": False, "response": "o nome do pet foi mudado para {} .", "is_response": False}
            )

        class PetPat(BaseTranslations.Pet.PetPat):
            no_pet_name: Response = Response(
                {"success": False, "response": "você não especificou o nome do pet.", "is_response": False}
            )
            no_pets: Response = Response(
                {"success": False, "response": "você fez carinho em {} {}", "is_response": False}
            )
            pet_pat: Response = Response(
                {
                    "success": False,
                    "response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    "is_response": False,
                }
            )
            wrong_pet_name: Response = Response(
                {"success": False, "response": "você não tem um pet com este nome..", "is_response": False}
            )

        class PetSell(BaseTranslations.Pet.PetSell):
            pass

    class Profile(BaseTranslations.Profile):
        class Mention(BaseTranslations.Profile.Mention):
            mention_on: Response = Response(
                {
                    "success": False,
                    "response": "outros usuários poderão mencionar você novamente nos comandos.",
                    "is_response": False,
                }
            )

        class NickName(BaseTranslations.Profile.NickName):
            nickname_too_large: Response = Response(
                {
                    "success": False,
                    "response": "o apelido {} é muito grande, por favor tente manter com no máximo 32 caracteres.",
                    "is_response": False,
                }
            )
            nickname_removed: Response = Response(
                {"success": False, "response": "seu apelido foi removido com sucesso!", "is_response": False}
            )
            nickname_changed: Response = Response(
                {"success": False, "response": "você alterou seu de apelido para {} com sucesso!", "is_response": False}
            )

        class SaveCity(BaseTranslations.Profile.SaveCity):
            city_removed: Response = Response(
                {"success": False, "response": "Cidade foi removida com sucesso!.", "is_response": False}
            )
            city_added: Response = Response(
                {
                    "success": False,
                    "response": "Você salvou {} como sua cidade, agora basta usar {}weather.",
                    "is_response": False,
                }
            )

        class SaveColor(BaseTranslations.Profile.SaveColor):
            color_removed: Response = Response(
                {"success": False, "response": "a cor foi removida com sucesso!", "is_response": False}
            )
            color_added: Response = Response(
                {
                    "success": False,
                    "response": 'você salvou a cor {} e pode visualizá-la usando "{}color"',
                    "is_response": False,
                }
            )

        class UnMention(BaseTranslations.Profile.UnMention):
            mention_off: Response = Response(
                {
                    "success": False,
                    "response": "agora outros usuários não poderão mais mencionar você nos comandos.",
                    "is_response": False,
                }
            )

    class Reminder(BaseTranslations.Reminder):
        class Remind(BaseTranslations.Reminder.Remind):
            bot: Response = Response(
                {
                    "success": False,
                    "response": "estou sempre aqui... não precisa me deixar lembretes.",
                    "is_response": False,
                }
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "esse usuário ainda não foi registrado. (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            user_opt_out: Response = Response(
                {"success": False, "response": "o usuário {} optou por desligar os reminds para.", "is_response": False}
            )
            author_too_much_reminds: Response = Response(
                {"success": False, "response": "já existem muitos lembretes seus pendentes...", "is_response": False}
            )
            user_too_much_reminds: Response = Response(
                {"success": False, "response": "já existem muitos lembretes pendentes para {}", "is_response": False}
            )
            time_not_found: Response = Response(
                {"success": False, "response": "não entendi o tempo que você me passou.", "is_response": False}
            )
            remind_on_back: Response = Response(
                {
                    "success": False,
                    "response": "{} será lembrado disso na próxima vez que falar no chat 📝 (ID {})",
                    "is_response": False,
                }
            )
            dont_have_time_machine: Response = Response(
                {"success": False, "response": "eu ainda não inventei a máquina do tempo.", "is_response": False}
            )
            minimum_time: Response = Response(
                {
                    "success": False,
                    "response": "o tempo mínimo para lembretes cronometrados é 1 minuto.",
                    "is_response": False,
                }
            )
            remind_on_time: Response = Response(
                {"success": False, "response": "{} será lembrado disso em {}. ⏲️(ID {})", "is_response": False}
            )

        class Reminds(BaseTranslations.Reminder.Reminds):
            remind_for: Response = Response(
                {"success": False, "response": "esse lembrete é para {}: {}.", "is_response": False}
            )
            remind_timed_with_content: Response = Response(
                {"success": False, "response": "esse lembrete é para {} em {}: {}.", "is_response": False}
            )
            remind_timed_without_content: Response = Response(
                {"success": False, "response": "esse lembrete era para {} há {}.", "is_response": False}
            )
            remind_deleted: Response = Response(
                {"success": False, "response": "seu lembrete de ID {} foi deletado.", "is_response": False}
            )
            remind_not_found: Response = Response(
                {"success": False, "response": "você não possui nenhum lembrete com esse ID.", "is_response": False}
            )
            no_id_selected: Response = Response(
                {
                    "success": False,
                    "response": "você deve passar o ID do lembrete que quer deletar.",
                    "is_response": False,
                }
            )
            author_reminds: Response = Response(
                {"success": False, "response": "seus lembretes pendentes são os de ID: {}.", "is_response": False}
            )
            author_dont_have_reminds: Response = Response(
                {"success": False, "response": "você não tem lembretes pendentes.", "is_response": False}
            )

        class RemindListener(BaseTranslations.Reminder.RemindListener):
            remind_timed_with_content: Response = Response(
                {"success": False, "response": "{} deixou um lembrete: {} (há {})", "is_response": False}
            )
            remind_timed_without_content: Response = Response(
                {"success": False, "response": "{} deixou um lembrete em branco (há {})", "is_response": False}
            )

    class Settings(BaseTranslations.Settings):
        class BanWord(BaseTranslations.Settings.BanWord):
            word_added: Response = Response(
                {"success": False, "response": "esse já é um termo banido.", "is_response": False}
            )
            word_already_on_list: Response = Response(
                {
                    "success": False,
                    "response": "não irei mais enviar mensagens que tiverem esse termo.",
                    "is_response": False,
                }
            )

        class Disable(BaseTranslations.Settings.Disable):
            command_dont_exist: Response = Response(
                {"success": False, "response": "esse comando não existe.", "is_response": False}
            )
            command_cannot_be_disabled: Response = Response(
                {"success": False, "response": "não pode ser desativado.", "is_response": False}
            )
            command_already_disabled: Response = Response(
                {"success": False, "response": '"{}" já está desativado.', "is_response": False}
            )
            command_disabled: Response = Response(
                {"success": False, "response": '"{}" foi desativado.', "is_response": False}
            )

        class Enable(BaseTranslations.Settings.Enable):
            command_dont_exist: Response = Response(
                {"success": False, "response": "esse comando não existe.", "is_response": False}
            )
            command_reactivated: Response = Response(
                {"success": False, "response": '"{}" foi reativado.', "is_response": False}
            )
            command_already_activated: Response = Response(
                {"success": False, "response": '"{}" já está ativado.', "is_response": False}
            )

        class Prefix(BaseTranslations.Settings.Prefix):
            prefix_invalid: Response = Response(
                {"success": False, "response": "este prefixo {prefixo} é invalido", "is_response": False}
            )
            prefix_invalid_or_absent: Response = Response(
                {"success": False, "response": "Esqueceu de mandar o prefixo ou ele é invalido.", "is_response": False}
            )
            prefix_already_in_use: Response = Response(
                {"success": False, "response": "O canal ja esta usando o prefixo {prefixo}.", "is_response": False}
            )
            prefix_changed: Response = Response(
                {"success": False, "response": 'O prefixo do canal foi alterado para "{}".', "is_response": False}
            )
            prefix_too_large: Response = Response(
                {
                    "success": False,
                    "response": "Atualmente eu so consigo armazenar prefixos de ate 2 caracteres o prefixo que você "
                    'tentou usar não é valido pois contem "{}" caracteres.',
                    "is_response": False,
                }
            )

        class Start(BaseTranslations.Settings.Start):
            already_on: Response = Response({"success": False, "response": "já estou ligado ☕", "is_response": False})
            started: Response = Response({"success": False, "response": "você me ligou ☕", "is_response": False})

        class Stop(BaseTranslations.Settings.Stop):
            stopped: Response = Response({"success": False, "response": "você me desligou 💤", "is_response": False})

        class UnBanWord(BaseTranslations.Settings.UnBanWord):
            word_removed: Response = Response(
                {"success": False, "response": '"{}" foi removido dos termos banidos.', "is_response": False}
            )
            word_not_found: Response = Response(
                {"success": False, "response": '"{}" não é um termo banidos.', "is_response": False}
            )

    class Tools(BaseTranslations.Tools):
        class Math(BaseTranslations.Tools.Math):
            result: Response = Response({"success": False, "response": "{}", "is_response": False})
            error: Response = Response(
                {
                    "success": False,
                    "response": "não consegui calcular... lembre-se: use * para multiplicação, use / para divisão, "
                    "e use ponto em vez de vírgula para números decimais. {}",
                    "is_response": False,
                }
            )

        class Shorten(BaseTranslations.Tools.Shorten):
            no_links_found: Response = Response(
                {"success": False, "response": "Use: `{}encurta <link>`", "is_response": False}
            )
            shorten_links: Response = Response(
                {"success": False, "response": "Aqui está os links: {}", "is_response": False}
            )
            shorten_link: Response = Response(
                {"success": False, "response": "Aqui está os link: {}", "is_response": False}
            )
            shorten_error: Response = Response(
                {"success": False, "response": "Não foi possível encurtar o link.", "is_response": False}
            )

        class Time(BaseTranslations.Tools.Time):
            time: Response = Response({"success": False, "response": "{}", "is_response": False})
            future_time: Response = Response({"success": False, "response": "em {}", "is_response": False})
            past_time: Response = Response({"success": False, "response": "há {}", "is_response": False})
            unit_not_found: Response = Response(
                {
                    "success": False,
                    "response": "as medidas suportadas atualmente são: anos, meses, semanas, dias, horas, "
                    "minutos e segundos. Caso nenhuma seja colocada, será dado o tempo completo convertido. ",
                    "is_response": False,
                }
            )
            too_much_time: Response = Response(
                {"success": False, "response": "tempo de mais para converter.", "is_response": False}
            )

        class UserId(BaseTranslations.Tools.UserId):
            user_not_found: Response = Response(
                {"success": False, "response": "não achei nenhum usuário com esse id.", "is_response": False}
            )
            id_or_name: Response = Response({"success": False, "response": "{}", "is_response": False})

        class Weather(BaseTranslations.Tools.Weather, WeatherTools):
            city_not_passed: Response = Response(
                {
                    "success": False,
                    "response": "você não enviou nenhuma cidade e não tem nenhuma cidade salva, "
                    "use {}savecity <cidade> para salvar uma cidade.",
                    "is_response": False,
                }
            )
            city_not_found: Response = Response(
                {
                    "success": False,
                    "response": "eu não encontrei nenhuma cidade com o nome de {}.",
                    "is_response": False,
                }
            )
            weather: Response = Response({"success": False, "response": "", "is_response": False})

            @staticmethod
            def format_weather(self: Response, ctx: Context, *args: Any, **kwargs: Any) -> Response:
                self.ctx = ctx
                success = kwargs.pop("success", True)
                response_list = kwargs.pop("response_list", None)
                handle = kwargs.pop("handle", None)
                self.is_response = True

                weather_obj = kwargs.pop("weather_obj")
                index = kwargs.pop("index")
                city = kwargs.pop("city")
                weather_str = kwargs.pop("weather_str")
                emoji = kwargs.pop("emoji")
                wind_direction = kwargs.pop("wind_direction")

                self.success = success
                self.response_list = response_list
                self.handle = handle

                current_temp, apparent_temp, max_temp, pressure, humidity, wind, precipitation = (
                    weather_obj.current_weather.temperature,
                    weather_obj.hourly.apparent_temperature[index],
                    weather_obj.daily.temperature_2m_max[0],
                    weather_obj.hourly.pressure_msl[index],
                    weather_obj.hourly.relative_humidity_2m[index],
                    weather_obj.current_weather.wind_speed,
                    weather_obj.hourly.precipitation[index],
                )
                unit_temp, unit_press, unit_humid, unit_wind, unit_precip = (
                    weather_obj.hourly_units.apparent_temperature,
                    weather_obj.hourly_units.pressure_msl,
                    weather_obj.hourly_units.relative_humidity_2m,
                    weather_obj.hourly_units.wind_speed_10m,
                    weather_obj.hourly_units.precipitation,
                )

                weather_city = f"{city.display}. {weather_str.capitalize()} {emoji.strip()},"
                temp_string = (
                    f"temperatura de {current_temp} {unit_temp}, máxima de {max_temp} {unit_temp} "
                    f"e aparente de {apparent_temp} {unit_temp},"
                )
                press_string = f"{pressure} {unit_press},"
                humid_string = f"{humidity}{unit_humid},"
                wind_string = f"{wind}{unit_wind} {wind_direction}"
                precip_string = f"" if precipitation == 0 else f", e precipitação de {precipitation} {unit_precip}"

                self.response_string = (
                    f"{weather_city} {temp_string} {press_string} " f"{humid_string} {wind_string} {precip_string}"
                )
                return self

    class Tower(BaseTranslations.Tower):
        class EnterTower(BaseTranslations.Tower.EnterTower):
            class_rank_up: Response = Response({"success": False, "response": "agora você é {}", "is_response": False})
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar continuar a escalada ⌛", "is_response": False}
            )
            tower_result: Response = Response({"success": False, "response": "{}", "is_response": False})
            class_choice: Response = Response(
                {"success": False, "response": "você escolheu {}! {}", "is_response": False}
            )
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! {}ed  " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class FastTower(BaseTranslations.Tower.FastTower):
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar continuar a escalada ⌛", "is_response": False}
            )
            tower_result: Response = Response({"success": False, "response": "{}", "is_response": False})
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! {}et " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class TowerLevel(BaseTranslations.Tower.TowerLevel):
            bot_nick: Response = Response(
                {"success": False, "response": "Eu apenas conto as historias dos encontros.", "is_response": False}
            )
            no_class_chosen: Response = Response(
                {"success": False, "response": "{} ainda não escolheu uma classe.", "is_response": False}
            )
            player_status: Response = Response(
                {
                    "success": False,
                    "response": "{} é {} ({}, {} XP). Esta no andar {} zona {}, com um total de {} "
                    "encontros ({} vitórias, {} derrotas, {.2f}% winrate) ♦",
                    "is_response": False,
                }
            )
            player_not_found: Response = Response({"success": False, "response": "", "is_response": False})
