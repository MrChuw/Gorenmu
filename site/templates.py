import pathlib
from textwrap import dedent

mkdocs_configs_path: pathlib.Path = pathlib.Path("./site/config")

redirect_path: pathlib.Path = pathlib.Path("./site/generated/index.html")

docs_path: pathlib.Path = pathlib.Path("./site/docs")


# TODO: change the site_url when choosing where to host
mkdocs_template: str = dedent("""
site_name: Gorenmu {language_commands}
site_url: http://localhost:3400{link}
docs_dir: '../../docs{link}'
site_dir: '../../generated{link}'
repo_url: https://github.com/MrChuw/Gorenmu/

theme:
  name: material  
  favicon: assets/images/favicon.png
  icon:
    logo: logo
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
  palette:
    scheme: slate
    primary: bot
    accent:  bot


plugins:
  - search:
      lang: {search_language_code}
  # - privacy
  - minify:
      minify_html: true
  - blog:
      post_excerpt_separator: <!-- more -->
  - rss:
      # match_path: blog/posts/.*
      use_git: false
      date_from_meta:
        as_creation: date.created
      categories:
        - categories
        - tags

extra:
  alternate:
{extras}

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences

nav:
  - {language_home}: index.md
  - Changelog: blog/index.md
  - {language_commands}:
      - {language_commands_lower}/index.md
{nav}
{alt_nav}

""").lstrip('\n')

metadata_template = dedent("""---
date:
  created: {created}
  updated: {updated}
categories:
{categories}
---\n\n
""").lstrip('\n')

authors_template = """
  {reference}:
    name: {name}
    description: {description}
    avatar: {avatar}\n
""".lstrip('\n')

language_change_menu_template: str = ("""
    - name: {name}
      link: /{link}/
      lang: {language_code}\n
""").lstrip('\n')

nav_template: str = "      - {Command_title}: {language_commands_lower}/{command_file}.md\n"

alt_nav_template_theme: str = "      - {name}:\n"
alt_nav_template: str = "        - {Command_title}: {language_commands_lower}/{command_file}.md\n"

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
