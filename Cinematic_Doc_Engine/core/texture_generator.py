"""
Texture Generator: Creates high-resolution organic film grain and vignette textures
using PIL and NumPy to give documentary visuals a cinematic, vintage film look (1080p/4K).
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def generate_vignette(width: int = 1920, height: int = 1080, output_path: str = "assets/overlays/vignette.png", intensity: float = 0.75):
    """
    Generates a smooth radial dark vignette mask.
    Center is transparent; edges fade to deep black/noir.
    """
    # Create radial gradient
    y, x = np.ogrid[:height, :width]
    center_y, center_x = height / 2.0, width / 2.0
    
    # Normalized distance from center (0 at center, 1 at corner)
    max_radius = np.sqrt(center_x**2 + center_y**2)
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2) / max_radius

    # Smooth curve starting around 0.4 from center
    vignette_alpha = np.clip((dist - 0.35) / 0.65, 0, 1) ** 2.2
    vignette_alpha = (vignette_alpha * (intensity * 255)).astype(np.uint8)

    # RGBA image: black with computed alpha
    img_array = np.zeros((height, width, 4), dtype=np.uint8)
    img_array[..., :3] = 0  # Black color
    img_array[..., 3] = vignette_alpha  # Alpha

    img = Image.fromarray(img_array)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path


def generate_film_grain(width: int = 1920, height: int = 1080, output_path: str = "assets/overlays/film_grain.png", intensity: float = 0.12):
    """
    Generates an organic 35mm film grain overlay.
    """
    # Random Gaussian noise
    noise = np.random.normal(128, 28, (height, width)).astype(np.uint8)
    
    # Slight blur to simulate analog grain clusters instead of digital salt-and-pepper noise
    noise_img = Image.fromarray(noise)
    noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=0.7))

    # Convert to RGBA overlay with gentle opacity
    noise_arr = np.array(noise_img)
    alpha = np.full((height, width), int(intensity * 255), dtype=np.uint8)
    
    rgba = np.stack([noise_arr, noise_arr, noise_arr, alpha], axis=-1)
    img = Image.fromarray(rgba)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    overlay_dir = os.path.join(base_dir, "assets", "overlays")
    
    vignette_path = os.path.join(overlay_dir, "vignette.png")
    grain_path = os.path.join(overlay_dir, "film_grain.png")
    
    print("Generating cinematic vignette...")
    generate_vignette(1920, 1080, vignette_path)
    print("Generating 35mm film grain texture...")
    generate_film_grain(1920, 1080, grain_path)
    print("Visual textures generated successfully!")
