# Pet
Pet-pet_pat = Fez carinho em: { $name } { $emoji } { $emote }
Pet-pet_not_found = Não encontrei nenhum pet com o nome de { $name }.

Pet-deco_helper = Usado para fazer carinho em um dos seus pets ou ver todos os seus pets.
Pet-deco_usage = Para usar: { $prefix }pet (nome do pet)
Pet-deco_description = Usado para fazer carinho em um dos seus pets ou ver todos os seus pets.

Pet-cmd_ex1_args = xXCoolNickXx
Pet-cmd_ex1_res = Fez carinho em: xXCoolNickXx 🐸 😚

# PetBuy
PetBuy-no_cookies = Você precisa ter cookies para comprar pets.
PetBuy-not_enough_cookies = Você não tem cookies o suficiente para comprar { $specie }. Junte mais { $price } para conseguir comprar.
PetBuy-pet_buy = Parabéns por comprar { $specie } { $emoji }, para mudar o nome do seu novo pet use { $prefix }{ $command } { $pet_id } (novo nome)
PetBuy-not_found = Eu não tenho nenhuma especie de { $specie } disponivel para você hoje, tente outro dia, ou pergunte para outras pessoas se não estão dispostas a trocar.
PetBuy-pet_list = Os pets disponiveis para você comprar hoje são: { $pets }

PetBuy-deco_helper = Comando usada para comprar pets, disponibilidade vai variar de acordo com cada usuario. Tambem pode ser usado para verificar os pets disponiveis para o dia.
PetBuy-deco_usage = Para usar: { $prefix }pet buy (especie) (opcional pet_name:xXCoolNickXx)
PetBuy-deco_description = Comando usada para comprar pets, disponibilidade vai variar de acordo com cada usuario. Tambem pode ser usado para verificar os pets disponiveis para o dia.

# PetList
PetList-bot_name = Eu crio todos os pets e distibuo uma pequena quantidade para vcs, em troca de um pequeno valor monetario.
PetList-mention_denied = Infelizmente { $name } não permite que outros usuarios verifiquem os pets dele.
PetList-pet = { $mention } possui: { $pets }
PetList-no_pets = adquira um dos pets disponíveis ({ $prefix }{ $invocation }) em troca de cookies.
PetList-user_no_pets = { $mention } não possui nenhum pet.
PetList-deco_helper = Comando utilizado para ver a lista de pets de alguem.
PetList-deco_usage = Para usar: {$prefix}pet (nick do usuário)
PetList-deco_description = Comando utilizado para ver a lista de pets de alguem.

PetName-cmd_ex1_args = xXCoolNickXx
PetName-cmd_ex1_res = @xXCoolNickXx possui: pet1, pet2, pet3, pet4, pet5...

# PetName
PetName-invalid_id = { $pet_id } não é um id valido, use { $prefix }pet list. Para ver os pets que você tem.
PetName-pet_renamed = { $pet_id } foi renomeado para { $pet_name }.
PetName-invalid_name = O nome { $pet_name } é inválido. O nome deve começar obrigatoriamente com uma letra ou número e não pode ultrapassar { $max_size } caracteres. Caracteres especiais e emojis são permitidos.

PetName-deco_helper = Comando utilizado para renomear seus pets.
PetName-deco_usage = Para usar: { $prefix }pet name (id) (name)
PetName-deco_description = Comando utilizado para renomear seus pets.

# PetSell
PetSell-bot_name = Eu não aceito devoluções.
PetSell-price_not_int = Preço deve ser um número inteiro válido.
PetSell-price_third = O preço mínimo para vender o pet é 1/3 do valor original.
PetSell-yourself = Você não pode vender seu pet próprio para si mesmo.
PetSell-not_enough_cookies = Não há suficientes cookies em { $name } para comprar esse pet.
PetSell-no_pets = Você não tem nenhum pet para vender.
PetSell-start = Iniciando venda do pet { $name } por { $price } cookies. { $buyer } tem 30 segundos para confirmar a venda.
PetSell-sold = Venda realizada com sucesso! Você recebeu { $earnings } cookies na forma de bônus.
PetSell-refused = A venda foi recusada.
PetSell-timeout = O tempo para confirmar a venda esgotou. A venda não ocorreu.
PetSell-pet_not_find = Não foi possível encontrar o pet com id { $id }.

PetSell-deco_helper = Comando utilizado para vender pets entres usuarios.
PetSell-deco_usage = Para usar: { $prefix }pet sell (user_name) (pet_id) (price)
PetSell-deco_description =Comando utilizado para vender pets entres usuarios.

PetSell-cmd_ex1_args = xXCoolNickXx 1 100
PetSell-cmd_ex1_res = ...
