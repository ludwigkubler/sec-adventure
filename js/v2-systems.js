// v2.0 Systems: Thought Cabinet, Skills, Karma, Crafting Tree, Companion,
// Fatica/Fame, Mini-games, Photo Mode, Memoryprint
// Tutto in un singolo modulo per ridurre overhead e dipendenze

const V2 = (() => {
  // ─── Thought Cabinet ───────────────────────────────────────────
  // Idee internalizzabili a scadenza che sbloccano dialoghi/scelte
  const THOUGHTS = {
    sospetto_guardiano: {
      nome: "Sospetto sul Guardiano",
      desc: "Qualcosa nel suo modo di rispondere agli enigmi non ti convince. Forse mente.",
      duration: 4*60, // minuti gioco
      reward_flag: "verita_guardiano",
      icon: "👁",
    },
    nostalgia_casa: {
      nome: "Nostalgia di casa",
      desc: "Ricordi una stanza, una voce, un odore. Ma non ricordi di chi.",
      duration: 6*60,
      reward_flag: "memoria_attivata",
      icon: "🏠",
    },
    eco_costruttore: {
      nome: "Eco del Costruttore",
      desc: "Ogni tanto sai cose senza averle imparate. Qualcosa in te ricorda.",
      duration: 8*60,
      reward_flag: "consapevolezza_costruttore",
      icon: "✦",
    },
    pieta_isola: {
      nome: "Pietà per l'isola",
      desc: "Più cammini, più senti che l'isola soffre. Forse ha bisogno di te, non viceversa.",
      duration: 5*60,
      reward_flag: "empatia_terra",
      icon: "🌿",
    },
    diffidenza_villaggio: {
      nome: "Diffidenza del villaggio",
      desc: "Sorridono ma ti studiano. Cosa nascondono?",
      duration: 3*60,
      reward_flag: "verita_villaggio",
      icon: "🔍",
    },
  };

  function startThought(id) {
    const t = THOUGHTS[id];
    if (!t) return false;
    const st = Engine.getState();
    if (!st.thoughts) st.thoughts = {};
    if (st.thoughts[id]) return false;
    const wc = WorldClock.getState();
    const startMin = wc.day * 1440 + wc.minutes;
    st.thoughts[id] = {
      started: startMin,
      finished: false,
    };
    Render.logSystem(`💭 Stai meditando: "${t.nome}"`);
    return true;
  }

  function tickThoughts() {
    const st = Engine.getState();
    if (!st.thoughts) return;
    const wc = WorldClock.getState();
    const nowMin = wc.day * 1440 + wc.minutes;
    for (const [id, ts] of Object.entries(st.thoughts)) {
      if (ts.finished) continue;
      const t = THOUGHTS[id];
      if (!t) continue;
      if (nowMin - ts.started >= t.duration) {
        ts.finished = true;
        if (t.reward_flag) Engine.setFlag(t.reward_flag, true);
        UI.showToast({title: `💭 Hai compreso: ${t.nome}`,
                      body: t.desc, kind: "achievement"});
      }
    }
  }

  // ─── Skill check ───────────────────────────────────────────────
  const SKILLS = {
    intuito:    {nome: "Intuito",    desc: "Vedere oltre l'apparenza"},
    meccanica:  {nome: "Meccanica",  desc: "Capire come funzionano le cose"},
    empatia:    {nome: "Empatia",    desc: "Sentire ciò che altri sentono"},
    resistenza: {nome: "Resistenza", desc: "Sopportare fatica e dolore"},
    occhio:     {nome: "Occhio Vivo",desc: "Notare i dettagli minuti"},
    voce:       {nome: "Voce",       desc: "Parlare bene, persuadere"},
  };

  function rollCheck(skill, difficulty) {
    const st = Engine.getState();
    if (!st.skills) st.skills = {};
    const level = st.skills[skill] || 1;
    const d6 = Math.floor(Math.random()*6) + 1;
    const d6b = Math.floor(Math.random()*6) + 1;
    const total = d6 + d6b + level;
    return {
      success: total >= difficulty,
      total, level, dice: [d6, d6b], skill, difficulty,
    };
  }
  function increaseSkill(skill, amount=1) {
    const st = Engine.getState();
    if (!st.skills) st.skills = {};
    st.skills[skill] = Math.min(8, (st.skills[skill] || 1) + amount);
    Render.logSystem(`🎯 ${SKILLS[skill]?.nome || skill} +${amount} (ora ${st.skills[skill]})`);
  }

  // ─── Karma fazioni ─────────────────────────────────────────────
  const FACTIONS = {
    villaggio:    {nome: "Villaggio",    desc: "Kaia, Marco, Tiko"},
    costruttori:  {nome: "Costruttori",  desc: "Archivista, Re-Automa"},
    mare:         {nome: "Il Mare",      desc: "Luna, abissi, profondità"},
  };
  function changeKarma(faction, delta) {
    const st = Engine.getState();
    if (!st.karma) st.karma = {villaggio:0, costruttori:0, mare:0};
    st.karma[faction] = (st.karma[faction] || 0) + delta;
    const arrow = delta > 0 ? "↑" : "↓";
    Render.logSystem(`${arrow} Reputazione con ${FACTIONS[faction].nome}: ${st.karma[faction] >= 0 ? "+" : ""}${st.karma[faction]}`);
  }
  function getKarma(faction) {
    const st = Engine.getState();
    return (st.karma && st.karma[faction]) || 0;
  }

  // ─── Crafting tree (visibile) ───────────────────────────────────
  // Estende le ricette esistenti con metadata UI
  function getCraftingTree() {
    const w = Engine.world();
    const st = Engine.getState();
    const recipes = w.recipes || [];
    return recipes.map(r => {
      const have = r.ingredienti.every(i => st.inv.includes(i));
      const known = r.ingredienti.every(i => st.taken[i] || st.inv.includes(i));
      return {
        ingredients: r.ingredienti,
        result: r.risultato,
        message: r.messaggio,
        unlocked: known,
        craftable: have,
      };
    });
  }

  // ─── Companion (Tiko ti segue dopo barca riparata) ──────────────
  function companionFollows() {
    const st = Engine.getState();
    return st.flags && st.flags.barca_riparata && !st.flags.tiko_separato;
  }
  function companionComment() {
    if (!companionFollows()) return null;
    const room = Engine.getState().room;
    const COMMENTS = {
      spiaggia: "Tiko: «Mi ricordo di quando da bambino raccoglievo conchiglie qui.»",
      caletta:  "Tiko: «Le pozze di marea. Mia madre mi ci portava a vedere i polpi.»",
      villaggio:"Tiko: «Casa. Ma ora non sembra più solo casa.»",
      molo:     "Tiko: «La barca naviga. Grazie a te.»",
      faro:     "Tiko: «Mai entrato qui. La gente del villaggio diceva che era proibito.»",
      pozzo_faro:"Tiko: «...non so se ho il coraggio di scendere ancora.»",
      grotte:   "Tiko: «Sento il sale sulle labbra. È casa — e non lo è.»",
      laguna:   "Tiko: «La perla nera. Si racconta da generazioni.»",
    };
    return COMMENTS[room] || null;
  }

  // ─── Fatica/Fame ────────────────────────────────────────────────
  function tickFatigue() {
    const st = Engine.getState();
    if (typeof st.fatigue !== "number") st.fatigue = 0;
    if (typeof st.hunger !== "number") st.hunger = 0;
    // +1 fatica e +1 fame ogni 5 min reali (ogni 100 min gioco)
    st.fatigue = Math.min(100, st.fatigue + 0.3);
    st.hunger = Math.min(100, st.hunger + 0.4);
    updateStatBars();
  }
  function rest() {
    const st = Engine.getState();
    st.fatigue = 0;
    WorldClock.advanceMinutes(360); // dormi 6 ore
    Render.logSystem("Hai dormito. La fatica è svanita.");
    updateStatBars();
  }
  function eat(itemId) {
    const st = Engine.getState();
    const NUTRI = {
      bacche: 25, pianta_rara: 15, erbe_secche: 10,
      antidoto: 0,
    };
    const n = NUTRI[itemId];
    if (typeof n !== "number") return false;
    st.hunger = Math.max(0, st.hunger - n);
    Engine.removeItem(itemId);
    Render.logSystem(`Hai mangiato. Fame -${n}.`);
    updateStatBars();
    return true;
  }
  function updateStatBars() {
    const st = Engine.getState();
    const res = document.getElementById("stat-resistenza");
    const hun = document.getElementById("stat-hunger");
    const fat = document.getElementById("stat-fatigue");
    if (res) res.style.width = Math.max(0, 100 - (st.hunger||0)*0.5 - (st.fatigue||0)*0.5) + "%";
    if (hun) hun.style.width = Math.max(0, 100 - (st.hunger||0)) + "%";
    if (fat) fat.style.width = Math.max(0, 100 - (st.fatigue||0)) + "%";
  }

  // ─── HUD clock + meteo ──────────────────────────────────────────
  function updateClockHud(ev) {
    const cl = document.getElementById("hud-clock");
    const we = document.getElementById("hud-weather");
    if (cl) cl.textContent = "🕐 " + WorldClock.getTimeString();
    if (we) {
      const ICONS = {clear:"☀", cloudy:"☁", rain:"🌧", storm:"⛈", fog:"🌫"};
      we.textContent = ICONS[ev?.weather || WorldClock.getState().weather] || "☀";
    }
  }

  // ─── Photo Mode ─────────────────────────────────────────────────
  function showPhotoMode() {
    UI.show(`
      <h3>📷 Modalità Fotografia</h3>
      <p style="text-align:center;color:#a89060">L'inquadratura attuale verrà fissata come ricordo.</p>
      <div style="text-align:center;margin:20px 0">
        <div style="display:inline-block;border:2px solid var(--accent-hot);padding:8px;background:#000;box-shadow:0 0 30px rgba(192,138,60,.3)">
          <div style="width:240px;height:150px;background:radial-gradient(circle at center,var(--accent),var(--bg));position:relative;display:flex;align-items:center;justify-content:center;color:var(--accent-hot);font-style:italic">${esc(Engine.room()?.nome || "Scena")}</div>
        </div>
      </div>
      <p style="text-align:center;font-size:13px;color:#7a6850">${WorldClock.getTimeString()} · ${WorldClock.getState().weather} · giorno ${WorldClock.getState().day}</p>
      <div class="modal-actions">
        <button id="ph-save">Salva nel diario</button>
        <button id="ph-close" style="opacity:.6">Annulla</button>
      </div>
    `);
    document.getElementById("ph-save").onclick = () => {
      const st = Engine.getState();
      if (!st.photos) st.photos = [];
      st.photos.push({
        room: st.room,
        time: WorldClock.getTimeString(),
        weather: WorldClock.getState().weather,
        day: WorldClock.getState().day,
      });
      UI.close();
      Render.logSystem(`📷 Foto salvata (${st.photos.length} totali)`);
    };
    document.getElementById("ph-close").onclick = UI.close;
  }
  function esc(s) { return String(s||"").replace(/[<>&"]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c])); }

  // ─── Mini-games minimi ──────────────────────────────────────────
  // Pesca: timing button — premi quando l'indicatore è nella zona verde
  function showFishing() {
    let cursor = 0, dir = 1, target = 50, win = false, ended = false;
    UI.show(`
      <h3>🎣 Pesca</h3>
      <p>Premi <b>SPAZIO</b> o clicca <b>STRAPPA</b> quando il pesce è nella zona verde.</p>
      <div id="fish-bar" style="position:relative;height:24px;background:#1a0e05;border:1px solid var(--border);border-radius:4px;margin:20px 0">
        <div id="fish-zone" style="position:absolute;left:40%;top:0;width:20%;height:100%;background:rgba(120,200,120,.4);border-left:2px solid #80c080;border-right:2px solid #80c080"></div>
        <div id="fish-cursor" style="position:absolute;top:0;left:0;width:6px;height:100%;background:var(--accent-hot);box-shadow:0 0 10px var(--accent-hot);transition:left .05s linear"></div>
      </div>
      <div class="modal-actions">
        <button id="fish-strap">STRAPPA</button>
        <button id="fish-close" style="opacity:.6">Lascia stare</button>
      </div>
    `);
    const cur = document.getElementById("fish-cursor");
    const interval = setInterval(() => {
      cursor += dir * 2;
      if (cursor >= 100) { cursor = 100; dir = -1; }
      if (cursor <= 0) { cursor = 0; dir = 1; }
      if (cur) cur.style.left = cursor + "%";
    }, 30);
    function strap() {
      if (ended) return;
      ended = true;
      clearInterval(interval);
      win = cursor >= 40 && cursor <= 60;
      if (win) {
        Audio.sfx("puzzle_ok");
        Engine.addItem("pesce_grosso");
        UI.showText("🎣", "Hai pescato un pesce grosso! Tiko sarà felice.");
      } else {
        Audio.sfx("puzzle_fail");
        UI.showText("🎣", "Il pesce è scappato. Riprova quando vuoi.");
      }
    }
    document.getElementById("fish-strap").onclick = strap;
    document.getElementById("fish-close").onclick = () => { clearInterval(interval); UI.close(); };
    const keyHandler = (e) => { if (e.key === " ") { e.preventDefault(); strap(); } };
    document.addEventListener("keydown", keyHandler);
    setTimeout(() => document.removeEventListener("keydown", keyHandler), 30000);
  }

  // ─── Init ───────────────────────────────────────────────────────
  function init() {
    if (window.WorldClock) {
      WorldClock.on(updateClockHud);
      const wc = WorldClock.getState();
      updateClockHud({weather: wc.weather});
    }
    // Tick fatica/fame ogni 30s reali
    setInterval(() => { tickFatigue(); tickThoughts(); }, 30000);
    setTimeout(updateStatBars, 500);
  }

  return {
    init,
    THOUGHTS, SKILLS, FACTIONS,
    startThought, tickThoughts,
    rollCheck, increaseSkill,
    changeKarma, getKarma,
    getCraftingTree,
    companionFollows, companionComment,
    rest, eat,
    updateStatBars, updateClockHud,
    showPhotoMode, showFishing,
  };
})();

if (typeof window !== "undefined") window.V2 = V2;
