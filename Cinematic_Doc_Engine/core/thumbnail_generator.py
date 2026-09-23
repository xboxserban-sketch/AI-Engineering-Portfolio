"""
Thumbnail Generator: Crafts high-CTR YouTube thumbnails for documentaries (Stil Lemmino / Fern / MagnatesMedia).
Applies aggressive mystery contrast, atmospheric color grading, and psychological text overlays (e.g. "LOCKED INSIDE").
"""

import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont


def create_youtube_thumbnail(
    base_image_path: str,
    output_path: str,
    text_overlay: str = "LOCKED INSIDE",
    subtitle_tag: str = "UNSOLVED",
    target_size: tuple = (1280, 720)
) -> str:
    """
    Creates a high-CTR YouTube thumbnail from a base archival image.
    Features:
    1. High-contrast noir & eerie saturation grading.
    2. Deep edge vignette to focus gaze on the center.
    3. Bold psychological text hook with drop shadow and high-contrast outline.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 1. Load and resize
    img = Image.open(base_image_path).convert("RGB")
    from PIL import ImageOps
    fitted = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.4))
    
    # 2. Thumbnail Color Grading (High Drama)
    # Boost contrast by 40% for small-screen pop
    contrast = ImageEnhance.Contrast(fitted).enhance(1.4)
    # Slight color boost on key accents
    color = ImageEnhance.Color(contrast).enhance(1.15)
    # Sharpness boost
    sharp = color.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=2))
    
    # 3. Add heavy dark vignette / gradient on bottom and left for text legibility
    overlay = Image.new("RGBA", target_size, (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Dark gradient from left/bottom
    w, h = target_size
    for x in range(w):
        # Darken the left 50% for text
        if x < int(w * 0.55):
            alpha = int(180 * (1.0 - (x / (w * 0.55))))
            draw_ov.line([(x, 0), (x, h)], fill=(10, 14, 20, alpha))
            
    # Combine
    thumb = Image.alpha_composite(sharp.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(thumb)
    
    # 4. Typography (Clean, Punchy, High-CTR)
    # Try finding an impact/arial font on Windows, fallback to default
    font_main = None
    font_sub = None
    font_candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguiemj.ttf",
        "C:/Windows/Fonts/tahoma.ttf"
    ]
    for fc in font_candidates:
        if os.path.exists(fc):
            try:
                font_main = ImageFont.truetype(fc, 78)
                font_sub = ImageFont.truetype(fc, 32)
                break
            except Exception:
                continue
                
    if not font_main:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    text_x = 60
    text_y = int(h * 0.42)
    
    # Draw Subtitle Tag (e.g. [CLASSIFIED] or [1900 INCIDENT] in warning red/amber)
    if subtitle_tag:
        tag_bg_x = text_x
        tag_bg_y = text_y - 50
        tag_text = f"  {subtitle_tag.upper()}  "
        draw.rectangle([tag_bg_x, tag_bg_y, tag_bg_x + 220, tag_bg_y + 38], fill=(185, 28, 28, 240))
        draw.text((tag_bg_x + 10, tag_bg_y + 4), tag_text, font=font_sub, fill=(255, 255, 255))
        
    # Draw Main Bold Hook (e.g. "LOCKED INSIDE") with deep black drop shadow & red/yellow accent
    words = text_overlay.upper().split()
    current_y = text_y
    for word in words:
        # Shadow
        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3), (5, 5), (0, 4)]:
            draw.text((text_x + dx, current_y + dy), word, font=font_main, fill=(0, 0, 0, 255))
        # Foreground: Bright yellow or white
        text_color = (255, 225, 50) if word in ["INSIDE", "SECRET", "DEAD", "VANISHED", "ALONE", "42"] else (255, 255, 255)
        draw.text((text_x, current_y), word, font=font_main, fill=text_color)
        current_y += 85
        
    # Final export
    final_thumb = thumb.convert("RGB")
    final_thumb.save(output_path, "JPEG", quality=95)
    print(f"  [Thumbnail] High-CTR Thumbnail exported to: {output_path}")
    return output_path


if __name__ == "__main__":
    test_in = "output/test_archive_photo.jpg"
    test_out = "output/test_youtube_thumbnail.jpg"
    if os.path.exists(test_in):
        create_youtube_thumbnail(test_in, test_out, text_overlay="LOCKED INSIDE", subtitle_tag="1900 MYSTERY")
