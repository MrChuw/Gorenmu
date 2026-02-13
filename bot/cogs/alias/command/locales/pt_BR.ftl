## Table
Table-alias_table_headers = Nome de Alias, Descrição, Invocação, Argumentos, Links para, Atualizado, Criado
Table-alias_table_replaces = Nenhuma descrição, Sem argumentos, Nada
Table-alias_table_name = { $name } aliases

## Alias
Alias-dont_have_alias = Você não tem o alias "{ $name }"!
Alias-alias_invalid_name = Seu nome de alias não é válido! Seu alias deve conter apenas letras, números e ter entre 2-30 caracteres de comprimento.
Alias-user_has_no_alias = O usuário { $name } não possui aliases registrados.
Alias-deco_helper = Comando usado para gerir aliases.
Alias-deco_usage = Para usar: { $prefix }alias add|check|copy|describe|edit|link|remove|rename (opções)

## Add
Add-no_command_to_add = Você não enviou um comando! Use: { $prefix }alias add (nome) (comando) (…argumentos)
Add-alias_name_conflict = Não é possível adicionar o alias "{ $name }" - você já possui um! Você pode “editar” sua definição, “renomear” ou “removê-la”.
Add-alias_created = Seu alias "{ $name }" foi criado com sucesso.
Add-command_dont_exist = Não é possível criar um alias! O comando "{ $name }" não existe.
Add-deco_helper = Este subcomando é usado para adicionar um alias.
Add-deco_usage = Como usar: { $prefix }alias add (nome) (comando) (…argumentos)
Add-deco_description = Este subcomando é usado para adicionar um alias.

# Add Examples
Add-cmd_ex1_prefix = ## Como criar um alias:{"\n"}- O exemplo a seguir usa [pipe](pipe.md) para passar a resposta de um comando para outro.
Add-cmd_ex1_args = add cool_name choice 1234 123456 | count
Add-cmd_ex1_res = seu alias "cool_name" foi criado com sucesso.
Add-cmd_ex1_suffix = No exemplo acima, criamos um alias chamado `cool_name`. O alias invocará o comando `choice` com os argumentos "1234" e "123456", e o resultado de `choice` será enviado para o comando `count`.

Add-cmd_ex2_prefix = ## Para usar o alias:
Add-cmd_ex2_args = { $prefix }{ $prefix }cool_name
Add-cmd_ex2_res = há um total de 4 caracteres. Entre eles, 0 são marcas de pontuação, 0 são letras maiúsculas, e 0 são caracteres especiais.
Add-cmd_ex2_suffix = Para usar o alias, basta usar `{ $prefix }{ $prefix }` seguido pelo nome do alias ({ $prefix } é o prefixo padrão do bot, se o prefixo do chat é diferente, basta repeti-lo 2 (dois) vezes e então o nome do alias).

# Add Admonitions
Add-adm1_title = Restrições para nomes de aliases!
Add-adm1_msg = - Deve ter entre 2 e 30 caracteres.{"\n"}- Pode conter letras, números, hífens (-), underscores (_), e uma ampla gama de caracteres Unicode (©), incluindo emojis (🔥).
Add-adm2_title = Cooldown para aliases criados!
Add-adm2_msg = Ao criar um alias, o tempo de espera (cooldown) do alias será o maior tempo de espera entre os comandos utilizados no alias. Portanto, se um comando pode ser usado 1x a cada 5 segundos e outro 3x a cada 10 segundos, o tempo de espera do alias será 1x a cada 5 segundos.

## Check
Check-user_alias_list = Lista dos seus aliases: { $names } | Lista detalhada: { $url }
Check-no_alias_found = Não foi possível encontrar { $alias_name } em { $user_name } aliases ou em qualquer um dos seus aliases!
Check-list_of_alias_of = Lista de aliases de { $mention }: { $url }
Check-list_of_special_case =
    Caso especial!
    Seu alias "{ $name }": { $url1 }
    Lista dos aliases de { $name }: { $url2 }
Check-alias_not_found = { $mention } não tem o alias "{ $alias }"!
Check-alias_deleted = { $alias } alias é um link para um alias diferente, mas o original foi excluído.
Check-normal_message = { $name } || Invoca: { $invocation } || Link: { $url }
Check-appendix_message = Este alias é um link para "{ $parent }" criado por { $original }. O alias tem os argumentos: { $invocation } || Link: { $url }
Check-appendix = Este alias é um link para "{ $name }" feito por { $owner }.
Check-message = { $user } alias "{ $name }" tem os argumentos: { $arg1 } { $arg2 }

Check-deco_helper = Este subcomando é usado para verificar informações de um alias.
Check-deco_usage = Como usar: { $prefix }alias check cool_name
Check-deco_description = Este subcomando é usado para verificar informações de um alias.

# Check Examples
Check-cmd_ex1_prefix = ## Como verificar um alias:
Check-cmd_ex1_args = check cool_name
Check-cmd_ex1_res = Usuário, o alias "cool_name" tem os argumentos: choice 1234 123456 | count || Link: (URL)

## Copy
Copy-alias_not_provided = Nenhum alias de destino fornecido!
Copy-target_alias_invalid_name = O nome do alias copiado não é válido e portanto não pode ser copiado!
Copy-no_alias_found = Não consegui encontrar { $alias } no usuário { $name }!
Copy-link_to_a_link = Você não pode copiar links para outros aliases. Em vez disso, use { $prefix }alias copy { $user } { $target }
Copy-copy_success = Alias "{ $name }" copiado com sucesso.
Copy-copy_with_name_of = Alias "{ $target }" copiado com sucesso. Com o nome "{ $name }".

Copy-deco_helper = Este subcomando é usado para copiar um alias.
Copy-deco_usage = Como usar: { $prefix }alias copy (usuário) (alias) (…argumentos)
Copy-deco_description = Este subcomando é usado para copiar um alias.

# Copy Examples
Copy-cmd_ex1_prefix = ## Como copiar um alias:
Copy-cmd_ex1_args = copy <usuário> cool_name
Copy-cmd_ex1_res = Usuário, alias "cool_name" copiado com sucesso.
Copy-cmd_ex1_suffix = Para copiar um alias, você só precisa do nome de usuário e do nome do alias.

## Describe
Describe-no_args_to_parse = Você não forneceu um alias ou uma descrição! Use: { $prefix }alias describe (nome) (…descrição)
Describe-description_updated = A descrição do alias "{ $name }" foi atualizada com sucesso.
Describe-description_reverted = A descrição do alias "{ $name }" foi removida com sucesso.

Describe-deco_helper = Este subcomando é usado para adicionar ou verificar a descrição de um alias.
Describe-deco_usage = Como usar: { $prefix }alias description cool_name (nova descrição)
Describe-deco_description = Este subcomando é usado para adicionar ou verificar a descrição de um alias.

# Describe Examples
Describe-cmd_ex1_prefix = ## Como adicionar uma descrição a um alias:
Describe-cmd_ex1_args = description cool_name (nova descrição)
Describe-cmd_ex1_res = Usuário, a descrição para o alias "cool_name" foi atualizada com sucesso.

## Edit
Edit-no_args_provided = Nenhum alias ou nome de comando fornecido!
Edit-edit_link = Você não pode editar links para outros aliases!
Edit-edit_success = Seu alias "{ $name }" foi editado com sucesso.
Edit-command_dont_exist = Não é possível editar o alias! O comando "{ $name }" não existe.

Edit-deco_helper = Este subcomando é usado para editar o comando e os argumentos de um alias.
Edit-deco_usage = Como usar: { $prefix }alias edit (alias) (comando) (…argumentos)
Edit-deco_description = Este subcomando é usado para editar o comando e os argumentos de um alias.

# Edit Examples
Edit-cmd_ex1_prefix = ## Como editar um alias:
Edit-cmd_ex1_args = edit cool_name count bla bla bla bla
Edit-cmd_ex1_res = Usuário, o alias "cool_name" foi editado com sucesso.

# Edit Admonitions
Edit-adm1_title = Alias vinculado.
Edit-adm1_msg = - Como aliases vinculados são apenas um ponteiro para o alias de outro usuário, não é possível editá-los.

## Link
Link-link_no_args = Você não forneceu um nome de usuário ou alias! Use: { $prefix }alias link (usuário) (nome do alias)
Link-alias_name_already_exists = Não é possível vincular um novo alias - você já possui um alias nomeado: { $name }!
Link-user_dont_has_alias = O usuário fornecido não possui o alias "{ $name }"!
Link-link_to_with_invalid_name = O alias original possui um nome inválido "{ $name }"! Por favor, forneça um nome customizado.
Link-link_custom_name_invalid = O nome customizado "{ $name }" não é válido. Por favor, forneça um nome válido.
Link-link_to_link = Você tentou criar um link a partir de um alias link (alias { $target_name } por { $user_name }), então usei o original como modelo{ $alias_name }. Quando o original mudar, o seu também mudará.
Link-link_success = Alias vinculado com sucesso{ $name }. Quando o original for alterado, o seu também será.
Link-link_name_string = , com um nome personalizado de "{ $name }"

Link-deco_helper = Este subcomando é usado para criar um link para um alias.
Link-deco_usage = Como usar: { $prefix }alias link (usuário) cool_name
Link-deco_description = Este subcomando é usado para criar um link para um alias.

# Link Examples
Link-cmd_ex1_prefix = ## Como linkar um alias:
Link-cmd_ex1_args = link (usuário) cool_name
Link-cmd_ex1_res = Usuário, alias vinculado com sucesso. Quando o original mudar, o seu também mudará.

Link-cmd_ex2_prefix = ## Também é possível criar um link e alterar o nome do alias:
Link-cmd_ex2_args = link (usuário) cool_name new_cool_name
Link-cmd_ex2_res = Usuário, alias vinculado com sucesso, com um nome personalizado "new_cool_name". Quando o original mudar, o seu também mudará.

Link-cmd_ex3_prefix = ## E se for um link para um link:
Link-cmd_ex3_args = link (usuário) cool_name
Link-cmd_ex3_res = Usuário, você tentou criar um link de um alias já vinculado (alias cool_name de <usuário>), então eu usei o original como seu modelo. Quando o original mudar, o seu também mudará.

## Remove
Remove-no_alias_name_provided = Nenhum nome de alias fornecido!
Remove-alias_removed = Seu alias "{ $name }" foi removido com sucesso.

Remove-deco_helper = Este subcomando é usado para excluir um alias.
Remove-deco_usage = Como usar: { $prefix }alias remove (alias)
Remove-deco_description = Este subcomando é usado para excluir um alias.

# Remove Examples
Remove-cmd_ex1_prefix = ## Para remover um alias:
Remove-cmd_ex1_args = remove cool_name
Remove-cmd_ex1_res = Usuário, seu alias "cool_name" foi removido com sucesso.
Remove-cmd_ex1_suffix = Ao excluir um alias, os links para este alias continuarão a existir e funcionar normalmente.

## Rename
Rename-no_name_provided = Você deve fornecer o nome alias atual e o novo!
Rename-alias_already_exists = Você já tem o alias "{ $name }"!
Rename-alias_renamed = Seu alias "{ $old }" foi renomeado com sucesso para "{ $new }".

Rename-deco_helper = Este subcomando é usado para renomear um alias.
Rename-deco_usage = Como usar: { $prefix }alias rename cool_name new_cool_name
Rename-deco_description = Este subcomando é usado para renomear um alias.

# Rename Examples
Rename-cmd_ex1_prefix = ## Para renomear um alias:
Rename-cmd_ex1_args = rename cool_name new_cool_name
Rename-cmd_ex1_res = Usuário, seu alias "cool_name" foi renomeado com sucesso para "new_cool_name".

## Extras
Extras-deco_description = Esta seção aborda o uso avançado de alias.

# Extras Examples
Extras-cmd_ex1_prefix = ## Primeiro, vamos criar um alias:
Extras-cmd_ex1_args = add advanced_usage choice 1234 123456 | count {"{0}"}
Extras-cmd_ex1_res = Usuário, seu alias "advanced_usage" foi criado com sucesso.

Extras-cmd_ex2_prefix = ## Como usar este tipo de alias:
Extras-cmd_ex2_args = { $prefix }{ $prefix }advanced_usage texto
Extras-cmd_ex2_res = Há um total de 10 caracteres. Entre eles, 0 são pontuação, 0 são letras maiúsculas, e 0 são caracteres especiais.
Extras-cmd_ex2_suffix =
    A resposta normal do comando seria algo como: `Há um total de 4 caracteres...` ou `Há um total de 6 caracteres...`, pois `choice` escolheria entre `1234` ou `123456` e então `count` retornaria o número de caracteres.
    {"\n\n"}Porém, devido à adição de `{"{0}"}` após `count`, ele irá pegar o conteúdo enviado na chamada do alias e substituir no lugar de `{"{0}"}`.
    {"\n\n"}Então o comando passado ao `count` seria algo como: `texto 1234`.

Extras-cmd_ex3_prefix = ## Um exemplo mais completo seria:
Extras-cmd_ex3_args = add advanced_usage2 choice 1234 123456 | count {"{0}"} {"{channel}"} {"{output}"} {"{user}"} {"{1+}"}
Extras-cmd_ex3_res = Usuário, seu alias "advanced_usage2" foi criado com sucesso.

# Extras Admonitions
Extras-adm1_title = O passo a passo que o bot seguirá será:
Extras-adm1_msg =
    - Substituir `{"{0}"}` por `algo_aqui`.
    - Substituir `{"{1+}"}` por `e no final`.
    - Substituir `{"{channel}"}` pelo nome do canal onde o comando foi executado, por exemplo, `gorenmu`.
    - Substituir `{"{user}"}` pelo seu nome de usuário, por exemplo, `xXNickOriginalXx`.
    - O comando completo será `choice 1234 123456 | count algo_aqui gorenmu {"{output}"} xXNickOriginalXx e no final`, que será processado pelo pipe handler.

Extras-adm2_title = O manipulador de pipe fará:
Extras-adm2_msg =
    - Processar a primeira parte: `choice 1234 123456` (por exemplo, suponha que escolha selecionou `1234`).
    - Processar a segunda parte: `count algo_aqui gorenmu {"{output}"} xXNickOriginalXx e no final`. Ao processar, `{"{output}"}` será substituído por `1234`.
    - Assim, os argumentos enviados para `count` serão `algo_aqui gorenmu 1234 xXNickOriginalXx e no final`.
    - E a resposta será: `Há um total de 50 caracteres. Entre eles, 1 é pontuação, 4 são letras maiúsculas, e 0 são caracteres especiais.`

Extras-adm3_title = Outras opções ao criar alias são:
Extras-adm3_msg =
    - `{"{output}"}`: insere a saída do comando anterior na posição `{"{output}"}`.
    - `{"{channel}"}`: substitui pelo nome do canal atual.
    - `{"{user}"}`: substitui pelo seu nome de usuário da Twitch.
    - `{"{0}"}`, `{"{1}"}`, `{"{2}"}`... você também pode usar `{"{3+}"}`, que captura todo o texto restante enviado na chamada do alias a partir da posição 3.

## Templates
# Partes da documentação
Template-part1 =
    # { $command_title }
    {"\n\n"}## Este comando pode ser usado { $rate } vezes seguidas, com um tempo de espera de { $per } por { $cooldown_type }.{"\n\n"}
Template-part2 = { $description }{"\n\n"}{ $aliases }{"\n\n"}
Template-part3 = ## A maneira de usar este comando é:{"\n\n"}

# Templates específicos
Template-alias_template =
    ## Todos os alias disponíveis para { $command_title } são:
        - { $aliases }{"\n\n"}
Template-command_template =
    ```text
        usuário: { $prefix }{ $command_name } { $args }

        bot: Usuário, { $response }
    ```{"\n"}
Template-admonition_template =
    !!! { $type } "{ $title }"

            { $message }{"\n\n"}

# Tipos de Bucket (Cooldown)
Template-bucket_type = { $type ->
    [channel] todos os usuários por canal
    [member] usuário por canal
    [user] usuário independente de canal
    [subscriber] subscriber
    [mod] moderação
    *[default] usuário
}
