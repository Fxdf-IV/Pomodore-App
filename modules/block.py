import subprocess
import os
import time
import tkinter as tk
from tkinter import filedialog
import psutil

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