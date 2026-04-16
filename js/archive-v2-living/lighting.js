// LightingMixer + WeatherOverlay (v2.0)
// Applica filtri CSS al #bg in base a fase giorno + meteo
// Crea/aggiorna #weather-overlay div con effetti rain/storm/fog
const Lighting = (() => {
  // LUT per fase: filter CSS + tint overlay
  const PHASE_FILTERS = {
    night: "saturate(.6) brightness(.45) contrast(1.15) hue-rotate(-15deg)",
    dawn:  "saturate(1.1) brightness(.85) contrast(1.05) hue-rotate(8deg) sepia(.18)",
    day:   "saturate(.95) brightness(1) contrast(1.0)",
    dusk:  "saturate(1.2) brightness(.78) contrast(1.1) hue-rotate(-10deg) sepia(.22)",
  };
  const PHASE_TINT = {
    night: "rgba(20, 30, 60, .45)",
    dawn:  "rgba(180, 100, 50, .22)",
    day:   "rgba(255, 250, 230, .04)",
    dusk:  "rgba(180, 60, 40, .28)",
  };
  // Weather overlay
  let lastPhase = null, lastWeather = null;

  function applyPhase(phase) {
    const bg = document.getElementById("bg");
    if (bg) bg.style.filter = PHASE_FILTERS[phase] || PHASE_FILTERS.day;
    let tint = document.getElementById("phase-tint");
    if (!tint) {
      tint = document.createElement("div");
      tint.id = "phase-tint";
      tint.style.cssText = "position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:multiply;transition:background-color 4s ease";
      const scene = document.getElementById("scene");
      if (scene) scene.appendChild(tint);
    }
    tint.style.backgroundColor = PHASE_TINT[phase] || PHASE_TINT.day;
  }

  function applyWeather(weather) {
    let overlay = document.getElementById("weather-overlay");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "weather-overlay";
      overlay.style.cssText = "position:absolute;inset:0;z-index:6;pointer-events:none;overflow:hidden";
      const scene = document.getElementById("scene");
      if (scene) scene.appendChild(overlay);
    }
    overlay.innerHTML = "";
    overlay.className = "weather-" + weather;
    if (weather === "rain") {
      for (let i = 0; i < 60; i++) {
        const drop = document.createElement("div");
        drop.className = "rain-drop";
        drop.style.cssText = `position:absolute;left:${Math.random()*100}%;top:${-Math.random()*30}%;width:1px;height:${10+Math.random()*15}px;background:linear-gradient(180deg,transparent,#a0c8e8);opacity:.45;animation:rainFall ${.4+Math.random()*.5}s linear ${Math.random()*.8}s infinite`;
        overlay.appendChild(drop);
      }
    } else if (weather === "storm") {
      for (let i = 0; i < 100; i++) {
        const drop = document.createElement("div");
        drop.style.cssText = `position:absolute;left:${Math.random()*100}%;top:${-Math.random()*30}%;width:1.5px;height:${15+Math.random()*20}px;background:linear-gradient(180deg,transparent,#80a0d0);opacity:.6;animation:rainFall ${.25+Math.random()*.3}s linear ${Math.random()*.5}s infinite;transform:rotate(-12deg)`;
        overlay.appendChild(drop);
      }
      // Lightning sporadico
      const flash = document.createElement("div");
      flash.style.cssText = "position:absolute;inset:0;background:#ffffff;opacity:0;animation:lightningFlash 6s linear infinite";
      overlay.appendChild(flash);
    } else if (weather === "fog") {
      for (let i = 0; i < 4; i++) {
        const fog = document.createElement("div");
        fog.style.cssText = `position:absolute;left:${-20+i*30}%;top:${20+Math.random()*40}%;width:80%;height:${30+Math.random()*40}%;background:radial-gradient(ellipse,rgba(220,220,220,.18),transparent 70%);animation:fogDrift ${30+Math.random()*40}s ease-in-out infinite alternate`;
        overlay.appendChild(fog);
      }
    } else if (weather === "cloudy") {
      // sottile velo grigio
      const veil = document.createElement("div");
      veil.style.cssText = "position:absolute;inset:0;background:radial-gradient(ellipse at top,rgba(120,130,140,.15),transparent 70%)";
      overlay.appendChild(veil);
    }
  }

  function update(ev) {
    if (ev.phase !== lastPhase) {
      applyPhase(ev.phase);
      lastPhase = ev.phase;
    }
    if (ev.weather !== lastWeather) {
      applyWeather(ev.weather);
      lastWeather = ev.weather;
    }
  }

  function init() {
    if (window.WorldClock) {
      WorldClock.on(update);
      // Apply iniziale
      const wc = WorldClock.getState();
      update({phase: WorldClock.getPhase(), weather: wc.weather});
    }
  }

  return {init, update, applyPhase, applyWeather};
})();

if (typeof window !== "undefined") window.Lighting = Lighting;
