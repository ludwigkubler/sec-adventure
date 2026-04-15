// State machine + reducer puro + event bus tipizzato (v2.0)
// Foundation per espandibilità: ogni mutazione passa dal reducer.
// Eventi tipizzati con discriminated union via JSDoc per checkJs.

/**
 * @typedef {Object} StateBase
 * @property {string} room
 * @property {string[]} inv
 * @property {Record<string,boolean>} flags
 * @property {Record<string,boolean>} taken
 * @property {Record<string,boolean>} visited
 * @property {Record<string,boolean>} codex
 * @property {Record<string,object>} achievements
 * @property {string|null} selected
 * @property {number} elapsed
 * @property {number|null} startedAt
 * @property {number} version
 */

/**
 * @typedef {Object} WorldClockState
 * @property {number} minutes  Game minutes 0..1440
 * @property {number} day       Day count from start (0..)
 * @property {string} weather   "clear"|"cloudy"|"rain"|"storm"|"fog"
 * @property {number} tideHigh  0..1 (tide level)
 */

/**
 * Event bus tipizzato. Sostituisce l'array `listeners` legacy.
 * @template T
 */
class EventBus {
  constructor() {
    /** @type {Map<string, Set<(ev:T)=>void>>} */
    this.handlers = new Map();
    /** @type {Set<(ev:T)=>void>} */
    this.allHandlers = new Set();
  }
  /** @param {(ev:T)=>void} fn */
  on(fn) { this.allHandlers.add(fn); return () => this.allHandlers.delete(fn); }
  /** @param {string} type @param {(ev:T)=>void} fn */
  onType(type, fn) {
    if (!this.handlers.has(type)) this.handlers.set(type, new Set());
    this.handlers.get(type).add(fn);
    return () => this.handlers.get(type)?.delete(fn);
  }
  /** @param {T & {type:string}} ev */
  emit(ev) {
    this.allHandlers.forEach(fn => { try { fn(ev); } catch(e) { console.error("[bus]", e); } });
    this.handlers.get(ev.type)?.forEach(fn => { try { fn(ev); } catch(e) { console.error("[bus]", e); } });
  }
}

// ─── Save schema migrations ───────────────────────────────────────
const SAVE_VERSION = 2;
const MIGRATIONS = {
  /** v1 → v2: aggiunge worldClock + skills + thoughts + karma */
  1: (s) => {
    s.worldClock = { minutes: 360, day: 0, weather: "clear", tideHigh: 0.5 };
    s.skills = { intuito: 1, meccanica: 1, empatia: 1, resistenza: 3, occhio: 1, voce: 1 };
    s.thoughts = {};
    s.karma = { villaggio: 0, costruttori: 0, mare: 0 };
    s.companions = {};
    s.fatigue = 0;
    s.hunger = 0;
    s.durability = {};
    s.prints = {};
    s.version = 2;
    return s;
  },
};

/**
 * Migra uno stato vecchio fino alla versione corrente.
 * @param {Partial<StateBase> & {version?:number}} state
 * @returns {StateBase}
 */
function migrateState(state) {
  if (!state.version) state.version = 1;
  while (state.version < SAVE_VERSION) {
    const m = MIGRATIONS[state.version];
    if (!m) { state.version++; continue; }
    state = m(state);
  }
  return /** @type {StateBase} */(state);
}

// ─── Cloud save adapter pattern ───────────────────────────────────
class LocalStorageAdapter {
  constructor(key="quellisola_save_v2") { this.key = key; }
  async save(state) { localStorage.setItem(this.key, JSON.stringify(state)); }
  async load() {
    const s = localStorage.getItem(this.key);
    if (!s) return null;
    try { return JSON.parse(s); } catch(e) { return null; }
  }
  async exists() { return !!localStorage.getItem(this.key); }
  async clear() { localStorage.removeItem(this.key); }
}

// Espongo globalmente per compat con script tag legacy
if (typeof window !== "undefined") {
  window.SaveLib = { EventBus, migrateState, LocalStorageAdapter, SAVE_VERSION };
}
if (typeof module !== "undefined") {
  module.exports = { EventBus, migrateState, LocalStorageAdapter, SAVE_VERSION };
}
