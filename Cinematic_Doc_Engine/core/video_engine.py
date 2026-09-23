"""
Video Engine: Assembles documentary scenes into a broadcast-quality master MP4.
Features:
- Dynamic Ken Burns camera motion (slow zoom in, zoom out, pan).
- 35mm film grain and vignette overlay blending.
- Frame-rate normalization (30fps / 1080p).
- Fast FFmpeg concat demuxing.
- High-retention subtitle burning (yellow/white typography with drop shadows).
"""

import os
import subprocess
from typing import List, Dict
import imageio_ffmpeg


FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()


def render_scene_clip(
    image_path: str,
    audio_path: str,
    duration: float,
    output_clip_path: str,
    motion: str = "zoom_in_slow",
    vignette_path: str = "assets/overlays/vignette.png",
    fps: int = 30,
    width: int = 1920,
    height: int = 1080
) -> str:
    """
    Renders an individual scene clip with Ken Burns motion, atmospheric vignette,
    and synchronized audio.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_clip_path)), exist_ok=True)
    
    total_frames = max(15, int(duration * fps))
    
    # Configure Ken Burns formula based on requested motion
    if motion == "zoom_out_slow":
        # Start at 1.15 zoom, shrink smoothly towards 1.0
        zoom_expr = f"max(1.15-0.15*(on/{total_frames}),1.0)"
        x_expr = "iw/2-(iw/zoom/2)"
        y_expr = "ih/2-(ih/zoom/2)"
    elif motion == "pan_left":
        # Slow pan horizontally across frame
        zoom_expr = "1.12"
        x_expr = f"(iw-iw/zoom)*(on/{total_frames})"
        y_expr = "ih/2-(ih/zoom/2)"
    else:  # default zoom_in_slow
        # Smooth inward push from 1.0 to 1.15
        zoom_expr = f"min(1.0+0.15*(on/{total_frames}),1.15)"
        x_expr = "iw/2-(iw/zoom/2)"
        y_expr = "ih/2-(ih/zoom/2)"

    # Build FFmpeg filter chain
    # 1. Scale input to large canvas to prevent zoom pixelation
    # 2. Apply zoompan
    # 3. Overlay vignette for dark film noir edges
    inputs = [
        "-loop", "1", "-i", image_path,
        "-i", audio_path
    ]
    
    has_vignette = vignette_path and os.path.exists(vignette_path)
    if has_vignette:
        inputs.extend(["-i", vignette_path])
        filter_str = (
            f"[0:v]scale=4000:-1,zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':d={total_frames}:s={width}x{height}:fps={fps}[zoomed];"
            f"[zoomed][2:v]overlay=0:0:format=auto[outv]"
        )
    else:
        filter_str = (
            f"[0:v]scale=4000:-1,zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':d={total_frames}:s={width}x{height}:fps={fps}[outv]"
        )

    cmd = [
        FFMPEG_BIN, "-y",
        *inputs,
        "-t", f"{duration:.3f}",
        "-filter_complex", filter_str,
        "-map", "[outv]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        output_clip_path
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_clip_path


def concatenate_clips(clip_paths: List[str], output_path: str) -> str:
    """
    Concatenates individual scene clips using FFmpeg concat demuxer (lossless & instant).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    list_file_path = output_path + ".txt"
    
    with open(list_file_path, "w", encoding="utf-8") as f:
        for clip in clip_paths:
            # Escape path for FFmpeg concat demuxer
            clean_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file_path,
        "-c", "copy",
        output_path
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(list_file_path):
        os.remove(list_file_path)
    return output_path


def burn_cinematic_subtitles(video_input: str, srt_path: str, video_output: str) -> str:
    """
    Burns retention-engineered subtitles into the video.
    Uses bold, high-legibility typography (White text, black outline, lower third).
    """
    os.makedirs(os.path.dirname(os.path.abspath(video_output)), exist_ok=True)
    
    # Normalize path for FFmpeg subtitles filter on Windows
    clean_srt = os.path.abspath(srt_path).replace("\\", "/").replace(":", "\\:")
    
    # Subtitle style: Arial Bold, size 24, white foreground (&H00FFFFFF), solid black outline (&H00000000), margin 40px from bottom
    sub_filter = f"subtitles='{clean_srt}':force_style='FontName=Arial,FontSize=23,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=2,Bold=1,Alignment=2,MarginV=42'"

    cmd = [
        FFMPEG_BIN, "-y",
        "-i", video_input,
        "-vf", sub_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        video_output
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return video_output


if __name__ == "__main__":
    print("Video Engine module loaded successfully.")
