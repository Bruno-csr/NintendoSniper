import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
import time
from datetime import datetime

# Importações dos nossos módulos
from utils import resource_path
from database.db_manager import init_db, carregar_config, salvar_config, get_db_connection
from modules.scraper import configurar_driver, buscar_preco_no_site
from modules.bot_telegram import enviar_msg

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("Nintendo Sniper v4.0")
        self.geometry("1000x700")
        
        try:
            self.iconbitmap(resource_path("gui/assets/icon.ico"))
        except:
            pass

        # Variáveis de Controle
        self.is_monitoring = False
        self.monitor_thread = None

        # Layout de Abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_monitor = self.tabview.add("Monitoramento")
        self.tab_config = self.tabview.add("Configurações do Bot")

        self.setup_aba_monitor()
        self.setup_aba_config()

    # --- ABA DE CONFIGURAÇÃO ---
    def setup_aba_config(self):
        token_atual, chat_atual = carregar_config()

        ctk.CTkLabel(self.tab_config, text="Configurações do Telegram", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.ent_token = ctk.CTkEntry(self.tab_config, placeholder_text="Bot Token", width=500)
        self.ent_token.pack(pady=10)
        if token_atual: self.ent_token.insert(0, token_atual)

        self.ent_chat_id = ctk.CTkEntry(self.tab_config, placeholder_text="Chat ID", width=500)
        self.ent_chat_id.pack(pady=10)
        if chat_atual: self.ent_chat_id.insert(0, chat_atual)

        btn_save = ctk.CTkButton(self.tab_config, text="Salvar Configurações", command=self.acao_salvar_config)
        btn_save.pack(pady=10)

        btn_test = ctk.CTkButton(self.tab_config, text="Testar Conexão", fg_color="green", command=self.acao_testar_bot)
        btn_test.pack(pady=10)

    def acao_salvar_config(self):
        salvar_config(self.ent_token.get(), self.ent_chat_id.get())
        messagebox.showinfo("Sucesso", "Configurações salvas!")

    def acao_testar_bot(self):
        sucesso, msg = enviar_msg("🔔 <b>Nintendo Sniper:</b> Conexão estabelecida com sucesso!")
        if sucesso: messagebox.showinfo("Teste OK", msg)
        else: messagebox.showerror("Erro", msg)

    # --- ABA DE MONITORAMENTO (INTERFACE) ---
    def setup_aba_monitor(self):
        # Frame de Entrada
        frame_add = ctk.CTkFrame(self.tab_monitor)
        frame_add.pack(fill="x", padx=10, pady=10)

        self.ent_nome = ctk.CTkEntry(frame_add, placeholder_text="Nome do Jogo", width=200)
        self.ent_nome.pack(side="left", padx=5, pady=5)

        self.ent_url = ctk.CTkEntry(frame_add, placeholder_text="URL da eShop", width=300)
        self.ent_url.pack(side="left", padx=5, pady=5)

        self.ent_alvo = ctk.CTkEntry(frame_add, placeholder_text="Preço Alvo (Ex: 50.00)", width=150)
        self.ent_alvo.pack(side="left", padx=5, pady=5)

        btn_add = ctk.CTkButton(frame_add, text="Adicionar", width=100, command=self.adicionar_jogo)
        btn_add.pack(side="left", padx=5)

        # Guardar o ID do jogo que está sendo editado
        self.editando_id = None 

        # Botão Inteligente (Adicionar/Salvar Alteração)
        self.btn_add = ctk.CTkButton(frame_add, text="Adicionar", width=100, command=self.processar_jogo)
        self.btn_add.pack(side="left", padx=5)

        # Botão para Limpar Seleção (Cancelar Edição)
        self.btn_limpar = ctk.CTkButton(frame_add, text="Limpar", width=60, fg_color="gray", command=self.limpar_campos)
        self.btn_limpar.pack(side="left", padx=5)
        
        # --- Tabela (Treeview) ---
        self.tree = ttk.Treeview(self.tab_monitor, columns=("ID", "Jogo", "Preço Atual", "Alvo"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Jogo", text="Jogo")
        self.tree.heading("Preço Atual", text="Último Preço")
        self.tree.heading("Alvo", text="Preço Alvo")
        self.tree.column("ID", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree.bind("<Double-1>", self.carregar_para_edicao)

        # --- Botões de Controle Inferiores ---
        frame_botoes = ctk.CTkFrame(self.tab_monitor, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=10, pady=10)

        self.btn_toggle = ctk.CTkButton(frame_botoes, text="Iniciar Monitoramento", fg_color="green", command=self.toggle_monitor)
        self.btn_toggle.pack(side="left", padx=5)

        # NOVO: Botão Atualizar Tabela
        self.btn_refresh = ctk.CTkButton(frame_botoes, text="🔄 Atualizar Tabela", width=120, fg_color="#3d3d3d", command=self.atualizar_tabela)
        self.btn_refresh.pack(side="left", padx=5)

        self.btn_remover = ctk.CTkButton(frame_botoes, text="Remover Selecionado", fg_color="#A83232", command=self.remover_jogo)
        self.btn_remover.pack(side="right", padx=5)

        self.atualizar_tabela()

    # --- LÓGICA DE MONITORAMENTO (O CORAÇÃO DO PROGRAMA) ---
    def toggle_monitor(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.btn_toggle.configure(text="Parar Monitoramento", fg_color="red")
            self.monitor_thread = threading.Thread(target=self.loop_principal, daemon=True)
            self.monitor_thread.start()
        else:
            self.is_monitoring = False
            self.btn_toggle.configure(text="Iniciar Monitoramento", fg_color="blue")

    def loop_principal(self):
        """Loop que roda em segundo plano para não travar a GUI"""
        while self.is_monitoring:
            driver = configurar_driver()
            conn = get_db_connection()
            cursor = conn.cursor()
            
            jogos = cursor.execute("SELECT id, nome, url, alvo FROM jogos").fetchall()
            
            for j_id, nome, url, alvo in jogos:
                if not self.is_monitoring: break
                
                preco_atual = buscar_preco_no_site(driver, nome, url)
                
                if preco_atual:
                    agora = datetime.now().strftime("%d/%m %H:%M")
                    
                    # 1. Registrar no histórico
                    cursor.execute("INSERT INTO historico (jogo_id, preco, data_hora) VALUES (?, ?, ?)", (j_id, preco_atual, agora))
                    
                    # 2. Lógica de Recorde (Menor preço já visto)
                    res_rec = cursor.execute("SELECT menor_preco FROM recordes WHERE jogo_id = ?", (j_id,)).fetchone()
                    if res_rec is None or preco_atual < res_rec[0]:
                        cursor.execute("INSERT OR REPLACE INTO recordes (jogo_id, menor_preco, data_registro) VALUES (?, ?, ?)", 
                                       (j_id, preco_atual, agora))
                        conn.commit()
                        if res_rec: # Só avisa se não for a primeira vez que vê o jogo
                            enviar_msg(f"🏆 <b>NOVO RECORDE HISTÓRICO!</b>\n🎮 {nome}\n📉 De: R$ {res_rec[0]:.2f}\n🔥 <b>Por: R$ {preco_atual:.2f}</b>")

                    # 3. Lógica do Alerta de Alvo (Sua solicitação)
                    if preco_atual <= alvo:
                        sucesso, retorno = enviar_msg(
                            f"🎯 <b>Alerta de Alvo!</b>\n"
                            f"🎮 Jogo: {nome}\n"
                            f"💰 Preço: R$ {preco_atual:.2f}\n"
                            f"🔗 <a href='{url}'>Ver na eShop</a>"
                        )
                        if not sucesso:
                            print(f"Erro Telegram: {retorno}")
                    
                    conn.commit()
            
            conn.close()
            driver.quit()
            self.after(0, self.atualizar_tabela)
            
            # Espera 30 minutos antes da próxima varredura
            for _ in range(1800):
                if not self.is_monitoring: break
                time.sleep(1)

    def adicionar_jogo(self):
        nome = self.ent_nome.get()
        url = self.ent_url.get()
        alvo = self.ent_alvo.get()
        if nome and url and alvo:
            conn = get_db_connection()
            conn.execute("INSERT INTO jogos (nome, url, alvo) VALUES (?, ?, ?)", (nome, url, float(alvo)))
            conn.commit()
            conn.close()
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Jogo adicionado!")

    def atualizar_tabela(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        conn = get_db_connection()
        jogos = conn.execute("SELECT id, nome, alvo FROM jogos").fetchall()
        for j in jogos:
            ultimo = conn.execute("SELECT preco FROM historico WHERE jogo_id = ? ORDER BY id DESC LIMIT 1", (j[0],)).fetchone()
            p_atual = f"R$ {ultimo[0]:.2f}" if ultimo else "Aguardando..."
            self.tree.insert("", "end", values=(j[0], j[1], p_atual, f"R$ {j[2]:.2f}", "Ativo"))
        conn.close()

    def carregar_para_edicao(self, event):
        """Carrega os dados da linha selecionada para os campos de entrada"""
        selecao = self.tree.selection()
        if not selecao:
            return

        item = self.tree.item(selecao[0])
        valores = item['values'] # [ID, Nome, Preço Atual, Alvo, Status]

        # Preenche os campos de entrada
        self.editando_id = valores[0]
        self.ent_nome.delete(0, "end")
        self.ent_nome.insert(0, valores[1])
        
        # Para a URL, precisamos buscar no banco, pois ela não está na tabela
        conn = get_db_connection()
        url = conn.execute("SELECT url FROM jogos WHERE id = ?", (self.editando_id,)).fetchone()[0]
        conn.close()
        
        self.ent_url.delete(0, "end")
        self.ent_url.insert(0, url)

        # Limpa o 'R$' do alvo antes de inserir no entry
        alvo_limpo = str(valores[3]).replace("R$ ", "").replace(",", ".")
        self.ent_alvo.delete(0, "end")
        self.ent_alvo.insert(0, alvo_limpo)

        # Muda a cara do botão
        self.btn_add.configure(text="Salvar Edição", fg_color="orange")

    def limpar_campos(self):
        self.editando_id = None # CRUCIAL: Volta para modo "Adição"
        self.ent_nome.delete(0, "end")
        self.ent_url.delete(0, "end")
        self.ent_alvo.delete(0, "end")
        self.btn_salvar.configure(text="Adicionar", fg_color=("#3a7ebf", "#1f538d"))

    def processar_jogo(self):
        nome = self.ent_nome.get().strip()
        url = self.ent_url.get().strip()
        alvo = self.ent_alvo.get().strip()

        if not (nome and url and alvo):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            valor_alvo = float(alvo.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Preço alvo deve ser um número (ex: 150.50)")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.editando_id:
                # MODO EDIÇÃO
                cursor.execute("""
                    UPDATE jogos 
                    SET nome = ?, url = ?, alvo = ? 
                    WHERE id = ?
                """, (nome, url, valor_alvo, self.editando_id))
                conn.commit()
                messagebox.showinfo("Sucesso", f"'{nome}' atualizado!")
            else:
                # MODO ADIÇÃO
                cursor.execute("""
                    INSERT INTO jogos (nome, url, alvo) 
                    VALUES (?, ?, ?)
                """, (nome, url, valor_alvo))
                conn.commit()
                messagebox.showinfo("Sucesso", f"'{nome}' adicionado!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))
        finally:
            conn.close()
            self.limpar_campos() # Reseta o ID e limpa entries
            self.atualizar_tabela() # Recarrega a lista visual

    def remover_jogo(self):
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um jogo para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este jogo do monitoramento?"):
            id_jogo = self.tree.item(selecao[0])['values'][0]
            conn = get_db_connection()
            conn.execute("DELETE FROM jogos WHERE id = ?", (id_jogo,))
            # Opcional: deletar histórico também para limpar o banco
            conn.execute("DELETE FROM historico WHERE jogo_id = ?", (id_jogo,))
            conn.commit()
            conn.close()
            self.atualizar_tabela()