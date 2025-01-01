import pygame
import math
import random
from constants import LEVEL_DESIGNS, GAME_CONSTANTS, SOUND_EFFECTS

class Platform:
    def __init__(self, screen_width, screen_height):
        # Platform boyutları
        self.width = GAME_CONSTANTS["PLATFORM_WIDTH"]
        self.height = GAME_CONSTANTS["PLATFORM_HEIGHT"]
        self.original_width = self.width
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Platform pozisyonu
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 40
        
        # Platform özellikleri
        self.speed = GAME_CONSTANTS["PLATFORM_SPEED"]
        self.sticky = False
        self.has_laser = False
        self.has_shield = False
        self.laser_cooldown = GAME_CONSTANTS["LASER_COOLDOWN"]
        self.last_laser_time = 0
        self.lasers = []
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sticky_ball = None
        self.sticky_offset = 0
        
        # Görsel özellikler
        self.current_level = 1
        self.platform_images = {}
        self.sticky_images = {}
        
        # Görselleri yükle
        for level in [1, 2, 3]:
            try:
                self.platform_images[level] = pygame.image.load(LEVEL_DESIGNS[level]["platform"])
                self.sticky_images[level] = pygame.image.load(LEVEL_DESIGNS[level]["sticky_platform"])
            except Exception as e:
                print(f"Platform görseli yüklenemedi (Level {level}): {e}")
        
        # Görselleri ölçeklendir
        self.scale_images()
        
    def scale_images(self):
        """Platform görsellerini boyutlandır"""
        for level in [1, 2, 3]:
            if level in self.platform_images:
                self.platform_images[level] = pygame.transform.scale(
                    self.platform_images[level], (self.width, self.height))
            if level in self.sticky_images:
                self.sticky_images[level] = pygame.transform.scale(
                    self.sticky_images[level], (self.width, self.height))
        
    def move(self, movement):
        """Platform hareketini güncelle"""
        new_x = self.x + movement
        if 0 <= new_x <= self.screen_width - self.width:
            self.x = new_x
            self.rect.x = self.x
            
            # Yapışkan top varsa onu da hareket ettir
            if self.sticky_ball:
                self.sticky_ball.x = self.x + self.sticky_offset
        
    def shoot_laser(self):
        """Lazer ışını oluştur"""
        current_time = pygame.time.get_ticks()
        if self.has_laser and current_time - self.last_laser_time > self.laser_cooldown:
            try:
                laser_sound = pygame.mixer.Sound(SOUND_EFFECTS["laser"])
                laser_sound.play()
            except Exception as e:
                print(f"Lazer sesi yüklenemedi: {e}")
            
            # İki lazer ışını oluştur
            laser_width = 4
            laser_positions = [
                self.rect.left + self.rect.width * 0.25,
                self.rect.left + self.rect.width * 0.75
            ]
            
            for x in laser_positions:
                laser = {
                    "rect": pygame.Rect(x - laser_width/2, 0, laser_width, self.rect.top),
                    "color": (231, 76, 60)  # Kırmızı
                }
                self.lasers.append(laser)
            
            self.last_laser_time = current_time
            
    def update_lasers(self):
        """Lazerleri güncelle"""
        for laser in self.lasers[:]:
            laser["rect"].y -= 10
            if laser["rect"].bottom < 0:
                self.lasers.remove(laser)
        
    def draw(self, screen):
        """Platform ve efektleri çiz"""
        # Platform görselini çiz
        current_image = self.sticky_images[self.current_level] if self.sticky else self.platform_images[self.current_level]
        if current_image:
            screen.blit(current_image, self.rect)
        else:
            # Yedek olarak dikdörtgen çiz
            pygame.draw.rect(screen, (52, 152, 219), self.rect)
        
        # Kalkan efekti
        if self.has_shield:
            shield_height = 5
            shield_rect = pygame.Rect(self.rect.x, self.rect.bottom,
                                    self.rect.width, shield_height)
            pygame.draw.rect(screen, (230, 126, 34), shield_rect)
            
        # Lazer efekti
        if self.has_laser:
            for laser in self.lasers:
                pygame.draw.rect(screen, laser["color"], laser["rect"])
        
    def reset(self):
        """Platform'u başlangıç durumuna getir"""
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height - 40
        self.width = self.original_width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sticky = False
        self.has_laser = False
        self.has_shield = False
        self.lasers.clear()
        self.sticky_ball = None
        self.sticky_offset = 0
        self.scale_images()
        
    def set_level(self, level):
        """Platform görselini seviyeye göre güncelle"""
        self.current_level = level
        
    def set_sticky(self, is_sticky):
        """Yapışkan modu ayarla ve ses çal"""
        self.sticky = is_sticky
        if is_sticky:
            try:
                sticky_sound = pygame.mixer.Sound(SOUND_EFFECTS["sticky"])
                sticky_sound.play()
            except Exception as e:
                print(f"Yapışkan platform sesi yüklenemedi: {e}")
                
    def attach_ball(self, ball):
        """Topu platforma yapıştır"""
        if self.sticky:
            self.sticky_ball = ball
            self.sticky_offset = ball.x - self.x
            ball.attach_to_platform(self)
            
    def release_ball(self):
        """Yapışık topu serbest bırak"""
        if self.sticky_ball:
            self.sticky_ball.launch()
            self.sticky_ball = None
            self.sticky_offset = 0

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 8
        self.original_radius = self.radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Top pozisyonu
        self.x = screen_width // 2
        self.y = screen_height - 60
        
        # Fizik sistemi
        self.physics = BallPhysics()
        self.active = False
        self.strong = False
        
        # Görsel özellikler
        self.color = (231, 76, 60)  # Kırmızı
        
        # Çarpışma kutusu
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                              self.radius * 2, self.radius * 2)
        
    def move(self):
        if self.active:
            self.x += self.physics.velocity_x
            self.y += self.physics.velocity_y
            
            # Duvar çarpışmaları
            if self.x - self.radius <= 0:
                self.x = self.radius
                self.physics.velocity_x = abs(self.physics.velocity_x)
            elif self.x + self.radius >= self.screen_width:
                self.x = self.screen_width - self.radius
                self.physics.velocity_x = -abs(self.physics.velocity_x)
                
            if self.y - self.radius <= 0:
                self.y = self.radius
                self.physics.velocity_y = abs(self.physics.velocity_y)
                
            # Çarpışma kutusunu güncelle
            self.rect.center = (self.x, self.y)
                
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.strong:
            pygame.draw.circle(screen, (241, 196, 15), 
                             (int(self.x), int(self.y)), self.radius - 2)
                             
    def attach_to_platform(self, platform):
        """Topu platforma yapıştır"""
        self.x = platform.x + platform.sticky_offset
        self.y = platform.y - self.radius
        self.active = False
        self.rect.center = (self.x, self.y)
        
    def launch(self):
        """Topu fırlat"""
        self.active = True
        self.physics.initialize_random_direction()
        
    def bounce(self, relative_x):
        """Platform çarpışmasında topun yönünü değiştir"""
        angle = relative_x * math.pi/3  # -60° ile 60° arası
        speed = math.sqrt(self.physics.velocity_x**2 + self.physics.velocity_y**2)
        
        self.physics.velocity_x = math.cos(angle) * speed
        self.physics.velocity_y = -abs(math.sin(angle) * speed)
        
    def reset(self):
        """Topu başlangıç konumuna getir"""
        self.active = False
        self.x = self.screen_width // 2
        self.y = self.screen_height - 60
        self.physics = BallPhysics()
        self.radius = self.original_radius
        self.rect.center = (self.x, self.y)
        
    def set_size(self, scale):
        """Top boyutunu değiştir"""
        self.radius = self.original_radius * scale
        self.physics.set_size(scale)
        self.rect.width = self.radius * 2
        self.rect.height = self.radius * 2
        
    def copy(self):
        """Topun kopyasını oluştur"""
        new_ball = Ball(self.screen_width, self.screen_height)
        new_ball.x = self.x
        new_ball.y = self.y
        new_ball.radius = self.radius
        new_ball.active = True
        new_ball.physics = BallPhysics()
        new_ball.physics.speed = self.physics.speed
        return new_ball

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

class Block:
    def __init__(self, x, y, width, height, block_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.block_type = block_type
        self.original_x = x
        
        # Blok özellikleri
        self.current_hits = 0
        self.hits_required = 1  # Varsayılan değer, create_block'ta güncellenir
        self.contains_powerup = False
        self.points = self.get_points()
        
        # Hareket özellikleri
        self.moving = block_type == "moving"
        self.move_speed = 2
        self.move_direction = 1
        
        # Renk (varsayılan değer, create_block'ta güncellenir)
        self.color = (52, 152, 219)  # Mavi
        
    def get_points(self):
        points = {
            "normal": 10,
            "hard": 20,
            "explosive": 30,
            "multi_hit": 50,
            "power_up": 25,
            "mystery": 40,
            "indestructible": 0,
            "moving": 35
        }
        return points.get(self.block_type, 10)
        
    def hit(self):
        self.current_hits += 1
        # Renk değişimi efekti
        self.color = tuple(min(c + 30, 255) for c in self.color)
        
        # Özel blok efektleri
        if self.block_type == "explosive" and self.current_hits >= self.hits_required:
            return "explosive"
        elif self.block_type == "mystery" and self.current_hits >= self.hits_required:
            return "mystery"
            
        return self.current_hits >= self.hits_required
        
    def update(self):
        if self.moving:
            # Blok hareketini güncelle
            self.rect.x += self.move_speed * self.move_direction
            
            # Hareket sınırlarını kontrol et
            if abs(self.rect.x - self.original_x) > 50:  # 50 piksel hareket sınırı
                self.move_direction *= -1
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        
        # Blok türüne göre özel efektler
        if self.block_type == "hard" and self.current_hits < self.hits_required:
            pygame.draw.rect(screen, (44, 62, 80), self.rect, 2, border_radius=5)
            
        elif self.block_type == "multi_hit":
            # Kalan vuruş sayısını göster
            hits_left = self.hits_required - self.current_hits
            text = pygame.font.Font(None, 20).render(str(hits_left), True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
            
        elif self.block_type == "mystery":
            # Yanıp sönen soru işareti
            if (pygame.time.get_ticks() // 500) % 2:
                text = pygame.font.Font(None, 20).render("?", True, (255, 255, 255))
                text_rect = text.get_rect(center=self.rect.center)
                screen.blit(text, text_rect)

class BlockManager:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.blocks = []
        self.block_width = 60
        self.block_height = 20
        self.padding = 5
        
    def create_block(self, x, y, block_type, powerup_chance, image=None):
        # Blok türüne göre renk ve vuruş sayısı belirle
        colors = {
            "normal": (52, 152, 219),  # Mavi
            "hard": (46, 204, 113),    # Yeşil
            "explosive": (231, 76, 60), # Kırmızı
            "multi_hit": (155, 89, 182),# Mor
            "power_up": (241, 196, 15), # Sarı
            "mystery": (149, 165, 166), # Gri
            "indestructible": (44, 62, 80), # Koyu gri
            "moving": (230, 126, 34)    # Turuncu
        }
        
        hits_required = {
            "normal": 1,
            "hard": 2,
            "explosive": 1,
            "multi_hit": 3,
            "power_up": 1,
            "mystery": 1,
            "indestructible": float('inf'),
            "moving": 2
        }
        
        block = Block(x, y, self.block_width, self.block_height, block_type)
        block.color = colors.get(block_type, (52, 152, 219))
        block.hits_required = hits_required.get(block_type, 1)
        block.image = image
        
        if block_type != "indestructible" and random.random() < powerup_chance:
            block.contains_powerup = True
            
        self.blocks.append(block)
        
    def update(self):
        for block in self.blocks:
            block.update()
            
    def handle_explosive_block(self, exploded_block):
        # Patlayan bloğun etrafındaki blokları yok et
        explosion_radius = 100
        blocks_to_remove = []
        
        for block in self.blocks:
            if block != exploded_block:
                distance = math.sqrt(
                    (block.rect.centerx - exploded_block.rect.centerx) ** 2 +
                    (block.rect.centery - exploded_block.rect.centery) ** 2
                )
                if distance <= explosion_radius:
                    blocks_to_remove.append(block)
                    
        for block in blocks_to_remove:
            self.blocks.remove(block)
            
    def handle_mystery_block(self, mystery_block):
        # Rastgele bir efekt uygula
        effects = ["extra_points", "power_up", "clear_row"]
        effect = random.choice(effects)
        
        if effect == "extra_points":
            return {"type": "points", "value": 100}
        elif effect == "power_up":
            return {"type": "power_up", "value": True}
        elif effect == "clear_row":
            # Aynı satırdaki tüm blokları temizle
            row_y = mystery_block.rect.y
            blocks_to_remove = [b for b in self.blocks if b.rect.y == row_y]
            for block in blocks_to_remove:
                self.blocks.remove(block)
            return {"type": "points", "value": len(blocks_to_remove) * 20}
            
    def draw(self, screen):
        for block in self.blocks:
            if hasattr(block, 'image') and block.image:
                screen.blit(block.image, block.rect)
            else:
                block.draw(screen)
            
    def get_remaining_blocks(self):
        return len([b for b in self.blocks if not isinstance(b, dict)]) 