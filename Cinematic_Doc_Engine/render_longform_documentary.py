"""
Long-Form Master Documentary Renderer:
Assembles an extensive 15-20 minute documentary with 8 Acts, 48 scenes,
Studio-mastered broadcast voiceover (100% free & unlimited, without ElevenLabs),
animated newspaper highlighter motion graphics, Foley sound design, and retention subtitles.
"""

import argparse
import io
import json
import os
import sys
import time
import subprocess

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.sound_designer import create_ambient_drone, create_tension_riser, create_heartbeat, create_whoosh, create_camera_shutter
from core.texture_generator import generate_vignette, generate_film_grain
from core.flannan_mega_script import get_mega_documentary_script
from core.asset_hunter import search_and_download_image
from core.audio_engine import (
    synthesize_speech_sync,
    get_media_duration,
    mix_scene_audio,
    create_retention_subtitles
)
from core.video_engine import (
    render_scene_clip,
    concatenate_clips,
    burn_cinematic_subtitles
)
from core.motion_graphics import create_animated_highlighter_clip
from core.thumbnail_generator import create_youtube_thumbnail
import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()


def ensure_core_assets():
    """Generates procedural sound design and visual overlays if missing."""
    audio_dir = os.path.join(BASE_DIR, "assets", "audio")
    overlay_dir = os.path.join(BASE_DIR, "assets", "overlays")
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(overlay_dir, exist_ok=True)
    
    drone_path = os.path.join(audio_dir, "ambient_suspense_drone.wav")
    riser_path = os.path.join(audio_dir, "tension_riser.wav")
    heart_path = os.path.join(audio_dir, "heartbeat.wav")
    whoosh_path = os.path.join(audio_dir, "whoosh.wav")
    shutter_path = os.path.join(audio_dir, "camera_shutter.wav")
    vignette_path = os.path.join(overlay_dir, "vignette.png")
    grain_path = os.path.join(overlay_dir, "film_grain.png")
    
    if not os.path.exists(drone_path):
        create_ambient_drone(60.0, drone_path)
    if not os.path.exists(riser_path):
        create_tension_riser(3.0, riser_path)
    if not os.path.exists(heart_path):
        create_heartbeat(heart_path)
    if not os.path.exists(whoosh_path):
        create_whoosh(whoosh_path)
    if not os.path.exists(shutter_path):
        create_camera_shutter(shutter_path)
    if not os.path.exists(vignette_path):
        generate_vignette(1920, 1080, vignette_path)
    if not os.path.exists(grain_path):
        generate_film_grain(1920, 1080, grain_path)


def run_longform_production(
    language: str = "en",
    output_folder: str = "output/flannan_18min_master",
    max_chapters: int = None
):
    print("=" * 80)
    print("🎬 CINEMATIC DOC ENGINE: STARTING 15-20 MIN LONG-FORM MASTER PRODUCTION")
    print("💎 Audio Mode: Studio Vocal Chain (100% Free, Warm Shure SM7B Broadcast EQ)")
    print(f"🌍 Language: {language.upper()} | Output: {output_folder}")
    print("=" * 80)
    
    start_time = time.time()
    os.makedirs(output_folder, exist_ok=True)
    ensure_core_assets()
    
    audio_dir = os.path.join(BASE_DIR, "assets", "audio")
    vignette_path = os.path.join(BASE_DIR, "assets", "overlays", "vignette.png")
    drone_path = os.path.join(audio_dir, "ambient_suspense_drone.wav")
    
    # 1. Load Mega Script
    doc_data = get_mega_documentary_script(language=language)
    chapters = doc_data["chapters"]
    if max_chapters:
        chapters = chapters[:max_chapters]
        
    all_scenes = []
    for c in chapters:
        all_scenes.extend(c["scenes"])
        
    print(f"\n[Step 1/5] 📜 Loaded Long-Form Architecture: {len(chapters)} Acts, {len(all_scenes)} Visual Scenes.")
    
    # 2. Acquire & Grade Archival Visuals
    print(f"\n[Step 2/5] 🔍 Sourcing Authentic Archival Visuals & Historical Charts ({len(all_scenes)} scenes)...")
    scene_assets = []
    for i, scene in enumerate(all_scenes, 1):
        img_path = os.path.join(output_folder, f"scene_{i:03d}.jpg")
        search_and_download_image(scene["visual_query"], img_path)
        scene_assets.append(img_path)
        
    # 3. Audio Studio: Studio Broadcast Voiceover & Multi-Layer Foley
    print(f"\n[Step 3/5] 🎙️ Synthesizing Studio Broadcast Narration & Layering Foley SFX...")
    rendered_audio_tracks = []
    scenes_timing = []
    current_time_offset = 0.0
    
    for i, scene in enumerate(all_scenes, 1):
        raw_voice = os.path.join(output_folder, f"voice_{i:03d}.wav")
        mixed_audio = os.path.join(output_folder, f"mix_{i:03d}.wav")
        
        # Synthesize with Studio Vocal Chain (Zero cost, rich broadcast EQ & compression)
        synthesize_speech_sync(scene["text"], raw_voice, language=language, use_elevenlabs=False)
        dur = get_media_duration(raw_voice)
        
        # Match Foley Sound Effect
        cue = scene.get("audio_cue")
        sfx_path = None
        if cue == "camera_shutter":
            sfx_path = os.path.join(audio_dir, "camera_shutter.wav")
        elif cue == "whoosh":
            sfx_path = os.path.join(audio_dir, "whoosh.wav")
        elif cue == "heartbeat_thud":
            sfx_path = os.path.join(audio_dir, "heartbeat.wav")
        elif cue == "tension_riser":
            sfx_path = os.path.join(audio_dir, "tension_riser.wav")
            
        mix_scene_audio(
            voice_path=raw_voice,
            output_path=mixed_audio,
            drone_path=drone_path,
            sfx_path=sfx_path,
            drone_volume=0.18
        )
        
        rendered_audio_tracks.append((mixed_audio, dur))
        scenes_timing.append({
            "id": i,
            "text": scene["text"],
            "global_start": current_time_offset,
            "duration": dur
        })
        current_time_offset += dur
        if i % 8 == 0 or i == len(all_scenes):
            print(f"  -> Synthesized {i}/{len(all_scenes)} scenes (Current Runtime: {current_time_offset / 60:.1f} minutes)...")

    # Generate Retention Subtitles
    srt_path = os.path.join(output_folder, "master_subtitles.srt")
    create_retention_subtitles(scenes_timing, srt_path)
    total_minutes = current_time_offset / 60.0
    print(f"\n✨ Total Documentary Duration: {total_minutes:.2f} MINUTES ({current_time_offset:.1f}s)")
    print(f"📝 Subtitles File: {srt_path}")
    
    # 4. Pro Video Assembly & Motion Graphics
    print(f"\n[Step 4/5] 🎥 Compositing Master Sequence ({len(all_scenes)} Video Clips)...")
    clip_paths = []
    
    for i, scene in enumerate(all_scenes, 1):
        img_path = scene_assets[i - 1]
        audio_path, dur = rendered_audio_tracks[i - 1]
        clip_path = os.path.join(output_folder, f"clip_{i:03d}.mp4")
        motion = scene.get("camera_motion", "zoom_in_slow")
        
        if scene.get("scene_type") == "highlighter":
            print(f"  [Motion Graphics {i}/{len(all_scenes)}] Rendering Animated Newspaper Highlighter...")
            raw_hl = os.path.join(output_folder, f"raw_hl_{i:03d}.mp4")
            create_animated_highlighter_clip(
                headline_text=scene.get("headline", "OFFICIAL MARITIME DISPATCH"),
                highlight_phrase=scene.get("highlight_phrase", "CLASSIFIED INVESTIGATION"),
                output_clip_path=raw_hl,
                duration_sec=dur
            )
            # Combine with audio
            merge_cmd = [
                FFMPEG_BIN, "-y",
                "-i", raw_hl,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                clip_path
            ]
            subprocess.run(merge_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(raw_hl):
                os.remove(raw_hl)
        else:
            render_scene_clip(
                image_path=img_path,
                audio_path=audio_path,
                duration=dur,
                output_clip_path=clip_path,
                motion=motion,
                vignette_path=vignette_path
            )
            
        clip_paths.append(clip_path)
        if i % 10 == 0 or i == len(all_scenes):
            print(f"  -> Rendered {i}/{len(all_scenes)} video clips...")
            
    # Concatenate all clips
    print("\n  -> Lossless Concatenation of all 8 Acts...")
    raw_master_video = os.path.join(output_folder, "raw_master_sequence.mp4")
    concatenate_clips(clip_paths, raw_master_video)
    
    # Burn retention subtitles
    final_master_video = os.path.join(output_folder, "Flannan_Isle_18Min_Master_Documentary.mp4")
    print(f"  -> Burning cinematic subtitles into final master release...")
    burn_cinematic_subtitles(raw_master_video, srt_path, final_master_video)
    
    # 5. YouTube Packaging
    print(f"\n[Step 5/5] 🖼️ Generating YouTube Master Packaging (Thumbnail & SEO)...")
    thumb_path = os.path.join(output_folder, "YouTube_Thumbnail_Master.jpg")
    create_youtube_thumbnail(
        base_image_path=scene_assets[0],
        output_path=thumb_path,
        text_overlay="LOCKED INSIDE",
        subtitle_tag="120 YEARS UNSOLVED"
    )
    
    metadata = {
        "title": doc_data["titles"][0],
        "titles_alternatives": doc_data["titles"],
        "runtime_minutes": total_minutes,
        "runtime_seconds": current_time_offset,
        "video_file": os.path.basename(final_master_video),
        "thumbnail_file": os.path.basename(thumb_path),
        "chapters_overview": [
            f"Act {c['chapter_id']}: {c['title']}" for c in chapters
        ]
    }
    with open(os.path.join(output_folder, "youtube_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"✨ FULL 15-20 MINUTE DOCUMENTARY PRODUCTION COMPLETED in {elapsed / 60:.1f} minutes!")
    print(f"📁 Master Video: {final_master_video}")
    print(f"🖼️ Master Thumbnail: {thumb_path}")
    print("=" * 80)
    return final_master_video, thumb_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="15-20 Min Long-Form Documentary Engine")
    parser.add_argument("--language", type=str, default="en", choices=["en", "ro"])
    parser.add_argument("--output", type=str, default="output/flannan_18min_master")
    parser.add_argument("--chapters", type=int, default=None, help="Max chapters to render (default: all 8 acts)")
    args = parser.parse_args()
    
    run_longform_production(language=args.language, output_folder=args.output, max_chapters=args.chapters)
