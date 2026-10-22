## Cookies
Cookies-invalid_option = Choose from one of the options "eat", "count", "top", "gift", "stock" or "sm"
Cookies-daily_limit_reached = You're still on cooldown, wait { $cooldown } until the next batch! ⌛
Cookies-user_not_found = user @{ $name } has not yet been registered and has not used any cookie commands.
Cookies-cookie_not_found = User @{ $name } has not yet used any command related to cookies.

Cookies-deco_helper = Command used to manage cookies.
Cookies-deco_usage = To use: { $prefix }cookie Eat|Count|Gift|Stock|Top|SlotMachine (options)
Cookies-deco_description = Command used to manage cookies.

## Eat
Cookie-Eat-not_eat = You didn't eat anything, wow!
Cookie-Eat-negative_eat = To eat { $amount } cookies, you must first know how to reverse entropy.
Cookie-Eat-multiple_eat = you ate { $amount } cookies in one sitting. 🥠
Cookie-Eat-eat = { $text }
Cookie-Eat-random_line = lines_en.txt

Cookie-Eat-deco_helper = Get your daily fortune.
Cookie-Eat-deco_usage = To use: { $prefix }cookie eat
Cookie-Eat-deco_description = This command is used to get a daily fortune.

# Eat Examples
Cookie-Eat-cmd_ex1_res = (random fortune from a list)

## Count
Cookie-Count-cc_bot_nick = I have infinite cookies, and I give away a fraction of them to you.

Cookie-Count-format_cookie_count =
    { $mention } { $consumed ->
        [0] { "" }
        *[other] { $verb } already eaten { $consumed } cookies 🥠.
    }{ $stocked ->
        [0] { "" }
        *[other] {" "}Has { $stocked } in stock.
    }{ $received ->
        [0] { "" }
        *[other] {" "}Was presented with { $received }.
    }{ $donated ->
        [0] { "" }
        *[other] {" "}Gifted { $donated }.
    }{ $unredeemed ->
        [0] { "" }
        *[other] {" "}And has a total of { $unredeemed } unredeemed.
    }{ $total ->
        [0] { "" }
        *[other] {" "}And there were a total of { $total } cookies have already been added to the account.
    }

Cookie-Count-deco_helper = Get status about cookies.
Cookie-Count-deco_usage = To use: { $prefix }cookie count (user_name)
Cookie-Count-deco_description = Get status about cookies.

# Count Examples
Cookie-Count-cmd_ex1_res = (status about your cookie account)
Cookie-Count-cmd_ex2_res = (status about other_user cookie account)

## Gift
Cookie-Gift-gift_bot_nick = I don't want your cookie.
Cookie-Gift-gift_user_himself = Did you try gifting it yourself, wow!
Cookie-Gift-gift_no_stock_but_cooldown = To gift, you must first redeem the { $amount } cookies you have available.
Cookie-Gift-not_gifted = You didn't gift anything, wow!
Cookie-Gift-negative_gift = You can't give negative cookies unless you're a cookie thief... and you're not, right?
Cookie-Gift-multiple_gift = you gifted @{ $person } with { $amount } cookie 🎁
Cookie-Gift-gift = you gave @{ $person } a cookie 🎁
Cookie-Gift-gift_on_cooldown_no_stock = You don`t have any cookies 🍪 stored or waiting to be redeemed. The next one arrives in { $cooldown }.

Cookie-Gift-deco_helper = Gift someone your daily cookie.
Cookie-Gift-deco_usage = To use: { $prefix }cookie gift (user_name) (amount|all)
Cookie-Gift-deco_description = Gift someone your daily cookie.

# Gift Examples
Cookie-Gift-cmd_ex1_res = you gifted @other_user with 1 cookie 🎁
Cookie-Gift-cmd_ex2_res = you gifted @other_user with 2 cookie 🎁
Cookie-Gift-cmd_ex3_res = you gifted @other_user with (all the cookies in your account) cookie 🎁

# Gift Admonitions
Cookie-Gift-adm1_title = Careful With All
Cookie-Gift-adm1_msg = Be careful with all, because you will transfer not only the unredeemed ones, but also the ones you have saved.

## Stock
Cookie-Stock-stock = you stocked { $amount } cookies 🍪, the next one comes out in 6h.
Cookie-Stock-stock_not_daily = you stocked { $amount } cookies 🍪.
Cookie-Stock-stock_not_enough_cookies = you can only stock { $amount } 🍪.

Cookie-Stock-deco_helper = Stock your daily cookie.
Cookie-Stock-deco_usage = To use: { $prefix }cookie stock (all)
Cookie-Stock-deco_description = Stock your daily cookie.

# Stock Examples
Cookie-Stock-cmd_ex1_res = you stocked 1 cookies 🍪, the next one comes out in 6h.
Cookie-Stock-cmd_ex2_res = you stocked (number of all available) cookies 🍪.

## Top
Cookie-Top-rank_dict =
    .stocked = stocked, stocked
    .streak = streak, streak
    .consumed = consumed, cookiers
    .donated = donated, givers
    .received = received, receivers
    .total = total, total

Cookie-Top-ranks = the ranks are: { $ranks }

Cookie-Top-top10_ish = top { $length } { $title }: { $tops } || You are in the { $index ->
    [one] { $index }st
    [two] { $index }nd
    [three] { $index }rd
    *[other] { $index }th
} position in the ranking with { $amount }.

Cookie-Top-deco_helper = See who are the top cookie eaters or donors.
Cookie-Top-deco_usage = To use: { $prefix }cookie top (or pass one of the options stocked | streak | consumed | donated | received | total)
Cookie-Top-deco_description = See who are the top cookie eaters or donors.

# Top Examples
Cookie-Top-cmd_ex1_res = top 10 stocked: 🏆 @user_name: (10) 🥈 ...
Cookie-Top-cmd_ex2_res = top 10 givers: 🏆 @user_name: (10) 🥈 ...

## SlotMachine
Cookie-SlotMachine-invalid_amount = you are trying to bet { $amount } but you only have { $available } unredeemed cookies.
Cookie-SlotMachine-cookie_win_suffix = and earned { $total } cookies. { $suffix }
Cookie-SlotMachine-cookie_loss_suffix = and lost everything. { $suffix }
Cookie-SlotMachine-accumulated_message = { $prefix } You have used { $amount } unredeemed cookie(s) { $suffix } { $emote }
Cookie-SlotMachine-last_cookie_message = { $prefix } You used your last available cookie { $suffix } { $emote }
Cookie-SlotMachine-time_suffix = The next one is available in { $time }.

Cookie-SlotMachine-deco_helper = Bet your daily cookie for a chance to win more.
Cookie-SlotMachine-deco_usage = To use: { $prefix }cookie slotmachine (all can be used to bet all unclaimed cookies quickly)
Cookie-SlotMachine-deco_description = Bet your daily cookie for a chance to win others.

# SlotMachine Examples
Cookie-SlotMachine-cmd_ex1_res = (the results of the slotmachine.)
Cookie-SlotMachine-cmd_ex2_res = (the results of the slotmachine.)
