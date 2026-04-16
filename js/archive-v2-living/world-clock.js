// WorldClock + WeatherFSM + TideSystem (v2.0)
// Tempo globale: 1440 min gioco = 45 min reali (32× speed)
// Espone fasi giorno: dawn, day, dusk, night
// Weather come Markov FSM con probabilità per bioma
// Tide come sinusoide a 2 cicli/giorno
const WorldClock = (() => {
  const REAL_MS_PER_GAME_MIN = (45 * 60 * 1000) / 1440; // ≈ 1875 ms

  /** @type {{minutes:number, day:number, weather:string, tideHigh:number}} */
  let state = {minutes: 360, day: 0, weather: "clear", tideHigh: 0.5};
  let lastTickMs = null;
  let listeners = [];
  let weatherTimer = null;

  function init(initialState) {
    if (initialState && typeof initialState === "object") {
      state = {...state, ...initialState};
    }
    lastTickMs = Date.now();
    if (!weatherTimer) {
      weatherTimer = setInterval(() => maybeShiftWeather(), 30000); // ogni 30s
    }
    setInterval(tick, 250);
  }

  function tick() {
    if (lastTickMs === null) return;
    const now = Date.now();
    const realDelta = now - lastTickMs;
    lastTickMs = now;
    const gameDelta = realDelta / REAL_MS_PER_GAME_MIN;
    state.minutes += gameDelta;
    if (state.minutes >= 1440) {
      state.minutes -= 1440;
      state.day++;
    }
    // Tide: sinusoide 2 cicli/24h
    const tideAngle = (state.minutes / 1440) * Math.PI * 4;
    state.tideHigh = (Math.sin(tideAngle) + 1) / 2; // 0..1
    notify();
  }

  // ─── Weather Markov FSM ───
  // Probabilità di transizione (semplificate)
  const TRANSITIONS = {
    clear:   {clear: 0.85, cloudy: 0.10, fog: 0.05},
    cloudy:  {cloudy: 0.60, clear: 0.20, rain: 0.15, fog: 0.05},
    rain:    {rain: 0.70, cloudy: 0.20, storm: 0.10},
    storm:   {storm: 0.50, rain: 0.40, cloudy: 0.10},
    fog:     {fog: 0.60, clear: 0.30, cloudy: 0.10},
  };
  // Bias per bioma (modifica probabilità base)
  const BIOME_BIAS = {
    spiaggia:        {fog: 1.5},
    caletta:         {fog: 1.5, rain: 1.2},
    scogliere:       {storm: 2, rain: 1.5},
    scogliere_sud:   {storm: 2, rain: 1.5},
    cima_vulcano:    {storm: 2.5, fog: 0.3},
    sentiero_montagna:{storm: 1.5, fog: 1.3},
    foresta:         {rain: 1.3},
    giungla:         {rain: 1.5, fog: 1.2},
    giungla_profonda:{rain: 1.5, fog: 1.5},
    villaggio:       {clear: 1.3},
    laguna:          {fog: 1.4},
  };

  function maybeShiftWeather(currentRoom) {
    const trs = TRANSITIONS[state.weather] || TRANSITIONS.clear;
    const bias = (currentRoom && BIOME_BIAS[currentRoom]) || {};
    // Applica bias e normalizza
    const weighted = {};
    let total = 0;
    for (const [w, p] of Object.entries(trs)) {
      weighted[w] = p * (bias[w] ?? 1);
      total += weighted[w];
    }
    const r = Math.random() * total;
    let acc = 0;
    for (const [w, p] of Object.entries(weighted)) {
      acc += p;
      if (r <= acc) {
        if (w !== state.weather) {
          state.weather = w;
          notify({weather_changed: w});
        }
        return;
      }
    }
  }

  // ─── Phase ───
  function getPhase() {
    const m = state.minutes;
    if (m < 5*60) return "night";
    if (m < 7*60) return "dawn";
    if (m < 18*60) return "day";
    if (m < 20*60) return "dusk";
    return "night";
  }
  function getPhaseProgress() {
    const m = state.minutes;
    const phases = [
      [0,        5*60,  "night"],
      [5*60,     7*60,  "dawn"],
      [7*60,    18*60,  "day"],
      [18*60,   20*60,  "dusk"],
      [20*60,   24*60,  "night"],
    ];
    for (const [s, e] of phases) if (m >= s && m < e) return (m - s) / (e - s);
    return 0;
  }

  function getTimeString() {
    const h = Math.floor(state.minutes / 60);
    const m = Math.floor(state.minutes % 60);
    return `${String(h).padStart(2,"0")}:${String(m).padStart(2,"0")}`;
  }

  function getState() { return {...state}; }
  function setMinutes(m) { state.minutes = m; notify(); }
  function advanceMinutes(m) { state.minutes += m; if (state.minutes >= 1440) { state.minutes -= 1440; state.day++; } notify(); }

  function on(fn) { listeners.push(fn); return () => { listeners = listeners.filter(f => f !== fn); }; }
  function notify(extra) {
    const ev = {minutes: state.minutes, phase: getPhase(), weather: state.weather,
                tideHigh: state.tideHigh, day: state.day, ...extra};
    listeners.forEach(fn => { try { fn(ev); } catch(e) { console.error(e); } });
  }

  return {init, getState, getPhase, getPhaseProgress, getTimeString,
          setMinutes, advanceMinutes, on, maybeShiftWeather};
})();

if (typeof window !== "undefined") window.WorldClock = WorldClock;
