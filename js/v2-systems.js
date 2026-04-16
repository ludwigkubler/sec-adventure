// v2.0 Systems (semplificato dopo rollback)
// Contenuto disponibile OPZIONALMENTE via Menu: Thought Cabinet, Skills, Crafting Tree, Photo Mode
// Nessuna feature invasiva auto-running (no fatigue tick, no clock tick)
const V2 = (() => {
  // ─── Thought Cabinet (opzionale) ─────────────────────────────
  const THOUGHTS = {
    sospetto_guardiano: {
      nome: "Sospetto sul Guardiano",
      desc: "Qualcosa nel modo in cui risponde non ti convince. Forse mente.",
      reward_flag: "verita_guardiano",
      icon: "👁",
    },
    nostalgia_casa: {
      nome: "Nostalgia di casa",
      desc: "Ricordi una stanza, una voce, un odore. Ma non ricordi di chi.",
      reward_flag: "memoria_attivata",
      icon: "🏠",
    },
    eco_costruttore: {
      nome: "Eco del Costruttore",
      desc: "Ogni tanto sai cose senza averle imparate. Qualcosa in te ricorda.",
      reward_flag: "consapevolezza_costruttore",
      icon: "✦",
    },
    pieta_isola: {
      nome: "Pietà per l'isola",
      desc: "Più cammini, più senti che l'isola soffre. Forse ha bisogno di te, non viceversa.",
      reward_flag: "empatia_terra",
      icon: "🌿",
    },
    diffidenza_villaggio: {
      nome: "Diffidenza del villaggio",
      desc: "Sorridono ma ti studiano. Cosa nascondono?",
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
    st.thoughts[id] = {started: Date.now(), finished: false};
    Render.logSystem(`💭 Stai meditando: "${t.nome}"`);
    // Finisce dopo 3 min reali (non più usa WorldClock)
    setTimeout(() => {
      const s = Engine.getState();
      if (s.thoughts && s.thoughts[id] && !s.thoughts[id].finished) {
        s.thoughts[id].finished = true;
        if (t.reward_flag) Engine.setFlag(t.reward_flag, true);
        UI.showToast({title: `💭 Hai compreso: ${t.nome}`, body: t.desc, kind: "achievement"});
      }
    }, 3 * 60 * 1000);
    return true;
  }

  // ─── Skill + Karma (opzionale, narrativa statistica) ─────────
  const SKILLS = {
    intuito:    {nome: "Intuito",    desc: "Vedere oltre l'apparenza"},
    meccanica:  {nome: "Meccanica",  desc: "Capire come funzionano le cose"},
    empatia:    {nome: "Empatia",    desc: "Sentire ciò che altri sentono"},
    resistenza: {nome: "Resistenza", desc: "Sopportare fatica e dolore"},
    occhio:     {nome: "Occhio Vivo",desc: "Notare i dettagli minuti"},
    voce:       {nome: "Voce",       desc: "Parlare bene, persuadere"},
  };
  const FACTIONS = {
    villaggio:   {nome: "Villaggio",   desc: "Kaia, Marco, Tiko"},
    costruttori: {nome: "Costruttori", desc: "Archivista, Re-Automa"},
    mare:        {nome: "Il Mare",     desc: "Luna, abissi, profondità"},
  };

  function rollCheck(skill, difficulty) {
    const st = Engine.getState();
    if (!st.skills) st.skills = {};
    const level = st.skills[skill] || 1;
    const d6 = Math.floor(Math.random()*6) + 1;
    const d6b = Math.floor(Math.random()*6) + 1;
    return {success: d6+d6b+level >= difficulty, total: d6+d6b+level, level, dice: [d6, d6b], skill, difficulty};
  }
  function getKarma(faction) {
    const st = Engine.getState();
    return (st.karma && st.karma[faction]) || 0;
  }

  // ─── Crafting tree ───────────────────────────────────────────
  function getCraftingTree() {
    const w = Engine.world();
    const st = Engine.getState();
    return (w.recipes || []).map(r => {
      const have = r.ingredienti.every(i => st.inv.includes(i));
      const known = r.ingredienti.every(i => st.taken[i] || st.inv.includes(i));
      return {
        ingredients: r.ingredienti, result: r.risultato, message: r.messaggio,
        unlocked: known, craftable: have,
      };
    });
  }

  // ─── Photo mode ──────────────────────────────────────────────
  function showPhotoMode() {
    const st = Engine.getState();
    UI.show(`
      <h3>📷 Modalità Fotografia</h3>
      <p style="text-align:center;color:#a89060">L'inquadratura attuale verrà fissata come ricordo.</p>
      <div style="text-align:center;margin:20px 0">
        <div style="display:inline-block;border:2px solid var(--accent-hot);padding:8px;background:#000;box-shadow:0 0 30px rgba(192,138,60,.3)">
          <div style="width:240px;height:150px;background:radial-gradient(circle at center,var(--accent),var(--bg));display:flex;align-items:center;justify-content:center;color:var(--accent-hot);font-style:italic">${esc(Engine.room()?.nome || "Scena")}</div>
        </div>
      </div>
      <div class="modal-actions">
        <button id="ph-save">Salva nel diario</button>
        <button id="ph-close" style="opacity:.6">Annulla</button>
      </div>
    `);
    document.getElementById("ph-save").onclick = () => {
      if (!st.photos) st.photos = [];
      st.photos.push({room: st.room, ts: Date.now()});
      UI.close();
      Render.logSystem(`📷 Foto salvata (${st.photos.length} totali)`);
    };
    document.getElementById("ph-close").onclick = UI.close;
  }
  function esc(s) { return String(s||"").replace(/[<>&"]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c])); }

  return {
    THOUGHTS, SKILLS, FACTIONS,
    startThought, rollCheck, getKarma,
    getCraftingTree, showPhotoMode,
  };
})();

if (typeof window !== "undefined") window.V2 = V2;
