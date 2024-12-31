import pygame
from game_objects import Platform, Ball, BlockManager
from power_up_system import PowerUpManager

class GameLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0
        self.combo = 0
        self.last_hit_time = 0
        self.combo_timeout = 2000  # 2 saniye
        
    def check_collisions(self, ball, platform, block_manager, power_up_manager):
        # Duvar çarpışmaları
        if ball.x - ball.radius <= 0:
            ball.x = ball.radius
            ball.dx = abs(ball.dx)
            pygame.mixer.Sound("Assests/topsesi.mp3").play()
        elif ball.x + ball.radius >= self.screen_width:
            ball.x = self.screen_width - ball.radius
            ball.dx = -abs(ball.dx)
            pygame.mixer.Sound("Assests/topsesi.mp3").play()
            
        if ball.y - ball.radius <= 0:
            ball.y = ball.radius
            ball.dy = abs(ball.dy)
            pygame.mixer.Sound("Assests/topsesi.mp3").play()
            
        # Platform çarpışması
        platform_rect = platform.rect.inflate(-10, -5)  # Daha hassas çarpışma için
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius,
                              ball.radius * 2, ball.radius * 2)
                              
        if platform_rect.colliderect(ball_rect):
            # Çarpışma açısını hesapla
            relative_x = (ball.x - (platform.rect.x + platform.rect.width/2)) / (platform.rect.width/2)
            ball.bounce(relative_x)
            ball.y = platform.rect.y - ball.radius  # Topun platformun içine girmesini önle
            pygame.mixer.Sound("Assests/topsesi.mp3").play()
            
            # Yapışkan platform kontrolü
            if platform.sticky:
                ball.active = False
                ball.attach_to_platform(platform)
            
        # Blok çarpışmaları
        blocks_to_remove = []
        for block in block_manager.blocks:
            # Topun merkezi ve yarıçapı ile blok arasındaki çarpışma kontrolü
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius,
                                  ball.radius * 2, ball.radius * 2)
            
            if ball_rect.colliderect(block.rect):
                # Çarpışma yönünü belirle
                dx = ball.x - block.rect.centerx
                dy = ball.y - block.rect.centery
                
                if abs(dx/block.rect.width) > abs(dy/block.rect.height):
                    ball.dx = abs(ball.dx) if dx > 0 else -abs(ball.dx)
                else:
                    ball.dy = abs(ball.dy) if dy > 0 else -abs(ball.dy)
                
                # Bloğu vur
                if ball.strong or block.hit():
                    if block.contains_powerup:
                        power_up_manager.spawn_powerup(
                            block.rect.centerx,
                            block.rect.centery
                        )
                    blocks_to_remove.append(block)
                    self.score += block.points * (1 + self.combo * 0.1)
                    self.combo += 1
                    pygame.mixer.Sound("Assests/skorses.mp3").play()
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