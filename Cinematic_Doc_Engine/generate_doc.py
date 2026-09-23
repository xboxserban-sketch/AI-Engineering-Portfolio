"""
Cinematic Doc Engine - Master Orchestrator
Generates end-to-end, high-retention, YouTube-ready documentaries (True Crime, Mysteries, History)
with authentic archival visuals, deep narrator voice, procedural sound design, and viral packaging.
"""

import argparse
import io
import json
import os
import sys
import time

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.sound_designer import create_ambient_drone, create_tension_riser, create_heartbeat
from core.texture_generator import generate_vignette, generate_film_grain
from core.narrative_engine import get_curated_template, DocumentaryScript
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
from core.thumbnail_generator import create_youtube_thumbnail


def ensure_core_assets():
    """Generates procedural sound design and visual overlays if missing."""
    audio_dir = os.path.join(BASE_DIR, "assets", "audio")
    overlay_dir = os.path.join(BASE_DIR, "assets", "overlays")
    
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(overlay_dir, exist_ok=True)
    
    drone_path = os.path.join(audio_dir, "ambient_suspense_drone.wav")
    riser_path = os.path.join(audio_dir, "tension_riser.wav")
    heart_path = os.path.join(audio_dir, "heartbeat.wav")
    vignette_path = os.path.join(overlay_dir, "vignette.png")
    grain_path = os.path.join(overlay_dir, "film_grain.png")
    
    if not os.path.exists(drone_path):
        print("[Assets] Generating ambient suspense drone...")
        create_ambient_drone(45.0, drone_path)
    if not os.path.exists(riser_path):
        print("[Assets] Generating tension riser SFX...")
        create_tension_riser(3.0, riser_path)
    if not os.path.exists(heart_path):
        print("[Assets] Generating heartbeat thump SFX...")
        create_heartbeat(heart_path)
    if not os.path.exists(vignette_path):
        print("[Assets] Generating cinematic vignette...")
        generate_vignette(1920, 1080, vignette_path)
    if not os.path.exists(grain_path):
        print("[Assets] Generating 35mm film grain...")
        generate_film_grain(1920, 1080, grain_path)


def run_pipeline(
    topic: str = "The Flannan Isle Mystery",
    language: str = "en",
    output_folder: str = "output/flannan_doc"
):
    print("=" * 70)
    print(f"🎬 CINEMATIC DOC ENGINE: Starting Production for '{topic}'")
    print(f"🌍 Language: {language.upper()} | Output: {output_folder}")
    print("=" * 70)
    
    start_time = time.time()
    os.makedirs(output_folder, exist_ok=True)
    
    # 0. Ensure assets
    ensure_core_assets()
    audio_dir = os.path.join(BASE_DIR, "assets", "audio")
    vignette_path = os.path.join(BASE_DIR, "assets", "overlays", "vignette.png")
    
    # 1. Narrative & Retention Script
    print("\n[Step 1/5] 📜 Engineering Psychological Retention Script & Open Loops...")
    script: DocumentaryScript = get_curated_template(topic, language=language)
    script_path = os.path.join(output_folder, "script.json")
    script.save(script_path)
    print(f"  -> Generated {len(script.scenes)} narrative scenes.")
    print("  -> Top High-CTR YouTube Titles:")
    for i, t in enumerate(script.titles[:3], 1):
        print(f"     {i}. {t}")
        
    # 2. Asset Hunter: Archival Photos
    print("\n[Step 2/5] 🔍 Hunting Authentic Archival Images & Press Clippings...")
    scene_assets = []
    for scene in script.scenes:
        sid = scene["id"]
        img_filename = f"scene_{sid:02d}.jpg"
        img_path = os.path.join(output_folder, img_filename)
        search_and_download_image(scene["visual_query"], img_path)
        scene_assets.append(img_path)
        
    # 3. Audio Studio: Voice Synthesis, Sound Design & Subtitles
    print("\n[Step 3/5] 🎙️ Synthesizing Voiceover & Dynamic Sound Design...")
    rendered_audio_tracks = []
    scenes_timing = []
    current_time_offset = 0.0
    
    for scene in script.scenes:
        sid = scene["id"]
        raw_voice_path = os.path.join(output_folder, f"voice_{sid:02d}.mp3")
        mixed_audio_path = os.path.join(output_folder, f"audio_mix_{sid:02d}.wav")
        
        print(f"  [Voice {sid}/{len(script.scenes)}] Synthesizing: \"{scene['text'][:45]}...\"")
        synthesize_speech_sync(scene["text"], raw_voice_path, language=language)
        dur = get_media_duration(raw_voice_path)
        
        # Audio cue selection (Pro Foley & Tension)
        sfx_path = None
        cue = scene.get("audio_cue")
        if cue == "heartbeat_thud":
            sfx_path = os.path.join(audio_dir, "heartbeat.wav")
        elif cue == "tension_riser":
            sfx_path = os.path.join(audio_dir, "tension_riser.wav")
        elif cue == "camera_shutter":
            sfx_path = os.path.join(audio_dir, "camera_shutter.wav")
        elif cue == "whoosh":
            sfx_path = os.path.join(audio_dir, "whoosh.wav")
            
        drone_path = os.path.join(audio_dir, "ambient_suspense_drone.wav")
        mix_scene_audio(
            voice_path=raw_voice_path,
            output_path=mixed_audio_path,
            drone_path=drone_path,
            sfx_path=sfx_path,
            drone_volume=0.20
        )
        
        rendered_audio_tracks.append((mixed_audio_path, dur))
        scenes_timing.append({
            "id": sid,
            "text": scene["text"],
            "global_start": current_time_offset,
            "duration": dur
        })
        current_time_offset += dur
        
    # Build subtitles
    srt_path = os.path.join(output_folder, "subtitles.srt")
    create_retention_subtitles(scenes_timing, srt_path)
    print(f"  -> Total Documentary Runtime: {current_time_offset:.1f} seconds")
    print(f"  -> Generated retention subtitles: {srt_path}")
    
    # 4. Video Compositor: Ken Burns & Subtitle Burning
    print("\n[Step 4/5] 🎥 Compositing Pro Documentary (Ken Burns, Motion Graphics, SFX)...")
    from core.motion_graphics import create_animated_highlighter_clip
    import subprocess
    import imageio_ffmpeg
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    clip_paths = []
    for i, scene in enumerate(script.scenes):
        sid = scene["id"]
        img_path = scene_assets[i]
        audio_path, dur = rendered_audio_tracks[i]
        clip_path = os.path.join(output_folder, f"clip_{sid:02d}.mp4")
        motion = scene.get("camera_motion", "zoom_in_slow")
        
        if scene.get("scene_type") == "highlighter":
            print(f"  [Pro Motion Graphics {sid}/{len(script.scenes)}] Drawing animated newspaper highlighter (dur: {dur:.2f}s)...")
            raw_hl = os.path.join(output_folder, f"raw_hl_{sid:02d}.mp4")
            create_animated_highlighter_clip(
                headline_text=scene.get("headline", "INVESTIGATION DISPATCH"),
                highlight_phrase=scene.get("highlight_phrase", "CLASSIFIED INCIDENT"),
                output_clip_path=raw_hl,
                duration_sec=dur
            )
            # Merge with audio
            merge_cmd = [
                ffmpeg_bin, "-y",
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
            print(f"  [Render Clip {sid}/{len(script.scenes)}] Motion: {motion}, Dur: {dur:.2f}s...")
            render_scene_clip(
                image_path=img_path,
                audio_path=audio_path,
                duration=dur,
                output_clip_path=clip_path,
                motion=motion,
                vignette_path=vignette_path
            )
        clip_paths.append(clip_path)
        
    # Concatenate all clips
    print("  -> Concatenating scene clips into master sequence...")
    raw_master_path = os.path.join(output_folder, "master_raw.mp4")
    concatenate_clips(clip_paths, raw_master_path)
    
    # Burn subtitles
    final_video_path = os.path.join(output_folder, f"{topic.replace(' ', '_')}_Master_Documentary.mp4")
    print(f"  -> Burning cinematic subtitles into {final_video_path}...")
    burn_cinematic_subtitles(raw_master_path, srt_path, final_video_path)
    
    # 5. Viral YouTube Packaging (Thumbnail & Metadata)
    print("\n[Step 5/5] 🖼️ Generating High-CTR Thumbnail & YouTube Metadata Package...")
    thumb_path = os.path.join(output_folder, "YouTube_Thumbnail_High_CTR.jpg")
    best_image = scene_assets[0] if scene_assets else img_path
    
    thumb_concept = script.thumbnail_concepts[0] if script.thumbnail_concepts else {}
    overlay_text = thumb_concept.get("text_overlay", "LOCKED INSIDE")
    create_youtube_thumbnail(
        base_image_path=best_image,
        output_path=thumb_path,
        text_overlay=overlay_text,
        subtitle_tag="1900 UNSOLVED"
    )
    
    # Save package metadata
    metadata = {
        "title_recommendations": script.titles,
        "selected_title": script.titles[0],
        "thumbnail_file": os.path.basename(thumb_path),
        "video_file": os.path.basename(final_video_path),
        "duration_seconds": current_time_offset,
        "description": (
            f"The complete investigation into {topic}.\n\n"
            f"Chapters:\n"
            f"0:00 - The Cold Open & Impossible Paradox\n"
            f"0:12 - The Discovery\n"
            f"0:26 - The Final Log Entry\n"
            f"0:38 - The Unanswered Question\n\n"
            f"#Documentary #Mystery #TrueCrime #History"
        )
    }
    meta_path = os.path.join(output_folder, "youtube_package_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"✨ PRODUCTION COMPLETE in {elapsed:.1f} seconds!")
    print(f"📁 Video Ready: {final_video_path}")
    print(f"🖼️ Thumbnail Ready: {thumb_path}")
    print(f"📝 Metadata & Titles: {meta_path}")
    print("=" * 70)
    return final_video_path, thumb_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cinematic Documentary AI Generator")
    parser.add_argument("--topic", type=str, default="The Flannan Isle Mystery", help="Topic or case name")
    parser.add_argument("--language", type=str, default="en", choices=["en", "ro"], help="Language ('en' or 'ro')")
    parser.add_argument("--output", type=str, default="output/flannan_doc", help="Output directory")
    args = parser.parse_args()
    
    run_pipeline(topic=args.topic, language=args.language, output_folder=args.output)
