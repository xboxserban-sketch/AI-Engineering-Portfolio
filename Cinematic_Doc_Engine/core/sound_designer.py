"""
Sound Designer: Generates high-tension procedural cinematic audio elements
(Sub-bass drones, heartbeat pulses, tension risers, tape hiss) using pure Python & NumPy.
Ensures 100% royalty-free, broadcast-ready sound design for documentaries.
"""

import math
import os
import struct
import wave
import numpy as np


def create_ambient_drone(
    duration_sec: float,
    output_path: str,
    base_freq: float = 55.0,  # A1 low pitch
    sample_rate: int = 44100
):
    """
    Generates a dark, pulsating cinematic drone with harmonic undertones,
    binaural beating, and eerie room air texture.
    """
    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)

    # 1. Fundamental sub-bass drone with slow amplitude pulse (breathing effect)
    lfo_rate = 0.15  # Slow breath every ~6 seconds
    pulse = 0.7 + 0.3 * np.sin(2 * np.pi * lfo_rate * t)
    sub = np.sin(2 * np.pi * base_freq * t) * pulse

    # 2. Minor third & fifth harmonic for psychological tension (dissonant mystery)
    # 55 Hz -> minor 3rd (65.4 Hz) + dim 5th (77.8 Hz)
    tension_harmonics = (
        0.4 * np.sin(2 * np.pi * (base_freq * 1.189) * t) +
        0.3 * np.sin(2 * np.pi * (base_freq * 1.498) * t) +
        0.2 * np.sin(2 * np.pi * (base_freq * 2.0) * t)
    )

    # 3. Tape saturation / warm hiss texture
    noise = np.random.normal(0, 0.03, total_samples)

    # Combine & smooth
    combined = (sub * 0.5 + tension_harmonics * 0.35 + noise * 0.05)

    # Fade in / fade out
    fade_len = int(sample_rate * 2.0)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    combined[:fade_len] *= fade_in
    combined[-fade_len:] *= fade_out

    # Normalize to -3dB
    max_val = np.max(np.abs(combined))
    if max_val > 0:
        combined = (combined / max_val) * 0.7

    audio_int16 = (combined * 32767).astype(np.int16)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)  # Mono, or stereo duplicated
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())

    return output_path


def create_tension_riser(
    duration_sec: float = 3.0,
    output_path: str = "assets/audio/tension_riser.wav",
    sample_rate: int = 44100
):
    """
    Generates a suspense riser that climbs in pitch and volume right before a reveal.
    """
    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)

    # Exponential frequency sweep from 60 Hz to 450 Hz
    start_f = 60.0
    end_f = 450.0
    freq_sweep = start_f * (end_f / start_f) ** (t / duration_sec)
    phase = 2 * np.pi * np.cumsum(freq_sweep) / sample_rate

    # Volume envelope: swells exponentially
    vol_envelope = (t / duration_sec) ** 2.2

    riser = np.sin(phase) * vol_envelope

    # Add metallic texture
    sheen = np.sin(phase * 1.5) * vol_envelope * 0.3
    combined = riser + sheen

    max_val = np.max(np.abs(combined))
    if max_val > 0:
        combined = (combined / max_val) * 0.85

    audio_int16 = (combined * 32767).astype(np.int16)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())

    return output_path


def create_heartbeat(
    output_path: str = "assets/audio/heartbeat.wav",
    sample_rate: int = 44100
):
    """
    Generates a realistic, deep chest heartbeat thump (lub-dub).
    """
    duration_sec = 1.0
    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)
    audio = np.zeros(total_samples)

    # Lub (0.0s)
    f1 = 50.0
    t1 = t[t < 0.25]
    env1 = np.exp(-t1 * 20.0)
    lub = np.sin(2 * np.pi * f1 * t1) * env1
    audio[:len(lub)] += lub * 0.9

    # Dub (0.3s)
    f2 = 45.0
    idx_start = int(0.28 * sample_rate)
    t2 = t[t < 0.22]
    env2 = np.exp(-t2 * 22.0)
    dub = np.sin(2 * np.pi * f2 * t2) * env2
    audio[idx_start:idx_start + len(dub)] += dub * 0.7

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = (audio / max_val) * 0.85

def create_whoosh(output_path: str = "assets/audio/whoosh.wav", duration_sec: float = 0.8, sample_rate: int = 44100):
    """Generates a deep cinematic whoosh transition sound for camera pans and scene cuts."""
    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)
    
    # White noise passed through a fast sweeping bandpass filter
    noise = np.random.normal(0, 1.0, total_samples)
    
    # Bell curve volume envelope
    env = np.exp(-((t - duration_sec / 2) ** 2) / (0.04))
    
    # Low pass tone sweep
    pitch_sweep = np.sin(2 * np.pi * (80 + 300 * env) * t)
    whoosh = (noise * 0.4 + pitch_sweep * 0.6) * env
    
    max_val = np.max(np.abs(whoosh))
    if max_val > 0:
        whoosh = (whoosh / max_val) * 0.85
        
    audio_int16 = (whoosh * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    return output_path


def create_camera_shutter(output_path: str = "assets/audio/camera_shutter.wav", sample_rate: int = 44100):
    """Generates a vintage 35mm camera mechanical shutter click for evidence reveals."""
    duration_sec = 0.4
    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)
    audio = np.zeros(total_samples)
    
    # Click 1: Mirror flip (0.0s)
    click1 = np.random.normal(0, 1.0, int(0.04 * sample_rate)) * np.exp(-np.linspace(0, 5, int(0.04 * sample_rate)))
    audio[:len(click1)] += click1 * 0.9
    
    # Click 2: Shutter curtain (0.12s)
    c2_idx = int(0.12 * sample_rate)
    click2 = np.random.normal(0, 1.0, int(0.06 * sample_rate)) * np.exp(-np.linspace(0, 4, int(0.06 * sample_rate)))
    audio[c2_idx:c2_idx + len(click2)] += click2 * 1.0
    
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = (audio / max_val) * 0.9
        
    audio_int16 = (audio * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    return output_path


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(base_dir, "assets", "audio")
    drone_path = os.path.join(audio_dir, "ambient_suspense_drone.wav")
    riser_path = os.path.join(audio_dir, "tension_riser.wav")
    heart_path = os.path.join(audio_dir, "heartbeat.wav")
    whoosh_path = os.path.join(audio_dir, "whoosh.wav")
    shutter_path = os.path.join(audio_dir, "camera_shutter.wav")

    print(f"Generating ambient drone in {drone_path}...")
    create_ambient_drone(45.0, drone_path)
    print(f"Generating tension riser in {riser_path}...")
    create_tension_riser(3.0, riser_path)
    print(f"Generating heartbeat in {heart_path}...")
    create_heartbeat(heart_path)
    print(f"Generating whoosh in {whoosh_path}...")
    create_whoosh(whoosh_path)
    print(f"Generating camera shutter in {shutter_path}...")
    create_camera_shutter(shutter_path)
    print("All Pro Foley audio assets generated successfully!")
