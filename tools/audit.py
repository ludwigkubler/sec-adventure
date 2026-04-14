#!/usr/bin/env python3
"""Audit del mondo: trova oggetti phantom (richiesti ma non spawnati),
deadend (raccolti ma inutili), e validità del grafo stanze."""
import json
from collections import defaultdict
from pathlib import Path

W = json.loads((Path(__file__).resolve().parent.parent / "data" / "world.json").read_text(encoding="utf-8"))

produced = defaultdict(list)
consumed = defaultdict(list)

for r in W["recipes"]:
    for ing in r["ingredienti"]:
        consumed[ing].append(f"recipe→{r['risultato']}")
    produced[r["risultato"]].append(f"recipe<{r['ingredienti']}")

for k, act in W["room_actions"].items():
    item, room = k.split("::")
    consumed[item].append(f"action@{room}")
    for ot in act.get("ottieni", []):
        produced[ot].append(f"action({item}@{room})")

for k, dl in W["deliveries"].items():
    item, npc = k.split("::")
    consumed[item].append(f"deliver→{npc}")
    for ot in dl.get("ottieni", []):
        produced[ot].append(f"delivery({item}→{npc})")
    for rm in dl.get("rimuovi", []):
        consumed[rm].append(f"delivery({item}→{npc})")

for rid, room in W["rooms"].items():
    for d, b in (room.get("uscite_bloccate") or {}).items():
        cond = b.get("condizione", "")
        if cond.startswith("oggetto:"):
            consumed[cond[8:]].append(f"unlock({rid},{d})")
    for o in room.get("oggetti", []):
        produced[o].append(f"spawn@{rid}")

for npc, stages in W["dialogues"].items():
    for s in stages:
        for o in s.get("opzioni", []):
            for ot in o.get("ottieni", []):
                produced[ot].append(f"dialog({npc})")
            for rm in o.get("rimuovi", []):
                consumed[rm].append(f"dialog({npc})")

for pid, p in W.get("puzzles", {}).items():
    if p.get("oggetto"):
        produced[p["oggetto"]].append(f"puzzle({pid})")
for pid, p in W.get("puzzles_interactive", {}).items():
    for ot in p.get("ottieni", []):
        produced[ot].append(f"interactive({pid})")

collectibles = set(W.get("collectibles", {}).keys())

phantom = [(it, consumed[it]) for it in W["items"] if it not in produced and consumed.get(it)]
deadend = [it for it in W["items"] if it in produced and not consumed.get(it) and it not in collectibles]
unreachable_rooms = [r for r in W["rooms"] if not any(
    r in (rm.get("uscite") or {}).values() or
    any(W.get("blocked_destinations",{}).get(f"{src}::{d}") == r for d in (rm.get("uscite_bloccate") or {}))
    for src, rm in W["rooms"].items()
) and r != W.get("start_room", "spiaggia")]

print("=" * 60)
print(f"AUDIT SUBMACHINE - {len(W['rooms'])} stanze, {len(W['items'])} oggetti")
print("=" * 60)
print(f"\n[CRITICAL] Oggetti PHANTOM (richiesti ma mai spawnati): {len(phantom)}")
for it, cs in phantom: print(f"  ❌ {it} richiesto da: {cs[:3]}")
print(f"\n[INFO] Oggetti DECORATIVI (raccolti ma inutili): {len(deadend)}")
for it in deadend: print(f"  • {it}")
print(f"\n[INFO] COLLEZIONABILI tracciati: {len(collectibles)}")
print(f"\n[CHECK] Stanze IRRAGGIUNGIBILI: {len(unreachable_rooms)}")
for r in unreachable_rooms: print(f"  ⚠ {r}")
print()
status = "OK" if not phantom and not unreachable_rooms else "ATTENZIONE"
print(f"Stato finale: {status}")
