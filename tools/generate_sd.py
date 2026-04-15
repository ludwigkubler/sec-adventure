#!/usr/bin/env python3
"""Genera sfondi stanze e ritratti NPC via SD-WebUI API su sec (via tunnel SSH)."""
import base64
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD = json.load(open(ROOT / "data" / "world.json", encoding="utf-8"))
ROOMS_DIR = ROOT / "assets" / "rooms"
NPCS_DIR = ROOT / "assets" / "npcs"
ROOMS_DIR.mkdir(parents=True, exist_ok=True)
NPCS_DIR.mkdir(parents=True, exist_ok=True)

# Stile visivo coerente per tutte le immagini
STYLE = (
    "flat illustration, minimal simple shapes, limited warm palette, "
    "sepia and ochre tones, dark outlines, mysterious abandoned atmosphere, "
    "submachine game style, point and click adventure, no text, no characters"
)
# Atto II ha uno stile più freddo/meccanico
STYLE_ATTO2 = (
    "flat illustration, minimal simple shapes, mechanical steampunk, "
    "verdigris green-blue cyan tones with bronze and copper accents, "
    "dark outlines, ancient underground civilization, machinery clockwork, "
    "syberia game style, point and click adventure, no text, no characters"
)
NEG = (
    "photorealistic, 3d render, text, watermark, signature, people, faces, "
    "blurry, low quality, distorted, modern, clean"
)

ROOM_PROMPTS = {
    "spiaggia": "tropical beach at dawn, sand, shipwreck debris, broken wooden planks, rope, glass bottle, calm sea horizon",
    "caletta": "small rocky cove, tide pools with shells, dark cave entrance on the right, steep cliffs",
    "grotte": "dark sea cave interior lit by torch, stalactites, wet stone walls, pool of water, ancient carvings",
    "tempio_sommerso": "underwater ancient temple ruins, coral columns, blue green light rays, mysterious stone altar",
    "foresta": "tropical jungle forest path, tall palm trees, vines, filtered sunlight, dense vegetation",
    "radura": "forest clearing, wildflowers, sunlight, tall grass, dirt paths going in multiple directions",
    "scogliere_sud": "rocky southern cliffs overlooking ocean, steep drop, seagulls, windy atmosphere",
    "villaggio": "small tropical village with thatched huts, wooden huts on stilts, central fire pit, palm trees",
    "molo": "old wooden pier stretching into calm bay, moored fishing boat, fishing nets, weathered wood",
    "giungla": "dense tropical jungle, huge tree roots, hanging vines, thick undergrowth blocking the path",
    "giungla_profonda": "deep dark jungle interior, ancient tree trunks, mist, mysterious atmosphere, swampy",
    "capanna_luna": "wooden shaman hut interior, hanging dried herbs, candles, mystical symbols, old maps on walls",
    "sentiero_montagna": "rocky mountain trail going up, pine trees, view of valley below, steep cliffs",
    "cima_vulcano": "volcano summit crater, red glowing lava, black volcanic rock, smoke, dramatic sky",
    "scogliere": "northern rocky cliffs with a tall stone lighthouse in distance, crashing waves",
    "faro": "inside an ancient stone lighthouse, spiral stairs, dormant brazier at top, arched windows, ocean view",
    "rovine": "ancient stone ruins overgrown with vines, broken columns, carved symbols, mysterious temple entrance",
    "sala_guardiano": "vast ancient stone hall, glowing spectral figure in center, ornate columns, mystical light",
    "cripta": "underground stone crypt, sarcophagi, torches, ancient carvings, dust, cobwebs",
    "laguna": "hidden tropical lagoon, turquoise water, waterfall, lush vegetation, peaceful atmosphere",
}

NPC_PROMPTS = {
    "kaia": "portrait of wise elderly island woman with white braided hair, weathered dark skin, shell necklace, serene expression",
    "marco": "portrait of bearded castaway man with worn clothes, sunburnt skin, determined eyes, wild hair",
    "tiko": "portrait of young island fisherman with dark hair, simple clothes, friendly smile, holding fishing net",
    "luna": "portrait of mysterious young woman shaman, flowing dark hair, tattoos, moon symbols, mystical aura",
    "guardiano": "portrait of spectral ancient guardian figure, glowing translucent blue, ornate ancient armor, ghostly aura",
}

# ─── Atto II — Le Profondità ───
ROOM_PROMPTS_ATTO2 = {
    "pozzo_faro": "vertical stone well with spiral staircase descending into darkness, glowing turquoise light from below, ancient carved stone walls, mysterious atmosphere",
    "cripta_meccanica": "low vaulted chamber with iron pillars, bronze shelves filled with copper gears and cogs, central rotating brass pedestal, dim greenish light",
    "sala_ingranaggi": "vast cathedral-like hall covered in giant rotating bronze gears and cogs on every surface, central iron platform, towering machinery, steampunk",
    "corridoio_vapore": "narrow corridor with thick copper pipes hissing steam, condensation on stone floor, warm orange light, claustrophobic atmosphere",
    "forgia_antica": "ancient forge with octagonal furnace burning liquid orange metal, two copper automaton figures hammering at anvil, tools on side table, mystical altar",
    "archivio": "circular seven-story library with metal-plate books on tall shelves, spiral staircase, central ethereal blue glowing figure floating, vast knowledge",
    "osservatorio": "underground observatory with dome ceiling projecting alien constellations, large brass astrolabe with empty lens slot, mosaic of three aligned stars",
    "cuore_macchina": "cubic chamber with massive golden pendulum hanging from ceiling, suspended dark crystal heart above, walls covered in shifting symbol mosaics",
    "agora_perduta": "vast underground octagonal plaza with carved buildings in living rock, eight colossal crowned statues, central basalt throne with patinated copper automaton king",
    "via_titani": "long avenue lined with twenty-meter tall Titan statues holding weapons, polished obsidian floor with inlaid symbols, circular stone portal at end with three geometric niches",
    "abisso": "deep chasm in underground world, rope and plank suspension bridge with broken ropes, gusts of wind, distant bright light far below",
    "radice_mondo": "perfect crystal sphere chamber with floating Tree of Light made of pure turquoise energy, central stone pedestal with dark titanic crown, sacred final destination",
}

NPC_PROMPTS_ATTO2 = {
    "archivista": "portrait of translucent ethereal female figure made of soft blue light, serene closed-eyed face, ghostly luminous aura, mystical archivist spirit",
    "re_automa": "portrait of colossal patinated copper-green automaton king, ornate metal body, simple iron crown, mask-like face with glowing slit eyes, ancient and majestic",
}

# ─── Stanze atmosferiche aggiunte (ultima iterazione) ───
ROOM_PROMPTS_EXTRA = {
    "cimitero_marino": "remote black sand cove with dozens of broken shipwrecks rusting on the beach, decaying wooden hulls with faded names, rusty metal creaking, melancholic atmosphere",
    "bivio_giungla": "deep jungle crossroads with a tall ancient stone totem covered in carvings of strange animals (bird with hooked beak, four-eyed fish, octopus-man), dense foliage, three overgrown paths, mystical",
    "corridoio_perduto": "dark low forgotten metal corridor underground, walls covered in thousands of carved names from different eras, dripping luminescent condensation, claustrophobic and reverent atmosphere",
    "cunicolo_nascosto": "small hidden shrine room behind a broken wall, ancient stone altar with a small copper lamp burning under intact glass dome, fine ancient dust, warm sacred light",
    "grotte_profonde": "deep sea cave chamber, dark volcanic walls, phosphorescent moss patches, pool of still water reflecting, ancient carved spirals on walls, mysterious blue-green glow, rocky outcrops, torchlight from off-frame, atmospheric cavern",
}

API = "http://127.0.0.1:7860/sdapi/v1/txt2img"


def sd_call(prompt, negative, width, height, steps=22, seed=-1, style=None):
    """Chiama l'API SD-WebUI via SSH su sec (nessuna apertura di porte)."""
    payload = {
        "prompt": f"{prompt}, {style or STYLE}",
        "negative_prompt": negative,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": 6.5,
        "sampler_name": "DPM++ 2M",
        "seed": seed,
    }
    payload_json = json.dumps(payload)
    # Via SSH: pipe del JSON a curl sul server
    cmd = [
        "ssh", "ludo@sec",
        f"curl -s -X POST {API} -H 'Content-Type: application/json' --data @-",
    ]
    result = subprocess.run(
        cmd, input=payload_json, capture_output=True, text=True, timeout=300
    )
    if result.returncode != 0:
        raise RuntimeError(f"SSH error: {result.stderr[:300]}")
    data = json.loads(result.stdout)
    if "images" not in data or not data["images"]:
        raise RuntimeError(f"No images in response: {str(data)[:200]}")
    return base64.b64decode(data["images"][0])


def do_rooms(skip_existing=True, prompts=ROOM_PROMPTS, style=None, label="room"):
    for rid, prompt in prompts.items():
        out = ROOMS_DIR / f"{rid}.png"
        if skip_existing and out.exists() and out.stat().st_size > 10000:
            print(f"[skip] {rid}")
            continue
        t0 = time.time()
        try:
            img = sd_call(prompt, NEG, width=960, height=576, steps=22,
                          seed=hash(rid) & 0xFFFFFFFF, style=style)
            out.write_bytes(img)
            print(f"[{label}] {rid:24s} {time.time()-t0:5.1f}s  {len(img)//1024}KB")
        except Exception as e:
            print(f"[FAIL] {rid}: {e}")


def do_npcs(skip_existing=True, prompts=NPC_PROMPTS, style=None):
    for nid, prompt in prompts.items():
        out = NPCS_DIR / f"{nid}.png"
        if skip_existing and out.exists() and out.stat().st_size > 10000:
            print(f"[skip] {nid}")
            continue
        t0 = time.time()
        try:
            img = sd_call(prompt, NEG, width=512, height=512, steps=22,
                          seed=hash(nid) & 0xFFFFFFFF, style=style)
            out.write_bytes(img)
            print(f"[npc ] {nid:24s} {time.time()-t0:5.1f}s  {len(img)//1024}KB")
        except Exception as e:
            print(f"[FAIL] {nid}: {e}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("rooms", "all"):
        do_rooms()
    if target in ("npcs", "all"):
        do_npcs()
    if target in ("atto2", "all", "rooms2"):
        do_rooms(prompts=ROOM_PROMPTS_ATTO2, style=STYLE_ATTO2, label="atto2")
    if target in ("atto2", "all", "npcs2"):
        do_npcs(prompts=NPC_PROMPTS_ATTO2, style=STYLE_ATTO2)
    if target in ("extra", "all"):
        # Stanze atmosferiche: atto I sepia, atto II verdigris
        atto1_extra = {k: v for k, v in ROOM_PROMPTS_EXTRA.items() if k in ("cimitero_marino","bivio_giungla","cunicolo_nascosto","grotte_profonde")}
        atto2_extra = {k: v for k, v in ROOM_PROMPTS_EXTRA.items() if k in ("corridoio_perduto",)}
        do_rooms(prompts=atto1_extra, style=STYLE, label="extra1")
        do_rooms(prompts=atto2_extra, style=STYLE_ATTO2, label="extra2")
    print("Done.")
