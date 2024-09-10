---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - count
---


# Count

# Este comando pode ser usado 3x seguidas, com o cooldown de 10 por usuário independente do canal.

Este comando pode contar o número de caracteres, letras maiúsculas, pontuações e caracteres especiais em um texto ou no conteúdo de uma URL. Se você fornecer um link e a tag `type:url`, o comando acessa o conteúdo da página e faz a contagem com base no que foi encontrado. E ele guardara o conteúdo da página em cache pôr 30 minutos (trinta minutos).


## As formas de utilizar este comando são:

```text
    user: +count  algum texto legal! com alguns 😄 personagens, espaciais!

    bot: Usuário, Há um total de 55 caracteres. Dentre eles, 3 são pontuações, 0 são letras maiúsculas e 1 são caracteres especiais.
```

```text
    user: +count https://example.com/

    bot: Usuário, Há um total de 20 caracteres. Dentre eles, 5 são pontuações, 0 são letras maiúsculas e 0 são caracteres especiais.
```

```text
    user: +count type:url https://example.com/ 

    bot: Usuário, Há um total de 1257 caracteres. Dentre eles, 188 são pontuações, 21 são letras maiúsculas e 0 são caracteres especiais.
```

```text
    user: +count type:url  https://example.com/ https://example.org/

    bot: Usuário, Há um total de 2514 caracteres. Dentre eles, 376 são pontuações, 42 são letras maiúsculas e 0 são caracteres especiais.
```

