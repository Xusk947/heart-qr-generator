import io
from qr.models import QRConfig
from qr.generator import QRCodeGenerator
from composer.composer import ImageComposer
from composer.models import CompositionConfig

def test_composition():
    # 1. Generate QR Code (Red)
    print("Generating red QR code...")
    target_color = (200, 0, 0)  # Dark red
    qr_gen = QRCodeGenerator()
    qr_config = QRConfig(
        fill_color=f"#{target_color[0]:02x}{target_color[1]:02x}{target_color[2]:02x}",
        back_color="transparent"
    )
    qr_buffer = qr_gen.generate("google.com", qr_config)
    
    # 2. Compose heart
    print("Composing heart shape with QR patterns and gap...")
    composer = ImageComposer()
    config = CompositionConfig(
        background_size=(1000, 1000),
        transparent_bg=True,
        qr_scale=0.9,
        add_heart=True,
        heart_color=target_color,
        heart_gap=20.0,
        use_qr_pattern_lobes=True,
        source_text="google.com"
    )
    final_buffer = composer.compose_centered(qr_buffer, config)
    
    # 3. Validation
    assert isinstance(final_buffer, io.BytesIO)
    assert final_buffer.getbuffer().nbytes > 0
    print(f"Success: Composed image size is {final_buffer.getbuffer().nbytes} bytes")

    # 4. Save for manual inspection
    output_filename = "composed_qr_test.png"
    with open(output_filename, "wb") as f:
        f.write(final_buffer.getvalue())
    print(f"Saved result to {output_filename}")

if __name__ == "__main__":
    test_composition()
    print("\nComposer test passed!")
