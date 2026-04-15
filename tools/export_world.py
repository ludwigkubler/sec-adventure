#!/usr/bin/env python3
"""Estrae i dati di mondo.py in un JSON consumabile dal motore web."""
import json
import re
import sys
from pathlib import Path

SRC = Path("/home/ludo/Scrivania/shmgs/games/avventura")
OUT = Path(__file__).resolve().parent.parent / "data" / "world.json"

sys.path.insert(0, str(SRC))
import mondo  # noqa: E402

TAG_RE = re.compile(r"\[/?[a-z ]+\]")


def clean(text):
    if not isinstance(text, str):
        return text
    return TAG_RE.sub("", text)


def clean_deep(obj):
    if isinstance(obj, dict):
        return {k: clean_deep(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_deep(x) for x in obj]
    if isinstance(obj, tuple):
        return [clean_deep(x) for x in obj]
    if isinstance(obj, str):
        return clean(obj)
    return obj


def tuple_key_dict(d):
    out = {}
    for k, v in d.items():
        key = "::".join(k) if isinstance(k, tuple) else str(k)
        out[key] = clean_deep(v)
    return out


# Mappa destinazioni per uscite bloccate (hardcoded in engine.py originale)
BLOCKED_DESTS = {
    "caletta::est": "grotte",
    "radura::nord": "giungla",
    "giungla::est": "rovine",
    "giungla_profonda::nord": "sentiero_montagna",
    "scogliere::ovest": "faro",
    "sala_guardiano::giù": "cripta",
    "molo::barca": "laguna",
    "grotte::giù": "tempio_sommerso",
}

world = {
    "intro": clean(mondo.INTRO),
    "finale": clean(mondo.FINALE),
    "rooms": clean_deep(mondo.STANZE),
    "items": clean_deep(mondo.OGGETTI),
    "characters": clean_deep(mondo.PERSONAGGI),
    "dialogues": clean_deep(mondo.DIALOGHI),
    "quests": clean_deep(mondo.QUEST),
    "puzzles": clean_deep(mondo.ENIGMI),
    "puzzles_interactive": {},
    "recipes": clean_deep(mondo.RICETTE),
    "room_actions": tuple_key_dict(mondo.AZIONI_STANZA),
    "deliveries": tuple_key_dict(mondo.CONSEGNE),
    "blocked_destinations": BLOCKED_DESTS,
    "start_room": "spiaggia",
    "finale_atto_ii": "",
}

# ─── Merge expansion (Atto II) ──────────────────────────────────────
EXP_PATH = OUT.parent / "expansion.json"
if EXP_PATH.exists():
    exp = json.loads(EXP_PATH.read_text(encoding="utf-8"))
    # Merge dicts (expansion wins su collisioni di chiave)
    for key in ("rooms", "items", "characters", "dialogues", "puzzles_interactive",
                "room_actions", "deliveries", "blocked_destinations"):
        world[key] = {**world.get(key, {}), **exp.get(key, {})}
    # Merge listcs
    world["recipes"] = world.get("recipes", []) + exp.get("recipes", [])
    # Patch a stanze esistenti
    for rid, patch in exp.get("room_patches", {}).items():
        if rid not in world["rooms"]:
            continue
        room = world["rooms"][rid]
        # ADD operations
        for add_key in ("uscite_bloccate_add", "esaminabili_add", "oggetti_add", "uscite_add"):
            base_key = add_key.replace("_add", "")
            if add_key in patch:
                room.setdefault(base_key, {} if isinstance(patch[add_key], dict) else [])
                if isinstance(patch[add_key], dict):
                    room[base_key].update(patch[add_key])
                else:
                    room[base_key].extend(patch[add_key])
        # REMOVE operations
        if "oggetti_remove" in patch:
            room["oggetti"] = [o for o in room.get("oggetti", []) if o not in patch["oggetti_remove"]]
    if "finale_atto_ii" in exp:
        world["finale_atto_ii"] = exp["finale_atto_ii"]
    for k in ("collectibles", "map_positions", "room_zones", "examinable_anchors", "epilogo_segreto"):
        if k in exp:
            world[k] = exp[k]
    print(f"  + expansion merged: +{len(exp.get('rooms',{}))} rooms, "
          f"+{len(exp.get('items',{}))} items, +{len(exp.get('characters',{}))} npcs")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(world, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}  rooms={len(world['rooms'])} items={len(world['items'])} "
      f"npcs={len(world['characters'])} puzzles={len(world['puzzles'])}+{len(world['puzzles_interactive'])} "
      f"recipes={len(world['recipes'])}")
