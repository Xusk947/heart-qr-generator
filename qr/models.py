from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class QRConfig:
    """Configuration for QR code generation."""
    
    # Default colors.
    DEFAULT_FILL_COLOR: Final[str] = "black"
    DEFAULT_BACK_COLOR: Final[str] = "white"
    
    fill_color: str = DEFAULT_FILL_COLOR
    back_color: str = DEFAULT_BACK_COLOR
    box_size: int = 20
    border: int = 0
