import pygame
import random
from constants import LEVEL_DESIGNS, GAME_CONSTANTS
from error_handler import GameErrorHandler

class LevelSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level = 1
        self.error_handler = GameErrorHandler()
        
        # Level assetlerini yükle
        self.assets = {}
        for level, paths in LEVEL_DESIGNS.items():
            self.assets[level] = {}
            for asset_type, path in paths.items():
                try:
                    if asset_type.endswith("_sound"):
                        self.assets[level][asset_type] = pygame.mixer.Sound(path)
                    else:
                        image = pygame.image.load(path)
                        if asset_type == "background":
                            image = pygame.transform.scale(image, (screen_width, screen_height))
                        elif "block" in asset_type:
                            image = pygame.transform.scale(image, (60, 20))
                        self.assets[level][asset_type] = image
                except Exception as e:
                    self.error_handler.handle_asset_error(path, e)
                    
    def create_level(self, block_manager):
        """Mevcut seviyeyi oluştur"""
        block_manager.blocks.clear()
        
        if self.current_level == 1:
            self._create_level_one(block_manager)
        elif self.current_level == 2:
            self._create_level_two(block_manager)
        elif self.current_level == 3:
            self._create_level_three(block_manager)
            
    def _create_level_one(self, block_manager):
        """1. seviye tasarımı"""
        rows = 5
        cols = 8
        block_width = GAME_CONSTANTS["BLOCK_WIDTH"]
        block_height = GAME_CONSTANTS["BLOCK_HEIGHT"]
        padding = GAME_CONSTANTS["BLOCK_PADDING"]
        start_x = (self.screen_width - (cols * (block_width + padding))) // 2
        start_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (block_width + padding)
                y = start_y + row * (block_height + padding)
                
                # Blok türünü belirle
                if row < 2:
                    block_type = "normal"
                    image = self.assets[1]["single_hit_block"]
                else:
                    block_type = "hard"
                    image = self.assets[1]["double_hit_block"]
                    
                # Power-up şansını belirle
                power_up_chance = 0.2 if row == rows-1 else 0.1
                    
                block_manager.create_block(x, y, block_type, power_up_chance, image)
                
    def _create_level_two(self, block_manager):
        """2. seviye tasarımı"""
        rows = 6
        cols = 10
        block_width = GAME_CONSTANTS["BLOCK_WIDTH"]
        block_height = GAME_CONSTANTS["BLOCK_HEIGHT"]
        padding = GAME_CONSTANTS["BLOCK_PADDING"]
        start_x = (self.screen_width - (cols * (block_width + padding))) // 2
        start_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (block_width + padding)
                y = start_y + row * (block_height + padding)
                
                # Blok türünü belirle
                if row % 2 == 0:
                    block_type = "normal"
                    image = self.assets[2]["single_hit_block"]
                else:
                    block_type = "hard"
                    image = self.assets[2]["double_hit_block"]
                    
                # Bazı blokları hareketli yap
                if row == 3 and col % 3 == 0:
                    block_type = "moving"
                    
                # Power-up şansını belirle
                power_up_chance = 0.3 if row == rows-1 else 0.2
                    
                block_manager.create_block(x, y, block_type, power_up_chance, image)
                
    def _create_level_three(self, block_manager):
        """3. seviye tasarımı"""
        # Normal bloklar
        rows = 4
        cols = 12
        block_width = GAME_CONSTANTS["BLOCK_WIDTH"]
        block_height = GAME_CONSTANTS["BLOCK_HEIGHT"]
        padding = GAME_CONSTANTS["BLOCK_PADDING"]
        start_x = (self.screen_width - (cols * (block_width + padding))) // 2
        start_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (block_width + padding)
                y = start_y + row * (block_height + padding)
                
                # Blok türünü belirle
                if col % 3 == 0:
                    block_type = "explosive"
                    image = self.assets[3]["single_hit_block"]
                elif row % 2 == 0:
                    block_type = "normal"
                    image = self.assets[3]["single_hit_block"]
                else:
                    block_type = "hard"
                    image = self.assets[3]["double_hit_block"]
                    
                # Power-up şansını belirle
                power_up_chance = 0.4 if row == rows-1 else 0.3
                    
                block_manager.create_block(x, y, block_type, power_up_chance, image)
                
        # Boss bloğu
        boss_width = GAME_CONSTANTS["BOSS_WIDTH"]
        boss_height = GAME_CONSTANTS["BOSS_HEIGHT"]
        boss_x = (self.screen_width - boss_width) // 2
        boss_y = start_y + rows * (block_height + padding) + 30
        
        boss_block = {
            "rect": pygame.Rect(boss_x, boss_y, boss_width, boss_height),
            "image": pygame.transform.scale(self.assets[3]["boss"], (boss_width, boss_height)),
            "hits": 0,
            "max_hits": GAME_CONSTANTS["BOSS_MAX_HITS"]
        }
        block_manager.blocks.append(boss_block)
        
    def get_background(self):
        """Mevcut seviyenin arka plan görselini döndür"""
        return self.assets.get(self.current_level, {}).get("background")
        
    def get_platform_image(self, is_sticky=False):
        """Mevcut seviyenin platform görselini döndür"""
        if is_sticky:
            return self.assets.get(self.current_level, {}).get("sticky_platform")
        return self.assets.get(self.current_level, {}).get("platform")
        
    def get_break_sound(self):
        """Mevcut seviyenin blok kırılma sesini döndür"""
        return self.assets.get(self.current_level, {}).get("break_sound")
        
    def next_level(self):
        """Sonraki seviyeye geç"""
        if self.current_level < 3:
            self.current_level += 1
            return True
        return False
        
    def is_level_complete(self, block_manager):
        """Seviyenin tamamlanıp tamamlanmadığını kontrol et"""
        # Son seviyede boss bloğu kontrolü
        if self.current_level == 3:
            for block in block_manager.blocks:
                if isinstance(block, dict) and block.get("hits", 0) < block.get("max_hits", 10):
                    return False
                    
        # Normal blokları kontrol et (indestructible bloklar hariç)
        remaining_blocks = [block for block in block_manager.blocks 
                          if not isinstance(block, dict) and block.block_type != "indestructible"]
        return len(remaining_blocks) == 0 