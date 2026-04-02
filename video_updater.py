"""
Emirhan Sen - Video Highlights Updater
=====================================
Bu script YouTube video linklerinden video kartları oluşturur.
Kullanım: python video_updater.py
"""

import re

def get_youtube_id(url):
    """YouTube URL'sinden video ID'sini çıkarır"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_thumbnail_url(video_id):
    """YouTube video thumbnail URL'lerini döndürür"""
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

def generate_video_html(video_id, title, description):
    """Video kartı HTML'i oluşturur"""
    thumbnail = get_thumbnail_url(video_id)
    return f'''                <div class="col-md-5 reveal">
                    <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" rel="noopener noreferrer"
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

def generate_all_html(videos):
    """Tüm video kartları için HTML üretir"""
    html_parts = []
    for i, video in enumerate(videos):
        video_id = get_youtube_id(video['url'])
        if video_id:
            html_parts.append(generate_video_html(video_id, video['title'], video['description']))
        else:
            print(f"⚠️ Video {i+1}: Geçersiz URL - {video['url']}")
    
    return '\n'.join(html_parts)

def main():
    print("=" * 50)
    print("🎬 Emirhan Sen - Video Highlights Updater")
    print("=" * 50)
    print()
    
    videos = []
    
    print("Video eklemek için bilgileri girin (boş bırakıp Enter'a basınca bitiş)")
    print()
    
    while True:
        print("-" * 40)
        
        url = input("📺 YouTube Video URL: ").strip()
        if not url:
            break
        
        video_id = get_youtube_id(url)
        if not video_id:
            print("❌ Geçersiz YouTube URL! Tekrar deneyin.")
            continue
        
        title = input("📝 Video Başlığı: ").strip()
        if not title:
            title = "St. Lawrence Squash Match"
        
        description = input("📄 Açıklama (örn: 'Liberty League · Feb 2026 · 45 min'): ").strip()
        if not description:
            description = "Squash Match"
        
        videos.append({
            'url': url,
            'title': title,
            'description': description
        })
        print(f"✅ Eklendi: {title}")
        print()
    
    if not videos:
        print("❌ Hiç video eklenmedi!")
        return
    
    print()
    print("=" * 50)
    print("📋 ÜRETILEN HTML KODU:")
    print("=" * 50)
    print()
    print(generate_all_html(videos))
    print()
    print("=" * 50)
    print("💡 Yukarıdaki kodu web sitesindeki video section'a yapıştırın")
    print()
    
    # Also save to file
    output_file = "video_updates.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(generate_all_html(videos))
    print(f"📁 HTML '{output_file}' dosyasına da kaydedildi!")

if __name__ == "__main__":
    main()
