import pygame
import random
import math

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.active_effects = {}
        self.fall_speed = 3
        
        # Power-up türleri ve özellikleri
        self.power_up_types = {
            "big_paddle": {
                "color": (46, 204, 113),  # Yeşil
                "duration": 10000,  # 10 saniye
                "icon": "↔",
                "description": "Büyük Raket"
            },
            "small_ball": {
                "color": (241, 196, 15),  # Sarı
                "duration": 8000,  # 8 saniye
                "icon": "○",
                "description": "Küçük Top"
            },
            "multi_ball": {
                "color": (155, 89, 182),  # Mor
                "duration": 15000,  # 15 saniye
                "icon": "⚈",
                "description": "Çoklu Top"
            },
            "laser": {
                "color": (231, 76, 60),  # Kırmızı
                "duration": 12000,  # 12 saniye
                "icon": "↯",
                "description": "Lazer"
            },
            "sticky": {
                "color": (52, 152, 219),  # Mavi
                "duration": 10000,  # 10 saniye
                "icon": "≡",
                "description": "Yapışkan Raket"
            },
            "shield": {
                "color": (230, 126, 34),  # Turuncu
                "duration": 8000,  # 8 saniye
                "icon": "⚡",
                "description": "Kalkan"
            }
        }
        
    def spawn_powerup(self, x, y):
        power_up_type = random.choice(list(self.power_up_types.keys()))
        power_up = {
            "rect": pygame.Rect(x, y, 30, 30),
            "type": power_up_type,
            "color": self.power_up_types[power_up_type]["color"],
            "creation_time": pygame.time.get_ticks()
        }
        self.power_ups.append(power_up)
        
    def update(self, platform, ball):
        current_time = pygame.time.get_ticks()
        
        # Power-up'ları güncelle
        for power_up in self.power_ups[:]:
            power_up["rect"].y += self.fall_speed
            
            # Platform ile çarpışma kontrolü
            if power_up["rect"].colliderect(platform.rect):
                self.activate_power_up(power_up["type"], platform, ball)
                self.power_ups.remove(power_up)
            
            # Ekrandan çıktı mı kontrolü
            elif power_up["rect"].top > platform.screen_height:
                self.power_ups.remove(power_up)
                
        # Aktif efektleri güncelle
        for power_type in list(self.active_effects.keys()):
            if current_time > self.active_effects[power_type]["end_time"]:
                self.deactivate_power_up(power_type, platform, ball)
                
    def activate_power_up(self, power_type, platform, ball):
        current_time = pygame.time.get_ticks()
        duration = self.power_up_types[power_type]["duration"]
        
        # Önceki aynı türdeki efekti kaldır
        if power_type in self.active_effects:
            self.deactivate_power_up(power_type, platform, ball)
            
        # Yeni efekti uygula
        if power_type == "big_paddle":
            platform.width *= 1.5
            platform.rect.width = platform.width
        elif power_type == "small_ball":
            ball.radius *= 0.7
        elif power_type == "multi_ball":
            # Yeni toplar ekle (ana oyun döngüsünde işlenecek)
            pass
        elif power_type == "laser":
            platform.has_laser = True
        elif power_type == "sticky":
            platform.sticky = True
        elif power_type == "shield":
            platform.has_shield = True
            
        # Efekti aktif efektlere ekle
        self.active_effects[power_type] = {
            "end_time": current_time + duration,
            "start_time": current_time
        }
        
    def deactivate_power_up(self, power_type, platform, ball):
        if power_type == "big_paddle":
            platform.width = platform.original_width
            platform.rect.width = platform.width
        elif power_type == "small_ball":
            ball.radius = ball.original_radius
        elif power_type == "multi_ball":
            # Ana oyun döngüsünde işlenecek
            pass
        elif power_type == "laser":
            platform.has_laser = False
        elif power_type == "sticky":
            platform.sticky = False
        elif power_type == "shield":
            platform.has_shield = False
            
        if power_type in self.active_effects:
            del self.active_effects[power_type]
            
    def draw(self, screen):
        # Power-up'ları çiz
        for power_up in self.power_ups:
            pygame.draw.rect(screen, power_up["color"], power_up["rect"], border_radius=5)
            # İkon çiz
            font = pygame.font.Font(None, 24)
            icon = font.render(self.power_up_types[power_up["type"]]["icon"], True, (255, 255, 255))
            icon_rect = icon.get_rect(center=power_up["rect"].center)
            screen.blit(icon, icon_rect)
            
        # Aktif efektleri göster
        y_offset = 50
        font = pygame.font.Font(None, 24)
        current_time = pygame.time.get_ticks()
        
        for power_type, effect_data in self.active_effects.items():
            remaining_time = (effect_data["end_time"] - current_time) / 1000  # saniye
            power_info = self.power_up_types[power_type]
            
            # Efekt bilgisi
            text = f"{power_info['description']}: {remaining_time:.1f}s"
            text_surface = font.render(text, True, power_info["color"])
            screen.blit(text_surface, (10, y_offset))
            
            # İlerleme çubuğu
            progress = (effect_data["end_time"] - current_time) / power_info["duration"]
            bar_width = 100
            bar_height = 5
            pygame.draw.rect(screen, (100, 100, 100), (120, y_offset + 8, bar_width, bar_height))
            pygame.draw.rect(screen, power_info["color"], 
                           (120, y_offset + 8, int(bar_width * progress), bar_height))
            
            y_offset += 30 