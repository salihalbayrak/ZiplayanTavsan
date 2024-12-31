import pygame
import json

class SettingsMenu:
    def __init__(self, screen, screen_width, screen_height, db):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.db = db
        
        # Fontlar ve renkler
        self.title_font = pygame.font.Font(None, int(0.08 * screen_height))
        self.text_font = pygame.font.Font(None, int(0.04 * screen_height))
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (52, 152, 219)
        self.green = (46, 204, 113)
        
        # Ayar kategorileri
        self.categories = ["Ses", "Görsel", "Kontroller"]
        self.current_category = 0
        
        # Aktif slider
        self.active_slider = None
        self.dragging = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Kategori değiştirme
            category_y = self.screen_height * 0.2
            for i, category in enumerate(self.categories):
                rect = pygame.Rect(
                    self.screen_width * (0.25 + i * 0.25) - 50,
                    category_y - 20,
                    100, 40
                )
                if rect.collidepoint(mouse_pos):
                    self.current_category = i
                    return True
                    
            # Slider kontrolü
            if self.current_category == 0:
                for i, (name, value) in enumerate(self.settings['sound'].items()):
                    slider_rect = pygame.Rect(
                        self.screen_width * 0.3,
                        self.screen_height * 0.3 + i * 80,
                        200, 10
                    )
                    if slider_rect.collidepoint(mouse_pos):
                        self.active_slider = name
                        self.dragging = True
                        return True
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                self.active_slider = None
                self.save_settings()
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.active_slider:
                mouse_x = event.pos[0]
                slider_x = self.screen_width * 0.3
                slider_width = 200
                value = (mouse_x - slider_x) / slider_width
                value = max(0, min(1, value))
                self.settings['sound'][self.active_slider] = value
                return True
                
        return False
        
    def save_settings(self):
        self.db.update_user_settings(self.current_user, self.settings)
        
    def load_settings(self, username):
        self.current_user = username
        settings = self.db.get_user_settings(username)
        if settings:
            self.settings = settings
        else:
            self.settings = {
                'sound': {
                    'master_volume': 1.0,
                    'music_volume': 0.7,
                    'effects_volume': 0.8
                },
                'theme': 'classic',
                'controls': {
                    'up': 'UP',
                    'down': 'DOWN',
                    'pause': 'P'
                }
            }
            self.save_settings() 