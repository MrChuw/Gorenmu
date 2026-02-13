# Translation for Set
Set-deco_helper = Comando principal para personalizar suas configurações de usuário.
Set-deco_usage = Uso: {$prefix}set (subcomando) [argumentos]
Set-deco_description = Comando principal para personalizar suas configurações de usuário.

# Translation for Set Mention
Mention-on_off_wrong_option = {$args} não é uma opção válida, escolha entre "on" ou "off"
Mention-mention_on = Você voltará a receber menções do bot nos comandos.
Mention-mention_off = Sempre que o bot disser seu nick, ele colocará um caractere invisível para evitar o ping.

Mention-deco_helper = Ativar ou desativar menções do bot.
Mention-deco_usage = Uso: {$prefix}set mention <on/off>
Mention-deco_description = Permite ativar ou desativar se o bot irá mencionar você diretamente ao responder.

# Commands
Mention-cmd_on_prefix = Ativar menções:
Mention-cmd_off_prefix = Desativar menções:

# Translation for Set City
City-city_added = Cidade adicionada com sucesso.
City-city_removed = Cidade removida com sucesso.

City-deco_helper = Definir ou remover sua cidade salva.
City-deco_usage = Uso: {$prefix}set city (nome ou remove) [hidden:true]
City-deco_description = Salva o nome de uma cidade no seu perfil, opcionalmente oculto da visualização pública.

# Commands
City-cmd_set_prefix = Definir cidade:
City-cmd_hide_prefix = Definir cidade e ocultar:
City-cmd_latlong_prefix = Definir a localização com lat e long e hidden:
City-cmd_remove_prefix = Remover cidade:

# Admonitions
City-adm_hide_title = Ocultar
City-adm_hide_msg = Use a flag `hidden` para ocultar sua cidade nas mensagens.

# Translation for Set Nick
Nick-nick_too_large = O apelido deve ter no máximo 32 caracteres, e não {$limit}.
Nick-nick_removed = Apelido removido com sucesso.
Nick-nick_changed = Apelido alterado com sucesso.

Nick-deco_helper = Definir ou remover um apelido personalizado.
Nick-deco_usage = Uso: {$prefix}set nick <apelido ou remove>
Nick-deco_description = Permite definir um apelido que o bot usará ao se referir a você.

# Commands
Nick-cmd_set_prefix = Definir apelido:
Nick-cmd_remove_prefix = Remover apelido:

# Admonitions
Nick-adm_short_title = Mantenha curto!
Nick-adm_short_msg = O apelido deve ter no máximo 32 caracteres.

# Translation for Set Color
Color-color_removed = Cor salva removida com sucesso.
Color-color_changed = Cor salva alterada com sucesso.

Color-deco_helper = Salvar ou remover uma cor personalizada.
Color-deco_usage = Uso: {$prefix}set color (#hex ou remove)
Color-deco_description = Define uma cor hexadecimal personalizada que pode ser usada em visualizações futuras.

# Commands
Color-cmd_set_prefix = Definir cor:
Color-cmd_remove_prefix = Remover cor:

# Translation for Set Reminder
Reminder-reminder_on = Lembrete ativado com sucesso.
Reminder-reminder_off = Lembrete desativado com sucesso.

Reminder-deco_helper = Ativar ou desativar lembretes.
Reminder-deco_usage = Uso: {$prefix}set reminder (on/off)
Reminder-deco_description = Alterna se o sistema irá marcar você em lembretes de outras pessoas.

# Commands
Reminder-cmd_on_prefix = Ativar lembretes:
Reminder-cmd_off_prefix = Desativar lembretes:

# Translation for Set Banword
Banword-add_remove = Escolha uma das opções válidas: adicionar, remover ou limpar. Não {$args}.
Banword-who = Como diabos você conseguiu fazer isso? Vou te denunciar agora.
Banword-added = Palavra(s) proibida adicionada. Agora irei censurar qualquer comando que a contenha.
Banword-removed = Palavra(s) proibida removida.
Banword-cleaned = Removi todas as palavras proibidas.
Banword-what = Não entendi essa opção {$option}

Banword-deco_helper = Comando usado para adicionar palavras proibidas que o bot não pode enviar no chat.
Banword-deco_usage = Para usar: {$prefix}set banword (add|remove|clean) (palavras)
Banword-deco_description = Comando usado para adicionar palavras proibidas que o bot não pode enviar no chat.

# Mapping
Banword-map_add = adicionar
Banword-map_remove = remover
Banword-map_clean = limpar

# Translation for Set Enable/Disable
Enable-why = Por que você esta tentando ativar/desativar {$args}?
Enable-no_command = Não tenho nenhum comando chamado {$args}.
Enable-command_already_enabled = O comando {$args} já está ativado.
Enable-command_enabled = O comando {$args} foi ativado.
Enable-command_disabled = O comando {$args} foi desativado.
Enable-command_already_disabled = O comando {$args} já está desativado.
Enable-options = Se você quiser ativar/desativar tudo, pode usar ativar/desativar tudo.
Enable-all_enabled = Todos os comandos foram ativados.
Enable-all_disabled = Todos os comandos foram desativados.

Enable-deco_helper = Um comando usado para ativar ou desativar outros comandos.
Enable-deco_usage = Para usar: {$prefix}set enable/disable (nome do comando or all)
Enable-deco_description = Um comando usado para ativar ou desativar outros comandos.

# Translation for Set Prefix
Prefix-too_long = O prefixo {$arg} é muito longo, por favor, mantenha-o mais curto que {$size}.
Prefix-prefix_changed = Prefixo alterado para {$args}

Prefix-deco_helper = Comando usado para alterar o prefixo do canal, qualquer comando com 2 caracteres funcionará.
Prefix-deco_usage = Para usar: {$prefix}set prefix (qualquer coisa)
Prefix-deco_description = Comando usado para alterar o prefixo do canal, qualquer comando com 2 caracteres funcionará.

# Translation for Set StartStop
StartStop-started = O bot foi ligado com sucesso.
StartStop-already_on = O bot já está ligado.
StartStop-stopped = O bot foi desligado com sucesso.
StartStop-already_off = O bot já está desligado.
StartStop-shrug = Não sei como você chegou aqui. Talvez seja um bug.

StartStop-deco_helper = Comando usado para ativar ou desativar o bot no chat.
StartStop-deco_usage = Para usar: {$prefix}set start(ou on)/stop(ou off)
StartStop-deco_description = Comando usado para ativar ou desativar o bot no chat.
