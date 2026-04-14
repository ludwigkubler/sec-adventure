// Rendering scena, hotspot, inventario. Stile minimalista, mystery mode.
const Render = (() => {
  const $bg = () => document.getElementById("bg");
  const $hot = () => document.getElementById("hotspots");
  const $log = () => document.getElementById("text-log");
  const $inv = () => document.getElementById("inventory-bar");
  const $hint = () => document.getElementById("cursor-hint");
  const $fog = () => document.getElementById("fog");

  // Posizioni anchor per le uscite (% della scena)
  const EXIT_POS = {
    nord:       {x: 50, y: 10, arrow: "↑"},
    sud:        {x: 50, y: 90, arrow: "↓"},
    est:        {x: 94, y: 50, arrow: "→"},
    ovest:      {x: 6,  y: 50, arrow: "←"},
    nordest:    {x: 88, y: 14, arrow: "↗"},
    nordovest:  {x: 12, y: 14, arrow: "↖"},
    sudest:     {x: 88, y: 86, arrow: "↘"},
    sudovest:   {x: 12, y: 86, arrow: "↙"},
    su:         {x: 94, y: 18, arrow: "▲"},
    giu:        {x: 94, y: 82, arrow: "▼"},
    dentro:     {x: 50, y: 32, arrow: "◉"},
    fuori:      {x: 50, y: 92, arrow: "○"},
    barca:      {x: 70, y: 92, arrow: "⛵"},
    nuota:      {x: 30, y: 92, arrow: "〰"},
  };

  // Hash stabile per posizionare item senza collisione
  // Se la stanza ha "room_zones" definite, usa quelle (slot semantici); altrimenti griglia.
  function posForItem(roomId, itemId, index) {
    const W = Engine.world();
    const zones = (W.room_zones || {})[roomId];
    if (zones && Array.isArray(zones.items) && zones.items.length > 0) {
      // Slot semantici, distribuiti deterministicamente
      const slot = zones.items[index % zones.items.length];
      const base = hash32(roomId + ":" + itemId);
      const jx = ((base >> 4) & 0x07) - 3;   // -3..+3
      const jy = ((base >> 11) & 0x07) - 3;
      return {x: Math.max(8, Math.min(92, slot[0] + jx)),
              y: Math.max(8, Math.min(92, slot[1] + jy))};
    }
    // Fallback griglia
    const base = hash32(roomId + ":" + itemId);
    const row = Math.floor(index / 3);
    const col = index % 3;
    const xStart = 24 + col * 22;
    const y = 62 + row * 12 + ((base & 0x0f) * 0.4);
    const xJitter = ((base >> 8) & 0x1f) * 0.3;
    return {x: Math.min(84, xStart + xJitter), y: Math.min(86, y)};
  }

  function posForNpc(roomId, npcId, index) {
    const W = Engine.world();
    const zones = (W.room_zones || {})[roomId];
    if (zones && Array.isArray(zones.npcs) && zones.npcs.length > 0) {
      const slot = zones.npcs[index % zones.npcs.length];
      return {x: slot[0], y: slot[1]};
    }
    return {x: 30 + index * 20, y: 55};
  }

  function posForExamine(roomId, key, index) {
    const base = hash32(roomId + "::" + key);
    const x = 20 + ((base & 0x3f) * 0.95);
    const y = 28 + (((base >> 6) & 0x1f) * 0.85);
    return {x: Math.max(14, Math.min(82, x)), y: Math.max(18, Math.min(60, y))};
  }

  function hash32(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = (h * 16777619) >>> 0;
    }
    return h;
  }

  let currentRoom = null;

  function drawScene(opts = {}) {
    const st = Engine.getState();
    const room = Engine.room();
    if (!room) return;

    const bg = $bg();
    const newBgUrl = `assets/rooms/${st.room}.png`;

    // Crossfade scena
    if (currentRoom !== st.room) {
      document.body.classList.add("transitioning");
      bg.classList.add("fading");
      setTimeout(() => {
        bg.style.backgroundImage = `url("${newBgUrl}"), linear-gradient(135deg, #3a2818, #1a1008)`;
        bg.classList.remove("fading");
        document.body.classList.remove("transitioning");
      }, 320);
      currentRoom = st.room;
    }

    const container = $hot();
    container.innerHTML = "";

    // Uscite (mystery mode: solo freccia, destinazione solo se visitata)
    for (const ex of Engine.roomExits(st.room)) {
      const info = EXIT_POS[ex.dir] || {x: 50, y: 50, arrow: "?"};
      const destRoom = ex.dest ? Engine.world().rooms[ex.dest] : null;
      const wouldBe = ex.wouldBe ? Engine.world().rooms[ex.wouldBe] : null;
      let tooltip;
      if (ex.blocked) {
        tooltip = wouldBe && Engine.wasVisited(ex.wouldBe)
          ? `verso ${wouldBe.nome} — bloccata`
          : "la via è bloccata";
      } else if (destRoom && Engine.wasVisited(ex.dest)) {
        tooltip = `verso ${destRoom.nome}`;
      } else {
        tooltip = "verso l'ignoto";
      }
      const h = makeHot("exit", ex.dir, info, info.arrow, tooltip);
      h.dataset.kind = "exit";
      h.dataset.dir = ex.dir;
      h.dataset.blocked = ex.blocked ? "1" : "";
      if (ex.blocked) h.classList.add("blocked");
      container.appendChild(h);
    }

    // NPC
    const npcs = Engine.roomNpcs(st.room);
    npcs.forEach((nid, i) => {
      const n = Engine.npc(nid);
      if (!n) return;
      const pos = posForNpc(st.room, nid, i);
      const img = `<img src="assets/npcs/${nid}.png" onerror="this.style.display='none'">`;
      const h = makeHot("npc", nid, pos, img, n.nome);
      h.dataset.kind = "npc";
      h.dataset.id = nid;
      container.appendChild(h);
    });

    // Items (world + extras spawnati da azioni)
    const items = [...Engine.roomItems(st.room), ...Engine.roomExtras(st.room)];
    items.forEach((iid, i) => {
      const it = Engine.item(iid);
      if (!it) return;
      const pos = posForItem(st.room, iid, i);
      const img = `<img src="assets/items/${iid}.svg" onerror="this.style.display='none'">`;
      const h = makeHot("item", iid, pos, img, it.nome_completo);
      h.dataset.kind = "item";
      h.dataset.id = iid;
      container.appendChild(h);
    });

    // Examinables
    const exs = room.esaminabili || {};
    Object.keys(exs).forEach((key, i) => {
      const pos = posForExamine(st.room, key, i);
      const h = makeHot("examine", key, pos, "◈", "osserva");
      h.dataset.kind = "examine";
      h.dataset.key = key;
      container.appendChild(h);
    });

    renderInventory();
  }

  function makeHot(type, id, pos, iconContent, label) {
    const d = document.createElement("div");
    d.className = "hotspot type-" + type;
    d.style.left = pos.x + "%";
    d.style.top = pos.y + "%";
    d.style.transform = "translate(-50%, -50%)";
    d.setAttribute("role", "button");
    d.setAttribute("tabindex", "0");
    d.setAttribute("aria-label", label);
    d.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        d.click();
      }
    });
    d.innerHTML = `<div class="icon" aria-hidden="true">${iconContent}</div><div class="label" aria-hidden="true">${escapeHtml(label)}</div>`;
    return d;
  }

  function renderInventory() {
    const st = Engine.getState();
    const inv = $inv();
    inv.innerHTML = "";
    if (st.inv.length === 0) {
      inv.innerHTML = '<div class="inv-empty">inventario vuoto</div>';
      return;
    }
    for (const iid of st.inv) {
      const it = Engine.item(iid);
      if (!it) continue;
      const slot = document.createElement("div");
      slot.className = "inv-slot" + (st.selected === iid ? " selected" : "");
      slot.dataset.id = iid;
      slot.innerHTML = `
        <img src="assets/items/${iid}.svg" alt="${escapeHtml(it.nome_completo)}" onerror="this.style.display='none'">
        <div class="inv-name">${escapeHtml(it.nome_completo)}</div>
      `;
      inv.appendChild(slot);
    }
  }

  // ─── ANIMAZIONI ───
  // Oggetto vola dalla scena all'inventario (al pickup) + particelle al punto di partenza
  function flyToInventory(fromEl, itemId) {
    if (!fromEl) return;
    const fromRect = fromEl.getBoundingClientRect();
    const inv = $inv();
    const toX = inv.getBoundingClientRect().left + 32;
    const toY = inv.getBoundingClientRect().top + 24;
    // Particelle al punto di pickup
    particleBurst(fromRect.left + fromRect.width/2, fromRect.top + fromRect.height/2, "#f0d088", 8);
    const clone = fromEl.cloneNode(true);
    clone.style.position = "fixed";
    clone.style.left = fromRect.left + "px";
    clone.style.top = fromRect.top + "px";
    clone.style.transition = "all 0.55s cubic-bezier(.55,-0.1,.4,1.4)";
    clone.style.zIndex = "300";
    clone.style.pointerEvents = "none";
    document.body.appendChild(clone);
    requestAnimationFrame(() => {
      clone.style.left = toX + "px";
      clone.style.top = toY + "px";
      clone.style.transform = "scale(0.3)";
      clone.style.opacity = "0.3";
    });
    setTimeout(() => clone.remove(), 600);
  }

  // Particelle radiali da un punto
  function particleBurst(x, y, color = "#f0b25a", count = 8) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    for (let i = 0; i < count; i++) {
      const p = document.createElement("div");
      p.className = "fx-particle";
      p.style.left = (x - 3) + "px";
      p.style.top = (y - 3) + "px";
      p.style.background = color;
      p.style.boxShadow = `0 0 8px ${color}`;
      document.body.appendChild(p);
      const angle = (i / count) * Math.PI * 2 + Math.random() * 0.3;
      const dist = 38 + Math.random() * 30;
      requestAnimationFrame(() => {
        p.style.transform = `translate(${Math.cos(angle)*dist}px, ${Math.sin(angle)*dist}px) scale(0.3)`;
        p.style.opacity = "0";
      });
      setTimeout(() => p.remove(), 700);
    }
  }
  function sparkleAt(x, y) { particleBurst(x, y, "#fff0a0", 14); }

  // Trova l'elemento DOM corrispondente a un oggetto (in inventario o nella scena)
  function findItemEl(itemId) {
    return document.querySelector(`.inv-slot[data-id="${itemId}"]`)
        || document.querySelector(`.hotspot[data-kind="item"][data-id="${itemId}"]`);
  }

  // Combine: catturo le posizioni dei due slot PRIMA che vengano rimossi.
  // Crea cloni di ICONE (per id) → volano al centro → flash → risultato vola in inv.
  function captureItemPos(itemId) {
    const el = findItemEl(itemId);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: r.left + r.width/2, y: r.top + r.height/2, w: r.width, h: r.height};
  }

  function animateCombine(srcPos1, srcPos2, srcId1, srcId2, resultId, callback) {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) { callback?.(); return; }
    if (!srcPos1 || !srcPos2) { callback?.(); return; }
    const scene = document.getElementById("scene").getBoundingClientRect();
    const cx = scene.left + scene.width / 2;
    const cy = scene.top + scene.height / 2;

    // Crea cloni "icona" basati su itemId (non clona DOM, costruisce da SVG)
    const makeIcon = (id, pos, dir) => {
      const c = document.createElement("div");
      c.style.cssText = `
        position:fixed; left:${pos.x - 27}px; top:${pos.y - 27}px;
        width:54px; height:54px; z-index:350; pointer-events:none; margin:0;
        background:rgba(20,14,8,.85); border:2px solid #f0d088; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        box-shadow:0 0 18px rgba(240,208,136,.5);
        transition:all 0.65s cubic-bezier(.4,0,.3,1);`;
      c.innerHTML = `<img src="assets/items/${id}.svg" style="width:42px;height:42px">`;
      document.body.appendChild(c);
      return {c, dir};
    };
    const clones = [
      makeIcon(srcId1, srcPos1, -1),
      makeIcon(srcId2, srcPos2, 1),
    ];

    requestAnimationFrame(() => {
      clones.forEach(({c, dir}) => {
        c.style.left = (cx - 27) + "px";
        c.style.top = (cy - 27) + "px";
        c.style.transform = `scale(1.6) rotate(${dir * 270}deg)`;
        c.style.opacity = "0.9";
      });
    });

    setTimeout(() => {
      // Flash bianco
      const flash = document.createElement("div");
      flash.className = "fx-flash";
      document.body.appendChild(flash);
      setTimeout(() => flash.remove(), 500);
      // Particelle multicolor al centro
      particleBurst(cx, cy, "#fff0a0", 16);
      particleBurst(cx, cy, "#f0b25a", 12);
      // Rimuovi i due cloni
      clones.forEach(({c}) => c.remove());

      // Risultato appare al centro e vola all'inventario
      if (resultId) {
        const result = document.createElement("div");
        result.className = "fx-result";
        result.style.cssText = `
          position:fixed; left:${cx-32}px; top:${cy-32}px; width:64px; height:64px;
          z-index:351; pointer-events:none;
          background:rgba(20,14,8,.85); border:2px solid #f0b25a; border-radius:50%;
          display:flex; align-items:center; justify-content:center;
          box-shadow: 0 0 30px #f0b25a, 0 0 60px rgba(240,178,90,.5);
          opacity:0; transform:scale(0.3);
          transition: all 0.4s cubic-bezier(.2,.8,.3,1.4);
        `;
        result.innerHTML = `<img src="assets/items/${resultId}.svg" style="width:48px;height:48px">`;
        document.body.appendChild(result);
        requestAnimationFrame(() => {
          result.style.opacity = "1";
          result.style.transform = "scale(1.1)";
        });
        setTimeout(() => {
          const inv = $inv().getBoundingClientRect();
          result.style.transition = "all 0.55s cubic-bezier(.55,-0.1,.4,1.4)";
          result.style.left = (inv.left + 30) + "px";
          result.style.top = (inv.top + 24) + "px";
          result.style.transform = "scale(0.4)";
          result.style.opacity = "0.4";
          result.style.boxShadow = "none";
          setTimeout(() => result.remove(), 600);
        }, 550);
      }
      callback?.();
    }, 700);
  }

  // Use-on-target: oggetto vola da posizione catturata al target con sparkle finale
  // srcPos = {x,y} catturato PRIMA di useOn (perché l'inv potrebbe essere ri-renderizzato)
  function animateUseOn(srcPos, srcItemId, targetEl, callback) {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) { callback?.(); return; }
    if (!srcPos || !targetEl) { callback?.(); return; }
    const tgt = targetEl.getBoundingClientRect();
    const tx = tgt.left + tgt.width / 2;
    const ty = tgt.top + tgt.height / 2;

    const clone = document.createElement("div");
    clone.style.cssText = `
      position:fixed; left:${srcPos.x - 24}px; top:${srcPos.y - 24}px;
      width:48px; height:48px; z-index:350; pointer-events:none; margin:0;
      background:rgba(20,14,8,.85); border:2px solid #f0d088; border-radius:6px;
      display:flex; align-items:center; justify-content:center;
      box-shadow:0 0 18px rgba(240,208,136,.6);
      transition:all 0.55s cubic-bezier(.3,0,.5,1);`;
    clone.innerHTML = `<img src="assets/items/${srcItemId}.svg" style="width:36px;height:36px">`;
    document.body.appendChild(clone);

    requestAnimationFrame(() => {
      clone.style.left = (tx - 25) + "px";
      clone.style.top = (ty - 25) + "px";
      clone.style.transform = "scale(1.5) rotate(20deg)";
    });
    setTimeout(() => {
      sparkleAt(tx, ty);
      clone.style.transition = "all 0.3s ease-out";
      clone.style.transform = "scale(2.2) rotate(40deg)";
      clone.style.opacity = "0";
      setTimeout(() => clone.remove(), 320);
      callback?.();
    }, 550);
  }
  // Espongo captureItemPos
  function getCapture(itemId) { return captureItemPos(itemId); }

  function logLine(text, cls = "narrative") {
    const log = $log();
    const d = document.createElement("div");
    d.className = "line " + cls + " enter";
    d.innerHTML = formatText(text);
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
    while (log.children.length > 60) log.removeChild(log.firstChild);
    requestAnimationFrame(() => d.classList.remove("enter"));
  }

  function logTitle(text) { logLine(text, "title"); }
  function logSystem(text) { logLine(text, "system"); }

  function formatText(t) {
    return escapeHtml(t).replace(/\n\n/g, "<br><br>").replace(/\n/g, "<br>");
  }
  function escapeHtml(s) {
    return String(s).replace(/[<>&"]/g, c => ({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"}[c]));
  }

  function showHint(txt, ev) {
    const hint = $hint();
    hint.textContent = txt;
    hint.style.display = "block";
    hint.style.left = (ev.clientX + 14) + "px";
    hint.style.top = (ev.clientY + 14) + "px";
  }
  function hideHint() { $hint().style.display = "none"; }

  // Cursore contestuale
  function setCursor(mode) {
    const g = document.getElementById("game");
    g.classList.remove("cur-use", "cur-combine");
    if (mode === "use") g.classList.add("cur-use");
  }

  return {drawScene, renderInventory, logLine, logTitle, logSystem, showHint, hideHint,
          flyToInventory, animateCombine, animateUseOn, captureItemPos: getCapture,
          particleBurst, sparkleAt, setCursor};
})();
