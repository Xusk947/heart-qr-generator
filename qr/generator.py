import io
import qrcode
from qrcode.image.pil import PilImage
from .interface import IQRGenerator
from .models import QRConfig

class QRCodeGenerator(IQRGenerator):
    """QR code generator using the qrcode library."""

    def generate(self, data: str, config: QRConfig = QRConfig()) -> io.BytesIO:
        """Generates a QR code image buffer."""
        
        Args:
            data: Content to encode.
            config: Styling configuration.
            
        Returns:
            io.BytesIO: Buffer containing the PNG image.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=config.box_size,
            border=config.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img: PilImage = qr.make_image(
            fill_color=config.fill_color,
            back_color=config.back_color
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        return buffer
