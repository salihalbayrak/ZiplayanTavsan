import os

# Temel dizinler
ASSET_DIR = "Assests"
SOUND_DIR = os.path.join(ASSET_DIR, "sound")
IMAGE_DIR = "images"

# Level tasarımları
LEVEL_DESIGNS = {
    1: {
        "background": os.path.join(ASSET_DIR, "tas", "taşlı_kısım.png"),
        "platform": os.path.join(ASSET_DIR, "tas", "alt_platform_taş.png"),
        "sticky_platform": os.path.join(ASSET_DIR, "tas", "tasyapisgan.png"),
        "single_hit_block": os.path.join(ASSET_DIR, "tas", "tek_vuruş_taş.png"),
        "double_hit_block": os.path.join(ASSET_DIR, "tas", "iki_vuruş_taş.png"),
        "break_sound": os.path.join(ASSET_DIR, "tas", "taş_blok_kırılma.mp3")
    },
    2: {
        "background": os.path.join(ASSET_DIR, "col", "çöl_kısmı.png"),
        "platform": os.path.join(ASSET_DIR, "col", "alt_platform_çöl.png"),
        "sticky_platform": os.path.join(ASSET_DIR, "col", "colyapisgan.png"),
        "single_hit_block": os.path.join(ASSET_DIR, "col", "tek_vuruş_çöl.png"),
        "double_hit_block": os.path.join(ASSET_DIR, "col", "iki_vuruş_çöl.png"),
        "break_sound": os.path.join(ASSET_DIR, "col", "cam_kırılma.mp3")
    },
    3: {
        "background": os.path.join(ASSET_DIR, "buz", "Buzlu_kısım_background.png"),
        "platform": os.path.join(ASSET_DIR, "buz", "alt_platform_buz.png"),
        "sticky_platform": os.path.join(ASSET_DIR, "buz", "buzyapisgan.png"),
        "single_hit_block": os.path.join(ASSET_DIR, "buz", "tek_vuruş_buz.png"),
        "double_hit_block": os.path.join(ASSET_DIR, "buz", "iki_vuruşta_buz.png"),
        "break_sound": os.path.join(ASSET_DIR, "buz", "buzsesi.mp3"),
        "boss": os.path.join(ASSET_DIR, "buz", "son_bölüm_yeni.png")
    }
}

# Joker görselleri
POWERUP_IMAGES = {
    "big_paddle": os.path.join(ASSET_DIR, "joker", "buyuk.png"),
    "small_ball": os.path.join(ASSET_DIR, "joker", "kucuktop.png"),
    "multi_ball": os.path.join(ASSET_DIR, "joker", "cogalantop.png"),
    "laser": os.path.join(ASSET_DIR, "joker", "lazer.png"),
    "sticky": os.path.join(ASSET_DIR, "joker", "yapısgan.png"),
    "shield": os.path.join(ASSET_DIR, "joker", "kalkan.png")
}

# Ses efektleri
SOUND_EFFECTS = {
    "hit": os.path.join(ASSET_DIR, "topsesi.mp3"),
    "score": os.path.join(ASSET_DIR, "skorses.mp3"),
    "multi_ball": os.path.join(SOUND_DIR, "çoktu_top.mp3"),
    "menu": os.path.join(SOUND_DIR, "giriş_ekranı_sesi.mp3"),
    "sticky": os.path.join(SOUND_DIR, "yapışma sesi.mp3"),
    "big_paddle": os.path.join(SOUND_DIR, "raket_büyüme.mp3"),
    "level_up": os.path.join(SOUND_DIR, "level_atlama.mp3"),
    "laser": os.path.join(SOUND_DIR, "lazer_atışı.mp3"),
    "small_ball": os.path.join(SOUND_DIR, "küçük_top.mp3"),
    "game_over": os.path.join(SOUND_DIR, "kaybetme_sesi.mp3"),
    "shield": os.path.join(SOUND_DIR, "kalkan.mp3"),
    "background": os.path.join(ASSET_DIR, "background_sound.mp3")
}

# Oyun sabitleri
GAME_CONSTANTS = {
    # Top fiziği
    "BALL_SPEED": 7,
    "BALL_SPEED_MULTIPLIER": 1.3,  # Top küçüldüğünde hız artış çarpanı
    "BALL_MIN_ANGLE": 30,  # Topun minimum sıçrama açısı
    "BALL_MAX_ANGLE": 150,  # Topun maksimum sıçrama açısı
    "MIN_VERTICAL_SPEED_RATIO": 0.2,  # Minimum dikey hız oranı
    
    # Platform kontrolü
    "PLATFORM_SPEED": 8,
    "PLATFORM_WIDTH": 100,
    "PLATFORM_HEIGHT": 20,
    
    # Joker sistemi
    "LASER_COOLDOWN": 500,  # Lazer atışları arası bekleme süresi (ms)
    "MULTI_BALL_COUNT": 3,  # Çoklu top sayısı
    "POWER_UP_DURATION": 10000,  # Joker etki süresi (ms)
    "POWER_UP_FALL_SPEED": 3,  # Joker düşme hızı
    
    # Blok sistemi
    "BLOCK_WIDTH": 60,
    "BLOCK_HEIGHT": 20,
    "BLOCK_PADDING": 5,
    
    # Boss sistemi
    "BOSS_WIDTH": 120,
    "BOSS_HEIGHT": 60,
    "BOSS_MAX_HITS": 10
} 