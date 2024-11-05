import tkinter as tk
from tkinter import messagebox, OptionMenu, Entry, Button

# Configuração Back-end da janela principal
class PomodoroTimer:
    def __init__(self):
        # Configurações iniciais do Pomodoro
        self.work_duration = 0 
        self.short_break_duration = 0 
        self.long_break_duration = 0 
        self.total_cycles = 0
        self.description = ""
        
        self.current_cycle = self.total_cycles
        self.short_break_count = self.total_cycles
        self.is_short_break_timer_active = False
        self.is_long_break_timer_active = False
        self.is_focus_timer_active = True
        self.is_timer_running = False             # Controla o estado do timer (False = parado)
        self.current_time = self.work_duration     # Tempo atual (inicia com tempo de foco selecionado)
        self.cycle_message = "Foco total! É hora de trabalhar."

    # Converte o tempo de segundos para o formato MM:SS.
    def format_time_to_display(self, total_seconds):
        minutes = total_seconds  // 60
        remaining_seconds = total_seconds  % 60
        return f"{minutes:02}:{remaining_seconds:02}"
    
    # Inicia o timer
    def start_timer(self):
        if not self.is_timer_running:
            self.is_timer_running = True
            self.update_timer()
        
    # Pausa o timer
    def pause_timer(self):
            if self.is_timer_running:
                self.is_timer_running = False

    # Para e reinicia o timer
    def stop_timer(self):
        self.current_cycle = self.total_cycles
        self.short_break_count = self.total_cycles
        self.is_timer_running = False
        self.current_time = self.work_duration
        self.cycle_message = "Foco total! É hora de trabalhar."
    
    # Atualiza o tempo restante a cada segundo e gerencia as trocas de ciclos.
    def update_timer(self):
        if self.is_timer_running:
            if self.current_time > 0 :
                self.current_time -= 1
            else:
                self.handle_cycle_switch()             # Quando o tempo termina, completa o ciclo de foco

    # Gerencia a mudança entre ciclos de pausas curtas e longas.
    def handle_cycle_switch(self):

        if     self.current_cycle == 1 :
                self.current_time = self.long_break_duration
                self.cycle_message = "Pausa longa! Descanse bem e recarregue suas energias."
                self.is_long_break_timer_active = True
                self.is_focus_timer_active = False
                self.is_short_break_timer_active = False          
                self.current_cycle = self.total_cycles
                self.short_break_count = self.total_cycles - 1
                print("Pausa longa")

        elif   self.current_cycle == self.short_break_count :
                self.current_time = self.short_break_duration
                self.cycle_message = "Pausa curta! Aproveite um momento para relaxar."                
                self.is_short_break_timer_active = True
                self.is_focus_timer_active = False
                self.is_long_break_timer_active = False
                self.short_break_count -= 1                
                print("Pausa curta ", self.short_break_count)

        else:
                self.start_focus_cycle()

    # Gerencia a mudança entre ciclos de foco.
    def start_focus_cycle(self):

        if     self.is_short_break_timer_active == True or self.is_long_break_timer_active == True :
                self.current_time = self.work_duration
                self.cycle_message = "Foco total! É hora de trabalhar."                        
                self.is_short_break_timer_active = False
                self.is_long_break_timer_active = False
                self.is_focus_timer_active = True
                self.current_cycle -= 1                    
                print("Ciclo atual ", self.current_cycle)

    # Chama a entrada do usuário, e armazena os valores retornados
    def configure_timer_settings(self, work_duration, short_break_duration, long_break_duration, total_cycles):
        self.work_duration = work_duration
        self.short_break_duration = short_break_duration
        self.long_break_duration = long_break_duration
        self.total_cycles = total_cycles
    
    def timer_options(self, option):

        match option:
            case 1:
                self.title = "Pomodoro Clássico"
                self.work_duration = 5
                self.short_break_duration = 2
                self.long_break_duration = 3 
                self.total_cycles = 4
                self.description = ("Esta é a abordagem original do método Pomodoro, que consiste em ciclos de 25 minutos de trabalho concentrado. A pausa curta de 5 minutos permite relaxar e recarregar as energias, enquanto a pausa longa, após quatro ciclos, oferece um tempo maior para descansar e refletir sobre o progresso feito, ajudando a evitar a fadiga mental. Tempo de foco: 01h40 (4 ciclos de 25 minutos). Tempo total de descanso: 00h40 (3 pausas curtas de 5 minutos + 1 pausa longa de 15 minutos).")

            case 2:
                self.title = "Pomodoro 60/15"
                self.work_duration = 60
                self.short_break_duration = 15
                self.long_break_duration = 30
                self.total_cycles = 4
                self.description = ("Neste método, você se dedica a 60 minutos de trabalho focado, seguido de uma pausa de 15 minutos. A pausa longa após quatro ciclos é de 30 minutos, permitindo um descanso mais profundo. É adequado para projetos que exigem longos períodos de atenção e concentração. Tempo de foco: 04h00 (4 ciclos de 60 minutos). Tempo total de descanso: 01h15 (3 pausas curtas de 15 minutos + 1 pausa longa de 30 minutos).")

            case 3:
                self.title = "Pomodoro 50/10"
                self.work_duration = 50
                self.short_break_duration = 10
                self.long_break_duration = 25
                self.total_cycles = 4
                self.description = ("Esta variação consiste em períodos mais longos de trabalho, com 50 minutos dedicados à concentração total em uma tarefa. As pausas curtas de 10 minutos ajudam a manter o fluxo de energia e foco. Após quatro ciclos, a pausa longa proporciona um intervalo mais significativo para recarregar as energias, ideal para tarefas que exigem mais tempo contínuo de atenção. Tempo de foco: 03h20 (200 minutos, 4 ciclos de 50 minutos). Tempo total de descanso: 00h55 (3 pausas curtas de 10 minutos + 1 pausa longa de 25 minutos).")

            case 4:
                self.title = "Pomodoro 52/17"
                self.work_duration = 52
                self.short_break_duration = 17
                self.long_break_duration = 0
                self.total_cycles = 1
                self.description = ("Consiste em 52 minutos de trabalho focado, seguidos de 17 minutos de pausa. É uma técnica popular entre trabalhadores que buscam maximizar a produtividade, permitindo um fluxo de trabalho contínuo sem pausas longas. Tempo de foco: 00:52 (Ciclicamente). Tempo total de descanso: 00h17 (Apenas pausas curtas).")

            case 5:
                self.title = "Pomodoro The (10/2) 6x"
                self.work_duration = 10
                self.short_break_duration = 2
                self.long_break_duration = 10
                self.total_cycles = 6
                self.description = ("Este método é composto por 10 minutos de trabalho intenso seguidos de 2 minutos de pausa. Após completar 6 ciclos, você faz uma pausa longa de 10 minutos. Essa técnica é ideal para tarefas curtas e rápidas, ajudando a manter a energia e a concentração, permitindo um fluxo constante de produtividade.Tempo de foco: 01h00 (6 ciclos de 10 minutos). Tempo total de descanso: 00h22 (6 pausas curtas de 2 minutos + 1 pausa longa de 10 minutos).")

            case 6:
                self.title = "Pomodoro Flexível"
                self.description = "Pomodoro Flexível: Durações personalizadas."
                
        # Defina configurações adicionais para outras opções de Pomodoro
        self.current_cycle = self.total_cycles
        self.current_time = self.work_duration  # Atualiza o tempo de trabalho inicial
        self.is_timer_running = False

# Configuração Front-end da janela principal
class PomodoroTimerUI:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("450x825")

        # Recebe todo retorno da classe PomodoroTimer (iniciando o timer)
        self.pomodoro = PomodoroTimer()

        self.selected_option = 0

        # Entrada personalizada "Pomodoro Flexível"
        self.work_time_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.shor_break_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.long_break_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.cycles_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))

        self.pomodoro.configure_timer_settings(self.work_time_entry, self.shor_break_entry, self.long_break_entry, self.cycles_entry)

        # Inicializa a seleção do Pomodoro Clássico
        self.current_option_selection = tk.IntVar(value=1)  # Começa com o case 1 selecionado
        self.pomodoro.timer_options(1)  # Aplica a configuração do Pomodoro Clássico

        # Elementos da interface gráfica (Título e cronômetro)
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Exibição do tempo formatado (MM:SS)
        self.time_label = tk.Label(root, text=self.pomodoro.format_time_to_display(self.pomodoro.current_time), font=("Helvetica", 36))
        self.time_label.pack(pady=20)

        self.title_label = tk.Label(root, text=self.get_title_text(), font=("Helvetica", 14))
        self.title_label.pack(pady=10)

        self.message_label = tk.Label(root, text=self.get_cycle_message_text(), font=("Helvetica", 10))
        self.message_label.pack(pady=10)

        self.focus_time_label = tk.Label(root, text= "Tempo de foco", font=("Helvetica", 7))
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

        self.create_pomodoro_option_selector()
        self.handle_pomodoro_option_change(1)

    def create_pomodoro_option_selector(self):
        self.current_option_selection = tk.IntVar(value=1)
        self.pomodoro_option_menu = OptionMenu(self.root, self.current_option_selection, *[int(i) for i in range(1, 7)], command=self.handle_pomodoro_option_change)
        self.pomodoro_option_menu.pack(pady=20)
 
    def display_custom_entries(self):
        self.focus_time_label.pack(pady=7)
        self.work_time_entry.pack(pady=5)
        self.short_break_label.pack(pady=7)
        self.shor_break_entry.pack(pady=5)
        self.long_break_label.pack(pady=7)
        self.long_break_entry.pack(pady=5)
        self.focus_cycles_label.pack(pady=7)
        self.cycles_entry.pack(pady=5)
        self.send_custom_values_button.pack(side=tk.RIGHT, padx=10)

    def hide_custom_input_fields(self):
        self.work_time_entry.pack_forget()
        self.shor_break_entry.pack_forget()
        self.long_break_entry.pack_forget()
        self.cycles_entry.pack_forget()
        self.focus_time_label.pack_forget()
        self.short_break_label.pack_forget()
        self.long_break_label.pack_forget()
        self.focus_cycles_label.pack_forget()
        self.send_custom_values_button.pack_forget()
    
    # Mostra ou oculta entradas baseadas na técnica selecionada.    
    def handle_pomodoro_option_change(self, value):
        self.selected_option = value
        self.check_custom_option(value)
        self.pomodoro.timer_options(int(value))
        self.update_timer_display()

        self.trigger_option_change_handler()
        self.pomodoro.timer_options(value)
        self.time_label.config(text=self.pomodoro.format_time_to_display(self.pomodoro.current_time))
        self.title_label.config(text=self.get_title_text())
        self.message_label.config(text=self.get_cycle_message_text())

    def check_custom_option(self, value):
        if value == 6:                          # Se a técnica selecionada for "Pomodoro Flexível"
            self.fill_timer_settings_fields()
            self.display_custom_entries()          # Mostra os campos de entrada
        else:
            self.hide_custom_input_fields()          # Oculta os campos de entrada

    def trigger_option_change_handler(self):
        self.handle_pomodoro_option_change
        self.pomodoro.configure_timer_settings
        self.stop_timer_ui()

    # Funções que chamam os métodos em PomodoroTimer
    def get_cycle_message_text(self):
        return self.pomodoro.cycle_message

    def get_title_text(self):
        return self.pomodoro.title

    def display_selected_option_description(self):
        option = self.current_option_selection.get()
        self.pomodoro.timer_options(option)
        description = self.pomodoro.description
        messagebox.showinfo("Descrição: ", description) 

    def fill_timer_settings_fields(self):
         self.update_timer_display()
         self.pomodoro.configure_timer_settings(
            int(self.work_time_entry.get()) * 60,
            int(self.shor_break_entry.get()) * 60,
            int(self.long_break_entry.get()) * 60,
            int(self.cycles_entry.get()))
        

         
    def start_timer_ui(self,):
        if not self.pomodoro.is_timer_running and self.pomodoro.current_time != 0:  # Inicia o cronômetro apenas se não estiver rodando
            self.pomodoro.start_timer()
            self.update_timer_display()

    def pause_timer_ui(self):
        self.pomodoro.pause_timer()

    def stop_timer_ui(self):
        self.pomodoro.stop_timer()
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

        if  self.pomodoro.is_timer_running:
                self.root.after(1000, self.update_timer_display)         # Chama novamente após 1 segundo
                self.pomodoro.update_timer()

    def reset_display_interface(self):
        self.time_label.config(text=self.pomodoro.format_time_to_display(self.pomodoro.current_time))
        self.title_label.config(text=self.get_title_text())

# Criação da janela principal e execução do aplicativo
root = tk.Tk()
app = PomodoroTimerUI(root)
root.mainloop()