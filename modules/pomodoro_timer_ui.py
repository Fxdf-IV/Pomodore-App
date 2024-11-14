import tkinter as tk
from tkinter import messagebox, OptionMenu, Button
from pomodoro_timer import PomodoroTimer
from website_manager import WebsiteManagerWindow

# Configuração Front-end da janela principal
class PomodoroTimerUI:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("450x825")

        # Recebe todo retorno da classe PomodoroTimer (iniciando o timer)
        self.pomodoro_timer = PomodoroTimer()

        self.selected_option = 0
        
        self.work_duration = f"{00:02}"
        self.short_break_duration = f"{00:02}"
        self.long_break_duration = f"{00:02}"
        self.total_cycles = f"{00:02}"
        
        # Inicializa a seleção do Pomodoro Clássico
        self.current_option_selection = tk.IntVar(value=1)  # Começa com o case 1 selecionado
        self.pomodoro_timer.timer_options(1)  # Aplica a configuração do Pomodoro Clássico

        # Elementos da interface gráfica (Título e cronômetro)
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Exibição do tempo formatado (MM:SS)
        self.time_label = tk.Label(root, text=self.pomodoro_timer.format_time_to_display(self.pomodoro_timer.current_time), font=("Helvetica", 36))

        # Exibição do tempo formatado (HH:MM:SS)
        self.time_custom_label = tk.Label(root, text=self.pomodoro_timer.format_time_to_display_custom(self.pomodoro_timer.current_time), font=("Helvetica", 36))
        self.time_custom_label.pack(pady=20)

        self.title_label = tk.Label(root, text=self.get_title_text(), font=("Helvetica", 14))
        self.title_label.pack(pady=10)

        self.message_label = tk.Label(root, text=self.get_cycle_message_text(), font=("Helvetica", 10))
        self.message_label.pack(pady=10)

        self.work_time_label = tk.Label(root, text= "Tempo de foco", font=("Helvetica", 7))
        self.short_break_label = tk.Label(root, text= "Pausa curta", font=("Helvetica", 7))
        self.long_break_label = tk.Label(root, text= "Pausa longa", font=("Helvetica", 7))
        self.focus_cycles_label = tk.Label(root, text= "Ciclos de foco", font=("Helvetica", 7))

        # Botões de controle (Iniciar, Parar e Redefinir)
        self.start_button = tk.Button(root, text="Start", command=self.start_timer_ui)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, text="Pause", command=self.pause_timer_ui)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(root, text="Stop", command=self.stop_timer_ui)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Botão para gerenciar sites bloqueados
        self.manage_sites_button = tk.Button(root, text="Gerenciar Sites", command=self.open_website_manager)
        self.manage_sites_button.pack(side=tk.LEFT, padx=10)

        self.send_custom_values_button = tk.Button(root, text="Send", command=self.send_custom_values_ui)

        # Botão para mostrar descrição da técnica selecionada
        self.show_description_button = Button(self.root, text="Mostrar Descrição", command=self.display_selected_option_description)
        self.show_description_button.pack(pady=10)

        self.explanation_methods = tk.Label(root, text= 
        """
        Tempo de decanso a cada 1h de foco

        Pomodoro Clássico:
        Tempo de foco: 01:40 - Descanso: 00:40
        24 minutos de descanso.

        Pomodoro de 50/10:
        Tempo de foco: 03:20 - Descanso: 00:55
        16,5 minutos de descanso.

        Pomodoro de 60/15:
        Tempo de foco: 04:00 - Descanso: 01:15
        30 minutos de descanso.

        Técnica 52/17:
        Tempo de foco: 00:52 - Descanso: 00:17
        ~19,6 minutos de descanso.

        Técnica (10/2) 6x:
        Tempo de foco: 01:00 - Descanso: 00:02 
        22 minutos de descanso.

        """, 
        font=("Helvetica", 7))
        self.explanation_methods.place(x=5, y=550)

        # Entrada personalizada "Pomodoro Flexível"
        self.work_hr_entry = tk.Entry(root, width=3)
        self.work_hr_entry.insert(0, "00")
        self.work_min_entry = tk.Entry(root, width=3)
        self.work_min_entry.insert(0, "00")
        self.work_sec_entry = tk.Entry(root, width=3)
        self.work_sec_entry.insert(0, "00")
        self.short_break_hr_entry = tk.Entry(root, width=3)
        self.short_break_hr_entry.insert(0, "00")
        self.short_break_min_entry = tk.Entry(root, width=3)
        self.short_break_min_entry.insert(0, "00")
        self.short_break_sec_entry = tk.Entry(root, width=3)
        self.short_break_sec_entry.insert(0, "00")
        self.long_break_hr_entry = tk.Entry(root, width=3)
        self.long_break_hr_entry.insert(0, "00")
        self.long_break_min_entry = tk.Entry(root, width=3)
        self.long_break_min_entry.insert(0, "00")
        self.long_break_sec_entry = tk.Entry(root, width=3)
        self.long_break_sec_entry.insert(0, "00")
        self.cycles_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))

        self.work_hr_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.work_min_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.work_sec_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.short_break_hr_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.short_break_min_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.short_break_sec_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.long_break_hr_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.long_break_min_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.long_break_sec_entry.bind("<KeyPress>", self.only_number_entry_values)
        self.cycles_entry.bind("<KeyPress>", self.only_number_entry_values)
        
        self.work_hr_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.work_min_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.work_sec_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.short_break_hr_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.short_break_min_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.short_break_sec_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.long_break_hr_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.long_break_min_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.long_break_sec_entry.bind("<KeyRelease>", self.replace_entry_values)
        self.cycles_entry.bind("<KeyRelease>", self.replace_entry_values)
    
        self.pomodoro_timer.configure_timer_settings(
            self.work_duration,
            self.short_break_duration,
            self.long_break_duration,
            self.cycles_entry
        )

        self.create_pomodoro_option_selector()
        self.handle_pomodoro_option_change(1)

    def create_pomodoro_option_selector(self):
        self.current_option_selection = tk.IntVar(value=1)
        self.pomodoro_option_menu = OptionMenu(self.root, self.current_option_selection, *[int(i) for i in range(1, 7)], command=self.handle_pomodoro_option_change)
        self.pomodoro_option_menu.pack(pady=20)
 
    def display_custom_entries(self):
        self.time_custom_label.pack_forget()

        self.work_time_label.pack(pady=7)
        self.work_hr_entry.pack(pady=5)
        self.work_min_entry.pack(pady=5)
        self.work_sec_entry.pack(pady=5)

        self.short_break_label.pack(pady=7)
        self.short_break_hr_entry.pack(pady=5)
        self.short_break_min_entry.pack(pady=5)
        self.short_break_sec_entry.pack(pady=5)
        
        self.long_break_label.pack(pady=7)
        self.long_break_hr_entry.pack(pady=5)
        self.long_break_min_entry.pack(pady=5)
        self.long_break_sec_entry.pack(pady=5)

        self.focus_cycles_label.pack(pady=7)
        self.cycles_entry.pack(pady=5)

        self.send_custom_values_button.pack(side=tk.RIGHT, padx=10)

    def hide_custom_input_fields(self):
        self.time_label.pack(pady=20)

        self.time_custom_label.pack_forget()

        self.work_time_label.pack_forget()
        self.work_hr_entry.pack_forget()
        self.work_min_entry.pack_forget()
        self.work_sec_entry.pack_forget()

        self.short_break_label.pack_forget()
        self.short_break_hr_entry.pack_forget()
        self.short_break_min_entry.pack_forget()
        self.short_break_sec_entry.pack_forget()

        self.long_break_label.pack_forget()
        self.long_break_hr_entry.pack_forget()
        self.long_break_min_entry.pack_forget()
        self.long_break_sec_entry.pack_forget()

        self.focus_cycles_label.pack_forget()
        self.cycles_entry.pack_forget()

        self.send_custom_values_button.pack_forget()
    
    # Mostra ou oculta entradas baseadas na técnica selecionada.    
    def handle_pomodoro_option_change(self, value):
        self.selected_option = value
        self.check_custom_option(value)
        self.pomodoro_timer.timer_options(int(value))
        self.update_timer_display()

        self.trigger_option_change_handler()
        self.pomodoro_timer.timer_options(value)
        self.reset_display_interface()
        self.message_label.config(text=self.get_cycle_message_text())

    def check_custom_option(self, value):
        if value == 6:                          # Se a técnica selecionada for "Pomodoro Flexível"
            self.fill_timer_settings_fields()
            self.display_custom_entries()         # Mostra os campos de entrada
        else:
            self.hide_custom_input_fields()          # Oculta os campos de entrada

    def trigger_option_change_handler(self):
        self.handle_pomodoro_option_change
        self.pomodoro_timer.configure_timer_settings
        self.stop_timer_ui()

    # Funções que chamam os métodos em PomodoroTimer
    def get_cycle_message_text(self):
        return self.pomodoro_timer.cycle_message

    def get_title_text(self):
        return self.pomodoro_timer.title

    def display_selected_option_description(self):
        option = self.current_option_selection.get()
        self.pomodoro_timer.timer_options(option)
        description = self.pomodoro_timer.description
        messagebox.showinfo("Descrição", description)

    def open_website_manager(self):
        WebsiteManagerWindow(self.root, self.pomodoro_timer.sites)

    def fill_timer_settings_fields(self):
        self.update_timer_display()

        self.work_duration = int(self.work_hr_entry.get()) * 3600 + int(self.work_min_entry.get()) * 60 + int(self.work_sec_entry.get())
        self.short_break_duration = int(self.short_break_hr_entry.get()) * 3600 + int(self.short_break_min_entry.get()) * 60 + int(self.short_break_sec_entry.get())
        self.long_break_duration = int(self.long_break_hr_entry.get()) * 3600 + int(self.long_break_min_entry.get()) * 60 + int(self.long_break_sec_entry.get())
    
        self.pomodoro_timer.configure_timer_settings(
            self.work_duration,
            self.short_break_duration,
            self.long_break_duration,
            int(self.cycles_entry.get())
        )
         
    def start_timer_ui(self,):
        if not self.pomodoro_timer.is_timer_running and self.pomodoro_timer.current_time != 0:  # Inicia o cronômetro apenas se não estiver rodando
            self.pomodoro_timer.start_timer()
            self.update_timer_display()

    def pause_timer_ui(self):
        self.pomodoro_timer.pause_timer()

    def stop_timer_ui(self):
        self.pomodoro_timer.stop_timer()
        self.update_timer_display()

    def send_custom_values_ui(self):
         if self.selected_option == 6 :
            try:
                 self.fill_timer_settings_fields()
                 self.stop_timer_ui()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores válidos.")
                     

    def update_timer_display(self):
        self.reset_display_interface()
        self.message_label.config(text=self.get_cycle_message_text())

        if  self.pomodoro_timer.is_timer_running:
                self.root.after(1000, self.update_timer_display)         # Chama novamente após 1 segundo
                self.pomodoro_timer.update_timer()

    def reset_display_interface(self):
        
        if self.selected_option != 6 :
            self.time_label.config(text=self.pomodoro_timer.format_time_to_display(self.pomodoro_timer.current_time))
            self.title_label.config(text=self.get_title_text())
        else:
            self.time_label.config(text=self.pomodoro_timer.format_time_to_display_custom(self.pomodoro_timer.current_time))
            self.title_label.config(text=self.get_title_text())

    def replace_entry(self, entry, default_value, replace_value, max_value):
        entry_value = entry.get()

        if entry_value == "":
            entry.delete(0, "end")
            entry.insert(0, f"{default_value:02}")

        elif int(entry_value) >= max_value:
            entry.delete(0, "end")
            entry.insert(0, f"{replace_value:02}")

    def replace_entry_values(self, event):
        replace_hr = 23
        replace_mm_ss = 59
        replace_null = 0

        # Aplica para as entradas de hora, minuto e segundo de todas as seções
        self.replace_entry(self.work_hr_entry, replace_null, replace_hr, 24)
        self.replace_entry(self.work_min_entry, replace_null, replace_mm_ss, 60)
        self.replace_entry(self.work_sec_entry, replace_null, replace_mm_ss, 60)

        self.replace_entry(self.short_break_hr_entry, replace_null, replace_hr, 24)
        self.replace_entry(self.short_break_min_entry, replace_null, replace_mm_ss, 60)
        self.replace_entry(self.short_break_sec_entry, replace_null, replace_mm_ss, 60)

        self.replace_entry(self.long_break_hr_entry, replace_null, replace_hr, 24)
        self.replace_entry(self.long_break_min_entry, replace_null, replace_mm_ss, 60)
        self.replace_entry(self.long_break_sec_entry, replace_null, replace_mm_ss, 60)

    def only_number_entry_values(self, event):

        if event.keysym in ["BackSpace", "Delete"]:
            return

        if not event.char.isdigit():
            return "break"