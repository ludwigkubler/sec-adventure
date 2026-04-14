# Contributing to L'Isola del Naufragio

Grazie per l'interesse! Welcome to contribute.

## Issues

- **Bug reports**: steps to reproduce + browser + screenshot if visual
- **Feature requests**: frame them as user story ("As a player, I want ...")
- **Translations**: open issue tagged `translation:<lang>` to coordinate

## Pull requests

### Before PR

1. Run syntax check: `for f in js/*.js; do node --check $f; done`
2. Run audit: `python3 tools/audit.py` — must show 0 phantoms, 0 unreachable
3. Test the full playthrough path (spiaggia → faro) and Act II (pozzo → radice)
4. Check both IT and EN languages

### Style

- **JavaScript**: vanilla, no frameworks. 2-space indent. No semicolons at EOL? Actually we use them. Be consistent.
- **CSS**: no preprocessor. Custom properties for colors. BEM-ish for complex components.
- **Python tools**: PEP 8, type hints where clear. Prefer pure functions.
- **Narrative text**: prefer concrete imagery over abstract. One scene per paragraph. Italics sparingly.

## Adding a new language

1. Copy `js/i18n.js` UI section, add your locale to `UI` dict
2. Copy `tools/build_en.py` as `tools/build_<lang>.py`
3. Translate all strings in the new build file
4. Add locale code to `LOCALES` in `i18n.js`
5. Add language toggle option

## Adding a new room

1. Edit `tools/build_expansion.py` — add to `ROOMS`
2. Add map position in `MAP_POSITIONS`
3. Add hotspot zones in `ROOM_ZONES`
4. Connect it via `uscite_add` in room_patches of an existing room
5. Run `python3 tools/build_expansion.py && python3 tools/export_world.py`
6. Generate a background image: `python3 tools/generate_sd.py <custom>` or manually
7. Run audit

## Adding a collectible

1. Add item to `ITEMS` in build_expansion.py
2. Add to `COLLECTIBLES` with lore text
3. Add SVG icon in `tools/generate_svg_items.py`
4. Place it in a room's `oggetti` list

## Commit messages

Format: `<area>: <short description>`

Examples:
- `engine: fix save/load of codex state`
- `i18n: add French translation for items`
- `ui: new pendulum puzzle rhythm tuning`
- `data: add hidden room unlocked by pickaxe`

## License

By contributing you agree your contribution will be licensed under MIT (code)
and CC BY-SA 4.0 (narrative).
