# Translation for Help
Help-help = { $prefix }{ $name }: { $helper } - Cooldown: { $cooldown } { $url } - Aliases: { $alias }
Help-command_site = Site in construction, here is the list of commands: { $url }
Help-suggested_command = I don't have a command named "{ $content }", maybe you meant "{ $suggested }".

Help-deco_helper = Command to get information about other commands.
Help-deco_usage = How to use: { $prefix }help (command name)
Help-deco_description = This command returns detailed information about another command, including its usage, cooldown time, and aliases. If no input is given, it returns a general site link with command listings.

# Commands
Help-cmd_ex1_prefix = When the command exists and has info.
Help-cmd_ex1_res = !ping: Command to check if the bot is alive. - Cooldown: 5s https://bot.mrchuw.com.br/commands/ping - Aliases: pong

Help-cmd_ex2_prefix = When the command doesn't exist but one is suggested.
Help-cmd_ex2_res = I don't have a command named "pign", maybe you meant "ping".

Help-cmd_ex3_prefix = When no argument is passed.
Help-cmd_ex3_res = Site in construction, here is the list of commands: https://bot.mrchuw.com.br

# Admonitions
Help-adm_suggestions_title = Command Suggestions
Help-adm_suggestions_msg = If a command isn't found, the bot may suggest the closest match.

Help-adm_meta_title = Aliases and Cooldowns
Help-adm_meta_msg = The help command will also list any aliases and cooldowns associated with the command.
