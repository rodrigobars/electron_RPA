from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Busca de elementos
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IncorrectAmount(Exception):
    def __init__(self):
        self.mensagem = "the 'amount' parameter is incorrect"
    
    def __str__(self):
        return self.mensagem

class Bot():
    def __init__(self):
        self.op = Options()
        self.op.add_experimental_option("excludeSwitches", ["enable-logging"])

    def start(self, headless=True) -> None:
        """
        - Starts driver and open Chrome in headless mode or not
        """

        if headless: self.op.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.op)

    def get(self, url: str) -> None:
        """
        - Search for the url page
        """

        self.driver.get(url)

    def catch_element(self, xpath: str, amount="one", maxWaitTime=10) -> None:
        """
        - Find for an element if amount=='one' or elements if amount=='all' by XPATH and store on caught
        """
        try:
            if amount in ['one', 'all']:
                if amount == 'one':
                    return WebDriverWait(self.driver, maxWaitTime).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                else:
                    return WebDriverWait(self.driver, maxWaitTime).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
            else:
                raise IncorrectAmount
        except IncorrectAmount as e:
            print(e)

    def javascript(self, script):
        self.driver.execute_script(script)