"""Top-level package for Deep Translator"""
"""

Check the original package, this one is modified to use aiohttp/aiohttp-client-cache.
https://pypi.org/project/deep-translator/
https://github.com/nidhaloff/deep-translator

https://pypi.org/project/aiohttp-client-cache/
https://github.com/requests-cache/aiohttp-client-cache


"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"


from .google import GoogleTranslator

__author__ = """Nidhal Baccouri"""
__email__ = "nidhalbacc@gmail.com"
__version__ = "1.9.1"

__all__ = [
    "GoogleTranslator",
]
