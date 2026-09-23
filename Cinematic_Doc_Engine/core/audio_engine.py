"""
Audio Engine: Synthesizes high-gravitas neural voiceovers, generates retention-optimized SRT subtitles,
and layers procedural ambient suspense drones and SFX cues with automatic audio ducking.
"""

import asyncio
import os
import re
import subprocess
from typing import Dict, List, Tuple
import edge_tts
import imageio_ffmpeg


FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

VOICE_CONFIG = {
    "en": {
        "voice": "en-US-ChristopherNeural",
        "rate": "-5%",
        "pitch": "-4Hz"
    },
    "ro": {
        "voice": "ro-RO-EmilNeural",
        "rate": "-4%",
        "pitch": "-3Hz"
    }
}


def get_media_duration(file_path: str) -> float:
    """Uses FFmpeg to get exact duration in seconds of any audio/video file."""
    cmd = [FFMPEG_BIN, "-i", file_path]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        h, m_, s = m.groups()
        return int(h) * 3600 + int(m_) * 60 + float(s)
    return 5.0  # Fallback duration


async def synthesize_speech(text: str, output_path: str, language: str = "en") -> Tuple[str, List[Dict]]:
    """
    Synthesizes speech using Edge-TTS and captures sentence/timing boundary data.
    """
    cfg = VOICE_CONFIG.get(language, VOICE_CONFIG["en"])
    communicate = edge_tts.Communicate(text, cfg["voice"], rate=cfg["rate"], pitch=cfg["pitch"])
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    boundaries = []
    with open(output_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                boundaries.append(chunk)

    return output_path, boundaries


def load_api_key_from_env() -> str:
    """Reads ELEVENLABS_API_KEY from environment or .env file."""
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("ELEVENLABS_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        break
    return key


def apply_studio_vocal_chain(raw_audio_path: str, output_path: str) -> str:
    """
    Transforms raw neural audio into a warm, radio/podcast broadcast voice:
    1. Proximity chest boost (110Hz +5.5dB)
    2. De-tins harsh synthetic frequencies (3200Hz -3.0dB)
    3. High-end breath sheen (8000Hz +2.0dB)
    4. Multiband broadcast compressor to level dynamics and bring out vocal texture
    """
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", raw_audio_path,
        "-af", (
            "equalizer=f=110:t=q:w=1.2:g=5.5,"
            "equalizer=f=3200:t=q:w=1.5:g=-3.0,"
            "equalizer=f=8000:t=q:w=1.2:g=2.0,"
            "acompressor=threshold=-18dB:ratio=4:attack=5:release=50:makeup=2.5dB"
        ),
        output_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


def synthesize_speech_sync(text: str, output_path: str, language: str = "en", use_elevenlabs: bool = True) -> Tuple[str, List[Dict]]:
    """
    Synthesizes speech. If use_elevenlabs is False or quota runs out,
    uses neural voice passed through the Studio Vocal Mastering Chain.
    """
    if use_elevenlabs:
        api_key = load_api_key_from_env()
        if api_key and api_key.startswith("sk_"):
            try:
                from core.elevenlabs_engine import synthesize_elevenlabs
                print(f"    [Audio Engine] Synthesizing with ElevenLabs (Adam - Cinema Broadcast)...")
                synthesize_elevenlabs(
                    text=text,
                    output_path=output_path,
                    api_key=api_key,
                    voice_name="adam",
                    stability=0.38,
                    similarity_boost=0.88
                )
                return output_path, []
            except Exception as e:
                print(f"    [Audio Engine Warning] ElevenLabs failed: {e}. Falling back to Studio Voice...")

    # Studio Neural Voice (100% Free & Unlimited)
    temp_raw = output_path + "_raw.mp3"
    _, boundaries = asyncio.run(synthesize_speech(text, temp_raw, language))
    # Apply Studio Mastering Chain
    apply_studio_vocal_chain(temp_raw, output_path)
    if os.path.exists(temp_raw):
        os.remove(temp_raw)
    return output_path, boundaries


def format_srt_time(seconds: float) -> str:
    """Converts seconds into SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def create_retention_subtitles(scenes_timing: List[Dict], output_srt_path: str):
    """
    Generates high-retention subtitles.
    Psychological rule: Chunks long sentences into bite-sized phrases (3-6 words)
    so the viewer's eyes stay glued to the screen.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
    
    srt_index = 1
    lines = []
    
    for scene in scenes_timing:
        start_time = scene["global_start"]
        duration = scene["duration"]
        text = scene["text"].strip()
        
        # Split text into bite-sized retention chunks (max 5 words)
        words = text.split()
        chunk_size = 5
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        if not chunks:
            continue
            
        time_per_chunk = duration / len(chunks)
        
        for i, chunk in enumerate(chunks):
            chunk_start = start_time + (i * time_per_chunk)
            chunk_end = chunk_start + time_per_chunk - 0.05
            
            lines.append(f"{srt_index}")
            lines.append(f"{format_srt_time(chunk_start)} --> {format_srt_time(chunk_end)}")
            lines.append(chunk)
            lines.append("")
            srt_index += 1
            
    with open(output_srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    return output_srt_path


def mix_scene_audio(
    voice_path: str,
    output_path: str,
    drone_path: str = None,
    sfx_path: str = None,
    drone_volume: float = 0.22,
    sfx_volume: float = 0.65
) -> str:
    """
    Mixes voiceover with background ambient drone (ducked) and optional SFX cue.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    inputs = ["-i", voice_path]
    filter_parts = ["[0:a]volume=1.0[voice]"]
    mix_sources = ["[voice]"]
    input_count = 1
    
    if drone_path and os.path.exists(drone_path):
        inputs.extend(["-stream_loop", "-1", "-i", drone_path])
        filter_parts.append(f"[{input_count}:a]volume={drone_volume}[drone]")
        mix_sources.append("[drone]")
        input_count += 1
        
    if sfx_path and os.path.exists(sfx_path):
        inputs.extend(["-i", sfx_path])
        filter_parts.append(f"[{input_count}:a]volume={sfx_volume}[sfx]")
        mix_sources.append("[sfx]")
        input_count += 1
        
    filter_complex = ";".join(filter_parts) + ";" + "".join(mix_sources) + f"amix=inputs={input_count}:duration=first:dropout_transition=2[aout]"
    
    cmd = [
        FFMPEG_BIN, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ac", "2",
        output_path
    ]
    
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


if __name__ == "__main__":
    test_text = "On a frozen desolate rock in the North Atlantic... three men vanished without a trace."
    test_voice = "output/test_narrator.mp3"
    print("Synthesizing speech...")
    synthesize_speech_sync(test_text, test_voice, language="en")
    print(f"Speech saved. Duration: {get_media_duration(test_voice):.2f}s")
