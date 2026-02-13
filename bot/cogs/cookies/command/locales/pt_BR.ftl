## Cookies
Cookies-invalid_option = Escolha entre uma das opções "eat", "count", "top", "gift", "stock" ou "sm"
Cookies-daily_limit_reached = Você ainda está em cooldown, espere { $cooldown } até o próximo lote! ⌛
Cookies-user_not_found = o usuário @{ $name } ainda não foi registrado e não usou nenhum comando de cookie.
Cookies-cookie_not_found = O usuário @{ $name } ainda não usou nenhum comando relacionado aos cookies.

Cookies-deco_helper = Comando usado para gerenciar cookies.
Cookies-deco_usage = Para usar: { $prefix }cookie Eat|Count|Gift|Stock|Top|SlotMachine (opções)
Cookies-deco_description = Comando usado para gerenciar cookies.

## Eat
Eat-not_eat = Você não comeu nada, nossa!
Eat-negative_eat = Para comer { $amount } cookies, você deve primeiro saber como reverter entropia.
Eat-multiple_eat = você comeu { $amount } cookies de uma só vez. 🥠
Eat-eat = { $text }
Eat-random_line = lines_pt_br.txt

Eat-deco_helper = Pegue seu biscoito da sorte diário.
Eat-deco_usage = Para usar: { $prefix }cookie eat
Eat-deco_description = Este comando é usado para pegar seu biscoito da sorte diário.

# Eat Examples
Eat-cmd_ex1_res = (Mensagem de sorte aleatória de uma lista)

## Count
Count-cc_bot_nick = Tenho cookies infinitos e dou uma fração deles para você.

Count-format_cookie_count =
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

Count-deco_helper = Veja o status dos cookies.
Count-deco_usage = Para usar: { $prefix }cookie count (nome_do_usuário)
Count-deco_description = Veja quantos cookies você ou outra pessoa possuem.

# Count Examples
Count-cmd_ex1_res = (Status sobre sua conta de cookies)
Count-cmd_ex2_res = (Status sobre a conta de cookies do outro usuário)

## Gift
Gift-gift_bot_nick = Não quero a seu cookie.
Gift-gift_user_himself = você tentou presentear você mesmo, uau!
Gift-gift_no_stock_but_cooldown = Para presentear, você deve primeiro resgatar os { $amount } cookies que você tem disponíveis.
Gift-not_gifted = Você não deu nada de presente, uau!
Gift-negative_gift = Você não pode dar cookies negativos, a menos que seja um ladrão de cookies... e você não é, certo?
Gift-multiple_gift = você presenteou @{ $person } com { $amount } cookie 🎁
Gift-gift = você deu um cookie para @{ $person } 🎁
Gift-gift_on_cooldown_no_stock = Você não tem nenhum cookie 🍪 armazenado ou aguardando para ser resgatado. O próximo chega em { $cooldown }.

Gift-deco_helper = Presenteie alguém com seus cookies.
Gift-deco_usage = Para usar: { $prefix }cookie gift (nome_do_usuário) (quantidade|all)
Gift-deco_description = Presenteie alguém com seus cookies.

# Gift Examples
Gift-cmd_ex1_res = Você deu 1 cookie 🎁 para @outro_usuário
Gift-cmd_ex2_res = Você deu 2 cookies 🎁 para @outro_usuário
Gift-cmd_ex3_res = Você deu (todos os cookies da sua conta) 🎁 para @outro_usuário

# Gift Admonitions
Gift-adm1_title = Cuidado com o 'all'!
Gift-adm1_msg = Cuidado ao usar 'all', pois você irá transferir não apenas os cookies não coletados, mas também os que você já armazenou.

## Stock
Stock-stock = você estocou { $amount } cookies 🍪, o próximo sai em 6h.
Stock-stock_not_daily = você estocou { $amount } cookies 🍪.
Stock-stock_not_enough_cookies = você só pode estocar { $amount }.

Stock-deco_helper = Estoque seus cookies diários para usar depois.
Stock-deco_usage = Para usar: { $prefix }cookie stock (all)
Stock-deco_description = Guarde seus cookies diários em vez de usá-los imediatamente.

# Stock Examples
Stock-cmd_ex1_res = Você estocou 1 cookie 🍪, o próximo estará disponível em 6h.
Stock-cmd_ex2_res = Você estocou (quantidade de todos disponíveis) cookies 🍪.

## Top
Top-rank_dict =
    .stocked = stocked, stocked
    .streak = streak, streak
    .consumed = consumed, cookiers
    .donated = donated, givers
    .received = received, receivers
    .total = total, total

Top-ranks = as categoria são: { $ranks }

Top-top10_ish = top { $length } { $title }: { $tops } || Você está na { $index }ª posição na classificação com { $amount }.

Top-deco_helper = Veja quem são os melhores comedores, doadores ou acumuladores de cookies.
Top-deco_usage = Para usar: { $prefix }cookie top (ou passe uma das opções stocked | streak | consumed | donated | received | total)
Top-deco_description = Veja quem são os melhores em acumular, doar, comer ou manter sequência de cookies.

# Top Examples
Top-cmd_ex1_res = Top 10 acumuladores: 🏆 @nome_usuário: (10) 🥈 ...
Top-cmd_ex2_res = Top 10 doadores: 🏆 @nome_usuário: (10) 🥈 ...

## SlotMachine
SlotMachine-invalid_amount = você está tentando apostar { $amount } mas só tem { $available } cookies não resgatados.
SlotMachine-cookie_win_suffix = e ganhou { $total } cookies. { $suffix }
SlotMachine-cookie_loss_suffix = e perdeu tudo. { $suffix }
SlotMachine-accumulated_message = { $prefix } Você usou { $amount } cookie(s) não resgatado(s) { $suffix } { $emote }
SlotMachine-last_cookie_message = { $prefix } Você usou seu último cookie disponível { $suffix } { $emote }
SlotMachine-time_suffix = O próximo está disponível em { $time }.

SlotMachine-deco_helper = Aposte seus cookies para tentar ganhar mais.
SlotMachine-deco_usage = Para usar: { $prefix }cookie slotmachine (all pode ser usado para apostar todos os cookies não coletados rapidamente)
SlotMachine-deco_description = Use a máquina caça-níquel de cookies para tentar multiplicar seus cookies.

# SlotMachine Examples
SlotMachine-cmd_ex1_res = (Resultado da máquina caça-níquel.)
SlotMachine-cmd_ex2_res = (Resultado da máquina caça-níquel.)
