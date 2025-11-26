# !/usr/bin/env python3
import sys
from pathlib import Path


def create_file_from_template(template_path: Path, output_path: Path, command_name: str, command_title: str) -> None:
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        return

    with open(template_path, encoding="utf-8") as f:
        content = f.read()

    content = content.replace("{command_name}", command_name).replace("{command_title}", command_title)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created: {output_path}")


def create_init_file(path: Path) -> None:
    init_path = path / "__init__.py"
    if not init_path.exists():
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("# -*- coding: utf-8 -*-\n")
        print(f"Created: {init_path}")


def ensure_init_for_path(path: Path, stop_at: Path) -> None:
    parts = list(path.relative_to(stop_at).parts)
    current = stop_at
    for part in parts:
        current = current / part
        create_init_file(current)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python tools/create.py <command_name> <command_title>")
        sys.exit(1)

    command_name = sys.argv[1]
    command_title = sys.argv[2]
    root = Path(__file__).resolve().parent.parent
    tools_dir = Path(__file__).resolve().parent
    templates_dir = tools_dir / "templates"

    # Target directories
    bot_dir = root / f"bot/cogs/{command_name}/command"
    tests_dir = root / f"tests/tests/cogs/{command_name}/{command_name}"

    # Template to output mapping
    files_to_create = [
        (templates_dir / "command_template", bot_dir / f"{command_name}.py"),
        (templates_dir / "translations_template", bot_dir / "translations.py"),
        (
            templates_dir / "test_command_template",
            tests_dir / f"test_{command_name}.py",
        ),
        (templates_dir / "test_params_template", tests_dir / "test_params.py"),
    ]
    for template_path, output_path in files_to_create:
        create_file_from_template(template_path, output_path, command_name, command_title)

    ensure_init_for_path(root / f"bot/cogs/{command_name}", root / "bot")
    ensure_init_for_path(bot_dir, root / "bot")
    ensure_init_for_path(root / f"tests/tests/cogs/{command_name}", root / "tests")
    ensure_init_for_path(tests_dir, root / "tests")

    print("All files and __init__.py created successfully.")


if __name__ == "__main__":
    main()
