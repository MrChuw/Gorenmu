from __future__ import annotations

from typing import Any, TYPE_CHECKING

from bot.translations import EnUsTranslations
from bot.translations.en_us.extras import Response
from bot.translations.pt_br.extras import Humanize, WeatherTools
from bot.translations.pt_br.extras import from_list_to_pet_list, pets, PetsDict
from bot.translations.pt_br.extras import fight_option
from bot.translations.pt_br.extras import dungeon_rank_dict
from bot.translations.pt_br.extras import Activity as ActivityExtras
from bot.translations.pt_br.extras import TimeTools, Timeago
from bot.translations.pt_br.extras import Dicio

if TYPE_CHECKING:
    from bot.ext.commands import Context


# TODO: Colocar o pipe false nos comandos que não podem ir para o pipe.
# TODO: adicionar um fallback para o idioma padrão caso não tenha a tradução.


class PtBrTranslations(EnUsTranslations):
    class SupportTools(EnUsTranslations.Exceptions):
        class TimeTools(EnUsTranslations.SupportTools.TimeTools):
            TimeTools: TimeTools = TimeTools
            Timeago: Timeago = Timeago

        class Lottery(EnUsTranslations.SupportTools.Lottery):
            bet_or_consultation: list[str] = ["aposta", "consultar"]

        class Humanize(EnUsTranslations.SupportTools.Lottery):
            Humanize: Humanize = Humanize

        class Dicio(EnUsTranslations.SupportTools.Dicio):
            Dicio: Dicio = Dicio

    class Exceptions(EnUsTranslations.Exceptions):
        class LotteryExceptions(EnUsTranslations.Exceptions.LotteryExceptions):
            lottery_seed: str = "algo horrível aconteceu, contate \"@{}\" aqui na twitch utilizando whispers."

        class ToolsExceptions(EnUsTranslations.Exceptions.ToolsExceptions):
            announcement: str = "algo de errado com o anuncio. {}"

        class BotMainLoopExceptions(EnUsTranslations.Exceptions.BotMainLoopExceptions):
            dev_required: str = "você precisa ser meu criador para executar esse comando."
            owner_required: str = "comandos reservados para o dono do bot."
            command_on_cooldown: str = "para usar o comando de novo volte {}."
            not_implemented: str = "esse comando está temporariamente desativado."

            error_not_registered: str = "ocorreu um erro inesperado, por favor, reporte o erro para @{}"

        class ResponseExceptions(EnUsTranslations.Exceptions.ResponseExceptions):
            error_on_command: str = "um erro aconteceu no comando \"{}\""
            pipe_response: str = "aqui está a resposta que foi gerada pelo comando anterior: {}"
            command_not_pipeble: str = "este comando não pôde ser utilizado com o pipe."

    class Afk(EnUsTranslations.Afk):
        afks: dict[str, ActivityExtras.Status] = ActivityExtras.afks

        class Afk(EnUsTranslations.Afk.Afk):
            message_too_long: Response = Response(
                {"success": False, "response": "Esta mensagem é muito longa."})
            afk_response: Response = Response({"success": True, "response": "{}: {}"})
            afk_content_response: Response = Response(
                {"success": True, "response": "{}: {} e deixou uma nota com: {}"})

        class IsAfk(EnUsTranslations.Afk.IsAfk):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sempre estou aqui... observando."}
            )
            author_nick: Response = Response(
                {"success": False, "response": "você não está trabalhando... obviamente"}
            )
            never_seen: Response = Response(
                {"success": False, "response": "não lembro de ja ter visto nenhum {}."}
            )
            is_afk: Response = Response({"success": False, "response": "@{} {}: {}"})
            is_afk_content: Response = Response(
                {"success": False, "response": "@{} {} e deixou um bilhete: {}"}
            )
            is_not_afk: Response = Response({"success": False, "response": "@{} não está Afk."})

        class RAfk(EnUsTranslations.Afk.RAfk):
            time_expired: Response = Response({
                    "success": False,
                    "response": "O tempo para voltar já passou.",
                    "pipe": False})
            is_afk: Response = Response({"success": False, "response": "{}: {}"})
            is_afk_content: Response = Response({
                    "success": False,
                    "response": "{} {} e deixou um bilhete: {}"})
            is_not_afk: Response = Response({"success": False, "response": "voce não está afk."})

        class AfkListeners(EnUsTranslations.Afk.AfkListeners):
                is_afk: Response = Response({"success": False, "response": "{}: {} (ficou {} {})"})
                is_afk_content: Response = Response(
                        {"success": False, "response": "{} {} e deixou um bilhete: {} (ficou {} {})"})

    class Alias(EnUsTranslations.Alias):
        user_not_found: Response = Response({
            "success": False,
            "response": "não há usuário com nome de {}.",
            "pipe": False})

        dont_have_alias: Response = Response({
                "success": False,
                "response": "Você não tem alias com nome de \"{}\"", "pipe": False})

        alias_invalid_name: Response = Response({
                "success": False,
                "response": "O nome do seu aliás não é valido. "
                            "Seu alias deve conter apenas letras, números e ter de 2 a 30 caracteres.",
                "pipe": False})

        class Add(EnUsTranslations.Alias.Add):
            no_command_to_add: Response = Response({
                "success": False,
                "response": "Você não enviou um comando! Uso: {}alias add (name) (command) (...arguments)",
                "pipe": False})

            alias_name_conflict: Response = Response({
                "success": False,
                "response": "Não é possível adicionar o alias \"{}\" - você já tem um! "
                            "Você pode \"edit\" sua definição, \"rename\" ou \"remove\".",
                "pipe": False})

            alias_crated: Response = Response({
                "success": False,
                "response": "Seu alias \"{}\" foi criado com sucesso.",
                "pipe": False})

            command_dont_exist: Response = Response({
                    "success": False,
                    "response": "Não é possível criar o alias! O comando \"{}\" não existe.", "pipe": False}
            )

        class Check(EnUsTranslations.Alias.Check):
            user_alias_list: Response = Response({
                "success": False,
                "response": "Sua lista de alias: {}",
                "pipe": False})

            no_alias_found: Response = Response({
                "success": False,
                "response": "Não consegui encontrar {} no do usuário {} ou em qualquer um dos seus aliases!",
                "pipe": False})

            list_of_alias_of: Response = Response({
                "success": False,
                "response": "Lista de alias do {}: {}",
                "pipe": False})

            list_of_special_case: Response = Response({
                "success": False,
                "response": "Caso Especial!\n"
                            "Seu alias \"{0}\": {1}\n"
                            "Lista de alias de {0}: {2}",
                "pipe": False})

            alias_not_found: Response = Response({
                "success": False,
                "response": "{} não tem o alias \"{}\"",
                "pipe": False})

            appendix: str = "Este alias é um link para \"{}\" feito por {}."

            alias_deleted: Response = Response({
                "success": False,
                "response": "{} alias é um link para um alias diferente, mas o original foi excluído.",
                "pipe": False})

            message: str = "{} {} alias \"{}\" tem esta definição: {} {} "

            final_message: Response = Response({
                "success": False,
                "response": "{} {}",
                "pipe": False})

        class Copy(EnUsTranslations.Alias.Copy):
            user_not_provided: Response = Response({
                "success": False,
                "response": "Nenhum usuário foi fornecido!",
                "pipe": False})

            alias_not_provided: Response = Response({
                "success": False,
                "response": "Nenhum alias de destino fornecido!",
                "pipe": False})

            target_alias_invalid_name: Response = Response({
                "success": False,
                "response": "O nome do alias copiado não é válido e portanto não pode ser copiado!",
                "pipe": False})

            link_to_a_link: Response = Response({
                "success": False,
                "response": 'Você não pode copiar links para outros aliases. '
                            'Em vez disso, use o link {}alias copy {} {}',
                "pipe": False})

            copy_success: Response = Response({
                "success": False,
                "response": "Alias \"{}\" copiado com sucesso.",
                "pipe": False})

        class Describe(EnUsTranslations.Alias.Describe):
            no_args_to_parse: Response = Response({
                "success": False,
                "response": "You didn't provide a name, or a command! Use: {}alias describe (name) (...description)",
                "pipe": False})

            description_updated: Response = Response({
                "success": False,
                "response": "A descrição do seu alias \"{}\" foi atualizada com sucesso.",
                "pipe": False})

            description_reseted: Response = Response({
                "success": False,
                "response": "A descrição do seu alias \"{}\" foi resetada com sucesso.",
                "pipe": False})

        class Edit(EnUsTranslations.Alias.Edit):
            no_args_provided: Response = Response(
                    {"success": False, "response": "Nenhum alias ou nome de comando fornecido!", "pipe": False}
            )

            edit_link: Response = Response(
                    {"success": False, "response": "Você não pode editar links para outros aliases!", "pipe": False}
            )

            edit_success: Response = Response(
                    {"success": False, "response": 'Seu alias "{}" foi editado com sucesso.', "pipe": False}
            )

            command_dont_exist: Response = Response({
                    "success": False,
                    "response": 'Não é possível editar o alias! O comando "{}" não existe.',
                    "pipe": False}
            )

        class Link(EnUsTranslations.Alias.Link):
            link_no_args: Response = Response({
                    "success": False,
                    "response": "Você não forneceu um usuário ou o nome do alias! "
                                "Use: {}alias link (usuário) (nome do alias)",
                    "pipe": False}
            )

            alias_name_already_exists: Response = Response({
                    "success": False,
                    "response": "Não é possível vincular um novo alias - você já tem um alias com esse nome!",
                    "pipe": False}
            )

            user_dont_has_alias: Response = Response({
                    "success": False,
                    "response": 'O usuário fornecido não tem o alias "{}"!',
                    "pipe": False}
            )

            appendix_link: str = ('Você tentou criar um link a partir de um alias já vinculado (alias {} por {}), '
                                  'então usei o original como seu modelo.')

            link_with_invalid_name: Response = Response({
                    "success": False,
                    "response": 'O nome do alias vinculado não é válido! {}',
                    "pipe": False}
            )

            link_name_string: str = ', com um nome personalizado "{}"'

            link_success: Response = Response({
                    "success": False,
                    "response": 'Alias vinculado com sucesso{}. '
                                'Quando o original mudar, o seu também mudará. {}',
                    "pipe": False}
            )

        class Remove(EnUsTranslations.Alias.Remove):
            no_alias_name_provided: Response = Response(
                    {"success": False, "response": "Nenhum nome de alias fornecido!", "pipe": False}
            )

            alias_removed: Response = Response(
                    {"success": False, "response": 'Seu alias "{}" foi removido com sucesso.', "pipe": False}
            )

        class Rename(EnUsTranslations.Alias.Rename):
            no_name_provided: Response = Response({
                    "success": False,
                    "response": "Você deve fornecer tanto o nome atual do alias quanto o novo!",
                    "pipe": False}
            )

            alias_already_exists: Response = Response({
                    "success": False,
                    "response": 'Você já tem o alias "{}"!'})

            alias_renamed: Response = Response({
                    "success": False,
                    "response": 'Seu alias "{}" foi renomeado com sucesso para "{}".',
                    "pipe": False}
            )




    class Admin(EnUsTranslations.Admin):
        class AddUser(EnUsTranslations.Admin.AddUser):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}."}
            )
            user_response: Response = Response(
                {
                    "success": False,
                    "response": "as infos de {} foram adicionadas.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class AddBot(EnUsTranslations.Admin.AddBot):
            user_not_found: Response = Response(
                {"success": False, "response": "eu ainda não vi esse bot em nenhum chat."}
            )
            user_already_added: Response = Response(
                {"success": False, "response": "o bot {} ja esta registrado."}
            )
            user_added: Response = Response(
                {"success": True, "response": "o bot {} foi adicionado aos bots."}
            )

        class AllChannels(EnUsTranslations.Admin.AllChannels):
            channels: Response = Response(
                {"success": False, "response": "aqui a lista de todos os canais que eu estou: {}"}
            )

        class Announce(EnUsTranslations.Admin.Announce):
            success: Response = Response(
                {"success": False, "response": "O comando foi executado com sucesso."}
            )

        class ApiBot(EnUsTranslations.Admin.ApiBot):
            added_with_success: Response = Response(
                {
                    "success": False,
                    "response": "O comando foi executado com sucesso. Com {} bots adicionados.",
                    "is_response": False,
                }
            )

        class ChannelLog(EnUsTranslations.Admin.ChannelLog):
            channel_already_added: Response = Response(
                {"success": False, "response": "Ja estou no canal {}."}
            )
            channel_added: Response = Response(
                {"success": True, "response": "Entrei no canal {}."}
            )

        class CookieGive(EnUsTranslations.Admin.CookieGive):
            cookie_given: Response = Response(
                {"success": True, "response": "você deu {} para {}."}
            )

        class CountUser(EnUsTranslations.Admin.CountUser):
            user_quantity: Response = Response(
                {"success": True, "response": "têm {} usuários no banco de dados."}
            )

        class DBGrep(EnUsTranslations.Admin.DBGrep):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}."}
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
                {"success": False, "response": "aqui as infos do canal: {}.", "response_list": []}
            )

        class DelFromDB(EnUsTranslations.Admin.DelFromDB):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nome {}."}
            )
            user_deleted: Response = Response(
                {"success": True, "response": "o usuário {} foi deletado do banco de dados."}
            )
            users_deleted: Response = Response(
                {
                    "success": True,
                    "response": "foi deletado {} usuários do canal {}.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class DisableNSFW(EnUsTranslations.Admin.DisableNSFW):
            commands_disabled: Response = Response(
                {"success": True, "response": "NSFW foi desabilitado em {} canais."}
            )

        class LotteryStart(EnUsTranslations.Admin.LotteryStart):
            pass  # TODO: Fazer quando refizer o loterica_start

        class Nada(EnUsTranslations.Admin.Nada):
            nada: Response = Response(
                {"success": True, "response": "O comando foi executado com sucesso. {}"}
            )

        class Reload(EnUsTranslations.Admin.Reload):
            commands_reloaded: Response = Response(
                {"success": True, "response": "Os comandos foram recarregados com sucesso."}
            )

        class Restart(EnUsTranslations.Admin.Restart):
            success: Response = Response(
                {"success": True, "response": "O bot foi reiniciado com sucesso."}
            )
            unexpected_error: Response = Response(
                {"success": False, "response": "Houve um erro ao reiniciar o bot: {}"}
            )

        class RGit(EnUsTranslations.Admin.RGit):
            git_pulled: Response = Response(
                {"success": True, "response": "O comando foi executado com sucesso."}
            )

    class Random(EnUsTranslations.Random):
        class Chance(EnUsTranslations.Random.Chance):
            random_percentage: Response = Response({"success": False, "response": "{:.2f}%."})

        class Choice(EnUsTranslations.Random.Choice):
            chosen_option: Response = Response({"success": False, "response": "{}"})

        class Count(EnUsTranslations.Random.Count):
            character_count: Response = Response(
                {
                    "success": False,
                    "response": "Com um total de {} caracteres. Onde {} são caracteres especiais.",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class HyperTranslate(EnUsTranslations.Random.HyperTranslate):
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
                {"success": False, "response": "Ocorreu um erro com a api de tradução."}
            )
            unexpected_error: Response = Response(
                {"success": False, "response": "Não foi possível traduzir o texto."}
            )
            translation: Response = Response({"success": False, "response": "{}"})

        class Imgur(EnUsTranslations.Random.Imgur):
            links: Response = Response({"success": False, "response": "", "response_list": []})
            timeout: Response = Response(
                {
                    "success": False,
                    "response": "100 segundos se passaram e eu não consegui gerar, espera um pouco e tente novamente.",
                    "is_response": False,
                }
            )

        class Imgur7(EnUsTranslations.Random.Imgur7):
            links: Response = Response({"success": False, "response": "", "response_list": []})
            timeout: Response = Response(
                {
                    "success": False,
                    "response": "100 segundos se passaram e eu não consegui gerar, espera um pouco e tente novamente.",
                    "is_response": False,
                }
            )

        class ImgurRepeated(EnUsTranslations.Random.ImgurRepeated):
            links_repeated: Response = Response(
                {
                    "success": False,
                    "response": "Quantidade total de imagens repetidas: {}",
                    "response_list": [],
                    "is_response": False,
                }
            )

        class RandomColor(EnUsTranslations.Random.RandomColor):
            response: Response = Response(
                {
                    "success": False,
                    "response": "aqui está uma cor aleatória: #{} https://goo.gl/search?%23{}",
                    "is_response": False,
                }
            )

            response_url: Response = Response(
                {"success": False, "response": "{} é {}. https://goo.gl/search?%23{} {}"}
            )

        class Reverse(EnUsTranslations.Random.Reverse):
            reversed_string: Response = Response({"success": False, "response": "{}"})

        class RandomLine(EnUsTranslations.Random.RandomLine):
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
                {"success": False, "response": "Não foi possível encontrar uma mensagem."}
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
                {"success": False, "response": "{} (enviada há {} por {} )"}
            )

        class Scp(EnUsTranslations.Random.Scp):
            links: Response = Response({"success": False, "response": "{}"})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente."}
            )

        class UpSideDown(EnUsTranslations.Random.UpSideDown):
            upsidedown: Response = Response({"success": False, "response": "{}"})

        class Wikihow(EnUsTranslations.Random.Wikihow):
            links: Response = Response({"success": False, "response": "{}"})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente."}
            )

        class Wikipedia(EnUsTranslations.Random.Wikihow):
            links: Response = Response({"success": False, "response": "{}"})
            unexpected_error: Response = Response(
                {"success": False, "response": "Aconteceu algum erro, tente novamente."}
            )

    class Annotations(EnUsTranslations.Annotations):
        class Annotation(EnUsTranslations.Annotations.Annotation):
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
                {"success": False, "response": "A anotação deve ter no máximo 450 caracteres."}
            )
            annotation_created: Response = Response(
                {"success": False, "response": "Anotação criada com sucesso.  📝 (ID: {})"}
            )

        class Annotations(EnUsTranslations.Annotations.Annotations):
            annotation_content: Response = Response(
                {"success": False, "response": "sua anotação de id {} é: {}"}
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
                {"success": False, "response": "você não possui nenhuma anotação com esse ID"}
            )
            no_id_provided: Response = Response(
                {
                    "success": False,
                    "response": "você deve passar o ID da anotação que quer deletar",
                    "is_response": False,
                }
            )
            all_annotations: Response = Response(
                {"success": False, "response": "suas anotações são os de ID: {}"}
            )
            no_annotations: Response = Response(
                {"success": False, "response": "você não tem anotações."}
            )

    class Lottery(EnUsTranslations.Lottery):
        class Bet(EnUsTranslations.Lottery.Bet):
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
                {"success": False, "response": "você não pode apostar mais que 15 números."}
            )
            only_numbers: Response = Response(
                {"success": False, "response": "envie apenas números de 1 a 60."}
            )
            duplicate_numbers: Response = Response(
                {"success": False, "response": "por favor escolha números não repetidos."}
            )
            minimum_bet: Response = Response(
                {"success": False, "response": "por favor escolha no mínimo 3 números."}
            )

        class Lottery(EnUsTranslations.Lottery.Lottery):
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
                {"success": False, "response": "você não pode apostar mais que 15 números."}
            )

            only_numbers: Response = Response(
                {"success": False, "response": "envie apenas números de 1 a 60."}
            )
            duplicate_numbers: Response = Response(
                {"success": False, "response": "por favor escolha números não repetidos."}
            )
            minimum_bet: Response = Response(
                {"success": False, "response": "por favor escolha no mínimo 3 números."}
            )

            bet_message: str = ("agora você precisa escolher ate 6 números de 1 a 60 (para a aposta padrão ou ate 15 "
                                "para a Aposta Máxima custando 1.294 cookies).")

            consultation_message: str = "você gostaria de consultar apostas passadas ou atuais?"
            past: str = "passadas"
            current: str = "atuais"

    class NSFW(EnUsTranslations.NSFW):
        class Boru(EnUsTranslations.NSFW.Boru):
            pls_wait: str = "por favor espera um pouco, estou gerando os links."
            unexpected_error: Response = Response({"success": False, "response": "{}"})
            success: Response = Response({"success": False, "response": ""})

        class AllBoorus(EnUsTranslations.NSFW.AllBoorus):
            pls_wait: str = "por favor espera um pouco, estou gerando os links."
            unexpected_error: Response = Response({"success": False, "response": "{}"})
            too_much_tags: Response = Response(
                {
                    "success": False,
                    "response": "Quantidade de tags ultrapassou o limite permitido de {}.",
                    "is_response": False,
                }
            )
            success: Response = Response({"success": False, "response": ""})

    class Cookies(EnUsTranslations.Cookies):
        cookie_lines: list[str] = None

        def cookie_file(self):  # TODO: Ver se funfa.
            with open("extras/cookies.txt", "r", encoding="utf-8") as file:
                cookie_lines = file.readlines()
            return cookie_lines

        class Cookie(EnUsTranslations.Cookies.Cookie):
            not_eat: Response = Response(
                {"success": False, "response": "você não comeu nada, uau!"}
            )
            negative_eat: Response = Response(
                {
                    "success": False,
                    "response": "para comer {} cookies, você primeiro deve saber reverter a entropia.",
                    "is_response": False,
                }
            )
            multiple_eat: Response = Response(
                {"success": False, "response": "você comeu {} cookies de uma só vez. 🥠"}
            )
            eat: Response = Response({"success": False, "response": ""})
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

        class CookieCount(EnUsTranslations.Cookies.CookieCount):
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
            cookie: Response = Response({"success": False, "response": ""})
            no_cookie: Response = Response(
                {"success": False, "response": "{} ainda não comeu nenhum cookie"}
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

        class Gift(EnUsTranslations.Cookies.Gift):
            invalid_amount: Response = Response(
                {
                    "success": False,
                    "response": "mande uma quantidade valida para doação e não {}.",
                    "is_response": False,
                }
            )
            bot_nick: Response = Response(
                {"success": False, "response": "eu não quero seu cookie."}
            )
            user_himself: Response = Response(
                {"success": False, "response": "você tentou presenteou você mesmo, uau!"}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            multiple_gift: Response = Response(
                {"success": False, "response": "você presenteou @{} com {} cookie(s) 🎁"}
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

        class SlotMachine(EnUsTranslations.Cookies.SlotMachine):
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

        class Stock(EnUsTranslations.Cookies.Stock):
            invalid_number: Response = Response(
                {
                    "success": False,
                    "response": "envie um número inteiro para o que deseja guardar e não {amount}.",
                    "is_response": False,
                }
            )
            single_stock: Response = Response(
                {"success": False, "response": "você estocou seu cookie diário 🍪"}
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
                {"success": False, "response": "você estocou seu cookie diário não resgatado 🍪"}
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

        class Top(EnUsTranslations.Cookies.Top):
            ranks: Response = Response({"success": False, "response": "os ranks são: {}"})
            top10_ish: Response = Response(
                {
                    "success": False,
                    "response": "top {} {}: {} || Você está na posição {}º do ranking com {}.",
                    "is_response": False,
                }
            )

    class Copy(EnUsTranslations.Copy):
        class Copy(EnUsTranslations.Copy.Copy):
            success: Response = Response({"success": False, "response": "o id da copypasta {}"})
            copy: Response = Response({"success": False, "response": "{}"})
            wrong_id: Response = Response(
                {"success": False, "response": "não existe copypasta com esse id."}
            )

        class DeleteCopy(EnUsTranslations.Copy.DeleteCopy):
            deleted: Response = Response(
                {"success": False, "response": "a copypasta de id {} foi deletada."}
            )
            not_owner: Response = Response(
                {"success": False, "response": "você precisa ser o criador da copy para apagar."}
            )
            error: Response = Response(
                {"success": False, "response": "envie {}delcopy delete {} para deletar."}
            )

        class RandomCopy(EnUsTranslations.Copy.RandomCopy):
            success: Response = Response({"success": False, "response": "{}"})

    class Dungeons(EnUsTranslations.Dungeons):
        dungeonrank_dict = dungeon_rank_dict

        class DungeonLevel(EnUsTranslations.Dungeons.DungeonLevel):
            bot_nick: Response = Response(
                {"success": False, "response": "eu apenas crio as dungeons..."}
            )
            no_class_chosen: Response = Response(
                {"success": False, "response": "{} ainda não escolheu a nova classe"}
            )
            player_status: Response = Response(
                {
                    "success": False,
                    "response": "{} é {} ({}, {} XP) com {} dungeons ({} vitórias, {} derrotas, {:.2f}% winrate) ♦",
                    "is_response": False,
                }
            )
            player_not_found: Response = Response(
                {"success": False, "response": "{} ainda não entrou em nenhuma dungeon"}
            )

        class DungeonRank(EnUsTranslations.Dungeons.DungeonRank):
            winrate: Response = Response(
                {
                    "success": False,
                    "response": "top {} {}: {} || você é o {}º no ranking com {:.2f}% {}.",
                    "is_response": False,
                }
            )
            player_rank = "|| Você está na posição {}º no ranking com {} {}."
            normal: Response = Response({"success": False, "response": "top {} {}: {} {}"})

        class DungeonEnter(EnUsTranslations.Dungeons.DungeonEnter):
            class_rank_up: Response = Response({"success": False, "response": "agora você é {}"})
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            dungeon_result: Response = Response({"success": False, "response": "{}"})
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar em outra dungeon ⌛"}
            )
            class_choice: Response = Response(
                {"success": False, "response": "você escolheu {}! {}"}
            )
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class DungeonFast(EnUsTranslations.Dungeons.DungeonFast):
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, digite '{}ed' e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar em outra dungeon ⌛"}
            )
            dungeon_result: Response = Response({"success": False, "response": "{}"})
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

    class General(EnUsTranslations.General):
        class BotInfo(EnUsTranslations.General.BotInfo):
            info: Response = Response(
                {
                    "success": False,
                    "response": "estou conectado à {} canais, com {} comandos, "
                    '"feito" por @{} em Python (Twitchio). '
                    "Site do boto: {}",
                    "is_response": False,
                }
            )
            site: Response = Response({"success": False, "response": "{}"})
            uptime: Response = Response({"success": False, "response": "eu acordei há {}"})

        class Bug(EnUsTranslations.General.Bug):
            bug_id: Response = Response(
                {"success": False, "response": "seu bug foi reportado 🐛 (ID {})"}
            )

        class Channels(EnUsTranslations.General.Channels):
            quantity: Response = Response(
                {"success": False, "response": "estou conectado em {quantidade} canais."}
            )
            names: Response = Response({"success": False, "response": "{}"})

        class Color(EnUsTranslations.General.Color):
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
            response: Response = Response({"success": False, "response": "{}"})
            response_link: Response = Response(
                {"success": False, "response": "{} é {}. https://goo.gl/search?%23{} {}"}
            )

        class Dict(EnUsTranslations.General.Dict):
            word_not_found: Response = Response(
                {"success": False, "response": "não encontrei a palavra {} no www.dicio.com.br"}
            )
            word: Response = Response(
                {"success": False, "response": "A palavra '{}' existe em {}"}
            )

        class Echo(EnUsTranslations.General.Echo):
            echo: Response = Response({"success": False, "response": "{}"})

        class Help(EnUsTranslations.General.Help):
            command_site: Response = Response(
                {
                    "success": False,
                    "response": "veja todos os comandos: https://gorenmu.vercel.app/docs/intro",
                    "is_response": False,
                }
            )
            command: Response = Response(
                {"success": False, "response": "{}{}: {} | Comando no site: {}"}
            )
            command_aliases: Response = Response(
                {"success": False, "response": "{}{} ({}): {} | Comando no site: {}"}
            )

        class Join(EnUsTranslations.General.Join):
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
                {"success": False, "response": "Entrei no canal com sucesso!"}
            )
            already_in_channel: Response = Response(
                {"success": False, "response": "Ja estou no canal {}!"}
            )

        class LastSeen(EnUsTranslations.General.LastSeen):
            bot_nick: Response = Response(
                {"success": False, "response": "eu estou em todos os lugares, a todo momento..."}
            )
            author: Response = Response(
                {"success": False, "response": "você foi visto pela última vez aqui ☝️"}
            )
            author_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{name} ainda não foi registrado (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            not_authorized: Response = Response(
                {"success": False, "response": "esse usuário optou por não permitir mencioná-lo"}
            )
            last_seen: Response = Response(
                {"success": False, "response": "@{} foi visto em @{} pela última vez: {} (há {})"}
            )

        class Leave(EnUsTranslations.General.Leave):
            not_in_channel: Response = Response(
                {"success": False, "response": "Eu não estou no seu canal {}!"}
            )
            left: Response = Response({"success": False, "response": "{} removido com sucesso!"})

        class Nicks(EnUsTranslations.General.Nicks):
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "não encontrei ninguem com nome de {} no meu banco de dados.",
                    "is_response": False,
                }
            )
            nicks: Response = Response({"success": False, "response": "{}"})
            last_nick: Response = Response({"success": False, "response": "{} → {}"})
            no_nick: Response = Response(
                {"success": False, "response": "nenhuma mudança de nick registrada ainda."}
            )

        class Ping(EnUsTranslations.General.Ping):
            ping: Response = Response(
                {"success": False, "response": "{} || RAM usada {} pelo python || {}"}
            )

        class PopOut(EnUsTranslations.General.PopOut):
            url: Response = Response(
                {"success": False, "response": "https://www.twitch.tv/popout/{}/chat?popout="}
            )

        class Preview(EnUsTranslations.General.Preview):
            no_stream: Response = Response(
                {"success": False, "response": "este usuário não esta em live."}
            )
            response: Response = Response({"success": False, "response": "{}"})

        class Spam(EnUsTranslations.General.Spam):
            content_not_valid: Response = Response(
                {"success": False, "response": "Por favor, digite um conteúdo para o spam."}
            )
            number_not_valid: Response = Response(
                {"success": False, "response": "'{}' não é um número."}
            )
            response: Response = Response({"success": False, "response": ""})

        class Suggest(EnUsTranslations.General.Suggest):
            suggest_id: Response = Response(
                {"success": False, "response": "sua sugestão foi anotada 📝 (ID {})"}
            )

    class Infos(EnUsTranslations.Infos):
        class AccountAge(EnUsTranslations.Infos.AccountAge):
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um usuário inválido."}
            )
            birthday_year: Response = Response(
                {"success": False, "response": "hoje completa {} ano que {} criou a conta 🎂"}
            )
            birthday_years: Response = Response(
                {"success": False, "response": "hoje completa {} anos que {} criou a conta 🎂"}
            )
            age: Response = Response(
                {"success": False, "response": "{} criou a conta em {} (há {})"}
            )

        class Avatar(EnUsTranslations.Infos.Avatar):
            user_not_found: Response = Response(
                {"success": False, "response": "minha foto de perfil: {} || {}"}
            )
            author_avatar: Response = Response(
                {"success": False, "response": "Usuário {} não exites."}
            )
            bot_avatar: Response = Response(
                {"success": False, "response": "sua foto de perfil: {} || {}"}
            )
            nick_avatar: Response = Response(
                {"success": False, "response": "foto de perfil de @{}: {} || {}"}
            )

        class FirstFollow(EnUsTranslations.Infos.FirstFollow):
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
                {"success": False, "response": "{} não segue e não é seguido por ninguém"}
            )

        class FollowAge(EnUsTranslations.Infos.FollowAge):
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um usuário inválido."}
            )
            follow_yourself: Response = Response(
                {"success": False, "response": "{} não pode se seguir."}
            )
            not_followed: Response = Response({"success": False, "response": "{} não segue {}"})
            follow: Response = Response(
                {"success": False, "response": "{} seguiu {} em {} (há {})"}
            )

        class Live(EnUsTranslations.Infos.Live):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sou um bot, não um streamer"}
            )
            user_not_found: Response = Response(
                {"success": False, "response": "@{channel} é um canal inválido"}
            )
            channel_offline: Response = Response(
                {"success": False, "response": "@{channel} está offline"}
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

        class Title(EnUsTranslations.Infos.Title):
            bot_nick: Response = Response(
                {"success": False, "response": "eu sou um bot, não um streamer."}
            )
            user_not_found: Response = Response(
                {"success": False, "response": "@{} é um canal inválido"}
            )
            no_title_game: Response = Response(
                {"success": False, "response": "@{} não têm nem título e nem jogo configurado."}
            )
            no_title: Response = Response({"success": False, "response": "{} 🎮 {}"})
            title_no_game: Response = Response({"success": False, "response": "{} 📑 {}"})
            full_title: Response = Response({"success": False, "response": "{} 📑 {} | 🎮 {}"})

    class Interactive(EnUsTranslations.Interactive):
        class Fight(EnUsTranslations.Interactive.Fight):
            options: list[str] = fight_option
            bot_nick: Response = Response(
                {"success": False, "response": "você nunca conseguiria me derrotar..."}
            )
            internal_fight: Response = Response(
                {"success": False, "response": "você iniciou uma luta interna..."}
            )
            already_fight: Response = Response(
                {"success": False, "response": "@{} já está sendo desafiado por @{}!"}
            )
            result: Response = Response({"success": False, "response": "{}"})
            refused: Response = Response(
                {"success": False, "response": "@{} recusou o desafio contra @{} LUL"}
            )
            timeout: Response = Response(
                {"success": False, "response": "@{} não respondeu ao seu desafio a tempo"}
            )

        class Hug(EnUsTranslations.Interactive.Hug):
            bot: Response = Response({"success": False, "response": "🤗"})
            yourself: Response = Response(
                {"success": False, "response": "você tentou se abraçar..."}
            )
            hug: Response = Response({"success": False, "response": "você abraçou @{} 🤗"})

        class Kiss(EnUsTranslations.Interactive.Kiss):
            bot: Response = Response({"success": False, "response": "😳"})
            yourself: Response = Response(
                {"success": False, "response": "você tentou se beijar..."}
            )
            kiss: Response = Response(
                {"success": False, "response": "você deu um beijinho em @{} 😚"}
            )

        class Love(EnUsTranslations.Interactive.Love):
            yourself: Response = Response(
                {"success": False, "response": "uma pessoa não pode ser shipada com ela mesma..."}
            )
            ship: Response = Response(
                {"success": False, "response": "@{} & @{}: {} com {}% de amor {}"}
            )

        class Pat(EnUsTranslations.Interactive.Pat):
            bot: Response = Response({"success": False, "response": "😊"})
            yourself: Response = Response(
                {"success": False, "response": "você tentou fazer cafuné em si mesmo..."}
            )
            pat: Response = Response({"success": False, "response": "você fez cafuné em @{} 😊"})

        class Penis(EnUsTranslations.Interactive.Penis):
            bot: Response = Response({"success": False, "response": "eu só tenho pen drive."})
            penis: Response = Response({"success": False, "response": "{} tem {}cm {}"})

        class Slap(EnUsTranslations.Interactive.Slap):
            bot: Response = Response({"success": False, "response": "vai bater na mãe 😠."})
            yourself: Response = Response(
                {"success": False, "response": "você se deu um tapa... 😕."}
            )
            slap: Response = Response(
                {"success": False, "response": "você deu um tapa em @{} 👋"}
            )

        class Tuck(EnUsTranslations.Interactive.Tuck):
            bot: Response = Response({"success": False, "response": "eu não posso dormir agora."})
            yourself: Response = Response(
                {"success": False, "response": "você foi para a cama 🛏"}
            )
            tuck: Response = Response(
                {"success": False, "response": "você colocou @{} na cama 🙂👉🛏"}
            )

    class Markov(EnUsTranslations.Markov):
        class Markov(EnUsTranslations.Markov.Markov):
            channel_not_found: Response = Response(
                {"success": False, "response": "@canal não encontrado no meu banco de dados."}
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
            markov_generated: Response = Response({"success": False, "response": "{}"})

    class Marry(EnUsTranslations.Marry):
        class Marry(EnUsTranslations.Marry.Marry):
            bot: Response = Response(
                {
                    "success": False,
                    "response": "não fui programado para fazer parte de um relacionamento.",
                    "is_response": False,
                }
            )
            yourself: Response = Response(
                {"success": False, "response": "você não pode se casar com você mesmo..."}
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
                {"success": False, "response": "vocês dois já são casados... não se lembra?"}
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
                {"success": False, "response": "{}, não há nenhum pedido de casamento para você."}
            )

            proposal_denied: Response = Response(
                {"success": False, "response": "{}, você recusou o pedido de casamento de @{} 💔"}
            )

            timeout: Response = Response(
                {
                    "success": False,
                    "response": "o tempo para pensar acabou, caso descidão se casar de novo use o comando novamente.",
                    "is_response": False,
                }
            )

        class Divorce(EnUsTranslations.Marry.Divorce):
            bot: Response = Response(
                {"success": False, "response": "eu nunca estaria casado com você."}
            )
            yourself: Response = Response(
                {"success": False, "response": "você não pode se livrar de você mesmo."}
            )
            not_married: Response = Response(
                {"success": False, "response": "você não está casado com ninguém."}
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

        class MarryAge(EnUsTranslations.Marry.MarryAge):
            bot: Response = Response(
                {"success": False, "response": "nunca me casarei com ninguém."}
            )
            user_not_found: Response = Response(
                {
                    "success": False,
                    "response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    "is_response": False,
                }
            )
            not_married: Response = Response(
                {"success": False, "response": "{} não esta casado com ninguém."}
            )
            married: str = "@{} está casado com @{} há {}"
            divorced: str = "@{} está separado de @{} há {} e quem pediu o divórcio foi @{}"
            response: Response = Response({"success": False, "response": ""})

    class Pet(EnUsTranslations.Pet):
        PetsDict: PetsDict = pets
        FromListToPetList = from_list_to_pet_list

        class Pet(EnUsTranslations.Pet.Pet):
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
                {"success": False, "response": "@{} optou por não permitir ser mencionado."}
            )
            pets: Response = Response({"success": False, "response": "{} possui {}"})
            no_pets: Response = Response(
                {
                    "success": False,
                    "response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    "is_response": False,
                }
            )
            user_no_pets: Response = Response(
                {"success": False, "response": "{} não possui nenhum pet."}
            )

        class PetBuy(EnUsTranslations.Pet.PetBuy):
            no_cookies: Response = Response(
                {
                    "success": False,
                    "response": "comece a estocar cookies para adquirir um pet ({}stock)",
                    "is_response": False,
                }
            )
            not_enough_cookies: Response = Response(
                {"success": False, "response": "estoque {} cookies para adquirir {}"}
            )
            name_too_large: str = (
                "vamos maneirar no tamanho do nome, " "tente novamente desta vez com um nome menor que 32 caracteres."
            )
            timeout: Response = Response(
                {"success": False, "response": "o tempo para comprar acabou tente novamente."}
            )
            timeout_response: Response = Response(
                {"success": False, "response": "você demorou de mais para responder."}
            )
            what_name: str = "qual nome você gostaria de da-lo?"
            are_you_sure: str = "tem certeza que deja nomear de {}? (yes ou no)"
            pet_name: str = "o seu pet sera nomeado {}"
            pet_buy: Response = Response(
                {"success": False, "response": "você adquiriu {} {} por {} cookies."}
            )
            no_options: Response = Response(
                {"success": False, "response": "escolha um dos pets disponíveis hoje ({}petlist)"}
            )

        class PetList(EnUsTranslations.Pet.PetList):
            pet_list: Response = Response(
                {"success": False, "response": "pets disponíveis (adquira com {}petbuy): {}"}
            )

        class PetName(EnUsTranslations.Pet.PetName):
            no_pets: Response = Response(
                {"success": False, "response": "Você não tem pets para dar nome."}
            )
            what_pet_to_name: str = (
                "qual dos pets você quer nomear: {}? " "(mande o número do pet que você gostaria de mudar.)"
            )
            timeout: Response = Response(
                {"success": False, "response": "você demorou de mais para responder."}
            )
            what_name: str = "qual nome você quer dar para {}?"
            new_name: Response = Response(
                {"success": False, "response": "o nome do pet foi mudado para {} ."}
            )

        class PetPat(EnUsTranslations.Pet.PetPat):
            no_pet_name: Response = Response(
                {"success": False, "response": "você não especificou o nome do pet."}
            )
            no_pets: Response = Response(
                {"success": False, "response": "você fez carinho em {} {}"}
            )
            pet_pat: Response = Response(
                {
                    "success": False,
                    "response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    "is_response": False,
                }
            )
            wrong_pet_name: Response = Response(
                {"success": False, "response": "você não tem um pet com este nome.."}
            )

        class PetSell(EnUsTranslations.Pet.PetSell):
            pass

    class Profile(EnUsTranslations.Profile):
        class Mention(EnUsTranslations.Profile.Mention):
            mention_on: Response = Response(
                {
                    "success": False,
                    "response": "outros usuários poderão mencionar você novamente nos comandos.",
                    "is_response": False,
                }
            )

        class NickName(EnUsTranslations.Profile.NickName):
            nickname_too_large: Response = Response(
                {
                    "success": False,
                    "response": "o apelido {} é muito grande, por favor tente manter com no máximo 32 caracteres.",
                    "is_response": False,
                }
            )
            nickname_removed: Response = Response(
                {"success": False, "response": "seu apelido foi removido com sucesso!"}
            )
            nickname_changed: Response = Response(
                {"success": False, "response": "você alterou seu de apelido para {} com sucesso!"}
            )

        class SaveCity(EnUsTranslations.Profile.SaveCity):
            city_removed: Response = Response(
                {"success": False, "response": "Cidade foi removida com sucesso!."}
            )
            city_added: Response = Response(
                {
                    "success": False,
                    "response": "Você salvou {} como sua cidade, agora basta usar {}weather.",
                    "is_response": False,
                }
            )

        class SaveColor(EnUsTranslations.Profile.SaveColor):
            color_removed: Response = Response(
                {"success": False, "response": "a cor foi removida com sucesso!"}
            )
            color_added: Response = Response(
                {
                    "success": False,
                    "response": 'você salvou a cor {} e pode visualizá-la usando "{}color"',
                    "is_response": False,
                }
            )

        class UnMention(EnUsTranslations.Profile.UnMention):
            mention_off: Response = Response(
                {
                    "success": False,
                    "response": "agora outros usuários não poderão mais mencionar você nos comandos.",
                    "is_response": False,
                }
            )

    class Reminder(EnUsTranslations.Reminder):
        class Remind(EnUsTranslations.Reminder.Remind):
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
                {"success": False, "response": "o usuário {} optou por desligar os reminds para."}
            )
            author_too_much_reminds: Response = Response(
                {"success": False, "response": "já existem muitos lembretes seus pendentes..."}
            )
            user_too_much_reminds: Response = Response(
                {"success": False, "response": "já existem muitos lembretes pendentes para {}"}
            )
            time_not_found: Response = Response(
                {"success": False, "response": "não entendi o tempo que você me passou."}
            )
            remind_on_back: Response = Response(
                {
                    "success": False,
                    "response": "{} será lembrado disso na próxima vez que falar no chat 📝 (ID {})",
                    "is_response": False,
                }
            )
            dont_have_time_machine: Response = Response(
                {"success": False, "response": "eu ainda não inventei a máquina do tempo."}
            )
            minimum_time: Response = Response(
                {
                    "success": False,
                    "response": "o tempo mínimo para lembretes cronometrados é 1 minuto.",
                    "is_response": False,
                }
            )
            remind_on_time: Response = Response(
                {"success": False, "response": "{} será lembrado disso em {}. ⏲️(ID {})"}
            )

        class Reminds(EnUsTranslations.Reminder.Reminds):
            remind_for: Response = Response(
                {"success": False, "response": "esse lembrete é para {}: {}."}
            )
            remind_timed_with_content: Response = Response(
                {"success": False, "response": "esse lembrete é para {} em {}: {}."}
            )
            remind_timed_without_content: Response = Response(
                {"success": False, "response": "esse lembrete era para {} há {}."}
            )
            remind_deleted: Response = Response(
                {"success": False, "response": "seu lembrete de ID {} foi deletado."}
            )
            remind_not_found: Response = Response(
                {"success": False, "response": "você não possui nenhum lembrete com esse ID."}
            )
            no_id_selected: Response = Response(
                {
                    "success": False,
                    "response": "você deve passar o ID do lembrete que quer deletar.",
                    "is_response": False,
                }
            )
            author_reminds: Response = Response(
                {"success": False, "response": "seus lembretes pendentes são os de ID: {}."}
            )
            author_dont_have_reminds: Response = Response(
                {"success": False, "response": "você não tem lembretes pendentes."}
            )

        class RemindListener(EnUsTranslations.Reminder.RemindListener):
            remind_timed_with_content: Response = Response(
                {"success": False, "response": "{} deixou um lembrete: {} (há {})"}
            )
            remind_timed_without_content: Response = Response(
                {"success": False, "response": "{} deixou um lembrete em branco (há {})"}
            )

    class Settings(EnUsTranslations.Settings):
        class BanWord(EnUsTranslations.Settings.BanWord):
            word_added: Response = Response(
                {"success": False, "response": "esse já é um termo banido."}
            )
            word_already_on_list: Response = Response(
                {
                    "success": False,
                    "response": "não irei mais enviar mensagens que tiverem esse termo.",
                    "is_response": False,
                }
            )

        class Disable(EnUsTranslations.Settings.Disable):
            command_dont_exist: Response = Response(
                {"success": False, "response": "esse comando não existe."}
            )
            command_cannot_be_disabled: Response = Response(
                {"success": False, "response": "não pode ser desativado."}
            )
            command_already_disabled: Response = Response(
                {"success": False, "response": '"{}" já está desativado.'}
            )
            command_disabled: Response = Response(
                {"success": False, "response": '"{}" foi desativado.'}
            )

        class Enable(EnUsTranslations.Settings.Enable):
            command_dont_exist: Response = Response(
                {"success": False, "response": "esse comando não existe."}
            )
            command_reactivated: Response = Response(
                {"success": False, "response": '"{}" foi reativado.'}
            )
            command_already_activated: Response = Response(
                {"success": False, "response": '"{}" já está ativado.'}
            )

        class Prefix(EnUsTranslations.Settings.Prefix):
            prefix_invalid: Response = Response(
                {"success": False, "response": "este prefixo {prefixo} é invalido"}
            )
            prefix_invalid_or_absent: Response = Response(
                {"success": False, "response": "Esqueceu de mandar o prefixo ou ele é invalido."}
            )
            prefix_already_in_use: Response = Response(
                {"success": False, "response": "O canal ja esta usando o prefixo {prefixo}."}
            )
            prefix_changed: Response = Response(
                {"success": False, "response": 'O prefixo do canal foi alterado para "{}".'}
            )
            prefix_too_large: Response = Response(
                {
                    "success": False,
                    "response": "Atualmente eu so consigo armazenar prefixos de ate 2 caracteres o prefixo que você "
                    'tentou usar não é valido pois contem "{}" caracteres.',
                    "is_response": False,
                }
            )

        class Start(EnUsTranslations.Settings.Start):
            already_on: Response = Response({"success": False, "response": "já estou ligado ☕"})
            started: Response = Response({"success": False, "response": "você me ligou ☕"})

        class Stop(EnUsTranslations.Settings.Stop):
            stopped: Response = Response({"success": False, "response": "você me desligou 💤"})

        class UnBanWord(EnUsTranslations.Settings.UnBanWord):
            word_removed: Response = Response(
                {"success": False, "response": '"{}" foi removido dos termos banidos.'}
            )
            word_not_found: Response = Response(
                {"success": False, "response": '"{}" não é um termo banidos.'}
            )

    class Tools(EnUsTranslations.Tools):
        class Math(EnUsTranslations.Tools.Math):
            result: Response = Response({"success": False, "response": "{}"})
            error: Response = Response(
                {
                    "success": False,
                    "response": "não consegui calcular... lembre-se: use * para multiplicação, use / para divisão, "
                    "e use ponto em vez de vírgula para números decimais. {}",
                    "is_response": False,
                }
            )

        class Shorten(EnUsTranslations.Tools.Shorten):
            no_links_found: Response = Response(
                {"success": False, "response": "Use: `{}encurta <link>`"}
            )
            shorten_links: Response = Response(
                {"success": False, "response": "Aqui está os links: {}"}
            )
            shorten_link: Response = Response(
                {"success": False, "response": "Aqui está os link: {}"}
            )
            shorten_error: Response = Response(
                {"success": False, "response": "Não foi possível encurtar o link."}
            )

        class Time(EnUsTranslations.Tools.Time):
            time: Response = Response({"success": False, "response": "{}"})
            future_time: Response = Response({"success": False, "response": "em {}"})
            past_time: Response = Response({"success": False, "response": "há {}"})
            unit_not_found: Response = Response(
                {
                    "success": False,
                    "response": "as medidas suportadas atualmente são: anos, meses, semanas, dias, horas, "
                    "minutos e segundos. Caso nenhuma seja colocada, será dado o tempo completo convertido. ",
                    "is_response": False,
                }
            )
            too_much_time: Response = Response(
                {"success": False, "response": "tempo de mais para converter."}
            )

        class UserId(EnUsTranslations.Tools.UserId):
            user_not_found: Response = Response(
                {"success": False, "response": "não achei nenhum usuário com esse id."}
            )
            id_or_name: Response = Response({"success": False, "response": "{}"})

        class Weather(EnUsTranslations.Tools.Weather, WeatherTools):
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
            weather: Response = Response({"success": False, "response": ""})

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

    class Tower(EnUsTranslations.Tower):
        class EnterTower(EnUsTranslations.Tower.EnterTower):
            class_rank_up: Response = Response({"success": False, "response": "agora você é {}"})
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar continuar a escalada ⌛"}
            )
            tower_result: Response = Response({"success": False, "response": "{}"})
            class_choice: Response = Response(
                {"success": False, "response": "você escolheu {}! {}"}
            )
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! {}ed  " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class FastTower(EnUsTranslations.Tower.FastTower):
            class_to_choose: Response = Response(
                {
                    "success": False,
                    "response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    "is_response": False,
                }
            )
            cooldown: Response = Response(
                {"success": False, "response": "aguarde {} para entrar continuar a escalada ⌛"}
            )
            tower_result: Response = Response({"success": False, "response": "{}"})
            class_first_choice: Response = Response(
                {
                    "success": False,
                    "response": "antes de continuar, escolha sua classe! {}et " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    "is_response": False,
                }
            )

        class TowerLevel(EnUsTranslations.Tower.TowerLevel):
            bot_nick: Response = Response(
                {"success": False, "response": "Eu apenas conto as historias dos encontros."}
            )
            no_class_chosen: Response = Response(
                {"success": False, "response": "{} ainda não escolheu uma classe."}
            )
            player_status: Response = Response(
                {
                    "success": False,
                    "response": "{} é {} ({}, {} XP). Esta no andar {} zona {}, com um total de {} "
                    "encontros ({} vitórias, {} derrotas, {.2f}% winrate) ♦",
                    "is_response": False,
                }
            )
            player_not_found: Response = Response({"success": False, "response": ""})
