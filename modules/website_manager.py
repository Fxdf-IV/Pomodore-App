import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import os

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
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=5)
        
        # Função interna para salvar o novo site
        def save():
            url = entry.get().strip()
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
        entry = ttk.Entry(dialog, width=40)
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
