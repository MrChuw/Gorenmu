## Cookies
Cookies-invalid_option = Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"
Cookies-daily_limit_reached = Você ainda está em cooldown, espere { $cooldown } até o próximo lote! ⌛
Cookies-user_not_found = o usuário @{ $name } ainda não foi registrado e não usou nenhum comando de cookie.
Cookies-cookie_not_found = O usuário @{ $name } ainda não usou nenhum comando relacionado aos cookies.

Cookies-deco_helper = Comando usado para gerenciar cookies.
Cookies-deco_usage = Para usar: { $prefix }cookie Eat|Count|Gift|Stock|Top|SlotMachine (opções)
Cookies-deco_description = Comando usado para gerenciar cookies.

## Eat
Cookie-Eat-not_eat = Você não comeu nada, nossa!
Cookie-Eat-negative_eat = Para comer { $amount } cookies, você deve primeiro saber como reverter entropia.
Cookie-Eat-multiple_eat = você comeu { $amount } cookies de uma só vez. 🥠
Cookie-Eat-eat = { $text }
Cookie-Eat-random_line = lines_pt_br.txt

Cookie-Eat-deco_helper = Pegue seu biscoito da sorte diário.
Cookie-Eat-deco_usage = Para usar: { $prefix }cookie eat
Cookie-Eat-deco_description = Este comando é usado para pegar seu biscoito da sorte diário.

# Eat Examples
Cookie-Eat-cmd_ex1_res = (Mensagem de sorte aleatória de uma lista)

## Count
Cookie-Count-cc_bot_nick = Tenho cookies infinitos e dou uma fração deles para você.

Cookie-Count-format_cookie_count =
    { $mention } { $consumed ->
        [0] { "" }
        *[other] { $verb } já comeu { $consumed } biscoitos 🥠.
    }{ $stocked ->
        [0] { "" }
        *[other] {" "}Tem { $stocked } em estoque.
    }{ $received ->
        [0] { "" }
        *[other] {" "}Foi apresentado com { $received }.
    }{ $donated ->
        [0] { "" }
        *[other] {" "}Presenteou { $donated }.
    }{ $unredeemed ->
        [0] { "" }
        *[other] {" "}E tem um total de { $unredeemed } não resgatados.
    }{ $total ->
        [0] { "" }
        *[other] {" "}E um total de { $total } cookies já foram adicionados à conta.
    }

Cookie-Count-deco_helper = Veja o status dos cookies.
Cookie-Count-deco_usage = Para usar: { $prefix }cookie count (nome_do_usuário)
Cookie-Count-deco_description = Veja quantos cookies você ou outra pessoa possuem.

# Count Examples
Cookie-Count-cmd_ex1_res = (Status sobre sua conta de cookies)
Cookie-Count-cmd_ex2_res = (Status sobre a conta de cookies do outro usuário)

## Gift
Cookie-Gift-gift_bot_nick = Não quero a seu cookie.
Cookie-Gift-gift_user_himself = você tentou presentear você mesmo, uau!
Cookie-Gift-gift_no_stock_but_cooldown = Para presentear, você deve primeiro resgatar os { $amount } cookies que você tem disponíveis.
Cookie-Gift-not_gifted = Você não deu nada de presente, uau!
Cookie-Gift-negative_gift = Você não pode dar cookies negativos, a menos que seja um ladrão de cookies... e você não é, certo?
Cookie-Gift-multiple_gift = você presenteou @{ $person } com { $amount } cookie 🎁
Cookie-Gift-gift = você deu um cookie para @{ $person } 🎁
Cookie-Gift-gift_on_cooldown_no_stock = Você não tem nenhum cookie 🍪 armazenado ou aguardando para ser resgatado. O próximo chega em { $cooldown }.

Cookie-Gift-deco_helper = Presenteie alguém com seus cookies.
Cookie-Gift-deco_usage = Para usar: { $prefix }cookie gift (nome_do_usuário) (quantidade|all)
Cookie-Gift-deco_description = Presenteie alguém com seus cookies.

# Gift Examples
Cookie-Gift-cmd_ex1_res = Você deu 1 cookie 🎁 para @outro_usuário
Cookie-Gift-cmd_ex2_res = Você deu 2 cookies 🎁 para @outro_usuário
Cookie-Gift-cmd_ex3_res = Você deu (todos os cookies da sua conta) 🎁 para @outro_usuário

# Gift Admonitions
Cookie-Gift-adm1_title = Cuidado com o 'all'!
Cookie-Gift-adm1_msg = Cuidado ao usar 'all', pois você irá transferir não apenas os cookies não coletados, mas também os que você já armazenou.

## Stock
Cookie-Stock-stock = você estocou { $amount } cookies 🍪, o próximo sai em 6h.
Cookie-Stock-stock_not_daily = você estocou { $amount } cookies 🍪.
Cookie-Stock-stock_not_enough_cookies = você só pode estocar { $amount }.

Cookie-Stock-deco_helper = Estoque seus cookies diários para usar depois.
Cookie-Stock-deco_usage = Para usar: { $prefix }cookie stock (all)
Cookie-Stock-deco_description = Guarde seus cookies diários em vez de usá-los imediatamente.

# Stock Examples
Cookie-Stock-cmd_ex1_res = Você estocou 1 cookie 🍪, o próximo estará disponível em 6h.
Cookie-Stock-cmd_ex2_res = Você estocou (quantidade de todos disponíveis) cookies 🍪.

## Top
Cookie-Top-rank_dict =
    .stocked = stocked, stocked
    .streak = streak, streak
    .consumed = consumed, cookiers
    .donated = donated, givers
    .received = received, receivers
    .total = total, total

Cookie-Top-ranks = as categoria são: { $ranks }

Cookie-Top-top10_ish = top { $length } { $title }: { $tops } || Você está na { $index }ª posição na classificação com { $amount }.

Cookie-Top-deco_helper = Veja quem são os melhores comedores, doadores ou acumuladores de cookies.
Cookie-Top-deco_usage = Para usar: { $prefix }cookie top (ou passe uma das opções stocked | streak | consumed | donated | received | total)
Cookie-Top-deco_description = Veja quem são os melhores em acumular, doar, comer ou manter sequência de cookies.

# Top Examples
Cookie-Top-cmd_ex1_res = Top 10 acumuladores: 🏆 @nome_usuário: (10) 🥈 ...
Cookie-Top-cmd_ex2_res = Top 10 doadores: 🏆 @nome_usuário: (10) 🥈 ...

## SlotMachine
Cookie-SlotMachine-invalid_amount = você está tentando apostar { $amount } mas só tem { $available } cookies não resgatados.
Cookie-SlotMachine-cookie_win_suffix = e ganhou { $total } cookies. { $suffix }
Cookie-SlotMachine-cookie_loss_suffix = e perdeu tudo. { $suffix }
Cookie-SlotMachine-accumulated_message = { $prefix } Você usou { $amount } cookie(s) não resgatado(s) { $suffix } { $emote }
Cookie-SlotMachine-last_cookie_message = { $prefix } Você usou seu último cookie disponível { $suffix } { $emote }
Cookie-SlotMachine-time_suffix = O próximo está disponível em { $time }.

Cookie-SlotMachine-deco_helper = Aposte seus cookies para tentar ganhar mais.
Cookie-SlotMachine-deco_usage = Para usar: { $prefix }cookie slotmachine (all pode ser usado para apostar todos os cookies não coletados rapidamente)
Cookie-SlotMachine-deco_description = Use a máquina caça-níquel de cookies para tentar multiplicar seus cookies.

# SlotMachine Examples
Cookie-SlotMachine-cmd_ex1_res = (Resultado da máquina caça-níquel.)
Cookie-SlotMachine-cmd_ex2_res = (Resultado da máquina caça-níquel.)
