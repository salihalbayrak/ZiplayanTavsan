import logging
from datetime import datetime

class GameErrorHandler:
    def __init__(self):
        logging.basicConfig(
            filename='error_log.txt',
            level=logging.ERROR,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            encoding='utf-8'
        )
        
    def log_error(self, error, error_type="general"):
        """Hatayı log dosyasına kaydet"""
        logging.error(f"{error_type}: {str(error)}")
        
    def handle_error(self, error, game_state):
        """Hatayı işle ve kullanıcıya göster"""
        self.log_error(error)
        if game_state:
            game_state.set_error(str(error))
            
    def handle_asset_error(self, asset_path, error):
        """Asset yükleme hatalarını işle"""
        error_msg = f"Asset yüklenemedi: {asset_path} - {str(error)}"
        self.log_error(error_msg, "asset_error")
        return None
        
    def handle_game_object_error(self, object_type, error):
        """Oyun nesnesi oluşturma hatalarını işle"""
        error_msg = f"{object_type} oluşturma hatası: {str(error)}"
        self.log_error(error_msg, "object_error")
        return None
        
    def handle_physics_error(self, component, error):
        """Fizik hesaplama hatalarını işle"""
        error_msg = f"Fizik hesaplama hatası ({component}): {str(error)}"
        self.log_error(error_msg, "physics_error")
        return None 