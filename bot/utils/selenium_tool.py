# -*- coding: utf-8 -*-
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


class Selenium:
    @staticmethod
    async def prepare_driver() -> Firefox:
        # Configurações do Firefox
        firefox_options = FirefoxOptions()
        # options.add_argument("--headless")

        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--disable-gpu")

        # Definir timeouts curtos
        firefox_options.set_preference("dom.max_script_run_time", 5)
        firefox_options.set_preference("dom.max_chrome_script_run_time", 5)

        # Desativar a detecção de rede
        firefox_options.set_preference("network.manage-offline-status", False)
        firefox_options.set_preference("network.predictor.enabled", False)
        firefox_options.set_preference("network.prefetch-next", False)
        firefox_options.set_preference("network.http.speculative-parallel-limit", 0)

        # Desativar o cache
        firefox_options.set_preference("browser.cache.disk.enable", False)
        firefox_options.set_preference("browser.cache.memory.enable", False)
        firefox_options.set_preference("browser.cache.offline.enable", False)
        firefox_options.set_preference("network.http.use-cache", False)

        # Desativar o carregamento de imagens e estilos
        firefox_options.set_preference("permissions.default.image", 2)  # 1: Carregar imagens, 2: Não carregar imagens
        firefox_options.set_preference("permissions.default.stylesheet", 2
                                       )  # 1: Carregar estilos, 2: Não carregar estilos

        # Outras opções comuns
        firefox_options.add_argument("--no-sandbox")  # Necessário para ambientes sem sandbox
        firefox_options.add_argument("--disable-dev-shm-usage")  # Desabilitar uso de /dev/shm

        geckodriver_path = "./utils/geckodriver"
        driver_service = FirefoxService(executable_path=geckodriver_path)
        driver = Firefox(options=firefox_options, service=driver_service)

        return driver
