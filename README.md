<h1 align="center">🤖 LinkedIn Auto Connect</h1>

<p align="center">
  Bot em Python + Selenium que pesquisa profissionais no LinkedIn e envia convites de conexão automaticamente.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Selenium-4-43B02A?style=for-the-badge&logo=selenium&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"/>
  <img src="https://img.shields.io/badge/status-estudo-yellow?style=for-the-badge"/>
</p>

<p align="center">
  <a href="#-aviso">Aviso</a> •
  <a href="#-o-que-o-bot-faz">O que faz</a> •
  <a href="#-estrutura-do-projeto">Estrutura</a> •
  <a href="#-pré-requisitos">Pré-requisitos</a> •
  <a href="#-como-executar">Como executar</a> •
  <a href="#-personalização">Personalização</a> •
  <a href="#-autor">Autor</a>
</p>

---

## ⚠️ Aviso

Este projeto foi criado **apenas para fins de estudo** do Selenium WebDriver.

- Automatizar ações no LinkedIn **viola os Termos de Uso** da plataforma e pode levar à **restrição ou banimento da conta**.
- **Não use com sua conta pessoal.** Se for testar, crie uma conta exclusiva para estudos.
- O LinkedIn muda o HTML com frequência, então os seletores podem parar de funcionar a qualquer momento.

## 🚀 O que o bot faz

1. Abre o Google Chrome (o ChromeDriver é baixado automaticamente pelo `webdriver-manager`).
2. Acessa o LinkedIn e faz login com as credenciais informadas.
3. Pesquisa pelo termo configurado (padrão: `developer python`) e abre a lista de pessoas.
4. Em cada página de resultados:
   - clica em **Conectar** e confirma em **Enviar agora**;
   - clica em **Seguir** nos perfis que só permitem seguir.
5. Avança para a próxima página e repete até não haver mais páginas.

> O bot usa os textos da interface em **português** (`Conectar`, `Seguir`, `Enviar agora`, `Avançar`). Com o LinkedIn em outro idioma, ele não encontra os botões.

## 📁 Estrutura do projeto

```
Linkedin_auto_connect/
├── main.py                       # Ponto de entrada: configura o Chrome e executa o fluxo
├── senha_email.py                # Credenciais de login (e-mail e senha)
├── bot/
│   └── bot.py                    # Classe Linkedin: locators, login, busca e conexões
└── page_element/
    └── page_element.py           # Classe base (Page Object) com esperas e ações genéricas
```

O projeto segue o padrão **Page Object**: `Page_element` concentra as ações reutilizáveis (esperar, clicar, digitar) e `Linkedin` contém os seletores e o fluxo específico do site.

## 🧰 Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/) instalado
- [Git](https://git-scm.com)
- Um editor, como o [VS Code](https://code.visualstudio.com/) (opcional)

## ▶️ Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/Fabio-arao/Linkedin_auto_connect.git
cd Linkedin_auto_connect
```

**2. Crie e ative um ambiente virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install selenium webdriver-manager pandas beautifulsoup4
```

**4. Informe suas credenciais** em `senha_email.py`:

```python
password = "sua_senha"
Email = "seu_email@exemplo.com"
```

> 🔒 Não faça commit desse arquivo com dados reais. Uma alternativa é adicioná-lo ao `.gitignore` ou usar variáveis de ambiente.

**5. Execute o bot**

```bash
python main.py
```

Ou abra o projeto no VS Code e pressione **F5**.

## 🛠️ Personalização

**Mudar o perfil buscado:** altere o termo em `bot/bot.py`, no método `go_to_connect_peoples()` (linha 49):

```python
self.wait_element_and_send_keys_enter(self.loc, "developer python")
```

Troque `"developer python"` por qualquer cargo ou área, como `"data engineer"` ou `"recrutador tech"`.

**Ajustar o ritmo:** os intervalos entre cliques ficam nos `time.sleep()` de `connect_peoples()`. Intervalos maiores deixam o comportamento menos parecido com o de um robô.

## 🐞 Problemas comuns

| Problema | Possível causa |
| --- | --- |
| O bot para na tela de login | O LinkedIn pediu verificação (código por e-mail ou CAPTCHA). Conclua manualmente na janela aberta. |
| Nenhum convite é enviado | Interface do LinkedIn em outro idioma ou seletores desatualizados em `bot/bot.py`. |
| Erro de versão do ChromeDriver | Atualize o Chrome e o pacote: `pip install -U webdriver-manager selenium`. |

## 👤 Autor

**Fábio Marques Arão**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-fabiomarquesarao-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/fabiomarquesarao)
[![E-mail](https://img.shields.io/badge/E--mail-fabinhoarao@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:fabinhoarao@gmail.com)

Sugestões e feedback são bem-vindos. Abra uma issue ou entre em contato.
