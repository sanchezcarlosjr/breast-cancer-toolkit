#!/usr/bin/env python
import argparse
import os

from PIL import Image


def resize_image(input_path, output_path, size=(640, 640)):
    """
    Resize the image to the specified size using LANCZOS interpolation.
    """
    with Image.open(input_path) as img:
        resized_image = img.resize(size, Image.LANCZOS)
        output_path = os.path.join(
            os.path.dirname(output_path), "processed", os.path.basename(output_path)
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        resized_image.save(output_path)
        print(f"Processed image saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Resize an image to 640x640 using LANCZOS interpolation."
    )
    parser.add_argument("input", help="Path to the input image file")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: The file {args.input} does not exist.")
    else:
        resize_image(args.input, args.input)
