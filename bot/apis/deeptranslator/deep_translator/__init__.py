"""Top-level package for Deep Translator"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"

from apis.deeptranslator.deep_translator.baidu import BaiduTranslator
from apis.deeptranslator.deep_translator.chatgpt import ChatGptTranslator
from apis.deeptranslator.deep_translator.deepl import DeeplTranslator
from apis.deeptranslator.deep_translator.detection import batch_detection, single_detection
from apis.deeptranslator.deep_translator.google import GoogleTranslator
from apis.deeptranslator.deep_translator.libre import LibreTranslator
from apis.deeptranslator.deep_translator.linguee import LingueeTranslator
from apis.deeptranslator.deep_translator.microsoft import MicrosoftTranslator
from apis.deeptranslator.deep_translator.mymemory import MyMemoryTranslator
from apis.deeptranslator.deep_translator.papago import PapagoTranslator
from apis.deeptranslator.deep_translator.pons import PonsTranslator
from apis.deeptranslator.deep_translator.qcri import QcriTranslator
from apis.deeptranslator.deep_translator.tencent import TencentTranslator
from apis.deeptranslator.deep_translator.yandex import YandexTranslator

__author__ = """Nidhal Baccouri"""
__email__ = "nidhalbacc@gmail.com"
__version__ = "1.9.1"

__all__ = [
    "GoogleTranslator",
    "PonsTranslator",
    "LingueeTranslator",
    "MyMemoryTranslator",
    "YandexTranslator",
    "MicrosoftTranslator",
    "QcriTranslator",
    "DeeplTranslator",
    "LibreTranslator",
    "PapagoTranslator",
    "ChatGptTranslator",
    "TencentTranslator",
    "BaiduTranslator",
    "single_detection",
    "batch_detection",
]
