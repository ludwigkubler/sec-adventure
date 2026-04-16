// Procedural sky: canvas con sole/luna/stelle che si muovono in base a WorldClock
// Si renderizza su #sky-canvas (creato da render.js) sopra #bg
const Sky = (() => {
  /** @type {HTMLCanvasElement|null} */
  let canvas = null;
  /** @type {CanvasRenderingContext2D|null} */
  let ctx = null;
  let lastDraw = 0;
  let stars = []; // posizioni stabili sull'emisfero

  function ensure() {
    canvas = document.getElementById("sky-canvas");
    if (!canvas) return false;
    ctx = canvas.getContext("2d");
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    if (!stars.length) generateStars();
    return true;
  }
  function generateStars() {
    for (let i = 0; i < 80; i++) {
      stars.push({
        x: Math.random(),
        y: Math.random() * 0.6,
        size: Math.random() * 1.5 + 0.4,
        twinkle: Math.random() * Math.PI * 2,
      });
    }
  }
  function draw() {
    if (!ctx) return;
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    if (!window.WorldClock) return;
    const wc = WorldClock.getState();
    const phase = WorldClock.getPhase();
    const t = wc.minutes / 1440; // 0..1

    // ─── Sky gradient per fase ───
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    if (phase === "night") {
      bgGrad.addColorStop(0, "#0a0e1a");
      bgGrad.addColorStop(0.6, "#1a1424");
      bgGrad.addColorStop(1, "#2a1a1a");
    } else if (phase === "dawn") {
      bgGrad.addColorStop(0, "#2a3050");
      bgGrad.addColorStop(0.5, "#a05828");
      bgGrad.addColorStop(1, "#d8a060");
    } else if (phase === "day") {
      bgGrad.addColorStop(0, "#5080a0");
      bgGrad.addColorStop(0.5, "#90b0c8");
      bgGrad.addColorStop(1, "#d0c8b0");
    } else if (phase === "dusk") {
      bgGrad.addColorStop(0, "#3a2050");
      bgGrad.addColorStop(0.5, "#a04030");
      bgGrad.addColorStop(1, "#603020");
    }
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // ─── Stars (visibili di notte e in dawn) ───
    if (phase === "night" || phase === "dawn" || phase === "dusk") {
      const alpha = phase === "night" ? 0.95 : (phase === "dawn" || phase === "dusk" ? 0.4 : 0);
      ctx.fillStyle = `rgba(255, 240, 200, ${alpha})`;
      stars.forEach((s, i) => {
        const tw = Math.sin(performance.now() / 800 + s.twinkle) * 0.3 + 0.7;
        ctx.globalAlpha = alpha * tw;
        ctx.beginPath();
        ctx.arc(s.x * w, s.y * h, s.size, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1;
    }

    // ─── Sun + Moon arc ───
    // Sun sorge a 5 (dawn end), tramonta a 19. Cammina su arco.
    const sunT = (wc.minutes - 5*60) / (14*60); // 0..1 da alba al tramonto
    if (sunT >= 0 && sunT <= 1) {
      const sunX = sunT * w;
      const sunY = h * 0.55 - Math.sin(sunT * Math.PI) * h * 0.45;
      const sunR = 22;
      // glow
      const sg = ctx.createRadialGradient(sunX, sunY, sunR*0.4, sunX, sunY, sunR*4);
      sg.addColorStop(0, "rgba(255, 240, 180, .85)");
      sg.addColorStop(0.4, "rgba(255, 200, 120, .35)");
      sg.addColorStop(1, "rgba(255, 180, 80, 0)");
      ctx.fillStyle = sg;
      ctx.beginPath(); ctx.arc(sunX, sunY, sunR*4, 0, Math.PI*2); ctx.fill();
      // disk
      ctx.fillStyle = phase === "dawn" || phase === "dusk" ? "#ffc070" : "#fff0c8";
      ctx.beginPath(); ctx.arc(sunX, sunY, sunR, 0, Math.PI*2); ctx.fill();
    }
    // Moon: 19→5 (night)
    const moonT = wc.minutes < 5*60 ? (wc.minutes + 24*60 - 19*60) / 10*60 :
                  wc.minutes >= 19*60 ? (wc.minutes - 19*60) / (10*60) : -1;
    if (moonT >= 0 && moonT <= 1) {
      const moonX = moonT * w;
      const moonY = h * 0.6 - Math.sin(moonT * Math.PI) * h * 0.4;
      const moonR = 16;
      const mg = ctx.createRadialGradient(moonX, moonY, moonR*0.3, moonX, moonY, moonR*3);
      mg.addColorStop(0, "rgba(220, 220, 240, .65)");
      mg.addColorStop(1, "rgba(180, 180, 220, 0)");
      ctx.fillStyle = mg;
      ctx.beginPath(); ctx.arc(moonX, moonY, moonR*3, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#e0e0f0";
      ctx.beginPath(); ctx.arc(moonX, moonY, moonR, 0, Math.PI*2); ctx.fill();
      // crater hint
      ctx.fillStyle = "rgba(160, 160, 180, .5)";
      ctx.beginPath(); ctx.arc(moonX-3, moonY-2, 3, 0, Math.PI*2); ctx.fill();
      ctx.beginPath(); ctx.arc(moonX+4, moonY+3, 2, 0, Math.PI*2); ctx.fill();
    }
  }

  function start() {
    if (!ensure()) return;
    function loop() {
      const now = performance.now();
      if (now - lastDraw > 200) { // throttle 5 fps (sky è lento)
        draw();
        lastDraw = now;
      }
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  }
  function resize() { if (canvas) { canvas.width = canvas.clientWidth; canvas.height = canvas.clientHeight; } }

  return {start, draw, resize};
})();

if (typeof window !== "undefined") {
  window.Sky = Sky;
  window.addEventListener("resize", () => Sky.resize && Sky.resize());
}
