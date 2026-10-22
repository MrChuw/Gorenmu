# Translation for Reminder

Reminder-bot_nick = I'm only here to remind others.

Reminder-author_too_much_reminds = You have reached the limit of unsent reminders.
Reminder-user_too_much_reminds = { $mention } has reached the limit of unsent reminders.
Reminder-date_not_valid = The provided date is not valid: { $date }
Reminder-remind_on_back = { $mention } will be reminded the next time they type in chat ({ $remind_id })
Reminder-dont_have_time_machine = I don't have a time machine to remind you in the past.
Reminder-minimum_time = The minimum time for a reminder is 1 minute.

Reminder-remind = { $mention } will be reminded the next time { $is_self ->
    [1] you
    *[0] they
} type in chat ({ $remind_id })

Reminder-remind_after = { $mention } will be reminded when { $is_self ->
    [1] you
    *[0] they
} type in chat, after: { $after } ({ $remind_id })

Reminder-remind_after_in = { $mention } will be reminded in { $time }, { $wait } after: { $after } ({ $remind_id })
Reminder-remind_after_timed = { $mention } will be reminded in { $time } after: { $after } ({ $remind_id })
Reminder-remind_timed = { $mention } will be reminded in { $time } ({ $remind_id })

Reminder-dispatched_message = { $target }, { $mention } left a reminder: { $content } ({ $time_diff } ago)
Reminder-dispatched_blank_message = { $target }, { $mention } left a blank reminder ({ $time_diff } ago)

Reminder-deco_helper = Command used to create a reminder for when you type in chat or with a set time.
Reminder-deco_usage = How to use: { $prefix }remindme <message> or { $prefix }remindme in 5h <message>.
Reminder-deco_description = Detailed description of the Reminder command.

# Commands
Reminder-cmd_ex1_prefix = Simple usage example.
Reminder-cmd_ex1_res = Expected response of the example.

# Admonitions
Reminder-adm_title = Attention
Reminder-adm_msg = Informative message for the Reminder command.
