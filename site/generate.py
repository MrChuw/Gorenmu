import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pathlib
from textwrap import dedent
from loguru import logger
import subprocess

from bot.bot import Gorenmu
from bot.ext.config import Config
from templates import (
    docs_path, home_index_template, language_change_menu_template, language_codes, language_commands, language_home,
    language_links, language_name, language_table, mkdocs_configs_path, mkdocs_template, nav_template, redirect_path,
    redirect_template, alt_nav_template_theme, alt_nav_template
)




def make_bot():
    configs = Config("config.toml", True)
    bot = Gorenmu(configs=configs, case_insensitive=True, retain_cache=True, log=logger)
    bot.start()
    return bot


def get_commands(bot: Gorenmu):
    command_doc_list: dict[str, dict[str, str | dict[str, str]]] = {}  # NOQA
    command_decorator_list: dict[str, dict[str, str | dict[str, str]]] = {}  # NOQA
    categories = bot.TranslationManager.languages["en"][0].categories
    for lang in bot.TranslationManager.languages:
        decorator_list = bot.TranslationManager.languages["en"][0].decorators
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


def generate_commands_files(command_list: dict, categories: list[str]):
    command_path_list: dict[str, dict[str, pathlib.Path | dict[str, pathlib.Path]]] = {}
    if not os.path.exists(docs_path):
        os.mkdir(docs_path)
    for language in command_list:
        if language not in command_path_list:
            command_path_list[language] = {}
        lang_path = docs_path / language
        commands_path = lang_path / language_commands[language_codes[language]].lower()
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
                    command_path.write_text(command_list[language][command_name][command_category_name])
                    command_path_list[language][command_name][command_category_name] = command_path
                continue
            command_path = commands_path / f"{command_name}.md"
            command_path.write_text(command_list[language][command_name])
            command_path_list[language][command_name] = command_path
    return command_path_list


def make_command_table(command_list, command_decorator_list, categories: list[str], exclude_categories: list[str]):  # NOQA
    command_table_list: dict[str, list] = {}
    markdown_tables: dict[str, str] = {}
    for lang in command_list:
        if lang not in command_table_list:
            command_table_list[lang] = []
        for command_name in command_list[lang]:
            if command_name in exclude_categories:
                continue
            if command_name in categories:
                for command_category in command_list[lang][command_name]:
                    command_table_list[lang].append(
                            {language_table[language_codes[lang]][0]: f"[{command_category}]({command_category}.md)",
                             language_table[language_codes[lang]][1]: command_decorator_list[lang][command_name][command_category].helper,
                             language_table[language_codes[lang]][2]: command_decorator_list[lang][command_name][command_category].extras,
                             }
                    )
                continue
            command_table_list[lang].append(
                    {language_table[language_codes[lang]][0]: f"[{command_name}]({command_name}.md)",
                     language_table[language_codes[lang]][1]: command_decorator_list[lang][command_name].helper,
                     language_table[language_codes[lang]][2]: command_decorator_list[lang][command_name].extras,
                     }
            )
        columns = command_table_list[lang][0].keys()
        max_lens = {coluna: max(len(str(item[coluna])) for item in command_table_list[lang] + [{coluna: coluna}]) for
                    coluna in columns}
        header = "| " + " | ".join(coluna.center(max_lens[coluna]) for coluna in columns) + " |"
        separator = "| " + " | ".join(":".ljust(max_lens[coluna] - 1, '-') + ":" for coluna in columns) + " |"
        lines = ["| " + " | ".join(str(item[coluna]).center(max_lens[coluna]) for coluna in columns) + " |" for item in
                 command_table_list[lang]]
        markdown_table = "\n".join([header, separator] + lines)

        markdown_tables[lang] = dedent("""
                # {command_lang}
    
                {table}
                """
                                       ).format(command_lang=language_commands[language_codes[lang]],
                                                table=markdown_table
                                                )

        commands_path = docs_path / lang / language_commands[language_codes[lang]].lower()
        commands_index_path = commands_path / "index.md"
        commands_index_path.write_text(markdown_tables[lang])

    return markdown_tables


def make_index(command_list, command_decorator_list, paths):  # NOQA
    for lang in command_list:
        home_path = docs_path / lang / "index.md"
        home_path.write_text(home_index_template[language_codes[lang]])


def make_mkdocs(command_list, categories: list[str]):
    for lang in command_list:
        if not os.path.exists(mkdocs_configs_path):
            os.mkdir(mkdocs_configs_path)
        lang_config = mkdocs_configs_path / lang
        if not os.path.exists(lang_config):
            os.mkdir(lang_config)
        lang_mkdocs = lang_config / "mkdocs.yml"
        nav_commands = [command for command in command_list[lang] if command not in categories]
        extras = "".join(language_change_menu_template.format(link=lang2, language_code=language_codes[lang2],
                                                              name=language_name[language_codes[lang2]]
                                                              ) for lang2 in command_list
                         )

        nav = "".join(nav_template.format(Command_title=command.title(),
                                          language_commands_lower=language_commands[language_codes[lang]].lower(),
                                          command_file=command
                                          ) for command in nav_commands
                      )
        alt_nav = ""
        for category in categories:
            alt_nav_commands = [command for command in command_list[lang][category] if type(command) is not dict]
            alt_nav += alt_nav_template_theme.format(name=category)
            alt_nav += "".join(alt_nav_template.format(Command_title=command.title(),
                                                     language_commands_lower=language_commands[language_codes[lang]].lower(),
                                                     command_file=command
                                                     ) for command in alt_nav_commands)

        mkdocs = mkdocs_template.format(link=language_links[language_codes[lang]], language_code=language_codes[lang],
                                        extras=extras, language_home=language_home[language_codes[lang]],
                                        language_commands=language_commands[language_codes[lang]],
                                        language_commands_lower=language_commands[language_codes[lang]].lower(),
                                        nav=nav, search_language_code=lang, alt_nav=alt_nav
                                        )
        lang_mkdocs.write_text(mkdocs)
        if not os.path.exists(redirect_path.parent):
            os.mkdir(redirect_path.parent)
        language_links_js = ",\n                ".join([f"'{lang}': '{link}'" for lang, link in language_links.items()])
        final_html = redirect_template % language_links_js
        redirect_path.write_text(final_html)


def build(command_list):
    for lang in command_list:
        lang_path = mkdocs_configs_path / lang / "mkdocs.yml"
        command = ['mkdocs', 'build', '-f', lang_path.resolve()]
        subprocess.run(command, check=True)
        ...
    ...


if __name__ == "__main__":
    mock_bot = make_bot()
    categories = mock_bot.TranslationManager.languages["en"][0].categories
    exclude_categories = mock_bot.TranslationManager.languages["en"][0].exclude_categories
    command_doc_list, command_decorator_list = get_commands(mock_bot)
    paths = generate_commands_files(command_doc_list, categories)
    command_index = make_command_table(command_doc_list, command_decorator_list, categories, exclude_categories)
    make_index(command_doc_list, command_decorator_list, paths)
    make_mkdocs(command_doc_list, categories)
    mock_bot.stop()
    build(command_doc_list)
