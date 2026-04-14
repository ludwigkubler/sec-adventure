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


def re_automa_portrait():
    """Ritratto stilizzato del Re-Automa — automa di rame patinato con corona di ferro."""
    random.seed(77)
    SW, SH = 512, 512
    img = Image.new("RGB", (SW, SH))
    # gradiente radial dorato → verdigris
    px = img.load()
    for y in range(SH):
        for x in range(SW):
            dx = (x - SW/2) / (SW/2)
            dy = (y - SH/2) / (SH/2)
            d = (dx*dx + dy*dy) ** 0.5
            t = max(0, min(1, d))
            r = int(35 + 25*(1-t))
            g = int(45 + 35*(1-t))
            b = int(48 + 10*(1-t))
            px[x, y] = (r, g, b)
    d = ImageDraw.Draw(img)
    cx, cy = SW//2, SH//2 + 20
    # Corpo: spalle stilizzate
    d.polygon([(cx-160, SH), (cx-110, cy+50), (cx+110, cy+50), (cx+160, SH)], fill=(80, 110, 90))
    d.polygon([(cx-150, SH), (cx-100, cy+60), (cx+100, cy+60), (cx+150, SH)], fill=(105, 135, 110))
    # Collo
    d.rectangle((cx-30, cy-20, cx+30, cy+70), fill=(95, 125, 100))
    # Testa (ovale/scudo)
    d.ellipse((cx-100, cy-160, cx+100, cy+30), fill=(140, 165, 135))
    # Dettagli placcature testa
    d.ellipse((cx-100, cy-160, cx+100, cy+30), outline=(60, 80, 60), width=3)
    # Maschera frontale più chiara
    d.ellipse((cx-75, cy-130, cx+75, cy+10), fill=(165, 185, 155))
    # Rivetti intorno
    for angle in range(0, 360, 30):
        import math
        rx = cx + int(92 * math.cos(math.radians(angle-90)))
        ry = cy - 65 + int(92 * math.sin(math.radians(angle-90)))
        d.ellipse((rx-5, ry-5, rx+5, ry+5), fill=(70, 90, 70), outline=(40, 55, 40))
    # Fessure occhi
    eye_y = cy - 85
    d.rectangle((cx-50, eye_y-3, cx-18, eye_y+3), fill=(10, 10, 12))
    d.rectangle((cx+18, eye_y-3, cx+50, eye_y+3), fill=(10, 10, 12))
    # Luce dentro le fessure (glow verde)
    for r_off in range(12, 2, -2):
        alpha = 200 - r_off * 15
        overlay = Image.new("RGBA", img.size, (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.rectangle((cx-48, eye_y-2, cx-20, eye_y+2), fill=(120, 220, 180, max(0, alpha)))
        od.rectangle((cx+20, eye_y-2, cx+48, eye_y+2), fill=(120, 220, 180, max(0, alpha)))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    # Linea della bocca (sottile, ferma)
    d.line((cx-30, cy-25, cx+30, cy-25), fill=(50, 65, 50), width=2)
    # Corona: ferro grezzo, 5 punte basse
    crown_y = cy - 160
    d.polygon([(cx-90, crown_y), (cx-90, crown_y-25), (cx-60, crown_y-15),
               (cx-30, crown_y-35), (cx, crown_y-15), (cx+30, crown_y-35),
               (cx+60, crown_y-15), (cx+90, crown_y-25), (cx+90, crown_y)],
              fill=(50, 50, 55), outline=(20, 20, 22))
    d.line((cx-90, crown_y-1, cx+90, crown_y-1), fill=(20, 20, 22), width=2)
    # Dettagli corpo: intarsi sul petto
    d.line((cx-40, cy+65, cx+40, cy+65), fill=(55, 80, 60), width=2)
    d.line((cx-30, cy+85, cx+30, cy+85), fill=(55, 80, 60), width=2)
    d.ellipse((cx-15, cy+100, cx+15, cy+130), fill=(120, 220, 180), outline=(55, 80, 60), width=2)
    # Patina verdigris sulla testa (macchie)
    for _ in range(25):
        bx = random.randint(cx-85, cx+85)
        by = random.randint(cy-145, cy+15)
        rr = random.randint(4, 12)
        overlay = Image.new("RGBA", img.size, (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((bx-rr, by-rr, bx+rr, by+rr), fill=(90, 130, 95, 60))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        d = ImageDraw.Draw(img)
    # Vignetta scura
    vg = Image.new("L", (SW, SH), 0)
    vgd = ImageDraw.Draw(vg)
    for i in range(20):
        a = int(240 - i*12)
        vgd.ellipse((-30-i*4, -30-i*4, SW+30+i*4, SH+30+i*4), outline=a)
    vg = vg.filter(ImageFilter.GaussianBlur(30))
    black = Image.new("RGB", (SW, SH), (15, 10, 8))
    img = Image.composite(img, black, vg)
    img.save(Path(__file__).resolve().parent.parent / "assets" / "npcs" / "re_automa.png", "PNG", optimize=True)
    print("  ✓ re_automa (portrait)")


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("all", "rooms"):
        print("Generating 3 atmospheric room placeholders:")
        bivio_giungla()
        corridoio_perduto()
        cunicolo_nascosto()
    if target in ("all", "npcs", "re_automa"):
        print("Generating NPC portrait placeholder:")
        re_automa_portrait()
    print("Done.")
