import pygame
from game_objects import Platform, Ball, BlockManager
from power_up_system import PowerUpManager
from constants import SOUND_EFFECTS

class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0
        self.combo = 0
        self.last_hit_time = 0
        self.combo_timeout = 2000  # 2 saniye
        
        # Ses efektlerini yükle
        try:
            self.hit_sound = pygame.mixer.Sound(SOUND_EFFECTS["hit"])
            self.score_sound = pygame.mixer.Sound(SOUND_EFFECTS["score"])
        except Exception as e:
            print(f"Ses efekti yüklenemedi: {e}")
            self.hit_sound = None
            self.score_sound = None
        
    def check_collisions(self, ball, platform, block_manager, power_up_manager):
        # Duvar çarpışmaları
        if ball.x - ball.radius <= 0:
            ball.x = ball.radius
            ball.physics.velocity_x = abs(ball.physics.velocity_x)
            if self.hit_sound:
                self.hit_sound.play()
        elif ball.x + ball.radius >= self.screen_width:
            ball.x = self.screen_width - ball.radius
            ball.physics.velocity_x = -abs(ball.physics.velocity_x)
            if self.hit_sound:
                self.hit_sound.play()
            
        if ball.y - ball.radius <= 0:
            ball.y = ball.radius
            ball.physics.velocity_y = abs(ball.physics.velocity_y)
            if self.hit_sound:
                self.hit_sound.play()
            
        # Platform çarpışması
        platform_rect = platform.rect.inflate(-10, -5)  # Daha hassas çarpışma için
        ball_rect = ball.rect
                              
        if platform_rect.colliderect(ball_rect):
            # Yapışkan platform kontrolü
            if platform.sticky:
                platform.attach_ball(ball)
            else:
                # Çarpışma açısını hesapla
                relative_x = (ball.x - (platform.rect.x + platform.rect.width/2)) / (platform.rect.width/2)
                ball.bounce(relative_x)
                ball.y = platform.rect.y - ball.radius  # Topun platformun içine girmesini önle
                if self.hit_sound:
                    self.hit_sound.play()
            
        # Blok çarpışmaları
        blocks_to_remove = []
        for block in block_manager.blocks:
            # Lazer çarpışması
            if platform.has_laser:
                for laser in platform.lasers[:]:
                    if isinstance(block, dict):  # Boss bloğu kontrolü
                        if laser["rect"].colliderect(block["rect"]):
                            block["hits"] += 1
                            if block["hits"] >= block["max_hits"]:
                                blocks_to_remove.append(block)
                            platform.lasers.remove(laser)
                            break
                    else:
                        if laser["rect"].colliderect(block.rect):
                            if block.hit():
                                if hasattr(block, 'contains_powerup') and block.contains_powerup:
                                    power_up_manager.spawn_powerup(
                                        block.rect.centerx,
                                        block.rect.centery
                                    )
                                blocks_to_remove.append(block)
                                self.score += block.points * (1 + self.combo * 0.1)
                                self.combo += 1
                                if self.score_sound:
                                    self.score_sound.play()
                            platform.lasers.remove(laser)
                            break
            
            # Top çarpışması
            if isinstance(block, dict):  # Boss bloğu kontrolü
                if ball_rect.colliderect(block["rect"]):
                    block["hits"] += 1
                    if block["hits"] >= block["max_hits"]:
                        blocks_to_remove.append(block)
                    ball.physics.velocity_y = -abs(ball.physics.velocity_y)
                    if self.hit_sound:
                        self.hit_sound.play()
                continue
                
            if ball_rect.colliderect(block.rect):
                # Çarpışma yönünü belirle
                dx = ball.x - block.rect.centerx
                dy = ball.y - block.rect.centery
                
                if abs(dx/block.rect.width) > abs(dy/block.rect.height):
                    ball.physics.velocity_x = abs(ball.physics.velocity_x) if dx > 0 else -abs(ball.physics.velocity_x)
                else:
                    ball.physics.velocity_y = abs(ball.physics.velocity_y) if dy > 0 else -abs(ball.physics.velocity_y)
                
                # Bloğu vur
                if ball.strong or block.hit():
                    if hasattr(block, 'contains_powerup') and block.contains_powerup:
                        power_up_manager.spawn_powerup(
                            block.rect.centerx,
                            block.rect.centery
                        )
                    blocks_to_remove.append(block)
                    self.score += block.points * (1 + self.combo * 0.1)
                    self.combo += 1
                    if self.score_sound:
                        self.score_sound.play()
                break
                
        # Blokları kaldır ve skoru güncelle
        for block in blocks_to_remove:
            if block in block_manager.blocks:
                block_manager.blocks.remove(block)
                
        # Combo süresini kontrol et
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.combo_timeout:
            self.combo = 0
        self.last_hit_time = current_time
        
        return self.score
        
    def update_score(self, points):
        self.score += points
        return self.score 