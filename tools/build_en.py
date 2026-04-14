#!/usr/bin/env python3
"""Traduce world.json (IT) → world.en.json mantenendo gli id ma sostituendo i testi narrativi.
Le traduzioni sono inline qui sotto. Ogni chiave = id del contenuto originale."""
import json, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = json.load(open(ROOT / "data" / "world.json", encoding="utf-8"))
OUT  = ROOT / "data" / "world.en.json"

INTRO_EN = """The storm betrayed you.

For three days the sea battered you like a broken toy, stripping you of
everything: the boat, the supplies, the memories of a normal life.

When the waves finally spat you onto the shore, you were more dead than alive.

Now you wake up. The sand is warm under your fingers. The sun burns your
skin. The sound of the sea fills the silence.

You're alive. But you're alone.

And this island... is on no map."""

FINALE_EN = """You kneel on the sand, and look up at the sky.

The lighthouse is burning. A thousand-year flame feeds on oil, crystal and gem,
and rises higher than the mast of any ship. The light sweeps the horizon in a
slow, methodical circle — a signal older than any SOS.

Minutes pass. Hours. Night falls. You wait.

Then, far out on the dark sea, a small light appears. It approaches. A ship.
A real ship — hull, sails, voices of men.

They see you. They turn. You raise a hand, and the hand trembles.

You're saved.

(And yet, as the boat draws near, you keep looking at the lighthouse. At its
unnatural flame. You don't know, and never will: what was it really that you
ignited up there?)

~ END ~"""

FINALE_ATTO_II_EN = """You put on the Titanic Crown.

For an instant, nothing. Then the eight points light up in cascade, and a soft,
cold light envelops you — not a fire, but a full moon shaped as a crown. You
know everything, all at once. You know who the Builders were, you know why they
chose to descend, you know what the Tree of Light is: the sleeping consciousness
of the world itself, and you are its new custodian.

The Tree opens before you like a flower. You are no longer afraid. You are no
longer alone.

Far, far above, on the island, the lighthouse keeps burning in the night. It
does not call for rescue. It calls for the next one. In a hundred years, in a
thousand, someone will see it, and wonder what it means.

You will tell them, when they arrive.

~ END ~"""

EPILOGO_SEGRETO_EN = (
    "SECRET EPILOGUE — All thirteen fragments collected.\n\n"
    "You found everything. The shells, the pearls, the diaries, the tablets: every forgotten "
    "voice the island and its depths had hidden. And listening to them all together, you understand.\n\n"
    "You are not a castaway. You were NEVER a castaway.\n\n"
    "You have returned. The storm that brought you here was your way of coming back — because "
    "you were one of them, one of the Builders, and when your civilization descended beneath "
    "the stone you did not descend with them. You remained outside. You forgot yourself. "
    "You wandered for millennia in one human life after another, until finally the current "
    "brought you back home.\n\n"
    "Now you know who you are. And they have always known."
)

ROOMS_EN = {
    "spiaggia": {
        "nome": "Shipwreck Beach",
        "descrizione": "You stand on a beach of golden sand scarred by the debris of the wreck. Broken planks, shreds of sail and tangled ropes lie scattered like the bones of a sea animal. The waves break lazily on the shore, bringing the sharp smell of salt and seaweed.\n\nThe wreck of your boat is stranded a little further on, tilted on one side like a wounded giant. To the north, thick tropical vegetation marks the edge of a forest. To the east, the rocks curve into a small cove.",
        "descrizione_breve": "The shipwreck beach. Debris scattered on golden sand. Forest to the north, a rocky cove to the east.",
        "esaminabili": {
            "relitto": "The wreck of your boat is beyond saving. The hull is torn in several places, the mast snapped. Among the debris you can make out a few usable planks and some pieces of rope.",
            "mare": "The sea stretches endless to the horizon. No sail, no land in sight. Just blue water and blue sky blending in the distance.",
            "sabbia": "Fine golden sand, dotted with shells and debris. Your footprints are the only ones visible.",
        },
    },
    "caletta": {
        "nome": "Rocky Cove",
        "descrizione": "A small inlet protected by walls of dark rock, smoothed by millennia of erosion. Tide pools swarm with life — small crabs, brightly colored anemones, starfish clinging to the rocks.\n\nThe walls of the cove are covered in moss and lichen. To the west you return to the beach. To the north a path climbs toward the island's interior. To the east, a dark opening in the rock seems to lead to sea caves.",
        "descrizione_breve": "The rocky cove with its tide pools. Beach to the west, path to the north, caves to the east.",
        "esaminabili": {
            "pozze": "The tide pools are tiny worlds. Miniature crabs flee among the algae, and a small octopus watches you with intelligent eyes before changing color and disappearing.",
            "pareti": "Dark volcanic rock, polished by the sea. Deep striations suggest eons of wave action.",
            "apertura": "A narrow dark opening in the rock. Beyond, only absolute darkness. A light source would help.",
        },
    },
    "grotte": {
        "nome": "Sea Caves",
        "descrizione": "Your torch reveals a cavity that extends further than you thought. The walls are wet and reflect the flame like mirrors of obsidian. In the center, a pool of still water so perfect it looks painted. Ancient carvings cover the walls — spirals, eyes, symbols you don't recognize but that seem to recognize you.\n\nA stalactite dripping water rhythmically, like a heart.",
        "descrizione_breve": "Sea cave lit by your torch. Incisions on the walls, central pool.",
        "esaminabili": {
            "incisioni": "Spirals that turn counterclockwise. Among them, three recurring symbols: an eye, a star, a root. The three again, here too.",
            "pozza": "The water is perfectly still. You see your reflection, but with something different: your face looks older, or younger, or both. Stepping closer, it corrects itself.",
            "stalattite": "Water drips from the tip every second and a half. Exactly. If this is a clock, it has been ticking for thousands of years.",
        },
    },
    "tempio_sommerso": {
        "nome": "Submerged Temple",
        "descrizione": "With the diving gear, you have descended into the depths of the cave. The water here is unexpectedly clear, luminous. Before you, an ancient temple stands among the corals — eight columns upright, eight broken, eight fallen. At the center, a stone altar bears three offerings: a seal, a trident, a coral crown. The sea has preserved them perfectly.",
        "descrizione_breve": "Submerged ancient temple. Altar with three offerings.",
        "esaminabili": {
            "colonne": "Columns of white stone streaked with blue veins. Each one has an inscription at the base in a language you don't know, but reading them aloud in your head you feel they make sense.",
            "altare": "A square basalt altar. On top, three objects untouched by time: a seal, a trident, a coral crown. Who put them there? And why?",
            "coralli": "Corals grow on the columns in patterns too regular to be natural. As if someone had taught them to grow like that.",
        },
    },
    "foresta": {
        "nome": "Tropical Forest",
        "descrizione": "A high forest of palms and tropical trees you can't name. The light comes through in golden slashes among the dense leaves, and the ground is a soft carpet of ferns and fallen fruit. Birds cry somewhere you cannot see, insects sing, and sometimes something larger moves among the shadows.\n\nTo the south, the beach. To the north, a clearing opens among the trunks.",
        "descrizione_breve": "Dense tropical forest. Beach to the south, clearing to the north.",
        "esaminabili": {
            "alberi": "The trunks are smooth, the wood of an unusual red. Carvings at the height of a man show they are old — and have been watched by humans before.",
            "uccelli": "You never see them. But the cries come from everywhere, always moving. Some sound almost like words.",
            "frutti": "Fruits fallen to the ground. Some you recognize — mangoes, bananas. Others no.",
        },
    },
    "radura": {
        "nome": "Forest Clearing",
        "descrizione": "A clearing where the sun reaches the ground. Wildflowers — yellow, red, purple — carpet it in random patches. In the center, a stone circle carved smooth, perhaps the foundation of something that no longer exists.\n\nTo the south the forest goes back to the beach. To the west, a village. To the north, the jungle wall begins — too thick to pass through without a good blade.",
        "descrizione_breve": "Sunny clearing with stone circle. Forest to the south, village to the west, dense jungle to the north.",
        "esaminabili": {
            "cerchio": "A circle of carved stones, each with a symbol. The symbols are worn, but one is clearer than the others: a stylized sun. Or is it a lighthouse?",
            "fiori": "Flowers of every color. Some smell like candy, others like ash. One has perfectly geometric petals — twenty-one, you count. A prime number.",
            "parete_vegetazione": "A wall of creepers and brambles, too thick to pass through. A good blade would help. Even better: a machete.",
        },
    },
    "scogliere_sud": {
        "nome": "Southern Cliffs",
        "descrizione": "Sheer cliffs overlooking the sea, wind in your hair, gulls circling far below. The rock is dark and slippery with spray. A message, half-buried in the sand of the path, catches your eye.\n\nThere's nowhere to go from here but back — unless you count the narrow staircase that descends south along the rock face, toward what looks like a remote cove of wrecks.",
        "descrizione_breve": "Southern cliffs overlooking the sea. A narrow staircase descends south.",
        "esaminabili": {
            "gabbiani": "Gulls glide in wide circles. One keeps watching you, its head tilted, as if it were about to tell you something it can't.",
            "roccia": "Dark volcanic rock, chipped by the wind of millennia. Some fragments contain glittering metal flecks.",
            "calata_sud": "A narrow staircase, carved into the rock, descends toward a remote cove. From up here you can't see the bottom, but you can feel the wind carrying up a smell of rotting wood and rust.",
        },
    },
    "villaggio": {
        "nome": "Inhabitants' Village",
        "descrizione": "A small village of thatched huts arranged in a circle around a central fire pit. Several figures move about their business with calm slowness. They wear clothes of woven fiber and shell necklaces. When they see you, they don't seem surprised — as if they had been expecting you.\n\nIn the center sits Kaia, the elder, on a stone bench. Two other villagers — Marco and Tiko — are busy at their tasks.",
        "descrizione_breve": "Small village with thatched huts. Kaia, Marco and Tiko here.",
        "esaminabili": {
            "focolare": "A fire pit still warm. A pot of something bubbling. The smell is of fish, herbs, and something else you don't recognize.",
            "capanne": "Well-built huts, woven palm roofs. Each has a decoration on the door: a shell, a feather, a geometric drawing.",
        },
    },
    "molo": {
        "nome": "Old Pier",
        "descrizione": "A wooden pier extending into a calm bay. Fishing nets hang to dry. A small boat is moored at the end, but it looks out of shape: some planks are loose, a piece of the prow is missing. Rusty nails scattered on the deck suggest someone was working on it and then stopped.",
        "descrizione_breve": "Wooden pier with a damaged boat. Fishing nets drying.",
        "esaminabili": {
            "barca": "A small fishing boat in rough shape. Some planks are loose, a piece of the prow is missing. With rusty nails and good wood you could fix it.",
            "reti": "Nets hung to dry. They smell of fish and salt. Professional work.",
            "acqua": "The water of the bay is calm and transparent. You see the bottom: rocks, algae, the occasional fish. Below, deeper down, something dark and big that barely moves.",
        },
    },
    "giungla": {
        "nome": "Jungle",
        "descrizione": "Thick tropical jungle that envelops you on every side. The machete makes every step possible: without it, you would not have gotten this far. Creepers hang from every tree, and the air is dense and hot. To the north, something bigger seems to loom through the vegetation — giant roots, smooth moss-covered stones. Perhaps ruins.",
        "descrizione_breve": "Thick tropical jungle, cleared with the machete.",
        "esaminabili": {
            "liane": "Creepers thick as arms, some with long thorns. If you wanted, you could cut one off — but then what?",
            "alberi_alti": "Trees so tall you can't see the top. Between the leaves, sometimes, sunlight filters in golden shafts.",
            "rumori": "Confused noises in the distance. Could be animals. Could be something else.",
        },
    },
    "giungla_profonda": {
        "nome": "Deep Jungle",
        "descrizione": "The jungle gets worse. Wet, dark, strangely silent. The paths here are irregular — as if made by something not shaped like a human. In the distance, you glimpse a precipice: a ravine that descends into darkness. You can't cross it without a rope.\n\nTo the north, a narrow path climbs upward toward the mountains. To the south-east, paths fork around an ancient stone totem.",
        "descrizione_breve": "Dark deep jungle. Precipice to the east (need rope). Mountain path north. Totem south-east.",
        "esaminabili": {
            "precipizio": "A ravine that descends into darkness. From up here you can't see the bottom. You'd need a good rope to climb down.",
            "fango": "The ground is muddy and bears strange prints. Not human feet. Not even animals you know.",
            "silenzio": "There's no insect noise here. No birds. Only the dripping of water and your own breathing.",
            "sentiero_sudest": "Toward the southeast, a narrow path winds among the tallest trunks. You can make out an opening — perhaps a crossroads.",
        },
    },
    "capanna_luna": {
        "nome": "Luna's Hut",
        "descrizione": "A wooden hut inside the jungle, hung with bundles of dried herbs and unlit candles. Luna sits in the center, on a mat, her eyes closed. When she opens them, they are luminous — a blue too clear for this world. She knew you were coming.",
        "descrizione_breve": "Luna's shaman hut, full of herbs and symbols.",
        "esaminabili": {
            "erbe": "Bundles of dried herbs hanging from the ceiling. Some you recognize (sage, thyme), others no. The smell is complex: sweet, bitter, medicinal.",
            "candele": "Candles of natural wax, unlit. Each one has a symbol carved at the base.",
            "mappe": "Old maps, drawn on bark. The island is drawn differently than on the map fragment you found — bigger, with extra parts that don't exist in today's reality.",
        },
    },
    "sentiero_montagna": {
        "nome": "Mountain Path",
        "descrizione": "A narrow path that climbs rapidly up the mountainside. Loose stones under your feet, cold wind, pines that get sparser the higher you go. Down on the valley, you can see almost the entire island — tiny, green, surrounded by the infinite blue of the sea.\n\nA pickaxe, abandoned, lies among the stones.",
        "descrizione_breve": "Mountain trail with an abandoned pickaxe.",
        "esaminabili": {
            "vista": "From up here the entire island looks like a toy. You can trace every place you have visited, in order. You are a small dot moving on something much older than you.",
            "pini": "Gnarled pine trees that grow between the rocks. The wind makes them whistle in a way that almost sounds like human voices.",
            "pietre": "Stones, loose, some pitted by tools. Someone worked up here. Long ago.",
        },
    },
    "cima_vulcano": {
        "nome": "Volcano Summit",
        "descrizione": "The summit of the volcano. A black crater opens at your feet, filled with slowly flowing lava that emits light and heat. The air is acrid and breathing burns, but from this position you can see the heart of the earth. On the crater's edge, a dark crystal juts out of the rock — shaped by the heat into a perfect point.",
        "descrizione_breve": "Volcano summit with lava crater. Volcanic crystal on the edge.",
        "esaminabili": {
            "lava": "The lava flows slowly, like thick blood. Dropping a stone in, it disappears with a hiss and a spray of sparks. Don't fall in.",
            "crepacci": "Small fissures from which yellowish gas escapes. The smell is unbearable. Best not to linger.",
            "cielo_vulcano": "From up here the sky is clearer than anywhere else. You see Venus even in broad daylight. It's comforting.",
        },
    },
    "scogliere": {
        "nome": "Northern Cliffs",
        "descrizione": "Rocky cliffs overlooking the sea, wind and waves crashing below. To the west, standing against the sky, the shape of the ancient lighthouse — a cylindrical tower of stone, dark and solitary. It waits.",
        "descrizione_breve": "Northern cliffs. The ancient lighthouse to the west.",
        "esaminabili": {
            "orizzonte": "Nothing. Empty sea to the horizon. If you came from somewhere, you can no longer remember which direction.",
            "faro": "The lighthouse stands against the sky. Ancient, worn, but still upright. It waits for someone to bring it back to life.",
            "mappa_frammento": "Among the rocks, a piece of parchment. A small fragment of an old map — you slip it into your bag without thinking.",
        },
    },
    "faro": {
        "nome": "Abandoned Lighthouse",
        "descrizione": "Inside the ancient lighthouse. A spiral staircase rises toward the top, where a dormant brazier awaits — three offerings to wake it: oil, crystal, gem. When all three are in place, the ancient flame will light up, and whatever happens next... happens.",
        "descrizione_breve": "Inside the lighthouse. Dormant brazier at the top awaiting three offerings.",
        "esaminabili": {
            "scala_spirale": "Worn stone steps. The center is hollowed by thousands of feet that climbed it before you.",
            "braciere": "A bronze brazier, round, with three indented slots. Each labeled: OIL, CRYSTAL, GEM. Put them in the right order, and the flame will awaken.",
            "diario_guardiano": "On a stool, a metal diary. Pages of ink and dust. The last page ends mid-sentence: 'I do not know if whoever comes after me will understand. I hope—'",
            "pavimento_faro": "When the lighthouse is lit, the stone floor opens like a metal flower. Below, a vertical well descends into the depths.",
        },
    },
    "rovine": {
        "nome": "Ancient Ruins",
        "descrizione": "The ruins of a civilization older than any you know. Stones covered in vines, half-fallen columns, floor tiles with carvings. At the center of the main court, an open arch leads 'inside' — to a vast hall.",
        "descrizione_breve": "Ancient ruins covered in vines. An arch leads inside.",
        "esaminabili": {
            "colonne_rotte": "Columns broken by time. The remains still standing are carved with scenes — people climbing, people descending, people meeting each other.",
            "tegole": "Floor tiles smooth from millennia of feet. Each has a symbol. Walking over them, you feel that the symbols change based on the direction.",
            "arco": "An open arch, with no door. The one inside.",
        },
    },
    "sala_guardiano": {
        "nome": "Guardian's Hall",
        "descrizione": "A vast hall of ancient stone, supported by columns carved with figures of animals you don't recognize. At the center, hovering at knee height above the ground, a luminous figure made of soft blue light. A guardian. An ancient one. It raises a hand when it sees you enter, and its voice reverberates from everywhere and nowhere:\n\n'Come forward, traveler. Two riddles await you. Two chances to prove that you know how to listen.'",
        "descrizione_breve": "Vast stone hall with the glowing Guardian at the center.",
        "esaminabili": {
            "guardiano_fig": "A figure of translucent blue light, in the shape of a human but too tall and too thin. Its face is calm and infinitely old.",
            "colonne_anim": "Columns carved with unknown animals: bird with hooked beak, four-eyed fish, octopus-man. The same figures you saw elsewhere.",
            "tavoletta": "On a small table, a metal tablet. Engraved with symbols that seem to shift when you don't look at them.",
        },
    },
    "cripta": {
        "nome": "Underground Crypt",
        "descrizione": "An underground crypt, dimly lit by your torch. Sarcophagi line the walls, some sealed, others open and empty. Dust, cobwebs, ancient incense. An ancient tablet, neglected, sits on a pedestal.\n\nAn irregular crack runs through the north wall. Loose stones seem to hide a tunnel behind them.",
        "descrizione_breve": "Underground crypt with sarcophagi and a cracked wall to the north.",
        "esaminabili": {
            "sarcofagi": "Stone sarcophagi, each one sealed. Some carved with names. You don't recognize them.",
            "polvere": "Dust thick enough to leave footprints. Your footprints are the only new ones here.",
            "pedestallo": "A pedestal of dark basalt. The top is smooth, and on it rests an ancient tablet.",
            "muro_screpolato": "An irregular crack runs through the north wall. Loose stones seem to hide a tunnel behind them. You'd need something sturdy to break it.",
        },
    },
    "laguna": {
        "nome": "Hidden Lagoon",
        "descrizione": "A lagoon of impossible turquoise water, hidden among the mangroves. A waterfall falls from a mossy rock, and the sound of falling water is the only sound for miles. In the middle of the water, a black pearl rests on a natural rock — as if placed there for you.",
        "descrizione_breve": "Hidden lagoon with waterfall and black pearl.",
        "esaminabili": {
            "cascata": "The waterfall is small but steady. The water is freshwater, drinkable. Behind the veil of water, something seems to glow. A cave? Or just reflections?",
            "mangrovie": "Mangroves rise from the water with roots exposed like long fingers. Small fish weave among them.",
            "perla": "A black pearl the size of your fist. It's on a natural pedestal of wet stone. Someone placed it there — recently, or long ago, you can't tell.",
        },
    },
    # ATTO II
    "pozzo_faro": {
        "nome": "The Lighthouse Well",
        "descrizione": "When the lighthouse flame rose toward the sky, something moved beneath your feet. The stone floor of the lighthouse opened like a metal flower, revealing a vertical well of black stone. A spiral staircase descends into darkness, lit by a green-blue light that pulses from below like a slow heartbeat.\n\nThe air rising from the well is cold and smells of damp stone and something older — a scent of worked metal and forgotten time.",
        "descrizione_breve": "Vertical well of the lighthouse. A spiral staircase descends.",
        "esaminabili": {
            "pavimento": "Perfectly interlocked stone slabs with spiral geometric patterns. They weren't laid, they were grown — as if the stone itself had been cultivated.",
            "scala": "A spiral staircase of basaltic stone. The steps are worn in the middle: thousands of steps before yours.",
            "luce_verde": "The light comes from far below. It's not fire — it's something alive. It pulses slowly, like a breath.",
        },
    },
    "cripta_meccanica": {
        "nome": "Mechanical Crypt",
        "descrizione": "The stairs end in a low-ceilinged hall supported by pillars of black iron. Along the walls, bronze shelves hold rows of small gears of every size, some still covered in fresh oil — as if someone had lubricated them yesterday.\n\nAt the center of the hall, a cylindrical pedestal rotates slowly on itself with a barely audible hum. To the north, a corridor runs into the rock. To the east, a narrower opening lets out a hiss of steam.",
        "descrizione_breve": "Anteroom to the machine-city. Gear shelves, rotating pedestal.",
        "esaminabili": {
            "piedistallo": "A brass column rotates on itself with perfect motion, as if nothing had ever stopped it. Above, the engraving of an open eye.",
            "scaffali": "Gears of every size, sorted by diameter. Fresh oil on your fingers: someone still cares for them.",
            "iscrizione": "An inscription on the wall in unknown characters. You recognize only one symbol: three concentric circles, like a target.",
            "ombra_ovest": "On the west wall, an anomalous shadow. Approaching, you see that it's actually the mouth of a low, forgotten corridor. A single metal plate barred it once, but it's fallen long ago.",
        },
    },
    "sala_ingranaggi": {
        "nome": "Hall of Gears",
        "descrizione": "You lose your breath. The hall is as big as a cathedral, and every surface — walls, ceiling, floor — is covered in gears turning slowly, locked into each other in a mathematical ballet of metal. The sound is that of a giant clock beating an unknown rhythm.\n\nAt the center, a circular iron platform sits still. A crank sticks out on its side, but the knob is missing. To the west the archive opens, to the east the observatory. To the north, a massive bronze door waits — closed.\n\nOn a side workbench, among various tools, you recognize a copper and iron steam valve.",
        "descrizione_breve": "Cathedral of rotating gears. Central platform, crank without knob, workbench with valve.",
        "esaminabili": {
            "piattaforma": "A circular platform of black iron. It doesn't move. The lateral crank spins freely: it should end with a knob which is missing.",
            "manovella": "The shaft is polished brass. On top, a hexagonal flange where evidently something was screwed on.",
            "ingranaggi_grandi": "The largest gears are as tall as houses. They turn without hurry, as if they had all the time in the world.",
        },
    },
    "corridoio_vapore": {
        "nome": "Steam Corridor",
        "descrizione": "The corridor is narrow and humid, crossed by thick copper pipes hissing under pressure. The valve you installed regulates the flow, but the air is still dense and hot, and the floor is covered in condensation reflecting the blue-green light.\n\nAt the end of the corridor, a low door leads to what must have been the ancients' forge.",
        "descrizione_breve": "Corridor of hissing copper pipes. Leads to the forge.",
        "esaminabili": {
            "tubi": "Copper pipes as thick as an arm, flowing with hot steam. The joints are hand-wrought.",
            "condensa": "Water on the floor reflects light in unstable pools. It drips from the ceiling too.",
            "valvola": "The valve you installed turns rhythmically, dosing the steam in controlled breaths.",
        },
    },
    "forgia_antica": {
        "nome": "Ancient Forge",
        "descrizione": "The hall is dominated by a large octagonal furnace still lit. Inside, the fire is not wood: it's something liquid and orange that flows and cools in patterns never the same. In front of the furnace, two copper automatons as tall as men move in slow motion, hammering with endless strokes a blade that never finishes being forged.\n\nOn a side table, abandoned tools. In a corner, a small altar with a stone chalice in the center — empty.",
        "descrizione_breve": "Forge still active with copper automatons. Altar with empty chalice.",
        "esaminabili": {
            "fornace": "The fire is not fire. It's a liquid metal that burns with a life of its own. Looking at it too long hurts your eyes.",
            "automi": "Two copper figures as tall as you. Their faces are smooth masks. They strike the hammer with perfect cadence, ignoring you.",
            "tavolo": "Blacksmith tools: pliers, tongs, files. A row of wrenches of every size. The dust is a thin uniform layer: work stopped not long ago.",
            "altare": "A basalt altar with a stone chalice at the center. The chalice has an internal groove as if to receive a sacred liquid.",
        },
    },
    "archivio": {
        "nome": "The Endless Archive",
        "descrizione": "A circular hall of seven floors, with shelves rising until they are lost in the darkness. A spiral staircase runs along the walls. The books are not paper — they are thin metal sheets, engraved. Thousands. Hundreds of thousands.\n\nIn the center, on a pedestal, floats a translucent figure: a woman's face made of light, eyes closed. Hands folded. She does not move, but you are breathing too loud, and suddenly she opens her eyes.",
        "descrizione_breve": "Circular library of seven floors. The Archivist floats at the center.",
        "esaminabili": {
            "scaffali": "Thin metal sheets, each engraved with thousands of tiny symbols. An entire civilization preserved.",
            "scala_spirale": "Rises to the seventh floor, where darkness swallows the light. The steps are made for feet smaller than yours.",
            "lastre_metallo": "You try to lift a sheet: it weighs like a page. It's metal, but flexible as paper. Technology you don't understand.",
        },
    },
    "osservatorio": {
        "nome": "Underground Observatory",
        "descrizione": "A hemispherical hall with a domed ceiling that — incredibly — projects above you the night sky. But this is not the sky you saw on the island: these are stars you have never seen, constellations of a world before yours.\n\nAt the center, a large brass astrolabe with levers, buttons and an empty lens on top where something evidently fit. On the wall, a mosaic of three aligned stars pulses rhythmically.",
        "descrizione_breve": "Observatory with projected sky. Astrolabe missing its lens.",
        "esaminabili": {
            "soffitto": "Stars projected by a hidden mechanism. You recognize some distorted constellations; others are completely new.",
            "astrolabio": "A wonderful brass astrolabe. The lens on top is missing: a circular groove awaits a new one, green in color.",
            "mosaico": "Three stars in a row — the belt of an ancient constellation? They pulse in sync.",
        },
    },
    "cuore_macchina": {
        "nome": "Heart of the Machine",
        "descrizione": "A cubic hall, empty at the center except for an immense golden pendulum that descends from the ceiling and swings slowly, slowly, on a lone pivot. Above the pendulum, suspended in mid-air, floats a crystal heart — the Heart of the Machine — dark, off, waiting.\n\nThe walls are covered with a mosaic of symbols that changes as you move: the pendulum reflects them onto you, and you are now part of the mechanism.",
        "descrizione_breve": "Hall of the giant pendulum. Dark crystal heart suspended above.",
        "esaminabili": {
            "pendolo": "Golden pendulum, swings in a perfect arc. The pivot is well oiled. Something is missing that should hold it: a stopper, a knob.",
            "cuore": "The Heart of the Machine. Opaque black crystal. Waits to be awakened — but by what?",
            "mosaico_pareti": "Symbols that rearrange as you walk. They seem to reflect your movement, as if the hall itself were conscious.",
        },
    },
    "agora_perduta": {
        "nome": "Lost Agora",
        "descrizione": "You emerge into a huge cavern that suddenly opens, and you realize you are inside the city. An octagonal plaza surrounded by buildings carved into living stone, tall as palaces. Colossal statues of crowned figures look down at you, immobile, eternal.\n\nAt the center of the plaza, on a basalt throne, sits a giant patinated metal automaton — the head bowed, waiting. As you approach, it slowly raises its gaze. It is alive. It was waiting for you.\n\nAt the feet of the throne, half-hidden, you make out an ancient chest closed by a four-wheel lock.",
        "descrizione_breve": "City plaza under the mountain. Automaton-King awaits on the throne. A locked chest at his feet.",
        "esaminabili": {
            "statue": "Eight colossal statues, each with a different crown. Kings and queens of an age before the ages.",
            "trono": "Basalt throne. The Automaton-King sits composed, waiting. He's not a statue: he breathes, slowly.",
            "edifici": "Buildings carved into living rock. Empty windows. It was a city, a real city. How many lived here? Where did they go?",
            "scrigno": "A black metal chest closed by a four-wheel lock. Above each wheel, mysterious symbols: planets, geometries, Roman numerals. The right combination opens it.",
        },
    },
    "via_titani": {
        "nome": "Avenue of the Titans",
        "descrizione": "A long avenue, as long as a Roman way, lined with stone statues twenty meters tall. The Titans — ancient guardians — sit or stand, each with a different weapon: a spear, a hammer, a book, a seal. Beneath your feet, smooth obsidian slabs, each with an inlaid symbol.\n\nAt the end of the avenue, a circular stone portal. Closed. Above it, three recesses: one triangular, one square, one pentagonal.",
        "descrizione_breve": "Avenue of colossal statues. Circular portal with three recesses.",
        "esaminabili": {
            "titani": "Eight statues, eight Titans. Each holds a symbol-object. Perhaps they say something, together.",
            "ossidiana": "Polished obsidian slabs, each with a symbol: stars, eyes, hands, seeds. Trodden by thousands of pilgrims.",
            "portale": "Circular dolomite portal. Doesn't open. Above, three geometric recesses: triangle, square, pentagon.",
            "incavi": "Triangle, square, pentagon. Three shapes. Three objects that probably fill them.",
        },
    },
    "abisso": {
        "nome": "The Abyss",
        "descrizione": "A huge crack in the world. Below you, the abyss descends beyond sight, breathing a cold wind that tastes of ancient stone. A suspension bridge of planks and ropes crosses the void toward a platform on the other side — but the main ropes are broken, two planks are missing, and the bridge sways dangerously with every breath.\n\nBelow you, far far away, you see a point of living light — something inhabits it. The Root of the World, perhaps.",
        "descrizione_breve": "Chasm crossed by a broken bridge. Below, a point of light.",
        "esaminabili": {
            "ponte": "Suspension bridge. The main ropes are broken; two planks of the floor are missing. Would need metal ropes and an iron rail to repair it.",
            "vuoto": "You look down and get dizzy. Below, a point of living light. Something alive moves down there.",
            "vento": "The wind rises from the abyss and smells of hot stone. It's not just air: it's the breath of something.",
        },
    },
    "radice_mondo": {
        "nome": "The Root of the World",
        "descrizione": "You have descended, you have crossed, you have opened. Now you are at the center.\n\nA perfect spherical hall of black crystal. At the center, suspended in mid-air with no support, is a tree of light — not a real tree, but a branching structure of pure green-blue light, the roots descending and the branches rising, infinite in both directions. It is the heart of the island, the source of every mystery you have encountered.\n\nBefore the tree, a stone pedestal. On it, a blackened metal crown: the Titanic Crown. Empty. Waiting to be completed.",
        "descrizione_breve": "Spherical hall with the Tree of Light. Titanic Crown on the pedestal.",
        "esaminabili": {
            "albero": "A tree made of pure light. Emits no heat, but you feel it singing in your bones. It is alive. It has been alive from before the island, from before everything.",
            "piedestallo": "Raw stone with a hollow to receive the crown. Below, an inscription: 'WHOEVER WEARS, DOES NOT RETURN THE SAME AS THEY WERE.'",
            "corona_vuota": "A black metal crown. Eight empty points. Each point seems made to receive a crystal or a star.",
        },
    },
    # ATMOSFERICHE
    "cimitero_marino": {
        "nome": "Sea Graveyard",
        "descrizione": "A remote cove where the sea has gathered the remains of a century of wrecks. Dozens of broken hulls rust on the black sand, some with the name still legible on the prow. The waves whisper among the bones of wood, and every now and then a metal creaks, as if something were waking underneath.\n\nThere is nothing to collect here. Only to listen. Only to remember that you are not the first to arrive — only the first still alive.",
        "descrizione_breve": "Remote cove full of ancient wrecks. Only silence and rust.",
        "esaminabili": {
            "relitti": "Dozens of broken hulls. On one: 'AURIGA - 1873'. On another: 'PALINURO - 1924'. A modern ship: 'Capricho II - 2019'. All ended up here. None ever left again.",
            "ossa_legno": "Bones of wood. Ships are creatures, and these are their carcasses. The tide moves them slowly, as if in pity.",
            "metallo_cigolante": "From one of the larger wrecks, a rhythmic creaking. Not wind, not wave. Something slower. Something patient.",
            "sabbia_nera": "Basalt sand, fine as powder. On the dunes, geometric patterns form when the wind turns. Your footprints erase themselves in seconds.",
        },
    },
    "bivio_giungla": {
        "nome": "Crossroads of the Ancients",
        "descrizione": "A natural crossroads in the deep jungle, where three paths meet around a two-meter-tall stone totem, carved with animal figures you don't recognize: a bird with a hooked beak, a fish with four eyes, a creature half-man and half-octopus.\n\nYou cannot proceed from here — the secondary paths lead only to dead ends thick with brambles. But this place has something. A presence.",
        "descrizione_breve": "Crossroads of paths around an ancient totem.",
        "esaminabili": {
            "totem": "Basalt stone carved with mastery you have never seen. The three figures look at each other in a circle, as if waiting for someone to complete the quartet.",
            "uccello_becco": "The bird has a hooked beak and deep eyes. Below its figure, an inscription: 'who flies sees all, but does not return'.",
            "pesce_quattro_occhi": "A fish with four eyes in a circle. Inscription: 'who swims in the dark is not afraid of it'.",
            "uomo_polipo": "The most disturbing figure: half-man, half-octopus. Inscription: 'who unites two worlds belongs to none'.",
            "sentieri_morti": "Three secondary paths wind into the vegetation, but after a few meters they are swallowed by brambles. Would need the machete and half a day. Not worth it.",
        },
    },
    "corridoio_perduto": {
        "nome": "Forgotten Corridor",
        "descrizione": "A low, forgotten corridor, discovered by chance among the shadows of the mechanical crypt. The ceiling drips with a condensation that barely glows, and the walls are covered with names — thousands of names — carved into the metal by different hands, in different eras.\n\nThey are the names of all the Builders who descended before you. Those who never came back up. The corridor ends in a smooth wall: no door, only a final inscription, at the top, too high to read clearly.",
        "descrizione_breve": "Forgotten corridor full of carved names.",
        "esaminabili": {
            "nomi": "Thousands of names. Some in characters you recognize, others in alphabets you have never seen. All engraved with care, some with tremor. One is a little girl: 'Mira, seven years old, descended with her mother.'",
            "iscrizione_alta": "The inscription at the top of the wall: 'WE HAVE CHOSEN. YOU WHO READ: YOU CAN TOO.' Below, in small: 'Not by force. Never by force.'",
            "condensa_brillante": "The drops from the ceiling glow faintly. They fall slowly, always in the same rhythm, as if counting something.",
            "pareti": "Black metal cold-worked. Polished by thousands of hands that touched it to read the names in the dark.",
        },
    },
    "cunicolo_nascosto": {
        "nome": "Hidden Tunnel",
        "descrizione": "You broke through the crypt wall with the pickaxe, and what opened is a low, dry, perfectly intact tunnel. Ancient dust laid on a stone altar. Above the altar, under an intact glass dome, a small copper lamp still burns with warm light — lit from who knows when, fed by who knows what.\n\nThe air smells of myrrh. On the back of the altar, an inscription: 'to the light that knows neither dawn nor dusk'.",
        "descrizione_breve": "Secret tunnel with an ancient eternal lamp.",
        "esaminabili": {
            "altare": "A small altar of white limestone. The top surface is polished by centuries of invisible offerings.",
            "cupola_vetro": "A small dome of blown glass, millennia old, still perfectly transparent. Technology you cannot explain.",
            "lampada": "The copper lamp glows with a small, perfectly still flame. It consumes no oil, emits no smoke. It has been glowing since before you were born.",
            "polvere": "Very fine dust, laid uniformly. Your footprints are the first in millennia.",
        },
    },
}

ITEMS_EN = {
    "legna": ("Beached wood", "Wooden planks recovered from the wreck. Dry and solid — perfect for building something or lighting a fire."),
    "corda": ("Sturdy rope", "A length of thick rope from the ship's rigging. Frayed but still strong."),
    "bottiglia": ("Empty glass bottle", "A green glass bottle, well-sealed, empty."),
    "pietra_focaia": ("Flint stone", "A dark, sharp stone. Struck with metal or hard wood, it creates sparks."),
    "conchiglia": ("Spiral shell", "A large spiral shell, beautiful. It seems to contain the sound of the sea."),
    "lama_antica": ("Ancient obsidian blade", "A long blade of volcanic obsidian, sharp as a razor. Ancient, but preserved. Could become a weapon — or a tool."),
    "artefatto_sacro": ("Jade sacred artifact", "A carved jade statuette, smaller than your palm but heavier than it looks. It depicts a female figure with open arms."),
    "ramo_robusto": ("Sturdy branch", "A long, thick branch, useful as a handle for something."),
    "bacche": ("Red berries", "A handful of red berries of uncertain type. They smell sweet. Eating them could restore energy, or could kill you."),
    "fiori": ("Unusual flowers", "A small bouquet of strange flowers. Someone might appreciate them."),
    "chiodi_arrugginiti": ("Rusty nails", "A handful of iron nails eaten by rust. Still usable, for practical purposes."),
    "messaggio_bottiglia": ("Message in a bottle", "Rolled-up parchment inside an old glass bottle. The writing is faded but legible."),
    "rete_pesca": ("Fishing net", "A professional fishing net, in good condition."),
    "olio_vegetale": ("Vegetable oil", "A vial of thick, aromatic oil, extracted from rare jungle plants. Burns with a steady warm flame — perfect for the lighthouse."),
    "resina": ("Tree resin", "Sticky golden resin collected from a wounded tree. Useful for sealing and gluing."),
    "pianta_rara": ("Rare plant", "A plant with jagged leaves and small white berries. Shines slightly in the shade. It is unknown to you, but not to Luna."),
    "erbe_secche": ("Dried herbs", "A bundle of dried healing herbs, bound with thin rope."),
    "piccone": ("Iron pickaxe", "A heavy pickaxe with an iron head and wooden handle. Made to break stones."),
    "cristallo_vulcanico": ("Volcanic crystal", "A dark crystal shaped by volcanic heat into a perfect point. When you hold it, your fingertips tingle."),
    "frammento_mappa": ("Map fragment", "A quarter of an old parchment map. Shows the island with a name you cannot read and a cross over the lighthouse."),
    "diario_guardiano": ("Guardian's diary", "A metal diary kept by the keeper of the lighthouse. Dense pages written in small handwriting."),
    "gemma_potere": ("Power gem", "A perfectly cut gem that shines with soft blue light. Source of energy for the ancient lighthouse."),
    "tavoletta_antica": ("Ancient tablet", "A flat stone tablet carved with symbols that shift slowly when you don't look at them."),
    "attrezzatura_sub": ("Diving gear", "Diving equipment for underwater exploration: goggles, regulator, ancient but functional fins."),
    "perla_nera": ("Black pearl", "A fist-sized black pearl. Pulses with its own inner light."),
    "sigillo_antico": ("Ancient seal", "A metal seal with a priest's mark of the old cult of the lighthouse."),
    "tridente": ("Ceremonial trident", "A bronze ceremonial trident with three points symbolizing the three powers of the lighthouse: oil, crystal, gem."),
    "corona_corallo": ("Coral crown", "A childlike crown of woven coral branches. Belonged to a girl of the sunken people."),
    "torcia": ("Lit torch", "Sturdy wood wrapped in resined cloth, lit by your flint. Burns steady."),
    "machete": ("Obsidian machete", "The ancient obsidian blade mounted on the sturdy branch. Cuts jungle vegetation like paper."),
    "medaglione": ("Ancients' medallion", "A golden medallion engraved with the symbol of the eight-pointed crown. Opens the way to the ruins of the Ancients."),
    "chiave_faro": ("Lighthouse key", "A golden key shaped for a specific lock. Given by the Guardian."),
    "chiave_antica": ("Ancient key", "A silver key of unusual design. Given by the Guardian after the second riddle."),
    "antidoto": ("Antidote", "An amber-colored antidote prepared by Luna. Neutralizes ancient poisons."),
    # ATTO II
    "spore_lumino": ("Luminescent spores", "Spores collected near the well. Glow with cold green light, perfect for illuminating dark passages."),
    "ingranaggio": ("Copper gear", "A well-wrought copper toothed gear. Heavy in your hand. Seems part of a larger mechanism."),
    "ruota_dentata": ("Iron toothed wheel", "A large toothed wheel of black iron, wider than your palm. Fits perfectly with other gears."),
    "binario_ferro": ("Iron rail", "An iron axle as long as your arm, with a toothed rack on one side. Good for repairing structures or creating mechanisms."),
    "martello_rame": ("Copper hammer", "A hammer with a patinated copper head, dark wood handle. Heavy, balanced, made for those who know how to work metal."),
    "pendolo_ottone": ("Brass pendulum", "A golden pendulum with an inverted droplet weight. On top, a hexagonal flange to fix it to a mechanism."),
    "valvola_vapore": ("Steam valve", "An industrial valve of copper and iron, with a circular knob. Regulates high-pressure steam flow."),
    "ampolla": ("Crystal vial", "A hand-blown crystal vial. Narrow at the top, wide at the bottom. Empty, but evidently designed to contain something precious."),
    "catena_oro": ("Short gold chain", "A chain of heavy gold links. More jewel than tool, but strong enough to carry considerable weight."),
    "tavoletta_runica": ("Runic tablet", "A thin metal tablet carved with symbols that change slowly when you look at them. The Archivist could decipher it."),
    "funi_metalliche": ("Metal cables", "Cables of intertwined metal filaments. Strong, flexible, perfect for repairing a suspension bridge."),
    "frammento_stella": ("Star fragment", "A tiny fragment of a metal that shines with its own light. It's cold, but looking at it long warms you inside."),
    "occhio_titano": ("Titan's Eye", "A hard stone eye, perhaps sapphire, the size of your fist. When you hold it in hand, you have the feeling something is watching you."),
    "sigillo_re": ("King's Seal", "A stamp seal of black stone, with the symbol of an eight-pointed crown. Ancient authority, carved in stone."),
    "muschio_blu": ("Bioluminescent moss", "Fluorescent moss growing in the depths. Emits a blue-greenish light that gives no heat."),
    "cristallo_radice": ("Root Crystal", "A green-blue crystal pulsing slowly, like a small heart. Warm. Alive."),
    "radice_madre": ("Mother Root", "A very small root of the Tree of Light. Pulses in your hand, gentle as a tamed creature."),
    "corona_titanica": ("Titanic Crown", "A black metal crown with eight empty points. Ancient beyond any measure. It has known heads you couldn't imagine."),
    "meccanismo_completo": ("Gear mechanism", "Gear and toothed wheel united in a working mechanism. Ready to be mounted."),
    "manovella_completa": ("Complete crank", "A crank with the pendulum as knob: heavy, turns smoothly. Ready for the platform."),
    "funi_metalliche_intrecciate": ("Bridge repair kit", "Metal cables braided with iron rail: all needed to repair a suspension bridge."),
    "lente_smeraldo": ("Emerald lens", "Green lens cut from a single emerald. Looking through it, ordinary light becomes speaking."),
    "corona_attivata": ("Activated Titanic Crown", "The crown filled with the three symbols: star, root, eye. Pulses with soft, cold light. Ready to be worn."),
    "manovella_temp": ("Crank shaft", "The bare shaft of the crank, unscrewed. Awaits a knob to be fixed on top."),
    "corona_titanica_step1": ("Titanic Crown (partial 1)", "The crown with a star fragment inserted in one point. Missing the eye and the root."),
    "corona_titanica_step2": ("Titanic Crown (partial 2)", "The crown with two of the three energies inserted. Missing the living root."),
    "lampada_eterna": ("Eternal Lamp", "A copper lamp with a small, perfectly still flame. It has been burning before you were born and will burn after you die. Guarded for millennia in a forgotten tunnel."),
}

CHARACTERS_EN = {
    "kaia": {
        "nome": "Kaia",
        "descrizione": "An elderly woman with skin dark and wrinkled like tree bark. Her eyes are deep and wise, and her white hair is gathered in braids decorated with shells. She wears a necklace of pearls and bones, and moves with calm, confident dignity. She is the village elder.",
    },
    "marco": {
        "nome": "Marco",
        "descrizione": "A bearded middle-aged man, skin burned by sun and wind, eyes determined. Wears worn sailor's clothes — perhaps he too is a castaway, but long before you.",
    },
    "tiko": {
        "nome": "Tiko",
        "descrizione": "A young islander fisherman, dark hair, friendly smile. Simple clothes, bare feet. Seems to live half in the sea.",
    },
    "luna": {
        "nome": "Luna",
        "descrizione": "A young shaman woman with flowing black hair. Eyes too blue for this world. Tattoos of moon symbols on her forearms. Speaks slowly, choosing each word.",
    },
    "guardiano": {
        "nome": "Guardian",
        "descrizione": "A figure of translucent blue light in the shape of a human, too tall and too thin. Its face is calm and infinitely ancient.",
    },
    "archivista": {
        "nome": "The Archivist",
        "descrizione": "A translucent figure of light, vaguely feminine, floating a meter above the floor. Her face is serene and her eyes, when open, are a blue you've seen only at the heart of flames. She speaks without moving her lips, a voice you hear inside rather than outside.",
    },
    "re_automa": {
        "nome": "The Automaton-King",
        "descrizione": "A colossal automaton four meters tall, patinated copper-green metal. His body is covered in delicate inlays, and his crown — the one he wears — is simple, raw iron. His face is a copper mask with two slits for eyes: in the slits, a calm and very ancient light.",
    },
}

COLLECTIBLES_EN = {
    "conchiglia": ("Spiral shell", "The sea has a memory of its own. Bring it close to your ear: you hear the ancient weeping of all the ships that did not return."),
    "perla_nera": ("Black pearl of the lagoon", "Black pearls are said to be born in oysters that have seen a murder. This one has seen something worse: an entire civilization sealing itself under stone."),
    "corona_corallo": ("Coral crown", "A childlike crown, made of woven coral twigs. It belonged to a girl of the sunken people. She played at being queen before the end."),
    "frammento_mappa": ("Ancient map fragment", "Only a quarter of the original chart. Shows the island with a name you can't read and a cross over the lighthouse. Under the cross, small: 'the door'."),
    "messaggio_bottiglia": ("Message in a bottle", "'If you read this, you are the eleventh. The first ten became the light of the lighthouse. You decide whether you want to be the last torchbearer or whether you want to extinguish it.' Signed: the tenth."),
    "diario_guardiano": ("Guardian's Diary", "Pages of small handwriting. The last line, hastily scrawled: 'We were not gods. We were just the first to understand. I'm sorry, reader. Now you have to understand after me.'"),
    "tavoletta_antica": ("Cipher tablet", "Three symbols repeat: an eye, a star, a root. Below, the phrase: 'When the three return together, the world breathes again.'"),
    "sigillo_antico": ("Submerged temple seal", "The seal of a priest of the lighthouse cult. On the back, two words: 'light only'."),
    "tridente": ("Ceremonial trident", "The three points represent the three powers of the lighthouse: oil, crystal, gem. Those who held it called the ships. Those who held it also sank them."),
    "cristallo_radice": ("Root Crystal", "Pulses to the rhythm of the Tree of Light. If you hold it close to your heart, you feel your heartbeat synchronize with its. You stop being afraid. You stop being in a hurry."),
    "muschio_blu": ("Bioluminescent moss of the Abyss", "Grows only where sunlight has never arrived and never will. And yet it shines. Lesson: light does not always come from outside."),
    "spore_lumino": ("Threshold spores", "Gates between worlds release spores when they open. These are the spores from the lighthouse well — the first threshold you crossed."),
    "lampada_eterna": ("Eternal Lamp", "A light that burns from always without consuming itself. The Builders said: 'true light doesn't come from fuel, it comes from the decision to shine'. You now carry this decision with you."),
}

# Messages (room_actions, deliveries, puzzles, quests, etc.) — translated by key
ACTIONS_EN = {
    "machete::radura": "You grab the machete and throw yourself against the wall of vegetation to the north. Stroke after stroke, vines and brambles give way to the obsidian blade. Sweat runs down your forehead, but after half an hour of work a path opens through the jungle.\n\nThe way north is now clear.",
    "corda::giungla_profonda": "You anchor the rope to a sturdy tree and descend into the ravine. The jungle below is deeper and darker, but you finally have access.",
    "olio_vegetale::faro": "You pour the oil into the central well of the brazier. It immediately becomes thick and fragrant. One of the three slots is lit.",
    "cristallo_vulcanico::faro": "You place the volcanic crystal in the left slot of the brazier. It starts to pulse in rhythm with itself. The second of three slots is now ready.",
    "gemma_potere::faro": "You place the power gem in the right slot. It glows blue, bathing the entire chamber. The third and last slot is ready.",
    "valvola_vapore::cripta_meccanica": "You screw the valve onto the corridor fitting. The hissing of steam calms into a regular breath. The passage is now safe.",
    "manovella_completa::sala_ingranaggi": "You screw the complete crank onto the platform pin. Now it has grip: you can turn it. You do. The platform rises with a roar of gears waking up. It rises to the Heart of the Machine, suspended above you.\n\nThe Heart lights up, slowly, from black to pulsing green-blue. The north door in the same hall clicks open.",
    "funi_metalliche_intrecciate::abisso": "You work for hours. The ropes are stretched, the rail serves as a new axle, the missing planks are replaced. When you finish, the bridge is solid. You can cross it.",
    "lente_smeraldo::osservatorio": "You insert the emerald lens into the groove on top of the astrolabe. The stars projected on the ceiling change: they group, align, form a clear design — three stars in a row, perfectly aligned with the mosaic on the wall.\n\nThere's a click under your feet: a hidden door opens in the floor.",
    "corona_attivata::radice_mondo": "You lift the Titanic Crown with both hands. It weighs more than you expected: the weight of time. You bring it slowly to your head.",
    "meccanismo_completo::via_titani": "You insert the mechanism into the three recesses of the portal. The three shapes — triangle, square, pentagon — match perfectly. The gears of the mechanism speak to those of the portal, and for the first time in millennia the circular stone opens. An alternative path to the Root of the World opens.",
    "piccone::cripta": "You strike a blow, two, three. The loose stones give way one after another. Ancient dust rises. When the wall collapses completely, you face a small dry tunnel opening northward. The light of a warm flame glows at the end.",
    "martello_rame::sala_ingranaggi": "With the copper hammer you loosen the bolt at the base of the crank. The bare shaft detaches: you can now take it with you to mount it elsewhere.",
}

RECIPES_MSG_EN = [
    "You rub the flint on the dry wood. One, two, three times — until a spark comes to life. The flame grows, wrapping the wood. You have created a torch!",
    "You mount the obsidian blade on the sturdy branch. Leather strips from your clothing tie it firmly. You have a machete!",
    "You fit the toothed wheel onto the gear. They speak immediately, teeth and cavities, and rotate together with a click of mechanical satisfaction. You have a complete mechanism.",
    "You attach the pendulum to the crank shaft. It weighs just right. Now the crank has its knob — it's complete, ready to be turned.",
    "You braid the metal ropes around the iron rail. Now you have a kit to repair the bridge: a solid structure with the ropes supporting it.",
    "You insert the star fragment into the crystal vial. The light concentrates, focuses, becomes a lens. Now you have an emerald that sees beyond appearance.",
    "You place the star fragment in one of the crown's points. The point closes around the fragment and shines. Something is still missing: the eye and the root.",
    "You place the Titan's Eye in a second point. The crown vibrates. One more thing is missing: life itself, the root.",
    "You place the Mother Root in the third point. The three energies speak to each other: star, mind, life. The eight points light up one after another in cascade. The Titanic Crown is now ACTIVE. It pulses, soft and cold, in your hands.",
]

QUESTS_EN = {
    "quest_kaia": {
        "nome": "The Sacred Artifact",
        "descrizione": "Kaia has asked you to recover the sacred artifact from the sea caves.",
        "obiettivi": [
            {"desc": "Find the sacred artifact in the sea caves"},
            {"desc": "Bring the artifact back to Kaia in the village"},
        ],
    },
    "quest_tiko": {
        "nome": "Tiko's Boat",
        "descrizione": "Tiko needs resin and rusty nails to repair the boat.",
        "obiettivi": [
            {"desc": "Find resin in the deep jungle"},
            {"desc": "Find rusty nails on the southern cliffs"},
            {"desc": "Bring both to Tiko at the pier"},
        ],
    },
    "quest_luna": {
        "nome": "The Rare Plant",
        "descrizione": "Luna seeks a rare plant that grows only on the volcano summit.",
        "obiettivi": [
            {"desc": "Find the rare plant on the volcano summit"},
            {"desc": "Bring it to Luna in her hut"},
        ],
    },
    "quest_faro": {
        "nome": "The Ancient Lighthouse",
        "descrizione": "Relight the ancient lighthouse by placing oil, crystal and gem in the brazier at the top.",
        "obiettivi": [
            {"desc": "Find the three components"},
            {"desc": "Place them in the lighthouse brazier"},
        ],
    },
}

PUZZLES_EN = {
    "enigma1": {
        "testo": "The Guardian raises a luminous hand and the hall darkens. His voice echoes like a memory from the past:\n\n\"I live without breath,\ncold as death.\nNever thirsty, always drinking.\nIn armor, never clanking.\nWhat am I?\"",
        "successo": "The Guardian nods slowly, and light returns to the hall.\n\n\"The fish. Correct. You know the life that hides beneath the surface — this is the first step of wisdom.\"\n\nAn iron key appears in his luminous hands and floats toward you.",
        "fallimento": "The Guardian shakes his head.\n\n\"That is not the right answer. Wisdom requires patience and reflection. Return when you have thought more carefully.\"",
    },
    "enigma2": {
        "testo": "The Guardian observes you with piercing eyes.\n\n\"Very well. The second riddle:\n\nI have cities without houses,\nforests without trees,\nrivers without water,\nmountains without stone.\nWhat am I?\"",
        "successo": "The Guardian extends a luminous hand.\n\n\"The map. Correct. You know how to read the world at a distance — this is the second step of wisdom.\"\n\nA silver key materializes before you.",
        "fallimento": "The Guardian shakes his head once more.\n\n\"Not quite. Observe the world as if it were drawn, not lived.\"",
    },
}

PUZZLES_INTERACTIVE_EN = {
    "lucchetto_scrigno": {
        "testo": "The ancient chest at the feet of the throne. Four wheels, each with mysterious symbols. An inscription: 'THE SUN RISES IN THE EAST, THE SACRED TRIANGLE POINTS SKYWARD, ON THE THIRD DAY THE KING CAME, AND THE EARTH, THIRD PLANET FROM THE SUN, WELCOMED HIM.'",
        "successo": "The wheels align with a metallic click. The chest opens with a hiss of air escaping after millennia. Inside, resting on a veil of ancient silk, is the King's Seal.",
        "fallimento": "The wheels click into wrong positions. The chest remains closed.",
    },
    "stelle_osservatorio": {
        "testo": "The mosaic of three stars pulses in waiting. On the wall, a mechanism with three stone wheels corresponds to the three projected stars. Align each with the dashed mark to complete the ancient constellation.",
        "successo": "The three stars align perfectly. A click resonates: on the central astrolabe, a small opening reveals a star fragment embedded in the brass — a gift to one who has learned to look at the right sky.",
        "fallimento": "The stars vibrate but are not aligned. Try again.",
    },
    "pendolo_cuore": {
        "testo": "The giant pendulum swings slowly above you. The hall accompanies it with a precise beat. If you follow it with your rhythm for four beats, the Heart may listen.",
        "successo": "You have followed perfect time. The Heart above you emits a brief but clear glow — something has readied itself. From now on, the Heart will respond more quickly to the next mechanical intervention.",
        "fallimento": "The rhythm is off. The pendulum continues unperturbed. Try again when you have the right timing within you.",
    },
}

DELIVERIES_EN = {
    "artefatto_sacro::kaia": "You hand the sacred artifact to Kaia. Her hands tremble as she takes the jade statuette. Tears fill her eyes.\n\n\"You found it... after all these years. This artifact protected our village. Without it, fishing was poor and the sea was rough. Thank you, stranger.\"\n\nShe removes a medallion from her neck and offers it to you.\n\n\"Take this. It is the medallion of the Ancients — it will open the doors of the ruins in the jungle. There you will find the answers you seek.\"",
    "resina::tiko": "Tiko takes the resin with a grateful nod. \"Perfect. Now all I need are the nails.\"",
    "chiodi_arrugginiti::tiko": "Tiko takes the nails and combines them with the resin. His face lights up.\n\n\"You've saved me, stranger. I can finally repair the boat.\"\n\nHe works swiftly. Within an hour, the boat is seaworthy. \"It's yours too now. Use it to reach the hidden lagoon to the west.\"",
    "pianta_rara::luna": "Luna accepts the rare plant with reverent hands. She inhales its scent deeply.\n\n\"You found it where few dare to go. Take this — an antidote for ancient poisons. You may need it.\"",
    "tavoletta_runica::archivista": "You offer the runic tablet to the Archivist. She accepts it delicately, and for the first time smiles truly.\n\n\"A lost tablet. I read it. Ah... it is a map. A map of the Heart of the Machine, and of its three weak points. Keep it, now it will be more useful to you than to me.\"\n\nAfter a moment, from her tunic of light she produces a small gift and offers it to you.",
    "sigillo_re::archivista": "The Archivist immediately recognizes the seal. \"The mark of the King. You have spoken with him. Good. Then this is yours.\"\n\nShe hands you a small tablet inscribed with the answers to an ancient riddle — a gift of knowledge.",
}

ROOM_EXAMINABLES_EN = {
    "caletta": {"rocce": "Polished volcanic rock, rich with deep striations. Some fragments contain small glittering metallic flecks — ferrite? Or something else."},
    "grotte": {
        "stalattiti": "Stone icicles hang from the ceiling, some very long. Water drips with perfect regularity.",
        "muschio": "Phosphorescent moss. Emits a faint bluish light. Useful to see even without a torch — briefly.",
        "acqua": "The water of the pool is unnaturally clear. You see your face — but it looks older, or younger, you can't tell.",
    },
    "tempio_sommerso": {"bassorilievi": "Reliefs on the columns show a civilization that revered the lighthouse. Robed figures, raised arms, a central flame that is more than flame."},
    "villaggio": {
        "fuoco": "A fire pit still warm. Recent embers. Someone cooks here every day.",
        "reti": "Fishing nets spread out to dry. Well-maintained. Someone fishes here.",
    },
    "giungla": {
        "alberi": "Tall trees, some with bark carved with symbols. The symbols seem recent — within years, not centuries.",
        "insetti": "Luminous insects among the branches. They move in patterns too regular to be random.",
    },
    "capanna_luna": {
        "mortaio": "A stone mortar stained with herbs. Luna prepares remedies here.",
        "vasetti": "Small pots with dried herbs, each labeled with symbols you don't recognize.",
    },
    "cima_vulcano": {
        "cratere": "The crater plunges into a red glowing void. Looking long enough, you see figures — or imagine them.",
        "panorama": "From here you see the entire island. Small, isolated, infinite around it.",
        "cristalli": "Crystals of various colors scattered across the ground, formed by volcanic heat.",
    },
    "faro": {
        "meccanismo": "A bronze mechanism at the top of the stairs. Three slots wait: one round (oil), one pointed (crystal), one squared (gem).",
        "scala": "A spiral staircase rising endlessly. Steps worn smooth by centuries.",
        "lente": "The great lens of the lighthouse, still intact. When lit, it will focus the light for miles.",
    },
    "rovine": {
        "iscrizioni": "Inscriptions in an unknown alphabet. But three symbols recur: eye, star, root.",
        "colonne": "Broken columns, some still upright. Each one had a function — what?",
        "portale": "A stone portal covered in creepers. Beyond it, the Guardian's Hall.",
    },
    "sala_guardiano": {
        "altare": "A black basalt altar, empty. Once something was placed here.",
        "mosaico": "A complex floor mosaic: three spirals converging toward a central point.",
        "simboli": "Ancient symbols on the walls. The Guardian reads them as if they were fresh.",
    },
    "cripta": {"piedistallo": "A dark basalt pedestal. The top is smooth — for an offering, or a resting place."},
    "radice_mondo": {"piedistallo": "Rough stone with a hollow to receive the crown. Beneath, an inscription: 'WHOEVER WEARS, DOES NOT RETURN THE SAME AS THEY WERE.'"},
    "scogliere": {
        "orizzonte": "Nothing. Empty sea to the horizon. You can't remember which direction you came from.",
        "mappa_frammento": "Among the rocks, a piece of parchment. A small fragment of an old map — you slip it in your bag.",
    },
    "radura": {"parete_vegetazione": "A wall of creepers and brambles, too thick to pass. A good blade would help — even better, a machete."},
}

# Dialoghi mancanti: Marco, Tiko, Kaia stage residui
DIALOGUES_FULL_EN = {
    "marco": [
        {
            "condizione": {"flag": "barca_riparata"},
            "saluto": "Marco grins. \"Tiko fixed the boat. Now we have a real hope of getting out — if the lighthouse ever lights up.\"",
            "opzioni": [
                {"testo": "Tell me about yourself", "risposta": "\"Shipwrecked, like you. Three years ago. Four? I've lost count. Kaia took me in. The villagers are good people — but they're not like us. They've been here forever.\""},
                {"testo": "Why haven't you left yet?", "risposta": "\"With what? Until Tiko fixed the boat, nothing. And even now, the currents here are cruel. The lighthouse — if it burns again — is the only real signal. Otherwise you die out there.\""},
                {"fine": True, "testo": "See you later."},
            ],
        },
        {
            "saluto": "Marco looks up from a piece of wood he's whittling. \"Another one. You're newer than me, I can tell by how you stand. Not resigned yet.\"",
            "opzioni": [
                {"testo": "How long have you been here?", "risposta": "\"Three years ago? Four? I've lost count. My ship broke up on the southern cliffs. I woke up on the same beach where you probably did. Same sand, same nothing.\""},
                {"testo": "Do you know anything about this island?", "risposta": "\"Kaia tells the old stories — Builders, ancient lighthouse, sunken people. Half legend, half warning. What I know for sure: this island doesn't want to let us go easily.\""},
                {"testo": "How do we leave?", "risposta": "\"The lighthouse. Everything turns on the lighthouse. Light it and maybe a ship sees it. Or maybe not. Or maybe something worse happens. I don't know — nobody does. Your choice.\""},
                {"testo": "Can you help me?", "risposta": "\"I stay here. I'm too tired to explore again. But if you find resin and nails for Tiko, the boat comes back to life. That's something. Good luck, friend.\""},
                {"fine": True, "testo": "Thank you, Marco."},
            ],
        },
    ],
    "tiko": [
        {
            "condizione": {"flag": "barca_riparata"},
            "saluto": "Tiko waves from the pier, cheerful. \"The boat sails again! Take it whenever you want — the hidden lagoon to the west is worth a visit. Black pearls, they say.\"",
            "opzioni": [
                {"testo": "Thank you, Tiko", "risposta": "\"It's I who thank you. Without your resin and nails this tub was only good for firewood.\"", "fine": True},
            ],
        },
        {
            "saluto": "Tiko is bent over the boat's keel, tools in his hands. He looks up when you arrive.\n\n\"Hey! Finally a fresh face. You don't happen to have some resin and rusty nails, by chance? I need them to fix this old hull.\"",
            "opzioni": [
                {"testo": "Where can I find them?", "risposta": "\"Resin from the trees of the deep jungle — careful, the path is overgrown without a machete. Rusty nails... the sea spits them onto the southern cliffs after every storm. Both are worth the effort, I promise.\""},
                {"testo": "What's in it for me?", "risposta": "\"Access to the boat. There's a hidden lagoon west of here — only reachable by sea. People say strange things grow there. Up to you.\""},
                {"testo": "Tell me about the village", "risposta": "\"I was born here. My mother was born here. Her mother too. None of us has ever left. Some say we can't. I never tried, to be honest.\""},
                {"fine": True, "testo": "I'll be back."},
            ],
        },
    ],
    "kaia": [
        None, None,  # Stage 0 e 1 già tradotti
        {
            "condizione": {"flag": "faro_acceso"},
            "saluto": "Kaia looks at you with eyes full of a sadness she cannot fully name.\n\n\"You lit the lighthouse. It is both good and bad. It is old news and fresh news. Be careful, stranger — the sea is not the only direction one can travel.\"",
            "opzioni": [
                {"testo": "What do you mean?", "risposta": "\"The lighthouse has more than one door. The one out is visible. The one in... it is not for everyone. Choose when the moment comes. I can say no more.\""},
                {"testo": "Will you come with me if a ship comes?", "risposta": "\"I was born on this island. My mother and her mother too. It is not my story to leave. You, however — you were brought here. Brought back, perhaps. We will see.\""},
                {"fine": True, "testo": "Goodbye, Kaia."},
            ],
        },
    ],
}

DIALOGUES_EN = {
    "kaia": {0: {
        "saluto": "Kaia welcomes you with a warm smile.\n\n'The medallion will guide you, stranger. The ruins hold ancient secrets — and perhaps the key to leaving this island.'",
        "opzioni": [
            {"testo": "Tell me about the ruins",
             "risposta": "'The ruins are what remains of the civilization that inhabited this island thousands of years ago. They were a wise people — they built the lighthouse, the temple, everything. Then the volcano erupted and the sea swallowed part of the island. The Guardian still protects the ruins. It is... the last of them. A spirit, an echo.'"},
            {"testo": "Tell me about the lighthouse",
             "risposta": "'The lighthouse was built by the Ancients to—'"},
        ],
    }, 1: {
        "saluto": "Kaia observes you with calm eyes, as if she already knew who you were.\n\n'You are the traveler expected. The sea has brought you here — it always brings the ones we need. What do you seek?'",
        "opzioni": [
            {"testo": "I want to leave this island",
             "risposta": "'Leaving is difficult. The currents here are cruel. But there is a way — the ancient lighthouse, to the north. If you could light it again, it would call a ship. But to light it, you must find three things: oil, crystal, and a gem.'"},
            {"testo": "Who are you?",
             "risposta": "'I am Kaia. I have lived on this island all my life, and my mother before me. We are descendants of the sunken people — those who lived here before the sea came. But I must ask you a favor, stranger. The sacred artifact of our village was lost in the sea caves. Bring it back to me.'"},
            {"testo": "Tell me about the sea caves",
             "risposta": "'They open to the east of the rocky cove. The entrance is dark — you will need light. Inside, the artifact waits. It is a small jade statuette — you cannot mistake it.'"},
            {"testo": "Goodbye", "fine": True},
        ],
    }},
    "archivista": {0: {
        "saluto": "The Archivist reopens her blue eyes.\n\n'You have returned, traveler. Knowledge never ends. What do you seek today?'",
        "opzioni": [
            {"testo": "Tell me about the Root of the World",
             "risposta": "'The Tree of Light is the source. When the first seed fell into the depths of the stone, from it germinated everything: our civilization, magic, the lighthouse itself. To reach the Root you must cross the Abyss, and to cross the Abyss you must first reactivate the Heart of the Machine.'"},
            {"testo": "How do I reactivate the Heart of the Machine?",
             "risposta": "'The Heart wants to be awakened by the pendulum. Find the brass pendulum in the forge. Combine it with the broken crank of the platform. Once completed, turn the crank and the platform will rise up to the Heart.'"},
            {"testo": "Tell me about the Automaton-King",
             "risposta": "'The last King. When our people understood that the end was near, the King chose to become an automaton to wait for whoever would come. He has waited for four thousand years. He was waiting for you.'"},
            {"testo": "How does the Titans' portal open?",
             "risposta": "'The three recesses want the three symbols of creation: the star (the cosmos), the eye (consciousness), the root (life). Find a star fragment, a Titan's eye, and a living root. Place them in the right niches.'"},
            {"fine": True, "testo": "Thank you, Archivist. I'll return."},
        ],
    }, 1: {
        "saluto": "The figure of light opens blue eyes. She studies you for a long moment — not with the senses, but with something deeper.\n\n'You are alive. And you have descended. Millennia have passed since the last visitor. My name is what you will call me. My name is forgotten, but my function is not: I am the Archive. What do you want to know, traveler?'",
        "opzioni": [
            {"testo": "Where am I?",
             "risposta": "'Under the island. Under the lighthouse. Under the sea. This is the City of the Builders, the last dwelling of the people who built the lighthouse to call the navigators — not as SOS, but as INVITATION. Few answer. You are one.'"},
            {"testo": "How do I proceed?",
             "risposta": "'Explore. Collect. Reactivate the Heart of the Machine in the hall to the north. Then speak with the Automaton-King. He will give you the final key. But remember: whoever reaches the Root never returns the same. I warn you.'"},
            {"testo": "Are you... alive?",
             "risposta": "'I am what remains of who I was. A function. A memory that has become a tool. It doesn't matter. What matters is that I am here, and you are here, and we have something to do together.'"},
            {"fine": True, "testo": "I must go."},
        ],
    }},
    "re_automa": {0: {
        "saluto": "The Automaton-King bows his head slightly. 'You have worn the crown. You are the next. Go, and reign gently.'",
        "opzioni": [{"fine": True, "testo": "I bow. Farewell, King."}],
    }, 1: {
        "saluto": "The Automaton-King raises his gaze toward you. He sees the activated crown in your hands. A vibration of energy runs through his metal body. His voice, when it arrives, is like the sound of bronze struck from far away:\n\n'You have found it. You have completed it. You have understood. Come forward, traveler.'",
        "opzioni": [
            {"testo": "What should I do now?",
             "risposta": "'Descend into the Abyss. Find the Root of the World. There, before the Tree of Light, wear the Crown. You will choose it. It will choose you. And you will know what you must be.'"},
            {"testo": "And you? What will become of you?",
             "risposta": "'I have waited four thousand years to give you this moment. When you wear the crown, I can finally turn off. It is the gift you will give me.'\n\nThe light in his eyes wavers, and for an instant you see something that resembles a smile."},
        ],
    }, 2: {
        "saluto": "The Automaton-King slowly raises his head. His voice arrives from very far away, as if crossing time to reach you:\n\n'You have come. Good. I did not know if you would manage to get this far. Now I see you, and I understand. Yes. You can make it. But first you must prepare.'",
        "opzioni": [
            {"testo": "Prepare for what?",
             "risposta": "'To wear the Titanic Crown. You will find it in the Root of the World, beyond the Abyss. But to activate it you must gather three symbols: a star from my observatory, the eye of a Titan from the avenue, and the living root of the Tree. Place them in the three higher empty points of the crown.'"},
            {"testo": "How do I cross the Abyss?",
             "risposta": "'The bridge is broken. Ropes and rail repair it. Look in the Archivist's library, and in the hall of gears.'"},
            {"testo": "What is beyond the Root?",
             "risposta": "'Not what you think. Not another room, not a new world. A choice. The Crown will ask you who you want to be. Think about it, traveler. Think well.'"},
            {"testo": "Who are you? Who were you?",
             "risposta": "'We were the Builders. We knew much, too much. When our civilization understood that we were the cause of our own ruin, we chose to descend — to seal ourselves under the stone, to let the world heal without us. I am the last. I was waiting for you.'"},
            {"fine": True, "testo": "I must reflect. I will return."},
        ],
    }},
}

# ─── Apply translations ────────────────────────────────────────────
EN = copy.deepcopy(SRC)

EN["intro"] = INTRO_EN
EN["finale"] = FINALE_EN
EN["finale_atto_ii"] = FINALE_ATTO_II_EN
EN["epilogo_segreto"] = EPILOGO_SEGRETO_EN

for rid, patch in ROOMS_EN.items():
    if rid in EN["rooms"]:
        for k, v in patch.items():
            if k == "esaminabili":
                EN["rooms"][rid].setdefault("esaminabili", {})
                EN["rooms"][rid]["esaminabili"].update(v)
            else:
                EN["rooms"][rid][k] = v

for iid, (name, desc) in ITEMS_EN.items():
    if iid in EN["items"]:
        EN["items"][iid]["nome_completo"] = name
        EN["items"][iid]["descrizione"] = desc

for cid, patch in CHARACTERS_EN.items():
    if cid in EN["characters"]:
        EN["characters"][cid].update(patch)

for cid, (name, lore) in COLLECTIBLES_EN.items():
    if cid in EN.get("collectibles", {}):
        EN["collectibles"][cid] = {"nome": name, "lore": lore}

for key, msg in ACTIONS_EN.items():
    if key in EN["room_actions"]:
        EN["room_actions"][key]["messaggio"] = msg

for i, msg in enumerate(RECIPES_MSG_EN):
    if i < len(EN["recipes"]):
        EN["recipes"][i]["messaggio"] = msg

# Dialoghi: primo giro sovrascrive stage-by-index (campi già tradotti)
for npc, stages_by_idx in DIALOGUES_EN.items():
    if npc in EN["dialogues"]:
        for idx, data in stages_by_idx.items():
            if idx < len(EN["dialogues"][npc]):
                stage = EN["dialogues"][npc][idx]
                if "saluto" in data: stage["saluto"] = data["saluto"]
                if "opzioni" in data:
                    for oi, opt in enumerate(data["opzioni"]):
                        if oi < len(stage.get("opzioni", [])):
                            for ok, ov in opt.items():
                                stage["opzioni"][oi][ok] = ov

# Dialoghi: secondo giro con lista piena (Marco/Tiko + Kaia extra stage)
for npc, stages in DIALOGUES_FULL_EN.items():
    if npc not in EN["dialogues"]: continue
    for si, new_stage in enumerate(stages):
        if new_stage is None: continue
        if si >= len(EN["dialogues"][npc]): continue
        cur = EN["dialogues"][npc][si]
        if "saluto" in new_stage: cur["saluto"] = new_stage["saluto"]
        if "opzioni" in new_stage:
            new_opts = new_stage["opzioni"]
            for oi in range(min(len(new_opts), len(cur.get("opzioni", [])))):
                for k, v in new_opts[oi].items():
                    cur["opzioni"][oi][k] = v

# Quests
for qid, q in QUESTS_EN.items():
    if qid in EN.get("quests", {}):
        EN["quests"][qid]["nome"] = q["nome"]
        EN["quests"][qid]["descrizione"] = q["descrizione"]
        for oi, ob in enumerate(q.get("obiettivi", [])):
            if oi < len(EN["quests"][qid].get("obiettivi", [])):
                EN["quests"][qid]["obiettivi"][oi]["desc"] = ob["desc"]

# Puzzles testuali
for pid, p in PUZZLES_EN.items():
    if pid in EN.get("puzzles", {}):
        for k, v in p.items():
            EN["puzzles"][pid][k] = v

# Puzzle interattivi
for pid, p in PUZZLES_INTERACTIVE_EN.items():
    if pid in EN.get("puzzles_interactive", {}):
        for k, v in p.items():
            EN["puzzles_interactive"][pid][k] = v

# Deliveries
for k, msg in DELIVERIES_EN.items():
    if k in EN.get("deliveries", {}):
        EN["deliveries"][k]["messaggio"] = msg

# Esaminabili mancanti
for rid, exs in ROOM_EXAMINABLES_EN.items():
    if rid in EN["rooms"]:
        EN["rooms"][rid].setdefault("esaminabili", {})
        for k, v in exs.items():
            EN["rooms"][rid]["esaminabili"][k] = v

OUT.write_text(json.dumps(EN, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  rooms translated: {len(ROOMS_EN)}/{len(EN['rooms'])}")
print(f"  items translated: {len(ITEMS_EN)}/{len(EN['items'])}")
print(f"  chars translated: {len(CHARACTERS_EN)}/{len(EN['characters'])}")
print(f"  collectibles translated: {len(COLLECTIBLES_EN)}/{len(EN.get('collectibles', {}))}")
print(f"  actions translated: {len(ACTIONS_EN)}/{len(EN['room_actions'])}")
