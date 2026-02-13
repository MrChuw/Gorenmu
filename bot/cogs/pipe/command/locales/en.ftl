# Translation for Pipe
Pipe-pipe = Pipe is not really a command. For more information, visit this link: {$link}

Pipe-deco_helper = Pipe is not really a command. For more information, visit the website.
Pipe-deco_usage = Pipe is not really a command. For more information, visit the website.
Pipe-deco_description = Pipe is not really a command. For more information, visit the website.

# Commands
Pipe-cmd_ex1 = {$prefix}example_command_1 <command options> | example_command_2
Pipe-cmd_ex2 = {$prefix}example_command_1 <command options> | example_command_2 <command 2 options> {"{"}output from command 1{"}"} <remaining command 2 options>

# Admonitions
Pipe-adm_cool_title = Cooldown!
Pipe-adm_cool_msg = The cooldown for the pipe will be the same as the cooldown of the commands used.
Pipe-adm_info_title = Pipe
Pipe-adm_info_msg = The Pipe is represented by the character '|' (vertical bar), and it is used to forward the output of one command to another.
Pipe-adm_work_title = How pipe works:
Pipe-adm_work_msg =
    ## The bot's step-by-step will be:  \n
    - Execute `example_command_1` with `<command options>` if any.  \n
    - Then it will execute `example_command_2` with the response from `example_command_1` added as an argument.  \n
    - If you use {"{"}output{"}"}, it will place the response from `example_command_1` in the specified position.
