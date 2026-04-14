// Bootstrap con i18n e HUD speedrun.
(async () => {
  // Carica la lingua corrente e il world localizzato
  const lang = I18n.getLang();
  const worldFile = lang === "en" ? "data/world.en.json" : "data/world.json";
  const resp = await fetch(worldFile);
  if (!resp.ok) {
    const fb = await fetch("data/world.json");
    if (!fb.ok) { document.body.innerHTML = "<pre>Error loading world.json</pre>"; return; }
    const world = await fb.json();
    initGame(world);
  } else {
    const world = await resp.json();
    initGame(world);
  }

  function initGame(world) {
    Engine.init(world);
    Input.wire();
    applyUIStrings();

    const title = document.getElementById("title-screen");
    const btnNew = document.getElementById("btn-new");
    const btnCont = document.getElementById("btn-continue");
    btnCont.disabled = !Engine.hasSave();

    btnNew.onclick = () => {
      Audio.resume();
      Engine.reset();
      Engine.startTimer();
      title.classList.add("hidden");
      UI.showIntro(world.intro, () => {
        Render.drawScene();
        Audio.setRoom(Engine.getState().room);
        Input.showSceneTitle();
        Input.describeRoom();
        if (!localStorage.getItem("isola_tutorial_seen")) {
          setTimeout(() => UI.showTutorial(), 800);
          localStorage.setItem("isola_tutorial_seen", "1");
        } else {
          setTimeout(() => Render.logSystem(I18n.t("hint_btn") + ": T/C/J/H/M/L/?/ESC"), 1500);
        }
      });
    };
    btnCont.onclick = () => {
      Audio.resume();
      if (!Engine.load()) return;
      Engine.startTimer();
      title.classList.add("hidden");
      Render.drawScene();
      Audio.setRoom(Engine.getState().room);
      Input.showSceneTitle();
      Input.describeRoom();
      Render.logSystem(I18n.t("save_loaded"));
    };

    // Autosave: salva SOLO quando il title-screen è nascosto (cioè durante il gioco)
    setInterval(() => {
      if (document.getElementById("title-screen").classList.contains("hidden")) {
        Engine.save();
      }
    }, 25000);

    // HUD timer + completion %
    setInterval(updateHud, 1000);
    updateHud();

    // Eventi engine
    Engine.on((ev) => {
      if (ev.type === "take" || ev.type === "inv" || ev.type === "select") {
        Render.renderInventory();
      }
      if (ev.type === "moved") updateHud();
      if (ev.type === "codex_found") {
        Audio.sfx("discovery");
        UI.showToast({title: `+1 Codex (${ev.found}/${ev.total})`,
                      body: ev.lore.nome, kind: "codex"});
      }
      if (ev.type === "achievement") {
        Audio.sfx(ev.id === "codex_completo" ? "fanfare" : "discovery");
        UI.showToast({title: ev.title, body: ev.desc, kind: "achievement"});
      }
      if (ev.type === "faro_acceso") {
        Engine.unlockAchievement("faro_acceso",
          lang === "en" ? "Ancient Light" : "Lume Antico",
          lang === "en" ? "You lit the ancient lighthouse." : "Hai acceso il faro antico.");
        Render.logTitle(lang === "en" ? "⚡ The ancient lighthouse awakens ⚡" : "⚡ Il faro antico si accende ⚡");
        Render.logLine(lang === "en"
          ? "Three components, three eras, three powers. Light tears the sky for the first time in centuries — but it does not only descend toward the sea. The stone floor of the lighthouse also trembles, and something opens beneath."
          : "Tre componenti, tre ere, tre poteri. La luce squarcia il cielo per la prima volta dopo secoli — ma la luce non scende solo verso il mare. Anche il pavimento di pietra del faro vibra, e qualcosa si apre sotto di esso.");
        setTimeout(() => UI.showFaroLit(world.finale), 1800);
      }
      if (ev.type === "ending_atto_ii") {
        Engine.unlockAchievement("corona_indossata",
          lang === "en" ? "Custodian of the Tree" : "Custode dell'Albero",
          lang === "en" ? "You wore the Titanic Crown." : "Hai indossato la Corona Titanica.");
        Render.logTitle(lang === "en" ? "✦ The Crown ✦" : "✦ La Corona ✦");
        setTimeout(() => {
          UI.showEnding(world.finale_atto_ii || world.finale);
          if (Engine.getState().flags.codex_completo) {
            setTimeout(() => UI.showSecretEpilogue(world.epilogo_segreto || ""), 800);
          }
        }, 1500);
      }
    });
  }

  function applyUIStrings() {
    // Title screen
    document.querySelector("#title-screen h1").textContent = "L'Isola del Naufragio";
    const subs = document.querySelector("#title-screen .subtitle");
    if (subs) subs.textContent = I18n.t("subtitle");
    const credits = document.querySelector("#title-screen .credits");
    if (credits) credits.textContent = I18n.t("credits");
    document.getElementById("btn-new").textContent = I18n.t("new_game");
    document.getElementById("btn-continue").textContent = I18n.t("continue");
  }

  function updateHud() {
    const st = Engine.getState();
    if (!st) return;
    const t = Engine.getElapsedSeconds();
    const m = String(Math.floor(t / 60)).padStart(2, "0");
    const s = String(t % 60).padStart(2, "0");
    const visited = Object.keys(st.visited || {}).length;
    const total = Object.keys(Engine.world().rooms).length;
    const codex = Engine.codexState();
    // Completamento: 40% esplorazione + 40% codex + 20% faro/corona
    const expPct = visited / total;
    const codPct = codex.total ? codex.found / codex.total : 0;
    const endPct = (st.flags.faro_acceso ? 0.5 : 0) + (st.flags.corona_indossata ? 0.5 : 0);
    const pct = Math.round((expPct*0.4 + codPct*0.4 + endPct*0.2) * 100);
    document.getElementById("hud-time").textContent = `⏱ ${m}:${s}`;
    document.getElementById("hud-rooms").textContent = `🏠 ${visited}/${total}`;
    document.getElementById("hud-pct").textContent = `✦ ${pct}%`;
  }

  // Language toggle global
  window.toggleLang = async () => {
    const cur = I18n.getLang();
    const next = cur === "it" ? "en" : "it";
    await I18n.setLang(next);
    location.reload();
  };
})();
