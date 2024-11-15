import json
import os

class SettingsManager:
    def __init__(self):
        self.settings = {
            'transition_time': 3,  # tempo entre ciclos (atualmente fixo em 3s)
            'show_cycle_count': True,  # mostrar contador de ciclos
            
            # Configurações de Sistema
            'close_browser': True,  # fechar navegador ao bloquear sites
            'auto_start_browser': True  # iniciar navegador após bloqueio
        }
        
        self.settings_file = "user_settings.json"
        self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as file:
                    saved_settings = json.load(file)
                    self.settings.update(saved_settings)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as file:
                json.dump(self.settings, file, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def get_setting(self, key):
        return self.settings.get(key)
    
    def update_setting(self, key, value):
        if key in self.settings:
            self.settings[key] = value
            return True
        return False
    
    def get_setting(self, key):
        return self.settings.get(key)
    
    def discard_changes(self):
        self.load_settings()