#!/usr/bin/env python3
"""
Extract selected pages/figures from PDFs into PNGs for use on the Quarto website.

Usage examples
--------------
# Example for Solanum paper (replace PDF path + page numbers once you confirm them)
python scripts/extract_figures.py \
  --pdf "/path/to/solanum.pdf" \
  --outdir "images/projects" \
  --extract "solanum_fig1:3:0,0,1,0.55" \
  --extract "solanum_fig3:6:0,0,1,0.75"

Notes
-----
- Page numbers are 0-indexed (Quarto/web screenshot convention).
- Crop boxes are relative fractions: x0,y0,x1,y1 in [0,1] of page width/height.
"""
import argparse
import os
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageChops

def tight_crop(img, border=10):
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - border)
    y0 = max(0, y0 - border)
    x1 = min(img.size[0], x1 + border)
    y1 = min(img.size[1], y1 + border)
    return img.crop((x0, y0, x1, y1))

def render_page(pdf_path, pno, zoom=2):
    doc = fitz.open(pdf_path)
    page = doc.load_page(pno)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img

def parse_extract(spec: str):
    # name:page:x0,y0,x1,y1
    name, page, box = spec.split(":")
    pno = int(page)
    x0, y0, x1, y1 = map(float, box.split(","))
    return name, pno, (x0, y0, x1, y1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="Path to PDF")
    ap.add_argument("--outdir", required=True, help="Output directory for PNGs")
    ap.add_argument("--extract", action="append", default=[], help="Extraction spec name:page:x0,y0,x1,y1")
    ap.add_argument("--zoom", type=float, default=2.0, help="Render zoom factor")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for spec in args.extract:
        name, pno, (x0, y0, x1, y1) = parse_extract(spec)
        img = render_page(args.pdf, pno, zoom=args.zoom)
        img = tight_crop(img, border=5)
        w, h = img.size
        crop = (int(x0*w), int(y0*h), int(x1*w), int(y1*h))
        out = outdir / f"{name}.png"
        img.crop(crop).save(out, format="PNG", optimize=True)
        print(f"Wrote {out}")

if __name__ == "__main__":
    main()
