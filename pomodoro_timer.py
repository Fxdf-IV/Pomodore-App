import tkinter as tk
from tkinter import messagebox, OptionMenu, Entry, Button

# Configuração Back-end da janela principal
class PomodoroTimer:
    def __init__(self):
        # Configurações iniciais do Pomodoro
        self.work_time = 0 * 60
        self.short_break = 0 * 60
        self.long_break = 0 * 60
        self.cycles = 4 - 1
        self.description = ""
        
        self.current_cycle = self.cycles
        self.short_break_count = self.cycles
        self.status_s_break_timer = False
        self.status_l_break_timer = False
        self.status_focus_timer = True
        self.timer_running = False             # Controla o estado do timer (False = parado)
        self.current_time = self.work_time     # Tempo atual (inicia com tempo de foco selecionado)
        self.mensage_cycle = "Foco total! É hora de trabalhar."
        print("CICLO INICIAL ", self.current_cycle)

     # Converte o tempo de segundos para o formato MM:SS.
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
    
     # Inicia o timer
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
        
     # Pausa o timer
    def pause_timer(self):
            if self.timer_running:
                self.timer_running = False

     # Para e reinicia o timer
    def stop_timer(self):
        self.current_cycle = self.cycles
        self.short_break_count = self.cycles
        self.timer_running = False
        self.current_time = self.work_time
        self.mensage_cycle = "Foco total! É hora de trabalhar."
    
     # Atualiza o tempo restante a cada segundo e gerencia as trocas de ciclos.
    def update_timer(self):
        if self.timer_running:
            if self.current_time > 0 :
                self.current_time -= 1
            else:
                self.breaks_time()             # Quando o tempo termina, completa o ciclo de foco     

     # Gerencia a mudança entre ciclos de pausas curtas e longas.
    def breaks_time(self):

        if     self.current_cycle == 0 :
                self.current_time = self.long_break
                self.mensage_cycle = "Pausa longa! Descanse bem e recarregue suas energias."
                self.status_l_break_timer = True
                self.status_focus_timer = False
                self.status_s_break_timer = False          
                self.current_cycle = self.cycles
                self.short_break_count = self.cycles - 1
                print("Pausa longa")

        elif   self.current_cycle == self.short_break_count :
                self.current_time = self.short_break
                self.mensage_cycle = "Pausa curta! Aproveite um momento para relaxar."                
                self.status_s_break_timer = True
                self.status_focus_timer = False
                self.status_l_break_timer = False
                self.short_break_count -= 1                
                print("Pausa curta ", self.short_break_count)

        else:
                self.focus_time()

        # Gerencia a mudança entre ciclos de foco.
    def focus_time(self):

        if     self.status_s_break_timer == True or self.status_l_break_timer == True :
                self.current_time = self.work_time
                self.mensage_cycle = "Foco total! É hora de trabalhar."                        
                self.status_s_break_timer = False
                self.status_l_break_timer = False
                self.status_focus_timer = True
                self.current_cycle -= 1                    
                print("Ciclo atual ", self.current_cycle)

    # Chama a entrada do usuário, e armazena os valores retornados
    def set_option_values(self, work_time, short_break, long_break, cycles):
        self.work_time = work_time
        self.short_break = short_break
        self.long_break = long_break
        self.cycles = cycles
    
    def set_timer(self, option):

        match option:
            case 1:
                self.title = "Pomodoro Clássico"
                self.work_time = 5
                self.short_break = 2
                self.long_break = 3 
                self.cycles = 4
                self.description = ("Esta é a abordagem original do método Pomodoro, que consiste em ciclos de 25 minutos de trabalho concentrado. A pausa curta de 5 minutos permite relaxar e recarregar as energias, enquanto a pausa longa, após quatro ciclos, oferece um tempo maior para descansar e refletir sobre o progresso feito, ajudando a evitar a fadiga mental. Tempo de foco: 01h40 (4 ciclos de 25 minutos). Tempo total de descanso: 00h40 (3 pausas curtas de 5 minutos + 1 pausa longa de 15 minutos).")

            case 2:
                self.title = "Pomodoro 60/15"
                self.work_time = 60
                self.short_break = 15
                self.long_break = 30
                self.cycles = 4
                self.description = ("Neste método, você se dedica a 60 minutos de trabalho focado, seguido de uma pausa de 15 minutos. A pausa longa após quatro ciclos é de 30 minutos, permitindo um descanso mais profundo. É adequado para projetos que exigem longos períodos de atenção e concentração. Tempo de foco: 04h00 (4 ciclos de 60 minutos). Tempo total de descanso: 01h15 (3 pausas curtas de 15 minutos + 1 pausa longa de 30 minutos).")

            case 3:
                self.title = "Pomodoro 50/10"
                self.work_time = 50
                self.short_break = 10
                self.long_break = 25
                self.cycles = 4
                self.description = ("Esta variação consiste em períodos mais longos de trabalho, com 50 minutos dedicados à concentração total em uma tarefa. As pausas curtas de 10 minutos ajudam a manter o fluxo de energia e foco. Após quatro ciclos, a pausa longa proporciona um intervalo mais significativo para recarregar as energias, ideal para tarefas que exigem mais tempo contínuo de atenção. Tempo de foco: 03h20 (200 minutos, 4 ciclos de 50 minutos). Tempo total de descanso: 00h55 (3 pausas curtas de 10 minutos + 1 pausa longa de 25 minutos).")

            case 4:
                self.title = "Pomodoro 52/17"
                self.work_time = 52
                self.short_break = 17
                self.long_break = 0
                self.cycles = 1
                self.description = ("Consiste em 52 minutos de trabalho focado, seguidos de 17 minutos de pausa. É uma técnica popular entre trabalhadores que buscam maximizar a produtividade, permitindo um fluxo de trabalho contínuo sem pausas longas. Tempo de foco: 00:52 (Ciclicamente). Tempo total de descanso: 00h17 (Apenas pausas curtas).")

            case 5:
                self.title = "Pomodoro The (10/2) 6x"
                self.work_time = 10
                self.short_break = 2
                self.long_break = 10
                self.cycles = 6
                self.description = ("Este método é composto por 10 minutos de trabalho intenso seguidos de 2 minutos de pausa. Após completar 6 ciclos, você faz uma pausa longa de 10 minutos. Essa técnica é ideal para tarefas curtas e rápidas, ajudando a manter a energia e a concentração, permitindo um fluxo constante de produtividade.Tempo de foco: 01h00 (6 ciclos de 10 minutos). Tempo total de descanso: 00h22 (6 pausas curtas de 2 minutos + 1 pausa longa de 10 minutos).")

            case 6:
                self.title = "Pomodoro Flexível"
                self.description = "Pomodoro Flexível: Durações personalizadas."
                
        # Defina configurações adicionais para outras opções de Pomodoro
        self.current_cycle = self.cycles
        self.current_time = self.work_time  # Atualiza o tempo de trabalho inicial
        self.timer_running = False

# Configuração Front-end da janela principal
class MainInterfaceWindow:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("450x650")

        # Recebe todo retorno da classe PomodoroTimer (iniciando o timer)
        self.pomodoro = PomodoroTimer()

        self.current_value = 0

        # Entrada personalizada "Pomodoro Flexível"
        self.work_time_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.shor_break_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.long_break_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))
        self.cycles_entry = tk.Entry(root, textvariable=tk.StringVar(value="0"))

        self.pomodoro.set_option_values(self.work_time_entry, self.shor_break_entry, self.long_break_entry, self.cycles_entry)

        # Inicializa a seleção do Pomodoro Clássico
        self.select_option = tk.IntVar(value=1)  # Começa com o case 1 selecionado
        self.pomodoro.set_timer(1)  # Aplica a configuração do Pomodoro Clássico

        # Elementos da interface gráfica (Título e cronômetro)
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Exibição do tempo formatado (MM:SS)
        self.time_display = tk.Label(root, text=self.pomodoro.format_time(self.pomodoro.current_time), font=("Helvetica", 36))
        self.time_display.pack(pady=20)

        self.title = tk.Label(root, text=self.text_title(), font=("Helvetica", 14))
        self.title.pack(pady=10)

        self.mensage = tk.Label(root, text=self.text_message_cycle(), font=("Helvetica", 10))
        self.mensage.pack(pady=10)

        self.text1 = tk.Label(root, text= "Tempo de foco", font=("Helvetica", 7))
        self.text2 = tk.Label(root, text= "Pausa curta", font=("Helvetica", 7))
        self.text3 = tk.Label(root, text= "Pausa longa", font=("Helvetica", 7))
        self.text4 = tk.Label(root, text= "Ciclos de foco", font=("Helvetica", 7))

        # Botões de controle (Iniciar, Parar e Redefinir)
        self.start_button = tk.Button(root, text="Start", command=self.start_timer_interface)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.stop_button = tk.Button(root, text="Pause", command=self.pause_timer_interface)
        self.stop_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(root, text="Stop", command=self.stop_timer_interface)
        self.reset_button.pack(side=tk.LEFT, padx=20)

        # Botão para mostrar descrição da técnica selecionada
        self.description_button = Button(self.root, text="Mostrar Descrição", command=self.show_description)
        self.description_button.pack(pady=10)

        self.select_box_pomodoro_option()
        self.on_option_change(1)

        
    def select_box_pomodoro_option(self):
        self.select_option = tk.IntVar(value=1)
        self.option_menu = OptionMenu(self.root, self.select_option, *[int(i) for i in range(1, 7)], command=self.on_option_change)
        self.option_menu.pack(pady=20)
 
    def show_custom_entries(self):
        self.text1.pack(pady=7)
        self.work_time_entry.pack(pady=5)
        self.text2.pack(pady=7)
        self.shor_break_entry.pack(pady=5)
        self.text3.pack(pady=7)
        self.long_break_entry.pack(pady=5)
        self.text4.pack(pady=7)
        self.cycles_entry.pack(pady=5)

    def hide_custom_entries(self):
        self.work_time_entry.pack_forget()
        self.shor_break_entry.pack_forget()
        self.long_break_entry.pack_forget()
        self.cycles_entry.pack_forget()
        self.text1.pack_forget()
        self.text2.pack_forget()
        self.text3.pack_forget()
        self.text4.pack_forget()
    
    # Mostra ou oculta entradas baseadas na técnica selecionada.    
    def on_option_change(self, value):
        self.current_value = value
        self.verify_custom_option(value)
        self.pomodoro.set_timer(int(value))
        self.update_timer_display()

        self.on_option_change_wrapper()
        self.pomodoro.set_timer(value)
        self.time_display.config(text=self.pomodoro.format_time(self.pomodoro.current_time))
        self.title.config(text=self.text_title())
        self.mensage.config(text=self.text_message_cycle())

    def verify_custom_option(self, value):
        if value == 6:                          # Se a técnica selecionada for "Pomodoro Flexível"
            self.fill_entry_values()
            self.show_custom_entries()          # Mostra os campos de entrada
        else:
            self.hide_custom_entries()          # Oculta os campos de entrada

    def on_option_change_wrapper(self):
        self.on_option_change
        self.pomodoro.set_option_values
        self.stop_timer_interface()

     # Funções que chamam os métodos em PomodoroTimer
    def text_message_cycle(self):
        return self.pomodoro.mensage_cycle

    def text_title(self):
        return self.pomodoro.title

    def show_description(self):
        option = self.select_option.get()
        self.pomodoro.set_timer(option)
        description = self.pomodoro.description
        messagebox.showinfo("Descrição: ", description) 

    def start_timer_interface(self,):
        if not self.pomodoro.timer_running and self.pomodoro.current_time != 0:  # Inicia o cronômetro apenas se não estiver rodando
            if self.current_value == 6 :
                self.fill_entry_values()
            self.pomodoro.start_timer()
            self.update_timer_display()

    def fill_entry_values(self):
         self.update_timer_display()
         self.pomodoro.set_option_values(
            int(self.work_time_entry.get()),
            int(self.shor_break_entry.get()),
            int(self.long_break_entry.get()),
            int(self.cycles_entry.get())
        )

    def pause_timer_interface(self):
        self.pomodoro.pause_timer()

    def stop_timer_interface(self):
        self.pomodoro.stop_timer()
        self.update_timer_display()

    def update_timer_display(self):
        self.reset_display_interface()
        self.mensage.config(text=self.text_message_cycle())

        if  self.pomodoro.timer_running:
                self.root.after(1000, self.update_timer_display)         # Chama novamente após 1 segundo
                self.pomodoro.update_timer()

    def reset_display_interface(self):
        self.time_display.config(text=self.pomodoro.format_time(self.pomodoro.current_time))
        self.title.config(text=self.text_title())

# Criação da janela principal e execução do aplicativo
root = tk.Tk()
app = MainInterfaceWindow(root)
root.mainloop()