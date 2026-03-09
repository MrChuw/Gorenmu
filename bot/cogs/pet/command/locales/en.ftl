# Pet
Pet-pet_pat = Patted: { $name } { $emoji } { $emote }
Pet-pet_not_found = Could not find any pet with the name of { $name }.

Pet-deco_helper = Used to give a pat to one of your pets or see all your pets.
Pet-deco_usage = To use: { $prefix }pet (pet name)
Pet-deco_description = Used to give a pat to one of your pets or see all your pets.

Pet-cmd_ex1_args = xXCoolNickXx
Pet-cmd_ex1_res = Patted: xXCoolNickXx 🐸 😚

# PetBuy
PetBuy-no_cookies = You need cookies to buy pets.
PetBuy-not_enough_cookies = You do not have enough cookies to buy { $specie }. Join more { $price } to be able to buy it.
PetBuy-pet_buy = Congratulations on buying { $specie } { $emoji }, to change the name of your new pet use { $prefix }{ $command } { $pet_id } (new name)
PetBuy-not_found = I do not have any { $specie } available for you today, try another day or ask other people if they are not willing to trade.
PetBuy-pet_list = The pets available for you to buy today are: { $pets }

PetBuy-deco_helper = Command used to buy pets. Availability varies depending on each user. It can also be used to check the available pets of the day.
PetBuy-deco_usage = To use: { $prefix }pet buy (species) (optional pet_name:xXCoolNickXx)
PetBuy-deco_description = Command used to buy pets. Availability varies depending on each user. It can also be used to check the available pets of the day.

# PetList
PetList-bot_name = I create all pets and distribute a small amount for you, in exchange for a small monetary value.
PetList-mention_denied = Unfortunately { $name } does not allow other users to check their pets.
PetList-pet = { $mention } has: { $pets }
PetList-no_pets = acquire one of the available pets ({ $prefix }{ $invocation }) in exchange for cookies.
PetList-user_no_pets = { $mention } does not have any pets.
PetList-deco_helper = Command used to view someone's pet list.
PetList-deco_usage = To use: {$prefix}pet (user nick)
PetList-deco_description = Command used to view someone's pet list.

PetName-cmd_ex1_args = xXCoolNickXx
PetName-cmd_ex1_res = @xXCoolNickXx has: pet1, pet2, pet3, pet4, pet5...

# PetName
PetName-invalid_id = { $pet_id } is not a valid ID. Use { $prefix }pet list. To see the pets you have.
PetName-pet_renamed = { $pet_id } was renamed to { $pet_name }.
PetName-invalid_name = The name { $pet_name } is invalid. The name must start with a letter or number and cannot exceed { $max_size } characters. Special characters and emojis are allowed.

PetName-deco_helper = Command used to rename your pets.
PetName-deco_usage = To use: { $prefix }pet name (id) (name)
PetName-deco_description = Command used to rename your pets.

# PetSell
PetSell-bot_name = I do not accept returns.
PetSell-price_not_int = Price must be a valid integer number.
PetSell-price_third = The minimum price to sell the pet is 1/3 of the original value.
PetSell-yourself = You cannot sell your own pet to yourself.
PetSell-not_enough_cookies = There are not enough cookies in { $name } to buy this pet.
PetSell-no_pets = You do not have any pets to sell.
PetSell-start = Starting the sale of the pet { $name } for { $price } cookies. { $buyer } has 30 seconds to confirm the sale.
PetSell-sold = Sale completed successfully! You received { $earnings } cookies as a bonus.
PetSell-refused = The sale was refused.
PetSell-timeout = The time to confirm the sale expired. The sale did not occur.
PetSell-pet_not_find = Could not find pet with ID { $id }.

PetSell-deco_helper = Command used to sell pets between users.
PetSell-deco_usage = To use: { $prefix }pet sell (user_name) (pet_id) (price)
PetSell-deco_description = Command used to sell pets between users.

PetSell-cmd_ex1_args = xXCoolNickXx 1 100
PetSell-cmd_ex1_res = ...
