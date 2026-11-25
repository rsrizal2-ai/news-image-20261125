#!/usr/bin/env python3
"""Build the 25 Nov 2026 world-news poster (1024x1024) from the generated
five-panel base illustration, overlaying crisp, verified headlines with PIL.
Deterministic: same input -> same output bytes (PNG, fixed settings)."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

SRC = "/home/hatch/workspace/makefun/news-image-20261125-assets/media-generation-news-20261125-base-v2-0-20edeea3-ab75-4dbe-b421-36526f289c08.png"
OUT = "entry.png"
W = H = 1024
NAVY = (10, 18, 38)
RED = (214, 48, 49)
AMBER = (245, 176, 65)
WHITE = (255, 255, 255)
LIGHT = (205, 214, 228)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def caption(draw, box, kicker, headline, sub):
    x0, y0, x1, y1 = box
    overlay = Image.new("RGBA", (x1 - x0, y1 - y0), (6, 12, 28, 215))
    draw._image.paste(overlay, (x0, y0), overlay)
    pad = 12
    cx = x0 + pad
    cy = y0 + 10
    kf = font(BOLD, 15)
    draw.text((cx, cy), kicker, font=kf, fill=AMBER)
    cy += 24
    hf = font(BOLD, 26)
    for ln in wrap(draw, headline, hf, x1 - x0 - 2 * pad):
        draw.text((cx, cy), ln, font=hf, fill=WHITE)
        cy += 30
    sf = font(REG, 17)
    for ln in wrap(draw, sub, sf, x1 - x0 - 2 * pad):
        draw.text((cx, cy), ln, font=sf, fill=LIGHT)
        cy += 21

def main():
    base = Image.open(SRC).convert("RGB")
    S = base.size[0]
    def crop(fx0, fy0, fx1, fy1):
        return base.crop((int(fx0 * S), int(fy0 * S), int(fx1 * S), int(fy1 * S)))

    panels = [
        crop(0.020, 0.020, 0.360, 0.475),   # chip / markets
        crop(0.370, 0.020, 0.685, 0.475),   # tanker / Hormuz
        crop(0.695, 0.020, 0.975, 0.475),   # supermarket / Cartagena
        crop(0.020, 0.490, 0.495, 0.985),   # trophy / Senegal
        crop(0.505, 0.490, 0.980, 0.985),   # astronaut / space
    ]
    canvas = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Masthead
    draw.text((28, 16), "THE WORLD TODAY", font=font(BOLD, 52), fill=WHITE)
    draw.text((28, 74), "WEDNESDAY  25  NOVEMBER  2026", font=font(BOLD, 24), fill=AMBER)
    draw.rectangle([W - 218, 22, W - 28, 82], fill=RED)
    draw.text((W - 203, 32), "5 STORIES", font=font(BOLD, 30), fill=WHITE)
    draw.rectangle([0, 112, W, 118], fill=RED)

    # Panel geometry: header 118, top row y 126..516 (390), bottom 524..914 (390), footer 922..1024
    top_h, bot_h = 390, 390
    top_y, bot_y = 126, 524
    tw = (W - 2 * 16 - 2 * 10) // 3  # 322
    bw = (W - 2 * 16 - 10) // 2      # 491
    geom = [
        (16, top_y, 16 + tw, top_y + top_h),
        (16 + tw + 10, top_y, 16 + 2 * tw + 10, top_y + top_h),
        (16 + 2 * tw + 20, top_y, 16 + 3 * tw + 20, top_y + top_h),
        (16, bot_y, 16 + bw, bot_y + bot_h),
        (16 + bw + 10, bot_y, 16 + 2 * bw + 10, bot_y + bot_h),
    ]
    for img, (x0, y0, x1, y1) in zip(panels, geom):
        canvas.paste(img.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
        draw.rectangle([x0, y0, x1, y1], outline=(255, 255, 255), width=3)

    caps = [
        ("MARKETS  •  AI SELLOFF", "NVIDIA FALLS 7%",
         "AI doubts sweep Asia — Japan's Nikkei drops 2.76%."),
        ("MIDDLE EAST  •  HORMUZ", "TWO TANKERS HIT MINES",
         "Blasts in the Strait of Hormuz rattle oil markets."),
        ("COLOMBIA  •  CARTAGENA", "HOSTAGES IN SUPERMARKET",
         "Armed men hold about 20 people in Cartagena."),
        ("FOOTBALL  •  AFCON", "SENEGAL CHAMPIONS AGAIN",
         "Africa Cup title restored after CAS ruling."),
        ("SPACE  •  HISTORY", "PAKISTAN'S FIRST ASTRONAUT",
         "Reaches China's space station as Shenzhou-24 launches."),
    ]
    for (x0, y0, x1, y1), (k, h, s) in zip(geom, caps):
        bar_h = 148 if y1 - y0 == top_h else 132
        caption(draw, (x0, y1 - bar_h, x1, y1), k, h, s)

    # Footer strip
    draw.rectangle([0, 922, W, H], fill=(6, 12, 28))
    draw.text((28, 936), "ALSO TODAY:", font=font(BOLD, 20), fill=AMBER)
    draw.text((28, 964),
              "Ukraine confirms strike on a Russian ship in the Gulf of Finland",
              font=font(REG, 19), fill=WHITE)
    draw.text((28, 990),
              "Democrats win a U.S. House majority of at least 259 seats",
              font=font(REG, 19), fill=WHITE)
    # Quantize to 256 colours so the PNG stays under the 1 MiB limit.
    canvas = canvas.quantize(colors=256, method=Image.MEDIANCUT,
                             dither=Image.FLOYDSTEINBERG).convert("RGB")
    canvas.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)

if __name__ == "__main__":
    main()
