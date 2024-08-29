from textwrap import dedent


class En:
        template: str = dedent("""
        # {command_title}
        
        ## This command can be used {rate}x times in succession, with a cooldown of {per} per {cooldown_type}.
        
        {description}
        
        ## All the alias available for AFK are:
            - {aliases}
        
        ## The ways to use this command are:

        ```text
        user: {prefix}{command_name}
        
        bot: User, 
        ```
        !!! warning "Maximum length!"
        
            The message could not be longer than 450 characters, if it is longer, an error will be returned.
        """) # NOQA


class PtBr:
        template = dedent("""
        # {command_title}
        
        # Este comando pode ser usado {rate}x seguidas, com o cooldown de {per} por {cooldown_type}.
        
        {description}
        
        ## Todos os aliases disponíveis para {command_name} são:
            - {aliases}
        
        ## As formas de utilizar este comando são:

        ```text
        user: {prefix}{command_name}
        
        bot: Usuário, 
        ```
        !!! warning "Tamanho Máximo!"
        
            A mensagem não pode ter mais que 450 caracteres; caso seja maior, retornará um erro.
        """) # NOQA














