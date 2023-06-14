from abc import ABC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import os, zipfile, random, time, math
from datetime import datetime, date
import uuid
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class Page_element(ABC):
    """
    Classe abstrata onde contém 
    todos os elementos, métodos e funções necessários para
    iteragir com webelements.
    """ 
    def __init__(self, webdriver, url=''):
        """
        Método construtor para iniciar o webdriver

        Args:
            webdriver: webdriver que será executado
            url (str, optional): url para acesso à adm. Defaults to ''.
        """
        self.webdriver = webdriver
        self.webdriver.maximize_window
        self.url = url
        self.wait2 = WebDriverWait(self.webdriver, 2)
        self.wait5 = WebDriverWait(self.webdriver, 5)
        self.wait10 = WebDriverWait(self.webdriver, 10)
        self.wait30 = WebDriverWait(self.webdriver, 30)


    def find(self, locator):
        """
        Encontra o WebElement de acordo com seu locator

        Args:
            locator (tuple): tupla com as informações do WebElement

        Returns:
            WebElement: Elemento do DOM
        """
        return self.webdriver.find_element(*locator)
    
    def finds(self, locator):
        """
        Encontra os WebElements de acordo com seu locator

        Args:
            locator (tuple): tupla com as informações do WebElement

        Returns:
            WebElement (list): lista com os elementos encontrados.
        """
       
        return self.webdriver.find_elements(*locator)    
        
    def open_url(self):
        """
        Abre a url no navegador
        """
        self.webdriver.get(self.url)

    def wait_element_and_click(self, locator):
        """
        Aguarda a presença do elemento por 30 segundos e clica no mesmo

        Args:
            locator (tuple): tupla com as informações do WebElement
        """
        self.wait30.until(EC.presence_of_element_located(locator))
        self.find(locator).click()
    
    def wait_element_and_click_argument(self, locator):
        """
        Utiliza o execute_script método de click do Js.
        Aguarda a presença do elemento por 30 segundos e clica no mesmo
        
        Args:
            locator (tuple): tupla com as informações do WebElement
        """
        self.wait30.until(EC.presence_of_element_located(locator))
        self.webdriver.execute_script("arguments[0].click();", self.find(locator))

    def wait_element_and_send_keys(self, locator, keys):
        """
        Aguarda a presença do elemento por 30 segundos e envia à ele a infomação de Keys

        Args:
            locator (tuple): tupla com as informações do WebElement
            keys (string): informação a ser enviada
        """
        self.wait30.until(EC.presence_of_element_located(locator))
        self.find(locator).send_keys(keys)

    def wait_element_and_send_keys_enter(self, locator, keys):
        """
        Aguarda a presença do elemento por 30 segundos e envia à ele a infomação de Keys

        Args:
            locator (tuple): tupla com as informações do WebElement
            keys (string): informação a ser enviada
        """
        self.wait30.until(EC.presence_of_element_located(locator))
        self.find(locator).send_keys(keys + Keys.ENTER)
