from page_element.page_element import Page_element
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from urllib.parse import quote
import time

class Linkedin(Page_element):
    """
    Classe que herda da classe Page_element, e que traz os locators e os 
    métodos de Login(), e connect_peoples() para fazer as conexões

    Args:
        Page_element (Class): Classe abstrata
    """
    #LOCATORS
    email = (By.CSS_SELECTOR, 'input[type="email"]')
    password = (By.CSS_SELECTOR, 'input[type="password"]')
    enter = (By.CLASS_NAME, 'sign-in-form__submit-button')
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
        campo_email = self.wait30.until(lambda d: self._visivel(self.email))
        campo_email.send_keys(Email)
        campo_senha = self.wait30.until(lambda d: self._visivel(self.password))
        campo_senha.send_keys(password + Keys.ENTER)

    def _visivel(self, locator):
        """Retorna o primeiro elemento visível do locator (o LinkedIn renderiza o form duplicado)."""
        for el in self.finds(locator):
            if el.is_displayed():
                return el
        return False
    

    def go_to_connect_peoples(self, termo="Tech recruiter"):
        """
        Abre direto a busca de PESSOAS pelo termo, sem depender da caixa de busca
        (os seletores do header do LinkedIn mudam com frequência).
        """
        # Espera o login terminar (até 2 min, dá tempo de resolver captcha/verificação na mão)

        WebDriverWait(self.webdriver, 120).until(
            lambda d: "/login" not in d.current_url and "checkpoint" not in d.current_url
        )
        self.url_busca = "https://www.linkedin.com/search/results/people/?keywords=" + quote(termo)
        self.webdriver.get(self.url_busca)
    
    def _acoes(self, palavra):
        """
        Retorna os botões/links de ação cujo texto visível OU aria-label contém a palavra.
        O 'Conectar' do LinkedIn hoje costuma ser um <a> com
        aria-label="Convidar Fulano para se conectar", e não um <button>.
        """
        palavra = palavra.lower()
        achados = []
        for el in self.finds((By.CSS_SELECTOR, 'button, a')):
            try:
                texto = (el.text or "").strip().lower()
                aria = (el.get_attribute("aria-label") or "").lower()
                if texto == palavra or palavra in aria:
                    achados.append(el)
            except Exception:
                continue
        return achados

    def _enviar_convite(self):
        """Clica no botão de envio do pop-up de convite (o nome varia entre versões)."""
        # O LinkedIn renderiza esse pop-up dentro de um shadow DOM (#interop-outlet),
        # onde XPath/find_element não enxergam. Este JS procura também dentro dos shadow roots.
        js = """
        // NÃO incluir 'enviar' puro: o chat do LinkedIn tem um botão "Enviar" que seria clicado no lugar.
        const nomes = ['enviar sem nota', 'enviar agora'];
        function busca(raiz) {
            for (const b of raiz.querySelectorAll('button')) {
                if (b.disabled) continue;
                const t = (b.innerText || '').trim().toLowerCase();
                const a = (b.getAttribute('aria-label') || '').toLowerCase();
                if (nomes.includes(t) || a.includes('enviar sem nota') || a.includes('enviar agora')) return b;
            }
            for (const el of raiz.querySelectorAll('*')) {
                if (el.shadowRoot) { const r = busca(el.shadowRoot); if (r) return r; }
            }
            return null;
        }
        const btn = busca(document);
        if (btn) { btn.click(); return true; }
        return false;
        """
        if not self.wait5.until(lambda d: d.execute_script(js)):
            raise RuntimeError("botão 'Enviar sem nota' não encontrado")

    def connect_peoples(self, max_paginas=100):
        """
        Percorre as páginas da busca pela URL (&page=N) em vez de clicar em "Avançar",
        cujo seletor muda com frequência. Para quando uma página vem sem perfis.
        """
        for pagina in range(1, max_paginas + 1):
            if pagina > 1:
                self.webdriver.get(f"{self.url_busca}&page={pagina}")
            time.sleep(4)
            # rola até o fim para carregar todos os resultados da página
            self.webdriver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)
            self.webdriver.execute_script('window.scrollTo(0, 0)')

            conectar = self._acoes('conectar')
            seguir = self._acoes('seguir')
            perfis = self.finds((By.CSS_SELECTOR, 'a[href*="/in/"]'))
            if not perfis and not conectar and not seguir:
                print(f"Página {pagina} sem resultados. Fim.")
                break
            print(f"Página {pagina}: {len(conectar)} 'Conectar' e {len(seguir)} 'Seguir' encontrados")

            for btn in conectar:
                try:
                    self.webdriver.execute_script("arguments[0].click();", btn)
                    self._enviar_convite()
                    time.sleep(2)
                except Exception as e:
                    print("Falha ao conectar:", type(e).__name__, str(e).splitlines()[0] if str(e) else "")
                    # fecha o pop-up, se ficou aberto, para não travar os próximos
                    try:
                        ActionChains(self.webdriver).send_keys(Keys.ESCAPE).perform()
                    except Exception:
                        pass
                    time.sleep(1)

            for btn in seguir:
                try:
                    self.webdriver.execute_script("arguments[0].click();", btn)
                    time.sleep(3)
                except Exception as e:
                    print("Falha ao seguir:", type(e).__name__, str(e).splitlines()[0] if str(e) else "")