# ASCII portrait generator

`generate_ascii_portrait.py` converts a local photograph into a coloured ASCII-art SVG. The profile README displays a generated SVG from `assets/`.

## Requirements

- Python 3.9 or newer
- Pillow (`python -m pip install Pillow`)

## Run

From the repository root:

```bash
python scripts/generate_ascii_portrait.py path/to/photo.jpg assets/alif-ascii-portrait.svg
```

Optional controls:

```bash
python scripts/generate_ascii_portrait.py path/to/photo.jpg assets/alif-ascii-portrait.svg --columns 112 --contrast 1.18
```

- `--columns` sets the number of character cells across the image (default: `112`).
- `--contrast` adjusts input image contrast before character selection (default: `1.18`).
- Output is a self-contained SVG with coloured text cells; the original image is not embedded.

## Privacy

Use a photograph stored locally and avoid committing the source image unless you intend to publish it. Review the generated SVG before sharing it publicly.
