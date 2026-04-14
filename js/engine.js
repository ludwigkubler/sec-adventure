// Stato di gioco + regole. Zero DOM qui.
const Engine = (() => {
  let W = null;               // world data
  let state = null;           // {room, inv, flags, dialogStage, taken, roomExtras}
  const listeners = [];

  const emit = (ev) => listeners.forEach(fn => fn(ev));
  const on = (fn) => listeners.push(fn);

  function newState() {
    return {
      room: (W && W.start_room) || "spiaggia",
      inv: [],
      flags: {},
      dialogStage: {},
      taken: {},
      examined: {},
      delivered: {},
      puzzleDone: {},
      selected: null,
      visited: {},
      codex: {},
      achievements: {},
      startedAt: null,
      elapsed: 0,
    };
  }
  let timerStart = null;
  function startTimer() { timerStart = Date.now(); if (!state.startedAt) state.startedAt = timerStart; }
  function getElapsedSeconds() {
    if (!timerStart) return (state.elapsed || 0);
    return Math.floor((state.elapsed || 0) + (Date.now() - timerStart) / 1000);
  }
  function freezeTimer() { if (timerStart) { state.elapsed = (state.elapsed||0) + Math.floor((Date.now()-timerStart)/1000); timerStart = null; } }

  function init(world) {
    W = world;
    state = newState();
    state.visited[state.room] = true;
    emit({type: "init"});
  }

  function world() { return W; }
  function getState() { return state; }
  function setState(s) { state = s; emit({type: "loaded"}); }

  // ---- Flag / condition evaluation ----
  // condizione può essere: "oggetto:xxx", "flag:xxx", "!flag:xxx"
  function checkCondition(cond) {
    if (!cond) return true;
    if (cond.startsWith("!")) return !checkCondition(cond.slice(1));
    const [type, val] = cond.split(":");
    if (type === "oggetto") return state.inv.includes(val);
    if (type === "flag") return !!state.flags[val];
    return false;
  }

  function checkObjCondition(obj) {
    // obj = {flag: "...", oggetto: "..."} (tutti devono valere)
    if (!obj) return true;
    for (const [k, v] of Object.entries(obj)) {
      if (k === "flag" && !state.flags[v]) return false;
      if (k === "oggetto" && !state.inv.includes(v)) return false;
      if (k === "no_flag" && state.flags[v]) return false;
    }
    return true;
  }

  // ---- Room queries ----
  function room(id) { return W.rooms[id || state.room]; }
  function item(id) { return W.items[id]; }
  function npc(id) { return W.characters[id]; }

  function roomItems(rid) {
    const r = W.rooms[rid];
    if (!r) return [];
    return (r.oggetti || []).filter(oid => {
      if (state.taken[oid]) return false;
      const it = W.items[oid];
      if (!it) return false;
      if (it.nascosto && !state.flags["vede_" + oid]) return false;
      return true;
    });
  }
  function roomExtras(rid) {
    const r = W.rooms[rid];
    if (!r) return [];
    const extras = state.roomExtras?.[rid] || [];
    return extras.filter(oid => !state.taken[oid]);
  }
  function roomNpcs(rid) {
    const r = W.rooms[rid];
    if (!r) return [];
    // NPC possono essere elencati nella stanza o avere "stanza" nel loro record
    const ids = new Set(r.npcs || []);
    for (const [nid, n] of Object.entries(W.characters)) {
      if (n.stanza === rid) ids.add(nid);
    }
    return [...ids];
  }
  function roomExits(rid) {
    const r = W.rooms[rid];
    if (!r) return [];
    const exits = [];
    for (const [dir, dest] of Object.entries(r.uscite || {})) {
      exits.push({dir, dest, blocked: null});
    }
    for (const [dir, info] of Object.entries(r.uscite_bloccate || {})) {
      const destKey = rid + "::" + dir;
      const dest = (W.blocked_destinations || {})[destKey] || info.destinazione || null;
      if (checkCondition(info.condizione)) {
        if (dest) exits.push({dir, dest, blocked: null});
      } else {
        exits.push({dir, dest: null, blocked: info.messaggio, wouldBe: dest, cond: info.condizione});
      }
    }
    return exits;
  }

  // ---- Actions ----
  function moveTo(dest) {
    if (!W.rooms[dest]) return {ok: false, msg: "Non puoi andare lì."};
    const firstTime = !state.visited[dest];
    state.room = dest;
    state.visited[dest] = true;
    emit({type: "moved", room: dest, firstTime});
    // Achievements geografici
    if (firstTime) {
      if (dest === "pozzo_faro") unlockAchievement("primo_pozzo", "Soglia varcata", "Hai disceso il pozzo del faro per la prima volta.");
      if (dest === "agora_perduta") unlockAchievement("agora", "Sotto la pietra", "Hai raggiunto l'Agorà perduta dei Costruttori.");
      if (dest === "radice_mondo") unlockAchievement("radice", "Al centro", "Hai raggiunto la Radice del Mondo.");
      // Atto I completo (visitate ≥18 stanze atto I)
      const atto1 = (W.map_positions||{});
      const atto1Ids = Object.entries(atto1).filter(([_,v])=>v.atto===1).map(([k])=>k);
      if (atto1Ids.length && atto1Ids.every(r => state.visited[r])) {
        unlockAchievement("esploratore_isola", "Esploratore", "Hai esplorato ogni angolo dell'isola.");
      }
    }
    return {ok: true, msg: firstTime ? `Arrivi a ${W.rooms[dest].nome}.` : `Torni a ${W.rooms[dest].nome}.`};
  }
  function wasVisited(rid){ return !!state.visited[rid]; }
  function tryExit(dir) {
    const r = W.rooms[state.room];
    const dest = (r.uscite || {})[dir];
    if (dest) return moveTo(dest);
    const b = (r.uscite_bloccate || {})[dir];
    if (b) {
      if (checkCondition(b.condizione)) {
        const d = (W.blocked_destinations || {})[state.room + "::" + dir] || b.destinazione;
        if (d) return moveTo(d);
      }
      return {ok: false, msg: b.messaggio || "La via è bloccata."};
    }
    return {ok: false, msg: "Non puoi andare in quella direzione."};
  }

  function takeItem(id) {
    const it = W.items[id];
    if (!it) return {ok:false, msg: "Non c'è nulla da prendere."};
    if (!it.portatile) return {ok:false, msg: `${it.nome_completo} non puoi portartelo via.`};
    // Guard double-pickup (race condition su click rapidi)
    if (state.taken[id] || state.inv.includes(id)) {
      return {ok:false, msg: `Hai già raccolto ${it.nome_completo}.`};
    }
    state.inv.push(id);
    state.taken[id] = true;
    // Codex: se è un collezionabile, traccialo
    if ((W.collectibles || {})[id]) {
      const wasNew = !state.codex[id];
      state.codex[id] = true;
      if (wasNew) {
        const total = Object.keys(W.collectibles).length;
        const found = Object.keys(state.codex).length;
        emit({type: "codex_found", id, found, total, lore: W.collectibles[id]});
        if (found === total && !state.flags.codex_completo) {
          state.flags.codex_completo = true;
          emit({type: "achievement", id: "codex_completo",
                title: "Codex Completo",
                desc: `Hai trovato tutti i ${total} frammenti di lore. Un epilogo segreto ti attende.`});
        }
      }
    }
    emit({type: "take", id});
    return {ok:true, msg: `Hai raccolto: ${it.nome_completo}.`};
  }

  function addItem(id) {
    if (!state.inv.includes(id)) state.inv.push(id);
    emit({type: "take", id});
  }
  function removeItem(id) {
    state.inv = state.inv.filter(x => x !== id);
    emit({type: "inv"});
  }
  function setFlag(f, v=true) {
    state.flags[f] = v;
    if (!state.flags.faro_acceso &&
        state.flags.faro_olio && state.flags.faro_cristallo && state.flags.faro_gemma) {
      state.flags.faro_acceso = true;
      checkSpeedrun("faro");
      emit({type: "faro_acceso"});
    }
    if (f === "corona_indossata" && v) {
      checkSpeedrun("corona");
      emit({type: "ending_atto_ii"});
    }
    emit({type: "flag", f});
  }
  function checkSpeedrun(which) {
    const elapsed = getElapsedSeconds();
    if (which === "faro") {
      if (elapsed <= 1800) unlockAchievement("speedrun_faro_30",
        "Speedrunner ⚡", "Faro acceso in meno di 30 minuti!");
    }
    if (which === "corona") {
      if (elapsed <= 3600) unlockAchievement("speedrun_corona_60",
        "Speedrunner Leggendario ⚡⚡", "Corona indossata in meno di 60 minuti!");
      const codexDone = state.flags.codex_completo;
      if (codexDone && elapsed <= 5400) unlockAchievement("perfetto",
        "Perfetto ✦", "Corona + Codex completo in meno di 90 minuti!");
    }
  }

  function examine(key) {
    const r = W.rooms[state.room];
    const exs = (r.esaminabili || {});
    if (exs[key]) {
      state.examined[state.room + "::" + key] = true;
      return {ok:true, msg: exs[key]};
    }
    return {ok:false, msg: `Non vedi nulla di particolare.`};
  }

  function inspectItem(id) {
    const it = W.items[id];
    if (!it) return {ok:false, msg: ""};
    return {ok:true, msg: it.descrizione || it.nome_completo};
  }

  // ---- Use item on target ----
  // target può essere: {kind:"item", id:"xxx"} (altro oggetto in inventario) per combinare
  //                    {kind:"room_item", id:"xxx"} oggetto nella stanza
  //                    {kind:"npc", id:"xxx"}
  //                    {kind:"exit", dir:"nord"}
  //                    {kind:"examine", key:"xxx"}
  //                    {kind:"room", id:roomId}  (usa oggetto "sulla stanza")
  function useOn(selected, target) {
    // NPC: consegna
    if (target.kind === "npc") {
      const key = selected + "::" + target.id;
      const del = W.deliveries[key];
      if (del) {
        if (state.delivered[key]) return {ok:false, msg:"Hai già consegnato questo."};
        state.delivered[key] = true;
        for (const rm of (del.rimuovi || [])) removeItem(rm);
        for (const ot of (del.ottieni || [])) addItem(ot);
        if (del.flag) setFlag(del.flag, true);
        return {ok:true, msg: del.messaggio};
      }
      return {ok:false, msg: `${W.characters[target.id].nome} non sembra interessato.`};
    }
    // Exit bloccato: sblocco?
    if (target.kind === "exit") {
      const r = W.rooms[state.room];
      const b = (r.uscite_bloccate || {})[target.dir];
      if (b && b.condizione === "oggetto:" + selected) {
        const d = (W.blocked_destinations || {})[state.room + "::" + target.dir] || b.destinazione;
        if (d) return moveTo(d);
      }
      return {ok:false, msg: "Non funziona così."};
    }
    // Combine (usare su un oggetto inventario)
    if (target.kind === "item") {
      const recipe = W.recipes.find(r =>
        (r.ingredienti.includes(selected) && r.ingredienti.includes(target.id) &&
         r.ingredienti[0] !== r.ingredienti[1]) ||
        (r.ingredienti[0] === selected && r.ingredienti[1] === target.id)
      );
      if (recipe) {
        for (const ing of recipe.ingredienti) removeItem(ing);
        addItem(recipe.risultato);
        return {ok:true, msg: recipe.messaggio, result: recipe.risultato, kind: "combine"};
      }
      return {ok:false, msg: "Questi due oggetti non si combinano."};
    }
    // Room action: usare l'oggetto sullo scenario (chiave=stanza corrente)
    if (target.kind === "room" || target.kind === "examine" || target.kind === "room_item") {
      const actionKey = selected + "::" + state.room;
      const act = W.room_actions[actionKey];
      if (act) {
        if (act.flag) setFlag(act.flag, true);
        if (act.consuma) removeItem(selected);
        if (act.ottieni) for (const ot of act.ottieni) addItem(ot);
        return {ok:true, msg: act.messaggio, audio: act.audio};
      }
    }
    return {ok:false, msg: "Non succede nulla."};
  }

  // ---- Dialog advance ----
  function dialogFor(npcId) {
    const stages = W.dialogues[npcId];
    if (!stages) return null;
    // prende il primo stage la cui condizione vale
    for (const s of stages) {
      if (checkObjCondition(s.condizione)) return s;
    }
    return stages[0];
  }

  // ---- Puzzle ----
  function tryPuzzle(pid, answer) {
    const p = W.puzzles[pid];
    if (!p) return null;
    // Normalizza: lowercase, trim, togli articoli/punteggiatura finale
    const norm = s => s.toLowerCase().trim()
      .replace(/[.!?;,]+$/, "")
      .replace(/^(un|una|uno|il|la|lo|i|gli|le|the|a|an)\s+/, "");
    const nAns = norm(answer);
    const ok = (p.risposte || []).some(a => norm(a) === nAns);
    if (ok) {
      state.puzzleDone[pid] = true;
      if (p.flag) setFlag(p.flag, true);
      if (p.oggetto) addItem(p.oggetto);
      if (p.ottieni) for (const ot of p.ottieni) addItem(ot);
      const gotItem = p.oggetto ? `\n\nHai ottenuto: ${W.items[p.oggetto]?.nome_completo || p.oggetto}.` : "";
      return {ok:true, msg: p.successo + gotItem};
    }
    return {ok:false, msg: p.fallimento};
  }

  // ---- Save / load ----
  const SAVE_KEY = "isola_naufragio_save_v1";
  const META_KEY = "isola_naufragio_meta_v1"; // achievement/codex persistenti cross-partita
  function save() {
    // Congela il timer per aggiornare state.elapsed prima di salvare
    freezeTimer();
    localStorage.setItem(SAVE_KEY, JSON.stringify(state));
    // Riparti il timer se stavamo giocando
    if (state.startedAt) startTimer();
    // Meta: achievement persistenti
    const meta = JSON.parse(localStorage.getItem(META_KEY) || "{}");
    for (const [aid, a] of Object.entries(state.achievements || {})) {
      if (!meta[aid]) meta[aid] = a;
    }
    localStorage.setItem(META_KEY, JSON.stringify(meta));
    return true;
  }
  function load() {
    const s = localStorage.getItem(SAVE_KEY);
    if (!s) return false;
    try {
      state = JSON.parse(s);
      // Inizializza campi nuovi se save vecchio
      if (!state.codex) state.codex = {};
      if (!state.achievements) state.achievements = {};
      if (!state.visited) state.visited = {};
      if (!state.elapsed) state.elapsed = 0;
      timerStart = null;
      emit({type: "loaded"});
      return true;
    } catch(e){ return false; }
  }
  function hasSave() { return !!localStorage.getItem(SAVE_KEY); }
  function reset() {
    state = newState();
    state.visited[state.room] = true;
    timerStart = null;
    localStorage.removeItem(SAVE_KEY);
    emit({type:"reset"});
  }
  function getMetaAchievements() {
    try { return JSON.parse(localStorage.getItem(META_KEY) || "{}"); }
    catch(e) { return {}; }
  }

  // ---- Select / deselect ----
  function select(id) { state.selected = id; emit({type:"select", id}); }
  function deselect() { state.selected = null; emit({type:"select", id:null}); }

  // Codex / map / achievements helpers
  function codexState() {
    const all = W.collectibles || {};
    const found = Object.keys(state.codex).length;
    const total = Object.keys(all).length;
    return {found, total, all, foundIds: state.codex};
  }
  function mapState() {
    return {
      positions: W.map_positions || {},
      visited: state.visited,
      current: state.room,
      rooms: W.rooms,
    };
  }
  function unlockAchievement(id, title, desc) {
    if (state.achievements[id]) return false;
    state.achievements[id] = {title, desc, when: Date.now()};
    emit({type: "achievement", id, title, desc});
    return true;
  }

  return {
    init, on, world, getState, setState,
    room, item, npc, roomItems, roomNpcs, roomExits, roomExtras,
    tryExit, takeItem, addItem, removeItem, setFlag, examine, inspectItem,
    useOn, dialogFor, tryPuzzle, checkCondition, checkObjCondition,
    save, load, hasSave, reset,
    select, deselect, wasVisited,
    codexState, mapState, unlockAchievement,
    startTimer, getElapsedSeconds, freezeTimer, getMetaAchievements,
  };
})();
