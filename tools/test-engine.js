// Test runner minimale (no Vitest dependency, plain node)
// Esegue assert sul reducer puro di engine.js
const fs = require("fs");
const path = require("path");

// Stub DOM globale per consentire eval di engine.js
global.document = {getElementById:()=>({innerHTML:"",classList:{add(){},remove(){},contains(){return false}},style:{},appendChild(){},removeChild(){},children:[],dataset:{},addEventListener(){}}),addEventListener(){},querySelectorAll:()=>[]};
global.localStorage = {s:{}, getItem(k){return this.s[k]||null}, setItem(k,v){this.s[k]=v}, removeItem(k){delete this.s[k]}};
global.window = global;

const root = path.resolve(__dirname, "..");
function loadJs(name) {
  const code = fs.readFileSync(path.join(root, "js", name), "utf-8");
  eval(code + `\nif (typeof Engine !== "undefined") global.Engine = Engine;`);
}

let pass = 0, fail = 0;
function test(name, fn) {
  try { fn(); pass++; console.log(`  ✓ ${name}`); }
  catch(e) { fail++; console.log(`  ❌ ${name}: ${e.message}`); }
}
function assert(cond, msg="assertion") { if (!cond) throw new Error(msg); }
function assertEq(a, b, msg) {
  if (JSON.stringify(a) !== JSON.stringify(b))
    throw new Error(`${msg||"eq"}: ${JSON.stringify(a)} !== ${JSON.stringify(b)}`);
}

console.log("=== State Machine tests ===");
loadJs("state-machine.js");
const SaveLib = global.SaveLib;

test("EventBus emits to global handlers", () => {
  const bus = new SaveLib.EventBus();
  let got = null;
  bus.on(ev => { got = ev; });
  bus.emit({type:"flag", key:"x", value:true});
  assertEq(got, {type:"flag", key:"x", value:true});
});
test("EventBus emits to type handlers only", () => {
  const bus = new SaveLib.EventBus();
  let a=0, b=0;
  bus.onType("flag", () => a++);
  bus.onType("moved", () => b++);
  bus.emit({type:"flag"}); bus.emit({type:"moved"}); bus.emit({type:"moved"});
  assertEq([a, b], [1, 2]);
});
test("Off-handler unsubscribes", () => {
  const bus = new SaveLib.EventBus();
  let n = 0;
  const off = bus.on(() => n++);
  bus.emit({type:"x"});
  off();
  bus.emit({type:"x"});
  assertEq(n, 1);
});
test("Migrations: v1 → v2 adds worldClock+skills+karma", () => {
  const old = {room:"spiaggia", inv:[], flags:{}, version:1};
  const m = SaveLib.migrateState(old);
  assert(m.version === 2);
  assert(m.worldClock && typeof m.worldClock.minutes === "number");
  assert(m.skills && m.skills.resistenza === 3);
  assert(m.karma && m.karma.villaggio === 0);
});
test("Migrations: undefined version defaults to 1", () => {
  const old = {room:"x"};
  const m = SaveLib.migrateState(old);
  assert(m.version === 2);
});

console.log("\n=== Engine tests (legacy compat) ===");
loadJs("engine.js");
const w = JSON.parse(fs.readFileSync(path.join(root, "data", "world.json"), "utf-8"));
Engine.init(w);

test("Engine starts in spiaggia with empty inv", () => {
  const st = Engine.getState();
  assertEq(st.room, "spiaggia");
  assertEq(st.inv.length, 0);
});
test("takeItem(legna) adds to inv", () => {
  const r = Engine.takeItem("legna");
  assert(r.ok);
  assert(Engine.getState().inv.includes("legna"));
});
test("takeItem twice on same item refuses (idempotent)", () => {
  const r = Engine.takeItem("legna");
  assert(!r.ok, "second pickup should fail");
});
test("setFlag emits event", () => {
  let got = null;
  Engine.on(ev => { if (ev.type === "flag") got = ev; });
  Engine.setFlag("test_flag", true);
  assert(got !== null);
});
test("Crafting recipe legna+pietra_focaia → torcia", () => {
  Engine.addItem("pietra_focaia");
  const res = Engine.useOn("legna", {kind:"item", id:"pietra_focaia"});
  assert(res.ok, "recipe should match");
  assert(Engine.getState().inv.includes("torcia"));
});

console.log(`\n=== ${pass} passed, ${fail} failed ===`);
process.exit(fail > 0 ? 1 : 0);
