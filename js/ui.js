// Modali: dialoghi, enigmi, esame, diario, aiuto, menu, finale.
const UI = (() => {
  const $modal = () => document.getElementById("modal");
  const $content = () => document.getElementById("modal-content");

  function show(html) {
    $content().innerHTML = html;
    $modal().classList.remove("hidden");
  }
  function close() { $modal().classList.add("hidden"); }

  function showText(title, body, onClose) {
    show(`
      <h3>${esc(title)}</h3>
      <p>${esc(body).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <div class="modal-actions">
        <button id="ui-close">Continua</button>
      </div>
    `);
    document.getElementById("ui-close").onclick = () => {
      close();
      if (onClose) onClose();
    };
  }

  function showDialog(npcId) {
    const npc = Engine.npc(npcId);
    const stage = Engine.dialogFor(npcId);
    if (!stage) { showText(npc?.nome || "?", "Non risponde."); return; }

    const optsHtml = (stage.opzioni || []).map((o, i) =>
      `<button class="dialog-opt" data-i="${i}">${esc(o.testo)}</button>`
    ).join("");
    show(`
      <h3>${esc(npc?.nome || npcId)}</h3>
      <p>${esc(stage.saluto || "").replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <div class="modal-actions">
        ${optsHtml}
        <button id="dlg-end" style="opacity:.7;margin-top:8px">Congedati</button>
      </div>
    `);
    document.querySelectorAll(".dialog-opt").forEach(btn => {
      btn.onclick = () => {
        Audio.sfx("click");
        const i = +btn.dataset.i;
        const opt = stage.opzioni[i];
        if (opt.tipo === "enigma" && opt.enigma_id) { close(); showPuzzle(opt.enigma_id); return; }
        if (opt.fine) { close(); return; }
        if (opt.azione && opt.azione.tipo === "flag") Engine.setFlag(opt.azione.id, true);
        if (opt.flag) Engine.setFlag(opt.flag, true);
        if (opt.ottieni) for (const o of opt.ottieni) Engine.addItem(o);
        if (opt.rimuovi) for (const r of opt.rimuovi) Engine.removeItem(r);
        showText(npc.nome, opt.risposta || "", () => showDialog(npcId));
      };
    });
    document.getElementById("dlg-end").onclick = () => { Audio.sfx("click"); close(); };
  }

  function showPuzzle(pid) {
    const p = Engine.world().puzzles[pid];
    if (!p) return;
    show(`
      <h3>~ Enigma ~</h3>
      <p>${esc(p.testo).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <input type="text" class="puzzle-input" id="puz-input" placeholder="la tua risposta...">
      <div class="modal-actions">
        <button id="puz-go">Rispondi</button>
        <button id="puz-cancel" style="opacity:.6">Rinuncia</button>
      </div>
    `);
    const input = document.getElementById("puz-input");
    input.focus();
    input.onkeydown = (e) => { if (e.key === "Enter") document.getElementById("puz-go").click(); };
    document.getElementById("puz-go").onclick = () => {
      const res = Engine.tryPuzzle(pid, input.value);
      Audio.sfx(res.ok ? "puzzle_ok" : "puzzle_fail");
      showText("Enigma", res.msg, () => Render.drawScene());
    };
    document.getElementById("puz-cancel").onclick = close;
  }

  // ─── Diario missioni ───
  function showJournal() {
    Audio.sfx("click");
    const w = Engine.world();
    const st = Engine.getState();
    const quests = Object.entries(w.quests || {});
    let html = `<h3>📖 Diario</h3>`;
    let any = false;
    for (const [qid, q] of quests) {
      const active = st.flags[q.flag_attivazione];
      const done = st.flags[q.flag_completamento];
      if (!active && !done) continue;
      any = true;
      html += `<div class="journal-quest ${done ? "done" : ""}"><h4>${esc(q.nome)}${done ? " ✓" : ""}</h4>`;
      html += `<div class="desc">${esc(q.descrizione)}</div>`;
      for (const ob of (q.obiettivi || [])) {
        const okFlag = ob.check?.startsWith("flag:") && st.flags[ob.check.slice(5)];
        const okItem = ob.check?.startsWith("oggetto:") && st.inv.includes(ob.check.slice(8));
        const ok = okFlag || okItem || done;
        html += `<div class="obj ${ok ? "done" : ""}">${esc(ob.desc)}</div>`;
      }
      html += `</div>`;
    }
    // Status faro
    const faroStat = ["faro_olio","faro_cristallo","faro_gemma"].map(f => st.flags[f]);
    if (faroStat.some(Boolean) || st.visited["faro"]) {
      any = true;
      const allDone = faroStat.every(Boolean);
      html += `<div class="journal-quest ${allDone ? "done" : ""}"><h4>Il Faro Antico${allDone ? " ✓" : ""}</h4>`;
      html += `<div class="desc">Tre componenti per accendere il faro e segnalare un soccorso.</div>`;
      html += `<div class="obj ${st.flags.faro_olio?"done":""}">Olio nel braciere</div>`;
      html += `<div class="obj ${st.flags.faro_cristallo?"done":""}">Cristallo nel braciere</div>`;
      html += `<div class="obj ${st.flags.faro_gemma?"done":""}">Gemma nel braciere</div>`;
      html += `</div>`;
    }
    if (!any) html += `<p class="journal-empty">Nessuna missione attiva. Esplora l'isola e parla con i suoi abitanti per scoprire cosa fare.</p>`;
    html += `<div class="modal-actions"><button id="ui-close">Chiudi</button></div>`;
    show(html);
    document.getElementById("ui-close").onclick = close;
  }

  function showHelp() {
    Audio.sfx("click");
    show(`
      <h3>Come si gioca</h3>
      <p><b>Muoversi:</b> clicca le frecce luminose ai bordi della scena. Il colore cyan indica una via aperta, il rosso scuro una bloccata.</p>
      <p><b>Raccogliere:</b> clicca un oggetto luminoso con anello dorato e finirà nel tuo inventario.</p>
      <p><b>Esaminare:</b> clicca i piccoli rombi ◈ per osservare i dettagli dell'ambiente.</p>
      <p><b>Parlare:</b> clicca il ritratto di un personaggio.</p>
      <p><b>Usare / Combinare:</b> clicca un oggetto nell'inventario per selezionarlo (si illumina), poi clicca su un altro oggetto, una porta bloccata, un personaggio, o un dettaglio della scena. Il gioco capirà cosa intendi.</p>
      <p><b>Esempio:</b> con legna selezionata, cliccala sulla pietra focaia per creare una torcia. Con la torcia, puoi sbloccare il passaggio buio nella caletta.</p>
      <p><b>Tasti:</b> J = diario · M = audio · ESC = chiudi/deseleziona · Click destro = deseleziona</p>
      <div class="modal-actions"><button id="ui-close">Chiudi</button></div>
    `);
    document.getElementById("ui-close").onclick = close;
  }

  function showMenu() {
    Audio.sfx("click");
    show(`
      <h3>Menu</h3>
      <div class="modal-actions">
        <button id="m-save">💾 Salva partita</button>
        <button id="m-load">📂 Carica partita</button>
        <button id="m-help">❓ Come si gioca</button>
        <button id="m-journal">📖 Diario</button>
        <button id="m-restart" style="opacity:.7">🔄 Ricomincia da capo</button>
        <button id="ui-close">Chiudi</button>
      </div>
    `);
    document.getElementById("m-save").onclick = () => { Engine.save(); Audio.sfx("puzzle_ok"); showText("Salvataggio", "Partita salvata."); };
    document.getElementById("m-load").onclick = () => {
      if (Engine.load()) { close(); Render.drawScene(); Audio.setRoom(Engine.getState().room); Render.logSystem("Partita caricata."); }
      else showText("Errore", "Nessun salvataggio trovato.");
    };
    document.getElementById("m-help").onclick = showHelp;
    document.getElementById("m-journal").onclick = showJournal;
    document.getElementById("m-restart").onclick = () => {
      if (confirm("Sei sicuro di voler ricominciare? I progressi attuali andranno persi.")) {
        Engine.reset(); location.reload();
      }
    };
    document.getElementById("ui-close").onclick = close;
  }

  function showIntro(text, onStart) {
    show(`
      <h3>L'Isola del Naufragio</h3>
      <p>${esc(text).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <div class="modal-actions">
        <button id="ui-start">Apri gli occhi</button>
      </div>
    `);
    document.getElementById("ui-start").onclick = () => { Audio.sfx("click"); close(); if (onStart) onStart(); };
  }

  function showEnding(text) {
    Audio.sfx("ending");
    show(`
      <h3>~ Il finale ~</h3>
      <p>${esc(text).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <div class="modal-actions">
        <button id="ui-restart">Ricomincia</button>
      </div>
    `);
    document.getElementById("ui-restart").onclick = () => { Engine.reset(); location.reload(); };
  }

  // Schermata speciale: il faro è acceso. Scelta tra finale "soccorso" o discesa nelle profondità.
  function showFaroLit(originalFinale) {
    Audio.sfx("ending");
    show(`
      <h3>~ Il Faro Antico ~</h3>
      <p>La luce del faro squarcia il cielo notturno. Da qualche parte, lontano, una nave la vedrà — e verrà a salvarti.</p>
      <p>Ma sotto i tuoi piedi, il pavimento di pietra del faro si è aperto come un fiore di metallo. Una scala scende nel buio, illuminata da una luce verde-azzurra che pulsa come un battito.</p>
      <p><i>Questo faro non era solo un faro. Era una porta. E la porta è ora aperta.</i></p>
      <div class="modal-actions">
        <button id="ui-rescue">Aspetta i soccorsi (fine canonica)</button>
        <button id="ui-descend">Scendi nelle profondità (Atto II)</button>
      </div>
    `);
    document.getElementById("ui-rescue").onclick = () => {
      close();
      setTimeout(() => showEnding(originalFinale), 400);
    };
    document.getElementById("ui-descend").onclick = () => {
      Audio.sfx("door");
      Engine.setFlag("visto_pozzo", true);
      close();
      Render.logSystem("Decidi di scendere. Il pavimento del faro si è aperto: il pozzo ti aspetta.");
      Render.logSystem("Cerca una nuova uscita verso il basso (giù).");
      Render.drawScene();
    };
  }

  // ─── PUZZLE INTERATTIVO: lucchetto a combinazione (4 rotelle) ───
  function showLockPuzzle(pid) {
    const puz = Engine.world().puzzles_interactive[pid];
    if (!puz) return;
    let current = puz.rotelle.map(() => 0); // indice corrente per ogni rotella

    function render() {
      const rotelle = puz.rotelle.map((symbols, i) => {
        const sym = symbols[current[i]];
        return `
          <div class="lock-wheel">
            <button class="lock-arrow" data-i="${i}" data-d="-1">▲</button>
            <div class="lock-symbol">${esc(sym)}</div>
            <button class="lock-arrow" data-i="${i}" data-d="1">▼</button>
          </div>
        `;
      }).join("");
      show(`
        <h3>~ Lucchetto ~</h3>
        <p>${esc(puz.testo).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
        <div class="lock-container">${rotelle}</div>
        <div class="modal-actions">
          <button id="lock-go">Prova la combinazione</button>
          <button id="lock-cancel" style="opacity:.6">Allontanati</button>
        </div>
      `);
      document.querySelectorAll(".lock-arrow").forEach(b => {
        b.onclick = () => {
          const i = +b.dataset.i;
          const d = +b.dataset.d;
          const len = puz.rotelle[i].length;
          current[i] = (current[i] + d + len) % len;
          Audio.sfx("click");
          render();
        };
      });
      document.getElementById("lock-go").onclick = () => {
        const tries = current.map((idx, i) => puz.rotelle[i][idx]);
        const ok = tries.every((s, i) => s === puz.soluzione[i]);
        if (ok) {
          Audio.sfx("puzzle_ok");
          if (puz.flag) Engine.setFlag(puz.flag, true);
          for (const o of (puz.ottieni || [])) Engine.addItem(o);
          showText("Lucchetto", puz.successo, () => Render.drawScene());
        } else {
          Audio.sfx("puzzle_fail");
          showText("Lucchetto", puz.fallimento, () => showLockPuzzle(pid));
        }
      };
      document.getElementById("lock-cancel").onclick = close;
    }
    render();
  }

  function esc(s) {
    return String(s||"").replace(/[<>&"]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c]));
  }

  // ─── CODEX (collezionabili lore) ───
  function showCodex() {
    Audio.sfx("click");
    const cs = Engine.codexState();
    const w = Engine.world();
    const cards = Object.entries(cs.all).map(([id, info]) => {
      const found = !!cs.foundIds[id];
      if (found) {
        return `<div class="codex-card found">
          <div class="codex-img"><img src="assets/items/${id}.svg" onerror="this.style.display='none'"></div>
          <div class="codex-info">
            <div class="codex-name">${esc(info.nome)}</div>
            <div class="codex-lore">${esc(info.lore)}</div>
          </div>
        </div>`;
      }
      return `<div class="codex-card locked">
        <div class="codex-img">?</div>
        <div class="codex-info">
          <div class="codex-name">??? sconosciuto ???</div>
          <div class="codex-lore">Non l'hai ancora trovato.</div>
        </div>
      </div>`;
    }).join("");
    const pct = Math.round((cs.found / cs.total) * 100);
    show(`
      <h3>📜 Codex — Frammenti di Storia</h3>
      <div class="codex-progress">
        <div class="codex-bar"><div class="codex-bar-fill" style="width:${pct}%"></div></div>
        <div class="codex-counter">${cs.found} / ${cs.total} raccolti</div>
      </div>
      <div class="codex-grid">${cards}</div>
      ${cs.found === cs.total ? '<p style="text-align:center;color:var(--accent-hot);font-style:italic;margin-top:14px">Hai svelato tutta la lore. Un epilogo segreto ti attende dopo il finale principale.</p>' : ""}
      <div class="modal-actions"><button id="ui-close">Chiudi</button></div>
    `);
    document.getElementById("ui-close").onclick = close;
  }

  // ─── MAP (mappa interattiva) ───
  function showMap() {
    Audio.sfx("click");
    const ms = Engine.mapState();
    const positions = ms.positions;
    const visited = ms.visited;
    const current = ms.current;
    const rooms = ms.rooms;

    // Costruisci il grafo: archi tra stanze visitate adiacenti
    const edges = [];
    for (const [rid, room] of Object.entries(rooms)) {
      if (!positions[rid]) continue;
      const exits = [...Object.values(room.uscite || {})];
      // include uscite_bloccate sbloccate? Considero solo collegamenti certi (uscite normali)
      for (const e of exits) {
        if (positions[e] && rid < e) {
          edges.push([rid, e]);
        }
      }
      // E le uscite bloccate, mostrate solo se entrambe visitate
      for (const [d, b] of Object.entries(room.uscite_bloccate || {})) {
        const dest = (Engine.world().blocked_destinations || {})[rid + "::" + d] || b.destinazione;
        if (dest && positions[dest] && visited[dest] && rid < dest) {
          edges.push([rid, dest]);
        }
      }
    }

    // Genera SVG
    const SVG_W = 720, SVG_H = 420;
    const sx = (x) => 30 + (x / 100) * (SVG_W - 60);
    const sy = (y) => 30 + (y / 100) * (SVG_H - 60);

    let svgEdges = "";
    for (const [a, b] of edges) {
      const va = visited[a], vb = visited[b];
      const cls = (va && vb) ? "edge known" : (va || vb) ? "edge half" : "edge unknown";
      svgEdges += `<line class="${cls}" x1="${sx(positions[a].x)}" y1="${sy(positions[a].y)}" x2="${sx(positions[b].x)}" y2="${sy(positions[b].y)}"/>`;
    }

    let svgNodes = "";
    for (const [rid, p] of Object.entries(positions)) {
      const v = !!visited[rid];
      const isCur = rid === current;
      const cls = isCur ? "node current" : v ? `node visited atto-${p.atto}` : "node unknown";
      const r = isCur ? 8 : 5;
      svgNodes += `<g><circle class="${cls}" cx="${sx(p.x)}" cy="${sy(p.y)}" r="${r}"/>`;
      if (v) {
        svgNodes += `<text class="map-label" x="${sx(p.x)}" y="${sy(p.y) - 10}" text-anchor="middle">${esc(rooms[rid]?.nome || rid)}</text>`;
      }
      svgNodes += `</g>`;
    }

    // Linee di separazione: superficie / sotterraneo
    const separator = `<line class="map-separator" x1="20" y1="${sy(35)}" x2="${SVG_W-20}" y2="${sy(35)}"/>
                       <text class="map-section" x="30" y="${sy(38)+18}">▼ ATTO II — Le Profondità</text>
                       <text class="map-section" x="30" y="${sy(35)-6}">▲ ATTO I — Superficie</text>`;

    const visitedCount = Object.keys(visited).length;
    const totalRooms = Object.keys(positions).length;

    show(`
      <h3>🗺 Mappa del Mondo</h3>
      <p style="font-size:13px;color:#a89060;text-align:center;margin-bottom:8px">
        Stanze esplorate: <b>${visitedCount}</b> / ${totalRooms}
      </p>
      <div class="map-container">
        <svg viewBox="0 0 ${SVG_W} ${SVG_H}" class="map-svg">
          ${separator}
          ${svgEdges}
          ${svgNodes}
        </svg>
      </div>
      <p style="font-size:12px;color:#7a6850;text-align:center;margin-top:6px">
        ● dorato = posizione attuale &nbsp; ● seppia = visitata (Atto I) &nbsp; ● cyan = visitata (Atto II) &nbsp; ● grigio = sconosciuta
      </p>
      <div class="modal-actions"><button id="ui-close">Chiudi</button></div>
    `);
    document.getElementById("ui-close").onclick = close;
  }

  // ─── TOAST achievement / discovery ───
  function showToast({title, body, kind = "achievement"}) {
    const t = document.createElement("div");
    t.className = "toast toast-" + kind;
    t.innerHTML = `
      <div class="toast-icon">${kind === "codex" ? "📜" : kind === "achievement" ? "🏆" : "✦"}</div>
      <div class="toast-text">
        <div class="toast-title">${esc(title)}</div>
        ${body ? `<div class="toast-body">${esc(body)}</div>` : ""}
      </div>
    `;
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add("show"));
    setTimeout(() => {
      t.classList.remove("show");
      setTimeout(() => t.remove(), 600);
    }, 4500);
  }

  // ─── EPILOGO SEGRETO ───
  function showSecretEpilogue(text) {
    Audio.sfx("ending");
    show(`
      <h3>~ Epilogo Segreto ~</h3>
      <p style="font-style:italic;color:var(--accent-hot)">${esc(text).replace(/\n\n/g,"</p><p style='font-style:italic;color:var(--accent-hot)'>").replace(/\n/g,"<br>")}</p>
      <div class="modal-actions"><button id="ui-restart">Ricomincia</button></div>
    `);
    document.getElementById("ui-restart").onclick = () => { Engine.reset(); location.reload(); };
  }

  // ─── Hint contestuale per stanza/stato gioco ───
  const HINTS = {
    "spiaggia":  () => "Raccogli legna, corda, bottiglia. Esplora est e nord.",
    "caletta":   () => hasItem("pietra_focaia") ? "Hai la pietra focaia. Torna indietro e combinala con la legna per una torcia." : "Raccogli la pietra focaia. Serve una torcia per procedere a est.",
    "radura":    () => hasFlag("sentiero_giungla") ? "Il sentiero a nord è aperto." : "Il sentiero a nord è bloccato. Serve un machete — cerca nella caletta e nel tempio sommerso i componenti.",
    "molo":      () => "Parla con Tiko e prova ad aiutarlo riparando la barca.",
    "villaggio": () => hasFlag("quest_kaia_completa") ? "Hai il medaglione. Esplora la giungla a est." : "Parla con Kaia e accetta la sua quest.",
    "rovine":    () => hasItem("medaglione") ? "Il medaglione ti permette di entrare." : "Serve il medaglione di Kaia per entrare.",
    "sala_guardiano": () => hasFlag("enigma2_risolto") ? "Hai entrambe le chiavi. Scendi nella cripta." : hasFlag("enigma1_risolto") ? "Un enigma risolto, uno da risolvere." : "Parla con il Guardiano e affronta i suoi due enigmi.",
    "cripta":    () => hasItem("piccone") && !hasFlag("cunicolo_aperto") ? "Hai il piccone! Prova a usarlo sul muro screpolato a nord." : hasFlag("cunicolo_aperto") ? "Il cunicolo a nord è aperto: entra." : "C'è un muro screpolato a nord. Servirebbe qualcosa di robusto.",
    "faro":      () => hasFlag("faro_acceso") ? "Il faro è acceso. Scendi nel pozzo verticale." : "Posiziona olio, cristallo, gemma nel braciere.",
    "cima_vulcano": () => "Raccogli il cristallo vulcanico per il faro.",
    "capanna_luna": () => "Luna accetta la pianta rara e in cambio ti dà l'antidoto.",
    "tempio_sommerso": () => "Raccogli gli artefatti antichi del tempio.",
    "scogliere": () => "Entra nel faro a ovest.",
    "giungla":   () => hasItem("medaglione") ? "Usa il medaglione sul portale a est per aprire le rovine." : "Porta con te il medaglione di Kaia per accedere alle rovine a est.",
    // Atto II
    "pozzo_faro": () => "Scendi ancora — le profondità ti attendono.",
    "cripta_meccanica": () => hasItem("valvola_vapore") ? "Usa la valvola sulla stanza per sbloccare il corridoio est." : "Raccogli gli ingranaggi; la valvola è in sala_ingranaggi.",
    "sala_ingranaggi": () => hasFlag("asta_estratta") && hasItem("pendolo_ottone") ? "Combina asta manovella e pendolo per completare la manovella." : hasItem("martello_rame") && !hasFlag("asta_estratta") ? "Usa il martello sulla manovella per estrarne l'asta." : "Raccogli martello, binario, valvola. Il martello sblocca l'asta della manovella.",
    "forgia_antica": () => "Raccogli il pendolo e l'ampolla.",
    "archivio": () => "Parla con l'Archivista. Consegnale la tavoletta runica per un dono.",
    "osservatorio": () => hasItem("lente_smeraldo") ? "Usa la lente sull'astrolabio per allineare le stelle." : "Trova il frammento di stella; combinalo con l'ampolla per la lente di smeraldo.",
    "cuore_macchina": () => hasItem("manovella_completa") ? "Torna in sala_ingranaggi e usa la manovella completa lì." : "Serve la manovella completa — costruiscila in sala_ingranaggi.",
    "agora_perduta": () => hasFlag("re_completato") ? "Attraversa il ponte a nord verso l'abisso (prima ripara il ponte)." : "Parla con il Re-Automa. Esamina lo scrigno ai piedi del trono.",
    "via_titani": () => hasItem("meccanismo_completo") ? "Usa il meccanismo sul portale." : "Il portale ha tre incavi. Oppure vai all'abisso.",
    "abisso": () => hasItem("funi_metalliche_intrecciate") ? "Usa le funi+binario sul ponte per ripararlo." : "Il ponte è rotto. Serve funi_metalliche (da archivio) + binario (da sala_ingranaggi).",
    "radice_mondo": () => hasItem("corona_attivata") ? "Usa la corona attivata qui per il finale." : hasItem("corona_titanica") ? "La corona va attivata: frammento_stella, occhio_titano, radice_madre." : "Raccogli la corona e la radice. Attivala con 3 componenti.",
    "cunicolo_nascosto": () => "Raccogli la lampada eterna — tredicesimo frammento di codex.",
  };
  const HINTS_EN = {
    "spiaggia":  () => "Collect wood, rope, bottle. Explore east and north.",
    "caletta":   () => hasItem("pietra_focaia") ? "You have the flint. Go back and combine it with wood for a torch." : "Collect the flint. You need a torch to proceed east.",
    "radura":    () => hasFlag("sentiero_giungla") ? "The north path is open." : "The north path is blocked. You need a machete — look in the cove and submerged temple for components.",
    "molo":      () => "Talk to Tiko and help him repair the boat.",
    "villaggio": () => hasFlag("quest_kaia_completa") ? "You have the medallion. Explore the jungle east." : "Talk to Kaia and accept her quest.",
    "rovine":    () => hasItem("medaglione") ? "The medallion lets you in." : "You need Kaia's medallion to enter.",
    "sala_guardiano": () => hasFlag("enigma2_risolto") ? "You have both keys. Descend to the crypt." : hasFlag("enigma1_risolto") ? "One riddle solved, one to go." : "Talk to the Guardian and face his two riddles.",
    "cripta":    () => hasItem("piccone") && !hasFlag("cunicolo_aperto") ? "You have the pickaxe! Try using it on the cracked wall to the north." : hasFlag("cunicolo_aperto") ? "The northern tunnel is open: enter." : "There's a cracked wall to the north. Need something sturdy.",
    "faro":      () => hasFlag("faro_acceso") ? "The lighthouse is lit. Go down the vertical well." : "Place oil, crystal, gem in the brazier.",
    "cima_vulcano": () => "Collect the volcanic crystal for the lighthouse.",
    "capanna_luna": () => "Luna accepts the rare plant and gives you the antidote in exchange.",
    "tempio_sommerso": () => "Collect the ancient temple artifacts.",
    "scogliere": () => "Enter the lighthouse to the west.",
    "giungla":   () => hasItem("medaglione") ? "Use the medallion on the east portal to open the ruins." : "Bring Kaia's medallion to access the ruins east.",
    "pozzo_faro": () => "Descend further — the depths await.",
    "cripta_meccanica": () => hasItem("valvola_vapore") ? "Use the valve on the room to unlock the east corridor." : "Collect the gears; the valve is in the gear hall.",
    "sala_ingranaggi": () => hasFlag("asta_estratta") && hasItem("pendolo_ottone") ? "Combine crank shaft and pendulum to complete the crank." : hasItem("martello_rame") && !hasFlag("asta_estratta") ? "Use the hammer on the crank to extract the shaft." : "Collect hammer, rail, valve. The hammer unlocks the crank shaft.",
    "forgia_antica": () => "Collect the pendulum and the vial.",
    "archivio": () => "Talk to the Archivist. Deliver the runic tablet for a gift.",
    "osservatorio": () => hasItem("lente_smeraldo") ? "Use the lens on the astrolabe to align the stars." : "Find the star fragment; combine with vial for emerald lens.",
    "cuore_macchina": () => hasItem("manovella_completa") ? "Go back to the gear hall and use the complete crank there." : "You need the complete crank — build it in the gear hall.",
    "agora_perduta": () => hasFlag("re_completato") ? "Cross the bridge north to the abyss (first repair the bridge)." : "Talk to the Automaton-King. Examine the chest at the feet of the throne.",
    "via_titani": () => hasItem("meccanismo_completo") ? "Use the mechanism on the portal." : "The portal has three recesses. Or go to the abyss.",
    "abisso": () => hasItem("funi_metalliche_intrecciate") ? "Use ropes+rail on the bridge to repair it." : "The bridge is broken. Need metal cables (from archive) + rail (from gear hall).",
    "radice_mondo": () => hasItem("corona_attivata") ? "Use the activated crown here for the ending." : hasItem("corona_titanica") ? "The crown must be activated: star_fragment, titan_eye, mother_root." : "Collect the crown and the root. Activate it with 3 components.",
    "cunicolo_nascosto": () => "Collect the eternal lamp — thirteenth codex fragment.",
  };
  function hasItem(id) { return Engine.getState().inv.includes(id); }
  function hasFlag(f) { return !!Engine.getState().flags[f]; }

  function showHint() {
    Audio.sfx("click");
    const lang = I18n.getLang();
    const room = Engine.getState().room;
    const map = lang === "en" ? HINTS_EN : HINTS;
    const fn = map[room];
    const text = fn ? fn() : I18n.t("hint_none");
    show(`
      <h3>💡 ${I18n.t("hint_btn")}</h3>
      <p style="color:#d8c090;font-style:italic">${esc(text)}</p>
      <div class="modal-actions"><button id="ui-close">${esc(I18n.t("close"))}</button></div>
    `);
    document.getElementById("ui-close").onclick = close;
  }

  // ─── Tutorial interattivo prima partita ───
  function showTutorial() {
    Audio.sfx("click");
    const steps = [1,2,3,4,5].map(i => I18n.t("tutorial_" + i));
    let idx = 0;
    function draw() {
      show(`
        <h3>🎓 ${I18n.t("help_title")}</h3>
        <p style="font-size:16px;line-height:1.7;min-height:120px">${esc(steps[idx])}</p>
        <div style="text-align:center;color:#7a6850;font-size:12px">${idx+1}/${steps.length}</div>
        <div class="modal-actions">
          ${idx < steps.length - 1
            ? `<button id="t-next">${esc(I18n.t("continue_btn"))} →</button>`
            : `<button id="t-done">${esc(I18n.t("tutorial_dismiss"))}</button>`}
          <button id="t-skip" style="opacity:.6">${esc(I18n.t("cancel"))}</button>
        </div>
      `);
      const nxt = document.getElementById("t-next");
      if (nxt) nxt.onclick = () => { idx++; Audio.sfx("click"); draw(); };
      const done = document.getElementById("t-done");
      if (done) done.onclick = () => { Audio.sfx("fanfare"); close(); };
      document.getElementById("t-skip").onclick = close;
    }
    draw();
  }

  // ─── Puzzle interattivo: ALLINEAMENTO STELLE (osservatorio) ───
  function showStarPuzzle(pid) {
    Audio.sfx("click");
    const puz = Engine.world().puzzles_interactive[pid];
    if (!puz) return;
    let angles = [Math.random()*360, Math.random()*360, Math.random()*360];
    const targets = puz.targets || [90, 180, 270];
    function draw() {
      const stars = angles.map((a, i) => `
        <div class="star-container">
          <svg viewBox="0 0 100 100" class="star-dial">
            <circle cx="50" cy="50" r="45" fill="none" stroke="#3a2818" stroke-width="1.5"/>
            <circle cx="50" cy="50" r="45" fill="none" stroke="#c08a3c" stroke-width="1.5" stroke-dasharray="3 3" transform="rotate(${targets[i]} 50 50)"/>
            <g transform="rotate(${a} 50 50)">
              <line x1="50" y1="50" x2="50" y2="10" stroke="#f0b25a" stroke-width="2"/>
              <circle cx="50" cy="10" r="5" fill="#fff0a0" stroke="#f0b25a" stroke-width="1.5"/>
            </g>
            <circle cx="50" cy="50" r="3" fill="#5c3e1c"/>
          </svg>
          <div class="star-buttons">
            <button class="star-btn" data-i="${i}" data-d="-15">◀</button>
            <span class="star-angle">${Math.round(a)}°</span>
            <button class="star-btn" data-i="${i}" data-d="15">▶</button>
          </div>
        </div>`).join("");
      show(`
        <h3>✦ ${I18n.t("puzzle")}</h3>
        <p>${esc(puz.testo).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
        <div class="stars-container">${stars}</div>
        <p style="text-align:center;color:#7a6850;font-size:11px">${I18n.getLang()==="en" ? "Align each star with the dashed mark." : "Allinea ogni stella con il segno tratteggiato."}</p>
        <div class="modal-actions">
          <button id="star-go">${esc(I18n.t("try_combination"))}</button>
          <button id="star-cancel" style="opacity:.6">${esc(I18n.t("step_away"))}</button>
        </div>
      `);
      document.querySelectorAll(".star-btn").forEach(b => {
        b.onclick = () => {
          const i = +b.dataset.i, d = +b.dataset.d;
          angles[i] = (angles[i] + d + 360) % 360;
          Audio.sfx("click");
          draw();
        };
      });
      document.getElementById("star-go").onclick = () => {
        const ok = angles.every((a, i) => {
          const diff = Math.abs(((a - targets[i] + 540) % 360) - 180) - 180;
          return Math.abs(diff) <= 10 || Math.abs(a - targets[i]) <= 10;
        });
        if (ok) {
          Audio.sfx("puzzle_ok");
          if (puz.flag) Engine.setFlag(puz.flag, true);
          for (const o of (puz.ottieni || [])) Engine.addItem(o);
          showText(I18n.t("puzzle"), puz.successo, () => Render.drawScene());
        } else {
          Audio.sfx("puzzle_fail");
          showText(I18n.t("puzzle"), puz.fallimento, () => showStarPuzzle(pid));
        }
      };
      document.getElementById("star-cancel").onclick = close;
    }
    draw();
  }

  // ─── Puzzle interattivo: PENDOLO RITMO (cuore_macchina) ───
  function showPendulumPuzzle(pid) {
    Audio.sfx("click");
    const puz = Engine.world().puzzles_interactive[pid];
    if (!puz) return;
    const target = puz.target_rhythm || [800, 800, 800, 800];
    let hits = [];
    let lastBeat = null;
    show(`
      <h3>✦ ${I18n.t("puzzle")}</h3>
      <p>${esc(puz.testo).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")}</p>
      <div id="pendulum-area">
        <div id="pendulum-rod"><div id="pendulum-weight"></div></div>
        <div id="pendulum-hits">${target.map((_,i) => `<span class="hit-mark" data-i="${i}">○</span>`).join("")}</div>
      </div>
      <p style="text-align:center;color:#a89060;font-size:13px">${I18n.getLang()==="en" ? "Click \"BEAT\" in sync with the pendulum, 4 times in a row." : "Clicca \"BATTI\" a tempo col pendolo, 4 volte di fila."}</p>
      <div class="modal-actions">
        <button id="pend-beat" style="padding:16px;font-size:16px">${I18n.getLang()==="en" ? "⚙ BEAT" : "⚙ BATTI"}</button>
        <button id="pend-cancel" style="opacity:.6">${esc(I18n.t("step_away"))}</button>
      </div>
    `);
    document.getElementById("pend-beat").onclick = () => {
      const now = Date.now();
      Audio.sfx("click");
      if (lastBeat !== null) {
        const delta = now - lastBeat;
        const expected = target[hits.length];
        const ok = Math.abs(delta - expected) <= 220;
        hits.push(ok);
        const el = document.querySelector(`.hit-mark[data-i="${hits.length-1}"]`);
        if (el) { el.textContent = ok ? "●" : "✗"; el.className = "hit-mark " + (ok ? "good" : "bad"); }
        if (hits.length >= target.length) {
          const allGood = hits.every(Boolean);
          setTimeout(() => {
            if (allGood) {
              Audio.sfx("puzzle_ok");
              if (puz.flag) Engine.setFlag(puz.flag, true);
              for (const o of (puz.ottieni || [])) Engine.addItem(o);
              showText(I18n.t("puzzle"), puz.successo, () => Render.drawScene());
            } else {
              Audio.sfx("puzzle_fail");
              showText(I18n.t("puzzle"), puz.fallimento, () => showPendulumPuzzle(pid));
            }
          }, 400);
        }
      }
      lastBeat = now;
    };
    document.getElementById("pend-cancel").onclick = close;
  }

  return {show, close, showText, showDialog, showPuzzle, showJournal, showHelp, showMenu,
          showIntro, showEnding, showFaroLit, showLockPuzzle,
          showCodex, showMap, showToast, showSecretEpilogue,
          showHint, showTutorial, showStarPuzzle, showPendulumPuzzle};
})();
