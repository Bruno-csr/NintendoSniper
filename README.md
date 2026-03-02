# 🎮 Nintendo Sniper v4.0

O **Nintendo Sniper** é uma aplicação automatizada de monitoramento de preços para a eShop da Nintendo brasileira. O projeto utiliza web scraping em tempo real para capturar valores, armazena o histórico em um banco de dados local (SQLite) e envia alertas instantâneos via Telegram sempre que um jogo atinge o preço alvo ou bate um recorde histórico de desconto.

## 📝 Por que este projeto existe?

Recentemente adquiri um **Nintendo Switch** e, como qualquer novo proprietário do console sabe, os preços dos jogos (especialmente os exclusivos da Nintendo) podem ser bastante elevados no Brasil. Diferente de outras plataformas, as promoções na eShop podem surgir sem aviso prévio e durar pouco tempo, o que torna o acompanhamento manual exaustivo e ineficiente.

Criei este software para automatizar a minha "Lista de Desejos". Em vez de abrir o site da Nintendo todos os dias para conferir dezenas de títulos, deixo o **Nintendo Sniper** rodando. Ele faz o trabalho pesado de verificar cada link, garantindo que eu nunca perca uma oportunidade de economizar.

Mais do que uma simples ferramenta de economia, este projeto foi uma excelente oportunidade para aplicar conceitos de **Arquitetura de Software Modular**, **Web Scraping** com Selenium, **Gerenciamento de Bancos de Dados Relacionais** com SQLite e **Segurança de Credenciais** usando variáveis de ambiente (.env).

---

## 🚀 O que o código faz?

* **Interface Gráfica (GUI):** Gerenciamento simples de jogos através de uma tela moderna construída com `CustomTkinter`.
* **Web Scraping Inteligente:** Localiza o preço do jogo principal ignorando conteúdos extras (DLCs) através de seletores XPath dinâmicos.
* **Banco de Dados SQLite:** Armazena sua lista de jogos, o histórico de todas as consultas e os recordes de menor preço já registrados.
* **Sistema de Recordes:** Notifica se o preço atual é o menor valor já visto pelo bot desde o início do monitoramento (Menor Preço Histórico).
* **Alertas via Telegram:** Integração com bot para notificações em tempo real diretamente no seu celular.
* **Monitoramento Automatizado**: Usa Selenium para verificar preços na eShop.
---

## 📚 Bibliotecas Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

* **CustomTkinter:** Interface visual moderna com suporte a Dark Mode.
* **Selenium:** Automação de navegador para extração de dados de páginas dinâmicas.
* **Webdriver-Manager:** Gerenciamento automático do driver do Chrome.
* **Requests:** Comunicação com a API do Telegram.
* **Python-Dotenv:** Proteção de chaves de API e tokens.
* **SQLite3:** Armazenamento local de dados (nativo do Python).

---

## ⚙️ Instalação Usando o GIT (Passo a Passo)

### 1. Pré-requisitos
* Python 3.10 ou superior instalado.
* Google Chrome instalado.
* Conda (opcional, mas recomendado).

### 2. Clonando o Repositório
```bash
git clone [https://github.com/seu-usuario/nintendo-sniper.git](https://github.com/seu-usuario/nintendo-sniper.git)
cd nintendo-sniper
```

3. Configurando o Ambiente
Via Conda (Recomendado):

```Bash
conda env create -f environment.yml
conda activate nintendo-sniper
```

Via Pip:

```Bash
pip install -r requirements.txt
```

4. Configuração de Credenciais
Renomeie o arquivo .env.example para .env.

Abra o arquivo .env e insira seu TELEGRAM_TOKEN e TELEGRAM_CHAT_ID.

5. Executando a Aplicação
```Bash
python main.py
```

### 🚀 Instalação (Executável)

1. Baixe o arquivo `NintendoSniper.zip` na aba [Releases](link-da-sua-release).
2. Extraia o conteúdo para uma pasta.
3. Abra o `NintendoSniper.exe`.
4. Na aba **Configurações do Bot**, insira seu Token do Telegram e Chat ID.
5. Adicione seus jogos favoritos e inicie o monitoramento!

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Interface Gráfica)
- [Selenium](https://www.selenium.dev/) (Web Scraping)
- [SQLite](https://www.sqlite.org/) (Armazenamento de Dados)
- [Requests](https://requests.readthedocs.io/) (Integração Telegram)


### 🛠 Como usar
Adicionar Jogos: Insira o nome exato do jogo (como aparece no título do site da Nintendo), a URL da loja e o preço máximo que deseja pagar.
Testar Conexão: Clique no botão "Testar Bot" para garantir que as notificações do Telegram estão chegando.
Monitorar: Clique em "Iniciar Monitor". A aplicação ficará verificando os preços em segundo plano (Headless) a cada 30 minutos.
Acompanhar: A tabela principal mostrará a última vez que o preço foi checado e qual era o valor no momento.

## 👤 Autor

Desenvolvido por **Bruno César de Almeida** - [LinkedIn](https://www.linkedin.com/in/bruno-cesar-de-almeida/)
