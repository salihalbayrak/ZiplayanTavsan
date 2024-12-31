# Breakout Oyunu

Modern bir yaklaşımla yeniden tasarlanmış klasik Breakout oyunu. Pygame kullanılarak Python'da geliştirilmiştir.

## Özellikler

### Oyun Mekanikleri
- Fizik tabanlı top hareketi
- Güç-up sistemi (çoklu top, büyük/küçük raket, kalkan vb.)
- Farklı zorluk seviyeleri
- Çeşitli blok tipleri ve dayanıklılık sistemi
- Combo ve puan sistemi

### Kullanıcı Özellikleri
- Kullanıcı profili ve istatistikler
- En yüksek skorlar tablosu
- Başarım sistemi ve rozetler
- Günlük görevler

### Özelleştirme
- Tema seçenekleri (Klasik, Neon, Retro)
- Ses ayarları (Ana ses, Müzik, Efektler)
- Kontrol ayarları
- Raket ve top rengi seçimi

## Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/kullaniciadi/breakout-oyunu.git

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Oyunu başlatın
python main.py
```

## Gereksinimler
- Python 3.8+
- Pygame 2.0+
- SQLite3

## Dizin Yapısı
```
C:.
│   database.py          # Veritabanı işlemleri
│   game_logic.py        # Oyun mantığı
│   game_mechanics.py    # Oyun mekanikleri
│   game_objects.py      # Oyun nesneleri
│   game_settings.py     # Ayarlar
│   game_states.py       # Durum yönetimi
│   leaderboard.py       # Skor tablosu
│   level_system.py      # Seviye sistemi
│   main.py             # Ana uygulama
│   power_up_system.py  # Güç-up sistemi
│   profile.py          # Profil yönetimi
│   settings_menu.py    # Ayarlar menüsü
│
├───Assets              # Ses dosyaları
├───images             # Görsel dosyalar
```

## Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
