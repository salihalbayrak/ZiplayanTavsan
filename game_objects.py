import pygame
import math
import random

class Platform:
    def __init__(self, screen_width, screen_height):
        # Platform boyutları
        self.width = 100
        self.height = 20
        self.original_width = self.width
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Platform pozisyonu
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 40
        
        # Platform özellikleri
        self.speed = 8
        self.color = (52, 152, 219)  # Mavi
        self.sticky = False  # Yapışkan platform power-up'ı için
        self.has_laser = False  # Lazer power-up'ı için
        self.has_shield = False  # Kalkan power-up'ı için
        self.laser_cooldown = 500  # Lazer atış hızı (ms)
        self.last_laser_time = 0
        self.lasers = []  # Aktif lazerler
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def move(self, direction, screen_width):
        if direction == "left":
            self.x = max(0, self.x - self.speed)
        elif direction == "right":
            self.x = min(screen_width - self.width, self.x + self.speed)
        self.rect.x = self.x
        
    def shoot_laser(self):
        current_time = pygame.time.get_ticks()
        if self.has_laser and current_time - self.last_laser_time > self.laser_cooldown:
            laser = {
                "rect": pygame.Rect(self.rect.centerx - 2, self.rect.top, 4, 10),
                "color": (231, 76, 60)  # Kırmızı
            }
            self.lasers.append(laser)
            self.last_laser_time = current_time
            
    def update_lasers(self):
        # Lazerleri yukarı hareket ettir
        laser_speed = 10
        for laser in self.lasers[:]:
            laser["rect"].y -= laser_speed
            if laser["rect"].bottom < 0:
                self.lasers.remove(laser)
        
    def draw(self, screen):
        # Platform çizimi
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        
        # Yapışkan platform efekti
        if self.sticky:
            pygame.draw.rect(screen, (46, 204, 113), 
                           (self.rect.x, self.rect.y, self.rect.width, 5))
                           
        # Kalkan efekti
        if self.has_shield:
            shield_height = 5
            shield_color = (230, 126, 34)  # Turuncu
            shield_rect = pygame.Rect(self.rect.x, self.rect.bottom,
                                    self.rect.width, shield_height)
            pygame.draw.rect(screen, shield_color, shield_rect)
            
        # Lazer efekti
        if self.has_laser:
            laser_indicator = pygame.Rect(self.rect.centerx - 3,
                                        self.rect.top - 5, 6, 5)
            pygame.draw.rect(screen, (231, 76, 60), laser_indicator)
            
        # Aktif lazerleri çiz
        for laser in self.lasers:
            pygame.draw.rect(screen, laser["color"], laser["rect"])

    def reset(self):
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height - 40
        self.width = self.original_width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sticky = False
        self.has_laser = False
        self.has_shield = False
        self.lasers.clear()

class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 8
        self.original_radius = self.radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Top pozisyonu
        self.x = screen_width // 2
        self.y = screen_height - 60
        
        # Top hızı ve açısı
        self.speed = 7
        self.original_speed = self.speed
        self.angle = -math.pi / 4  # 45 derece
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        
        self.color = (231, 76, 60)  # Kırmızı
        self.active = False  # Top harekette mi?
        self.strong = False  # Güçlü top power-up'ı
        
    def move(self):
        if self.active:
            self.x += self.dx
            self.y += self.dy
            
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.strong:
            pygame.draw.circle(screen, (241, 196, 15), 
                             (int(self.x), int(self.y)), self.radius - 2)
            
    def attach_to_platform(self, platform):
        self.x = platform.x + platform.width // 2
        self.y = platform.y - self.radius
        
    def launch(self):
        self.active = True
        # Başlangıç açısını ve hızını ayarla
        self.angle = -math.pi / 4  # 45 derece
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

    def bounce(self, relative_x):
        angle = relative_x * math.pi/3  # -60 ile 60 derece arası
        self.dx = math.cos(angle) * self.speed
        self.dy = -math.sin(angle) * self.speed

    def reset(self):
        self.active = False
        self.x = self.screen_width // 2
        self.y = self.screen_height - 60
        self.dx = math.cos(-math.pi/4) * self.speed
        self.dy = math.sin(-math.pi/4) * self.speed

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
        
    def create_block(self, x, y, block_type, powerup_chance):
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
        block.color = colors.get(block_type, (52, 152, 219))  # Varsayılan mavi
        block.hits_required = hits_required.get(block_type, 1)
        
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
            block.draw(screen)
            
    def get_remaining_blocks(self):
        return len(self.blocks) 