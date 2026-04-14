// Sistema di internazionalizzazione IT/EN.
// Carica data/world.<lang>.json e sostituisce il world attivo + stringhe UI.
const I18n = (() => {
  const LOCALES = ["it", "en"];
  let current = localStorage.getItem("isola_lang") || "it";
  const strings = {it: {}, en: {}};

  // Stringhe UI (hardcoded nella shell, non provenienti da world.json)
  const UI = {
    it: {
      new_game: "Nuova partita",
      continue: "Continua",
      subtitle: "~ un'avventura grafica ~",
      credits: "avventura punta-e-clicca · audio procedurale · tecnologia open source",
      open_eyes: "Apri gli occhi",
      close: "Chiudi",
      cancel: "Annulla",
      answer: "Rispondi",
      try_combination: "Prova la combinazione",
      give_up: "Rinuncia",
      step_away: "Allontanati",
      wait: "Aspetta i soccorsi (fine canonica)",
      descend: "Scendi nelle profondità (Atto II)",
      restart: "Ricomincia",
      dismiss: "Congedati",
      continue_btn: "Continua",
      journal: "📖 Diario",
      codex: "📜 Codex — Frammenti di Storia",
      map: "🗺 Mappa del Mondo",
      menu: "Menu",
      help_title: "Come si gioca",
      ending: "~ Il finale ~",
      secret_epilogue: "~ Epilogo Segreto ~",
      puzzle: "~ Enigma ~",
      lock: "~ Lucchetto ~",
      save: "💾 Salva partita",
      load: "📂 Carica partita",
      help_menu: "❓ Come si gioca",
      journal_menu: "📖 Diario",
      restart_menu: "🔄 Ricomincia da capo",
      save_saved: "Partita salvata.",
      save_loaded: "Partita caricata.",
      save_missing: "Nessun salvataggio trovato.",
      audio_on: "Audio riattivato.",
      audio_off: "Audio disattivato.",
      deselect: "Deselezionato.",
      inv_empty: "inventario vuoto",
      empty_journal: "Nessuna missione attiva. Esplora l'isola e parla con i suoi abitanti per scoprire cosa fare.",
      codex_tail: "Hai svelato tutta la lore. Un epilogo segreto ti attende dopo il finale principale.",
      explored: "Stanze esplorate",
      gold_current: "● dorato = posizione attuale",
      sepia_visited: "● seppia = visitata (Atto I)",
      cyan_visited: "● cyan = visitata (Atto II)",
      gray_unknown: "● grigio = sconosciuta",
      collected: "raccolti",
      unknown_frag: "??? sconosciuto ???",
      not_found: "Non l'hai ancora trovato.",
      lang_toggle: "🌐 English",
      hint_btn: "💡 Suggerimento",
      time: "Tempo",
      completion: "Completamento",
      rooms_visited: "Stanze",
      selected_hint: "Selezionato \"{name}\". Per COMBINARE: clicca un altro oggetto in inventario. Per USARE: clicca un personaggio, una porta, un dettaglio. (shift+click = esamina, click destro = deseleziona)",
      help_body: `
<p><b>Muoversi:</b> clicca le frecce luminose ai bordi della scena. Il colore cyan indica una via aperta, il rosso scuro una bloccata.</p>
<p><b>Raccogliere:</b> clicca un oggetto luminoso con anello dorato e finirà nel tuo inventario.</p>
<p><b>Esaminare:</b> clicca i piccoli rombi ◈ per osservare i dettagli dell'ambiente.</p>
<p><b>Parlare:</b> clicca il ritratto di un personaggio.</p>
<p><b>Usare / Combinare:</b> clicca un oggetto nell'inventario per selezionarlo (si illumina), poi clicca su un altro oggetto, una porta bloccata, un personaggio, o un dettaglio della scena. Il gioco capirà cosa intendi.</p>
<p><b>Esempio:</b> con legna selezionata, cliccala sulla pietra focaia per creare una torcia.</p>
<p><b>Tasti:</b> T=mappa · C=codex · J=diario · H=hint · M=audio · L=lingua · ESC=chiudi · click destro=deseleziona</p>`,
      tutorial_1: "Benvenuto, naufrago. Il cielo brucia e la sabbia è calda.",
      tutorial_2: "Guarda in basso: i frammenti dorati pulsanti sono oggetti da raccogliere. Cliccali.",
      tutorial_3: "Le frecce cyan ai bordi ti portano altrove. Tooltip al passaggio del mouse ti dice la destinazione se già visitata.",
      tutorial_4: "I rombi ◈ nascondono dettagli dell'ambiente da esaminare.",
      tutorial_5: "Quando hai un oggetto selezionato, cliccalo su un altro oggetto per combinare, o su una porta/personaggio per usare.",
      tutorial_dismiss: "Ho capito, parto.",
      hint_none: "In questa stanza non ho suggerimenti particolari. Prova a esaminare i dettagli, parlare con chi incontri, o usare un oggetto dell'inventario.",
    },
    en: {
      new_game: "New Game",
      continue: "Continue",
      subtitle: "~ a graphic adventure ~",
      credits: "point-and-click adventure · procedural audio · open source technology",
      open_eyes: "Open your eyes",
      close: "Close",
      cancel: "Cancel",
      answer: "Answer",
      try_combination: "Try the combination",
      give_up: "Give up",
      step_away: "Step away",
      wait: "Wait for rescue (canonical ending)",
      descend: "Descend into the depths (Act II)",
      restart: "Restart",
      dismiss: "Take your leave",
      continue_btn: "Continue",
      journal: "📖 Journal",
      codex: "📜 Codex — Lore Fragments",
      map: "🗺 World Map",
      menu: "Menu",
      help_title: "How to play",
      ending: "~ The ending ~",
      secret_epilogue: "~ Secret Epilogue ~",
      puzzle: "~ Riddle ~",
      lock: "~ Lock ~",
      save: "💾 Save game",
      load: "📂 Load game",
      help_menu: "❓ How to play",
      journal_menu: "📖 Journal",
      restart_menu: "🔄 Restart from scratch",
      save_saved: "Game saved.",
      save_loaded: "Game loaded.",
      save_missing: "No save found.",
      audio_on: "Audio on.",
      audio_off: "Audio muted.",
      deselect: "Deselected.",
      inv_empty: "inventory empty",
      empty_journal: "No active quest. Explore the island and talk to its inhabitants to find out what to do.",
      codex_tail: "You have revealed all the lore. A secret epilogue awaits after the main ending.",
      explored: "Rooms explored",
      gold_current: "● gold = current position",
      sepia_visited: "● sepia = visited (Act I)",
      cyan_visited: "● cyan = visited (Act II)",
      gray_unknown: "● gray = unknown",
      collected: "collected",
      unknown_frag: "??? unknown ???",
      not_found: "You haven't found it yet.",
      lang_toggle: "🌐 Italiano",
      hint_btn: "💡 Hint",
      time: "Time",
      completion: "Completion",
      rooms_visited: "Rooms",
      selected_hint: "Selected \"{name}\". To COMBINE: click another item in inventory. To USE: click a character, a door, a detail. (shift+click = examine, right-click = deselect)",
      help_body: `
<p><b>Moving:</b> click the glowing arrows at the edges of the scene. Cyan means an open path, dark red a blocked one.</p>
<p><b>Picking up:</b> click a glowing object with a gold ring to add it to your inventory.</p>
<p><b>Examining:</b> click the small diamonds ◈ to observe environmental details.</p>
<p><b>Talking:</b> click the portrait of a character.</p>
<p><b>Using / Combining:</b> click an item in your inventory to select it (it will glow), then click another item, a blocked door, a character, or an environmental detail. The game will understand.</p>
<p><b>Example:</b> with wood selected, click it on the flint to create a torch.</p>
<p><b>Keys:</b> T=map · C=codex · J=journal · H=hint · M=audio · L=language · ESC=close · right-click=deselect</p>`,
      tutorial_1: "Welcome, castaway. The sky burns and the sand is warm.",
      tutorial_2: "Look below: pulsing gold fragments are items to collect. Click them.",
      tutorial_3: "Cyan arrows at the edges take you elsewhere. Hover tooltip tells you the destination if already visited.",
      tutorial_4: "The diamonds ◈ hide environmental details to examine.",
      tutorial_5: "When you have an item selected, click it on another item to combine, or on a door/character to use.",
      tutorial_dismiss: "Got it, let's go.",
      hint_none: "I have no particular suggestion for this room. Try examining details, talking to those you meet, or using an inventory item.",
    },
  };

  async function loadLang(lang) {
    current = lang;
    localStorage.setItem("isola_lang", lang);
    if (strings[lang] && Object.keys(strings[lang]).length) return strings[lang];
    try {
      const r = await fetch(`data/world.${lang}.json`);
      if (r.ok) strings[lang] = await r.json();
    } catch(e) {}
    return strings[lang] || {};
  }

  function getWorld() { return strings[current] || {}; }
  function getLang() { return current; }
  function getLocales() { return LOCALES; }

  // t("key") → stringa UI localizzata
  function t(key, vars={}) {
    const src = UI[current]?.[key] || UI.it[key] || key;
    return String(src).replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? `{${k}}`);
  }

  async function setLang(lang) {
    if (!LOCALES.includes(lang)) return;
    await loadLang(lang);
    // emit event if callback registered
    if (onChange) onChange(lang);
  }

  let onChange = null;
  function setOnChange(fn) { onChange = fn; }

  return {loadLang, getWorld, getLang, getLocales, t, setLang, setOnChange};
})();
