# Translation for Set
Set-deco_helper = Comando principal para personalizar suas configurações de usuário.
Set-deco_usage = Uso: {$prefix}set (subcomando) [argumentos]
Set-deco_description = Comando principal para personalizar suas configurações de usuário.

# Translation for Set Mention
Set-Mention-on_off_wrong_option = {$args} não é uma opção válida, escolha entre "on" ou "off"
Set-Mention-mention_on = Você voltará a receber menções do bot nos comandos.
Set-Mention-mention_off = Sempre que o bot disser seu nick, ele colocará um caractere invisível para evitar o ping.

Set-Mention-deco_helper = Ativar ou desativar menções do bot.
Set-Mention-deco_usage = Uso: {$prefix}set mention <on/off>
Set-Mention-deco_description = Permite ativar ou desativar se o bot irá mencionar você diretamente ao responder.

# Commands
Set-Mention-cmd_on_prefix = Ativar menções:
Set-Mention-cmd_off_prefix = Desativar menções:

# Translation for Set City
Set-City-city_added = Cidade adicionada com sucesso.
Set-City-city_removed = Cidade removida com sucesso.

Set-City-deco_helper = Definir ou remover sua cidade salva.
Set-City-deco_usage = Uso: {$prefix}set city (nome ou remove) [hidden:true]
Set-City-deco_description = Salva o nome de uma cidade no seu perfil, opcionalmente oculto da visualização pública.

# Commands
Set-City-cmd_set_prefix = Definir cidade:
Set-City-cmd_hide_prefix = Definir cidade e ocultar:
Set-City-cmd_latlong_prefix = Definir a localização com lat e long e hidden:
Set-City-cmd_remove_prefix = Remover cidade:

# Admonitions
Set-City-adm_hide_title = Ocultar
Set-City-adm_hide_msg = Use a flag `hidden` para ocultar sua cidade nas mensagens.

# Translation for Set Nick
Set-Nick-nick_too_large = O apelido deve ter no máximo 32 caracteres, e não {$limit}.
Set-Nick-nick_removed = Apelido removido com sucesso.
Set-Nick-nick_changed = Apelido alterado com sucesso.

Set-Nick-deco_helper = Definir ou remover um apelido personalizado.
Set-Nick-deco_usage = Uso: {$prefix}set nick <apelido ou remove>
Set-Nick-deco_description = Permite definir um apelido que o bot usará ao se referir a você.

# Commands
Set-Nick-cmd_set_prefix = Definir apelido:
Set-Nick-cmd_remove_prefix = Remover apelido:

# Admonitions
Set-Nick-adm_short_title = Mantenha curto!
Set-Nick-adm_short_msg = O apelido deve ter no máximo 32 caracteres.

# Translation for Set Color
Set-Color-color_removed = Cor salva removida com sucesso.
Set-Color-color_changed = Cor salva alterada com sucesso.

Set-Color-deco_helper = Salvar ou remover uma cor personalizada.
Set-Color-deco_usage = Uso: {$prefix}set color (#hex ou remove)
Set-Color-deco_description = Define uma cor hexadecimal personalizada que pode ser usada em visualizações futuras.

# Commands
Set-Color-cmd_set_prefix = Definir cor:
Set-Color-cmd_remove_prefix = Remover cor:

# Translation for Set Reminder
Set-Reminder-reminder_on = Lembrete ativado com sucesso.
Set-Reminder-reminder_off = Lembrete desativado com sucesso.

Set-Reminder-deco_helper = Ativar ou desativar lembretes.
Set-Reminder-deco_usage = Uso: {$prefix}set reminder (on/off)
Set-Reminder-deco_description = Alterna se o sistema irá marcar você em lembretes de outras pessoas.

# Commands
Set-Reminder-cmd_on_prefix = Ativar lembretes:
Set-Reminder-cmd_off_prefix = Desativar lembretes:

# Translation for Set Banword
Set-Banword-add_remove = Escolha uma das opções válidas: adicionar, remover ou limpar. Não {$args}.
Set-Banword-who = Como diabos você conseguiu fazer isso? Vou te denunciar agora.
Set-Banword-added = Palavra(s) proibida adicionada. Agora irei censurar qualquer comando que a contenha.
Set-Banword-removed = Palavra(s) proibida removida.
Set-Banword-cleaned = Removi todas as palavras proibidas.
Set-Banword-what = Não entendi essa opção {$option}

Set-Banword-deco_helper = Comando usado para adicionar palavras proibidas que o bot não pode enviar no chat.
Set-Banword-deco_usage = Para usar: {$prefix}set banword (add|remove|clean) (palavras)
Set-Banword-deco_description = Comando usado para adicionar palavras proibidas que o bot não pode enviar no chat.

# Mapping
Set-Banword-map_add = adicionar
Set-Banword-map_remove = remover
Set-Banword-map_clean = limpar

# Translation for Set Enable/Disable
Set-Enable-why = Por que você esta tentando ativar/desativar {$args}?
Set-Enable-no_command = Não tenho nenhum comando chamado {$args}.
Set-Enable-command_already_enabled = O comando {$args} já está ativado.
Set-Enable-command_enabled = O comando {$args} foi ativado.
Set-Enable-command_disabled = O comando {$args} foi desativado.
Set-Enable-command_already_disabled = O comando {$args} já está desativado.
Set-Enable-options = Se você quiser ativar/desativar tudo, pode usar ativar/desativar tudo.
Set-Enable-all_enabled = Todos os comandos foram ativados.
Set-Enable-all_disabled = Todos os comandos foram desativados.

Set-Enable-deco_helper = Um comando usado para ativar ou desativar outros comandos.
Set-Enable-deco_usage = Para usar: {$prefix}set enable/disable (nome do comando or all)
Set-Enable-deco_description = Um comando usado para ativar ou desativar outros comandos.

# Translation for Set Prefix
Set-Prefix-too_long = O prefixo {$arg} é muito longo, por favor, mantenha-o mais curto que {$size}.
Set-Prefix-prefix_changed = Prefixo alterado para {$args}

Set-Prefix-deco_helper = Comando usado para alterar o prefixo do canal, qualquer comando com 2 caracteres funcionará.
Set-Prefix-deco_usage = Para usar: {$prefix}set prefix (qualquer coisa)
Set-Prefix-deco_description = Comando usado para alterar o prefixo do canal, qualquer comando com 2 caracteres funcionará.

# Translation for Set StartStop
Set-StartStop-started = O bot foi ligado com sucesso.
Set-StartStop-already_on = O bot já está ligado.
Set-StartStop-stopped = O bot foi desligado com sucesso.
Set-StartStop-already_off = O bot já está desligado.
Set-StartStop-shrug = Não sei como você chegou aqui. Talvez seja um bug.

Set-StartStop-deco_helper = Comando usado para ativar ou desativar o bot no chat.
Set-StartStop-deco_usage = Para usar: {$prefix}set start(ou on)/stop(ou off)
Set-StartStop-deco_description = Comando usado para ativar ou desativar o bot no chat.
