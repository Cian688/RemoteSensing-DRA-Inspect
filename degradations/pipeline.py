from __future__ import annotations

import hashlib
import io
from typing import Dict, Iterable

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

DEGRADATION_NAMES = (
    'clean',
    'noise',
    'blur',
    'light',
    'lowres',
    'jpeg',
    'color',
    'haze',
    'cloudveil',
    'cloud_like_veil',
)


def _to_uint8(image: np.ndarray) -> np.ndarray:
    return np.clip(image, 0, 255).astype(np.uint8)


def _deterministic_rng(image: Image.Image, name: str, severity: float) -> np.random.Generator:
    array = np.asarray(image.convert('RGB'), dtype=np.uint8)
    payload = name.encode('utf-8') + b'|' + repr(float(severity)).encode('utf-8') + b'|' + array.tobytes()
    digest = hashlib.sha256(payload).digest()
    seed = int.from_bytes(digest[:8], byteorder='little', signed=False)
    return np.random.default_rng(seed)


def apply_degradation(image: Image.Image, name: str, severity: float = 1.0) -> Image.Image:
    image = image.convert('RGB')
    if name == 'clean':
        return image
    if name == 'noise':
        rng = _deterministic_rng(image, name, severity)
        array = np.asarray(image).astype(np.float32)
        sigma = 8.0 * severity
        noisy = array + rng.normal(0.0, sigma, size=array.shape)
        return Image.fromarray(_to_uint8(noisy))
    if name == 'blur':
        radius = max(0.5, 1.5 * severity)
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    if name == 'light':
        brightness_factor = max(0.5, 1.0 - 0.25 * severity)
        contrast_factor = max(0.7, 1.0 - 0.10 * severity)
        image = ImageEnhance.Brightness(image).enhance(brightness_factor)
        return ImageEnhance.Contrast(image).enhance(contrast_factor)
    if name == 'lowres':
        width, height = image.size
        scale = max(2, int(round(2 + severity)))
        down = image.resize((max(1, width // scale), max(1, height // scale)), Image.BILINEAR)
        return down.resize((width, height), Image.BILINEAR)
    if name == 'jpeg':
        quality = int(max(15, 75 - 30 * severity))
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)
        return Image.open(buffer).convert('RGB')
    if name == 'color':
        array = np.asarray(image).astype(np.float32)
        shift = np.array([10.0, -6.0, 4.0], dtype=np.float32) * severity
        return Image.fromarray(_to_uint8(array + shift.reshape(1, 1, 3)))
    if name == 'haze':
        array = np.asarray(image).astype(np.float32)
        airlight = 255.0 * min(0.45, 0.18 * severity)
        transmission = max(0.35, 1.0 - 0.28 * severity)
        hazy = transmission * array + (1.0 - transmission) * airlight
        hazy = Image.fromarray(_to_uint8(hazy))
        return ImageEnhance.Contrast(hazy).enhance(max(0.55, 1.0 - 0.18 * severity))
    if name in {'cloudveil', 'cloud_like_veil'}:
        rng = _deterministic_rng(image, name, severity)
        array = np.asarray(image).astype(np.float32)
        width, height = image.size
        low_w = max(8, width // 8)
        low_h = max(8, height // 8)
        mask = rng.uniform(0.0, 1.0, size=(low_h, low_w)).astype(np.float32)
        mask_img = Image.fromarray(_to_uint8(mask * 255.0)).resize((width, height), Image.BILINEAR)
        blur_radius = max(3.0, 6.0 * severity)
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        mask_arr = np.asarray(mask_img).astype(np.float32) / 255.0
        veil_strength = min(0.6, 0.22 * severity)
        veil = np.clip(mask_arr * veil_strength, 0.0, 1.0)[..., None]
        whitened = array * (1.0 - veil) + 255.0 * veil
        whitened = Image.fromarray(_to_uint8(whitened))
        return ImageEnhance.Contrast(whitened).enhance(max(0.5, 1.0 - 0.22 * severity))
    raise ValueError(f'Unsupported degradation: {name}')


def generate_variants(image: Image.Image, names: Iterable[str], severity: float = 1.0) -> Dict[str, Image.Image]:
    return {name: apply_degradation(image, name=name, severity=severity) for name in names}
