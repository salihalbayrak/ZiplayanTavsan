import pygame
from constants import GAME_CONSTANTS
import random

class Block:
    def __init__(self, x, y, block_type, power_up_chance, image=None):
        self.rect = pygame.Rect(x, y, GAME_CONSTANTS["BLOCK_WIDTH"], GAME_CONSTANTS["BLOCK_HEIGHT"])
        self.block_type = block_type
        self.power_up_chance = power_up_chance
        self.hits = 0
        self.max_hits = self.get_max_hits(block_type)
        self.image = image
        self.moving = block_type == "moving"
        self.move_direction = 1
        self.move_speed = 2
        self.original_x = x
        self.move_range = 100
        self.points = self.get_points()
        self.contains_powerup = False
        
    def get_max_hits(self, block_type):
        """Blok türüne göre maksimum vuruş sayısını belirle"""
        max_hits = {
            "normal": 1,
            "hard": 2,
            "explosive": 1,
            "moving": 2,
            "indestructible": float('inf'),
            "mystery": 1,
            "multi_hit": 3
        }
        return max_hits.get(block_type, 1)
        
    def get_points(self):
        """Blok türüne göre puan değerini belirle"""
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
        """Bloğa vuruş uygula"""
        if self.block_type != "indestructible":
            self.hits += 1
            # Özel blok efektleri
            if self.block_type == "explosive" and self.hits >= self.max_hits:
                return "explosive"
            elif self.block_type == "mystery" and self.hits >= self.max_hits:
                return "mystery"
            return self.hits >= self.max_hits
        return False
        
    def update(self):
        """Bloğu güncelle (hareket vb.)"""
        if self.moving:
            new_x = self.rect.x + (self.move_speed * self.move_direction)
            if abs(new_x - self.original_x) > self.move_range:
                self.move_direction *= -1
            else:
                self.rect.x = new_x
                
class BlockManager:
    def __init__(self):
        self.blocks = []
        
    def create_block(self, x, y, block_type, power_up_chance, image=None):
        """Yeni blok oluştur"""
        block = Block(x, y, block_type, power_up_chance, image)
        if block_type != "indestructible" and random.random() < power_up_chance:
            block.contains_powerup = True
        self.blocks.append(block)
        
    def update(self):
        """Tüm blokları güncelle"""
        for block in self.blocks:
            if isinstance(block, Block):
                block.update()
                
    def draw(self, screen):
        """Blokları çiz"""
        for block in self.blocks:
            if isinstance(block, Block):
                if block.image:
                    screen.blit(block.image, block.rect)
                else:
                    # Yedek olarak dikdörtgen çiz
                    color = self.get_block_color(block)
                    pygame.draw.rect(screen, color, block.rect)
                    
                    # Blok türüne göre özel efektler
                    if block.block_type == "hard" and block.hits < block.max_hits:
                        pygame.draw.rect(screen, (44, 62, 80), block.rect, 2)
                    elif block.block_type == "multi_hit":
                        hits_left = block.max_hits - block.hits
                        text = pygame.font.Font(None, 20).render(str(hits_left), True, (255, 255, 255))
                        text_rect = text.get_rect(center=block.rect.center)
                        screen.blit(text, text_rect)
                    elif block.block_type == "mystery":
                        if (pygame.time.get_ticks() // 500) % 2:
                            text = pygame.font.Font(None, 20).render("?", True, (255, 255, 255))
                            text_rect = text.get_rect(center=block.rect.center)
                            screen.blit(text, text_rect)
                            
            elif isinstance(block, dict):  # Boss bloğu
                screen.blit(block["image"], block["rect"])
                
    def get_block_color(self, block):
        """Blok türüne göre renk döndür"""
        colors = {
            "normal": (52, 152, 219),     # Mavi
            "hard": (231, 76, 60),        # Kırmızı
            "explosive": (241, 196, 15),   # Sarı
            "moving": (46, 204, 113),     # Yeşil
            "indestructible": (149, 165, 166),  # Gri
            "mystery": (155, 89, 182),     # Mor
            "multi_hit": (230, 126, 34)    # Turuncu
        }
        return colors.get(block.block_type, (255, 255, 255))  # Varsayılan beyaz
        
    def handle_collision(self, ball, level_system):
        """Top ile blok çarpışmalarını yönet"""
        for block in self.blocks[:]:  # Kopyasını al çünkü silme olabilir
            if isinstance(block, Block):
                if ball.rect.colliderect(block.rect):
                    # Çarpışma yönünü belirle
                    dx = ball.x - block.rect.centerx
                    dy = ball.y - block.rect.centery
                    
                    if abs(dx/block.rect.width) > abs(dy/block.rect.height):
                        ball.physics.velocity_x *= -1  # Yatay çarpışma
                    else:
                        ball.physics.velocity_y *= -1  # Dikey çarpışma
                        
                    # Bloğa vuruş uygula
                    hit_result = block.hit()
                    
                    # Özel blok efektleri
                    if hit_result == "explosive":
                        self.handle_explosive_block(block)
                        self.blocks.remove(block)
                        return True, block.power_up_chance
                    elif hit_result == "mystery":
                        self.handle_mystery_block(block)
                        self.blocks.remove(block)
                        return True, 1.0
                    elif hit_result is True:
                        # Blok kırılma sesi
                        break_sound = level_system.get_break_sound()
                        if break_sound:
                            break_sound.play()
                            
                        # Bloğu listeden çıkar
                        self.blocks.remove(block)
                        return True, block.power_up_chance
                        
            elif isinstance(block, dict):  # Boss bloğu
                if ball.rect.colliderect(block["rect"]):
                    ball.physics.velocity_y *= -1
                    block["hits"] += 1
                    if block["hits"] >= block["max_hits"]:
                        self.blocks.remove(block)
                        return True, 1.0  # Boss'u yenince kesin power-up düşür
                        
        return False, 0
        
    def handle_explosive_block(self, source_block):
        """Patlayıcı bloğun etrafındaki blokları patlat"""
        explosion_range = 100
        blocks_to_remove = []
        
        for block in self.blocks:
            if isinstance(block, Block) and block != source_block:
                dx = block.rect.centerx - source_block.rect.centerx
                dy = block.rect.centery - source_block.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                
                if distance <= explosion_range:
                    blocks_to_remove.append(block)
                    
        # Etkilenen blokları sil
        for block in blocks_to_remove:
            if block in self.blocks:
                self.blocks.remove(block)
                
    def handle_mystery_block(self, mystery_block):
        """Gizem bloğunun efektini uygula"""
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
            
    def get_remaining_blocks(self):
        """Kalan blok sayısını döndür"""
        return len([b for b in self.blocks if isinstance(b, Block) and b.block_type != "indestructible"]) 