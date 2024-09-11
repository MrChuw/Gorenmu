---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - annotations
---


# Annotations

## Este comando pode ser usado 3x seguidas, com o cooldown de 10 por usuário independente do canal.

!!! tip "Annotations e Alias"

    Use alias e anotações juntos para criar comandos personalizados. Por exemplo, com +alias add bolos note check <id>, você poderá usar ++bolos para que o bot envie automaticamente o conteúdo da anotação, sem precisar usar o comando completo note check <id>.

Este comando serve para criar anotações que 

## Todos os aliases disponíveis para Annotations são:
    - note, annotation



## As formas de utilizar este comando são:

```text
    user: +annotations add Uma anotação de algo que eu quero poder checar para sempre.

    bot: Usuário, Anotação criada com sucesso. 📝 (ID: <id da anotação>)
```

```text
    user: +annotations add title:"título para facilitar lembrar o conteúdo" Uma anotação de algo que eu quero poder checar para sempre.

    bot: Usuário, Anotação criada com sucesso. 📝 (ID: <id da anotação>)
```

```text
    user: +annotations check

    bot: Usuário, Suas anotações são as de ID: <título se tiver [id]>
```

```text
    user: +annotations check <id>

    bot: Usuário, <Conteúdo da anotação.>
```

```text
    user: +annotations delete <id>

    bot: Usuário, Sua anotação de ID <id> foi deletada com sucesso. 🗑
```

!!! warning "Tamanho Máximo para o add!"

    A mensagem não pode ter mais que 450 caracteres; caso seja maior, retornará um erro.

!!! warning "Tamanho Máximo para o Titulo do add!"

    A mensagem não pode ter mais que 32 caracteres; caso seja maior, retornará um erro.

