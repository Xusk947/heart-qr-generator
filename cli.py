import argparse
from qr.models import QRConfig
from qr.generator import QRCodeGenerator
from composer.composer import ImageComposer
from composer.models import CompositionConfig

def hex_to_rgb(value: str):
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

def main():
    parser = argparse.ArgumentParser(description="Generate heart-shaped QR codes.")
    parser.add_argument("text", help="The text or URL for the QR code.")
    parser.add_argument("-o", "--output", default="heart_qr.png", help="Output file path.")
    parser.add_argument("-c", "--color", default="#c80000", help="Heart color in hex (e.g., #ff0000).")
    parser.add_argument("-s", "--size", type=int, default=1000, help="Output image size in pixels.")
    parser.add_argument("-g", "--gap", type=float, default=20.0, help="Gap between QR and heart lobes.")
    parser.add_argument("-bg", "--bg-color", default="#ffffff", help="Background color in hex (only if --solid-bg is used).")
    parser.add_argument("--solid-bg", action="store_true", help="Use a solid background instead of transparent.")

    args = parser.parse_args()

    target_color = hex_to_rgb(args.color)
    bg_color = hex_to_rgb(args.bg_color)

    print(f"Generating QR code for {args.text}")
    qr_gen = QRCodeGenerator()
    qr_config = QRConfig(
        fill_color=args.color,
        back_color=args.bg_color if args.solid_bg else "transparent"
    )
    qr_buffer = qr_gen.generate(args.text, qr_config)

    print("Formatting heart geometry...")
    composer = ImageComposer()
    config = CompositionConfig(
        background_size=(args.size, args.size),
        bg_color=bg_color,
        transparent_bg=not args.solid_bg,
        qr_scale=0.9,
        add_heart=True,
        heart_color=target_color,
        heart_gap=args.gap,
        use_qr_pattern_lobes=True,
        source_text=args.text
    )

    final_buffer = composer.compose_centered(qr_buffer, config)

    with open(args.output, "wb") as f:
        f.write(final_buffer.getvalue())
    
    print(f"File saved to {args.output}")

if __name__ == "__main__":
    main()
