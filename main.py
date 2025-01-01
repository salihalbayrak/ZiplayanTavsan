import pygame
import sys
from game_states import GameState, GameError
from game_objects import Platform, Ball
from game_mechanics import Controls
from power_up_system import PowerUpManager
from level_system import LevelSystem
from block_manager import BlockManager
from game_logic import GameLogic
from error_handler import GameErrorHandler
from constants import SOUND_EFFECTS

# Pygame başlat
pygame.init()
    pygame.mixer.init()

# Ekran ayarları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

# FPS sınırı
clock = pygame.time.Clock()
        
        # Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Oyun nesneleri
game_state = GameState()
error_handler = GameErrorHandler()
controls = Controls()
platform = Platform(screen_width, screen_height)
ball = Ball(screen_width, screen_height)
block_manager = BlockManager()
power_up_manager = PowerUpManager(screen_width, screen_height)
level_system = LevelSystem(screen_width, screen_height)
game_logic = GameLogic(screen_width, screen_height)

# Ses efektleri
sounds = {}
for name, path in SOUND_EFFECTS.items():
    try:
        sounds[name] = pygame.mixer.Sound(path)
except Exception as e:
        error_handler.handle_asset_error(path, e)

def draw_menu():
    """Menüyü çiz"""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    
    # Menü başlığı
    title = font.render("BREAKOUT", True, WHITE)
    title_rect = title.get_rect(center=(screen_width/2, screen_height/4))
    screen.blit(title, title_rect)
    
    # Menü seçenekleri
    options = ["Oyuna Başla", "Ayarlar", "Çıkış"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i*60))
        screen.blit(text, text_rect)
        
    pygame.display.flip()

def handle_menu_input(mouse_pos):
    """Menü girişlerini işle"""
    # Menü seçeneklerinin konumları
    options = {
        "start": pygame.Rect(screen_width/2 - 100, screen_height/2 - 20, 200, 40),
        "settings": pygame.Rect(screen_width/2 - 100, screen_height/2 + 40, 200, 40),
        "exit": pygame.Rect(screen_width/2 - 100, screen_height/2 + 100, 200, 40)
    }
    
    # Tıklanan seçeneği kontrol et
    if options["start"].collidepoint(mouse_pos):
        game_state.change_state("game")
        if "menu" in sounds:
            sounds["menu"].play()
    elif options["settings"].collidepoint(mouse_pos):
        game_state.change_state("settings")
    elif options["exit"].collidepoint(mouse_pos):
            return False
    return True

def handle_game_input():
    """Oyun girdilerini işle"""
    try:
        # Kontrol sınıfından hareket yönünü al
        movement = controls.get_movement()
        
        # Platform hareketini güncelle
        if movement != 0:
            platform.move(movement)
        
        # Aksiyon tuşu kontrolü
        if controls.is_action_pressed():
            # Top aktif değilse fırlat
            if not ball.active:
                ball.launch()
            # Top yapışıksa serbest bırak
            elif platform.sticky_ball:
                platform.release_ball()
            # Lazer varsa ateşle
            elif platform.has_laser:
                platform.shoot_laser()
                
    except Exception as e:
        raise GameError(f"Girdi işleme hatası: {str(e)}", "handle_game_input")

def game_loop():
    try:
        # FPS sınırı
        clock.tick(60)
        
        # Oyun durumu kontrolü
        if game_state.paused:
            return
            
        # Platform ve top kontrolü
        handle_game_input()
        
        # Top hareketi
        if ball.active:
            ball.move()
            
            # Top ekrandan çıktı mı?
            if ball.y > screen_height:
                game_state.lives -= 1
                if game_state.lives <= 0:
                    game_state.change_state("game_over")
                    if "game_over" in sounds:
                        sounds["game_over"].play()
                else:
        ball.reset()
        platform.reset()
        
        # Çarpışma kontrolü
        game_logic.check_collisions(ball, platform, block_manager, power_up_manager)
        
        # Power-up'ları güncelle
        power_up_manager.update(platform, ball)
        
        # Blokları güncelle
        block_manager.update()
        
        # Level tamamlandı mı?
        if level_system.is_level_complete(block_manager):
            if level_system.next_level():
                # Sonraki levele geç
                level_system.create_level(block_manager)
                ball.reset()
                platform.reset()
                platform.set_level(level_system.current_level)
                if "level_up" in sounds:
                    sounds["level_up"].play()
            else:
                # Oyun bitti
                game_state.change_state("victory")
                
        # Ekranı temizle
        screen.fill(BLACK)
        
        # Arka planı çiz
        background = level_system.get_background()
        if background:
            screen.blit(background, (0, 0))
        
        # Oyun nesnelerini çiz
        platform.draw(screen)
        ball.draw(screen)
        block_manager.draw(screen)
        power_up_manager.draw(screen)
        
        # Skor ve can gösterimi
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Skor: {game_state.score}", True, WHITE)
        lives_text = font.render(f"Can: {game_state.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen_width - 100, 10))
        
        # Ekranı güncelle
        pygame.display.flip()
        
    except Exception as e:
        raise GameError(f"Oyun döngüsünde hata: {str(e)}", "game_loop")

# Ana oyun döngüsü
running = True

while running:
    try:
        # Fare pozisyonunu al
        mouse_pos = pygame.mouse.get_pos()
        
        # Olayları kontrol et
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state.state == "game":
                        game_state.paused = not game_state.paused
                    else:
                        running = False
                elif event.key == pygame.K_m:
                    if game_state.state == "game":
                        game_state.change_state("menu")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.state == "menu":
                    running = handle_menu_input(mouse_pos)
        
        # Durum kontrolü
            if game_state.state == "menu":
            draw_menu()
        elif game_state.state == "game" and not game_state.paused:
            game_loop()
            
        # Ekranı güncelle
        pygame.display.flip()
        
    except Exception as e:
        error_handler.handle_error(e, game_state)

# Oyunu kapat
pygame.quit()
sys.exit()

