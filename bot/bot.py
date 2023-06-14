from page_element.page_element import Page_element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class Linkedin(Page_element):
    """
    Classe que herda da classe Page_element, e que traz os locators e os 
    métodos de Login(), e connect_peoples() para fazer as conexões

    Args:
        Page_element (Class): Classe abstrata
    """
    #LOCATORS
    email = (By.NAME, 'session_key' )
    password = (By.NAME, 'session_password')
    enter = (By.CLASS_NAME, 'sign-in-form__submit-button')
    loc = (By.CSS_SELECTOR,'input[class*="search-global-typeahead__input"]')
    ampli = (By.CSS_SELECTOR, 'div[class*="search-results__cluster-bottom-banner"]')
    all_loc = (By.CSS_SELECTOR, 'ul[class*="reusable-search__entity-result-list "]')
    all_button_conect = (By.TAG_NAME, 'button') 
    button_pass = (By.CSS_SELECTOR, 'button[aria-label="Enviar agora"]')
    page = (By.CSS_SELECTOR, 'li[data-test-pagination-page-btn="100"]')
    btn2 = (By.XPATH, "//button[@aria-label='Enviar agora']")
    li_loc = (By.CLASS_NAME, "entity-result__item" )
    next_loc = (By.XPATH, "//button[@aria-label='Avançar']")

    def login(self, password, Email):
        """
        Recebe por parâmetro, username e password, 
        que atravéz do método wait_element_and_send_keys() efetua o login
        no website.

        Args:
            username (string): Usuário préviamente cadastrado na administradora
            password (string): senha préviamente cadastrada na administradora
        """
        self.wait_element_and_send_keys(self.email, Email)
        self.wait_element_and_send_keys(self.password, password)
        self.wait_element_and_click_argument(self.enter)
    

    def go_to_connect_peoples(self):
        self.wait_element_and_click(self.loc)
        self.wait_element_and_send_keys_enter(self.loc, "desenvolvedor js")
        self.webdriver.execute_script('window.scroll(0,500)')
        self.wait_element_and_click(self.ampli)
    
    def connect_peoples(self):
        #all_dt = self.bot.finds(self.bot.all_loc)
        time.sleep(2)
        while True:
            botoes = self.finds(self.all_button_conect)
            conectar = [bt for bt in botoes if bt.text == 'Conectar']
            seguir = [bt for bt in botoes if bt.text == 'Seguir']
            time.sleep(2)
            try:
                for btn in conectar:
                    time.sleep(1)
                    self.webdriver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                    env = self.webdriver.find_element(By.XPATH, "//button[@aria-label='Enviar agora']")
                    self.webdriver.execute_script("arguments[0].click();", env)
                    
                for btn in seguir:
                    time.sleep(3)
                    self.webdriver.execute_script("arguments[0].click();", btn)
            except:
                pass 

            self.webdriver.execute_script('window.scroll(0, 1500)')
            time.sleep(2)
            try:
                avan = self.webdriver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Avançar"]')
                self.webdriver.execute_script("arguments[0].click();", avan)
                #self.bot.wait_element_and_click(self.bot.next_loc)
                time.sleep(2)
            except:
                break