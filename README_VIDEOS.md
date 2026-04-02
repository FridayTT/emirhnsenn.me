# Video Highlights Otomasyonu

## Kullanım

### 1. Video Ekleme
`add_videos.py` dosyasını bir metin editörü ile açın.

`VIDEOS` listesine yeni video ekleyin:

```python
VIDEOS = [
    {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID",  # YouTube URL
        "title": "Video Basligi",      # Başlık
        "description": "Aciklama"      # Açıklama (tarih, süre vs)
    },
    # Daha fazla video ekleyin...
]
```

### 2. Scripti Çalıştırma
```bash
python add_videos.py
```

### 3. HTML'yi Web Sitesine Yapıştırma
- Script çalıştırıldığında HTML kodu ekrana basılır
- Aynı zamanda `video_output.html` dosyasına kaydedilir
- Bu kodu web sitesindeki `<!-- VIDEO HIGHLIGHTS -->` bölümüne yapıştırın

## Örnek

```python
VIDEOS = [
    {
        "url": "https://www.youtube.com/watch?v=ABC123",
        "title": "St. Lawrence vs Princeton - Highlights",
        "description": "Liberty League · Feb 2026"
    },
    {
        "url": "https://www.youtube.com/watch?v=DEF456",
        "title": "Match of the Season",
        "description": "CSA Nationals · Mar 2026"
    },
]
```

## Notlar
- Sadece YouTube videoları desteklenir
- Thumbnail otomatik olarak YouTube'dan çekilir
- Her video `col-md-5` sınıfında - 2 video yan yana görünür
