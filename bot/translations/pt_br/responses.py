from __future__ import annotations

from typing import Any, TYPE_CHECKING

from bot.translations import EnTranslations
from bot.translations.en.extras import Response
from bot.translations.pt_br.extras import Humanize, WeatherTools
from bot.translations.pt_br.extras import from_list_to_pet_list, pets, PetsDict
from bot.translations.pt_br.extras import fight_option
from bot.translations.pt_br.extras import dungeon_rank_dict
from bot.translations.pt_br.extras import Activity as ActivityExtras
from bot.translations.pt_br.extras import TimeTools, Timeago
from bot.translations.pt_br.extras import Dicio
from .extras import Values, bets_values

if TYPE_CHECKING:
    from bot.ext.commands import Context


class PtBrTranslations(EnTranslations):
    class SupportTools(EnTranslations.Exceptions):
        Humanize: Humanize = Humanize

        mention: str = "você"

        class TimeTools(EnTranslations.SupportTools.TimeTools):
            TimeTools: TimeTools = TimeTools
            Timeago: Timeago = Timeago
            strftime: str = "%H:%M:%S %d-%m-%Y"

        class Lottery(EnTranslations.SupportTools.Lottery):
            bet_or_consultation: list[str] = ["aposta", "consultar"]

        class Dicio(EnTranslations.SupportTools.Dicio):
            Dicio: Dicio = Dicio

    class Exceptions(EnTranslations.Exceptions):
        class LotteryExceptions(EnTranslations.Exceptions.LotteryExceptions):
            lottery_seed: str = "algo horrível aconteceu, contate \"@{}\" aqui na twitch utilizando whispers."

        class ToolsExceptions(EnTranslations.Exceptions.ToolsExceptions):
            announcement: str = "algo de errado com o anuncio. {}"

        class BotMainLoopExceptions(EnTranslations.Exceptions.BotMainLoopExceptions):
            dev_required: str = "você precisa ser meu criador para executar esse comando."
            owner_required: str = "comandos reservados para o dono do bot."
            command_on_cooldown: str = "para usar o comando de novo volte {}."
            not_implemented: str = "esse comando está temporariamente desativado."

            error_not_registered: str = "ocorreu um erro inesperado, por favor, reporte o erro para @{}"

        class ResponseExceptions(EnTranslations.Exceptions.ResponseExceptions):
            error_on_command: str = "um erro aconteceu no comando \"{}\""
            pipe_response: str = "aqui está a resposta que foi gerada pelo comando anterior: {}"
            command_not_pipeble: str = "este comando não pôde ser utilizado com o pipe."

    class Admin(EnTranslations.Admin):
        class Nada(EnTranslations.Admin.Nada):
            nada: Response = Response({
                    "success": True,
                    "response": "O comando foi executado com sucesso. {}"})

        class Reload(EnTranslations.Admin.Reload):
            commands_reloaded: Response = Response({
                    "success": True,
                    "response": "Os comandos foram recarregados com sucesso."})

        class Restart(EnTranslations.Admin.Restart):
            success: Response = Response({"response": "O bot foi reiniciado com sucesso."})
            unexpected_error: Response = Response({"response": "Houve um erro ao reiniciar o bot: {}"})

    class Others(EnTranslations.Others):
        class Pipe(EnTranslations.Others.Pipe):
            response: Response = Response({"response": "Pipe não é realmente um comando. "
                                                       "Para mais informações, visite este link: {}"})

    class Afk(EnTranslations.Afk):
        afks: dict[str, ActivityExtras.Status] = ActivityExtras.afks

        class Afk(EnTranslations.Afk.Afk):
            message_too_long: Response = Response({"response": "Esta mensagem é muito longa."})
            afk_response: Response = Response({"success": True, "response": "{}: {}"})
            afk_content_response: Response = Response(
                {"success": True, "response": "{}: {} e deixou uma nota com: {}"})

        class IsAfk(EnTranslations.Afk.IsAfk):
            bot_nick: Response = Response(
                {"response": "eu sempre estou aqui... observando."}
            )
            author_nick: Response = Response(
                {"response": "você não está trabalhando... obviamente"}
            )
            never_seen: Response = Response(
                {"response": "não lembro de ja ter visto nenhum {}."}
            )
            is_afk: Response = Response({"response": "@{} {}: {}"})
            is_afk_content: Response = Response(
                {"response": "@{} {} e deixou um bilhete: {}"}
            )
            is_not_afk: Response = Response({"response": "@{} não está Afk."})

        class RAfk(EnTranslations.Afk.RAfk):
            time_expired: Response = Response({"response": "O tempo para voltar já passou.",
                    "pipe": False})
            is_afk: Response = Response({"response": "{}: {}"})
            is_afk_content: Response = Response({"response": "{} {} e deixou um bilhete: {}"})
            is_not_afk: Response = Response({"response": "voce não está afk."})

        class AfkListeners(EnTranslations.Afk.AfkListeners):
                is_afk: Response = Response({"response": "{}: {} (ficou {} {})"})
                is_afk_content: Response = Response(
                        {"response": "{} {} e deixou um nota: {} (ficou {} {})"})

    class Alias(EnTranslations.Alias):
        user_not_found: Response = Response({"response": "não há usuário com nome de {}."})

        dont_have_alias: Response = Response({"response": "Você não tem alias com nome de \"{}\""})

        alias_invalid_name: Response = Response({"response": "O nome do seu aliás não é valido. "
                                                             "Seu alias deve conter apenas letras, "
                                                             "números e ter de 2 a 30 caracteres."})

        user_has_no_alias: Response = Response({"response": "O usuário {} não têm nenhum aliás registrado."})

        alias_table_headers: list[str] = [
                "Nome do alias", "Descrição", "Invoca", "Argumentos", "Link para", "Atualizado", "Criado"
        ]

        alias_table_replaces: list[str] = ["Sem descrição", "Sem argumentos", "Nenhum"]

        alias_table_name: str = "Aliases de {}"

        class Add(EnTranslations.Alias.Add):
            no_command_to_add: Response = Response({"response": "Você não enviou um comando! "
                                                                "Uso: {}alias add (name) (command) (...arguments)"})

            alias_name_conflict: Response = Response({"response": "Não é possível adicionar o alias \"{}\" - "
                                                                  "você já tem um com este nome! Você pode \"edit\" "
                                                                  "sua definição, \"rename\" ou \"remove\"."})

            alias_crated: Response = Response({"response": "Seu alias \"{}\" foi criado com sucesso."})

            command_dont_exist: Response = Response({"response": "Não é possível criar o alias! "
                                                                 "O comando \"{}\" não existe."})

        class Check(EnTranslations.Alias.Check):
            user_alias_list: Response = Response({"response": "Sua lista de alias: {} | Lista detalhada: {}"})

            no_alias_found: Response = Response({"response": "Não consegui encontrar {} no do usuário {} "
                                                             "ou em qualquer um dos seus aliases!"})

            list_of_alias_of: Response = Response({"response": "Lista de alias do {}: {}"})

            list_of_special_case: Response = Response({
                "response": "Caso Especial! \n"
                            "Seu alias \"{0}\": {1}\n"
                            "Lista de alias de {0}: {2}"})

            alias_not_found: Response = Response({"response": "{} não tem o alias \"{}\""})

            alias_deleted: Response = Response({"response": "O alias \"{}\" é um link para um alias diferente, "
                                                            "mas o original foi excluído."})

            appendix_message: Response = Response({"response": "Este alias é um link para \"{}\" feito por {}. "
                                                               "O alias \"{}\" tem os argumentos: {} || Link: {}"})

            normal_message: Response = Response({"response": "O alias \"{}\" tem os argumentos: {} || Link: {}"})

        class Copy(EnTranslations.Alias.Copy):
            user_not_provided: Response = Response({"response": "Nenhum usuário foi fornecido!"})

            alias_not_provided: Response = Response({"response": "Nenhum alias de destino fornecido!"})

            target_alias_invalid_name: Response = Response({"response": "O nome do alias a ser copiado não é válido e, "
                                                                        "portanto, não pode ser copiado!"})

            no_alias_found: Response = Response({"response": "Não consegui encontrar {} no usuário {}!"})

            link_to_a_link: Response = Response({"response": 'Você não pode copiar links para outros aliases. '
                                                             'Em vez disso, use o link {}alias copy {} {}'})

            copy_success: Response = Response({"response": "Alias \"{}\" copiado com sucesso."})

            copy_with_name_of: Response = Response({"response": "Alias \"{}\" copiado com sucesso. "
                                                                "Com o nome de \"{}\"."})

        class Describe(EnTranslations.Alias.Describe):
            no_args_to_parse: Response = Response({"response": "Você não forneceu um alias ou descrição! "
                                                               "Use: {}alias describe <alias> <descrição>"})

            description_updated: Response = Response({"response": "A descrição do alias \"{}\" "
                                                                  "foi atualizada com sucesso."})

            description_reverted: Response = Response({"response": "A descrição do alias \"{}\" "
                                                                   "foi redefinida com sucesso."})

        class Edit(EnTranslations.Alias.Edit):
            no_args_provided: Response = Response({"response": "Nenhum alias ou nome de comando fornecido!"})

            edit_link: Response = Response({"response": "Você não pode editar links para outros aliases!"})

            edit_success: Response = Response({"response": 'O alias "{}" foi editado com sucesso.'})

            command_dont_exist: Response = Response({"response": 'Não é possível editar o alias! '
                                                                 'O comando "{}" não existe.'})

        class Link(EnTranslations.Alias.Link):
            link_no_args: Response = Response({"response": "Você não forneceu um usuário ou o nome do alias! "
                                                           "Use: {}alias link (usuário) (nome do alias)"})

            alias_name_already_exists: Response = Response({"response": "Não é possível vincular um novo alias - "
                                                                        "você já tem um alias com esse nome!"})

            user_dont_has_alias: Response = Response({"response": 'O usuário fornecido não tem o alias "{}"!'})

            link_with_invalid_name: Response = Response({"response": 'O nome do alias vinculado não é válido! {}'})

            link_name_string: str = ', com um nome personalizado de "{}". '

            link_to_link: Response = Response({"response": "Você tentou criar um link a partir de um alias link"
                                                           " (alias \"{}\" por {}), então usei o original como seu "
                                                           "modelo{} Quando o original mudar, o seu também mudará. "})

            link_success: Response = Response({"response": 'Alias vinculado com sucesso{} '
                                                           'Quando o original mudar, o seu também mudará.'})

        class Remove(EnTranslations.Alias.Remove):
            no_alias_name_provided: Response = Response({"response": "Nenhum nome de alias fornecido!"})

            alias_removed: Response = Response({"response": 'Seu alias "{}" foi removido com sucesso.'})

        class Rename(EnTranslations.Alias.Rename):
            no_name_provided: Response = Response({"response": "Você deve fornecer tanto o nome "
                                                               "atual do alias quanto o novo!"})

            alias_already_exists: Response = Response({"response": 'Você já tem o alias "{}"!'})

            alias_renamed: Response = Response({"response": 'Seu alias "{}" foi renomeado com sucesso para "{}".'})

    class Chance(EnTranslations.Chance):
        random_percentage: Response = Response({"response": "{:.2f}%."})

    class Choice(EnTranslations.Choice):
        choice_separators: list[str] = EnTranslations.Choice.base_separators + ["ou"]
        chosen_option: Response = Response({"response": "{}"})

    class Count(EnTranslations.Count):
        character_count: Response = Response({"response": "Há um total de {} caracteres. "
                                                          "Dentre eles, {} são pontuações, {} "
                                                          "são letras maiúsculas e {} são caracteres especiais."})

    class HyperTranslate(EnTranslations.HyperTranslate):
        lang: str = "pt"

        quantity_error: Response = Response({"response": "Você deve informar a quantidade de vezes que vai ser "
                                                         "traduzido. Como exemplo: `{}hypertranslate 10 <texto>`"})

        starter_string: str = "Estou traduzindo o texto..."

        unexpected_error: Response = Response({"response": "Não foi possível traduzir o texto."})

        translation: Response = Response({"response": "{}"})

    class NSFW(EnTranslations.NSFW):
        class Imgur(EnTranslations.NSFW.Imgur):
            links: Response = Response({"response": ""})

            time_message: str = "Tempo: {} "

            all_images_embed: str = "Todas as imagens que foram geradas: {} "

            all_images_embed_time: str = "Tempo: {} || Todas as imagens: {} "

            timeout: Response = Response({"response": "100 segundos se passaram e eu não consegui gerar. "
                                                      "Espere um pouco e tente novamente."})

        class ImgurRepeated(EnTranslations.NSFW.ImgurRepeated):
            links_repeated: Response = Response({"response": "Quantidade total de imagens repetidas: {} || Imagens: {}"})
            no_repeated: Response = Response({"response": "Nenhuma imagem repetida."})

        class Boru(EnTranslations.NSFW.Boru):
            original: str = "Original"
            preview: str = "Preview"
            pls_wait: str = "por favor espera um pouco, estou gerando os links."
            unexpected_error: Response = Response({"response": "{}"})
            success: Response = Response({"response": "{}"})
            too_much_tags: Response = Response({"response": "Quantidade de tags ultrapassou o limite permitido de {}."})

    class RandomColor(EnTranslations.RandomColor):
        response_url: Response = Response({"response": "#{} é {}. {}"})

    class Reverse(EnTranslations.Reverse):
        reversed_string: Response = Response({"response": "{}"})

    class RandomLine(EnTranslations.RandomLine):
        channel_not_found: Response = Response({"response": "Não encontrei nenhum canal com o nome @{} ."})
        user_not_found: Response = Response({"response": "Não encontrei nenhum usuário com o nome @{}."})
        no_message_found: Response = Response({"response": "Não foi possível encontrar nenhuma mensagem de @{} em @{}."})
        random_line: Response = Response({"response": "{} (enviada há {} por @{})"})

    class Scp(EnTranslations.Scp):
        links: Response = Response({})
        unexpected_error: Response = Response({"response": "Aconteceu algum erro, tente novamente."})

    class UpSideDown(EnTranslations.UpSideDown):
        upsidedown: Response = Response({"response": "{}"})

    class Wikihow(EnTranslations.Wikihow):
        url: str = "https://pt.wikihow.com/Especial:Randomizer"
        links: Response = Response({})
        unexpected_error: Response = Response({"response": "Aconteceu algum erro, tente novamente."})

    class Wikipedia(EnTranslations.Wikihow):
        url: str = "https://pt.wikipedia.org/wiki/Special:Random"
        links: Response = Response({})
        unexpected_error: Response = Response({"response": "Aconteceu algum erro, tente novamente."})

    class Annotations(EnTranslations.Annotations):
        too_much_characters: Response = Response({"response": "A anotação deve ter no máximo 450 caracteres."})
        title_too_long: Response = Response({"response": "O titulo deve ter no máximo 32 caracteres."})
        too_few_characters: Response = Response({"response": "Você se esqueceu de enviar o conteúdo da anotação."})
        annotation_created: Response = Response({"response": "Anotação criada com sucesso. 📝 (ID: {})"})
        no_annotations_with_id: Response = Response({"response": "Você não possui nenhuma anotação com o ID {}."})
        all_annotations: Response = Response({"response": "Suas anotações são as de ID: {}"})
        annotation_content: Response = Response({"response": "{}"})
        deleted: Response = Response({"response": "Sua anotação de ID {} foi deletada com sucesso. 🗑"})
        id_not_provided: Response = Response({"response": "{} não é um ID válido."})
        option_not_recognized: Response = Response({"response": "As opções válidas são apenas "
                                                                "\"add\" \"check\" \"delete\""})

    class Lottery(EnTranslations.Lottery):
        bets_values: list[Values] = bets_values
        past: list[str] = EnTranslations.Lottery.past_base + ["velhas", "passadas"]
        current: list[str] = EnTranslations.Lottery.current_base + ["atuais", "novas"]
        only_numbers: Response = Response({"response": "Envie apenas números de 1 a 60."})
        duplicate_numbers: Response = Response({"response": "Por favor, escolha números não repetidos."})
        not_enough_cookies: Response = Response({"response": "Você não tem cookies suficientes para fazer uma aposta. "
                                                             "O valor mínimo é 5 cookies."})
        not_enough_cookies_more_five: Response = Response({"response": "Você não tem cookies suficientes para fazer "
                                                                       "uma aposta. A quantidade de cookies que vc "
                                                                       "precia é {}"})
        bet_place: Response = Response({"response": "A aposta foi criada com os números {} e o valor de {} cookies. "
                                                    "(ID: {})"})
        lottery_lock: Response = Response({"response": "Desculpe, a lotérica está fechada enquanto os resultados "
                                                       "estão sendo computados."})
        timeout: Response = Response({"response": "Você demorou muito tempo para escolher uma opção."})
        too_much_numbers: Response = Response({"response": "Você não pode apostar em mais de 15 números."})
        minimum_bet: Response = Response({"response": "Por favor, escolha no mínimo 3 números."})

        no_bet_id: Response = Response({"response": "Você não tem nenhuma aposta com este ID."})
        ticket_info: Response = Response({"response": "Aposta com os números: {} no valor de {} criada há {}."})
        no_old_bets_found: Response = Response({"response": "Você não possui nenhuma aposta passada/fechada."})
        old_bets: Response = Response({"response": "Suas apostas passadas são: {}, com o valor total de {}."})
        no_active_bets_found: Response = Response({"response": "Você não possui nenhuma aposta ativa na rodada atual."})
        active_bets: Response = Response({"response": "Suas apostas atuais são: {}, com o valor total de {}."})
        no_bets: Response = Response({"response": "Você não tem nenhuma aposta feita até agora."})
        all_bets: Response = Response({"response": "Todas as suas apostas são: {}, com o valor total de {}."})
        unknown_option: Response = Response({"response": "As opções da lotérica sao: \"create\" e \"check\"."})
        lottery_announce_messages: list[str] = [
                "Em 30 minutos a lotérica vai começar calcular os resultados o prêmio total é de {}, use {}lottery "
                "create <números> para participar.",
                "Em 15 minutos a lotérica vai começar calcular os resultados.",
                "Em 1 minuto a lotérica vai começar calcular os resultados.",
                "Loteria fechada, começando a computar os resultados.",
        ]

        winners: str = ("Os números sorteados foram: {}, todos os ganhadores serão notificados com um remind com os "
                        "valores e números sorteados.")

        no_winners: str = ("Os números sorteados foram: {}, não houve ganhadores, o premio de {} acumulou para o "
                           "próximo sorteio.")

        lottery_result_announce: str = "A loteria acabou e aqui estão os resultado: {}"
        remind_message: str = "Você ganhou {} cookies na lotérica! Os tickets ganhadores foram: {}"

    class Cookies(EnTranslations.Cookies):
        pass

    class Copy(EnTranslations.Copy):
        class Copy(EnTranslations.Copy.Copy):
            success: Response = Response({"response": "o id da copypasta {}"})
            copy: Response = Response({"response": "{}"})
            wrong_id: Response = Response(
                {"response": "não existe copypasta com esse id."}
            )

        class DeleteCopy(EnTranslations.Copy.DeleteCopy):
            deleted: Response = Response(
                {"response": "a copypasta de id {} foi deletada."}
            )
            not_owner: Response = Response(
                {"response": "você precisa ser o criador da copy para apagar."}
            )
            error: Response = Response(
                {"response": "envie {}delcopy delete {} para deletar."}
            )

        class RandomCopy(EnTranslations.Copy.RandomCopy):
            success: Response = Response({"response": "{}"})

    class Dungeons(EnTranslations.Dungeons):
        dungeonrank_dict = dungeon_rank_dict

        class DungeonLevel(EnTranslations.Dungeons.DungeonLevel):
            bot_nick: Response = Response(
                {"response": "eu apenas crio as dungeons..."}
            )
            no_class_chosen: Response = Response(
                {"response": "{} ainda não escolheu a nova classe"}
            )
            player_status: Response = Response(
                {"response": "{} é {} ({}, {} XP) com {} dungeons ({} vitórias, {} derrotas, {:.2f}% winrate) ♦",
                    
                }
            )
            player_not_found: Response = Response(
                {"response": "{} ainda não entrou em nenhuma dungeon"}
            )

        class DungeonRank(EnTranslations.Dungeons.DungeonRank):
            winrate: Response = Response(
                {"response": "top {} {}: {} || você é o {}º no ranking com {:.2f}% {}.",
                    
                }
            )
            player_rank = "|| Você está na posição {}º no ranking com {} {}."
            normal: Response = Response({"response": "top {} {}: {} {}"})

        class DungeonEnter(EnTranslations.Dungeons.DungeonEnter):
            class_rank_up: Response = Response({"response": "agora você é {}"})
            class_to_choose: Response = Response(
                {"response": "antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    
                }
            )
            dungeon_result: Response = Response({"response": "{}"})
            cooldown: Response = Response(
                {"response": "aguarde {} para entrar em outra dungeon ⌛"}
            )
            class_choice: Response = Response(
                {"response": "você escolheu {}! {}"}
            )
            class_first_choice: Response = Response(
                {"response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    
                }
            )

        class DungeonFast(EnTranslations.Dungeons.DungeonFast):
            class_to_choose: Response = Response(
                {"response": "antes de continuar, digite '{}ed' e sua nova classe: {} ou {}",
                    
                }
            )
            cooldown: Response = Response(
                {"response": "aguarde {} para entrar em outra dungeon ⌛"}
            )
            dungeon_result: Response = Response({"response": "{}"})
            class_first_choice: Response = Response(
                {"response": "antes de continuar, escolha sua classe! "
                    "Digite {}ed Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    
                }
            )

    class General(EnTranslations.General):
        class BotInfo(EnTranslations.General.BotInfo):
            info: Response = Response(
                {"response": "estou conectado à {} canais, com {} comandos, "
                    '"feito" por @{} em Python (Twitchio). '
                    "Site do boto: {}",
                    
                }
            )
            site: Response = Response({"response": "{}"})
            uptime: Response = Response({"response": "eu acordei há {}"})

        class Bug(EnTranslations.General.Bug):
            bug_id: Response = Response(
                {"response": "seu bug foi reportado 🐛 (ID {})"}
            )

        class Channels(EnTranslations.General.Channels):
            quantity: Response = Response(
                {"response": "estou conectado em {quantidade} canais."}
            )
            names: Response = Response({"response": "{}"})

        class Color(EnTranslations.General.Color):
            user_not_found: Response = Response(
                {"response": "eu não encontrei ninguém com o nick de {} e isso também não é uma cor valida.",
                    
                }
            )
            unexpected_error: Response = Response(
                {"response": "Veja o nome da cor pelo HEX ou a cor de alguém pelo nick. "
                    "Ex: {}cor ff00ff ou {}cor {}",
                    
                }
            )
            user_has_no_color = "o usuário {} não tem nenhuma cor salva."
            user_color = "{} cor salva"
            author_color = "sua cor salva é"
            response: Response = Response({"response": "{}"})
            response_link: Response = Response(
                {"response": "{} é {}. https://goo.gl/search?%23{} {}"}
            )

        class Dict(EnTranslations.General.Dict):
            word_not_found: Response = Response(
                {"response": "não encontrei a palavra {} no www.dicio.com.br"}
            )
            word: Response = Response(
                {"response": "A palavra '{}' existe em {}"}
            )

        class Echo(EnTranslations.General.Echo):
            echo: Response = Response({"response": "{}"})

        class Help(EnTranslations.General.Help):
            command_site: Response = Response(
                {"response": "veja todos os comandos: https://gorenmu.vercel.app/docs/intro",
                    
                }
            )
            command: Response = Response(
                {"response": "{}{}: {} | Comando no site: {}"}
            )
            command_aliases: Response = Response(
                {"response": "{}{} ({}): {} | Comando no site: {}"}
            )

        class Join(EnTranslations.General.Join):
            join_message = (
                "Opa. Fui convidado a me instalar aqui, caso queira saber meus comandos entre em "
                '" {} " ou mande {}help. Se o bot cair manda whisper ou mensagem no '
                "chat do {} ."
            )
            already_in_channel_disabled: Response = Response(
                {"response": "Eu nunca sai do canal {} e vc pôde me ativar novamente usando {}start !",
                    
                }
            )
            joined: Response = Response(
                {"response": "Entrei no canal com sucesso!"}
            )
            already_in_channel: Response = Response(
                {"response": "Ja estou no canal {}!"}
            )

        class LastSeen(EnTranslations.General.LastSeen):
            bot_nick: Response = Response(
                {"response": "eu estou em todos os lugares, a todo momento..."}
            )
            author: Response = Response(
                {"response": "você foi visto pela última vez aqui ☝️"}
            )
            author_not_found: Response = Response(
                {"response": "@{name} ainda não foi registrado (não usou nenhum comando)",
                    
                }
            )
            not_authorized: Response = Response(
                {"response": "esse usuário optou por não permitir mencioná-lo"}
            )
            last_seen: Response = Response(
                {"response": "@{} foi visto em @{} pela última vez: {} (há {})"}
            )

        class Leave(EnTranslations.General.Leave):
            not_in_channel: Response = Response(
                {"response": "Eu não estou no seu canal {}!"}
            )
            left: Response = Response({"response": "{} removido com sucesso!"})

        class Nicks(EnTranslations.General.Nicks):
            user_not_found: Response = Response(
                {"response": "não encontrei ninguem com nome de {} no meu banco de dados.",
                    
                }
            )
            nicks: Response = Response({"response": "{}"})
            last_nick: Response = Response({"response": "{} → {}"})
            no_nick: Response = Response(
                {"response": "nenhuma mudança de nick registrada ainda."}
            )

        class Ping(EnTranslations.General.Ping):
            ping: Response = Response(
                {"response": "{} || RAM usada {} pelo python || {}"}
            )

        class PopOut(EnTranslations.General.PopOut):
            url: Response = Response(
                {"response": "https://www.twitch.tv/popout/{}/chat?popout="}
            )

        class Preview(EnTranslations.General.Preview):
            no_stream: Response = Response(
                {"response": "este usuário não esta em live."}
            )
            response: Response = Response({"response": "{}"})

        class Spam(EnTranslations.General.Spam):
            content_not_valid: Response = Response(
                {"response": "Por favor, digite um conteúdo para o spam."}
            )
            number_not_valid: Response = Response(
                {"response": "'{}' não é um número."}
            )
            response: Response = Response({"response": ""})

        class Suggest(EnTranslations.General.Suggest):
            suggest_id: Response = Response(
                {"response": "sua sugestão foi anotada 📝 (ID {})"}
            )

    class Infos(EnTranslations.Infos):
        class AccountAge(EnTranslations.Infos.AccountAge):
            user_not_found: Response = Response(
                {"response": "@{} é um usuário inválido."}
            )
            birthday_year: Response = Response(
                {"response": "hoje completa {} ano que {} criou a conta 🎂"}
            )
            birthday_years: Response = Response(
                {"response": "hoje completa {} anos que {} criou a conta 🎂"}
            )
            age: Response = Response(
                {"response": "{} criou a conta em {} (há {})"}
            )

        class Avatar(EnTranslations.Infos.Avatar):
            user_not_found: Response = Response(
                {"response": "minha foto de perfil: {} || {}"}
            )
            author_avatar: Response = Response(
                {"response": "Usuário {} não exites."}
            )
            bot_avatar: Response = Response(
                {"response": "sua foto de perfil: {} || {}"}
            )
            nick_avatar: Response = Response(
                {"response": "foto de perfil de @{}: {} || {}"}
            )

        class FirstFollow(EnTranslations.Infos.FirstFollow):
            first_and_follow: Response = Response(
                {"response": "{} seguiu primeiro @{} e foi seguido primeiro por @{}",
                    
                }
            )
            not_first_but_followed: Response = Response(
                {"response": "{} não segue ninguém e foi seguido primeiro por @{}",
                    
                }
            )
            follow_but_not_followed: Response = Response(
                {"response": "{} seguiu primeiro @{} e não é seguido por ninguém",
                    
                }
            )
            alone: Response = Response(
                {"response": "{} não segue e não é seguido por ninguém"}
            )

        class FollowAge(EnTranslations.Infos.FollowAge):
            user_not_found: Response = Response(
                {"response": "@{} é um usuário inválido."}
            )
            follow_yourself: Response = Response(
                {"response": "{} não pode se seguir."}
            )
            not_followed: Response = Response({"response": "{} não segue {}"})
            follow: Response = Response(
                {"response": "{} seguiu {} em {} (há {})"}
            )

        class Live(EnTranslations.Infos.Live):
            bot_nick: Response = Response(
                {"response": "eu sou um bot, não um streamer"}
            )
            user_not_found: Response = Response(
                {"response": "@{channel} é um canal inválido"}
            )
            channel_offline: Response = Response(
                {"response": "@{channel} está offline"}
            )
            stream: Response = Response(
                {"response": "{} está streamando {} para {} viewers: {} (há {})",
                    
                }
            )
            stream_with_print: Response = Response(
                {"response": "{} está streamando {} para {} viewers: {} (há {}) || Print {}",
                    
                }
            )

        class Title(EnTranslations.Infos.Title):
            bot_nick: Response = Response(
                {"response": "eu sou um bot, não um streamer."}
            )
            user_not_found: Response = Response(
                {"response": "@{} é um canal inválido"}
            )
            no_title_game: Response = Response(
                {"response": "@{} não têm nem título e nem jogo configurado."}
            )
            no_title: Response = Response({"response": "{} 🎮 {}"})
            title_no_game: Response = Response({"response": "{} 📑 {}"})
            full_title: Response = Response({"response": "{} 📑 {} | 🎮 {}"})

    class Interactive(EnTranslations.Interactive):
        class Fight(EnTranslations.Interactive.Fight):
            options: list[str] = fight_option
            bot_nick: Response = Response(
                {"response": "você nunca conseguiria me derrotar..."}
            )
            internal_fight: Response = Response(
                {"response": "você iniciou uma luta interna..."}
            )
            already_fight: Response = Response(
                {"response": "@{} já está sendo desafiado por @{}!"}
            )
            result: Response = Response({"response": "{}"})
            refused: Response = Response(
                {"response": "@{} recusou o desafio contra @{} LUL"}
            )
            timeout: Response = Response(
                {"response": "@{} não respondeu ao seu desafio a tempo"}
            )

        class Hug(EnTranslations.Interactive.Hug):
            bot: Response = Response({"response": "🤗"})
            yourself: Response = Response(
                {"response": "você tentou se abraçar..."}
            )
            hug: Response = Response({"response": "você abraçou @{} 🤗"})

        class Kiss(EnTranslations.Interactive.Kiss):
            bot: Response = Response({"response": "😳"})
            yourself: Response = Response(
                {"response": "você tentou se beijar..."}
            )
            kiss: Response = Response(
                {"response": "você deu um beijinho em @{} 😚"}
            )

        class Love(EnTranslations.Interactive.Love):
            yourself: Response = Response(
                {"response": "uma pessoa não pode ser shipada com ela mesma..."}
            )
            ship: Response = Response(
                {"response": "@{} & @{}: {} com {}% de amor {}"}
            )

        class Pat(EnTranslations.Interactive.Pat):
            bot: Response = Response({"response": "😊"})
            yourself: Response = Response(
                {"response": "você tentou fazer cafuné em si mesmo..."}
            )
            pat: Response = Response({"response": "você fez cafuné em @{} 😊"})

        class Penis(EnTranslations.Interactive.Penis):
            bot: Response = Response({"response": "eu só tenho pen drive."})
            penis: Response = Response({"response": "{} tem {}cm {}"})

        class Slap(EnTranslations.Interactive.Slap):
            bot: Response = Response({"response": "vai bater na mãe 😠."})
            yourself: Response = Response(
                {"response": "você se deu um tapa... 😕."}
            )
            slap: Response = Response(
                {"response": "você deu um tapa em @{} 👋"}
            )

        class Tuck(EnTranslations.Interactive.Tuck):
            bot: Response = Response({"response": "eu não posso dormir agora."})
            yourself: Response = Response(
                {"response": "você foi para a cama 🛏"}
            )
            tuck: Response = Response(
                {"response": "você colocou @{} na cama 🙂👉🛏"}
            )

    class Markov(EnTranslations.Markov):
        class Markov(EnTranslations.Markov.Markov):
            channel_not_found: Response = Response(
                {"response": "@canal não encontrado no meu banco de dados."}
            )
            user_not_found: Response = Response(
                {"response": "@{} usuário não encontrado no meu banco de dados.",
                    
                }
            )
            no_start: Response = Response(
                {"response": "não encontrei nenhuma mensagem com o inicio {} para iniciar a geração",
                    
                }
            )
            markov_generated: Response = Response({"response": "{}"})

    class Marry(EnTranslations.Marry):
        class Marry(EnTranslations.Marry.Marry):
            bot: Response = Response(
                {"response": "não fui programado para fazer parte de um relacionamento.",
                    
                }
            )
            yourself: Response = Response(
                {"response": "você não pode se casar com você mesmo..."}
            )
            user_not_found: Response = Response(
                {"response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    
                }
            )
            proposal_already_in_progress: Response = Response(
                {"response": "antes você precisa responder ao pedido de @{}! Digite 'yes' ou 'no",
                    
                }
            )
            someone_arrived_first: Response = Response(
                {"response": "@{} chegou primeiro e já fez uma proposta à mão de @{}",
                    
                }
            )
            already_married: Response = Response(
                {"response": "vocês dois já são casados... não se lembra?"}
            )
            author_limit_reached: Response = Response(
                {"response": "você já está casado(a) com {} pessoas não é o suficiente?",
                    
                }
            )
            limit_reached: Response = Response(
                {"response": "@{} já está com o {} pessoas, não há espaço para mais um...",
                    
                }
            )
            not_enough_cookies: Response = Response(
                {"response": "para pagar a aliança e todo o casório, você deve juntar mais {} cookies.",
                    
                }
            )

            proposal_message: str = (
                "você pediu a mão de @{}, o usuário deve digitar 'yes' ou 'no' / 'sim' ou 'não', 💐💍"
            )

            not_enough_cookies2: Response = Response(
                {"response": "parece que @{} gastou todos os cookies que eram pra aliança... "
                    "o casamento precisou ser cancelado",
                    
                }
            )
            proposal_accept: Response = Response(
                {"response": "{}, você aceitou o pedido de @{}, felicidades para o casal! 🎉💞",
                    
                }
            )
            no_proposal: Response = Response(
                {"response": "{}, não há nenhum pedido de casamento para você."}
            )

            proposal_denied: Response = Response(
                {"response": "{}, você recusou o pedido de casamento de @{} 💔"}
            )

            timeout: Response = Response(
                {"response": "o tempo para pensar acabou, caso descidão se casar de novo use o comando novamente.",
                    
                }
            )

        class Divorce(EnTranslations.Marry.Divorce):
            bot: Response = Response(
                {"response": "eu nunca estaria casado com você."}
            )
            yourself: Response = Response(
                {"response": "você não pode se livrar de você mesmo."}
            )
            not_married: Response = Response(
                {"response": "você não está casado com ninguém."}
            )
            user_not_found: Response = Response(
                {"response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    
                }
            )
            divorce: Response = Response(
                {"response": "então, é isso... da próxima vez, case-se com alguém "
                    "que realmente te ame, e não qualquer pessoa por aí",
                    
                }
            )
            wrong_person: Response = Response(
                {"response": "você não sabe nem o nome da pessoa com quem está casado?",
                    
                }
            )

        class MarryAge(EnTranslations.Marry.MarryAge):
            bot: Response = Response(
                {"response": "nunca me casarei com ninguém."}
            )
            user_not_found: Response = Response(
                {"response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    
                }
            )
            not_married: Response = Response(
                {"response": "{} não esta casado com ninguém."}
            )
            married: str = "@{} está casado com @{} há {}"
            divorced: str = "@{} está separado de @{} há {} e quem pediu o divórcio foi @{}"
            response: Response = Response({"response": ""})

    class Pet(EnTranslations.Pet):
        PetsDict: PetsDict = pets
        FromListToPetList = from_list_to_pet_list

        class Pet(EnTranslations.Pet.Pet):
            bot: Response = Response(
                {"response": "eu tenho todos os pets, e ofereço alguns pra vocês",
                    
                }
            )
            user_not_found: Response = Response(
                {"response": "@{} ainda não foi registrado! (não usou nenhum comando)",
                    
                }
            )
            mention_denied: Response = Response(
                {"response": "@{} optou por não permitir ser mencionado."}
            )
            pets: Response = Response({"response": "{} possui {}"})
            no_pets: Response = Response(
                {"response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    
                }
            )
            user_no_pets: Response = Response(
                {"response": "{} não possui nenhum pet."}
            )

        class PetBuy(EnTranslations.Pet.PetBuy):
            no_cookies: Response = Response(
                {"response": "comece a estocar cookies para adquirir um pet ({}stock)",
                    
                }
            )
            not_enough_cookies: Response = Response(
                {"response": "estoque {} cookies para adquirir {}"}
            )
            name_too_large: str = (
                "vamos maneirar no tamanho do nome, " "tente novamente desta vez com um nome menor que 32 caracteres."
            )
            timeout: Response = Response(
                {"response": "o tempo para comprar acabou tente novamente."}
            )
            timeout_response: Response = Response(
                {"response": "você demorou de mais para responder."}
            )
            what_name: str = "qual nome você gostaria de da-lo?"
            are_you_sure: str = "tem certeza que deja nomear de {}? (yes ou no)"
            pet_name: str = "o seu pet sera nomeado {}"
            pet_buy: Response = Response(
                {"response": "você adquiriu {} {} por {} cookies."}
            )
            no_options: Response = Response(
                {"response": "escolha um dos pets disponíveis hoje ({}petlist)"}
            )

        class PetList(EnTranslations.Pet.PetList):
            pet_list: Response = Response(
                {"response": "pets disponíveis (adquira com {}petbuy): {}"}
            )

        class PetName(EnTranslations.Pet.PetName):
            no_pets: Response = Response(
                {"response": "Você não tem pets para dar nome."}
            )
            what_pet_to_name: str = (
                "qual dos pets você quer nomear: {}? " "(mande o número do pet que você gostaria de mudar.)"
            )
            timeout: Response = Response(
                {"response": "você demorou de mais para responder."}
            )
            what_name: str = "qual nome você quer dar para {}?"
            new_name: Response = Response(
                {"response": "o nome do pet foi mudado para {} ."}
            )

        class PetPat(EnTranslations.Pet.PetPat):
            no_pet_name: Response = Response(
                {"response": "você não especificou o nome do pet."}
            )
            no_pets: Response = Response(
                {"response": "você fez carinho em {} {}"}
            )
            pet_pat: Response = Response(
                {"response": "adquira um dos pets disponíveis ({}petlist) em troca de cookies.",
                    
                }
            )
            wrong_pet_name: Response = Response(
                {"response": "você não tem um pet com este nome.."}
            )

        class PetSell(EnTranslations.Pet.PetSell):
            pass

    class Profile(EnTranslations.Profile):
        class Mention(EnTranslations.Profile.Mention):
            mention_on: Response = Response(
                {"response": "outros usuários poderão mencionar você novamente nos comandos.",
                    
                }
            )

        class NickName(EnTranslations.Profile.NickName):
            nickname_too_large: Response = Response(
                {"response": "o apelido {} é muito grande, por favor tente manter com no máximo 32 caracteres.",
                    
                }
            )
            nickname_removed: Response = Response(
                {"response": "seu apelido foi removido com sucesso!"}
            )
            nickname_changed: Response = Response(
                {"response": "você alterou seu de apelido para {} com sucesso!"}
            )

        class SaveCity(EnTranslations.Profile.SaveCity):
            city_removed: Response = Response(
                {"response": "Cidade foi removida com sucesso!."}
            )
            city_added: Response = Response(
                {"response": "Você salvou {} como sua cidade, agora basta usar {}weather.",
                    
                }
            )

        class SaveColor(EnTranslations.Profile.SaveColor):
            color_removed: Response = Response(
                {"response": "a cor foi removida com sucesso!"}
            )
            color_added: Response = Response(
                {"response": 'você salvou a cor {} e pode visualizá-la usando "{}color"',
                    
                }
            )

        class UnMention(EnTranslations.Profile.UnMention):
            mention_off: Response = Response(
                {"response": "agora outros usuários não poderão mais mencionar você nos comandos.",
                    
                }
            )

    class Reminder(EnTranslations.Reminder):
        class Remind(EnTranslations.Reminder.Remind):
            bot: Response = Response(
                {"response": "estou sempre aqui... não precisa me deixar lembretes.",
                    
                }
            )
            user_not_found: Response = Response(
                {"response": "esse usuário ainda não foi registrado. (não usou nenhum comando)",
                    
                }
            )
            user_opt_out: Response = Response(
                {"response": "o usuário {} optou por desligar os reminds para."}
            )
            author_too_much_reminds: Response = Response(
                {"response": "já existem muitos lembretes seus pendentes..."}
            )
            user_too_much_reminds: Response = Response(
                {"response": "já existem muitos lembretes pendentes para {}"}
            )
            time_not_found: Response = Response(
                {"response": "não entendi o tempo que você me passou."}
            )
            remind_on_back: Response = Response(
                {"response": "{} será lembrado disso na próxima vez que falar no chat 📝 (ID {})",
                    
                }
            )
            dont_have_time_machine: Response = Response(
                {"response": "eu ainda não inventei a máquina do tempo."}
            )
            minimum_time: Response = Response(
                {"response": "o tempo mínimo para lembretes cronometrados é 1 minuto.",
                    
                }
            )
            remind_on_time: Response = Response(
                {"response": "{} será lembrado disso em {}. ⏲️(ID {})"}
            )

        class Reminds(EnTranslations.Reminder.Reminds):
            remind_for: Response = Response(
                {"response": "esse lembrete é para {}: {}."}
            )
            remind_timed_with_content: Response = Response(
                {"response": "esse lembrete é para {} em {}: {}."}
            )
            remind_timed_without_content: Response = Response(
                {"response": "esse lembrete era para {} há {}."}
            )
            remind_deleted: Response = Response(
                {"response": "seu lembrete de ID {} foi deletado."}
            )
            remind_not_found: Response = Response(
                {"response": "você não possui nenhum lembrete com esse ID."}
            )
            no_id_selected: Response = Response(
                {"response": "você deve passar o ID do lembrete que quer deletar.",
                    
                }
            )
            author_reminds: Response = Response(
                {"response": "seus lembretes pendentes são os de ID: {}."}
            )
            author_dont_have_reminds: Response = Response(
                {"response": "você não tem lembretes pendentes."}
            )

        class RemindListener(EnTranslations.Reminder.RemindListener):
            remind_timed_with_content: Response = Response(
                {"response": "{} deixou um lembrete: {} (há {})"}
            )
            remind_timed_without_content: Response = Response(
                {"response": "{} deixou um lembrete em branco (há {})"}
            )

    class Settings(EnTranslations.Settings):
        class BanWord(EnTranslations.Settings.BanWord):
            word_added: Response = Response(
                {"response": "esse já é um termo banido."}
            )
            word_already_on_list: Response = Response(
                {"response": "não irei mais enviar mensagens que tiverem esse termo.",
                    
                }
            )

        class Disable(EnTranslations.Settings.Disable):
            command_dont_exist: Response = Response(
                {"response": "esse comando não existe."}
            )
            command_cannot_be_disabled: Response = Response(
                {"response": "não pode ser desativado."}
            )
            command_already_disabled: Response = Response(
                {"response": '"{}" já está desativado.'}
            )
            command_disabled: Response = Response(
                {"response": '"{}" foi desativado.'}
            )

        class Enable(EnTranslations.Settings.Enable):
            command_dont_exist: Response = Response(
                {"response": "esse comando não existe."}
            )
            command_reactivated: Response = Response(
                {"response": '"{}" foi reativado.'}
            )
            command_already_activated: Response = Response(
                {"response": '"{}" já está ativado.'}
            )

        class Prefix(EnTranslations.Settings.Prefix):
            prefix_invalid: Response = Response(
                {"response": "este prefixo {prefixo} é invalido"}
            )
            prefix_invalid_or_absent: Response = Response(
                {"response": "Esqueceu de mandar o prefixo ou ele é invalido."}
            )
            prefix_already_in_use: Response = Response(
                {"response": "O canal ja esta usando o prefixo {prefixo}."}
            )
            prefix_changed: Response = Response(
                {"response": 'O prefixo do canal foi alterado para "{}".'}
            )
            prefix_too_large: Response = Response(
                {"response": "Atualmente eu so consigo armazenar prefixos de ate 2 caracteres o prefixo que você "
                    'tentou usar não é valido pois contem "{}" caracteres.',
                    
                }
            )

        class Start(EnTranslations.Settings.Start):
            already_on: Response = Response({"response": "já estou ligado ☕"})
            started: Response = Response({"response": "você me ligou ☕"})

        class Stop(EnTranslations.Settings.Stop):
            stopped: Response = Response({"response": "você me desligou 💤"})

        class UnBanWord(EnTranslations.Settings.UnBanWord):
            word_removed: Response = Response(
                {"response": '"{}" foi removido dos termos banidos.'}
            )
            word_not_found: Response = Response(
                {"response": '"{}" não é um termo banidos.'}
            )

    class Tools(EnTranslations.Tools):
        class Math(EnTranslations.Tools.Math):
            result: Response = Response({"response": "{}"})
            error: Response = Response(
                {"response": "não consegui calcular... lembre-se: use * para multiplicação, use / para divisão, "
                    "e use ponto em vez de vírgula para números decimais. {}",
                    
                }
            )

        class Shorten(EnTranslations.Tools.Shorten):
            no_links_found: Response = Response(
                {"response": "Use: `{}encurta <link>`"}
            )
            shorten_links: Response = Response(
                {"response": "Aqui está os links: {}"}
            )
            shorten_link: Response = Response(
                {"response": "Aqui está os link: {}"}
            )
            shorten_error: Response = Response(
                {"response": "Não foi possível encurtar o link."}
            )

        class Time(EnTranslations.Tools.Time):
            time: Response = Response({"response": "{}"})
            future_time: Response = Response({"response": "em {}"})
            past_time: Response = Response({"response": "há {}"})
            unit_not_found: Response = Response(
                {"response": "as medidas suportadas atualmente são: anos, meses, semanas, dias, horas, "
                    "minutos e segundos. Caso nenhuma seja colocada, será dado o tempo completo convertido. ",
                    
                }
            )
            too_much_time: Response = Response(
                {"response": "tempo de mais para converter."}
            )

        class UserId(EnTranslations.Tools.UserId):
            user_not_found: Response = Response(
                {"response": "não achei nenhum usuário com esse id."}
            )
            id_or_name: Response = Response({"response": "{}"})

        class Weather(EnTranslations.Tools.Weather, WeatherTools):
            city_not_passed: Response = Response(
                {"response": "você não enviou nenhuma cidade e não tem nenhuma cidade salva, "
                    "use {}savecity <cidade> para salvar uma cidade.",
                    
                }
            )
            city_not_found: Response = Response(
                {"response": "eu não encontrei nenhuma cidade com o nome de {}.",
                    
                }
            )
            weather: Response = Response({"response": ""})

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

    class Tower(EnTranslations.Tower):
        class EnterTower(EnTranslations.Tower.EnterTower):
            class_rank_up: Response = Response({"response": "agora você é {}"})
            class_to_choose: Response = Response(
                {"response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    
                }
            )
            cooldown: Response = Response(
                {"response": "aguarde {} para entrar continuar a escalada ⌛"}
            )
            tower_result: Response = Response({"response": "{}"})
            class_choice: Response = Response(
                {"response": "você escolheu {}! {}"}
            )
            class_first_choice: Response = Response(
                {"response": "antes de continuar, escolha sua classe! {}ed  " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    
                }
            )

        class FastTower(EnTranslations.Tower.FastTower):
            class_to_choose: Response = Response(
                {"response": "Antes de continuar, digite o comando e sua nova classe: {} ou {}",
                    
                }
            )
            cooldown: Response = Response(
                {"response": "aguarde {} para entrar continuar a escalada ⌛"}
            )
            tower_result: Response = Response({"response": "{}"})
            class_first_choice: Response = Response(
                {"response": "antes de continuar, escolha sua classe! {}et " "Guerreiro(a), Arqueiro(a) ou Mago(a)",
                    
                }
            )

        class TowerLevel(EnTranslations.Tower.TowerLevel):
            bot_nick: Response = Response(
                {"response": "Eu apenas conto as historias dos encontros."}
            )
            no_class_chosen: Response = Response(
                {"response": "{} ainda não escolheu uma classe."}
            )
            player_status: Response = Response(
                {"response": "{} é {} ({}, {} XP). Esta no andar {} zona {}, com um total de {} "
                    "encontros ({} vitórias, {} derrotas, {.2f}% winrate) ♦",
                    
                }
            )
            player_not_found: Response = Response({"response": ""})



    class AdminOld(EnTranslations.Admin):
        class AddUser(EnTranslations.Admin.AddUser):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}."}
            )
            user_response: Response = Response(
                {"response": "as infos de {} foram adicionadas.",
                    "response_list": [],
                    
                }
            )

        class AddBot(EnTranslations.Admin.AddBot):
            user_not_found: Response = Response(
                {"response": "eu ainda não vi esse bot em nenhum chat."}
            )
            user_already_added: Response = Response(
                {"response": "o bot {} ja esta registrado."}
            )
            user_added: Response = Response(
                {"success": True, "response": "o bot {} foi adicionado aos bots."}
            )

        class AllChannels(EnTranslations.Admin.AllChannels):
            channels: Response = Response(
                {"response": "aqui a lista de todos os canais que eu estou: {}"}
            )

        class Announce(EnTranslations.Admin.Announce):
            success: Response = Response(
                {"response": "O comando foi executado com sucesso."}
            )

        class ApiBot(EnTranslations.Admin.ApiBot):
            added_with_success: Response = Response(
                {"response": "O comando foi executado com sucesso. Com {} bots adicionados.",
                    
                }
            )

        class ChannelLog(EnTranslations.Admin.ChannelLog):
            channel_already_added: Response = Response(
                {"response": "Ja estou no canal {}."}
            )
            channel_added: Response = Response(
                {"success": True, "response": "Entrei no canal {}."}
            )

        class CookieGive(EnTranslations.Admin.CookieGive):
            cookie_given: Response = Response(
                {"success": True, "response": "você deu {} para {}."}
            )

        class CountUser(EnTranslations.Admin.CountUser):
            user_quantity: Response = Response(
                {"success": True, "response": "têm {} usuários no banco de dados."}
            )

        class DBGrep(EnTranslations.Admin.DBGrep):
            user_not_found: Response = Response(
                {"success": True, "response": "não existe nenhum usuário com nick {}."}
            )
            user_info: Response = Response(
                {"response": "aqui as infos do usuário: {}.",
                    "response_list": [],
                    
                }
            )
            channel_info: Response = Response(
                {"response": "aqui as infos do canal: {}.", "response_list": []}
            )

        class DelFromDB(EnTranslations.Admin.DelFromDB):
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
                    
                }
            )

        class DisableNSFW(EnTranslations.Admin.DisableNSFW):
            commands_disabled: Response = Response(
                {"success": True, "response": "NSFW foi desabilitado em {} canais."}
            )

        class LotteryStart(EnTranslations.Admin.LotteryStart):
            pass  # TODO: Fazer quando refizer o loterica_start

        class RGit(EnTranslations.Admin.RGit):
            git_pulled: Response = Response(
                {"success": True, "response": "O comando foi executado com sucesso."}
            )
