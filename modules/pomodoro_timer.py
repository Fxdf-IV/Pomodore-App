import time
from block import WebsiteBlocker

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
        self.is_timer_running = False              # Controla o estado do timer (False = parado)
        self.current_time = self.work_duration     # Tempo atual (inicia com tempo de foco selecionado)
        self.cycle_message = "Foco total! É hora de trabalhar."

        self.block = WebsiteBlocker()
        self.sites = ["facebook.com", "x.com", "youtube.com"]
    
    def block_unblock_websites(self):
        if not self.is_focus_timer_active:
            self.block.unblock_websites(self.sites)

        else:
            self.block.clear_dns_cache()
            self.block.close_browser()
            time.sleep(1)
            self.block.block_websites(self.sites)
            self.block.start_browser()

    # Converte o tempo de segundos para o formato MM:SS.
    def format_time_to_display(self, total_seconds):
        minutes = total_seconds  // 60
        remaining_seconds = total_seconds  % 60
        return f"{minutes:02}:{remaining_seconds:02}"
    
    # Converte o tempo de segundos para o formato HH:MM:SS.
    def format_time_to_display_custom(self, total_seconds):
        hours = total_seconds // 3600  # Calcula as horas
        minutes = (total_seconds % 3600) // 60  # Calcula os minutos
        remaining_seconds = total_seconds % 60  # Calcula os segundos restantes
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"
    
    # Inicia o timer
    def start_timer(self):
        if not self.is_timer_running:
            self.is_timer_running = True
            self.update_timer()
            self.block_unblock_websites()
        
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
        self.block.unblock_websites(self.sites)
        self.cycle_message = "Foco total! É hora de trabalhar."
    
    # Atualiza o tempo restante a cada segundo e gerencia as trocas de ciclos.
    def update_timer(self):
        if self.is_timer_running:
            if self.current_time > 0 :
                self.current_time -= 1
            else:
                time.sleep(3)
                self.handle_cycle_switch()             # Quando o tempo termina, completa o ciclo de foco

    # Gerencia a mudança entre ciclos de pausas curtas e longas.
    def handle_cycle_switch(self):
        print("PAUSA CURTA INICIAL ", self.short_break_count)
        
        if     self.current_cycle == 1 :
                self.current_time = self.long_break_duration
                self.cycle_message = "Pausa longa! Descanse bem e recarregue suas energias."
                self.is_long_break_timer_active = True
                self.is_focus_timer_active = False
                self.is_short_break_timer_active = False          
                self.current_cycle = self.total_cycles + 1
                self.short_break_count = self.total_cycles
                print("PAUSA LONGA __________")

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

        self.block_unblock_websites()

    # Gerencia a mudança entre ciclos de foco.
    def start_focus_cycle(self):
        print("CICLO INICIAL ", self.current_cycle)
        if     self.is_short_break_timer_active == True or self.is_long_break_timer_active == True :
                self.current_time = self.work_duration
                self.cycle_message = "Foco total! É hora de trabalhar."                        
                self.is_short_break_timer_active = False
                self.is_long_break_timer_active = False
                self.is_focus_timer_active = True
                self.current_cycle -= 1
                print("Ciclo atual ", self.current_cycle)

    # Chama a entrada do usuário, e armazena os valores retornados
    def configure_timer_settings(self, work_duration, short_break_duration, long_break_duration, cycles_entry):
        self.work_duration = work_duration
        self.short_break_duration = short_break_duration
        self.long_break_duration = long_break_duration
        self.total_cycles = cycles_entry
    
    def timer_options(self, option):

        match option:
            case 1:
                self.title = "Pomodoro Clássico"
                self.work_duration = 2
                self.short_break_duration = 2
                self.long_break_duration = 2
                self.total_cycles = 4
                self.description = ("Esta é a abordagem original do método Pomodoro, que consiste em ciclos de 25 minutos de trabalho concentrado. A pausa curta de 5 minutos permite relaxar e recarregar as energias, enquanto a pausa longa, após quatro ciclos, oferece um tempo maior para descansar e refletir sobre o progresso feito, ajudando a evitar a fadiga mental. Tempo de foco: 01h40 (4 ciclos de 25 minutos). Tempo total de descanso: 00h40 (3 pausas curtas de 5 minutos + 1 pausa longa de 15 minutos).")

            case 2:
                self.title = "Pomodoro 60/15"
                self.work_duration = 1
                self.short_break_duration = 1
                self.long_break_duration = 1
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
                self.total_cycles = 0
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

