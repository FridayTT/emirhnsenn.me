"""
TAM OTOMASYON - Video Ekleme Scripti
====================================
Bu script direkt index.html dosyasini günceller.
Kullanim: python auto_video_update.py
"""

import re
import os

# ═══════════════════════════════════════════════════════════════
# VIDEO LISTESI - Yeni videolari buraya ekle
# ═══════════════════════════════════════════════════════════════

VIDEOS = [
    {
        "url": "https://youtu.be/-HehF4XwKiM?t=12333",
        "title": "CSA Divisional Championship vs Dickinson",
        "description": "CSA · Mar 1, 2026"
    },
    {
        "url": "https://youtu.be/qLYug7WsHnU?t=17473",
        "title": "CSA Divisional Championship vs Hamilton",
        "description": "CSA · Feb 28, 2026"
    },
    # YENI VIDEO EKLEMEK ICIN:
    # {
    #     "url": "https://youtu.be/VIDEO_ID?t=12345",
    #     "title": "MAC ADI",
    #     "description": "LIG · TARIH"
    # },
]

# ═══════════════════════════════════════════════════════════════
# ASAGI DAKI KODU DEGISTIRMA
# ═══════════════════════════════════════════════════════════════

def get_youtube_id(url):
    patterns = [
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_timestamp(url):
    match = re.search(r'\?t=(\d+)', url)
    return match.group(1) if match else None

def get_watch_url(url, video_id):
    timestamp = get_timestamp(url)
    if timestamp:
        return f"https://www.youtube.com/watch?v={video_id}&t={timestamp}"
    return f"https://www.youtube.com/watch?v={video_id}"

def generate_video_html(video_url, title, description):
    video_id = get_youtube_id(video_url)
    if not video_id:
        return None
    
    thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    watch_url = get_watch_url(video_url, video_id)
    
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

def update_index_html(videos):
    index_path = "index.html"
    
    if not os.path.exists(index_path):
        print(f"[HATA] {index_path} bulunamadi!")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Video HTML'lerini olustur
    video_htmls = []
    for video in videos:
        html = generate_video_html(video['url'], video['title'], video['description'])
        if html:
            video_htmls.append(html)
    
    if not video_htmls:
        print("[HATA] Gecerli video yok!")
        return False
    
    videos_block = '\n'.join(video_htmls)
    
    # Video section'u bul
    start_marker = 'Latest Matches</h2>'
    search_idx = content.find(start_marker)
    if search_idx == -1:
        print("[HATA] Latest Matches bolumu bulunamadi!")
        return False
    
    # row div'in basini bul
    div_start = content.find('<div class="row g-4 justify-content-center">', search_idx)
    if div_start == -1:
        print("[HATA] Video div'i bulunamadi!")
        return False
    
    # </section> sonunu bul
    section_end = content.find('</section>', div_start)
    if section_end == -1:
        print("[HATA] Section sonu bulunamadi!")
        return False
    
    # Eski section'u al (div_start'dan section_end'e kadar)
    old_section = content[div_start:section_end]
    
    # Yeni section'u olustur
    new_section = f'''<div class="row g-4 justify-content-center">
{videos_block}
            </div>
        </div>
    </section>'''
    
    # Degistir
    new_html = content.replace(old_section, new_section, 1)
    
    if new_html == content:
        print("[HATA] Degisiklik yapilamadi!")
        return False
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True

def main():
    print("=" * 60)
    print("TAM OTOMASYON - Video Ekleme")
    print("=" * 60)
    
    # Videolari kontrol et
    valid = []
    for i, video in enumerate(VIDEOS, 1):
        video_id = get_youtube_id(video['url'])
        if video_id:
            ts = get_timestamp(video['url'])
            ts_info = f" @ {ts}s" if ts else ""
            valid.append(video)
            print(f"[OK] Video {i}: {video['title']}{ts_info}")
        else:
            print(f"[X] Video {i}: Gecersiz URL - {video['url']}")
    
    if not valid:
        print("\n[HATA] Gecerli video yok!")
        return
    
    print("\n" + "-" * 60)
    
    if update_index_html(valid):
        print(f"[BASARILI] {len(valid)} video eklendi!")
        print(f"[BASARILI] index.html guncellendi!")
    else:
        print("[HATA] index.html guncellemede sorun olustu!")

if __name__ == "__main__":
    main()
