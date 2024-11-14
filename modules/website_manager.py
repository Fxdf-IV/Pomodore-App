import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import json
import re
import subprocess
import os
import time
import psutil

# Configuração da janela de gerenciamento de sites bloqueados
class WebsiteManagerWindow:
    def __init__(self, parent, sites_list):
        # Configurações iniciais da janela
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Sites Bloqueados")
        self.window.geometry("500x400")
        self.sites_list = sites_list                   # Lista de sites recebida do PomodoroTimer
        
        # Frame principal para organização dos elementos
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de sites bloqueados
        self.sites_listbox = tk.Listbox(self.main_frame, width=50, height=15)
        self.sites_listbox.pack(pady=10)
        
        # Frame para organização dos botões
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)
        
        # Botões de controle (Adicionar, Editar e Remover)
        ttk.Button(self.button_frame, text="Adicionar", command=self.add_site).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Editar", command=self.edit_site).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Remover", command=self.remove_site).pack(side=tk.LEFT, padx=5)
        
        # Carrega a lista inicial de sites
        self.update_sites_list()
        
    # Atualiza a exibição da lista de sites
    def update_sites_list(self):
        self.sites_listbox.delete(0, tk.END)          # Limpa a lista atual
        for site in self.sites_list:                  # Adiciona cada site à lista
            self.sites_listbox.insert(tk.END, site)
    
    # Valida o formato da URL inserida
    def is_valid_url(self, url):
        pattern = r'^[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
        return re.match(pattern, url) is not None
    
    # Abre janela para adicionar novo site
    def add_site(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Adicionar Site")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="URL do site:").pack(pady=5)
        
        # Criando fonte em itálico para o placeholder
        italic_font = font.Font(family="Helvetica", size=9, slant="italic")
        
        # Criando um estilo personalizado para o Entry com placeholder
        entry = tk.Entry(dialog, width=40, font=italic_font, fg="gray")
        entry.pack(pady=5)
        
        # Texto placeholder
        placeholder = " Insira dessa forma, Ex: instagram.com "
        entry.insert(0, placeholder)
        
        # Função para limpar o placeholder quando o usuário clicar
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(font=("Helvetica", 9), fg="black")  # Remove o itálico
                
        # Função para restaurar o placeholder se o campo estiver vazio
        def on_focus_out(event):
            if not entry.get():
                entry.config(font=italic_font, fg="gray")  # Restaura o itálico
                entry.insert(0, placeholder)
        
        # Vinculando os eventos de foco
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        # Função interna para salvar o novo site
        def save():
            url = entry.get().strip()
            if url == placeholder:  # Não salvar se ainda estiver com o placeholder
                messagebox.showerror("Erro", "Por favor, insira uma URL válida!")
                return
                
            if self.is_valid_url(url):                # Valida o formato da URL
                if url not in self.sites_list:        # Verifica se o site já existe
                    self.sites_list.append(url)
                    self.update_sites_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("Aviso", "Este site já está na lista!")
            else:
                messagebox.showerror("Erro", "URL inválida!")
        
        ttk.Button(dialog, text="Salvar", command=save).pack(pady=5)
    
    # Abre janela para editar site existente
    def edit_site(self):
        selection = self.sites_listbox.curselection()
        if not selection:                             # Verifica se um site foi selecionado
            messagebox.showwarning("Aviso", "Selecione um site para editar!")
            return
            
        index = selection[0]
        old_url = self.sites_list[index]
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Editar Site")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="URL do site:").pack(pady=5)
        entry = tk.Entry(dialog, width=40)
        entry.insert(0, old_url)                      # Preenche com a URL atual
        entry.pack(pady=5)
        
        # Função interna para salvar as alterações
        def save():
            url = entry.get().strip()
            if self.is_valid_url(url):                # Valida o formato da URL
                if url != old_url and url in self.sites_list:
                    messagebox.showwarning("Aviso", "Este site já está na lista!")
                else:
                    self.sites_list[index] = url
                    self.update_sites_list()
                    dialog.destroy()
            else:
                messagebox.showerror("Erro", "URL inválida!")
        
        ttk.Button(dialog, text="Salvar", command=save).pack(pady=5)
    
    # Remove o site selecionado da lista
    def remove_site(self):
        selection = self.sites_listbox.curselection()
        if not selection:                             # Verifica se um site foi selecionado
            messagebox.showwarning("Aviso", "Selecione um site para remover!")
            return
            
        if messagebox.askyesno("Confirmar", "Deseja remover este site da lista?"):
            index = selection[0]
            del self.sites_list[index]               # Remove o site da lista
            self.update_sites_list()                 # Atualiza a exibição

# Configuração da classe WebsiteBlocker            
class WebsiteBlocker:
    def __init__(self):
        self.hosts_path = self.get_hosts_path()                     # Obtém o caminho do arquivo hosts
        self.redirect = "127.0.0.1"                                 # IP de redirecionamento
        self.browser_choice = None
        self.browser_closed = False
        self.browser_started = False

        self.ask_for_browser()

    def get_hosts_path(self):
        if os.name == 'nt':                                         # Sistema operacional Windows
            return "C:\\Windows\\System32\\drivers\\etc\\hosts"
        
        if os.name == 'posix':                                      # Sistemas Linux ou Mac
            return "/etc/hosts"

    def ask_for_browser(self):
        root = tk.Tk()
        root.withdraw()                                             # Não mostrar a janela principal do Tkinter

        print("Selecione o executável do seu navegador:")           # Abre uma janela para o usuário escolher o executável do navegador
        browser_path = filedialog.askopenfilename(title="Selecione o navegador", filetypes=[("Arquivos executáveis", "*.exe;*.app;*")])

        if browser_path:
            self.browser_choice = browser_path                      # Armazena o caminho do arquivo do navegador
            print(f"Navegador selecionado: {os.path.basename(self.browser_choice)}")
        else:
            print("Nenhum navegador foi selecionado.")

    def generate_browser_variations(self):
        if self.browser_choice:
            base_name = os.path.basename(self.browser_choice).lower()       # Obtem o nome do arquivo do navegador a partir do caminho completo
            variations = [base_name]

            variations.append(base_name.replace(".exe", ""))
            variations.append(base_name.replace(".exe", "") + " browser")
            variations.append(base_name.replace(".exe", "") + ".exe")
            
            return variations
        return []

    def close_browser(self):
        closed_processes = []                                               # Lista para armazenar processos já fechados

        for proc in psutil.process_iter(['pid', 'name']):                   # Lista os processos em execução no sistema
            for variation in self.generate_browser_variations():            # Verificar se o nome do processo contém uma das variações geradas
                if variation in proc.info['name'].lower():
                    try:
                        if proc.info['pid'] not in closed_processes:
                            print(proc.info)
                            if os.path.basename(self.browser_choice).lower() in proc.info['name'].lower():
                                print(f"Fechando o processo {proc.info['name']} (PID: {proc.info['pid']})...")
                                proc.terminate()
                                proc.wait()
                                closed_processes.append(proc.info['pid'])   # Marca o processo como fechado
                                print(f"Navegador {proc.info['name']} fechado com sucesso.")
                                self.browser_closed = True                  # Marca como fechado
                        else:
                            print(f"Processo {proc.info['name']} (PID: {proc.info['pid']}) já foi fechado.")
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                        print(f"Erro ao tentar fechar o processo: {e}")

    def start_browser(self):
            if not os.path.isfile(self.browser_choice):
                print(f"Erro: O navegador {os.path.basename(self.browser_choice)} não foi encontrado no caminho especificado.")
                return

            print(f"Iniciando o processo para o navegador: {self.browser_choice}")
            process = subprocess.Popen([self.browser_choice], shell=True)
            time.sleep(1)

            if process.poll() is None:
                self.browser_closed = False
                print(f"Navegador {os.path.basename(self.browser_choice)} reiniciado com sucesso.")\
                
            else:
                print(f"Erro ao tentar reiniciar o navegador: {os.path.basename(self.browser_choice)}.")

            if not self.browser_closed:
                print("Navegador não foi fechado corretamente. Não reiniciando.")
    
    def clear_dns_cache(self):
        if os.name == 'nt':     # Windows
            subprocess.run(["ipconfig", "/flushdns"], check=True)
            print("Cache DNS limpo com sucesso.")

        if os.name == 'posix':  # Linux ou Mac                     # O comando varia entre distribuições e versões do macOS
                                                                
            subprocess.run(["sudo", "systemd-resolve", "--flush-caches"], check=True)
            subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], check=True)
            subprocess.run(["sudo", "dscacheutil", "-flushcache"], check=True)
            print("Cache DNS limpo com sucesso")

    def generate_domain_variations(self, site):
        variations = []
    
        # Adiciona a versão padrão
        variations.append(site)

        # Adiciona a versão com "www"
        variations.append(f"www.{site}")

        # Adiciona a versão para dispositivos móveis, se possível
        variations.append(f"m.{site}")
    
        # Adiciona versões com e sem "http" ou "https"
        variations.append(f"http://{site}")
        variations.append(f"https://{site}")
    
        return variations
    
    def block_websites(self, sites):     
        with open(self.hosts_path, 'r') as file:
            content = file.readlines()

        for site in sites:                                             # Para cada site fornecido pelo usuário
            variations = self.generate_domain_variations(site)         # Gera as variações possíveis do site

            with open(self.hosts_path, 'a') as file:
                for variation in variations:
                    entry = f"{self.redirect} {variation}\n"           # Gera a linha a ser adicionada ao arquivo

                    if entry not in content:                           # Se a variação ainda não está no arquivo hosts
                        file.write(entry)                              # Adiciona a variação ao arquivo
                        print(f"Site {variation} bloqueado com sucesso.")
                    else:
                        print(f"Site {variation} já está bloqueado.")
        
    def unblock_websites(self, sites):
        with open(self.hosts_path, 'r') as file:
            content = file.readlines()

        with open(self.hosts_path, 'w') as file:
            for line in content:

                if not any(variation in line for site in sites for variation in self.generate_domain_variations(site)):
                    file.write(line)
                else:
                    print(f"Site desbloqueado: {line.strip()}")

        self.clear_dns_cache()
        print(f"Caminho do navegador: {self.browser_choice}")