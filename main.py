import os
import sys
from database.db_manager import init_db
from gui.app_interface import App
from utils import resource_path  # Importado do arquivo neutro que criamos

def main():
    # 1. Configura o diretório de trabalho
    # Garante que o .db e o log fiquem na pasta onde o usuário colocou o .exe
    if getattr(sys, 'frozen', False):
        # Se for o executável, aponta para a pasta do .exe
        os.chdir(os.path.dirname(sys.executable))
    else:
        # Se for script .py, aponta para a pasta do script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 2. Inicializa o Banco de Dados
    try:
        init_db()
    except Exception as e:
        # Como é um .exe, prints podem não aparecer; uma messagebox seria o ideal aqui
        print(f"Erro fatal ao inicializar o banco de dados: {e}")
        sys.exit(1)

    # 3. Inicia a Interface Gráfica
    try:
        app = App()
        # O ícone agora é carregado dentro do __init__ da classe App 
        # usando o resource_path, então não precisamos repetir aqui.
        app.mainloop()
    except Exception as e:
        print(f"Erro inesperado na aplicação: {e}")

if __name__ == "__main__":
    main()