import tkinter as tk
from tkinter import ttk

class SettingsWindow:
    def __init__(self, parent, settings_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Configurações")
        self.window.geometry("500x400")
        
        self.settings_manager = settings_manager
        
        # Frame principal
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar as seções de configurações
        self.create_transition_settings()
        self.create_system_settings()

        # Frame para os botões
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20, fill=tk.X)

        # Botão Salvar
        self.save_button = ttk.Button(self.button_frame, text="Salvar", command=self.save_and_close)
        self.save_button.pack(side=tk.RIGHT, padx=5)
        
        # Botão Cancelar
        self.cancel_button = ttk.Button(self.button_frame, text="Cancelar", command=self.cancel_and_close)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
    
    # Frame para configurações de transição
    def create_transition_settings(self):
        frame = ttk.LabelFrame(self.main_frame, text="Configurações de Transição", padding="5")
        frame.pack(fill=tk.X, pady=5)
        
        # Tempo de transição
        ttk.Label(frame, text="Tempo entre ciclos:").pack(side=tk.LEFT, padx=5)
        times = ["3s", "5s", "10s"]
        self.transition_time = ttk.Combobox(frame, values=times, width=10, state="readonly")
        self.transition_time.set(f"{self.settings_manager.get_setting('transition_time')}s")
        self.transition_time.pack(side=tk.LEFT, padx=5)
        self.transition_time.bind('<<ComboboxSelected>>', self.on_transition_time_change)
    
    # Frame para configurações do sistema
    def create_system_settings(self):
        frame = ttk.LabelFrame(self.main_frame, text="Configurações do Sistema", padding="5")
        frame.pack(fill=tk.X, pady=5)
        
        # Checkbox para mostrar contador de ciclos
        self.show_cycles = tk.BooleanVar(value=self.settings_manager.get_setting('show_cycle_count'))
        ttk.Checkbutton(frame, 
                       text="Mostrar contador de ciclos", 
                       variable=self.show_cycles,
                       command=self.on_show_cycles_change).pack(anchor=tk.W, pady=2)
        
        # Checkbox para fechar navegador
        self.close_browser = tk.BooleanVar(value=self.settings_manager.get_setting('close_browser'))
        ttk.Checkbutton(frame, 
                       text="Fechar navegador ao bloquear sites", 
                       variable=self.close_browser,
                       command=self.on_close_browser_change).pack(anchor=tk.W, pady=2)
        
        # Checkbox para auto iniciar navegador
        self.auto_start = tk.BooleanVar(value=self.settings_manager.get_setting('auto_start_browser'))
        ttk.Checkbutton(frame, 
                       text="Iniciar navegador após bloqueio", 
                       variable=self.auto_start,
                       command=self.on_auto_start_change).pack(anchor=tk.W, pady=2)
    
    # Callbacks
    def on_transition_time_change(self, event):
        value = int(self.transition_time.get().replace('s', ''))
        self.settings_manager.update_setting('transition_time', value)
    
    def on_show_cycles_change(self):
        self.settings_manager.update_setting('show_cycle_count', self.show_cycles.get())
    
    def on_close_browser_change(self):
        self.settings_manager.update_setting('close_browser', self.close_browser.get())
    
    def on_auto_start_change(self):
        self.settings_manager.update_setting('auto_start_browser', self.auto_start.get())

    def save_and_close(self):
        if self.settings_manager.save_settings():
            self.window.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar as configurações!")

    def cancel_and_close(self):
        self.settings_manager.discard_changes()
        self.window.destroy()