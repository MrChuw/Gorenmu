from textwrap import dedent
from bot.translations.en.site_templates import EnSiteTemplates



class PtBrSiteTemplates(EnSiteTemplates):
    language_code: dict[str, str] = {"pt_br": "pt-BR"}
    link: str = '/pt_br/'
    home: str = 'Página Inicial'
    commands: str = 'Comandos'
    table: list[str] = ['Nome do Comando', 'Descrição', 'Extras']
    name: str = 'Português'

    home_index_template: str = dedent(f"""
    ---
    date: 2024-09-09
    ---

    # Página Inicial
    # Ainda não sei oque colocar aqui.

    [Os comandos estão aqui]({commands.lower()}/index.md)
    """).lstrip('\n')

    blog_index_template: str = dedent("""
    ---
    date: 2024-09-09
    ---

    # Changelogs
    """).lstrip('\n')

    authors_descriptions = {
            "Creator": "Criador",
            "Maintainer": "Mantenedor",
            "Contributor": "Contribuinte",
    }

    changelogs = [
            dedent("""
                    ---
                    date:
                      created: 2024-09-10T02:01:07.661-03:00
                      updated: 2024-09-10T02:01:07.661-03:00
                    authors:
                      - mrchuw
                    categories:
                      - asdf
                    slug: Changelog-1
                    title: Changelog 1
                    ---
            
                    # Changelog - 
            
                    <!-- more -->
            
                    """).lstrip('\n'),
    ]







