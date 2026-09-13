#!/usr/bin/env python3
"""Convert a photograph into a deterministic, coloured ASCII-art SVG."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

CHARACTERS = "@%#*+=-:. "


def render_ascii(
    source: Path,
    output: Path,
    columns: int = 112,
    contrast: float = 1.18,
    background: str = "#07111f",
) -> None:
    image = Image.open(source).convert("RGB")
    cell_width, cell_height = 8, 12
    rows = round((image.height / image.width) * columns * (cell_width / cell_height))
    image = image.resize((columns, rows), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    grayscale = ImageOps.grayscale(image)

    width, height = columns * cell_width, rows * cell_height
    lines = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}">'
        ),
        f'<rect width="100%" height="100%" rx="18" fill="{background}"/>',
        (
            '<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            'font-size="12" font-weight="700" dominant-baseline="hanging">'
        ),
    ]

    for y in range(rows):
        for x in range(columns):
            red, green, blue = image.getpixel((x, y))
            luminance = grayscale.getpixel((x, y))
            character = CHARACTERS[
                min(len(CHARACTERS) - 1, luminance * len(CHARACTERS) // 256)
            ]
            if character == " ":
                continue

            boost = 1.16
            colour = tuple(min(255, round(channel * boost)) for channel in (red, green, blue))
            fill = f"#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}"
            lines.append(
                f'<text x="{x * cell_width}" y="{y * cell_height}" '
                f'fill="{fill}">{html.escape(character)}</text>'
            )

    lines.extend(["</g>", "</svg>"])
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input photograph")
    parser.add_argument("output", type=Path, help="Output SVG")
    parser.add_argument("--columns", type=int, default=112, help="ASCII grid width")
    parser.add_argument("--contrast", type=float, default=1.18)
    args = parser.parse_args()

    render_ascii(args.source, args.output, args.columns, args.contrast)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
