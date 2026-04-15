# 📜 ROADMAP v2.0 — "The Castaway's Isle" (Living World)

> Documento di sintesi dell'audit multi-agente eseguito su v1.5.
> v1.5 deve sembrare preistoria.

## 🎯 Audit consolidato v1.5 — Voto medio: **6.3/10**

| Dimensione | Voto | Critica principale |
|---|---|---|
| Architettura tecnica | 6.8 | IIFE singleton, mondo monolitico, no test, no modding |
| Grafica/Asset | 6.2 | SDXL flat senza palette lock, NPC mix stilistico, parallax 2 layer |
| Marketing/Positioning | 5.5 | Tecnicismo invendibile, "AI art" red flag Steam, no brand |
| Esperienza giocatore | 6.5 | Esplorazione piatta, NPC statici, dialoghi monostadio, no choices |
| Ambiente dinamico | 6.5 | Sfondi statici, no day/night, no weather, no reactivity |

**Target v2.0**: 9.0/10 medio. Trasformazione da "hobby project promettente" a "indie release commerciale credibile".

---

## 🧭 Pillars v2.0

1. **LIVING WORLD** — l'isola respira: clock globale, weather, marea, NPC che si spostano, palette che cambia
2. **DEPTH** — meccaniche stratificate (skill/karma/thought-cabinet), scelte con peso reale, fallimento recuperabile
3. **VISUAL FIDELITY** — parallax 5-layer, light maps, paintover manuale su SDXL, HUD diegetico, cinematics scriptate
4. **EXPANDABILITY** — TypeScript+Vite, room-as-module lazy, puzzle-as-plugin, mod loader, editor visuale
5. **COMMERCE-READY** — rebrand, Steam EA, leaderboard online, soundtrack export, controller, mobile

---

## 📅 ROADMAP (5 fasi, ~5-6 mesi)

### FASE 0 — FOUNDATION (settimana 1-2)
- [ ] Migrazione TypeScript + Vite + ESM (preserva compat)
- [ ] Engine refactor: state machine pure-reducer + event bus tipizzato (`mitt`-style)
- [ ] Save schema versioning + migrations
- [ ] Vitest suite, 80%+ coverage su reducer
- [ ] ServiceWorker PWA (offline play)
- [ ] Cloud save adapter pattern (Local/Supabase/Firebase)

### FASE 1 — VISUAL ENGINE (settimana 3-5)
- [ ] **Canvas multi-layer**: 5 plane parallax (sky / bg-far / bg-mid / bg-near / fg)
- [ ] **WorldClock**: 1440 min gioco = 45 min reali, fasi {dawn, day, dusk, night}
- [ ] **LightingMixer**: LUT shift CSS filter (`hue-rotate`, `brightness`, `saturate`) per fase
- [ ] **WeatherFSM**: clear/cloudy/rain/storm/fog con probabilità per bioma
- [ ] **TideSystem**: sinusoide 2 cicli/giorno → modifica spawn in spiaggia/molo/caletta
- [ ] **ProceduralSky**: canvas con sole/luna in posizione = f(clock), stelle a 21:00, costellazioni
- [ ] **Bioluminescenza notturna** (giungla/grotte/abisso)
- [ ] **Memoryprint**: orme persistite nel save, dissolte dalla marea
- [ ] **Mouse parallax** sui layer al passaggio

### FASE 2 — ASSET PIPELINE v2 (settimana 6-8)
- [ ] **ControlNet-Depth pipeline**: SDXL + depth-map → split automatico in 4 layer PNG
- [ ] **Krita paintover** manuale per polish edges + lighting (5 stanze pilota: spiaggia, faro, archivio, radice, cuore_macchina)
- [ ] **Light maps PNG** per torcia on/off, giorno/notte/crepuscolo (`mix-blend-mode: screen`)
- [ ] **Portraits ridisegnati** 7 NPC stile uniforme (Procreate/Krita), 4-frame idle sprite-sheet
- [ ] **NPC spritesheet** wander animation (12 fps)
- [ ] **HUD diegetico**: zaino → "taccuino del naufrago" (pagine sfogliabili, ink stains, corner fold)
- [ ] **Topbar** ridisegnata stile rope-tied icons
- [ ] **Palette ufficiale lock** in `:root`:
  - Atto I: `--sepia #c08a3c`, `--ocra #8a5a28`, `--sand #e8d7b0`
  - Atto II: `--verdigris #4a8a82`, `--bronze #8c6a3a`, `--copper-hot #d89060`
  - Radice: `--bio-cyan #5ac8b8`, `--root-purple #4a3050`

### FASE 3 — GAMEPLAY DEPTH (settimana 9-12)
- [ ] **Thought Cabinet** (Disco Elysium-style): internalizzi idee a scadenza che sbloccano dialoghi
- [ ] **Skill check** con 6 skill (Intuito, Meccanica, Empatia, Resistenza, Occhio Vivo, Voce) + dadi narrativi + reroll
- [ ] **Karma/Reputazione fazioni**: Villaggio vs Costruttori vs Mare → influenza finali
- [ ] **Crafting tree visibile**: pannello con 30+ ricette, nodi grigi/colorati
- [ ] **Companion system**: Tiko ti segue dopo barca riparata, commenta stanze (Atreus-like)
- [ ] **Dream sequences**: 4 stanze oniriche con puzzle simbolici + backstory Naufrago
- [ ] **Day/Night gameplay**: alcune stanze (capanna_luna) accessibili solo di notte
- [ ] **Fatica/Fame**: azioni consumano energia, dormire rigenera ma avanza tempo
- [ ] **Resource economy**: conchiglie come valuta col mercato Kaia
- [ ] **Riparazione a durabilità**: torcia/lanterna si consuma, manutenzione richiesta
- [ ] **Memory lore system**: codex sbloccati appaiono come voce narrante nelle stanze connesse

### FASE 4 — CONTENT EXPANSION (settimana 13-16)
- [ ] **Atto III "L'Oceano Interno"**: 15 nuove stanze oltre la Radice (mare sotterraneo, isole-frammento)
- [ ] **Prologo giocabile** (10 min): la nave prima del naufragio, scelta classe (mercante/fuggiasco/studioso) → perk + lettere personali
- [ ] **5 finali totali**: soccorso / corona-tiranno / corona-sacrificio / unione Re-Automa / segreto-Costruttore + bad-ending Luna morta
- [ ] **New Game+ "Prospettiva Tiko"**: rigiochi col pescatore, 4 codex esclusivi, dialoghi alternativi
- [ ] **Mini-games integrati**: pesca (timing), cucina (alchimia per Luna), riparazione barca (puzzle tubi), decifrazione codici (Mastermind), navigazione astrolabio
- [ ] **Companion side-arc** per ogni NPC: 3-stage personal quest
- [ ] **Time-gated quest**: "Luna muore in 3 giorni" con timer reale
- [ ] **Investigation Disco-Elysium**: interrogatorio Guardiano 12 domande, contraddizioni, bluff check
- [ ] **Survival events**: tempesta allaga spiaggia, eruzione blocca vulcano 1h
- [ ] **Boss narrativi**: duello enigmi col Guardiano 3 round con stake crescenti
- [ ] **Perma-change mondo**: allagare tempio chiude stanze permanentemente

### FASE 5 — CINEMATIC & POLISH (settimana 17-19)
- [ ] **Cutscene scriptate** (4 momenti chiave): faro-acceso, corona-indossata, re-automa-reveal, radice-finale (layer fade + camera-zoom + audio sting)
- [ ] **Photo/Sketch mode**: diario disegni, screenshot condivisibili, glifi puzzle key
- [ ] **Foreground particles** layer (pioggia davanti, foglie in focus, sparks)
- [ ] **Audio-visual sync** per cinematics
- [ ] **Editor visuale stanze** (Svelte app) — drag anchors su canvas, sostituisce examinable_anchors manuali
- [ ] **CLI scaffolding**: `npx isola new-room <id>`
- [ ] **Mod loader**: zip-based (JSON + PNG), sandbox no-eval, registry runtime
- [ ] **Performance budget**: 60fps desktop / 30fps mobile, ≤50 particles totali, RAF unico
- [ ] **Mobile responsive layout**

### FASE 6 — COMMERCE-READY (settimana 20-22)
- [ ] **Rebrand**: "The Castaway's Isle" (EN primario) / "L'Isola del Naufragio" (IT)
- [ ] **Logo**: faro stilizzato + onda, gradient sepia→verdigris (2 atti)
- [ ] **Tagline**: *"Light the lighthouse. Become the next keeper."*
- [ ] **Steam Cloud saves**
- [ ] **Controller support** (gamepad API)
- [ ] **Soundtrack export** (.wav dal motore audio — hook press)
- [ ] **Speedrun leaderboard online** (Supabase free tier)
- [ ] **Chapter select** post-finale
- [ ] **Trailer 75s** (hook 0-3s: faro che si accende)
- [ ] **8 screenshot** curated (4 Atto I + 4 Atto II)
- [ ] **3 GIF loopable** <3MB (combine, iris, pendulum)
- [ ] **Press kit** (`presskit()` format)
- [ ] **Devlog video** "how procedural audio works" (HN + GMTK)
- [ ] **itch.io PWYM** soft launch (min 0€, suggested 6€)
- [ ] **Steam Early Access** 9.99€ launch -15% primo mese
- [ ] **Bundle OST** 12.99€
- [ ] **Outreach**: 80 curator + 50 streamer keys (Keymailer)
- [ ] **Steam Next Fest demo** (Atto I completo, 45 min)

---

## 🎨 Brand identity v2.0

| Elemento | Valore |
|---|---|
| Nome (EN) | The Castaway's Isle |
| Nome (IT) | L'Isola del Naufragio |
| Tagline | "Light the lighthouse. Become the next keeper." |
| Logo concept | Faro stilizzato sopra un'onda, gradient sepia→verdigris |
| Sound design pitch | "Every sound is born from code" (vero USP, sostituisce "AI art") |
| Comparable | "Submachine's dread meets Outer Wilds' epiphany loop, in 2 hours" |
| Pricing | itch.io PWYM 6€ suggested · Steam EA 9.99€ |

---

## 👥 Target personas (marketing)

- **Marco, 34, Milano** — "Il Nostalgico Flash". 15€/mese su indie, gioca Submachine/Samorost. Reddit + Warp Door newsletter.
- **Alex, 22, Berlin** — "Streamer Cozy-Mystery". Twitch affiliate 200 viewer, completa giochi 2-3h in singolo stream. Keymailer + TikTok.
- **Giulia, 41, Roma** — "Lettrice Narrativa". Steam wishlist lunga, compra Disco Elysium / Oxenfree / KRZ. Steam curator + IT press.

---

## 📊 KPI realistici

- **Wishlist Steam pre-launch**: 5,000
- **Vendite primi 30 giorni**: 1,500-3,000 copie
- **Break-even**: ~800 copie
- **Long Tail target**: tipo *A Short Hike* (passaparola, 6-12 mesi crescita)

---

## 🚦 Strategia esecuzione realistica

Lo scope completo è 5-6 mesi full-time. Per evitare scope-creep, splittiamo in **3 release intermedie**:

- **v2.0 "Living World Foundation"** (~3 mesi): Fase 0+1+2 + Companion+Crafting tree (parte di 3)
  - Quello che fa dire "v1.5 era preistoria"
- **v2.1 "Depth & Companions"** (~1 mese): rest of Fase 3 + Cinematics (parte di 5)
- **v2.2 "Content Expansion"** (~1.5 mesi): Fase 4 (Atto III + mini-games + 5 finali)
- **v2.3 "Commerce Launch"** (~1 mese): Fase 6 (rebrand + Steam EA)

**Branch strategy**: `v2-foundation`, `v2-living`, `v2-depth`, `v2-content`, `v2-commerce`. Merge sequenziale su `main` con tag.

---

## ⚠️ Rischi & mitigazioni

- **Scope creep**: rispettare gli split v2.0/2.1/2.2/2.3, non compressare
- **AI art reputazione Steam**: dichiarare "SDXL-assisted concept, human-finalized" + paintover manuale + crediti chiari nel press kit
- **Performance multi-layer canvas**: budget rigido 60fps desktop, fallback 2D semplificato per mobile
- **Save migration**: ogni schema bump richiede script idempotente + backup automatico
- **Asset rigeneration**: mantenere backup di ogni versione PNG (oggi: `/tmp/rooms_backup_v14/`)

---

## 🔑 Decisioni da prendere ora

1. **Rebrand sì/no** prima di Steam? (raccomandato: sì, ma manteniamo `sec-adventure` come repo dev)
2. **Steam Direct fee 100$** quando? (raccomandato: mese 5)
3. **Accettiamo TypeScript migration** ora o restiamo vanilla? (raccomandato: sì TS, fa scalare)
4. **Mod loader** è feature v2.x o v3.0? (raccomandato: v3.0, troppo grande per ora)
5. **Mobile responsive**: nice-to-have o blocker per Steam? (raccomandato: nice-to-have, prima desktop perfetto)
