from bot.bot import Linkedin
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from dotenv import load_dotenv
import time, os

load_dotenv()
Email = os.getenv("LINKEDIN_EMAIL")
Password = os.getenv("LINKEDIN_PASSWORD")
if not Email or not Password:
    raise SystemExit("Defina LINKEDIN_EMAIL e LINKEDIN_PASSWORD no arquivo .env (veja .env.example).")


class Aplication():
    """
    Classe principal da aplicação
    """
    def __init__(self):
        """
        Método principal que inicializa a classe...

        Atributes:
            s(chromedriver) = recebe a classe Service que herda do chromedriver e faz a instalação 
            automática do driver toda vez que roda, sem a necessidade de instalar no path.
            options(chromedriver) = carrega a classe ChromeOptions()
            prefs = faz o dowload na raiz do diretorio.

        """
        self.s=Service(ChromeDriverManager().install())
        self.options = ChromeOptions()
        self.prefs = {"download.default_directory" : os.getcwd(),         
                      "profile.content_settings.exceptions.automatic_downloads.*.setting": 1, 
                      "safebrowsing.disable_download_protection": True,
                      # não oferecer "Salvar senha?" nem avisar de "senha vazada"
                      "credentials_enable_service": False,
                      "profile.password_manager_enabled": False,
                      "profile.password_manager_leak_detection": False }
        self.options.add_experimental_option("prefs", self.prefs)
        self.options.add_experimental_option("excludeSwitches", ['enable-logging', 'enable-automation'])
        self.execute_bot()

    def execute_bot(self):
        """
        Inicia a execuçao do Bot.
        """
        self.webdriver = Chrome(service=self.s, options=self.options)
        self.url = 'https://www.linkedin.com/login'
        self.bot = Linkedin(self.webdriver, self.url)
        self.webdriver.maximize_window()  
        self.bot.open_url()
        self.bot.login(Password, Email) 
        self.bot.go_to_connect_peoples()
        self.bot.connect_peoples()
    

            



if __name__=="__main__":
    Aplication()