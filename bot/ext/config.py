# -*- coding: utf-8 -*-
import os
import pathlib
from enum import Enum
from typing import Dict, List

import toml
from dotenv import load_dotenv

load_dotenv()


def expand_env_vars(config: dict) -> dict:
    for section, options in config.items():
        if isinstance(options, dict):
            for key, value in options.items():
                if isinstance(value, str):
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        env_var = value[2:-1]
                        config[section][key] = os.getenv(env_var, value)

                if isinstance(value, dict):
                    for key2, value2 in value.items():
                        if isinstance(value2, str):
                            while "${" in value2 and "}" in value2:
                                start_idx = value2.index("${") + 2
                                end_idx = value2.index("}")
                                env_var = value2[start_idx:end_idx]
                                env_value = os.getenv(env_var, "")
                                value2 = value2.replace(f"${{{env_var}}}", env_value)
                            config[section][key] = value2
    return config


def load_config(config_path: str) -> Dict[str, dict]:
    with open(config_path, 'r') as f:
        config = toml.load(f)
    config = expand_env_vars(config)
    return config


def prefix_generator(prefixes: str) -> List[str]:
    if len(prefixes) == 1:
        return [prefixes]
    combinacoes = []
    prefixes = [x for x in prefixes]

    def gerar_combinacoes(atual, tamanho):
        if tamanho == 0:
            combinacoes.append(atual)
            return
        for char in prefixes:
            gerar_combinacoes(atual + char, tamanho - 1)

    # Gerar combinações de 1 e 2 caracteres
    for tamanho in range(2, 3):
        gerar_combinacoes("", tamanho)

    return combinacoes + prefixes


def cog_path_generator(cogs: list, cogs_path: pathlib.Path) -> List[str]:
    for cog in cogs_path.iterdir():
        if cog.is_dir():
            for file in cog.iterdir():
                if file.is_file() and file.suffix == ".py":
                    # cogs.append(f"{cogs_path.name}/{cog.name}/{file.name}")
                    cogs.append(file)
            continue
    return cogs


class DatabaseType(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    MARIA_DB = "mariadb"
    POSTGRESQL = "postgres"
    MEMORY = "memory"


class CacheType(Enum):
    REDIS = "redis"
    VALKEY = "valkey"
    MEMORY = "memory"
    MEMCACHED = "memcached"


class LoggingType(Enum):
    CRITICAL = "critical"
    FATAL = CRITICAL
    ERROR = "error"
    WARNING = "warning"
    WARN = WARNING
    INFO = "info"
    DEBUG = "debug"
    NOTSET = "notset"


class DevelopmentConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.development: bool = data.get("development", False)


class BotConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.color: str = data.get("color", "#000000")
        self.dev_userid: str = data.get("dev_userid", "Exemple")
        self.prefix: List[str] = [data.get("default_prefix", "+")]
        allowed_prefix: str | None = data.get("allowed_prefix_list", None)
        if allowed_prefix:
            self.prefix = prefix_generator(str(self.prefix) + allowed_prefix)
        self.allowed_prefix_size: int = data.get("allowed_prefix_size", 1)
        self.site_url: str = data.get("site_url", "https://exemple.org")
        self.pastbin_url: str = data.get('pastbin_url', "https://bit.exemple.org")
        self.imagem_link_upload_thing_url: str = data.get("imagem_link_upload_thing_url", "https://uploadthing.com")
        self.file_upload_url: str = data.get("file_upload_url", "https://upload.exemple.org")
        self.imgur_permitidos: List[int] = data.get("imgur_authorized_ids", [411010313])


class ApisConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.site_api_key: str = data.get("site_api_key", "api_exemple")
        self.shlink_url: str = data.get("site", "https://shlink.exemple.com/rest/v3/short-urls")
        self.shlink_key: str = data.get("shlink_key", "api_exemple")
        self.access_token: str = data.get("access_token", "api_exemple")
        if not data.get("access_oauth_token"):
            raise Exception(
                    "Missing access oauth token to generate oauth token go to: https://twitchtokengenerator.com/"
            )
        self.access_oauth_token: str = data.get("access_oauth_token", "api_exemple")
        self.refresh_token: str = data.get("refresh_token", "api_exemple")
        self.client_id: str = data.get("client_id", "api_exemple")
        self.api_client_secret: str = data.get("api_client_secret", "api_exemple")
        self.api_client_id: str = data.get("api_client_id", "api_exemple")


class DatabaseConfig:
    def __init__(self, data: Dict[str, dict], mock: bool) -> None:
        db_type = data.get("type", "sqlite")
        try:
            self.type: DatabaseType = DatabaseType(db_type)
        except ValueError:
            print(f"Unknown database type: {db_type}, using sqlite")
            self.type: DatabaseType = DatabaseType.SQLITE
        self.login: str = data.get("login", "root")
        self.password: str = data.get("password", "root")
        self.host: str = data.get("host", "localhost")
        self.port: int = data.get("port", 3306)
        self.name: str = data.get("name", "gorenmu")

        if self.type is DatabaseType.SQLITE:
            self.database_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            self.database_file: str = os.path.join(self.database_dir, "db.sqlite3")
            self.database_uri: str = f"sqlite://{self.database_file}"
        elif self.type is (DatabaseType.MARIA_DB or DatabaseType.MYSQL):
            self.database_uri = "mysql"
        elif self.type is DatabaseType.POSTGRESQL:
            self.database_uri = "asyncpg"
        else:
            self.database_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            self.database_file: str = os.path.join(self.database_dir, "db.sqlite3")
            self.database_uri: str = f"sqlite://{self.database_file}"

        if self.type in [DatabaseType.POSTGRESQL, DatabaseType.MARIA_DB, DatabaseType.MYSQL]:
            self.database_uri = (f"{self.database_uri}://"
                                 f"{self.login}:{self.password}@"
                                 f"{self.host}:{self.port}/{self.name}")

        if self.type is DatabaseType.MEMORY or mock:
            self.database_uri: str = "sqlite://:memory:"

        self.DB_CONFIG = {"connections": {"default": self.database_uri
                                          }, "apps": {"models": {"models": ["bot.models"], "default_connection": "default",
                                                                 }
                                                      },
                          }


class LoggerConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.version: str = data.get("version", "1")
        self.disable_existing_loggers: bool = data.get("disable_existing_loggers", False)
        self.format: str = data.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.level: str = data.get("level", "INFO")
        self.enqueue: bool = data.get("enqueue", True)
        self.colorize: bool = data.get("colorize", True)

    def to_dict(self) -> Dict[str, dict | bool]:
        return {"version": self.version, "disable_existing_loggers": self.disable_existing_loggers,
                "format": self.format, "level": self.level,
                }


class CacheConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        cache_type = data.get("type", "memory")
        try:
            self.type: CacheType = CacheType(cache_type)
        except ValueError:
            print(f"Unknown cache type: {cache_type}, using memory")
            self.type: CacheType = CacheType.MEMORY
        self.host: str = data.get("host", "localhost")
        self.port: int = data.get("port", 6379)
        self.password: str = data.get("password", "root")
        self.namespace: str = data.get("namespace", "gorenmu")


class Config:
    def __init__(self, config, mock: bool = False) -> None:
        config = load_config(config)
        self.stage = config.get("stage", "dev")
        self.version = config.get("version", "1.0.0")
        self.BotConfig = BotConfig(config["bot"])
        self.DatabaseConfig = DatabaseConfig(config["database"], mock)
        self.LoggerConfig = LoggerConfig(config["logger"])
        self.ApisConfig = ApisConfig(config["apis"])
        self.CacheConfig = CacheConfig(config["cache"])
        self.DevelopmentConfig = DevelopmentConfig(config["development"])


imgur_permitidos = ["beyxo_", "mr_chuw"]
