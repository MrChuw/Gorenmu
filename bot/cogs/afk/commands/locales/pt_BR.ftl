## AFK
AFK-afk = { $status } { $emoji }
AFK-content = { $status } { $emoji } e deixou uma nota com: { $content }
AFK-deco_helper = Comando para definir seu status.
AFK-deco_usage = Como usar: { $prefix }Afk (mensagem)
AFK-deco_description = Este comando define seu status para AFK.

# AFK Examples
AFK-cmd_ex1_res = você foi AFK: 🏃 ⌨️
AFK-cmd_ex2_args = Mensagem legal.
AFK-cmd_ex2_res = você ficou AFK: 🏃 ️ e deixou um bilhete com: Mensagem legal.

# AFK Admonitions
AFK-adm_title = Tamanho máximo!
AFK-adm_msg = A mensagem não poderia ser mais de 450 caracteres.

# AFK Activities (Label, Emoji, Ação, No momento, Passado, Contexto)
AFK-prop_list = está, você, você continuou, você
AFK-afk_list = afk, 🏃⌨, ficou ausente, ausente, voltou, ausente
AFK-read_list = read, 📖, foi ler, lendo, leu, lendo
AFK-brb_list = brb, 🏃⌨, volta logo, ausente, voltou, ausente
AFK-eat_list = food, 🍽, foi comer, comendo, comeu, comendo
AFK-play_list = game, 🎮, foi jogar, jogando, jogou, jogando
AFK-sleep_list = gn, 💤, foi dormir, dormindo, acordou, dormindo
AFK-study_list = study, 📚, foi estudar, estudando, estudou, estudando
AFK-art_list = art, 🎨, foi desenhar, desenhando, desenhou, desenhando
AFK-watch_list = watch, 📺, foi assistir, assistindo, assistiu, assistindo
AFK-shower_list = shower, 🚿, foi tomar banho, no banho, tomou banho, no banho
AFK-code_list = code, 💻, foi programar, programando, programou, programando
AFK-work_list = work, 💼, foi trabalhar, trabalhando, trabalhou, trabalhando

## IsAFK
IsAFK-bot = Estou sempre aqui... assistindo.
IsAFK-author = você não está afk... obviamente.
IsAFK-is_afk = @{ $name } { $status } { $emoji } (há { $time })
IsAFK-is_afk_content = @{ $name } { $status } { $emoji } e deixou uma nota: { $message } (há { $time })
IsAFK-is_not_afk = @{ $name } não é AFK.
IsAFK-deco_helper = Digite o comando e o nome do usuário para ver se eles são AFK.
IsAFK-deco_usage = Como usar: { $prefix }IsAfk (nome de usuário)
IsAFK-deco_description = Este comando verifica se um usuário é AFK ou não.

# IsAFK Examples
IsAFK-cmd_ex1_args = usuário2
IsAFK-cmd_ex1_res = @usuário2 não está AFK.
IsAFK-cmd_ex2_args = usuário3
IsAFK-cmd_ex2_res = @usuário3 está AFK.

## RAFK
RAFK-return_expired = para retornar AFK
RAFK-afk = { $status } { $emoji }
RAFK-content = { $status } { $emoji } e deixou uma nota com: { $content }
RAFK-deco_helper = Retornar ao status AFK.
RAFK-deco_usage = Para usar: { $prefix }rafk
RAFK-deco_description = Este comando é usado para retornar ao status AFK.

# RAFK Examples
RAFK-cmd_ex1_res = @usuário2 você permaneceu AFK: 🏃 ⌨️
RAFK-cmd_ex2_args = (mensagem)
RAFK-cmd_ex2_res = @usuário2 você permaneceu AFK: 🏃 ⌨️ e deixou uma nota: (mensagem)

# RAFK Admonitions
RAFK-adm_title = Tempo máximo!
RAFK-adm_msg = A partir do momento em que você envia uma mensagem no chat, você tem 2 minutos para retornar ao status AFK.

## AFKReturn
AFKReturn-afk = { $status } { $emoji } (estava ausente por { $a_time } { $clock })
AFKReturn-content = { $status } { $emoji } e deixou uma nota: { $message } (estava ausente por { $a_time } { $clock })
