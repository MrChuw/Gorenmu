# -*- coding: utf-8 -*-
import os
import sys
from typing import Optional, Union
from somali.data.variaveis import *

class Config:
    version: str = "0.1.0"
    log_level: str = "INFO"
    access_token: str = ""
    client_secret: Optional[str] = "CLIENT_SECRET"
    prefix: Optional[str] = "",
    owner: Optional[str] = ''
    site_url: Optional[str] = "BOT_SITE_URL"
    ai_url: Optional[str] = "BOT_AI_URL"
    ai_key: Optional[str] = "BOT_AI_KEY"
    bugs_webhook_url: Optional[str] = "DISCORD_WEBHOOK_BUGS"
    suggestions_webhook_url: Optional[str] = "DISCORD_WEBHOOK_SUGGESTIONS"
    host: Optional[str] = "0.0.0.0"
    port: Optional[str] = "5001"
    color_bot: str = "COLOR_BOT", 0x9147FF
    color_green: str = "COLOR_BOT", 0x23C552
    color_red: str = "COLOR_BOT", 0xF84F31


class ApiConfig:
    analytics_url: Optional[str] = "https://tracker.dashbot.io/track"
    analytics_key: Optional[str] = ""
    bugsnag_key: Optional[str] = "API_BUGSNAG_KEY"
    color_url: Optional[str] = "https://www.thecolorapi.com"
    crypto_url: Optional[str] = "https://rest.coinapi.io/v1/exchangerate"
    crypto_key: Optional[str] = ""
    currency_url: Optional[str] = "https://v6.exchangerate-api.com/v6"
    currency_key: Optional[str] = ""
    dicio_url: Optional[str] = "API_DICIO_URL", "http://www.dicio.com.br"
    math_url: Optional[str] = "https://api.mathjs.org/v4"
    tmdb_url: Optional[str] = "https://api.themoviedb.org/3"
    tmdb_key: Optional[str] = "API_TMDB_KEY"
    translate_url: Optional[str] = "https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute"
    twitch_url: Optional[str] = "https://decapi.me/twitch"
    weather_key: Optional[str] = "API_WEATHER_KEY"
    database_url: str = "DATABASE_URL"
    redis_url: Optional[str] = ""


class ProdConfig(Config, ApiConfig):
    mode: str = "prod"
    database_url: str = os.environ.get("DATABASE_URL")
    redis_url: Optional[str] = os.environ.get("REDIS_URL")


class LocalConfig(Config, ApiConfig):
    mode: str = "local"
    if os.environ.get("DATABASE_URL"):
        database_url: str = os.environ["DATABASE_URL"]
    else:
        database_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        database_file: str = os.path.join(database_dir, "db.sqlite3")
        database_url: str = f"sqlite:///{database_file}"
    redis_url: Optional[str] = os.environ.get("REDIS_URL")


class TestConfig(Config, ApiConfig):
    mode: str = "test"
    database_url: str = "sqlite://:memory:"
    redis_url: None = None
    bugsnag_key: None = None


config_options: dict = {"prod": ProdConfig, "local": LocalConfig, "test": TestConfig}
config_mode: str = os.environ.get("CONFIG_MODE", "local")

try:
    config: Union[ProdConfig, LocalConfig, TestConfig] = config_options[config_mode]
except KeyError:
    sys.exit(f"[CRITICAL] Invalid <CONFIG_MODE>. Expected 'local', 'test' or 'prod', not '{config_mode}'.")
else:
    print(f"[INFO] Running with <CONFIG_MODE>='{config.mode}'")
