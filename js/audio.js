// Audio procedurale: musica ambient per bioma + SFX. Solo Web Audio API, zero file.
const Audio = (() => {
  let ctx = null;
  let masterGain = null;
  let musicGain = null;
  let sfxGain = null;
  let currentAmbient = null;
  let muted = false;

  let compressor = null;
  let sharedNoiseBuffer = null;
  function ensure() {
    if (ctx) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    // DynamicsCompressor tra master e destination: evita clipping in fanfare/ending/wall_break
    compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -20;
    compressor.knee.value = 8;
    compressor.ratio.value = 4;
    compressor.attack.value = 0.005;
    compressor.release.value = 0.12;
    compressor.connect(ctx.destination);
    masterGain = ctx.createGain();
    masterGain.gain.value = 0.7;
    masterGain.connect(compressor);
    musicGain = ctx.createGain();
    musicGain.gain.value = 0.35;
    musicGain.connect(masterGain);
    sfxGain = ctx.createGain();
    sfxGain.gain.value = 0.55;
    sfxGain.connect(masterGain);
    // Shared noise buffer (4s): unica allocazione per tutta la sessione (~768KB)
    const len = ctx.sampleRate * 4;
    sharedNoiseBuffer = ctx.createBuffer(1, len, ctx.sampleRate);
    const data = sharedNoiseBuffer.getChannelData(0);
    for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * 0.5;
  }
  function resume() {
    ensure();
    if (ctx.state === "suspended") ctx.resume();
  }

  // Mappa bioma → preset musicale
  // Ogni preset: array di frequenze base + parametri di filtro/movimento
  const BIOMI = {
    spiaggia:   {freqs:[110, 165, 220], cutoff:1200, lfoRate:0.07, type:"sine",   noise:0.04, name:"onda"},
    caletta:    {freqs:[98, 147, 196],  cutoff:900,  lfoRate:0.05, type:"sine",   noise:0.05, name:"caletta"},
    grotte:     {freqs:[55, 82.4, 110], cutoff:380,  lfoRate:0.04, type:"sine",   noise:0.06, name:"grotte"},
    tempio_sommerso:{freqs:[65, 98, 130], cutoff:520, lfoRate:0.03, type:"triangle", noise:0.03, name:"tempio"},
    foresta:    {freqs:[146, 220, 293], cutoff:1500, lfoRate:0.09, type:"sawtooth", noise:0.08, name:"foresta"},
    radura:     {freqs:[174, 261, 349], cutoff:1700, lfoRate:0.08, type:"sine",   noise:0.06, name:"radura"},
    scogliere_sud:{freqs:[110, 174, 220], cutoff:1100, lfoRate:0.10, type:"sine", noise:0.07, name:"vento"},
    villaggio:  {freqs:[196, 261, 392], cutoff:1800, lfoRate:0.06, type:"triangle", noise:0.04, name:"villaggio"},
    molo:       {freqs:[123, 185, 247], cutoff:1000, lfoRate:0.05, type:"sine",   noise:0.05, name:"molo"},
    giungla:    {freqs:[130, 196, 261], cutoff:1300, lfoRate:0.08, type:"sawtooth", noise:0.10, name:"giungla"},
    giungla_profonda:{freqs:[87, 130, 174], cutoff:700, lfoRate:0.04, type:"sawtooth", noise:0.12, name:"profondo"},
    capanna_luna:{freqs:[155, 233, 311], cutoff:1400, lfoRate:0.05, type:"sine", noise:0.03, name:"sciamana"},
    // Sentiero montagna: aria rarefatta, quarta sopra a spiaggia — distinto armonicamente
    sentiero_montagna:{freqs:[138, 207, 277, 415], cutoff:2200, lfoRate:0.14, type:"triangle", noise:0.03, name:"vetta"},
    cima_vulcano:{freqs:[55, 73.4, 110], cutoff:600, lfoRate:0.04, type:"sawtooth", noise:0.15, name:"vulcano"},
    scogliere:  {freqs:[98, 147, 196], cutoff:1100, lfoRate:0.10, type:"sine", noise:0.07, name:"scogliere"},
    faro:       {freqs:[82.4, 123, 165], cutoff:850, lfoRate:0.04, type:"triangle", noise:0.04, name:"faro"},
    rovine:     {freqs:[65, 98, 146], cutoff:600, lfoRate:0.03, type:"sawtooth", noise:0.05, name:"rovine"},
    sala_guardiano:{freqs:[73, 110, 165], cutoff:700, lfoRate:0.025, type:"sine", noise:0.03, name:"guardiano"},
    cripta:     {freqs:[58, 87, 116], cutoff:450, lfoRate:0.03, type:"sawtooth", noise:0.05, name:"cripta"},
    // Laguna: fifth inferiore rispetto a radura, texture glass-like, più spaziale
    laguna:     {freqs:[116, 174, 233, 349], cutoff:2000, lfoRate:0.05, type:"triangle", noise:0.03, name:"laguna"},
    // ─── Atto II — biomi sotterranei ───
    pozzo_faro:       {freqs:[55, 73.4, 110], cutoff:500, lfoRate:0.025, type:"triangle", noise:0.06, name:"pozzo"},
    cripta_meccanica: {freqs:[65, 98, 130, 195], cutoff:700, lfoRate:0.06, type:"square", noise:0.04, name:"meccanica"},
    sala_ingranaggi:  {freqs:[55, 73.4, 110, 165, 220], cutoff:1100, lfoRate:0.12, type:"square", noise:0.07, name:"ingranaggi"},
    corridoio_vapore: {freqs:[110, 165, 220], cutoff:1800, lfoRate:0.18, type:"sawtooth", noise:0.18, name:"vapore"},
    forgia_antica:    {freqs:[82.4, 123, 165, 220], cutoff:900, lfoRate:0.08, type:"sawtooth", noise:0.12, name:"forgia"},
    archivio:         {freqs:[131, 196, 262, 392], cutoff:1400, lfoRate:0.04, type:"sine", noise:0.02, name:"archivio"},
    osservatorio:     {freqs:[174, 261, 349, 523], cutoff:1700, lfoRate:0.05, type:"triangle", noise:0.03, name:"stelle"},
    cuore_macchina:   {freqs:[55, 82.4, 110, 165], cutoff:600, lfoRate:0.025, type:"sine", noise:0.04, name:"cuore"},
    agora_perduta:    {freqs:[98, 147, 196, 294], cutoff:1100, lfoRate:0.04, type:"triangle", noise:0.05, name:"agora"},
    via_titani:       {freqs:[73.4, 110, 165, 220], cutoff:900, lfoRate:0.04, type:"sine", noise:0.04, name:"titani"},
    abisso:           {freqs:[41, 65, 87], cutoff:380, lfoRate:0.02, type:"sawtooth", noise:0.10, name:"abisso"},
    radice_mondo:     {freqs:[110, 165, 220, 330, 440, 660], cutoff:2200, lfoRate:0.05, type:"sine", noise:0.02, name:"radice"},
  };

  function buildAmbient(preset) {
    const out = ctx.createGain();
    out.gain.value = 0;

    // Filtro lowpass condiviso
    const filter = ctx.createBiquadFilter();
    filter.type = "lowpass";
    filter.frequency.value = preset.cutoff;
    filter.Q.value = 1.4;
    filter.connect(out);

    const oscs = [];
    const lfos = [];

    preset.freqs.forEach((f, i) => {
      const osc = ctx.createOscillator();
      osc.type = preset.type;
      osc.frequency.value = f;

      const oscGain = ctx.createGain();
      oscGain.gain.value = 0.18 / (i + 1);
      osc.connect(oscGain).connect(filter);

      // LFO sulla detune per dare movimento
      const lfo = ctx.createOscillator();
      lfo.type = "sine";
      lfo.frequency.value = preset.lfoRate * (1 + i * 0.3);
      const lfoGain = ctx.createGain();
      lfoGain.gain.value = 6 + i * 2;
      lfo.connect(lfoGain).connect(osc.detune);

      // LFO sull'ampiezza
      const ampLfo = ctx.createOscillator();
      ampLfo.type = "sine";
      ampLfo.frequency.value = preset.lfoRate * 0.5;
      const ampLfoGain = ctx.createGain();
      ampLfoGain.gain.value = 0.04;
      ampLfo.connect(ampLfoGain).connect(oscGain.gain);

      osc.start();
      lfo.start();
      ampLfo.start();
      oscs.push(osc);
      lfos.push(lfo, ampLfo);
    });

    // Strato di noise filtrato — usa il buffer condiviso (unica allocazione per sessione)
    if (preset.noise > 0 && sharedNoiseBuffer) {
      const noiseSrc = ctx.createBufferSource();
      noiseSrc.buffer = sharedNoiseBuffer;
      noiseSrc.loop = true;
      const noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = "bandpass";
      noiseFilter.frequency.value = preset.cutoff * 0.8;
      noiseFilter.Q.value = 0.6;
      const noiseGain = ctx.createGain();
      noiseGain.gain.value = preset.noise;
      noiseSrc.connect(noiseFilter).connect(noiseGain).connect(out);
      noiseSrc.start();
      oscs.push(noiseSrc);
    }

    out.connect(musicGain);
    return {out, stop: () => {
      try {
        const t = ctx.currentTime;
        out.gain.cancelScheduledValues(t);
        out.gain.setValueAtTime(out.gain.value, t);
        out.gain.linearRampToValueAtTime(0, t + 1.2);
        setTimeout(() => {
          oscs.forEach(o => { try { o.stop(); } catch(e){} });
          out.disconnect();
        }, 1400);
      } catch(e) {}
    }};
  }

  function setRoom(roomId) {
    if (muted) return;
    ensure();
    const preset = BIOMI[roomId] || BIOMI.spiaggia;
    if (currentAmbient) currentAmbient.stop();
    const a = buildAmbient(preset);
    currentAmbient = a;
    const t = ctx.currentTime;
    a.out.gain.setValueAtTime(0, t);
    a.out.gain.linearRampToValueAtTime(0.85, t + 1.5);
  }

  // ---- SFX ----
  function envOsc({type="sine", freq, freq2, dur=0.18, attack=0.005, gain=0.4}) {
    const o = ctx.createOscillator();
    o.type = type;
    o.frequency.value = freq;
    if (freq2 !== undefined) {
      o.frequency.setValueAtTime(freq, ctx.currentTime);
      o.frequency.exponentialRampToValueAtTime(freq2, ctx.currentTime + dur);
    }
    const g = ctx.createGain();
    g.gain.value = 0;
    o.connect(g).connect(sfxGain);
    const t = ctx.currentTime;
    g.gain.linearRampToValueAtTime(gain, t + attack);
    g.gain.exponentialRampToValueAtTime(0.001, t + dur);
    o.start(t);
    o.stop(t + dur + 0.05);
  }

  function noiseBurst({dur=0.12, gain=0.3, cutoff=2000}) {
    const buf = ctx.createBuffer(1, ctx.sampleRate * dur, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const f = ctx.createBiquadFilter();
    f.type = "lowpass";
    f.frequency.value = cutoff;
    const g = ctx.createGain();
    g.gain.value = gain;
    src.connect(f).connect(g).connect(sfxGain);
    // Cleanup esplicito a fine playback: libera grafo audio
    src.onended = () => { try { src.disconnect(); f.disconnect(); g.disconnect(); } catch(e){} };
    src.start();
  }

  // Subtitle opzionali per SFX narrativi (accessibility)
  const SFX_SUBTITLES = {
    door:        {it: "[porta che si apre]", en: "[door opens]"},
    wall_break:  {it: "[muro che crolla]",  en: "[wall collapses]"},
    fusion:      {it: "[oggetti che si fondono]", en: "[items fusing]"},
    pickup:      {it: "[raccolto]", en: "[picked up]"},
    combine:     {it: "[combinato]", en: "[combined]"},
    puzzle_ok:   {it: "[enigma risolto]", en: "[puzzle solved]"},
    puzzle_fail: {it: "[enigma sbagliato]", en: "[puzzle wrong]"},
    fanfare:     {it: "[fanfara]", en: "[fanfare]"},
    ending:      {it: "[finale]", en: "[ending]"},
    discovery:   {it: "[scoperta]", en: "[discovery]"},
    fail:        {it: "[niente]", en: "[nothing happens]"},
  };
  let captionsOn = localStorage.getItem("isola_captions") === "1";
  function toggleCaptions() {
    captionsOn = !captionsOn;
    localStorage.setItem("isola_captions", captionsOn ? "1" : "0");
    return captionsOn;
  }
  function captionsEnabled() { return captionsOn; }
  function emitCaption(name) {
    if (!captionsOn) return;
    const sub = SFX_SUBTITLES[name];
    if (!sub) return;
    const lang = (window.I18n && I18n.getLang()) || "it";
    const txt = sub[lang] || sub.it;
    if (window.Render && Render.logSystem) Render.logSystem(txt);
  }

  function sfx(name) {
    emitCaption(name);
    if (muted || !ctx) return;
    resume();
    switch (name) {
      case "click":   envOsc({type:"sine", freq:880, freq2:660, dur:0.05, gain:0.18}); break;
      case "hover":   envOsc({type:"sine", freq:1320, dur:0.04, gain:0.06}); break;
      case "pickup":  envOsc({type:"triangle", freq:440, freq2:880, dur:0.18, gain:0.32});
                      setTimeout(()=>envOsc({type:"sine", freq:1320, dur:0.12, gain:0.18}), 90); break;
      case "fail":    envOsc({type:"sawtooth", freq:200, freq2:120, dur:0.22, gain:0.25}); break;
      case "door":    noiseBurst({dur:0.4, gain:0.25, cutoff:600});
                      envOsc({type:"sine", freq:90, freq2:50, dur:0.5, gain:0.4}); break;
      case "combine": envOsc({type:"triangle", freq:330, freq2:660, dur:0.12, gain:0.22});
                      setTimeout(()=>envOsc({type:"sine", freq:880, freq2:1320, dur:0.18, gain:0.22}), 100);
                      setTimeout(()=>envOsc({type:"sine", freq:1760, dur:0.18, gain:0.22}), 220); break;
      case "puzzle_ok": [523, 659, 784, 1047].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"triangle", freq:f, dur:0.22, gain:0.28}), i*120)); break;
      case "puzzle_fail": [330, 277, 220].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"sawtooth", freq:f, dur:0.25, gain:0.24}), i*150)); break;
      case "ending":  for (let i = 0; i < 8; i++)
                        setTimeout(() => envOsc({type:"triangle", freq:440 + i*55, dur:1.2, gain:0.24}), i * 180);
                      break;
      case "select":  envOsc({type:"square", freq:660, dur:0.05, gain:0.12}); break;
      case "discovery":
                      // Trillo cristallino veloce
                      [1320, 1760, 2349, 2637].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"sine", freq:f, dur:0.18, gain:0.20}), i*60));
                      break;
      case "fanfare":
                      [523, 659, 784, 1047, 1319, 1568, 2093].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"triangle", freq:f, dur:0.55, gain:0.22}), i*100));
                      setTimeout(()=>{ for (let i = 0; i < 4; i++)
                        envOsc({type:"sine", freq:1047 + i*523, dur:1.5, gain:0.12}); }, 800);
                      break;
      case "fusion":
                      // Whoosh ascendente + chime trasformazione + flash sonoro
                      noiseBurst({dur:0.25, gain:0.20, cutoff:3000});
                      [330, 523, 784, 1175].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"triangle", freq:f, freq2:f*2, dur:0.18, gain:0.22}), i*70));
                      setTimeout(()=>envOsc({type:"sine", freq:2349, dur:0.45, gain:0.16}), 320);
                      setTimeout(()=>envOsc({type:"sine", freq:1760, dur:0.55, gain:0.12}), 380);
                      break;
      case "sparkle":
                      // Pip cristallino veloce per use-on-target
                      [1760, 2349, 2637, 3136].forEach((f,i) =>
                        setTimeout(()=>envOsc({type:"sine", freq:f, dur:0.10, gain:0.16}), i*30));
                      break;
      case "wall_break":
                      // Thud + crollo
                      envOsc({type:"sawtooth", freq:80, freq2:50, dur:0.15, gain:0.42});
                      noiseBurst({dur:0.45, gain:0.30, cutoff:1200});
                      setTimeout(()=>noiseBurst({dur:0.35, gain:0.20, cutoff:600}), 180);
                      setTimeout(()=>envOsc({type:"sine", freq:60, freq2:40, dur:0.5, gain:0.30}), 100);
                      break;
      case "particle":
                      envOsc({type:"sine", freq:2349, dur:0.05, gain:0.10});
                      break;
    }
  }

  // ─── Suoni per materiale (categorizzazione oggetti) ───
  const MATERIALS = {
    wood:    ["legna","ramo_robusto","torcia","piccone","tavoletta_antica","ruota_dentata","leva_ottone"],
    cord:    ["corda","rete_pesca","cintura_cuoio","funi_metalliche"],
    glass:   ["bottiglia","messaggio_bottiglia","ampolla","lente_smeraldo","sfera_cristallo"],
    stone:   ["pietra_focaia","frammento_mappa","sigillo_antico","tavoletta_runica"],
    metal:   ["lama_antica","chiodi_arrugginiti","chiave_faro","chiave_antica","machete","ingranaggio","pendolo_ottone","martello_rame","binario_ferro","valvola_vapore","manovella","catena_oro"],
    organic: ["bacche","fiori","erbe_secche","pianta_rara","resina","olio_vegetale","antidoto","spore_lumino","muschio_blu","radice_madre"],
    mystic:  ["artefatto_sacro","medaglione","gemma_potere","cristallo_vulcanico","perla_nera","tridente","corona_corallo","attrezzatura_sub","conchiglia","diario_guardiano","cuore_macchina","occhio_titano","cristallo_radice","sigillo_re","frammento_stella","corona_titanica"],
  };
  const MAT_INDEX = {};
  for (const [m, ids] of Object.entries(MATERIALS)) ids.forEach(i => MAT_INDEX[i] = m);
  function materialOf(itemId) { return MAT_INDEX[itemId] || "stone"; }

  // Profili sonori per (azione, materiale)
  // Ogni profilo: una sequenza di chiamate sintetiche
  function play_pickup_wood()    { envOsc({type:"triangle", freq:200, freq2:140, dur:0.10, gain:0.30});
                                   setTimeout(()=>envOsc({type:"square", freq:90, dur:0.06, gain:0.18}), 60); }
  function play_pickup_cord()    { noiseBurst({dur:0.18, gain:0.22, cutoff:1800});
                                   envOsc({type:"sine", freq:380, freq2:280, dur:0.18, gain:0.12}); }
  function play_pickup_glass()   { envOsc({type:"sine", freq:1760, dur:0.10, gain:0.18});
                                   setTimeout(()=>envOsc({type:"sine", freq:2349, dur:0.18, gain:0.18}), 50);
                                   setTimeout(()=>envOsc({type:"sine", freq:2637, dur:0.20, gain:0.12}), 110); }
  function play_pickup_stone()   { noiseBurst({dur:0.10, gain:0.30, cutoff:900});
                                   envOsc({type:"square", freq:130, freq2:90, dur:0.08, gain:0.18}); }
  function play_pickup_metal()   { envOsc({type:"sine", freq:1568, dur:0.20, gain:0.18});
                                   setTimeout(()=>envOsc({type:"sine", freq:2349, dur:0.30, gain:0.14}), 80);
                                   setTimeout(()=>envOsc({type:"sine", freq:1175, dur:0.40, gain:0.10}), 160); }
  function play_pickup_organic() { noiseBurst({dur:0.18, gain:0.18, cutoff:3500});
                                   envOsc({type:"sine", freq:600, freq2:400, dur:0.10, gain:0.10}); }
  function play_pickup_mystic()  { for (let i = 0; i < 5; i++)
                                     setTimeout(()=>envOsc({type:"sine", freq:880 + i*180, dur:0.55, gain:0.10}), i*60); }

  function play_combine_wood()   { play_pickup_wood();
                                   setTimeout(()=>noiseBurst({dur:0.15, gain:0.20, cutoff:600}), 80); }
  function play_combine_metal()  { for (let i = 0; i < 3; i++)
                                     setTimeout(()=>envOsc({type:"sine", freq:1175 + i*300, dur:0.18, gain:0.20}), i*80); }
  function play_combine_glass()  { play_pickup_glass();
                                   setTimeout(()=>envOsc({type:"sine", freq:1976, dur:0.4, gain:0.10}), 200); }
  function play_combine_mystic() { for (let i = 0; i < 8; i++)
                                     setTimeout(()=>envOsc({type:"sine", freq:660 + i*110, dur:0.7, gain:0.12}), i*70); }
  function play_combine_default(){ envOsc({type:"triangle", freq:330, freq2:660, dur:0.12, gain:0.22});
                                   setTimeout(()=>envOsc({type:"sine", freq:880, freq2:1320, dur:0.18, gain:0.22}), 100);
                                   setTimeout(()=>envOsc({type:"sine", freq:1760, dur:0.18, gain:0.22}), 220); }

  function play_use_metal()      { envOsc({type:"sine", freq:880, dur:0.25, gain:0.18});
                                   setTimeout(()=>envOsc({type:"sine", freq:1175, dur:0.35, gain:0.14}), 100); }
  function play_use_mystic()     { for (let i = 0; i < 6; i++)
                                     setTimeout(()=>envOsc({type:"triangle", freq:440 + i*88, dur:0.6, gain:0.14}), i*50); }
  function play_use_organic()    { noiseBurst({dur:0.3, gain:0.15, cutoff:2500});
                                   envOsc({type:"sine", freq:300, dur:0.25, gain:0.10}); }
  function play_use_default()    { envOsc({type:"triangle", freq:550, freq2:330, dur:0.18, gain:0.22}); }

  const PROFILES = {
    pickup: {wood:play_pickup_wood, cord:play_pickup_cord, glass:play_pickup_glass,
             stone:play_pickup_stone, metal:play_pickup_metal, organic:play_pickup_organic,
             mystic:play_pickup_mystic},
    combine:{wood:play_combine_wood, metal:play_combine_metal, glass:play_combine_glass,
             mystic:play_combine_mystic, stone:play_combine_default,
             organic:play_combine_default, cord:play_combine_default},
    use:    {metal:play_use_metal, mystic:play_use_mystic, organic:play_use_organic,
             wood:play_use_default, glass:play_use_default, stone:play_use_default,
             cord:play_use_default},
  };

  function sfxItem(action, itemId) {
    if (muted || !ctx) return;
    resume();
    const mat = materialOf(itemId);
    const profileSet = PROFILES[action];
    const profile = profileSet?.[mat] || profileSet?.stone || (() => sfx(action));
    profile();
  }

  function toggleMute() {
    muted = !muted;
    if (masterGain) masterGain.gain.value = muted ? 0 : 0.7;
    return muted;
  }
  function isMuted(){ return muted; }

  return {resume, setRoom, sfx, sfxItem, materialOf, toggleMute, isMuted,
          toggleCaptions, captionsEnabled};
})();
