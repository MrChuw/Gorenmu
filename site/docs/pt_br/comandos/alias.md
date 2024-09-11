---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - alias
---



# Alias

## Este comando pode ser usado 3x seguidas, com o cooldown de 10 por usuário independente do canal.

!!! warning "Restrições para os nomes dos aliases!"

    - Devem ter entre 2 e 30 caracteres.
    - Podem conter letras, números, traços, subtraços e uma ampla variedade de caracteres Unicode, incluindo emojis.

!!! warning "Cooldown para os aliases criados!"

    Ao criar um alias, o cooldown do alias será o cooldown dos comandos utilizados no alias. Portanto, se um comando pode ser usado 1x a cada 5 segundos e outro 3x a cada 10 segundos, o cooldown do alias será 1x a cada 5 segundos.


Este comando gerencia alias personalizados para comandos. Com ele, você pode:

 - Adicionar um novo alias para um comando existente.
 - Verificar ou listar alias existentes.
 - Copiar alias de outro usuário.
 - Descrever um alias com uma descrição personalizada.
 - Editar um alias existente, atualizando o comando associado.
 - Linkar um alias para outro alias ou criar um alias baseado em um alias existente.
 - Remover um alias.
 - Renomear um alias.

Use o comando seguido de uma ação (add, check, copy, describe, edit, link, remove, rename) para realizar a tarefa desejada.


## Como criar um alias:
 - O exemplo a seguir faz uso de [pipe](pipe.md) para passar a resposta de um comando para outro.

```text
user: +alias add nome_legal choice 1234 123456 | count

bot: Usuário, seu alias "nome_legal" foi criado com sucesso.
```

Com o exemplo acima, criamos um alias chamado `nome_legal`. O alias invocará o comando `choice` com os argumentos "1234" e "123456", e o resultado do `choice` será enviado para o comando `count`.

## Para usar o alias:

```text
user: ++nome_legal

bot: Usuário, há um total de 4 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
ou
bot: Usuário, há um total de 6 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
```

Para usar o alias, basta usar `++` e o nome do alias (+ é o prefixo padrão do bot; se o prefixo do chat for diferente, basta repetir o prefixo 2 (duas) vezes e então o nome do alias).

## Como verificar um alias:

```text
user: +alias check nome_legal 

bot: Usuário, o alias "nome_legal" tem os argumentos: choice 1234 123456 | count || Link: <url>
```

## Como copiar um alias:

```text
user: +alias copy <nome do usuário> nome_legal 

bot: Usuário, alias "nome_legal" copiado com sucesso.
```

Para copiar um alias, você só precisa do nome do usuário e do nome do alias.

## Como adicionar uma descrição a um alias:

```text
user: +alias description nome_legal <nova descrição>

bot: Usuário, a descrição do alias "nome_legal" foi atualizada com sucesso.
```

## Como editar o comando/argumentos de um alias:

```text
user: +alias edit nome_legal choice 123 1234 12345 | count

bot: Usuário, o alias "nome_legal" foi editado com sucesso.
```

No exemplo acima, a edição do comando foi nos argumentos, mudando de `1234 123456` para `123 1234 12345`. Para atualizar, você deve enviar o comando completo e mudar apenas a parte que deseja atualizar.

## Como linkar um alias:

```text
user: +alias link <usuário> nome_legal

bot: Usuário, alias vinculado com sucesso. Quando o original mudar, o seu também mudará.
```

Também é possível criar um link e mudar o nome do alias.

```text
user: +alias link <usuário> nome_legal outro_nome_legal

bot: Usuário, alias vinculado com sucesso, com um nome personalizado "outro_nome_legal". Quando o original mudar, o seu também mudará.
```

E caso seja um link para um link:

```text
user: +alias link <usuário> nome_legal

bot: Usuário, você tentou criar um link a partir de um alias já vinculado (alias nome_legal por <usuário>), então usei o original como seu modelo. Quando o original mudar, o seu também mudará.
```

## Para remover um alias:

```text
user: +alias remove nome_legal

bot: Usuário, seu alias "nome_legal" foi removido com sucesso.
```

Ao deletar um alias, os links para este alias continuarão existindo e funcionando.

## Para renomear um alias:

```text
user: +alias rename nome_legal outro_nome_legal

bot: Usuário, seu alias "nome_legal" foi renomeado com sucesso para "outro_nome_legal".
```

# Uso avançado do alias:

## Primeiro, vamos criar um alias:

```text
user: +alias add uso_avancado choice 1234 123456 | count {0}

bot: Usuário, seu alias "uso_avancado" foi criado com sucesso.
```

## A forma de utilizar este tipo de alias:

```text
user: ++uso_avancado texto

bot: Há um total de 10 caracteres. Dentre eles, 0 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
```

A resposta normal do comando seria: `Há um total de 4 caracteres. etc` ou `Há um total de 6 caracteres. etc`, pois o `choice` escolheria entre `1234` ou `123456` e então o `count` retornaria a quantidade de caracteres.

Mas, devido à adição do `{0}` depois do count, ele irá pegar o conteúdo do que foi enviado ao invocar o alias e substituirá o `{0}`.

# Outras opções ao criar o alias são:
 - `{output}`: ele colocará o output do último comando na posição de `{output}`.
 - `{channel}`: ele substituirá pelo nome do canal atual.
 - `{user}`: ele substituirá pelo seu nick na Twitch.
 - `{0}`, `{1}`, `{2}` etc., podendo também utilizar `{3+}`, que irá pegar todo texto que foi enviado ao invocar o alias e substituir.

## Um exemplo mostrando todos seria:

```text
user: +alias add uso_avancado2 choice 1234 123456 | count {0} {channel} {output} {user} {1+}

bot: Usuário, seu alias "uso_avancado2" foi criado com sucesso.
```

Vamos imaginar que você utilizou o comando desta forma: `++uso_avancado2 algo_aqui e no final`:

## O passo a passo do bot será:
 - Substituir o `{0}` por `algo_aqui`.
 - Substituir o `{1+}` por `e no final`.
 - Substituir o `{channel}` pelo canal ao qual a mensagem foi enviada, exemplo: `gorenmu`.
 - Substituir o `{user}` pelo seu nick, exemplo: `xXNickOriginalXx`.
 - Enviar o resultado `choice 1234 123456 | count algo_aqui gorenmu {output} xXNickOriginalXx e no final` para ser processado pelo pipe.

## Ao chegar no pipe, ele irá:
 - Processar a primeira parte: `choice 1234 123456` (como exemplo, vamos dizer que `choice` escolheu `1234`).
 - Processar a segunda parte: `count algo_aqui gorenmu {output} xXNickOriginalXx e no final`; ao processar a segunda parte, ele vai substituir `{output}` por `1234`.
 - Então, o comando que será enviado para o count será `count algo_aqui gorenmu 1234 xXNickOriginalXx e no final`. 
 - E a resposta será `Há um total de 50 caracteres. Dentre eles, 1 são pontuações, 4 são letras maiúsculas e 0 são caracteres especiais.`

