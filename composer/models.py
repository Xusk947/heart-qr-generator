from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass(frozen=True)
class CompositionConfig:
    """Settings for QR code composition on a background."""
    
    background_size: Tuple[int, int] = (1000, 1000)
    bg_color: str = "white"
    rotation_angle: float = -225.0
    qr_scale: float = 0.9  # Scale relative to max dimension (0.9 = 10% margin)
    add_heart: bool = True
    heart_color: Tuple[int, int, int] = (0, 0, 0)
    heart_gap: float = 0.0  # Optional spacing between QR and lobes
    use_qr_pattern_lobes: bool = False  # If True, lobes will be filled with QR patterns
    source_text: str = ""  # Input text for pattern generation
    transparent_bg: bool = False  # Make background transparent

