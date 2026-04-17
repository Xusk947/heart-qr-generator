import io
from PIL import Image
from qr.generator import QRCodeGenerator
from qr.models import QRConfig
from composer.models import CompositionConfig

text = "https://admin-jdm2uur05sg6uv0nm9nfwxep.back.nabi.dev/api/files/download?path=%2Fbuckets%2Fpocketbase%2FUntitled.jpg"
qr_gen = QRCodeGenerator()
qr_config = QRConfig(fill_color="black", back_color="white", border=0)
qr_buffer = qr_gen.generate(text, qr_config)
qr_img = Image.open(qr_buffer)
print(f"Main QR size: {qr_img.size}")

s = qr_img.width
gap = 20
heart_extent = s + gap + s/2 # from left edge of square to right edge of lobe
print(f"Heart unrotated extent from center: {s/2 + gap + s/2} = {s + gap}")
print(f"Required pattern size: {2*(s + gap)}")

# Now simulate pattern generation
text_list = list(text)
shuffled_text = ("".join(text_list)) * max(1, (300 // len(text)) + 1)
pattern_config = QRConfig(fill_color="black", box_size=20, back_color="white", border=0)
pattern_buffer = qr_gen.generate(shuffled_text, pattern_config)
pattern_img = Image.open(pattern_buffer)
print(f"Pattern QR size: {pattern_img.size}")
