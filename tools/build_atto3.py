#!/usr/bin/env python3
"""ATTO III — L'Oceano Interno
Oltre la Radice del Mondo, una via verso l'Oceano Sotterraneo.
8 stanze + Prologo (1 stanza) + 5 finali alternativi.

Genera data/atto3.json — fuso da export_world.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "atto3.json"

# ─────────────────────────────────────────────────────────────────────
# PROLOGO — la nave prima del naufragio (1 stanza giocabile, scelta classe)
# ─────────────────────────────────────────────────────────────────────
PROLOGO_STANZA = {
    "ponte_nave": {
        "nome": "Ponte della Procyon",
        "descrizione": (
            "La Procyon scricchiola sotto la prima onda davvero alta. Sei sul ponte, "
            "tiene male il mare grosso, e a poppa il timoniere ha lasciato il timone "
            "per fissare la cassa di legno alla rete.\n\n"
            "Hai pochi minuti prima che la prossima ondata ti porti via tutto. "
            "Qui sotto, nella stiva, ci sono ancora i tuoi effetti personali. "
            "Cosa scegli di portare con te?"
        ),
        "descrizione_breve": "Ponte della Procyon nella tempesta. Pochi secondi per scegliere.",
        "uscite": {},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "stiva": "Apri il portello della stiva. Tre oggetti rimasti: una bussola di tuo padre, una lettera mai consegnata, una chiave di ferro che non ricordi a cosa apra.",
            "timoniere": "Il timoniere urla qualcosa che il vento ti porta via. Ha la barba fradicia e gli occhi pieni di paura.",
            "mare": "Il mare. Già lo conosci. Già ti aspetta.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────
# ATTO III — 8 nuove stanze sotto la Radice
# ─────────────────────────────────────────────────────────────────────
ROOMS_ATTO3 = {
    "discesa_radice": {
        "nome": "Discesa dalla Radice",
        "descrizione": (
            "Sotto le radici dell'Albero di Luce, una scala di pietra calcarea scende "
            "in un'acqua azzurra fluorescente. L'aria si fa salata. Il rumore di onde "
            "lontane risuona sotto gli archi naturali.\n\n"
            "Hai disceso il faro, hai disceso il pozzo, ora discendi anche questo: "
            "perché sai che oltre la Radice c'è un mare. Un mare interno, un mare "
            "che nessuno ha mai navigato."
        ),
        "descrizione_breve": "Scala calcarea sotto la Radice. L'acqua azzurra ti chiama.",
        "uscite": {"su": "radice_mondo", "giu": "spiaggia_interna"},
        "uscite_bloccate": {},
        "oggetti": ["spore_radice"],
        "npcs": [],
        "esaminabili": {
            "scala": "Scala scolpita prima della pietra che la contiene. Le impronte sono di esseri leggeri come bambini.",
            "acqua_blu": "L'acqua brilla di una luce viva. Non è chimica: è qualcosa che vive disciolto.",
            "archi_naturali": "Archi di pietra erosi da millenni di gocciolio. Bellissimi.",
        },
    },
    "spiaggia_interna": {
        "nome": "Spiaggia dell'Oceano Interno",
        "descrizione": (
            "Una spiaggia dentro la pietra. Sabbia di quarzo nero che scintilla, mare "
            "azzurro fluorescente che lecca la riva senza onde. Sopra, niente cielo: "
            "una volta di pietra alta come una cattedrale, costellata di cristalli "
            "che imitano stelle.\n\n"
            "All'orizzonte, tre piccole isole: una di pietra, una di metallo, una "
            "di luce verde. Una barca minuscola — fatta come una foglia — è arenata "
            "sulla sabbia. Ti aspetta."
        ),
        "descrizione_breve": "Spiaggia interna. Tre isole all'orizzonte. Barca-foglia sulla riva.",
        "uscite": {"su": "discesa_radice", "dentro": "altare_oceano", "giu": "fondale_dimenticato"},
        "uscite_bloccate": {
            "ovest": {"condizione": "oggetto:barca_foglia",
                      "messaggio": "Devi prima raccogliere la barca-foglia per attraversare l'oceano interno."},
            "est":   {"condizione": "oggetto:barca_foglia",
                      "messaggio": "Senza la barca non puoi raggiungere l'isola di metallo."},
            "nord":  {"condizione": "oggetto:barca_foglia",
                      "messaggio": "Senza la barca non puoi raggiungere l'isola di luce."},
        },
        "oggetti": ["barca_foglia"],
        "npcs": [],
        "esaminabili": {
            "sabbia_quarzo": "Sabbia che scintilla quando la sposti. Ogni grano è un piccolo cristallo.",
            "stelle_pietra": "I cristalli sul soffitto disegnano costellazioni che riconosci — e altre che no.",
            "isole": "Tre isole. Una di pietra grezza. Una di metallo lucido. Una di luce verde.",
            "barca_foglia": "Una barca a forma di foglia gigante, levigata. Galleggerà.",
        },
    },
    "isola_pietra": {
        "nome": "Isola della Pietra",
        "descrizione": (
            "Un cumulo di pietra al centro dell'oceano interno. Niente vegetazione, "
            "niente acqua dolce. Al centro, scolpito direttamente nella roccia, "
            "un volto enorme con occhi chiusi. La sua bocca è una grotta verticale "
            "che si chiude quando ti avvicini.\n\n"
            "Sulla pietra accanto al volto, un'iscrizione in caratteri antichi: "
            "«Chi torna ha già scelto.»"
        ),
        "descrizione_breve": "Isola di sola pietra. Volto scolpito gigante con bocca-grotta.",
        "uscite": {"sud": "spiaggia_interna"},
        "uscite_bloccate": {},
        "oggetti": ["pietra_decisione"],
        "npcs": [],
        "esaminabili": {
            "volto": "Un volto che potrebbe essere il tuo, da vecchio. O un Costruttore. O nessuno.",
            "bocca_grotta": "La bocca si chiude quando provi ad entrare. Conosce qualcosa che tu non sai.",
            "iscrizione_pietra": "Caratteri che ora capisci senza fatica. «Chi torna ha già scelto.»",
        },
    },
    "isola_metallo": {
        "nome": "Isola del Metallo",
        "descrizione": (
            "Un'isola interamente di bronzo levigato dal mare interno. Al centro, una "
            "macchina circolare alta tre metri, fatta di ingranaggi che ruotano lenti. "
            "Sulla macchina, sette leve. Sopra le leve, un cartiglio: «Solo una si abbassa "
            "veramente.»\n\n"
            "Una voce metallica risuona dall'interno: «Hai scelto di venire? O sei stato portato?»"
        ),
        "descrizione_breve": "Isola di bronzo. Macchina con sette leve. Voce metallica interna.",
        "uscite": {"sud": "spiaggia_interna"},
        "uscite_bloccate": {},
        "oggetti": ["leva_settima"],
        "npcs": [],
        "esaminabili": {
            "macchina_circolare": "Una macchina che continua a funzionare anche se non sa più cosa.",
            "sette_leve": "Sette leve identiche. Solo una si abbassa veramente — le altre fanno finta.",
            "voce_metallica": "Una voce che parla dall'interno della macchina. Non puoi vederla, ma ti vede.",
        },
    },
    "isola_luce": {
        "nome": "Isola della Luce",
        "descrizione": (
            "L'isola che brilla di luce verde — l'avevi vista da lontano. Da vicino non "
            "è terra: è un'increspatura dell'acqua tenuta ferma da qualcosa, e dentro "
            "l'increspatura cammina una figura. Non ha età, non ha sesso, non ha contorni.\n\n"
            "«Ti aspettavo,» dice senza muovere bocca. «Sei tornato. Bentornato.»"
        ),
        "descrizione_breve": "Isola di luce. Figura senza contorni che parla.",
        "uscite": {"sud": "spiaggia_interna"},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": ["figura_luce"],
        "esaminabili": {
            "increspatura": "Acqua trattenuta da una memoria. È così che si fanno le isole, qui.",
            "figura": "Più la guardi, più sembra avere il tuo volto. O il volto di tutti quelli che ami.",
        },
    },
    "altare_oceano": {
        "nome": "Altare dell'Oceano",
        "descrizione": (
            "Un altare emerge dalla sabbia interna, di pietra nera. Sopra l'altare, "
            "tre coppe vuote. Su ogni coppa una parola: PIETRA, METALLO, LUCE.\n\n"
            "Hai i tre simboli con te (o ne avrai). Ognuno aprirà un finale diverso."
        ),
        "descrizione_breve": "Altare con tre coppe: pietra, metallo, luce. Scegli un finale.",
        "uscite": {"giu": "spiaggia_interna"},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "altare_nero": "Pietra che assorbe la luce. Pesa più di quanto sembri.",
            "coppa_pietra": "PIETRA — il finale del custode. Resti per sempre.",
            "coppa_metallo": "METALLO — il finale del costruttore. Diventi macchina.",
            "coppa_luce": "LUCE — il finale del viaggiatore. Trasformi e parti.",
        },
    },
    "fondale_dimenticato": {
        "nome": "Fondale Dimenticato",
        "descrizione": (
            "Sotto la spiaggia interna, immergendoti, scopri un fondale piatto coperto di "
            "oggetti dimenticati: orologi che non segnano l'ora, libri che non si aprono, "
            "sedie senza nessuno seduto.\n\n"
            "È il deposito delle cose che la gente lascia nel mondo di sopra senza accorgersi.\n\n"
            "In fondo, una crepa più scura. Qualcosa di antico pulsa dentro."
        ),
        "descrizione_breve": "Fondale di oggetti dimenticati. Crepa scura in fondo.",
        "uscite": {"su": "spiaggia_interna", "giu": "abisso_finale"},
        "uscite_bloccate": {},
        "oggetti": ["chiave_dimenticata"],
        "npcs": [],
        "esaminabili": {
            "orologio_fermo": "Un orologio fermo. Sul retro, un'incisione: «Per Rebecca, dal primo amore.» Non hai mai amato una Rebecca.",
            "libro_chiuso": "Un libro che non si apre. La copertina è bianca, ma la senti pesante di parole.",
            "sedia_vuota": "Una sedia vuota. Qualcuno l'aveva amata abbastanza da non sostituirla mai.",
        },
    },
    "abisso_finale": {
        "nome": "Abisso dell'Oceano Interno",
        "descrizione": (
            "Da una crepa nella spiaggia interna, una voragine scende — e scende — fino "
            "a un punto bianco, lontanissimo. Lì sotto qualcosa pulsa: un cuore non umano, "
            "antichissimo. Forse il vero cuore dell'isola.\n\n"
            "Una scala a chiocciola, sottile come un filo, ti aspetta."
        ),
        "descrizione_breve": "Voragine nella spiaggia interna. Cuore non umano in fondo.",
        "uscite": {"su": "spiaggia_interna"},
        "uscite_bloccate": {
            "giu": {"condizione": "oggetto:corona_attivata",
                    "messaggio": "Senza la Corona Titanica attivata, scendere significa morire."}
        },
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "punto_bianco": "Pulsa lentamente, come un battito. Non sai dire se sia luce o vita.",
            "scala_filo": "Una scala a chiocciola sottile come un filo. Per scendere serve coraggio. E qualcosa di più.",
            "cuore_pulsante": "Il cuore dell'isola. Non è una metafora.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────
# Nuovi oggetti Atto III
# ─────────────────────────────────────────────────────────────────────
def make_item(nome, completo, desc, alias=None):
    return {"nome": nome, "nome_completo": completo, "descrizione": desc,
            "descrizione_terra": f"Trovi {completo.lower()} qui.",
            "portatile": True, "nascosto": False, "alias": alias or [nome]}

ITEMS_ATTO3 = {
    "spore_radice": make_item("spore_radice", "Spore della Radice",
        "Spore raccolte alla base dell'Albero di Luce. Brillano debolmente.", ["spore_radice"]),
    "barca_foglia": make_item("barca_foglia", "Barca-foglia",
        "Una barca a forma di foglia gigante. Ti trasporta sulle isole dell'oceano interno.", ["barca", "foglia"]),
    "pietra_decisione": make_item("pietra_decisione", "Pietra della Decisione",
        "Una pietra liscia che pesa più di quanto dovrebbe. La porti come un peso volontario.", ["pietra", "decisione"]),
    "leva_settima": make_item("leva_settima", "La Settima Leva",
        "L'unica leva vera tra sette identiche. Hai dovuto sentirla con le dita per riconoscerla.", ["leva", "settima"]),
    "chiave_dimenticata": make_item("chiave_dimenticata", "Chiave dimenticata",
        "Una chiave qualunque, di qualcuno. Apre qualcosa che non sai. Forse dentro di te.", ["chiave_dimenticata"]),
    # Prologo
    "bussola_padre": make_item("bussola_padre", "Bussola di tuo padre",
        "Una bussola di rame che apparteneva a tuo padre. L'ago punta sempre verso ciò che ti manca.", ["bussola_padre"]),
    "lettera_mai_consegnata": make_item("lettera", "Lettera mai consegnata",
        "Una lettera scritta a qualcuno che amavi e che non hai più rivisto. Non la consegnerai mai.", ["lettera"]),
    "chiave_ferro_dimenticata": make_item("chiave_ferro", "Chiave di ferro",
        "Una chiave di ferro che non ricordi a cosa apra. La porti perché non riesci a lasciarla.", ["chiave_ferro"]),
}

# ─────────────────────────────────────────────────────────────────────
# Nuovi NPC
# ─────────────────────────────────────────────────────────────────────
CHARACTERS_ATTO3 = {
    "figura_luce": {
        "nome": "La Figura di Luce",
        "descrizione": "Una figura senza età, sesso, contorni. Quando la guardi prende il volto di chi ami. Quando le parli, parla con la tua voce.",
        "alias": ["figura", "luce", "specchio"],
        "stanza": "isola_luce",
    },
}

DIALOGUES_ATTO3 = {
    "figura_luce": [
        {
            "saluto": "«Sei tornato.»\n\n«Sei sempre stato qui. Ogni Naufrago è lo stesso Naufrago. Ogni Costruttore è lo stesso Costruttore. C'è solo uno di noi, e siamo tu.»",
            "opzioni": [
                {"testo": "Chi sei davvero?",
                 "risposta": "«Sono ciò che resta quando smetti di essere te. Sono il fondo. Sono la luce sotto le luci. Per i Costruttori ero la Madre. Per i marinai sono il Faro. Per te sono qualunque cosa tu mi chieda di essere.»"},
                {"testo": "Posso scegliere come finire?",
                 "risposta": "«Tre coppe sull'altare nero, in cima a quel sentiero. PIETRA: resti come custode. METALLO: diventi parte della macchina. LUCE: parti, e con te parte il faro. Scegli ciò che ti somiglia di più.»"},
                {"testo": "C'è una quarta scelta?",
                 "risposta": "«C'è sempre una quarta scelta. Si chiama abisso, ed è scendere ancora più giù. Solo chi indossa la Corona ATTIVATA può sopravvivere. Lì sotto pulsa il vero cuore dell'isola — e ti riconoscerà.»"},
                {"testo": "Una quinta?",
                 "risposta": "«La quinta è la più semplice e la più ardua: tornare al ponte della Procyon e scegliere di non partire mai. Ma per farlo servirebbe un dono che nessuno mai ha avuto: poter cambiare il proprio passato. Non posso dartelo. Nessuno può.»"},
                {"fine": True, "testo": "Vado a scegliere."},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────
# Cinque finali
# ─────────────────────────────────────────────────────────────────────
FINALI_V2 = {
    "soccorso": (
        "Aspetti. La luce del faro chiama. Una nave arriva. Ti porta via.\n\n"
        "Non saprai mai cosa hai abbandonato.\n\n~ Fine: Soccorso ~"
    ),
    "corona_titanica": (
        "Indossi la Corona. La Radice ti accoglie. Sai tutto, di colpo. Sei custode.\n\n"
        "L'isola respira con te. Aspetti il prossimo.\n\n~ Fine: Corona Titanica ~"
    ),
    "pietra": (
        "Bevi dalla coppa di PIETRA.\n\n"
        "Senti i tuoi piedi mettere radici nella sabbia. La pelle si fa scoglio. "
        "Gli occhi si fanno cristallo. In pochi minuti diventi un'altra statua "
        "dei Titani — una nuova, l'ottava più una.\n\n"
        "Stai qui. Non parti più. Vedi il mare, il sole, la luna, le navi, i naufraghi.\n\n"
        "Tutti i prossimi naufraghi vedranno te.\n\n~ Fine: Custode di Pietra ~"
    ),
    "metallo": (
        "Bevi dalla coppa di METALLO.\n\n"
        "Il tuo corpo si raffredda lentamente. Le ossa diventano rame, il cuore una "
        "ruota dentata. Gli ingranaggi della macchina circolare si aprono per te. "
        "Entri. Diventi un automa, parte della macchina che continua a funzionare "
        "anche se non sa più cosa.\n\n"
        "Forse un giorno qualcuno entrerà. Forse no.\n\n~ Fine: Costruttore Eterno ~"
    ),
    "luce": (
        "Bevi dalla coppa di LUCE.\n\n"
        "Non senti più il peso del corpo. Diventi luce — la luce che brilla nell'oceano "
        "interno, che brilla nel faro, che brilla nei sogni di chi è altrove.\n\n"
        "Il faro lassù si spegne. Il mondo perderà il suo richiamo. Forse era il momento.\n\n"
        "Tu sei dove vuoi essere, sempre. E vai.\n\n~ Fine: Viaggiatore di Luce ~"
    ),
    "abisso_segreto": (
        "Indossi la Corona. Scendi nell'abisso interno. Il punto bianco si apre.\n\n"
        "Il vero cuore dell'isola è una creatura più antica di te, più antica dei "
        "Costruttori. Ti riconosce. Non è ostile. È una madre. Sussurra il tuo nome — "
        "il tuo VERO nome, quello che non ricordi — e all'improvviso ricordi.\n\n"
        "Non sei un naufrago. Sei un figlio dell'isola tornato. Tutto questo è casa.\n\n"
        "Non c'è bisogno di scegliere niente. Sei.\n\n~ Fine Segreto: Casa ~"
    ),
}

# ─────────────────────────────────────────────────────────────────────
# Room actions per i finali
# ─────────────────────────────────────────────────────────────────────
ROOM_ACTIONS_ATTO3 = {
    ("pietra_decisione", "altare_oceano"): {
        "messaggio": "Posi la Pietra della Decisione nella coppa di PIETRA. La pietra si scioglie come zucchero nell'acqua. La coppa si riempie di liquido grigio.",
        "flag": "fine_pietra_pronta", "consuma": True,
    },
    ("leva_settima", "altare_oceano"): {
        "messaggio": "Posi la Settima Leva nella coppa di METALLO. La leva si scioglie come neve. La coppa si riempie di liquido bronzeo.",
        "flag": "fine_metallo_pronta", "consuma": True,
    },
    ("spore_radice", "altare_oceano"): {
        "messaggio": "Posi le spore della Radice nella coppa di LUCE. Le spore si dissolvono in fluorescenza. La coppa si riempie di liquido verde-azzurro.",
        "flag": "fine_luce_pronta", "consuma": True,
    },
}

# Map positions Atto III
MAP_POSITIONS_ATTO3 = {
    "ponte_nave":         {"x": 6,  "y": 50, "atto": 0},
    "discesa_radice":     {"x": 92, "y": 38, "atto": 3},
    "spiaggia_interna":   {"x": 88, "y": 50, "atto": 3},
    "isola_pietra":       {"x": 78, "y": 60, "atto": 3},
    "isola_metallo":      {"x": 88, "y": 65, "atto": 3},
    "isola_luce":         {"x": 96, "y": 60, "atto": 3},
    "altare_oceano":      {"x": 88, "y": 75, "atto": 3},
    "fondale_dimenticato":{"x": 92, "y": 88, "atto": 3},
    "abisso_finale":      {"x": 96, "y": 92, "atto": 3},
}

BLOCKED_DESTS_ATTO3 = {
    "radice_mondo::giu": "discesa_radice",
    "spiaggia_interna::ovest": "isola_pietra",
    "spiaggia_interna::est": "isola_metallo",
    "spiaggia_interna::nord": "isola_luce",
    "abisso_finale::giu": "fine_segreto_abisso",
}

# ─────────────────────────────────────────────────────────────────────
# Patches per radice_mondo: aggiungere uscita "giu" verso discesa_radice
# (gated dalla scelta player di scendere ancora)
# ─────────────────────────────────────────────────────────────────────
ROOM_PATCHES_ATTO3 = {
    "radice_mondo": {
        "uscite_bloccate_add": {
            "giu": {"condizione": "flag:vuoi_scendere_ancora",
                    "messaggio": "Sotto la Radice c'è un altro mondo. Per scendere devi voler davvero non tornare uguale."}
        },
        "esaminabili_add": {
            "scala_oceano": "Sotto le radici dell'Albero, una scala calcarea scende. Conduce a un mare interno. Per andarci devi accettare di non tornare uguale.",
        },
    },
}

# Output
def tk(d): return {"::".join(k): v for k, v in d.items()}

atto3 = {
    "rooms": {**ROOMS_ATTO3, **PROLOGO_STANZA},
    "items": ITEMS_ATTO3,
    "characters": CHARACTERS_ATTO3,
    "dialogues": DIALOGUES_ATTO3,
    "room_actions": tk(ROOM_ACTIONS_ATTO3),
    "blocked_destinations": BLOCKED_DESTS_ATTO3,
    "room_patches": ROOM_PATCHES_ATTO3,
    "map_positions": MAP_POSITIONS_ATTO3,
    "finali_v2": FINALI_V2,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(atto3, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  rooms={len(ROOMS_ATTO3)}+1prologo items={len(ITEMS_ATTO3)} npcs={len(CHARACTERS_ATTO3)} actions={len(ROOM_ACTIONS_ATTO3)} finali={len(FINALI_V2)}")
