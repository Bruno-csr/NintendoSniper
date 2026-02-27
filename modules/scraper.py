import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Importante: A lógica de comparar preço e enviar msg deve ficar no loop do Monitor 
# (na gui ou no main), mas aqui definimos as ferramentas.

def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    # Otimizações extras para rodar "por baixo dos panos" sem consumir muita RAM
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Gerencia o driver automaticamente
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def buscar_preco_no_site(driver, nome_jogo, url):
    try:
        driver.get(url)
        # Em vez de sleep fixo, o ideal seria WebDriverWait, 
        # mas 5-7s é seguro para a eShop que é pesada.
        time.sleep(6) 
        
        # Estratégia de XPath aprimorada
        # 1. Tenta achar o preço vinculado ao nome exato do jogo
        xpath_especifico = f"//h1[contains(text(), '{nome_jogo}')]/ancestor::section//span[contains(text(), 'R$')]"
        
        try:
            # Tenta o seletor que você criou (ajustado para h1 que é comum em títulos)
            elemento = driver.find_element(By.XPATH, xpath_especifico)
        except:
            # Fallback: Pega o primeiro preço R$ que aparecer na página (Geralmente o principal)
            try:
                elemento = driver.find_element(By.XPATH, "//span[contains(text(), 'R$')]")
            except:
                return None

        # Limpeza do texto com Regex
        texto_preco = elemento.text
        busca = re.search(r'(\d+[\d.]*,\d{2})', texto_preco)
        
        if busca:
            # Transforma "1.250,50" em 1250.50 (float)
            valor_limpo = busca.group(1).replace('.', '').replace(',', '.')
            return float(valor_limpo)
            
    except Exception as e:
        # No .exe, esse print não aparece, mas ajuda no debug durante o desenvolvimento
        print(f"Erro ao raspar {nome_jogo}: {e}")
        
    return None