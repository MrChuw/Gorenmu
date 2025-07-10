# -*- coding: utf-8 -*-
import os
import re
from enum import Enum
from itertools import product
from typing import Any, Dict, List

import toml
from dotenv import load_dotenv
from yarl import URL

from bot.exceptions import MissingOAuthTokenError

# nltk.download("wordnet")
load_dotenv()


def expand_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    def expand_value(val: Any) -> Any:
        if isinstance(val, str):
            return re.sub(r"\$\{([^}]+)}", lambda m: os.getenv(m.group(1), m.group(0)), val)
        elif isinstance(val, dict):
            return {k: expand_value(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [expand_value(i) for i in val]
        return val

    return {k: expand_value(v) for k, v in config.items()}


def load_config(config_path: str) -> Dict[str, dict]:
    with open(config_path, "r") as f:
        config = toml.load(f)
    config = expand_env_vars(config)
    return config


def prefix_generator(prefixes: str) -> List[str]:
    if len(prefixes) == 1:
        return [prefixes]

    comb = ["".join(p) for p in product(prefixes, repeat=2)]
    return comb + list(prefixes)


class DatabaseType(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    MARIA_DB = "mariadb"
    POSTGRESQL = "postgresql"
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
        self.test: bool = data.get("test", False)


class BotConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.bot_id: int = data.get("bot_id", 0000000)
        self.color: str = data.get("color", "#000000")
        self.dev_userid: str = data.get("dev_userid", "Exemple")
        self.dev_name: str = data.get("dev_name", "Exemple")
        self.dev_display_name: str = data.get("dev_display_name", "Exemple")
        self.prefix: List[str] = [data.get("default_prefix", "+")]
        if allowed_prefix := data.get("allowed_prefix_list"):
            self.prefix = prefix_generator(f"{self.prefix}{allowed_prefix}")
        self.allowed_prefix_size: int = data.get("allowed_prefix_size", 1)
        self.site_url: str = data.get("site_url", "https://exemple.org")


class ApisConfig:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.color_site_url: URL = URL(data.get("color_site_url", "https://color.exemple.org"))
        self.site_api_key: str = data.get("site_api_key", "api_exemple")
        self.shlink_url: URL = URL(data.get("shlink_url", "https://shlink.exemple.org/rest/v3/short-urls"))
        self.shlink_key: str = data.get("shlink_key", "api_exemple")
        self.access_token: str = data.get("access_token", "api_exemple")
        if not data.get("access_oauth_token"):
            raise MissingOAuthTokenError(
                "Missing access oauth token to generate oauth token go to: https://twitchtokengenerator.com/"
            )
        self.access_oauth_token: str = data.get("access_oauth_token", "api_exemple")
        self.refresh_token: str = data.get("refresh_token", "api_exemple")
        self.client_id: str = data.get("client_id", "api_exemple")
        self.api_client_secret: str = data.get("api_client_secret", "api_exemple")
        self.api_client_id: str = data.get("api_client_id", "api_exemple")
        self.image_carousel: URL = URL(data.get("image_carousel", "https://uploadthing.com"))
        self.image_carousel_api_key: str = data.get("image_carousel_api_key", "api_exemple")
        self.file_upload_api_key: URL = URL(data.get("file_upload_api_key", "https://upload.exemple.org"))
        self.pastebin_url: URL = URL(data.get("pastebin_url", "https://bit.exemple.org"))
        self.enable_site_endpoints: bool = data.get("enable_site_endpoints", False)


class DatabaseConfig:
    def __init__(self, data: Dict[str, dict], mock: bool) -> None:
        db_type = data.get("type", "sqlite")

        try:
            self.type: DatabaseType = DatabaseType(db_type)
        except ValueError:
            print(f"Unknown database type: {db_type}, defaulting to sqlite")
            self.type = DatabaseType.SQLITE

        self.login = data.get("login", "root")
        self.password = data.get("password", "root")
        self.host = data.get("host", "localhost")
        self.port = data.get("port", 3306)
        self.name = data.get("name", "gorenmu")

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        sqlite_file = os.path.join(base_dir, "db.sqlite3")

        if self.type == DatabaseType.SQLITE:
            self.database_uri = f"sqlite://{sqlite_file}"
        elif self.type in [DatabaseType.MARIA_DB, DatabaseType.MYSQL]:
            self.database_uri = f"mysql://{self.login}:{self.password}@{self.host}:{self.port}/{self.name}"
        elif self.type == DatabaseType.POSTGRESQL:
            self.database_uri = f"asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.name}"
        else:
            self.database_uri = f"sqlite://{sqlite_file}"

        if self.type == DatabaseType.MEMORY or mock:
            self.database_uri = "sqlite://:memory:"

        self.DB_CONFIG = {
            "connections": {"default": self.database_uri},
            "apps": {"models": {"models": ["bot.models"], "default_connection": "default"}},
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
        self.ApisConfig = ApisConfig(config["apis"])
        self.CacheConfig = CacheConfig(config["cache"])
        self.DevelopmentConfig = DevelopmentConfig(config["development"])
        self.mock = mock
        self.default_lang = "en"
