import io
import random
from PIL import Image
from .models import CompositionConfig
from .heart.processor import HeartProcessor
from qr.generator import QRCodeGenerator
from qr.models import QRConfig

class ImageComposer:
    """Rotates and centers QR codes on backgrounds."""

    def compose_centered(
        self, 
        qr_buffer: io.BytesIO, 
        config: CompositionConfig = CompositionConfig()
    ) -> io.BytesIO:
        """Rotates and centers the QR code on a new background."""
        # Load images
        # Load as RGBA so we can preserve transparency if the QR code has a transparent background
        qr_img = Image.open(qr_buffer).convert("RGBA")
        
        # Fix sub-pixel shifts by using a shared canvas size.
        # Rotate all images on same-sized canvases to match centers.
        base_size = max(qr_img.width, qr_img.height)
        # Expanded size for rotation safety
        canvas_dim = int(base_size * 2.5) 
        
        def center_on_canvas(img: Image.Image, dim: int) -> Image.Image:
            # Use RGBA to support transparency in bounding boxes.
            canvas = Image.new("RGBA", (dim, dim), (255, 255, 255, 0))
            off = (dim - img.width) // 2, (dim - img.height) // 2
            canvas.paste(img.convert("RGBA"), off)
            return canvas

        # Use the same canvas size for both images.
        qr_canvas = center_on_canvas(qr_img, canvas_dim)
        
        if config.add_heart:
            heart_proc = HeartProcessor()
            
            # Generate and rotate pattern on the shared canvas.
            pattern_canvas = None
            if config.use_qr_pattern_lobes and config.source_text:
                # 1. Repeat source text to ensure enough pattern density
                text_list = list(config.source_text)
                random.shuffle(text_list)
                shuffled_text = ("".join(text_list)) * max(1, (300 // len(config.source_text)) + 1)
                
                qr_gen = QRCodeGenerator()
                hex_color = f"#{config.heart_color[0]:02x}{config.heart_color[1]:02x}{config.heart_color[2]:02x}"
                
                # Use custom background color for the pattern if not transparent
                if config.transparent_bg:
                    bg_pattern = "transparent"
                elif isinstance(config.bg_color, tuple):
                    bg_pattern = f"#{config.bg_color[0]:02x}{config.bg_color[1]:02x}{config.bg_color[2]:02x}"
                else:
                    bg_pattern = config.bg_color

                pattern_config = QRConfig(
                    fill_color=hex_color, 
                    box_size=20,
                    back_color=bg_pattern,
                    border=0
                )
                pattern_buffer = qr_gen.generate(shuffled_text, pattern_config)
                # Keep RGBA for pattern so we can align transparency
                raw_pattern = Image.open(pattern_buffer).convert("RGBA")
                pattern_canvas = center_on_canvas(raw_pattern, canvas_dim)
                
            # Add heart lobes.
            # Pass unrotated canvas to HeartProcessor.
            qr_canvas = heart_proc.add_lobes(
                qr_canvas, 
                config.heart_color, 
                qr_img.size, # Using the original QR dimensions for math
                gap=config.heart_gap,
                pattern_image=pattern_canvas
            )
            
            # Rotate the combined shape.
            rotated_qr = qr_canvas.rotate(
                config.rotation_angle, 
                resample=Image.BILINEAR,
                fillcolor=(255, 255, 255, 0)
            )
        else:
            # If no heart, just rotate the base qr
            rotated_qr = qr_canvas.rotate(
                config.rotation_angle, 
                resample=Image.BILINEAR,
                fillcolor=(255, 255, 255, 0)
            )

        # 2. Crop to remove transparent padding.
        bbox = rotated_qr.getbbox()
        if bbox:
            rotated_qr = rotated_qr.crop(bbox)

        # 3. Create background.
        bg_w, bg_h = config.background_size
        if config.transparent_bg:
            background = Image.new("RGBA", (bg_w, bg_h), (0, 0, 0, 0))
        else:
            bg_col = config.bg_color if isinstance(config.bg_color, tuple) else config.bg_color
            background = Image.new("RGB", (bg_w, bg_h), bg_col)

        # 4. Scale heart to fit background.
        target_size = int(min(bg_w, bg_h) * config.qr_scale)
        
        # Scale the resulting heart shape while maintaining aspect ratio
        current_w, current_h = rotated_qr.size
        scale = target_size / max(current_w, current_h)
        new_size = (int(current_w * scale), int(current_h * scale))
        rotated_qr = rotated_qr.resize(new_size, Image.LANCZOS)

        # 5. Center the heart.
        qr_w, qr_h = rotated_qr.size
        offset = ((bg_w - qr_w) // 2, (bg_h - qr_h) // 2)

        # 6. Paste onto background using alpha mask.
        if config.transparent_bg:
            # For RGBA to RGBA, alpha pasting is standard
            background.paste(rotated_qr, offset, mask=rotated_qr)
        else:
            # Ensure background RGB blends with rotated_qr's alpha
            background.paste(rotated_qr, offset, mask=rotated_qr)

        # Save to buffer
        output_buffer = io.BytesIO()
        background.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        return output_buffer
