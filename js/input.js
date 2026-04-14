// Gestione click + tastiera + audio feedback.
const Input = (() => {
  let lastHover = null;
  let busy = false;
  const withBusy = (ms, fn) => {
    if (busy) return;
    busy = true;
    try { fn(); } finally { setTimeout(() => { busy = false; }, ms); }
  };

  function wire() {
    const hot = document.getElementById("hotspots");
    hot.addEventListener("click", onHotspotClick);
    hot.addEventListener("mousemove", onHotspotHover);
    hot.addEventListener("mouseleave", () => { Render.hideHint(); lastHover = null; });

    const inv = document.getElementById("inventory-bar");
    inv.addEventListener("click", onInventoryClick);

    document.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      if (Engine.getState().selected) {
        Engine.deselect();
        Render.renderInventory();
        Render.setCursor("none");
        Audio.sfx("select");
        Render.logSystem("Deselezionato.");
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT") return;
      if (e.key === "Escape") {
        const m = document.getElementById("modal");
        if (!m.classList.contains("hidden")) { UI.close(); return; }
        if (Engine.getState().selected) {
          Engine.deselect(); Render.renderInventory(); Render.setCursor("none");
        }
      }
      if (e.key === "j" || e.key === "J") UI.showJournal();
      if (e.key === "c" || e.key === "C") UI.showCodex();
      if (e.key === "t" || e.key === "T") UI.showMap();
      if (e.key === "h" || e.key === "H") UI.showHint();
      if (e.key === "l" || e.key === "L") window.toggleLang && window.toggleLang();
      if (e.key === "?") UI.showHelp();
      if (e.key === "m" || e.key === "M") {
        const muted = Audio.toggleMute();
        document.getElementById("btn-mute").textContent = muted ? "🔇" : "🔊";
        Render.logSystem(muted ? "Audio disattivato." : "Audio riattivato.");
      }
      if ((e.key === "s" && e.ctrlKey)) {
        e.preventDefault(); Engine.save(); Render.logSystem("Partita salvata.");
      }
    });

    // Topbar
    document.getElementById("btn-journal").onclick = () => UI.showJournal();
    document.getElementById("btn-codex").onclick = () => UI.showCodex();
    document.getElementById("btn-map").onclick = () => UI.showMap();
    document.getElementById("btn-help").onclick = () => UI.showHelp();
    document.getElementById("btn-menu").onclick = () => UI.showMenu();
    const hintBtn = document.getElementById("btn-hint");
    if (hintBtn) hintBtn.onclick = () => UI.showHint();
    const langBtn = document.getElementById("btn-lang");
    if (langBtn) langBtn.onclick = () => window.toggleLang && window.toggleLang();
    document.getElementById("btn-mute").onclick = () => {
      const muted = Audio.toggleMute();
      document.getElementById("btn-mute").textContent = muted ? "🔇" : "🔊";
    };
  }

  function onHotspotHover(e) {
    const hs = e.target.closest(".hotspot");
    if (!hs) { Render.hideHint(); lastHover = null; return; }
    if (hs !== lastHover) {
      Audio.sfx("hover");
      lastHover = hs;
    }
    const label = hs.querySelector(".label")?.textContent;
    if (label) Render.showHint(label, e);
    else Render.hideHint();
  }

  function onHotspotClick(e) {
    if (busy) return;
    const hs = e.target.closest(".hotspot");
    if (!hs) return;
    Audio.resume();
    const kind = hs.dataset.kind;
    const st = Engine.getState();
    const selected = st.selected;

    if (kind === "exit") {
      const dir = hs.dataset.dir;
      if (selected) {
        const srcPos = Render.captureItemPos(selected);
        const res = Engine.useOn(selected, {kind: "exit", dir});
        if (res.ok) {
          Audio.sfx("door");
          withBusy(700, () => {
            Render.animateUseOn(srcPos, selected, hs, () => {
              Render.logLine(res.msg);
              Engine.deselect(); Render.setCursor("none");
              Render.drawScene();
              Audio.setRoom(Engine.getState().room);
              showSceneTitle();
              describeRoom();
            });
          });
        } else {
          Audio.sfx("fail");
          Render.logSystem(res.msg);
        }
        return;
      }
      const res = Engine.tryExit(dir);
      if (res.ok) {
        Audio.sfx("door");
        withBusy(400, () => {
          Render.logLine(res.msg);
          Render.drawScene();
          Audio.setRoom(Engine.getState().room);
          showSceneTitle();
          describeRoom();
        });
      } else {
        Audio.sfx("fail");
        Render.logSystem(res.msg);
      }
      return;
    }

    if (kind === "item") {
      const id = hs.dataset.id;
      if (selected) {
        const res = Engine.useOn(selected, {kind: "item", id});
        if (res.ok) {
          Audio.sfxItem("combine", id);
          Render.logLine(res.msg);
          Engine.deselect(); Render.setCursor("none");
        } else {
          Audio.sfx("fail");
          Render.logSystem(res.msg);
        }
        Render.drawScene();
        return;
      }
      Render.flyToInventory(hs, id);
      const res = Engine.takeItem(id);
      if (res.ok) Audio.sfxItem("pickup", id); else Audio.sfx("fail");
      Render.logLine(res.msg, res.ok ? "narrative" : "system");
      setTimeout(() => Render.drawScene(), 200);
      return;
    }

    if (kind === "npc") {
      const nid = hs.dataset.id;
      Audio.sfx("click");
      if (selected) {
        const srcPos = Render.captureItemPos(selected);
        const res = Engine.useOn(selected, {kind: "npc", id: nid});
        if (res.ok) {
          Audio.sfxItem("use", selected);
          Engine.deselect(); Render.setCursor("none");
          Render.animateUseOn(srcPos, selected, hs, () => {
            UI.showText(Engine.npc(nid).nome, res.msg);
            Render.drawScene();
          });
        } else {
          Audio.sfx("fail");
          Render.logSystem(res.msg);
        }
        return;
      }
      UI.showDialog(nid);
      return;
    }

    if (kind === "examine") {
      const key = hs.dataset.key;
      Audio.sfx("click");
      if (selected) {
        const srcPos = Render.captureItemPos(selected);
        const itName = Engine.item(selected).nome_completo;
        const res = Engine.useOn(selected, {kind: "examine", key});
        if (res.ok) {
          // Suono speciale dell'azione (es. wall_break) o suono materiale standard
          if (res.audio) Audio.sfx(res.audio);
          else Audio.sfxItem("use", selected);
          Engine.deselect(); Render.setCursor("none");
          Render.animateUseOn(srcPos, selected, hs, () => {
            UI.showText("Usi " + itName, res.msg);
            Render.drawScene();
          });
        } else {
          Audio.sfx("fail");
          Render.logSystem(res.msg);
        }
        return;
      }
      // Trigger di puzzle interattivo: se l'examine corrisponde a un puzzle nella stanza corrente
      const ip = Engine.world().puzzles_interactive || {};
      const room = Engine.getState().room;
      for (const [pid, p] of Object.entries(ip)) {
        if (p.stanza === room && p.trigger_examine === key) {
          if (p.flag && Engine.getState().flags[p.flag]) {
            UI.showText(key, I18n.getLang()==="en" ? "Already solved." : "Già risolto.");
          } else {
            if (p.tipo === "lucchetto") UI.showLockPuzzle(pid);
            else if (p.tipo === "stelle") UI.showStarPuzzle(pid);
            else if (p.tipo === "pendolo") UI.showPendulumPuzzle(pid);
          }
          return;
        }
      }
      const res = Engine.examine(key);
      UI.showText(key, res.msg);
      return;
    }
  }

  function onInventoryClick(e) {
    if (busy) return;
    const slot = e.target.closest(".inv-slot");
    if (!slot) return;
    Audio.resume();
    const id = slot.dataset.id;
    const st = Engine.getState();

    // Caso 1: c'è già un oggetto selezionato e clicco un ALTRO oggetto in inventario → COMBINA
    if (st.selected && st.selected !== id) {
      const sel = st.selected;
      const pos1 = Render.captureItemPos(sel);
      const pos2 = Render.captureItemPos(id);
      const res = Engine.useOn(sel, {kind: "item", id});
      if (res.ok) {
        Audio.sfx("fusion");
        Engine.deselect();
        Render.setCursor("none");
        Render.renderInventory();
        withBusy(900, () => {
          Render.animateCombine(pos1, pos2, sel, id, res.result, () => {
            Audio.sfxItem("combine", res.result);
            Render.logLine(res.msg);
          });
        });
      } else {
        Audio.sfx("fail");
        Render.logSystem(res.msg);
        Render.renderInventory();
      }
      return;
    }

    // Caso 2: clicco l'oggetto già selezionato → DESELEZIONA
    if (st.selected === id) {
      Engine.deselect();
      Render.setCursor("none");
      Audio.sfx("select");
      Render.renderInventory();
      return;
    }

    // Caso 3: nessuno selezionato → SELEZIONA, oppure SHIFT+click → ESAMINA
    if (e.shiftKey || e.ctrlKey) {
      const it = Engine.item(id);
      Audio.sfx("click");
      UI.showText(it.nome_completo, it.descrizione || "Niente di particolare.");
      return;
    }
    Engine.select(id);
    Render.setCursor("use");
    Audio.sfx("select");
    Render.logSystem(`Selezionato "${Engine.item(id).nome_completo}". Per COMBINARE: clicca un altro oggetto in inventario. Per USARE: clicca un personaggio, una porta, un dettaglio. (shift+click = esamina, click destro = deseleziona)`);
    Render.renderInventory();
  }

  function describeRoom() {
    const r = Engine.room();
    Render.logTitle(r.nome);
    const st = Engine.getState();
    // Prima volta: descrizione lunga; visite successive: breve
    const isFirst = !st._described?.[Engine.getState().room];
    if (!st._described) st._described = {};
    st._described[Engine.getState().room] = true;
    const txt = isFirst ? r.descrizione : (r.descrizione_breve || r.descrizione);
    Render.logLine(txt);
  }

  function showSceneTitle() {
    const t = document.getElementById("scene-title");
    t.textContent = Engine.room().nome;
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 2400);
  }

  return {wire, describeRoom, showSceneTitle};
})();
