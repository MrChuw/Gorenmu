---
date:
  created: 2024-09-09
  updated: 2024-09-09
categories:
  - pipe
---



# Pipe

# Isto não é realmente um comando.

!!! warning "Cooldown!"

    O cooldown do pipe será igual ao cooldown dos comandos utilizados.

O Pipe é representado pelo caractere "|" (barra vertical), que serve para encaminhar a saída de um comando para outro.

## Como usar pipe:

```text
user: +exemplo_de_comando_1 <opções do comando> | exemplo_de_comando_2 
ou 
user: +exemplo_de_comando_1 <opções do comando> | exemplo_de_comando_2 <opções do comando 2> {output} <resto das opções do comando 2>
```

## O passo a passo do bot será:
 - Executar o `exemplo_de_comando_1` com `<opções do comando>` caso tenha alguma.
 - Em seguida, ele executará o `exemplo_de_comando_2` com a resposta do comando `exemplo_de_comando_1` adicionada como argumento.
   - Se você utilizar `{output}`, ele colocará a resposta de `exemplo_de_comando_1` na posição especificada.

