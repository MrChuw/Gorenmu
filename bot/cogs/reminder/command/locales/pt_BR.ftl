# Translation for Reminder

Reminder-bot_nick = Eu estou aqui somente para lembrar os outros.

Reminder-author_too_much_reminds = Você já atingiu o limite de lembretes não enviados.
Reminder-user_too_much_reminds = { $mention } já atingiu o limite de lembretes não enviados.
Reminder-date_not_valid = A data informada não é válida: { $date }
Reminder-remind_on_back = { $mention } será lembrado na próxima vez que digitar no chat ({ $remind_id })
Reminder-dont_have_time_machine = Não tenho uma máquina do tempo para lembrar você no passado.
Reminder-minimum_time = O tempo mínimo para um lembrete é 1 minuto.

Reminder-remind = { $mention } será lembrado na próxima vez que { $is_self ->
    [1] você
    *[0] ele(a)
} digitar no chat ({ $remind_id })

Reminder-remind_after = { $mention } será lembrado quando { $is_self ->
    [1] você
    *[0] ele(a)
} digitar, depois de: { $after } ({ $remind_id })

Reminder-remind_after_in = { $mention } será lembrado em { $time }, { $wait } depois de: { $after } ({ $remind_id })
Reminder-remind_after_timed = { $mention } será lembrado em { $time } depois de: { $after } ({ $remind_id })
Reminder-remind_timed = { $mention } será lembrado em { $time } ({ $remind_id })

Reminder-dispatched_message = { $target }, { $mention } deixou um lembrete: { $content } (há { $time_diff })
Reminder-dispatched_blank_message = { $target }, { $mention } deixou um lembrete em branco (há { $time_diff })

Reminder-deco_helper = Comando usado para criar um lembrete para quando digitar no chat ou com tempo determinado.
Reminder-deco_usage = Como usar: { $prefix }remindme <mensagem> ou { $prefix }remindme in 5h <mensagem>.
Reminder-deco_description = Descrição detalhada do comando Reminder.

# Commands
Reminder-cmd_ex1_prefix = Exemplo de uso simples.
Reminder-cmd_ex1_res = Resposta esperada do exemplo.

# Admonitions
Reminder-adm_title = Atenção
Reminder-adm_msg = Mensagem informativa para o comando Reminder.
