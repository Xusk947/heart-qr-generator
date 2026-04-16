from abc import ABC, abstractmethod
from io import BytesIO
from .models import QRConfig

class IQRGenerator(ABC):
    """Interface for QR code generation."""

    @abstractmethod
    def generate(self, data: str, config: QRConfig) -> BytesIO:
        """Generates a QR code image buffer."""
        pass
