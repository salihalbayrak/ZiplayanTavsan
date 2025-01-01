import pygame
import math
import random
from constants import GAME_CONSTANTS

class BallPhysics:
    def __init__(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = GAME_CONSTANTS["BALL_SPEED"]
        self.original_speed = self.speed
        self.size_multiplier = 1.0
        
    def initialize_random_direction(self):
        """Rastgele başlangıç açısı (30° ile 150° arası)"""
        angle = math.radians(random.uniform(
            GAME_CONSTANTS["BALL_MIN_ANGLE"],
            GAME_CONSTANTS["BALL_MAX_ANGLE"]
        ))
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = -self.speed * math.sin(angle)
        
    def update_velocity(self, collision_normal):
        """Çarpışma sonrası hızı güncelle"""
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        dot_product = self.velocity_x * collision_normal[0] + self.velocity_y * collision_normal[1]
        
        # Yansıma vektörünü hesapla
        self.velocity_x = self.velocity_x - 2 * dot_product * collision_normal[0]
        self.velocity_y = self.velocity_y - 2 * dot_product * collision_normal[1]
        
        # Hızı normalize et ve orijinal hızı koru
        current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        self.velocity_x = (self.velocity_x / current_speed) * speed
        self.velocity_y = (self.velocity_y / current_speed) * speed
        
        # Minimum dikey hız kontrolü
        min_vertical_speed = speed * GAME_CONSTANTS["MIN_VERTICAL_SPEED_RATIO"]
        if abs(self.velocity_y) < min_vertical_speed:
            self.velocity_y = math.copysign(min_vertical_speed, self.velocity_y)
            # Hız vektörünü tekrar normalize et
            current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            self.velocity_x = (self.velocity_x / current_speed) * speed
            self.velocity_y = (self.velocity_y / current_speed) * speed
        
    def set_size(self, multiplier):
        """Top boyutunu ve hızını ayarla"""
        self.size_multiplier = multiplier
        # Boyut küçüldükçe hız artar
        speed_multiplier = GAME_CONSTANTS["BALL_SPEED_MULTIPLIER"] / multiplier
        self.speed = self.original_speed * speed_multiplier

class Controls:
    def __init__(self):
        self.left_keys = [pygame.K_LEFT, pygame.K_a]
        self.right_keys = [pygame.K_RIGHT, pygame.K_d]
        self.action_keys = [pygame.K_SPACE]
        self.speed = GAME_CONSTANTS["PLATFORM_SPEED"]
        
    def get_movement(self):
        """Hareket yönünü al"""
        keys = pygame.key.get_pressed()
        movement = 0
        
        # Sol hareket
        if any(keys[key] for key in self.left_keys):
            movement -= self.speed
            
        # Sağ hareket
        if any(keys[key] for key in self.right_keys):
            movement += self.speed
            
        return movement
        
    def is_action_pressed(self):
        """Aksiyon tuşuna basılıp basılmadığını kontrol et"""
        keys = pygame.key.get_pressed()
        return any(keys[key] for key in self.action_keys)
        
    def move(self, platform):
        """Platform hareketini yönet"""
        movement = self.get_movement()
        if movement != 0:
            platform.move(movement)

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.active = False
        self.duration = 10  # saniye
        self.start_time = 0
        
        # Güç-up türleri ve etkileri
        self.effects = {
            "big_paddle": 1.5,    # Raket boyutu çarpanı
            "small_ball": 0.7,    # Top boyutu çarpanı
            "slow_motion": 0.5,   # Hız çarpanı
            "multi_ball": 3,      # Top sayısı
            "shield": True        # Kalkan durumu
        }
        
    def apply_effect(self, game_objects):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
        if self.type == "big_paddle":
            game_objects["paddle"].height *= self.effects["big_paddle"]
        elif self.type == "small_ball":
            game_objects["ball"].width *= self.effects["small_ball"]
            game_objects["ball"].height *= self.effects["small_ball"]
        elif self.type == "slow_motion":
            game_objects["ball_speed"] *= self.effects["slow_motion"]
        elif self.type == "multi_ball":
            # Yeni toplar ekle
            for _ in range(self.effects["multi_ball"] - 1):
                new_ball = game_objects["ball"].copy()
                game_objects["balls"].append(new_ball)
        elif self.type == "shield":
            game_objects["shield_active"] = self.effects["shield"]
            
    def remove_effect(self, game_objects):
        self.active = False
        
        if self.type == "big_paddle":
            game_objects["paddle"].height /= self.effects["big_paddle"]
        elif self.type == "small_ball":
            game_objects["ball"].width /= self.effects["small_ball"]
            game_objects["ball"].height /= self.effects["small_ball"]
        elif self.type == "slow_motion":
            game_objects["ball_speed"] /= self.effects["slow_motion"]
        elif self.type == "multi_ball":
            game_objects["balls"] = [game_objects["balls"][0]]
        elif self.type == "shield":
            game_objects["shield_active"] = False

class DifficultyManager:
    def __init__(self):
        self.difficulties = {
            "easy": {
                "ball_speed": 5,
                "paddle_size": 1.2,
                "score_multiplier": 1,
                "powerup_frequency": 0.1,
                "obstacle_count": 0
            },
            "normal": {
                "ball_speed": 7,
                "paddle_size": 1.0,
                "score_multiplier": 1.5,
                "powerup_frequency": 0.05,
                "obstacle_count": 3
            },
            "hard": {
                "ball_speed": 10,
                "paddle_size": 0.8,
                "score_multiplier": 2,
                "powerup_frequency": 0.03,
                "obstacle_count": 5
            }
        }
        
    def apply_difficulty(self, difficulty, game_objects):
        settings = self.difficulties[difficulty]
        
        # Top hızını ayarla
        game_objects["ball_speed"] = settings["ball_speed"]
        
        # Raket boyutunu ayarla
        original_height = game_objects["paddle"].height
        game_objects["paddle"].height = original_height * settings["paddle_size"]
        
        # Engelleri ekle
        game_objects["obstacles"] = []
        for _ in range(settings["obstacle_count"]):
            obstacle = pygame.Rect(
                random.randint(100, 500),
                random.randint(100, 350),
                30, 30
            )
            game_objects["obstacles"].append(obstacle)
            
        return settings["score_multiplier"] 