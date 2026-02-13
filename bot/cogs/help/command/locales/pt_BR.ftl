# Translation for Help
Help-help = { $prefix }{ $name }: { $helper } - Cooldown: { $cooldown } { $url } - Aliases: { $alias }
Help-command_site = Site em construção, aqui está a lista de comandos: { $url }
Help-suggested_command = Não tenho um comando com o nome "{ $content }", talvez você quis dizer "{ $suggested }".

Help-deco_helper = Comando para obter informações sobre outros comandos.
Help-deco_usage = Como usar: { $prefix }help (nome do comando)
Help-deco_description = Este comando retorna informações detalhadas sobre outro comando, incluindo como usá-lo, tempo de espera (cooldown) e apelidos (aliases). Se nenhum nome for fornecido, ele retorna o site com a lista de comandos.

# Commands
Help-cmd_ex1_prefix = Quando o comando existe e há informações.
Help-cmd_ex1_res = !ping: Comando para verificar se o bot está ativo. - Cooldown: 5s https://bot.mrchuw.com.br/commands/ping - Aliases: pong

Help-cmd_ex2_prefix = Quando o comando não existe mas há uma sugestão.
Help-cmd_ex2_res = Não tenho um comando com o nome "pign", talvez você quis dizer "ping".

Help-cmd_ex3_prefix = Quando nenhum argumento é passado.
Help-cmd_ex3_res = Site em construção, aqui está a lista de comandos: https://bot.mrchuw.com.br

# Admonitions
Help-adm_suggestions_title = Sugestões de Comando
Help-adm_suggestions_msg = Se um comando não for encontrado, o bot pode sugerir o mais próximo.

Help-adm_meta_title = Aliases e Cooldown
Help-adm_meta_msg = O comando de ajuda também listará os apelidos e o tempo de espera de cada comando.
