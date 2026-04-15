#!/usr/bin/env python3
"""Genera icone SVG semplici e stilizzate per ogni oggetto del gioco.
Usa forme geometriche essenziali con palette seppia/ocra coerente con le stanze SD.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD = json.load(open(ROOT / "data" / "world.json", encoding="utf-8"))
OUT = ROOT / "assets" / "items"
OUT.mkdir(parents=True, exist_ok=True)

# Palette
BG = "#2a1a0c"
OUTLINE = "#1a0e05"
GOLD = "#c08a3c"
LIGHT = "#e8d7b0"
RED = "#b04030"
GREEN = "#6a8040"
BLUE = "#4878a0"
WOOD = "#8a5a30"
STONE = "#707068"

VIEWBOX = 'viewBox="0 0 64 64"'

# Ogni entry → callable che ritorna l'SVG interno (senza <svg> wrapper)
def legna():      return f'''<g>
  <rect x="6" y="24" width="52" height="9" rx="3" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="2"/>
  <line x1="6" y1="28" x2="58" y2="28" stroke="#6a4020" stroke-width="1" opacity=".6"/>
  <line x1="10" y1="31" x2="54" y2="31" stroke="#6a4020" stroke-width="1" opacity=".4"/>
  <rect x="10" y="36" width="44" height="8" rx="2" fill="#6a4020" stroke="{OUTLINE}" stroke-width="2"/>
  <line x1="14" y1="40" x2="50" y2="40" stroke="#4a2812" stroke-width="1" opacity=".6"/>
  <circle cx="12" cy="28" r="1.5" fill="#3a2010" opacity=".6"/>
  <circle cx="46" cy="40" r="1.5" fill="#3a2010" opacity=".6"/>
</g>'''
def corda():      return f'''<g>
  <path d="M6 22 Q14 10 22 22 T38 22 T56 22 Q58 24 58 26" stroke="{WOOD}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M6 22 Q14 10 22 22 T38 22 T56 22 Q58 24 58 26" stroke="#6a4020" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M6 32 Q14 20 22 32 T38 32 T56 32" stroke="{WOOD}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M6 32 Q14 20 22 32 T38 32 T56 32" stroke="#5a3010" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M6 42 Q14 30 22 42 T38 42 T56 42" stroke="#6a4020" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M6 42 Q14 30 22 42 T38 42 T56 42" stroke="#4a2010" stroke-width="1.5" fill="none" stroke-linecap="round" opacity=".7"/>
  <!-- Frays -->
  <line x1="6" y1="22" x2="3" y2="20" stroke="{WOOD}" stroke-width="1"/>
  <line x1="6" y1="22" x2="2" y2="24" stroke="{WOOD}" stroke-width="1"/>
</g>'''
def bottiglia():  return f'<rect x="24" y="8" width="16" height="10" fill="#405848" stroke="{OUTLINE}" stroke-width="2"/><path d="M20 20 L20 54 Q20 58 24 58 L40 58 Q44 58 44 54 L44 20 Z" fill="#5a8070" stroke="{OUTLINE}" stroke-width="2"/><rect x="28" y="4" width="8" height="6" fill="#3a2818" stroke="{OUTLINE}" stroke-width="1"/>'
def pietra_focaia(): return f'<polygon points="10,40 24,14 44,18 54,36 48,54 20,52" fill="{STONE}" stroke="{OUTLINE}" stroke-width="2"/><polygon points="20,30 30,20 40,30 35,42 22,40" fill="#909088"/>'
def conchiglia(): return f'<path d="M32 8 Q52 28 52 46 Q42 56 32 56 Q22 56 12 46 Q12 28 32 8 Z" fill="#e8c0a0" stroke="{OUTLINE}" stroke-width="2"/><path d="M32 12 L32 54 M20 22 L44 22 M16 34 L48 34 M20 46 L44 46" stroke="#b8866a" stroke-width="1.5" fill="none"/>'
def lama_antica(): return f'<polygon points="30,6 36,6 38,42 30,42" fill="#b8b8c0" stroke="{OUTLINE}" stroke-width="2"/><rect x="22" y="42" width="22" height="6" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="2"/><rect x="28" y="48" width="10" height="12" fill="#5a3820" stroke="{OUTLINE}" stroke-width="2"/>'
def artefatto_sacro(): return f'<polygon points="32,6 48,24 48,48 32,58 16,48 16,24" fill="#70a080" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="32" r="8" fill="#2a4030" stroke="#a0c090" stroke-width="1.5"/><path d="M32 20 L32 44 M20 32 L44 32" stroke="#2a4030" stroke-width="1.5"/>'
def ramo_robusto(): return f'<path d="M6 52 Q20 40 30 32 T54 12" stroke="{WOOD}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M30 32 L22 24 M38 24 L44 18 M16 46 L10 50" stroke="{WOOD}" stroke-width="3" stroke-linecap="round"/>'
def bacche():     return f'<circle cx="20" cy="36" r="8" fill="{RED}" stroke="{OUTLINE}" stroke-width="2"/><circle cx="36" cy="28" r="8" fill="{RED}" stroke="{OUTLINE}" stroke-width="2"/><circle cx="44" cy="44" r="8" fill="{RED}" stroke="{OUTLINE}" stroke-width="2"/><path d="M36 20 L40 10 M20 28 L18 18" stroke="{GREEN}" stroke-width="2"/>'
def fiori():      return f'<circle cx="32" cy="32" r="6" fill="#e0c040"/><circle cx="32" cy="18" r="8" fill="#d8506a" stroke="{OUTLINE}" stroke-width="1"/><circle cx="46" cy="32" r="8" fill="#d8506a" stroke="{OUTLINE}" stroke-width="1"/><circle cx="32" cy="46" r="8" fill="#d8506a" stroke="{OUTLINE}" stroke-width="1"/><circle cx="18" cy="32" r="8" fill="#d8506a" stroke="{OUTLINE}" stroke-width="1"/>'
def chiodi_arrugginiti(): return f'<path d="M12 8 L20 12 L18 54 L14 54 Z" fill="#8a5030" stroke="{OUTLINE}" stroke-width="1.5"/><path d="M32 8 L40 12 L38 54 L34 54 Z" fill="#8a5030" stroke="{OUTLINE}" stroke-width="1.5"/><path d="M50 8 L58 12 L56 54 L52 54 Z" fill="#8a5030" stroke="{OUTLINE}" stroke-width="1.5"/>'
def messaggio_bottiglia(): return f'<rect x="16" y="12" width="32" height="42" rx="3" fill="#d8c8a0" stroke="{OUTLINE}" stroke-width="2"/><path d="M22 22 L42 22 M22 30 L40 30 M22 38 L42 38 M22 46 L38 46" stroke="#8a6030" stroke-width="1.5"/>'
def rete_pesca(): return f'<path d="M8 20 L56 20 L48 56 L16 56 Z" fill="none" stroke="{WOOD}" stroke-width="2"/>' + "".join(f'<path d="M{8+i*6} 20 L{16+i*5} 56" stroke="{WOOD}" stroke-width="1.5"/>' for i in range(9)) + "".join(f'<path d="M8 {20+i*9} L56 {20+i*9}" stroke="{WOOD}" stroke-width="1.5"/>' for i in range(5))
def olio_vegetale(): return f'<path d="M22 10 L42 10 L42 20 L46 24 L46 56 Q46 58 44 58 L20 58 Q18 58 18 56 L18 24 L22 20 Z" fill="#d0a040" stroke="{OUTLINE}" stroke-width="2"/><rect x="26" y="4" width="12" height="8" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1.5"/>'
def resina():     return f'<ellipse cx="32" cy="40" rx="18" ry="20" fill="#d08030" stroke="{OUTLINE}" stroke-width="2"/><path d="M32 20 Q26 30 24 40" stroke="#e8a060" stroke-width="2" fill="none"/>'
def pianta_rara(): return f'<rect x="22" y="44" width="20" height="16" fill="#5a3820" stroke="{OUTLINE}" stroke-width="2"/><path d="M32 44 L32 8" stroke="{GREEN}" stroke-width="2"/><path d="M32 16 Q20 18 14 12 Q20 22 32 22 Q44 22 50 12 Q44 18 32 16 Z" fill="#7a9050" stroke="{OUTLINE}" stroke-width="1.5"/><circle cx="32" cy="14" r="5" fill="#e0a0d0" stroke="{OUTLINE}" stroke-width="1"/>'
def erbe_secche(): return "".join(f'<path d="M{14+i*10} 56 L{16+i*10} 12 Q{18+i*10} 8 {20+i*10} 12 L{22+i*10} 56 Z" fill="#a89060" stroke="{OUTLINE}" stroke-width="1.5"/>' for i in range(4))
def piccone():    return f'<path d="M8 16 L32 28 L56 16 L50 32 L32 40 L14 32 Z" fill="{STONE}" stroke="{OUTLINE}" stroke-width="2"/><rect x="30" y="38" width="5" height="24" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="1.5"/>'
def cristallo_vulcanico(): return f'<polygon points="32,4 48,24 40,56 24,56 16,24" fill="#d84030" stroke="{OUTLINE}" stroke-width="2"/><polygon points="32,4 40,24 32,42 24,24" fill="#e8806a" stroke="#d84030" stroke-width="1"/>'
def frammento_mappa(): return f'<path d="M8 10 L54 6 L58 52 L10 56 Z" fill="#d0b080" stroke="{OUTLINE}" stroke-width="2"/><path d="M20 20 Q30 26 44 24 M18 36 Q28 32 46 38 M22 48 L44 46" stroke="#6a4020" stroke-width="1.5" fill="none"/><circle cx="40" cy="28" r="3" fill="{RED}"/>'
def diario_guardiano(): return f'<rect x="12" y="8" width="40" height="48" rx="2" fill="#5a3020" stroke="{OUTLINE}" stroke-width="2"/><rect x="12" y="8" width="6" height="48" fill="#3a1810"/><path d="M24 20 L46 20 M24 28 L44 28 M24 36 L46 36 M24 44 L42 44" stroke="#d0b080" stroke-width="1.5"/>'
def gemma_potere(): return f'<polygon points="32,6 52,26 32,58 12,26" fill="#6060d8" stroke="{OUTLINE}" stroke-width="2"/><polygon points="32,6 42,26 32,40 22,26" fill="#a0a0e8" stroke="#6060d8" stroke-width="1"/><circle cx="32" cy="26" r="4" fill="#ffffff" opacity="0.6"/>'
def tavoletta_antica(): return f'<rect x="10" y="14" width="44" height="36" rx="2" fill="#a89060" stroke="{OUTLINE}" stroke-width="2"/><path d="M18 22 L46 22 M18 28 L40 28 M18 34 L44 34 M18 40 L38 40" stroke="#4a3010" stroke-width="1.5"/>'
def attrezzatura_sub(): return f'<rect x="22" y="8" width="20" height="28" rx="4" fill="#3050a0" stroke="{OUTLINE}" stroke-width="2"/><circle cx="26" cy="24" r="3" fill="#e0e0ff"/><circle cx="38" cy="24" r="3" fill="#e0e0ff"/><path d="M22 36 Q16 44 16 56 M42 36 Q48 44 48 56" stroke="#2a2a2a" stroke-width="3" fill="none"/>'
def perla_nera():  return f'<circle cx="32" cy="32" r="22" fill="#1a1a2a" stroke="{OUTLINE}" stroke-width="2"/><circle cx="26" cy="26" r="8" fill="#4a4a6a" opacity="0.6"/><circle cx="24" cy="24" r="3" fill="#a0a0c0" opacity="0.9"/>'
def sigillo_antico(): return f'<circle cx="32" cy="32" r="26" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="32" r="18" fill="none" stroke="{OUTLINE}" stroke-width="1.5"/><polygon points="32,14 40,28 56,28 44,38 48,54 32,46 16,54 20,38 8,28 24,28" fill="{OUTLINE}" opacity="0.5"/>'
def tridente():   return f'<rect x="30" y="28" width="4" height="32" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="1.5"/><polygon points="20,8 22,28 30,28 32,18 34,28 42,28 44,8 38,20 32,10 26,20" fill="#c0c0c8" stroke="{OUTLINE}" stroke-width="2"/>'
def corona_corallo(): return f'<path d="M8 46 L12 20 L20 38 L28 16 L36 38 L44 18 L52 38 L56 46 L56 58 L8 58 Z" fill="#e08070" stroke="{OUTLINE}" stroke-width="2"/><circle cx="28" cy="16" r="4" fill="#d84030"/><circle cx="44" cy="18" r="3" fill="#d84030"/>'
def torcia():     return f'''<g>
  <!-- Handle with grain -->
  <rect x="28" y="32" width="8" height="28" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="2"/>
  <line x1="28" y1="38" x2="36" y2="38" stroke="#5a3010" stroke-width=".5" opacity=".8"/>
  <line x1="28" y1="46" x2="36" y2="46" stroke="#5a3010" stroke-width=".5" opacity=".8"/>
  <line x1="28" y1="54" x2="36" y2="54" stroke="#5a3010" stroke-width=".5" opacity=".8"/>
  <!-- Wrap -->
  <path d="M20 32 L44 32 L38 22 L26 22 Z" fill="#5a3820" stroke="{OUTLINE}" stroke-width="2"/>
  <line x1="24" y1="26" x2="40" y2="26" stroke="#3a2010" stroke-width=".8"/>
  <line x1="22" y1="30" x2="42" y2="30" stroke="#3a2010" stroke-width=".8"/>
  <!-- Outer flame -->
  <path d="M20 22 Q32 -2 44 22 Q32 10 20 22 Z" fill="#ff6020" stroke="#c04010" stroke-width="1.5">
    <animate attributeName="opacity" values="0.75;1;0.75" dur="1.2s" repeatCount="indefinite"/>
  </path>
  <!-- Inner flame -->
  <path d="M26 20 Q32 4 38 20 Q32 12 26 20 Z" fill="#ffc040">
    <animate attributeName="opacity" values="1;0.7;1" dur="0.8s" repeatCount="indefinite"/>
  </path>
  <!-- Core hot spot -->
  <ellipse cx="32" cy="14" rx="3" ry="5" fill="#fff0a0">
    <animate attributeName="rx" values="2;3.5;2" dur="1s" repeatCount="indefinite"/>
  </ellipse>
</g>'''
def machete():    return f'''<g>
  <!-- Blade with shine -->
  <path d="M14 10 L58 44 L54 50 L10 16 Z" fill="#d4d4e0" stroke="{OUTLINE}" stroke-width="2"/>
  <path d="M14 10 L58 44 L56 46 L12 12 Z" fill="#f0f0ff" opacity=".5"/>
  <path d="M30 24 L54 44 L52 48 L28 28 Z" fill="#a0a0b0" opacity=".4"/>
  <!-- Handle wood -->
  <rect x="2" y="8" width="18" height="10" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="2" transform="rotate(-35 11 14)"/>
  <line x1="7" y1="10" x2="17" y2="20" stroke="#5a3010" stroke-width="1" transform="rotate(-35 11 14)" opacity=".7"/>
  <!-- Guard -->
  <rect x="18" y="6" width="4" height="14" fill="#707078" stroke="{OUTLINE}" stroke-width="1.5" transform="rotate(-35 20 13)"/>
</g>'''
def medaglione(): return f'''<g>
  <!-- Cord -->
  <path d="M20 14 Q32 8 44 14" stroke="{WOOD}" stroke-width="2.5" fill="none"/>
  <path d="M20 14 Q32 8 44 14" stroke="#5a3010" stroke-width=".5" fill="none" opacity=".7"/>
  <!-- Gold outer ring -->
  <circle cx="32" cy="38" r="22" fill="#d4a040" stroke="{OUTLINE}" stroke-width="2"/>
  <circle cx="32" cy="38" r="20" fill="{GOLD}"/>
  <!-- Inner recess -->
  <circle cx="32" cy="38" r="15" fill="#8a5820" stroke="{OUTLINE}" stroke-width="1"/>
  <circle cx="32" cy="38" r="14" fill="none" stroke="#d4a040" stroke-width=".8"/>
  <!-- Central star -->
  <polygon points="32,26 35,34 44,34 37,40 40,50 32,44 24,50 27,40 20,34 29,34" fill="{OUTLINE}"/>
  <polygon points="32,29 34,34 40,34 35,38 37,46 32,42 27,46 29,38 24,34 30,34" fill="#f0c060" opacity=".7"/>
  <!-- Shine highlight -->
  <ellipse cx="26" cy="30" rx="5" ry="3" fill="#ffe080" opacity=".6" transform="rotate(-30 26 30)"/>
</g>'''
def chiave_faro(): return f'''<g>
  <!-- Bow (head ring) decorato -->
  <circle cx="18" cy="32" r="12" fill="#d4a040" stroke="{OUTLINE}" stroke-width="2"/>
  <circle cx="18" cy="32" r="8" fill="#2a1a0c" stroke="{OUTLINE}" stroke-width="1"/>
  <circle cx="18" cy="32" r="5" fill="#d4a040"/>
  <!-- 4 ornamental points -->
  <path d="M18 20 L20 23 L18 26 L16 23 Z" fill="#f0c060"/>
  <path d="M18 38 L20 41 L18 44 L16 41 Z" fill="#f0c060"/>
  <path d="M6 32 L9 30 L12 32 L9 34 Z" fill="#f0c060"/>
  <path d="M24 32 L27 30 L30 32 L27 34 Z" fill="#f0c060"/>
  <!-- Shaft -->
  <rect x="30" y="29" width="26" height="6" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="1.5"/>
  <line x1="30" y1="32" x2="56" y2="32" stroke="#a06820" stroke-width=".5"/>
  <!-- Teeth (bit) -->
  <rect x="42" y="28" width="3" height="10" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="1"/>
  <rect x="48" y="28" width="3" height="14" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="1"/>
  <rect x="53" y="28" width="3" height="8" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="1"/>
  <!-- Shine -->
  <circle cx="14" cy="28" r="2" fill="#ffe080" opacity=".6"/>
</g>'''
def chiave_antica(): return f'''<g>
  <circle cx="18" cy="32" r="12" fill="#707078" stroke="{OUTLINE}" stroke-width="2"/>
  <circle cx="18" cy="32" r="8" fill="#1a1a22" stroke="{OUTLINE}" stroke-width="1"/>
  <circle cx="18" cy="32" r="5" fill="#909098"/>
  <!-- Rune etched -->
  <text x="18" y="35" font-size="8" text-anchor="middle" fill="#3a3a42" font-family="serif">◈</text>
  <!-- Shaft -->
  <rect x="30" y="29" width="26" height="6" fill="#909098" stroke="{OUTLINE}" stroke-width="1.5"/>
  <line x1="30" y1="32" x2="56" y2="32" stroke="#5a5a62" stroke-width=".5"/>
  <!-- Teeth -->
  <rect x="44" y="28" width="3" height="10" fill="#909098" stroke="{OUTLINE}" stroke-width="1"/>
  <rect x="50" y="28" width="3" height="12" fill="#909098" stroke="{OUTLINE}" stroke-width="1"/>
  <circle cx="14" cy="28" r="2" fill="#c0c0c8" opacity=".5"/>
</g>'''
def antidoto():   return f'<rect x="22" y="8" width="20" height="8" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1.5"/><path d="M22 16 L22 50 L26 58 L38 58 L42 50 L42 16 Z" fill="#70c080" stroke="{OUTLINE}" stroke-width="2"/><rect x="26" y="22" width="12" height="20" fill="#3a8050" opacity="0.6"/>'

# ─── Atto II: oggetti delle profondità ───
def spore_lumino(): return f'<circle cx="20" cy="22" r="6" fill="#80ff90" opacity="0.8"/><circle cx="42" cy="20" r="5" fill="#80ff90" opacity="0.7"/><circle cx="32" cy="40" r="7" fill="#80ff90" opacity="0.85"/><circle cx="48" cy="46" r="4" fill="#80ff90" opacity="0.6"/><circle cx="16" cy="48" r="5" fill="#80ff90" opacity="0.7"/><circle cx="32" cy="40" r="3" fill="#ffffff"/>'
def ingranaggio():  return f'<g transform="translate(32 32)"><g fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5">' + "".join(f'<rect x="-4" y="-26" width="8" height="10" transform="rotate({i*45})"/>' for i in range(8)) + f'</g><circle r="18" fill="#c08850" stroke="{OUTLINE}" stroke-width="2"/><circle r="6" fill="#1a0e05"/></g>'
def ruota_dentata(): return f'<g transform="translate(32 32)"><g fill="#5a5860" stroke="{OUTLINE}" stroke-width="1.5">' + "".join(f'<rect x="-3" y="-28" width="6" height="8" transform="rotate({i*30})"/>' for i in range(12)) + f'</g><circle r="20" fill="#707068" stroke="{OUTLINE}" stroke-width="2"/><circle r="14" fill="none" stroke="{OUTLINE}" stroke-width="1.5"/><circle r="4" fill="#1a0e05"/></g>'
def binario_ferro(): return f'<rect x="6" y="28" width="52" height="8" fill="#5a5860" stroke="{OUTLINE}" stroke-width="1.5"/>' + "".join(f'<rect x="{8+i*5}" y="22" width="3" height="6" fill="#5a5860" stroke="{OUTLINE}" stroke-width="1"/>' for i in range(10))
def martello_rame(): return f'<rect x="14" y="14" width="36" height="20" fill="#c08850" stroke="{OUTLINE}" stroke-width="2"/><rect x="20" y="34" width="4" height="24" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1.5"/>'
def pendolo_ottone(): return f'<rect x="30" y="6" width="4" height="22" fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5"/><circle cx="32" cy="6" r="3" fill="#5a3820"/><path d="M32 28 L48 50 L40 58 L24 58 L16 50 Z" fill="#d4a060" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="42" r="6" fill="#c08850" opacity="0.6"/>'
def valvola_vapore(): return f'<rect x="22" y="32" width="20" height="20" fill="#5a5860" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="20" r="14" fill="none" stroke="#c08850" stroke-width="3"/>' + "".join(f'<rect x="30" y="6" width="4" height="8" fill="#c08850" transform="rotate({i*60} 32 20)"/>' for i in range(6)) + f'<circle cx="32" cy="20" r="3" fill="{OUTLINE}"/>'
def ampolla():    return f'<path d="M28 8 L36 8 L36 18 Q44 22 44 32 L44 54 Q44 58 40 58 L24 58 Q20 58 20 54 L20 32 Q20 22 28 18 Z" fill="#a0d8e0" stroke="{OUTLINE}" stroke-width="2" opacity="0.85"/><rect x="28" y="4" width="8" height="6" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1"/><ellipse cx="32" cy="44" rx="9" ry="7" fill="#80c0d0" opacity="0.5"/>'
def catena_oro(): return "".join(f'<ellipse cx="{12+i*10}" cy="32" rx="6" ry="4" fill="none" stroke="#d4a040" stroke-width="2.5"/>' for i in range(5))
def tavoletta_runica(): return f'<rect x="14" y="10" width="36" height="44" rx="2" fill="#909088" stroke="{OUTLINE}" stroke-width="2"/>' + "".join(f'<text x="{20+i%3*10}" y="{22+i//3*10}" font-size="8" fill="{OUTLINE}" font-family="serif">⌘</text>' for i in range(9))
def funi_metalliche(): return f'<path d="M8 16 Q20 22 32 16 T56 16" stroke="#a0a0a8" stroke-width="3.5" fill="none"/><path d="M8 32 Q20 38 32 32 T56 32" stroke="#a0a0a8" stroke-width="3.5" fill="none"/><path d="M8 48 Q20 54 32 48 T56 48" stroke="#a0a0a8" stroke-width="3.5" fill="none"/>'
def frammento_stella(): return f'<polygon points="32,4 38,24 58,28 42,40 48,60 32,48 16,60 22,40 6,28 26,24" fill="#fff0a0" stroke="#d0a040" stroke-width="2"/><polygon points="32,4 36,24 32,40 28,24" fill="#ffffff" opacity="0.7"/>'
def occhio_titano(): return f'<ellipse cx="32" cy="32" rx="26" ry="14" fill="#fff" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="32" r="11" fill="#3050a0" stroke="{OUTLINE}" stroke-width="1.5"/><circle cx="32" cy="32" r="5" fill="#1a0e05"/><circle cx="29" cy="29" r="2" fill="#ffffff"/>'
def sigillo_re():  return f'<rect x="14" y="20" width="36" height="36" fill="#1a1208" stroke="{OUTLINE}" stroke-width="2"/><circle cx="32" cy="38" r="14" fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5"/><polygon points="32,28 36,36 44,36 38,42 40,50 32,46 24,50 26,42 20,36 28,36" fill="{OUTLINE}"/><rect x="22" y="6" width="20" height="14" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1.5"/>'
def muschio_blu(): return "".join(f'<circle cx="{14+(i%4)*12}" cy="{20+(i//4)*15}" r="{4+i%3}" fill="#4090c0" opacity="0.7"/>' for i in range(8)) + f'<rect x="6" y="48" width="52" height="10" fill="#5a4030" stroke="{OUTLINE}" stroke-width="1"/>'
def cristallo_radice(): return f'<polygon points="32,6 50,28 40,58 24,58 14,28" fill="#40c0a0" stroke="{OUTLINE}" stroke-width="2"/><polygon points="32,6 40,28 32,40 24,28" fill="#80e0c0" stroke="#40c0a0" stroke-width="1"/><circle cx="32" cy="34" r="4" fill="#ffffff" opacity="0.7"/>'
def radice_madre(): return f'<path d="M32 8 Q32 18 28 24 T22 36 T18 50 M32 8 Q34 16 38 24 T46 38 T50 52 M32 8 Q32 22 32 36 T32 56" stroke="#80c0a0" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="32" cy="8" r="6" fill="#a0e0c0" stroke="{OUTLINE}" stroke-width="1"/>'
def corona_titanica(): return f'<path d="M8 44 L14 20 L22 36 L32 14 L42 36 L50 20 L56 44 Z" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><rect x="8" y="44" width="48" height="14" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><circle cx="14" cy="20" r="3" fill="#1a0e05" stroke="#5a4848"/><circle cx="32" cy="14" r="3" fill="#1a0e05" stroke="#5a4848"/><circle cx="50" cy="20" r="3" fill="#1a0e05" stroke="#5a4848"/>'
def corona_attivata(): return f'<path d="M8 44 L14 20 L22 36 L32 14 L42 36 L50 20 L56 44 Z" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><rect x="8" y="44" width="48" height="14" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><circle cx="14" cy="20" r="4" fill="#fff0a0" stroke="#d0a040" stroke-width="1"><animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/></circle><circle cx="32" cy="14" r="4" fill="#80c0a0" stroke="#40c0a0" stroke-width="1"><animate attributeName="opacity" values="0.6;1;0.6" dur="2.4s" repeatCount="indefinite"/></circle><circle cx="50" cy="20" r="4" fill="#3050a0" stroke="#3050a0" stroke-width="1"><animate attributeName="opacity" values="0.6;1;0.6" dur="1.8s" repeatCount="indefinite"/></circle>'
def meccanismo_completo(): return f'<g transform="translate(22 32)"><circle r="14" fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5"/></g><g transform="translate(42 32)"><circle r="10" fill="#707068" stroke="{OUTLINE}" stroke-width="1.5"/></g>' + f'<text x="32" y="55" font-size="9" fill="{GOLD}" text-anchor="middle">⚙</text>'
def manovella_completa(): return f'<rect x="30" y="14" width="4" height="28" fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5"/><circle cx="32" cy="14" r="6" fill="#d4a060" stroke="{OUTLINE}" stroke-width="1.5"/><path d="M32 42 L48 50 L40 58 L24 58 L16 50 Z" fill="#c08850" stroke="{OUTLINE}" stroke-width="2"/>'
def manovella_temp(): return f'<rect x="30" y="14" width="4" height="44" fill="#c08850" stroke="{OUTLINE}" stroke-width="1.5"/><polygon points="26,8 38,8 36,14 28,14" fill="#5a3820" stroke="{OUTLINE}" stroke-width="1"/>'
def funi_metalliche_intrecciate(): return f'<path d="M8 32 Q20 16 32 32 T56 32" stroke="#a0a0a8" stroke-width="4" fill="none"/><path d="M8 32 Q20 48 32 32 T56 32" stroke="#a0a0a8" stroke-width="4" fill="none"/><rect x="6" y="28" width="52" height="8" fill="#5a5860" stroke="{OUTLINE}" stroke-width="1.5" opacity="0.7"/>'
def lente_smeraldo(): return f'<circle cx="32" cy="32" r="22" fill="none" stroke="#c08850" stroke-width="3"/><circle cx="32" cy="32" r="18" fill="#40a070" stroke="{OUTLINE}" stroke-width="1.5" opacity="0.85"/><ellipse cx="26" cy="26" rx="6" ry="4" fill="#80e0a0" opacity="0.6"/>'
def corona_titanica_step1(): return f'<path d="M8 44 L14 20 L22 36 L32 14 L42 36 L50 20 L56 44 Z" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><rect x="8" y="44" width="48" height="14" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><circle cx="14" cy="20" r="4" fill="#fff0a0" stroke="#d0a040" stroke-width="1"/>'
def corona_titanica_step2(): return f'<path d="M8 44 L14 20 L22 36 L32 14 L42 36 L50 20 L56 44 Z" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><rect x="8" y="44" width="48" height="14" fill="#3a3038" stroke="{OUTLINE}" stroke-width="2"/><circle cx="14" cy="20" r="4" fill="#fff0a0" stroke="#d0a040"/><circle cx="32" cy="14" r="4" fill="#3050a0" stroke="#3050a0"/>'
def lampada_eterna(): return f'<rect x="22" y="48" width="20" height="8" fill="#8a5030" stroke="{OUTLINE}" stroke-width="1.5"/><path d="M18 48 L46 48 L42 30 Q42 24 32 24 Q22 24 22 30 Z" fill="#c08850" stroke="{OUTLINE}" stroke-width="2"/><path d="M28 24 Q24 18 24 12 Q24 6 32 6 Q40 6 40 12 Q40 18 36 24 Z" fill="#fff0a0" stroke="#d0a040" stroke-width="1.5"><animate attributeName="opacity" values="0.7;1;0.7" dur="2.4s" repeatCount="indefinite"/></path><circle cx="32" cy="14" r="3" fill="#ffffff"/>'
# v1.4 new items
def conchiglia_offerta(): return f'''<g>
  <path d="M32 6 Q52 24 50 44 Q40 56 32 56 Q24 56 14 44 Q12 24 32 6 Z" fill="#f0d4b8" stroke="{OUTLINE}" stroke-width="2"/>
  <!-- Three concentric circles (the offering mark) -->
  <circle cx="32" cy="36" r="12" fill="none" stroke="#a06040" stroke-width="1.5"/>
  <circle cx="32" cy="36" r="8" fill="none" stroke="#a06040" stroke-width="1.2"/>
  <circle cx="32" cy="36" r="4" fill="#a06040"/>
  <!-- Ridges -->
  <path d="M28 12 Q32 30 36 12" stroke="#d0a080" stroke-width="1" fill="none"/>
  <path d="M22 18 Q32 32 42 18" stroke="#d0a080" stroke-width="1" fill="none"/>
</g>'''
def legno_stagionato(): return f'''<g>
  <rect x="4" y="24" width="56" height="16" fill="#5a3818" stroke="{OUTLINE}" stroke-width="2"/>
  <rect x="4" y="24" width="56" height="3" fill="#7a4820" opacity=".7"/>
  <line x1="4" y1="32" x2="60" y2="32" stroke="#3a2010" stroke-width="1"/>
  <!-- Wood grain -->
  <path d="M8 28 Q20 26 32 28 T60 28" stroke="#3a2010" stroke-width=".8" fill="none"/>
  <path d="M8 36 Q20 34 32 36 T60 36" stroke="#3a2010" stroke-width=".8" fill="none"/>
  <!-- Knot -->
  <ellipse cx="24" cy="32" rx="3" ry="5" fill="#2a1408" stroke="#3a2010" stroke-width="1"/>
  <circle cx="46" cy="30" r="2" fill="#2a1408"/>
</g>'''
def lima_arrugginita(): return f'''<g>
  <!-- Handle -->
  <rect x="6" y="28" width="16" height="8" fill="{WOOD}" stroke="{OUTLINE}" stroke-width="2"/>
  <rect x="6" y="28" width="16" height="2" fill="#5a3010" opacity=".7"/>
  <!-- File body with rust gradient -->
  <rect x="22" y="28" width="38" height="8" fill="#a05030" stroke="{OUTLINE}" stroke-width="2"/>
  <!-- Teeth pattern -->
  <g stroke="#3a1810" stroke-width=".6">
    {''.join(f'<line x1="{26+i*2}" y1="28" x2="{24+i*2}" y2="36"/>' for i in range(16))}
  </g>
  <!-- Rust specks -->
  <circle cx="32" cy="30" r="1" fill="#3a1810"/>
  <circle cx="44" cy="34" r=".8" fill="#3a1810"/>
  <circle cx="52" cy="31" r=".8" fill="#3a1810"/>
</g>'''
def bussola_antica(): return f'''<g>
  <!-- Outer brass ring -->
  <circle cx="32" cy="32" r="26" fill="#a07030" stroke="{OUTLINE}" stroke-width="2"/>
  <circle cx="32" cy="32" r="22" fill="#d4a040" stroke="{OUTLINE}" stroke-width="1.5"/>
  <!-- Dark face -->
  <circle cx="32" cy="32" r="18" fill="#2a1a0c" stroke="{OUTLINE}" stroke-width="1"/>
  <!-- Cardinal marks -->
  <text x="32" y="18" font-size="6" fill="#d4a040" text-anchor="middle" font-weight="bold">N</text>
  <text x="50" y="35" font-size="6" fill="#d4a040" text-anchor="middle">E</text>
  <text x="32" y="51" font-size="6" fill="#d4a040" text-anchor="middle">S</text>
  <text x="14" y="35" font-size="6" fill="#d4a040" text-anchor="middle">W</text>
  <!-- Needle (points NE toward lighthouse) -->
  <polygon points="32,14 34,32 32,50 30,32" fill="#c04030" stroke="{OUTLINE}" stroke-width="1">
    <animateTransform attributeName="transform" type="rotate" from="-10 32 32" to="10 32 32" dur="3s" repeatCount="indefinite" additive="sum" values="-10 32 32;10 32 32;-10 32 32"/>
  </polygon>
  <!-- Needle north tip -->
  <polygon points="32,14 34,32 30,32" fill="#e0a040"/>
  <!-- Pivot -->
  <circle cx="32" cy="32" r="2" fill="#f0e0a0"/>
</g>'''
def orchidea_lunare(): return f'''<g>
  <!-- Stem -->
  <path d="M32 58 Q30 46 32 32 Q34 22 32 12" stroke="#4a6a40" stroke-width="2" fill="none"/>
  <!-- 5 silver petals -->
  <ellipse cx="32" cy="18" rx="6" ry="10" fill="#e0e0f0" stroke="#8080a0" stroke-width="1"/>
  <ellipse cx="22" cy="24" rx="6" ry="10" fill="#e0e0f0" stroke="#8080a0" stroke-width="1" transform="rotate(-60 22 24)"/>
  <ellipse cx="42" cy="24" rx="6" ry="10" fill="#e0e0f0" stroke="#8080a0" stroke-width="1" transform="rotate(60 42 24)"/>
  <ellipse cx="26" cy="32" rx="6" ry="10" fill="#e0e0f0" stroke="#8080a0" stroke-width="1" transform="rotate(-30 26 32)"/>
  <ellipse cx="38" cy="32" rx="6" ry="10" fill="#e0e0f0" stroke="#8080a0" stroke-width="1" transform="rotate(30 38 32)"/>
  <!-- Center -->
  <circle cx="32" cy="26" r="4" fill="#a0a0c0" stroke="#6060a0" stroke-width="1"/>
  <circle cx="32" cy="26" r="1.5" fill="#fff0f0"/>
  <!-- Leaf -->
  <path d="M32 44 Q22 48 20 54 Q28 52 32 48" fill="#4a6a40" stroke="#2a3a20" stroke-width="1"/>
</g>'''

RENDERERS = {
    "legna": legna, "corda": corda, "bottiglia": bottiglia,
    "pietra_focaia": pietra_focaia, "conchiglia": conchiglia,
    "lama_antica": lama_antica, "artefatto_sacro": artefatto_sacro,
    "ramo_robusto": ramo_robusto, "bacche": bacche, "fiori": fiori,
    "chiodi_arrugginiti": chiodi_arrugginiti,
    "messaggio_bottiglia": messaggio_bottiglia, "rete_pesca": rete_pesca,
    "olio_vegetale": olio_vegetale, "resina": resina,
    "pianta_rara": pianta_rara, "erbe_secche": erbe_secche,
    "piccone": piccone, "cristallo_vulcanico": cristallo_vulcanico,
    "frammento_mappa": frammento_mappa,
    "diario_guardiano": diario_guardiano, "gemma_potere": gemma_potere,
    "tavoletta_antica": tavoletta_antica,
    "attrezzatura_sub": attrezzatura_sub, "perla_nera": perla_nera,
    "sigillo_antico": sigillo_antico, "tridente": tridente,
    "corona_corallo": corona_corallo, "torcia": torcia,
    "machete": machete, "medaglione": medaglione,
    "chiave_faro": chiave_faro, "chiave_antica": chiave_antica,
    "antidoto": antidoto,
    # Atto II
    "spore_lumino": spore_lumino, "ingranaggio": ingranaggio, "ruota_dentata": ruota_dentata,
    "binario_ferro": binario_ferro, "martello_rame": martello_rame,
    "pendolo_ottone": pendolo_ottone, "valvola_vapore": valvola_vapore,
    "ampolla": ampolla, "catena_oro": catena_oro,
    "tavoletta_runica": tavoletta_runica, "funi_metalliche": funi_metalliche,
    "frammento_stella": frammento_stella, "occhio_titano": occhio_titano,
    "sigillo_re": sigillo_re, "muschio_blu": muschio_blu,
    "cristallo_radice": cristallo_radice, "radice_madre": radice_madre,
    "corona_titanica": corona_titanica, "corona_attivata": corona_attivata,
    "meccanismo_completo": meccanismo_completo,
    "manovella_completa": manovella_completa, "manovella_temp": manovella_temp,
    "funi_metalliche_intrecciate": funi_metalliche_intrecciate,
    "lente_smeraldo": lente_smeraldo,
    "corona_titanica_step1": corona_titanica_step1,
    "corona_titanica_step2": corona_titanica_step2,
    "lampada_eterna": lampada_eterna,
    "conchiglia_offerta": conchiglia_offerta,
    "legno_stagionato": legno_stagionato,
    "lima_arrugginita": lima_arrugginita,
    "bussola_antica": bussola_antica,
    "orchidea_lunare": orchidea_lunare,
}


def wrap(inner, name):
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" {VIEWBOX} '
        f'width="64" height="64">\n'
        f'  <title>{name}</title>\n'
        f'  <rect width="64" height="64" fill="#1a1208" rx="4"/>\n'
        f'  {inner}\n'
        f'</svg>\n'
    )


def placeholder(iid, name):
    letters = "".join(ch for ch in name if ch.isalpha()).upper()[:2] or "?"
    return (
        f'<circle cx="32" cy="32" r="24" fill="{GOLD}" stroke="{OUTLINE}" stroke-width="2"/>'
        f'<text x="32" y="40" text-anchor="middle" font-size="22" fill="{OUTLINE}" '
        f'font-family="Georgia" font-weight="bold">{letters}</text>'
    )


written = 0
missing = []
for iid, item in WORLD["items"].items():
    r = RENDERERS.get(iid)
    inner = r() if r else placeholder(iid, iid)
    if not r:
        missing.append(iid)
    (OUT / f"{iid}.svg").write_text(wrap(inner, item["nome_completo"]), encoding="utf-8")
    written += 1

print(f"Wrote {written} SVG icons.")
if missing:
    print("Placeholder usato per:", missing)
