import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "sound": {
                "master_volume": 1.0,
                "music_volume": 0.7,
                "effects_volume": 0.8
            },
            "theme": {
                "current_theme": "classic",
                "racket_color": (255, 255, 255),
                "ball_color": (255, 0, 0)
            },
            "controls": {
                "up_key": "UP",
                "down_key": "DOWN",
                "sensitivity": 1.0
            }
        }
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = self.default_settings
            self.save_settings()
    
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4) 