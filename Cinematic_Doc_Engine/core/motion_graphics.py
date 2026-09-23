"""
Motion Graphics Engine: Creates signature "Pro Editor" animations:
1. Animated Yellow Highlighter on vintage documents & newspapers (stil Lemmino / Vox).
2. Film Burn & Light Leak chapter transition overlays.
3. 2.5D Parallax depth motion.
"""

import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import imageio_ffmpeg


FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()


def create_animated_highlighter_clip(
    headline_text: str,
    highlight_phrase: str,
    output_clip_path: str,
    duration_sec: float = 4.0,
    fps: int = 30,
    width: int = 1920,
    height: int = 1080
) -> str:
    """
    Renders an authentic, animated vintage newspaper / police report clipping
    where a fluorescent yellow highlighter draws itself smoothly across the key phrase.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_clip_path)), exist_ok=True)
    temp_frames_dir = output_clip_path + "_frames"
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    # 1. Create Base Newspaper Background (Aged paper texture, columns, title)
    paper = Image.new("RGB", (width, height), (228, 220, 204))  # Aged paper color
    draw = ImageDraw.Draw(paper)
    
    # Add paper noise & slight vignette
    noise = np.random.normal(0, 12, (height, width, 3)).astype(np.int16)
    paper_arr = np.clip(np.array(paper, dtype=np.int16) + noise, 0, 255).astype(np.uint8)
    paper = Image.fromarray(paper_arr)
    draw = ImageDraw.Draw(paper)
    
    # Try finding fonts
    font_masthead = None
    font_headline = None
    font_body = None
    font_candidates = [
        "C:/Windows/Fonts/georgiab.ttf",
        "C:/Windows/Fonts/timesbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]
    for fc in font_candidates:
        if os.path.exists(fc):
            try:
                font_masthead = ImageFont.truetype(fc, 38)
                font_headline = ImageFont.truetype(fc, 58)
                font_body = ImageFont.truetype(fc, 28)
                break
            except Exception:
                continue
    if not font_masthead:
        font_masthead = ImageFont.load_default()
        font_headline = ImageFont.load_default()
        font_body = ImageFont.load_default()
        
    # Newspaper Header
    draw.line([(120, 140), (width - 120, 140)], fill=(40, 35, 30), width=4)
    draw.text((120, 90), "THE INVESTIGATIVE CHRONICLE  //  OFFICIAL ARCHIVE DISPATCH", font=font_masthead, fill=(40, 35, 30))
    draw.line([(120, 150), (width - 120, 150)], fill=(40, 35, 30), width=1)
    
    # Big Headline
    draw.text((120, 210), headline_text.upper(), font=font_headline, fill=(20, 15, 10))
    draw.line([(120, 290), (width - 120, 290)], fill=(70, 60, 50), width=2)
    
    # Body Text lines
    start_y = 350
    lead_text = "OFFICIAL RECORD: During the initial inspection, detectives discovered an anomaly."
    full_sentence = f"{lead_text} {highlight_phrase} All other personal belongings remained undisturbed."
    
    # Wrap text
    words = full_sentence.split()
    line1 = " ".join(words[:10])
    line2 = " ".join(words[10:20])
    line3 = " ".join(words[20:])
    
    draw.text((120, start_y), line1, font=font_body, fill=(35, 30, 25))
    draw.text((120, start_y + 48), line2, font=font_body, fill=(35, 30, 25))
    draw.text((120, start_y + 96), line3, font=font_body, fill=(35, 30, 25))
    
    # Highlighter coordinates on line2 where highlight_phrase sits
    hl_x_start = 120
    hl_y_start = start_y + 42
    hl_width = 750
    hl_height = 42
    
    total_frames = int(duration_sec * fps)
    anim_start_frame = int(fps * 0.6)  # starts highlighting at 0.6s
    anim_duration_frames = int(fps * 1.5)  # takes 1.5s to draw the line
    
    # Generate animated frames with slow camera push-in
    for frame_idx in range(total_frames):
        current_img = paper.copy()
        
        # Calculate highlight progress (0.0 to 1.0)
        if frame_idx < anim_start_frame:
            progress = 0.0
        elif frame_idx >= anim_start_frame + anim_duration_frames:
            progress = 1.0
        else:
            progress = (frame_idx - anim_start_frame) / float(anim_duration_frames)
            
        if progress > 0:
            current_hl_w = int(hl_width * progress)
            # Create yellow highlight layer with transparency
            hl_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            hl_draw = ImageDraw.Draw(hl_layer)
            # Fluorescent highlighter yellow with transparency
            hl_draw.rectangle(
                [hl_x_start - 6, hl_y_start, hl_x_start + current_hl_w, hl_y_start + hl_height],
                fill=(255, 235, 0, 160)
            )
            # Alpha composite
            current_img = Image.alpha_composite(current_img.convert("RGBA"), hl_layer).convert("RGB")
            
        # Subtle slow camera zoom in (1.0 to 1.08)
        zoom = 1.0 + (0.08 * (frame_idx / total_frames))
        zw = int(width / zoom)
        zh = int(height / zoom)
        crop_x = int((width - zw) * 0.3)
        crop_y = int((height - zh) * 0.35)
        cropped = current_img.crop((crop_x, crop_y, crop_x + zw, crop_y + zh))
        frame_final = cropped.resize((width, height), Image.Resampling.BILINEAR)
        
        frame_final.save(os.path.join(temp_frames_dir, f"frame_{frame_idx:04d}.jpg"), "JPEG", quality=90)

    # Encode with FFmpeg
    cmd = [
        FFMPEG_BIN, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%04d.jpg"),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        output_clip_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleanup frames
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    
    print(f"  [Motion Graphics] Animated Newspaper Highlighter created: {output_clip_path}")
    return output_clip_path


if __name__ == "__main__":
    test_out = "output/test_highlighter.mp4"
    create_animated_highlighter_clip(
        headline_text="Lighthouse Mystery: Key Record Found",
        highlight_phrase="THE OUTER STEEL DOOR WAS LOCKED FROM THE INSIDE.",
        output_clip_path=test_out
    )
