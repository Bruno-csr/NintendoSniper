import requests
from database.db_manager import carregar_config

def enviar_msg(texto):
    """
    Busca as credenciais no banco de dados e envia uma mensagem para o Telegram.
    Retorna (True, mensagem) em caso de sucesso ou (False, erro) em caso de falha.
    """
    token, chat_id = carregar_config()
    
    if not token or not chat_id:
        return False, "Configurações do Telegram ausentes. Configure na aba Ajustes."
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": texto,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            return True, "Mensagem enviada com sucesso!"
        else:
            dados_erro = response.json()
            descricao = dados_erro.get("description", "Erro desconhecido")
            return False, f"Erro na API: {descricao}"

    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão: {e}"