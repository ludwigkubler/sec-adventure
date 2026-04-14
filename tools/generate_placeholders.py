#!/usr/bin/env python3
"""Placeholder PNG stilizzati per le 3 stanze senza SD.
Pennelli PIL, gradient + elementi geometrici semplici per dare atmosfera.
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "rooms"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 960, 576

def vertical_gradient(top, bot):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(top[0] * (1-t) + bot[0] * t)
        g = int(top[1] * (1-t) + bot[1] * t)
        b = int(top[2] * (1-t) + bot[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img


def add_noise(img, amount=12):
    px = img.load()
    for y in range(H):
        for x in range(W):
            n = random.randint(-amount, amount)
            r, g, b = px[x, y]
            px[x, y] = (max(0,min(255,r+n)), max(0,min(255,g+n)), max(0,min(255,b+n)))
    return img


def vignette(img):
    vg = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(vg)
    for i in range(25):
        a = int(255 - i*10)
        d.ellipse((-40-i*5, -40-i*5, W+40+i*5, H+40+i*5), outline=a)
    vg = vg.filter(ImageFilter.GaussianBlur(25))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(img, black, vg)


# ─── bivio_giungla — crocevia con totem ───
def bivio_giungla():
    random.seed(42)
    img = vertical_gradient((22, 50, 28), (10, 30, 18))  # verde scuro
    d = ImageDraw.Draw(img)
    # Nebbia in basso
    for _ in range(120):
        x = random.randint(0, W); y = random.randint(H-200, H)
        r = random.randint(30, 80)
        d.ellipse((x-r, y-r, x+r, y+r), fill=(40, 60, 40))
    # Tronchi d'albero laterali sfumati
    for _ in range(5):
        x = random.choice([random.randint(0, 120), random.randint(W-120, W)])
        w = random.randint(30, 80)
        d.rectangle((x, 0, x+w, H), fill=(30, 20, 14))
    # Totem centrale al centro basso
    cx, cy = W//2, H-140
    # Base
    d.rectangle((cx-70, cy, cx+70, cy+140), fill=(55, 45, 38))
    d.rectangle((cx-60, cy+5, cx+60, cy+135), fill=(35, 28, 22))
    # Figure sul totem (rettangoli con occhi)
    for i, color in enumerate([(180, 120, 60), (120, 180, 180), (200, 100, 100)]):
        y = cy + 10 + i*40
        d.rectangle((cx-45, y, cx+45, y+35), outline=color, width=2)
        # occhio
        d.ellipse((cx-8, y+10, cx+8, y+26), fill=color)
        d.ellipse((cx-4, y+14, cx+4, y+22), fill=(10, 10, 10))
    # Sentieri a Y che convergono
    d.polygon([(W//2 - 20, H), (W//2 + 20, H), (W//2, cy+140)], fill=(80, 70, 50))
    img = add_noise(img, 8)
    img = vignette(img)
    img.save(OUT / "bivio_giungla.png", "PNG", optimize=True)
    print("  ✓ bivio_giungla")


# ─── corridoio_perduto — muro di nomi ───
def corridoio_perduto():
    random.seed(43)
    img = vertical_gradient((28, 30, 38), (12, 14, 22))  # blu-viola scuro
    d = ImageDraw.Draw(img)
    # Prospettiva corridoio: muri laterali che si chiudono
    # Muro sinistro
    d.polygon([(0,0),(W//2-30,H//3),(W//2-30,H*2//3),(0,H)], fill=(18, 18, 26))
    # Muro destro
    d.polygon([(W,0),(W//2+30,H//3),(W//2+30,H*2//3),(W,H)], fill=(18, 18, 26))
    # Soffitto
    d.polygon([(0,0),(W,0),(W//2+30,H//3),(W//2-30,H//3)], fill=(8, 10, 16))
    # Pavimento
    d.polygon([(0,H),(W,H),(W//2+30,H*2//3),(W//2-30,H*2//3)], fill=(10, 12, 18))
    # Nomi incisi sui muri (linee orizzontali sottili = testo stilizzato)
    for side in [-1, 1]:
        for row in range(28):
            y = 100 + row*14
            if y > H-80: break
            # Restringimento verso il fondo
            factor = 1 - abs(y - H//2) / (H//2) * 0.5
            x_start = 20 if side == -1 else W - int(180*factor) - 20
            x_end = 20 + int(160*factor) if side == -1 else W - 20
            gray = random.randint(50, 90)
            # Simula linee di testo
            x = x_start
            while x < x_end:
                word_w = random.randint(15, 40)
                d.line((x, y, min(x+word_w, x_end), y), fill=(gray, gray-4, gray-8), width=1)
                x += word_w + random.randint(4, 8)
    # Fondo: muro liscio con alone di luce fioca
    d.rectangle((W//2-30, H//3, W//2+30, H*2//3), fill=(14, 16, 22))
    for i in range(15):
        r = 35 - i
        alpha_col = max(0, 100 - i*7)
        d.ellipse((W//2-r, H//2-r*0.7, W//2+r, H//2+r*0.7), fill=(alpha_col+14, alpha_col+14, alpha_col+22))
    img = add_noise(img, 6)
    img = vignette(img)
    img.save(OUT / "corridoio_perduto.png", "PNG", optimize=True)
    print("  ✓ corridoio_perduto")


# ─── cunicolo_nascosto — altarino con lampada ───
def cunicolo_nascosto():
    random.seed(44)
    img = vertical_gradient((35, 25, 15), (15, 10, 6))  # marrone scuro
    d = ImageDraw.Draw(img)
    # Parete ovale sfumata (tunnel)
    cx, cy = W//2, H//2
    # Altare al centro
    alt_w, alt_h = 160, 80
    alt_x, alt_y = cx - alt_w//2, H - 180
    d.rectangle((alt_x, alt_y, alt_x+alt_w, alt_y+alt_h), fill=(60, 55, 45))
    d.rectangle((alt_x+5, alt_y+5, alt_x+alt_w-5, alt_y+alt_h-5), fill=(45, 40, 32))
    # Cupola di vetro sull'altare
    d.ellipse((cx-40, alt_y-55, cx+40, alt_y+15), outline=(200, 200, 220), width=2)
    # Lampada dentro la cupola
    d.rectangle((cx-8, alt_y-15, cx+8, alt_y), fill=(140, 90, 50))  # base lampada
    # Fiamma (alone di luce caldo)
    for r in range(80, 10, -5):
        alpha = int(255 * (1 - r/80) * 0.6)
        # Crea un'ombra sfumata gialla
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((cx-r, alt_y-30-r, cx+r, alt_y-30+r), fill=(255, 220, 120, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    # Punto bianco centrale = fiamma
    d.ellipse((cx-5, alt_y-34, cx+5, alt_y-24), fill=(255, 255, 220))
    # Polvere (punti sparsi in basso)
    for _ in range(60):
        x = random.randint(alt_x-20, alt_x+alt_w+20)
        y = random.randint(alt_y+alt_h, H)
        d.ellipse((x, y, x+2, y+2), fill=(100, 85, 70))
    img = add_noise(img, 6)
    img = vignette(img)
    img.save(OUT / "cunicolo_nascosto.png", "PNG", optimize=True)
    print("  ✓ cunicolo_nascosto")


if __name__ == "__main__":
    print("Generating 3 atmospheric placeholders:")
    bivio_giungla()
    corridoio_perduto()
    cunicolo_nascosto()
    print("Done.")
