from __future__ import annotations
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Any, Dict, TYPE_CHECKING

import pathlib
from textwrap import dedent
from loguru import logger
import subprocess

from bot.bot import Gorenmu
from bot.ext.config import Config
from templates import (
    docs_path, language_change_menu_template, mkdocs_configs_path, mkdocs_template, nav_template, redirect_path,
    redirect_template, alt_nav_template_theme, alt_nav_template, metadata_template, authors_template)


if TYPE_CHECKING:
    from bot.translations import TranslationManager



def make_bot():
    configs = Config("config.toml", True)
    bot = Gorenmu(configs=configs, case_insensitive=True, retain_cache=True, log=logger)
    bot.start()
    return bot


def get_commands(bot: Gorenmu):
    command_doc_list: dict[str, dict[str, str | dict[str, str]]] = {}  # NOQA
    command_decorator_list: dict[str, dict[str, str | dict[str, str]]] = {}  # NOQA
    manager: TranslationManager = bot.TranslationManager
    categories = manager.languages["en"][0].categories
    for lang in manager.languages:
        decorator_list = manager.languages["en"][0].decorators
        if lang not in command_doc_list:
            command_doc_list[lang] = {}
        if lang not in command_decorator_list:
            command_decorator_list[lang] = {}
        for command_name in decorator_list:
            if command_name in bot.commands:
                docs = bot.commands[command_name].docs[lang]
                if command_name in docs and len(docs) == 1:
                    command_doc_list[lang][command_name] = docs[command_name]
                else:
                    for sub_doc in docs:
                        command_doc_list[lang][sub_doc] = docs[sub_doc]
                command = bot.commands[command_name]
                if lang in command.decorators:
                    decorator = command.decorators[lang]
                    if "usage" in dir(decorator):
                        command_decorator_list[lang][command_name] = decorator
                    else:
                        for classe in dir(decorator):
                            if classe.startswith("__") or classe.startswith("get_"):
                                continue
                            else:
                                command_decorator_list[lang][classe.lower()] = getattr(decorator, classe)
            elif command_name in categories:
                category_name = command_name
                for command_nsfw_name in decorator_list[category_name]:
                    if category_name not in command_doc_list[lang]:
                        command_doc_list[lang][category_name] = {}
                    if category_name not in command_decorator_list[lang]:
                        command_decorator_list[lang][category_name] = {}
                    docs = bot.commands[command_nsfw_name].docs[lang]

                    if command_nsfw_name in docs and len(docs) == 1:
                        command_doc_list[lang][category_name][command_nsfw_name] = docs[command_nsfw_name]
                    else:
                        for sub_doc in docs:
                            command_doc_list[lang][category_name][sub_doc] = docs[sub_doc]
                    command = bot.commands[command_nsfw_name]
                    if lang in command.decorators:
                        decorator = command.decorators[lang]
                        if "usage" in dir(decorator):
                            command_decorator_list[lang][category_name][command_nsfw_name] = decorator
                        else:
                            for classe in dir(decorator):
                                if classe.startswith("__") or classe.startswith("get_"):
                                    continue
                                else:
                                    command_decorator_list[lang][category_name][classe.lower()] = getattr(decorator,
                                                                                                          classe)

    return command_doc_list, command_decorator_list


def generate_commands_files(command_list: dict, command_decorator_list, categories: list[str], manager: TranslationManager):
    command_path_list: dict[str, dict[str, pathlib.Path | dict[str, pathlib.Path]]] = {}
    if not os.path.exists(docs_path):
        os.mkdir(docs_path)
    for language in command_list:
        if language not in command_path_list:
            command_path_list[language] = {}
        lang_path = docs_path / language
        commands_path = lang_path / manager.site[language].commands.lower()
        if not os.path.exists(lang_path):
            os.mkdir(lang_path)
        if not os.path.exists(commands_path):
            os.mkdir(commands_path)
        for command_name in command_list[language]:
            if command_name in categories:
                if command_name not in command_path_list[language]:
                    command_path_list[language][command_name] = {}
                for command_category_name in command_list[language][command_name]:
                    command_path = commands_path / f"{command_category_name}.md"
                    metadata = metadata_template.format(
                            created=command_decorator_list[language][command_name][command_category_name].created,
                            updated=command_decorator_list[language][command_name][command_category_name].updated,
                            categories=dedent(f"""  - {command_name}
                              - {command_category_name}
                            """)
                    )
                    command_path.write_text(metadata + command_list[language][command_name][command_category_name])
                    command_path_list[language][command_name][command_category_name] = command_path
                continue
            command_path = commands_path / f"{command_name}.md"
            metadata = metadata_template.format(
                created = command_decorator_list[language][command_name].created,
                updated = command_decorator_list[language][command_name].updated,
                categories=f"  - {command_name}"
            )
            command_path.write_text(metadata + command_list[language][command_name])
            command_path_list[language][command_name] = command_path
    return command_path_list


def make_command_table(command_list, command_decorator_list, categories: list[str], exclude_categories: list[str], manager: TranslationManager):  # NOQA
    command_table_list: list[dict[str, str]] = []
    for lang in command_list:
        language_table = manager.site[lang].table
        for command_name in command_list[lang]:
            if command_name in exclude_categories:
                continue
            if command_name in categories:
                command_table_list.extend(
                        {language_table[0]: f"[{command_category}]({command_category}.md)",
                         language_table[1]: command_decorator_list[lang][command_name ][command_category].helper,
                         language_table[2]: command_decorator_list[lang][command_name][command_category].extras,
                         } for command_category in command_list[lang][command_name])
                continue
            command_table_list.append(
                    {language_table[0]: f"[{command_name}]({command_name}.md)",
                     language_table[1]: command_decorator_list[lang][command_name].helper,
                     language_table[2]: command_decorator_list[lang][command_name].extras,
                     }
            )
        columns = command_table_list[0].keys()
        max_lens = {coluna: max(len(str(item[coluna])) for item in command_table_list + [{coluna: coluna}]) for
                    coluna in columns}
        header = "| " + " | ".join(coluna.center(max_lens[coluna]) for coluna in columns) + " |"
        separator = "| " + " | ".join(":".ljust(max_lens[coluna] - 1, '-') + ":" for coluna in columns) + " |"
        lines = ["| " + " | ".join(str(item[coluna]).center(max_lens[coluna]) for coluna in columns) + " |" for item in
                 command_table_list]
        markdown_table = "\n".join([header, separator] + lines)

        markdown_tables = dedent("""
                # {command_lang}
    
                {table}
                """).format(command_lang=manager.site[lang].commands,
                            table=markdown_table,
                            )

        commands_path = docs_path / lang / manager.site[lang].commands.lower()
        commands_index_path = commands_path / "index.md"
        commands_index_path.write_text(markdown_tables)
        command_table_list = []


def make_index(manager: TranslationManager):  # NOQA
    for lang in manager.site:
        home_path = docs_path / lang / "index.md"
        home_path.write_text(manager.site[lang].home_index_template)


def generate_authors(manager):
    return "".join(
        authors_template.format(
            reference=author['reference'],
            name=author['name'],
            description=manager.authors_descriptions.get(author.get('description_tipe', 'Maintainer')),
            avatar=author.get('avatar', ""),
        ) for author in manager.authors
    )


def generate_changelogs(manager, path: pathlib.Path):
    for index, changelog in enumerate(manager.changelogs):
        changelog_path = path / f"{index}.md"
        changelog_path.write_text(changelog)


def make_blog(manager: TranslationManager):
    for lang in manager.site:
        blog_path = docs_path / lang / "blog"
        blog_index = blog_path / "index.md"
        blog_index.write_text(manager.site[lang].blog_index_template)
        authors_path = blog_path / ".authors.yml"
        authors = generate_authors(manager.site[lang])
        authors_path.write_text("authors:\n" + authors)
        posts_path = blog_path / "posts"
        generate_changelogs(manager.site[lang], posts_path)
    ...


def make_mkdocs(command_list, categories: list[str], manager: TranslationManager):
    for lang in command_list:
        if not os.path.exists(mkdocs_configs_path):
            os.mkdir(mkdocs_configs_path)
        lang_config = mkdocs_configs_path / lang
        if not os.path.exists(lang_config):
            os.mkdir(lang_config)
        lang_mkdocs = lang_config / "mkdocs.yml"
        nav_commands = [command for command in command_list[lang] if command not in categories]
        extras = "".join(language_change_menu_template.format(link=lang2,
                                                              language_code=manager.site[lang2].language_code[lang2],
                                                              name=manager.site[lang2].name
                                                              ) for lang2 in command_list
                         )

        nav = "".join(nav_template.format(Command_title=command.title(),
                                          language_commands_lower=manager.site[lang].commands.lower(),
                                          command_file=command
                                          ) for command in nav_commands
                      )
        alt_nav = ""
        for category in categories:
            alt_nav_commands = [command for command in command_list[lang][category] if type(command) is not dict]
            alt_nav += alt_nav_template_theme.format(name=category)
            alt_nav += "".join(alt_nav_template.format(Command_title=command.title(),
                                                     language_commands_lower=manager.site[lang].commands.lower(),
                                                     command_file=command
                                                     ) for command in alt_nav_commands)

        mkdocs = mkdocs_template.format(link=manager.site[lang].link, language_code=manager.site[lang].language_code[lang],
                                        extras=extras, language_home=manager.site[lang].home,
                                        language_commands=manager.site[lang].commands,
                                        language_commands_lower=manager.site[lang].commands.lower(),
                                        nav=nav, search_language_code=lang, alt_nav=alt_nav
                                        )
        lang_mkdocs.write_text(mkdocs)
    if not os.path.exists(redirect_path.parent):
        os.mkdir(redirect_path.parent)
    language_links = {lang: manager.site[lang].language_code[lang] for lang in manager.site}
    language_links_js = ",\n                ".join([f"'{lang}': '{link}'" for lang, link in language_links.items()])
    final_html = redirect_template % language_links_js
    redirect_path.write_text(final_html)


def build(command_list):
    for lang in command_list:
        lang_path = mkdocs_configs_path / lang / "mkdocs.yml"
        command = ['mkdocs', 'build', '-f', lang_path.resolve()]
        subprocess.run(command, check=True)





if __name__ == "__main__":
    mock_bot = make_bot()
    manager = mock_bot.TranslationManager
    categories = mock_bot.TranslationManager.languages["en"][0].categories
    exclude_categories = mock_bot.TranslationManager.languages["en"][0].exclude_categories
    command_doc_list, command_decorator_list = get_commands(mock_bot)
    paths = generate_commands_files(command_doc_list, command_decorator_list, categories, manager)
    make_command_table(command_doc_list, command_decorator_list, categories, exclude_categories, manager)
    make_index(manager)
    make_blog(manager)
    make_mkdocs(command_doc_list, categories, manager)
    mock_bot.stop()
    build(command_doc_list)
