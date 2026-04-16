import math
from PIL import Image, ImageDraw
from typing import Tuple, Final

class HeartProcessor:
    """Draws heart lobes around a centered QR code."""

    def add_lobes(
        self, 
        image: Image.Image, 
        color: Tuple[int, int, int], 
        qr_size: Tuple[int, int],
        gap: float = 0.0,
        pattern_image: Image.Image = None
    ) -> Image.Image:
        """Adds lobes to the right and bottom edges. Alignment is based on the center point."""
        # Use the canvas size.
        dim_w, dim_h = image.size
        center_x, center_y = dim_w / 2, dim_h / 2
        
        # Use the square QR size.
        s = qr_size[0]
        radius = s / 2
        
        # Right lobe center.
        # On the right edge: x = center_x + s/2
        # y = center_y
        c1_x = center_x + (s / 2) + gap
        c1_y = center_y
        
        # Bottom lobe center.
        # On the bottom edge: x = center_x
        # y = center_y + s/2
        c2_x = center_x
        c2_y = center_y + (s / 2) + gap
        
        # Bounding boxes
        bbox1 = [c1_x - radius, c1_y - radius, c1_x + radius, c1_y + radius]
        bbox2 = [c2_x - radius, c2_y - radius, c2_x + radius, c2_y + radius]
        
        if pattern_image:
            # Fill lobes with a QR pattern.
            mask = Image.new("L", image.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            
            # RIGHT lobe points Right. From 270 (Top) CW to 90 (Bottom).
            mask_draw.pieslice(bbox1, start=270, end=90, fill=255)
            # BOTTOM lobe points Down. From 0 (Right) CW to 180 (Left).
            mask_draw.pieslice(bbox2, start=0, end=180, fill=255)
            
            image.paste(pattern_image, (0, 0), mask)
        else:
            # Fill lobes with solid color.
            draw = ImageDraw.Draw(image)
            draw.pieslice(bbox1, start=270, end=90, fill=color)
            draw.pieslice(bbox2, start=0, end=180, fill=color)
        
        return image
