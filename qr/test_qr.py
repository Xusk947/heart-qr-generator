import os
import io
from qr.generator import QRCodeGenerator
from qr.models import QRConfig

def test_generation():
    generator = QRCodeGenerator()
    
    # Test case 1: some_text
    print("Testing 'some_text' generation...")
    text_data = "some_text"
    buffer = generator.generate(text_data)
    assert isinstance(buffer, io.BytesIO), "Output should be BytesIO"
    assert buffer.getbuffer().nbytes > 0, "Buffer should not be empty"
    print(f"Success: Generated {buffer.getbuffer().nbytes} bytes for '{text_data}'")

    # Test case 2: google.com with custom color
    print("\nTesting 'google.com' generation with custom colors...")
    url_data = "google.com"
    config = QRConfig(fill_color="blue", back_color="yellow")
    buffer_custom = generator.generate(url_data, config)
    assert isinstance(buffer_custom, io.BytesIO), "Output should be BytesIO"
    assert buffer_custom.getbuffer().nbytes > 0, "Buffer should not be empty"
    print(f"Success: Generated {buffer_custom.getbuffer().nbytes} bytes for '{url_data}' (Blue on Yellow)")

    # Save for manual check
    # output_path = "test_qr_output.png"
    # with open(output_path, "wb") as f:
    #     f.write(buffer_custom.getvalue())
    # print(f"\nSaved test image to {output_path}")

if __name__ == "__main__":
    test_generation()
    print("\nAll tests passed successfully!")
