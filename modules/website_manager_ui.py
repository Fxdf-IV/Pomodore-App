import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import re
import os

class WebsiteManagerWindow:
    def __init__(self, parent, sites_list, website_manager):
        # Configurações iniciais da janela
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Sites Bloqueados")
        self.window.geometry("500x400")
        self.sites_list = sites_list                   # Lista de sites recebida do PomodoroTimer
        self.website_manager = website_manager         # Usando a instância existente do WebsiteBlocker
        
        # Frame principal para organização dos elementos
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para entrada de site
        self.entry_frame = ttk.Frame(self.main_frame)
        self.entry_frame.pack(fill=tk.X, pady=5)
        
        # Campo de entrada com placeholder
        self.site_entry = ttk.Entry(self.entry_frame, width=40)
        self.site_entry.pack(side=tk.LEFT, padx=5)
        
        # Botão de adicionar ao lado do campo
        ttk.Button(self.entry_frame, text="Adicionar", command=self.add_site).pack(side=tk.LEFT, padx=5)
        
        # Texto placeholder
        self.placeholder = "Ex: instagram.com"
        self.site_entry.insert(0, self.placeholder)
        self.site_entry.config(foreground="gray")
        
        # Eventos do placeholder
        self.site_entry.bind("<FocusIn>", self.on_entry_click)
        self.site_entry.bind("<FocusOut>", self.on_focus_out)
        self.site_entry.bind("<Return>", lambda e: self.add_site())  # Permite adicionar com Enter
        
        # Lista de sites bloqueados
        self.sites_listbox = tk.Listbox(self.main_frame, width=50, height=15)
        self.sites_listbox.pack(pady=10)
        
        # Frame para organização dos botões
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)
        
        # Botões de controle (Editar e Remover)
        ttk.Button(self.button_frame, text="Editar", command=self.edit_site).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Remover", command=self.remove_site).pack(side=tk.LEFT, padx=5)

        # Frame adicional para o botão do navegador
        self.browser_frame = ttk.Frame(self.main_frame)
        self.browser_frame.pack(pady=5)
        
        # Botão para selecionar navegador
        ttk.Button(self.browser_frame, text="Selecionar Navegador", command=self.select_browser).pack(pady=5)
        
        # Carrega a lista inicial de sites
        self.update_sites_list()
    
    def on_entry_click(self, event):
        if self.site_entry.get() == self.placeholder:
            self.site_entry.delete(0, tk.END)
            self.site_entry.config(foreground="black")
    
    def on_focus_out(self, event):
        if not self.site_entry.get():
            self.site_entry.insert(0, self.placeholder)
            self.site_entry.config(foreground="gray")
    
    def update_sites_list(self):
        self.sites_listbox.delete(0, tk.END)          # Limpa a lista atual
        for site in self.sites_list:                  # Adiciona cada site à lista
            self.sites_listbox.insert(tk.END, site)
    
    def is_valid_url(self, url):
        pattern = r'^[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
        return re.match(pattern, url) is not None
    
    def add_site(self):
        url = self.site_entry.get().strip()
        if url == self.placeholder:  # Não salvar se ainda estiver com o placeholder
            messagebox.showerror("Erro", "Por favor, insira uma URL válida!")
            return
            
        if self.is_valid_url(url):                # Valida o formato da URL
            if url not in self.sites_list:        # Verifica se o site já existe
                self.sites_list.append(url)
                self.update_sites_list()
                self.site_entry.delete(0, tk.END)  # Limpa o campo
                self.site_entry.insert(0, self.placeholder)  # Restaura o placeholder
                self.site_entry.config(foreground="gray")
                self.window.focus_set()  # Remove o foco do campo
            else:
                messagebox.showwarning("Aviso", "Este site já está na lista!")
        else:
            messagebox.showerror("Erro", "URL inválida!")
    
    def edit_site(self):
        selected = self.sites_listbox.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione um site para editar!")
            return
            
        current_url = self.sites_list[selected[0]]
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Editar Site")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="URL do site:").pack(pady=5)
        entry = ttk.Entry(dialog, width=40)
        entry.insert(0, current_url)
        entry.pack(pady=5)
        
        def save():
            url = entry.get().strip()
            if self.is_valid_url(url):
                if url != current_url and url in self.sites_list:
                    messagebox.showwarning("Aviso", "Este site já está na lista!")
                else:
                    self.sites_list[selected[0]] = url
                    self.update_sites_list()
                    dialog.destroy()
            else:
                messagebox.showerror("Erro", "URL inválida!")
        
        ttk.Button(dialog, text="Salvar", command=save).pack(pady=5)
    
    def remove_site(self):
        selected = self.sites_listbox.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor, selecione um site para remover!")
            return
            
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este site?"):
            del self.sites_list[selected[0]]
            self.update_sites_list()

    def select_browser(self):
        browser_path = filedialog.askopenfilename(
            title="Selecione o navegador",
            filetypes=[("Arquivos executáveis", "*.exe;*.app;*")]
        )
        
        if browser_path:
            if self.website_manager.set_browser_path(browser_path):
                messagebox.showinfo("Sucesso", f"Navegador selecionado: {os.path.basename(browser_path)}")
            else:
                messagebox.showerror("Erro", "Caminho do navegador inválido")
