import pathlib
from textwrap import dedent

language_codes: dict[str, str] = {
        "en": "en",
        "pt_br": "pt-BR",
}

language_links: dict[str, str] = {
        'en': '/en/',
        'pt-BR': '/pt_br/',
}

language_home: dict[str, str] = {
        'en': 'Home',
        'pt-BR': 'Página Inicial',
}

language_commands: dict[str, str] = {
        'en': 'Commands',
        'pt-BR': 'Comandos',
}

language_table: dict[str, list[str]] = {
        'en': ['Command Name', 'Description', 'Extras'],
        'pt-BR': ['Nome do Comando', 'Descrição', 'Extras'],
}

language_name: dict[str, str] = {
        'en': 'English',
        'pt-BR': 'Português',
}

home_index_template: dict[str, str] = {'en': dedent("""
                                        # Home
                                        # I still don't know what to put here.

                                        [The commands are here](commands/index.md)
                                        """),
                                       'pt-BR': dedent("""
                                        # Página Inicial
                                        # Ainda não sei oque colocar aqui.

                                        [Os comandos estão aqui](comandos/index.md)
                                        
                                        """)}

mkdocs_configs_path: pathlib.Path = pathlib.Path("./site/config")

redirect_path: pathlib.Path = pathlib.Path("./site/generated/index.html")

docs_path: pathlib.Path = pathlib.Path("./site/docs")

mkdocs_template: str = dedent("""
site_name: Gorenmu {language_commands}
site_url: http://localhost:3400/{link}
docs_dir: '../../docs/{link}'
site_dir: '../../generated/{link}'

theme:
  name: material
  custom_dir: '../../overrides/'
  language: {language_code}
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - search.suggest
    - search.highlight
    - search.share
    - navigation.instant
    - navigation.prune
    - navigation.indexes
    - toc.follow

plugins:
  - search:
      lang: {search_language_code}
  - privacy
  - offline
  - minify:
      minify_html: true
extra:
  alternate:
{extras}
repo_url: https://github.com/MrChuw/Gorenmu/

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences

nav:
  - {language_home}: index.md
  - Blog: blog/index.md
  - {language_commands}:
      - {language_commands_lower}/index.md
{nav}

"""
                              )

language_change_menu_template: str = ("""    - name: {name}
      link: /{link}/
      lang: {language_code}\n
""")

nav_template: str = "      - {Command_title}: {language_commands_lower}/{command_file}.md\n"

redirect_template: str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Redirect</title>
    <script>
        function redirectToLanguage() {
            const userLang = navigator.language || navigator.userLanguage;

            const languageLinks = {
                %s
            };

            for (const [lang, link] of Object.entries(languageLinks)) {
                if (userLang.startsWith(lang)) {
                    window.location.href = link;
                    return;
                }
            }

            // Default to English if no match is found
            window.location.href = languageLinks['en'];
        }

        window.onload = redirectToLanguage;
    </script>
</head>
<body>
    <p>Redirecting to the appropriate documentation...</p>
</body>
</html>
"""
