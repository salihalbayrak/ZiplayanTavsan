import random

class LevelSystem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level = 1
        self.levels = {}
        self.create_levels()
        
    def create_levels(self):
        # Her seviye için blok düzenini oluştur
        for level in range(1, 11):  # 10 seviye
            self.levels[level] = {
                "block_count": 3 + level * 2,  # Her seviyede artan blok sayısı
                "hard_block_chance": min(0.1 * level, 0.5),  # Sert blok olasılığı (max %50)
                "special_block_chance": min(0.05 * level, 0.3),  # Özel blok olasılığı (max %30)
                "powerup_chance": min(0.2 + 0.02 * level, 0.4),  # Power-up düşme olasılığı (max %40)
                "ball_speed": min(5 + level * 0.5, 10),  # Top hızı (max 10)
                "points_multiplier": 1 + level * 0.1,  # Puan çarpanı
                "block_types": self.get_level_block_types(level)  # Seviyeye özel blok türleri
            }
            
    def get_level_block_types(self, level):
        # Temel blok türleri
        block_types = ["normal", "hard"]
        
        # Seviye 3'ten sonra özel bloklar ekle
        if level >= 3:
            block_types.extend(["explosive", "multi_hit"])
        
        # Seviye 5'ten sonra daha fazla özel blok
        if level >= 5:
            block_types.extend(["power_up", "mystery"])
            
        # Seviye 7'den sonra nadir bloklar
        if level >= 7:
            block_types.extend(["indestructible", "moving"])
            
        return block_types
            
    def get_level_layout(self, level, block_manager):
        if level > 10:
            level = 10  # Maksimum seviye
            
        level_data = self.levels[level]
        
        # Blok yöneticisini temizle ve yeni blokları oluştur
        block_manager.blocks.clear()
        
        # Blok sayısını ve türlerini ayarla
        rows = min(3 + level, 8)  # Her seviyede satır sayısı artar
        cols = self.screen_width // (block_manager.block_width + block_manager.padding)
        
        for row in range(rows):
            for col in range(cols):
                x = col * (block_manager.block_width + block_manager.padding)
                y = row * (block_manager.block_height + block_manager.padding) + 50
                
                # Blok türünü belirle
                if random.random() < level_data["hard_block_chance"]:
                    block_type = "hard"
                elif random.random() < level_data["special_block_chance"] and len(level_data["block_types"]) > 2:
                    # Özel bloklar varsa seç
                    special_blocks = level_data["block_types"][2:]
                    if special_blocks:
                        block_type = random.choice(special_blocks)
                    else:
                        block_type = "normal"
                else:
                    block_type = "normal"
                    
                # Bloğu oluştur
                block_manager.create_block(x, y, block_type, level_data["powerup_chance"])
        
        return {
            "ball_speed": level_data["ball_speed"],
            "points_multiplier": level_data["points_multiplier"]
        }
        
    def is_level_complete(self, block_manager):
        # Yıkılabilir blok kaldı mı kontrol et
        for block in block_manager.blocks:
            if block.block_type != "indestructible":
                return False
        return True
        
    def get_level_info(self, level):
        if level in self.levels:
            return self.levels[level]
        return None 
        
    def start_level(self, level):
        self.current_level = level
        return self.get_level_info(level) 