## AFK
AFK-afk = { $status } { $emoji }
AFK-content = { $status } { $emoji } and left a note with: { $content }
AFK-deco_helper = Command to set your status.
AFK-deco_usage = How to use: { $prefix }Afk (message)
AFK-deco_description = This command sets your status to AFK.

# AFK Examples
AFK-cmd_ex1_res = you went AFK: 🏃 ⌨️
AFK-cmd_ex2_args = Nice message.
AFK-cmd_ex2_res = you went AFK: 🏃 ⌨️ and left a note with: Nice message.

# AFK Admonitions
AFK-adm_title = Maximum length!
AFK-adm_msg = The message could not be longer than 450 characters.

# AFK Activities (List format: label, emoji, action, ongoing, past, context)
AFK-prop_list = it's, you, you continued, you
AFK-afk_list = afk, 🏃⌨, went afk, afk, came back, afk
AFK-read_list = read, 📖, went to read, reading, read, reading
AFK-brb_list = brb, 🏃⌨, coming back soon, away, came back, away
AFK-eat_list = food, 🍽, went to eat, eating, ate, eating
AFK-play_list = game, 🎮, went to play, playing, played, playing
AFK-sleep_list = gn, 💤, went to sleep, sleeping, woke up, sleeping
AFK-study_list = study, 📚, went to study, studying, studied, studying
AFK-art_list = art, 🎨, went to draw, drawing, drew, drawing
AFK-watch_list = watch, 📺, went to watch, watching, watched, watching
AFK-shower_list = shower, 🚿, went to shower, in the shower, took a shower, the shower
AFK-code_list = code, 💻, went to code, coding, coded, coding
AFK-work_list = work, 💼, went to work, working, worked, working

## IsAFK
IsAFK-bot = I'm always here… watching.
IsAFK-author = you're not afk… obviously.
IsAFK-is_afk = @{ $name } { $status } { $emoji } (for { $time })
IsAFK-is_afk_content = @{ $name } { $status } { $emoji } and left a note: { $message } (for { $time })
IsAFK-is_not_afk = @{ $name } is not AFK.
IsAFK-deco_helper = Type the command and the user's name to see if they are AFK.
IsAFK-deco_usage = How to use: { $prefix }IsAfk (username)
IsAFK-deco_description = This command checks if a user is AFK or not.

# IsAFK Examples
IsAFK-cmd_ex1_args = user2
IsAFK-cmd_ex1_res = @user2 is not AFK.
IsAFK-cmd_ex2_args = user3
IsAFK-cmd_ex2_res = @user3 is AFK.

## RAFK
RAFK-return_expired = to return AFK
RAFK-afk = { $status } { $emoji }
RAFK-content = { $status } { $emoji } and left a note with: { $content }
RAFK-deco_helper = Return to AFK status.
RAFK-deco_usage = To use: { $prefix }rafk
RAFK-deco_description = This command is used to return to AFK status.

# RAFK Examples
RAFK-cmd_ex1_res = @user2 you remained AFK: 🏃 ⌨️
RAFK-cmd_ex2_args = (message)
RAFK-cmd_ex2_res = @user2 you remained AFK: 🏃 ⌨️ and left a note: (message)

# RAFK Admonitions
RAFK-adm_title = Maximum Time!
RAFK-adm_msg = From the moment you send a message in the chat, you have 2 minutes to return to AFK status.

## AFKReturn
AFKReturn-afk = { $status } { $emoji } (was away for { $a_time } { $clock })
AFKReturn-content = { $status } { $emoji } and left a note: { $message } (was away for { $a_time } { $clock })
