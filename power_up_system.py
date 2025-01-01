import pygame
import random
import math
from constants import POWERUP_IMAGES, SOUND_EFFECTS, GAME_CONSTANTS

class PowerUpManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.power_ups = []
        self.active_effects = {}
        
        # Joker görselleri
        self.images = {}
        for name, path in POWERUP_IMAGES.items():
            try:
                self.images[name] = pygame.image.load(path)
            except Exception as e:
                print(f"Joker görseli yüklenemedi ({path}): {e}")
                
        # Ses efektleri
        self.sounds = {}
        for name, path in SOUND_EFFECTS.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Ses efekti yüklenemedi ({path}): {e}")
                
    def spawn_powerup(self, x, y):
        """Yeni bir joker oluştur"""
        power_up_types = ["multi_ball", "sticky", "big_paddle", "laser", "small_ball", "shield"]
        power_up_type = random.choice(power_up_types)
        
        power_up = {
            "type": power_up_type,
            "rect": pygame.Rect(x, y, 30, 30),
            "speed": 3,
            "image": self.images.get(power_up_type)
        }
        self.power_ups.append(power_up)
        
    def update(self, platform, ball):
        """Jokerleri güncelle"""
        # Düşen jokerleri güncelle
        for power_up in self.power_ups[:]:
            power_up["rect"].y += power_up["speed"]
            
            # Platform ile çarpışma kontrolü
            if power_up["rect"].colliderect(platform.rect):
                self.apply_effect(power_up["type"], platform, ball)
                self.power_ups.remove(power_up)
                continue
                
            # Ekrandan çıkan jokerleri temizle
            if power_up["rect"].top > self.screen_height:
                self.power_ups.remove(power_up)
                
        # Aktif efektleri güncelle
        current_time = pygame.time.get_ticks()
        for effect_type, effect_data in list(self.active_effects.items()):
            if current_time > effect_data["end_time"]:
                self.remove_effect(effect_type, platform, ball)
                
    def apply_effect(self, effect_type, platform, ball):
        """Joker efektini uygula"""
        current_time = pygame.time.get_ticks()
        duration = GAME_CONSTANTS["POWER_UP_DURATION"]
        
        # Ses efektini çal
        if effect_type in self.sounds:
            self.sounds[effect_type].play()
            
        if effect_type == "multi_ball":
            self.create_multi_balls(ball)
        elif effect_type == "sticky":
            platform.sticky = True
            self.active_effects["sticky"] = {
                "end_time": current_time + duration
            }
        elif effect_type == "big_paddle":
            platform.width *= 1.5
            platform.rect.width = platform.width
            platform.scale_images()
            self.active_effects["big_paddle"] = {
                "end_time": current_time + duration
            }
        elif effect_type == "laser":
            platform.has_laser = True
            self.active_effects["laser"] = {
                "end_time": current_time + duration
            }
        elif effect_type == "small_ball":
            ball.set_size(0.7)  # Top boyutunu %70'e düşür
            self.active_effects["small_ball"] = {
                "end_time": current_time + duration
            }
        elif effect_type == "shield":
            platform.has_shield = True
            self.active_effects["shield"] = {
                "end_time": current_time + duration
            }
            
    def remove_effect(self, effect_type, platform, ball):
        """Joker efektini kaldır"""
        if effect_type == "sticky":
            platform.sticky = False
            platform.sticky_ball = None
        elif effect_type == "big_paddle":
            platform.width = platform.original_width
            platform.rect.width = platform.width
            platform.scale_images()
        elif effect_type == "laser":
            platform.has_laser = False
            platform.lasers.clear()
        elif effect_type == "small_ball":
            ball.set_size(1.0)  # Normal boyuta döndür
        elif effect_type == "shield":
            platform.has_shield = False
            
        if effect_type in self.active_effects:
            del self.active_effects[effect_type]
            
    def create_multi_balls(self, original_ball):
        """Çoklu top oluştur"""
        new_balls = []
        angles = [-30, 30]  # Yeni topların açıları
        
        for angle in angles:
            new_ball = original_ball.copy()
            speed = math.sqrt(new_ball.physics.velocity_x**2 + new_ball.physics.velocity_y**2)
            
            new_ball.physics.velocity_x = math.cos(math.radians(angle)) * speed
            new_ball.physics.velocity_y = -abs(math.sin(math.radians(angle)) * speed)
            new_ball.active = True
            new_balls.append(new_ball)
            
        return new_balls
        
    def draw(self, screen):
        """Jokerleri çiz"""
        for power_up in self.power_ups:
            if power_up["image"]:
                screen.blit(power_up["image"], power_up["rect"]) 