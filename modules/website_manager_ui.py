import tkinter as tk
from tkinter import ttk, messagebox, font
import re

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

        # Frame adicional para o botão do navegador
        self.browser_frame = ttk.Frame(self.main_frame)
        self.browser_frame.pack(pady=5)
        
        # Botão para selecionar o navegador
        ttk.Button(self.browser_frame, text="Selecione seu navegador", command=self.website_manager.ask_for_browser).pack(pady=5)
        
        # Carrega a lista inicial de sites
        self.update_sites_list()
        
    def update_sites_list(self):
        self.sites_listbox.delete(0, tk.END)          # Limpa a lista atual
        for site in self.sites_list:                  # Adiciona cada site à lista
            self.sites_listbox.insert(tk.END, site)
    
    def is_valid_url(self, url):
        pattern = r'^[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$'
        return re.match(pattern, url) is not None
    
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
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(font=("Helvetica", 9), fg="black")  # Remove o itálico
                
        def on_focus_out(event):
            if not entry.get():
                entry.config(font=italic_font, fg="gray")  # Restaura o itálico
                entry.insert(0, placeholder)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
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
