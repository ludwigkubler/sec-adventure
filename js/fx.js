// FX ambientali. Popola #ambient-fx con particles/overlay CSS-animati per stanza.
// Tutte le animazioni sono in CSS (keyframes): zero requestAnimationFrame, GPU-friendly.
// Max ~30 nodi concorrenti. Rispetta prefers-reduced-motion (nessun elemento creato).
const FX = (() => {
  const $fx = () => document.getElementById("ambient-fx");
  let currentRoom = null;
  const reduced = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ─── Mappa roomId → preset FX ───
  // (tenuta locale perché world.json non contiene campo `bioma`)
  const ROOM_PRESET = {
    // Atto I — costa & foresta
    spiaggia: "beach", caletta: "beach", molo: "beach",
    laguna: "beach", scogliere: "beach", scogliere_sud: "beach",
    cimitero_marino: "beach",
    foresta: "forest", radura: "forest",
    giungla: "forest", giungla_profonda: "forest", bivio_giungla: "forest",
    villaggio: "village", capanna_luna: "village",
    sentiero_montagna: "mountain", cima_vulcano: "mountain",
    cripta: "crypt", grotte: "crypt", rovine: "crypt",
    tempio_sommerso: "crypt", sala_guardiano: "crypt",
    corridoio_perduto: "crypt", cunicolo_nascosto: "crypt",
    // Atto II — macchina
    pozzo_faro: "atto2", cripta_meccanica: "atto2",
    corridoio_vapore: "atto2", archivio: "atto2",
    osservatorio: "atto2", cuore_macchina: "atto2",
    agora_perduta: "atto2", via_titani: "atto2", abisso: "atto2",
    faro: "atto2",
    // Varianti con scintille
    sala_ingranaggi: "atto2_gears",
    forgia_antica: "atto2_gears",
    // Finale
    radice_mondo: "roots",
  };

  // ─── Builder per preset ───
  // Ritornano array di HTMLElement da appendere.
  const BUILDERS = {
    // 1) BEACH: onde (3 strisce orizzontali) + gabbiani (5 V lontani)
    beach() {
      const out = [];
      for (let i = 0; i < 3; i++) {
        const w = el("div", "fx-wave fx-wave-" + i);
        out.push(w);
      }
      for (let i = 0; i < 5; i++) {
        const g = el("div", "fx-gull");
        g.style.top = (6 + Math.random() * 22) + "%";
        g.style.animationDelay = (-Math.random() * 40) + "s";
        g.style.animationDuration = (28 + Math.random() * 22) + "s";
        g.textContent = "︵";
        out.push(g);
      }
      // Glint d'acqua
      out.push(el("div", "fx-sunglint"));
      return out; // 3 + 5 + 1 = 9
    },

    // 2) FOREST: foglie che cadono + raggi di luce volumetrica
    forest() {
      const out = [];
      // 3 shaft di luce
      for (let i = 0; i < 3; i++) {
        const s = el("div", "fx-lightshaft fx-lightshaft-" + i);
        out.push(s);
      }
      // 14 foglie
      const glyphs = ["❧", "✿", "❦", "·", "•"];
      for (let i = 0; i < 14; i++) {
        const lf = el("div", "fx-leaf");
        lf.style.left = (Math.random() * 100) + "%";
        lf.style.animationDelay = (-Math.random() * 18) + "s";
        lf.style.animationDuration = (9 + Math.random() * 8) + "s";
        lf.style.color = `hsl(${30 + Math.random() * 40},55%,${45 + Math.random() * 20}%)`;
        lf.textContent = glyphs[i % glyphs.length];
        out.push(lf);
      }
      return out; // 3 + 14 = 17
    },

    // 3) VILLAGE: fumo focolare + luccioline
    village() {
      const out = [];
      for (let i = 0; i < 4; i++) {
        const p = el("div", "fx-smoke");
        p.style.left = (42 + Math.random() * 16) + "%";
        p.style.animationDelay = (-Math.random() * 8) + "s";
        out.push(p);
      }
      for (let i = 0; i < 10; i++) {
        const f = el("div", "fx-firefly");
        f.style.left = (Math.random() * 100) + "%";
        f.style.top = (40 + Math.random() * 50) + "%";
        f.style.animationDelay = (-Math.random() * 6) + "s";
        f.style.animationDuration = (4 + Math.random() * 5) + "s";
        out.push(f);
      }
      return out; // 14
    },

    // 4) MOUNTAIN: polvere di vento orizzontale + nebbia bassa
    mountain() {
      const out = [];
      for (let i = 0; i < 12; i++) {
        const d = el("div", "fx-dust");
        d.style.top = (Math.random() * 95) + "%";
        d.style.animationDelay = (-Math.random() * 10) + "s";
        d.style.animationDuration = (4 + Math.random() * 4) + "s";
        out.push(d);
      }
      out.push(el("div", "fx-fogband fx-fogband-1"));
      out.push(el("div", "fx-fogband fx-fogband-2"));
      return out; // 14
    },

    // 5) CRYPT: gocce verticali occasionali + nebbia fluttuante
    crypt() {
      const out = [];
      for (let i = 0; i < 6; i++) {
        const d = el("div", "fx-drop");
        d.style.left = (8 + Math.random() * 84) + "%";
        d.style.animationDelay = (-Math.random() * 7) + "s";
        d.style.animationDuration = (5 + Math.random() * 6) + "s";
        out.push(d);
      }
      out.push(el("div", "fx-mist fx-mist-1"));
      out.push(el("div", "fx-mist-2"));
      return out; // 8
    },

    // 6) ATTO II: polvere luminosa + glow pulsante dal basso
    atto2() {
      const out = [];
      for (let i = 0; i < 14; i++) {
        const m = el("div", "fx-mote");
        m.style.left = (Math.random() * 100) + "%";
        m.style.animationDelay = (-Math.random() * 14) + "s";
        m.style.animationDuration = (10 + Math.random() * 8) + "s";
        out.push(m);
      }
      out.push(el("div", "fx-underglow"));
      return out; // 15
    },

    // 6b) ATTO II + scintille (forgia/sala_ingranaggi)
    atto2_gears() {
      const out = BUILDERS.atto2();
      for (let i = 0; i < 8; i++) {
        const s = el("div", "fx-spark");
        s.style.left = (30 + Math.random() * 40) + "%";
        s.style.top = (40 + Math.random() * 40) + "%";
        s.style.animationDelay = (-Math.random() * 6) + "s";
        s.style.animationDuration = (1.5 + Math.random() * 2) + "s";
        out.push(s);
      }
      return out; // 23
    },

    // 7) ROOTS: spore luminose + pulsazione verde-azzurra
    roots() {
      const out = [];
      out.push(el("div", "fx-rootpulse"));
      for (let i = 0; i < 16; i++) {
        const s = el("div", "fx-spore");
        s.style.left = (Math.random() * 100) + "%";
        s.style.animationDelay = (-Math.random() * 16) + "s";
        s.style.animationDuration = (12 + Math.random() * 10) + "s";
        out.push(s);
      }
      return out; // 17
    },
  };

  function el(tag, cls) {
    const d = document.createElement(tag);
    d.className = cls;
    return d;
  }

  function clear() {
    const host = $fx();
    if (host) host.innerHTML = "";
  }

  function setRoom(roomId) {
    if (roomId === currentRoom) return;
    currentRoom = roomId;
    clear();
    if (reduced()) return;
    const host = $fx();
    if (!host) return;
    const preset = ROOM_PRESET[roomId];
    if (!preset) return;
    const build = BUILDERS[preset];
    if (!build) return;
    const nodes = build();
    // Safety cap: max 30 concurrent
    const frag = document.createDocumentFragment();
    nodes.slice(0, 30).forEach(n => frag.appendChild(n));
    host.appendChild(frag);
    host.dataset.preset = preset;
  }

  return { setRoom, clear, _presets: ROOM_PRESET };
})();
