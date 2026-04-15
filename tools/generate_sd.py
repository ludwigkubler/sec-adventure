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
    "submachine game style, point and click adventure, no text, no characters, "
    "highly detailed, intricate textures, atmospheric perspective, "
    "cinematic composition, painterly quality, rich shadows"
)
# Atto II ha uno stile più freddo/meccanico
STYLE_ATTO2 = (
    "flat illustration, minimal simple shapes, mechanical steampunk, "
    "verdigris green-blue cyan tones with bronze and copper accents, "
    "dark outlines, ancient underground civilization, machinery clockwork, "
    "syberia game style, point and click adventure, no text, no characters, "
    "highly detailed, intricate clockwork mechanisms, patinated brass, "
    "dramatic underground lighting, atmospheric perspective, painterly"
)
NEG = (
    "photorealistic, 3d render, text, watermark, signature, people, faces, "
    "blurry, low quality, distorted, modern, clean"
)

ROOM_PROMPTS = {
    "spiaggia": "tropical beach at dawn, weathered shipwreck hull tilted in foreground with broken oak planks splintered and salt-crusted, tangled hemp ropes coiled on golden sand mixed with shell fragments and seaweed, midground driftwood logs and a half-buried glass bottle, distant horizon with gentle waves and faint mist, soft warm rim light from low sun, cinematic depth of field, hyper-detailed textures of weathered wood grain and rusted nails, atmospheric haze",
    "caletta": "small rocky cove at golden hour, foreground tide pools glinting with shells starfish and orange algae over wet pitted stone, midground barnacle-encrusted boulders and a dark gaping cave entrance on the right with dripping moss, background steep weathered cliffs streaked with ochre mineral veins, salt spray haze, warm sidelight casting long shadows, hyper-detailed wet stone textures and crusted mineral deposits",
    "grotte": "dark sea cave interior lit by a guttering torch, foreground wet black pebbles and a shallow reflective water pool with ripples, midground jagged stalactites dripping mineral water over moss-covered stone ledges, background ancient carved spiral glyphs on weathered limestone walls fading into darkness, volumetric torchlight beams cutting through damp mist, hyper-detailed wet stone and calcified drip textures, brooding chiaroscuro",
    "tempio_sommerso": "underwater ancient temple ruins, foreground broken coral-encrusted stone altar with scattered offerings and drifting silt particles, midground toppled columns overgrown with red coral and swaying sea fans, background massive arched doorway fading into deep blue green haze with cathedral light rays, schools of small silhouetted fish, caustic god-rays from surface, hyper-detailed barnacle and coral textures, mystical submerged atmosphere",
    "foresta": "tropical jungle forest path, foreground large fern fronds and moss-wrapped tree roots breaking through loamy soil with scattered fallen palm leaves, midground tall palm trunks and hanging liana vines dripping with dew, background dense canopy with filtered dappled sunlight shafts and distant greenish haze, butterflies drifting through light beams, warm humid atmosphere, hyper-detailed bark and leaf textures, painterly depth",
    "radura": "forest clearing bathed in golden hour light, foreground wildflowers and tall swaying grass with morning dew and small stones, midground a weathered wooden signpost at a crossroads with dirt paths branching in multiple directions, background ring of sunlit tree trunks fading into misty forest edge, volumetric light rays piercing the canopy, hyper-detailed grass blade and flower petal textures, warm serene atmosphere",
    "scogliere_sud": "rocky southern cliffs overlooking the ocean at late afternoon, foreground tufts of windswept ochre grass and cracked limestone edge with scattered seabird feathers, midground jagged cliff face dropping into crashing foamy waves, background distant sea stacks and seagulls wheeling against hazy sky, strong coastal wind motion, warm sidelight, hyper-detailed weathered rock textures and salt erosion",
    "villaggio": "small tropical village at dusk, foreground a central stone fire pit with glowing embers and wooden benches surrounded by scattered clay pots and woven baskets, midground cluster of thatched huts on sturdy wooden stilts with hanging lanterns and drying fishing nets, background tall palm trees silhouetted against warm orange sky, smoke drifting gently, hyper-detailed thatch and woven rope textures, inviting golden atmosphere",
    "molo": "old wooden pier stretching into a calm morning bay, foreground warped salt-stained planks with barnacles and coiled tarred ropes, midground a weathered fishing boat moored with tangled nets floats and wooden crates, background misty horizon with distant sailboats and pale sunrise reflections on glassy water, gentle golden light, hyper-detailed wood grain and peeling paint textures, serene maritime atmosphere",
    "giungla": "dense tropical jungle, foreground massive twisted buttress tree roots covered in moss and crawling insects breaking across the path, midground curtain of thick hanging vines and broad banana leaves blocking passage with patches of filtered light, background fog-shrouded towering trees fading into deep green gloom, humid mist particles, warm dappled sunlight, hyper-detailed bark moss and fungi textures, claustrophobic lushness",
    "giungla_profonda": "deep dark jungle interior at twilight, foreground gnarled ancient tree trunks with phosphorescent fungi and twisted exposed roots in black swamp water, midground thick tendrils of mist weaving between moss-draped branches, background faint silhouettes of enormous trees lost in fog with a single distant shaft of pale light, eerie stillness, hyper-detailed moss bark and murky water textures, ominous mysterious atmosphere",
    "capanna_luna": "wooden shaman hut interior lit by candlelight, foreground a cluttered altar table with open leather-bound grimoire brass bowls crystals and melting beeswax candles dripping wax, midground bundles of dried herbs hanging from ceiling beams and chalk-drawn mystical symbols on warped plank walls, background old parchment maps pinned beside a small shuttered window leaking moonlight, dust motes floating in warm candle glow, hyper-detailed wood grain herb and parchment textures",
    "sentiero_montagna": "rocky mountain trail climbing upward at midday, foreground loose gravel and scattered granite stones bordered by hardy wildflowers and twisted pine saplings, midground switchback path carved into the cliffside with a weathered wooden railing, background sweeping vista of forested valley far below with hazy distant peaks and drifting clouds, crisp warm sunlight, hyper-detailed stone and pine needle textures, majestic atmospheric depth",
    "cima_vulcano": "volcano summit crater at dusk, foreground cracked black volcanic rock with glowing fissures of molten orange magma and drifting sulfur smoke, midground jagged basalt ridge encircling a churning red lava lake bubbling violently, background massive ash plume rising against a bruised purple red sky with falling embers, intense heat haze shimmer, hyper-detailed cooled lava textures and glowing cracks, apocalyptic dramatic atmosphere",
    "scogliere": "northern rocky cliffs at stormy afternoon, foreground wet black slate boulders slick with sea spray and tufts of salt-hardy grass, midground crashing white-foam waves exploding against jagged cliff base sending mist into the air, background tall weathered stone lighthouse silhouetted on the distant promontory under dramatic moody clouds, gulls wheeling, cold diffuse light, hyper-detailed wet rock and breaking wave textures",
    "faro": "inside an ancient stone lighthouse, foreground wrought iron spiral staircase winding upward with worn stone steps and cast-iron railings polished by centuries of hands, midground thick curved stone walls inset with arched leaded windows showing a sweeping ocean view with distant gulls, background a cold dormant cast-iron brazier at the top platform beneath a soot-blackened copper dome, shafts of cool ocean light crossing dust motes, hyper-detailed mortar stone and iron textures, reverent echoing atmosphere",
    "rovine": "ancient stone ruins overgrown with vines at late afternoon, foreground toppled column fragments and cracked flagstones choked with creeping ivy and wildflowers, midground partially collapsed archway with weathered carved glyphs depicting forgotten rituals, background mysterious shadowed temple entrance framed by towering banyan trees and hazy golden light, soft sunbeams cutting through hanging dust, hyper-detailed moss-eaten stone carving textures, melancholic sacred atmosphere",
    "sala_guardiano": "vast ancient stone hall, foreground mosaic floor with concentric carved rings and scattered offerings of wilted flowers, midground rows of towering ornate columns wrapped in faded golden bands leading the eye inward, background a glowing spectral guardian figure of translucent amber light hovering above a raised altar with radiating mystical beams and drifting particles, reverent volumetric god-rays, hyper-detailed weathered stone and gilded relief textures, awe-inspiring sacred atmosphere",
    "cripta": "underground stone crypt lit by flickering torches, foreground cracked stone sarcophagus with carved figures and scattered bone fragments on the dusty floor, midground more coffins along mossy niche walls with guttering wall-mounted torches casting wavering shadows, background corridor fading into blackness with draped cobwebs and faint carved glyphs, heavy dust motes in torchlight, hyper-detailed stone tomb chisel marks and cobweb textures, oppressive gothic atmosphere",
    "laguna": "hidden tropical lagoon at midday, foreground clear turquoise shallows with visible white pebbles and small colorful fish darting over sand, midground smooth basalt boulders ringed by lush ferns orchids and palms with a cascading waterfall feeding the pool in mist, background lush cliffside draped in hanging vines and sunlit mossy rock walls, warm dappled light and prismatic water reflections, hyper-detailed leaf water and stone textures, peaceful paradise atmosphere",
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
    "pozzo_faro": "vertical stone well shaft descending into darkness, foreground edge of cracked flagstone platform and the top of a wrought-iron spiral staircase bolted to the curved wall, midground moss-streaked ancient carved stone panels depicting spirals and glyphs lit by sconces, background deep well plunging into glowing turquoise luminescence far below with drifting vapor, volumetric cyan light rising upward, hyper-detailed weathered stone and iron rivet textures, vertiginous mystical atmosphere",
    "cripta_meccanica": "low vaulted chamber with iron pillars, foreground central rotating brass pedestal inlaid with complex engraved sigils sitting on a circular mosaic floor, midground tall bronze shelves crammed with intricate copper gears cogs and mechanical relics, background ribbed vault ceiling and arched alcoves fading into dim greenish gloom, shafts of patinated verdigris light, steam wisps drifting, hyper-detailed tarnished brass and oxidized copper textures, arcane workshop atmosphere",
    "sala_ingranaggi": "vast cathedral-like hall of machinery, foreground raised central iron platform with riveted grate flooring and control levers, midground colossal rotating bronze gears and interlocking cogs covering every wall meshing in constant motion, background soaring cavernous vault lost in greenish mist with towering clockwork spires and hanging chains, shafts of dusty light cutting between rotating teeth, hyper-detailed oiled brass tooth and rivet textures, awe-inspiring steampunk cathedral atmosphere",
    "corridoio_vapore": "narrow claustrophobic corridor, foreground wet riveted iron floor grate with beaded condensation and scattered puddles reflecting warm light, midground thick copper pipes crisscrossing the ceiling and walls hissing jets of white steam from brass valves, background corridor end dissolving into thick vapor with a distant warm orange glow of a furnace door, volumetric steam swirls, hyper-detailed patinated copper joints and rust streak textures, suffocating industrial atmosphere",
    "forgia_antica": "ancient underground forge, foreground a scarred iron anvil flanked by two towering patinated copper automaton smiths mid-hammer-strike with sparks flying, midground octagonal stone furnace blazing with liquid orange molten metal casting warm glow, background side workbench littered with ancient tools tongs and ceremonial molds beneath a small altar with candles and sacred engravings, dancing firelight and heat haze, hyper-detailed glowing metal and soot-blackened stone textures, mythic industrial atmosphere",
    "archivio": "circular seven-story library, foreground polished marble floor inlaid with concentric brass star maps and a low reading lectern, midground towering wrought-iron shelves packed with etched metal-plate books connected by a wrought spiral staircase ringing each level, background central void where a serene ethereal blue glowing female figure floats haloed by drifting luminous glyphs, motes of light swirling upward, hyper-detailed engraved plate and wrought-iron filigree textures, sacred scholarly atmosphere",
    "osservatorio": "underground observatory, foreground a large articulated brass astrolabe on a tripod with an empty lens slot and scattered engraved star charts on a stone table, midground circular mosaic floor depicting three aligned stars inlaid with silver and lapis, background towering dome ceiling projecting shifting alien constellations of pinprick lights across dark mineral-veined stone, cool cyan starlight and drifting dust, hyper-detailed brass gear astrolabe and mosaic tessera textures, cosmic contemplative atmosphere",
    "cuore_macchina": "cubic chamber, foreground cracked obsidian floor inscribed with pulsing glyph rings, midground a massive golden pendulum hanging from an ornate ceiling mount swinging slowly over the room, background all four walls covered in shifting mosaic panels of continuously rearranging symbols surrounding a suspended dark crystal heart pulsing with inner red-green light, humming energy, hyper-detailed gilded mechanism and mosaic tile textures, sacred mechanical atmosphere",
    "agora_perduta": "vast underground octagonal plaza carved into living rock, foreground basalt throne on a raised dais occupied by a patinated copper automaton king with ornate regalia and slit-glowing eyes, midground wide mosaic square ringed by eight colossal crowned stone statues of ancestors staring inward, background terraces of facade buildings carved directly into the cavern walls with lit windows fading into greenish gloom, volumetric downlight from fissures above, hyper-detailed carved rock and patinated copper textures, regal ancient atmosphere",
    "via_titani": "long ceremonial avenue, foreground polished obsidian floor inlaid with silver geometric symbols reflecting overhead light, midground twin rows of twenty-meter tall Titan statues holding weapons armor weathered by ages with moss in the crevices, background circular stone portal at the avenue's end inset with three empty geometric niches glowing faintly, cool volumetric light beams and drifting dust, hyper-detailed carved granite and silver inlay textures, monumental sacred atmosphere",
    "abisso": "deep chasm in the underground world, foreground splintered wooden plank edge of a rickety suspension bridge with frayed hemp ropes and loose boards missing, midground broken bridge span swaying over the infinite drop with whipping wind-lashed ropes, background vast black chasm with a single distant pinprick of bright white light far below and hints of cavern walls lost in depth, swirling wind motion lines and mist, hyper-detailed rope fray and weathered plank textures, vertiginous terrifying atmosphere",
    "radice_mondo": "perfect crystalline sphere chamber, foreground cracked stone pedestal at the center holding a dark titanic crown resting on a velvet cloth with scattered petals, midground the floating Tree of Light made of pure turquoise energy branches spreading upward with drifting luminous leaves, background curved crystal walls refracting the Tree into a kaleidoscope of cyan and gold reflections into infinity, pulsing volumetric radiance and floating motes, hyper-detailed crystal facet and energy filament textures, transcendent sacred final atmosphere",
}

NPC_PROMPTS_ATTO2 = {
    "archivista": "portrait of translucent ethereal female figure made of soft blue light, serene closed-eyed face, ghostly luminous aura, mystical archivist spirit",
    "re_automa": "portrait of colossal patinated copper-green automaton king, ornate metal body, simple iron crown, mask-like face with glowing slit eyes, ancient and majestic",
}

# ─── Stanze atmosferiche aggiunte (ultima iterazione) ───
ROOM_PROMPTS_EXTRA = {
    "cimitero_marino": "remote black sand cove at overcast dusk, foreground rusted anchor half-buried in volcanic sand with tangled chains and scattered barnacle-crusted bones of ships, midground dozens of decaying wooden shipwreck hulls tilted at impossible angles with faded peeling names and splintered masts, background hazy grey sea meeting a leaden sky with circling silhouetted gulls, cold moist wind and drifting mist, hyper-detailed rotted wood iron rust and wet black sand textures, melancholic graveyard atmosphere",
    "bivio_giungla": "deep jungle crossroads at dappled afternoon, foreground a tall ancient moss-covered stone totem carved with strange animals (hook-beaked bird, four-eyed fish, octopus-man) surrounded by offerings of shells and flowers, midground three overgrown divergent paths winding into thick emerald foliage, background towering jungle canopy with filtered god-rays piercing hanging vines and drifting pollen motes, humid mystical atmosphere, hyper-detailed moss-eaten carving bark and fern textures",
    "corridoio_perduto": "dark low forgotten metal corridor deep underground, foreground riveted iron floor plates streaked with dripping luminescent cyan condensation pooling between grates, midground narrow walls densely engraved with thousands of carved names in different alphabets and eras glowing faintly, background corridor fading into perfect blackness with a single distant pinprick of pale cyan light, cold humid air and faint echoing whispers, claustrophobic reverent atmosphere, hyper-detailed etched metal and condensation droplet textures",
    "cunicolo_nascosto": "small hidden shrine chamber revealed behind a broken stone wall, foreground rubble of the collapsed wall and scattered ancient dust catching light, midground a carved stone altar holding a small copper oil lamp burning steadily under an intact glass dome flanked by withered offerings, background niche walls with faded fresco fragments of forgotten deities and hairline cracks, drifting motes in sacred warm golden light, hyper-detailed fine ancient dust copper patina and cracked plaster textures, hushed reverent atmosphere",
    "grotte_profonde": "deep sea cave chamber, foreground dark volcanic rock outcrops rising from a still pool of black water perfectly reflecting the ceiling, midground curved walls patched with glowing phosphorescent blue-green moss illuminating ancient carved spiral glyphs, background chamber receding into mysterious darkness with a single shaft of warm torchlight from off-frame cutting through the gloom, drifting mineral mist, hyper-detailed wet volcanic rock moss and carved spiral textures, atmospheric mystical cavern",
}

API = "http://127.0.0.1:7860/sdapi/v1/txt2img"


def sd_call(prompt, negative, width, height, steps=32, seed=-1, style=None):
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
            img = sd_call(prompt, NEG, width=960, height=576, steps=32,
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
            img = sd_call(prompt, NEG, width=512, height=512, steps=32,
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
