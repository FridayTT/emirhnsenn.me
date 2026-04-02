"""
HIZLI KULLANIM - Video bilgilerini buraya yazın ve scripti calistirin
"""

# ═══════════════════════════════════════════════════════════════
# VIDEO LISTESI - Her video icin bilgileri doldurun
# Timestamp (?t=12333) video'nun o dakikadan baslamasini saglar
# ═══════════════════════════════════════════════════════════════

VIDEOS = [
    {
        "url": "https://youtu.be/-HehF4XwKiM?t=12333",  # Video URL + timestamp
        "title": "CSA Divisional Championship vs Dickinson",  # Baslik
        "description": "CSA · Mar 1, 2026"  # Aciklama
    },
    {
        "url": "https://youtu.be/qLYug7WsHnU?t=17473",  # Video URL + timestamp
        "title": "CSA Divisional Championship vs Hamilton",  # Baslik
        "description": "CSA · Feb 28, 2026"  # Aciklama
    },
    # YENI VIDEO EKLEMEK ICIN YUKARIYA EKLEYIN
]

# ═══════════════════════════════════════════════════════════════
# ASAGI DAKI KODU DEGISTIRMEYIN
# ═══════════════════════════════════════════════════════════════

import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def get_youtube_id(url):
    """Video ID'yi URL'den cikarir (timestamp'i de korur)"""
    patterns = [
        r'youtu\.be/([a-zA-Z0-9_-]{11})',  # youtu.be/VIDEO_ID
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',  # youtube.com/watch?v=VIDEO_ID
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',  # youtube.com/embed/VIDEO_ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_timestamp(url):
    """URL'deki timestamp'i (?t=12333) cikarir"""
    match = re.search(r'\?t=(\d+)', url)
    if match:
        return match.group(1)
    return None

def get_thumbnail_url(video_id):
    """Thumbnail URL'i - maxresdefault en yuksek kalite"""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def get_watch_url(url, video_id):
    """Watch URL'i timestamp ile"""
    timestamp = get_timestamp(url)
    if timestamp:
        return f"https://www.youtube.com/watch?v={video_id}&t={timestamp}"
    return f"https://www.youtube.com/watch?v={video_id}"

def generate_video_html(video_url, title, description):
    """Video karti HTML'i uretir"""
    video_id = get_youtube_id(video_url)
    if not video_id:
        return None
    
    thumbnail = get_thumbnail_url(video_id)
    watch_url = get_watch_url(video_url, video_id)
    timestamp = get_timestamp(video_url)
    timestamp_text = f"?t={timestamp}s" if timestamp else ""
    
    return f'''<div class="col-md-5 reveal">
    <a href="{watch_url}" target="_blank" rel="noopener noreferrer"
        class="video-card">
        <div class="video-thumbnail">
            <img src="{thumbnail}" alt="{title}"
                loading="lazy">
            <div class="video-play-btn"><i class="bi bi-play-fill"></i></div>
        </div>
        <div class="video-title">{title}</div>
        <div class="video-meta">{description}</div>
    </a>
</div>'''

def main():
    print("Video Highlights Generator (with Timestamp Support)")
    print("=" * 50)
    
    valid_videos = []
    
    for i, video in enumerate(VIDEOS, 1):
        video_id = get_youtube_id(video["url"])
        if video_id:
            timestamp = get_timestamp(video["url"])
            ts_info = f" @ {timestamp}s" if timestamp else ""
            valid_videos.append((video["url"], video["title"], video["description"]))
            print(f"[OK] Video {i}: {video['title']}{ts_info}")
        else:
            print(f"[X] Video {i}: Gecersiz URL - {video['url']}")
    
    if not valid_videos:
        print("\n[!] Hic gecerli video yok!")
        return
    
    print("\n" + "=" * 50)
    print("KOPYALANACAK HTML KODU:")
    print("=" * 50 + "\n")
    
    html_output = []
    for video_url, title, description in valid_videos:
        html = generate_video_html(video_url, title, description)
        if html:
            print(html)
            html_output.append(html)
    
    with open("video_output.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html_output))
    
    print(f"\n[OK] HTML 'video_output.html' dosyasina kaydedildi!")

if __name__ == "__main__":
    main()
