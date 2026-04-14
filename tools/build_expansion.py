#!/usr/bin/env python3
"""ATTO II — Le Profondità.
Quando il faro si accende, invece di terminare, rivela un pozzo che scende
nelle profondità dell'isola. Là sotto, una civiltà-macchina perduta attende.
Stile: Syberia + Viaggio al centro della Terra.

Genera data/expansion.json — viene fuso da export_world.py con il mondo base.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "expansion.json"

# ─────────────────────────────────────────────────────────────────────
# STANZE — 12 nuove location sotterranee
# ─────────────────────────────────────────────────────────────────────
ROOMS = {
    "pozzo_faro": {
        "nome": "Il Pozzo del Faro",
        "descrizione": (
            "Quando la fiamma del faro si è alzata al cielo, qualcosa si è mosso sotto "
            "i tuoi piedi. Il pavimento di pietra del faro si è aperto come un fiore di "
            "metallo, rivelando un pozzo verticale di pietra nera. Una scala a chiocciola "
            "scende nell'oscurità, illuminata da una luce verde-azzurra che pulsa dal "
            "basso come un battito cardiaco lento.\n\n"
            "L'aria che sale dal pozzo è fredda e profuma di pietra umida e di qualcosa "
            "di più antico — un odore di metallo lavorato e di tempo dimenticato."
        ),
        "descrizione_breve": "Pozzo verticale del faro. Una scala a chiocciola scende.",
        "uscite": {"su": "faro", "giu": "cripta_meccanica"},
        "uscite_bloccate": {},
        "oggetti": ["spore_lumino"],
        "npcs": [],
        "esaminabili": {
            "pavimento": "Lastre di pietra ad incastro perfetto, con motivi geometrici a spirale. Non sono stati posati, sono stati cresciuti — come se la pietra stessa fosse stata coltivata.",
            "scala": "Una scala a chiocciola di pietra basaltica. I gradini sono consumati al centro: migliaia di passi prima dei tuoi.",
            "luce_verde": "La luce viene da molto in basso. Non è fuoco — è qualcosa di vivente. Pulsa lentamente, come un respiro.",
        },
    },
    "cripta_meccanica": {
        "nome": "Cripta Meccanica",
        "descrizione": (
            "La scala finisce in una sala bassa con il soffitto a volta sostenuto da "
            "pilastri di ferro nero. Lungo le pareti, scaffali di bronzo ospitano file "
            "di piccoli ingranaggi di ogni dimensione, alcuni ancora coperti di olio "
            "fresco — come se qualcuno li avesse lubrificati ieri.\n\n"
            "Al centro della sala, un piedistallo cilindrico ruota lentamente su sé stesso "
            "con un ronzio appena percettibile. A nord, un corridoio si addentra nella "
            "roccia. A est, un'apertura più stretta lascia uscire un sibilo di vapore."
        ),
        "descrizione_breve": "Anticamera della città-macchina. Scaffali di ingranaggi, piedistallo rotante.",
        "uscite": {"su": "pozzo_faro", "nord": "sala_ingranaggi"},
        "uscite_bloccate": {"est": {"condizione": "flag:valvola_installata",
                                     "messaggio": "Il sibilo di vapore è troppo intenso. Senza una valvola che regoli la pressione, il corridoio è una camera di morte."}},
        "oggetti": ["ingranaggio", "ruota_dentata"],
        "npcs": [],
        "esaminabili": {
            "piedistallo": "Una colonna di ottone ruota su sé stessa con un movimento perfetto, come se nulla l'avesse mai fermata. Sopra, l'incisione di un occhio aperto.",
            "scaffali": "Ingranaggi di ogni misura, ordinati per diametro. Olio fresco sulle dita: qualcuno se ne prende ancora cura.",
            "iscrizione": "Un'iscrizione sulla parete in caratteri sconosciuti. Riconosci solo un simbolo: tre cerchi concentrici, come una mira.",
        },
    },
    "sala_ingranaggi": {
        "nome": "Sala degli Ingranaggi",
        "descrizione": (
            "Resti senza fiato. La sala è grande come una cattedrale, e ogni superficie — "
            "pareti, soffitto, pavimento — è coperta di ingranaggi che ruotano lentamente, "
            "incastrati gli uni negli altri in un balletto matematico di metallo. Il rumore "
            "è quello di un orologio gigantesco che batte un tempo sconosciuto.\n\n"
            "Al centro, una piattaforma circolare di ferro è ferma. Una manovella ne sporge "
            "sul lato, ma manca il pomello. A ovest si apre l'archivio, a est l'osservatorio. "
            "A nord, una porta di bronzo massiccio attende — chiusa.\n\n"
            "Su un banco di lavoro laterale, fra strumenti vari, riconosci una valvola di "
            "rame e ferro per regolare il vapore."
        ),
        "descrizione_breve": "Cattedrale di ingranaggi rotanti. Piattaforma centrale, manovella senza pomello, banco con valvola.",
        "uscite": {"sud": "cripta_meccanica", "ovest": "archivio", "est": "osservatorio"},
        "uscite_bloccate": {"nord": {"condizione": "flag:cuore_riattivato",
                                      "messaggio": "La porta di bronzo è inerte. Non c'è serratura, non c'è maniglia. Aspetta qualcosa che la richiami in vita."}},
        "oggetti": ["binario_ferro", "martello_rame", "valvola_vapore"],
        "npcs": [],
        "esaminabili": {
            "piattaforma": "Una piattaforma circolare di ferro nero. Non si muove. La manovella laterale gira a vuoto: dovrebbe terminare con un pomello che manca.",
            "manovella": "L'asta è di ottone lucido. Sulla cima, una flangia esagonale dove evidentemente si avvitava qualcosa.",
            "ingranaggi_grandi": "Gli ingranaggi più grandi sono alti come case. Ruotano senza fretta, come se avessero tutto il tempo del mondo.",
        },
    },
    "corridoio_vapore": {
        "nome": "Corridoio del Vapore",
        "descrizione": (
            "Il corridoio è stretto e umido, attraversato da grossi tubi di rame che "
            "sibilano sotto pressione. La valvola che hai installato regola il flusso, "
            "ma l'aria è ancora densa e calda, e il pavimento è coperto da uno strato di "
            "condensa che riflette la luce verde-azzurra.\n\n"
            "All'estremità del corridoio, una porta bassa porta a quella che doveva essere "
            "la forgia degli antichi."
        ),
        "descrizione_breve": "Corridoio di tubi di rame sibilanti. Conduce alla forgia.",
        "uscite": {"ovest": "cripta_meccanica", "est": "forgia_antica"},
        "uscite_bloccate": {},
        "oggetti": ["catena_oro"],
        "npcs": [],
        "esaminabili": {
            "tubi": "Tubi di rame del diametro di un braccio, percorsi da vapore caldo. Le giunture sono lavorate a mano.",
            "condensa": "L'acqua sul pavimento riflette la luce in pozze instabili. Stilla anche dal soffitto.",
            "valvola": "La valvola che hai installato gira ritmicamente, dosando il vapore in respiri controllati.",
        },
    },
    "forgia_antica": {
        "nome": "Forgia Antica",
        "descrizione": (
            "La sala è dominata da una grande fornace ottagonale ancora accesa. Dentro, "
            "il fuoco non è di legno: è qualcosa di liquido e arancione che scorre e si "
            "raffredda in disegni mai uguali. Davanti alla fornace, due automi di rame "
            "alti come uomini si muovono al rallentatore, battendo con martelli infiniti "
            "una lama che non si finisce mai di forgiare.\n\n"
            "Su un tavolo laterale, strumenti abbandonati. In un angolo, un piccolo "
            "altare con un calice di pietra al centro — vuoto."
        ),
        "descrizione_breve": "Forgia ancora attiva con automi di rame. Altare con calice vuoto.",
        "uscite": {"ovest": "corridoio_vapore"},
        "uscite_bloccate": {},
        "oggetti": ["pendolo_ottone", "ampolla"],
        "npcs": [],
        "esaminabili": {
            "fornace": "Il fuoco non è fuoco. È un metallo liquido che brucia di vita propria. Guardarlo a lungo fa male agli occhi.",
            "automi": "Due figure di rame alte come te. I loro volti sono maschere lisce. Battono il martello con perfetta cadenza, ignorandoti.",
            "tavolo": "Strumenti da fabbro: pinze, tenaglie, lime. Una fila di chiavi inglesi di tutte le misure. La polvere è uno strato sottile e uniforme: lavoro fermo da poco.",
            "altare": "Un altare di basalto con un calice di pietra al centro. Il calice ha una scanalatura interna come per ricevere un liquido sacro.",
        },
    },
    "archivio": {
        "nome": "L'Archivio Senza Fine",
        "descrizione": (
            "Una sala circolare a sette piani, con scaffali che salgono fino a perdersi nel "
            "buio. Una scala a spirale corre lungo le pareti. I libri non sono di carta — "
            "sono lastre di metallo sottile, incise. Migliaia. Centomila.\n\n"
            "Al centro, su un piedistallo, fluttua una figura traslucida: un volto di donna "
            "fatto di luce, gli occhi chiusi. Le mani conserte. Non si muove, ma stai "
            "respirando troppo forte, e improvvisamente apre gli occhi."
        ),
        "descrizione_breve": "Biblioteca circolare a sette piani. L'Archivista fluttua al centro.",
        "uscite": {"est": "sala_ingranaggi"},
        "uscite_bloccate": {},
        "oggetti": ["funi_metalliche", "tavoletta_runica"],
        "npcs": ["archivista"],
        "esaminabili": {
            "scaffali": "Lastre di metallo sottile, ognuna incisa con migliaia di simboli minutissimi. Un'intera civiltà conservata.",
            "scala_spirale": "Sale fino al settimo piano, dove l'oscurità inghiotte la luce. I gradini sono fatti per piedi più piccoli dei tuoi.",
            "lastre_metallo": "Provi a sollevare una lastra: pesa come una pagina. È metallo, ma flessibile come carta. Tecnologia che non comprendi.",
        },
    },
    "osservatorio": {
        "nome": "Osservatorio Sotterraneo",
        "descrizione": (
            "Una sala emisferica con un soffitto a cupola che — incredibile — proietta sopra "
            "di te il cielo notturno. Ma non è il cielo che vedevi sull'isola: queste sono "
            "stelle che non hai mai visto, costellazioni di un mondo prima del tuo.\n\n"
            "Al centro, un grande astrolabio di ottone con leve, pulsanti e una lente vuota "
            "in cima dove evidentemente si incastrava qualcosa. Sul muro, un mosaico di tre "
            "stelle in fila che pulsa ritmicamente."
        ),
        "descrizione_breve": "Osservatorio col cielo proiettato. Astrolabio con lente mancante.",
        "uscite": {"ovest": "sala_ingranaggi"},
        "uscite_bloccate": {"dentro": {"condizione": "flag:stelle_allineate",
                                        "messaggio": "Le stelle del soffitto si muovono in una danza che non sai leggere. Devi prima allinearle."}},
        "oggetti": ["frammento_stella"],
        "npcs": [],
        "esaminabili": {
            "soffitto": "Stelle proiettate da un meccanismo nascosto. Riconosci alcune costellazioni distorte; altre sono completamente nuove.",
            "astrolabio": "Un meraviglioso astrolabio di ottone. La lente in cima manca: una scanalatura circolare ne aspetta una nuova, di colore verde.",
            "mosaico": "Tre stelle in fila — la cintura di una costellazione antica? Pulsano in sincronia.",
        },
    },
    "cuore_macchina": {
        "nome": "Il Cuore della Macchina",
        "descrizione": (
            "Una sala cubica, vuota al centro tranne per un immenso pendolo dorato che "
            "scende dal soffitto e oscilla lentamente, lentamente, su un perno solitario. "
            "Sopra il pendolo, sospeso a mezz'aria, fluttua un cuore di cristallo — il "
            "Cuore della Macchina — spento, scuro, in attesa.\n\n"
            "Le pareti sono coperte da un mosaico di simboli che cambia mentre ti muovi: "
            "il pendolo te le riflette addosso, e tu sei ora parte del meccanismo."
        ),
        "descrizione_breve": "Sala del pendolo gigante. Cuore di cristallo spento sospeso sopra.",
        "uscite": {"sud": "sala_ingranaggi"},
        "uscite_bloccate": {"nord": {"condizione": "flag:cuore_riattivato",
                                      "messaggio": "Una porta di pietra. Non si apre. Il Cuore sopra di te è spento."}},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "pendolo": "Pendolo dorato, oscilla in un arco perfetto. Il perno è ben oliato. Manca qualcosa che lo trattenga: un fermo, un pomello.",
            "cuore": "Il Cuore della Macchina. Cristallo nero opaco. Aspetta di essere risvegliato — ma da cosa?",
            "mosaico_pareti": "Simboli che si ricompongono mentre cammini. Sembrano riflettere il tuo movimento, come se la sala stessa fosse cosciente.",
        },
    },
    "agora_perduta": {
        "nome": "Agorà Perduta",
        "descrizione": (
            "Sbuchi in un'enorme caverna che si apre all'improvviso, e ti rendi conto di "
            "essere dentro la città. Una piazza ottagonale circondata da edifici scolpiti "
            "nella pietra viva, alti come palazzi. Statue colossali di figure incoronate "
            "ti guardano dall'alto, immobili, eterne.\n\n"
            "Al centro della piazza, su un trono di basalto, siede un automa di metallo "
            "patinato — gigantesco — la testa china in attesa. Quando ti avvicini, alza "
            "lentamente lo sguardo. È vivo. Ti aspettava.\n\n"
            "Ai piedi del trono, mezzo nascosto, intravedi uno scrigno antico chiuso da "
            "un lucchetto a quattro rotelle."
        ),
        "descrizione_breve": "Piazza della città sotto la montagna. Re-Automa attende sul trono. Uno scrigno chiuso ai suoi piedi.",
        "uscite": {"sud": "cuore_macchina", "est": "via_titani"},
        "uscite_bloccate": {"nord": {"condizione": "flag:ponte_riparato",
                                      "messaggio": "Un ponte sospeso si srotola sull'abisso, ma le funi sono spezzate. Andare avanti sarebbe morte."}},
        "oggetti": [],
        "npcs": ["re_automa"],
        "esaminabili": {
            "statue": "Otto statue colossali, ognuna con una corona diversa. Re ed regine di un'era prima delle ere.",
            "trono": "Trono di basalto. Il Re-Automa siede composto, in attesa. Non è una statua: respira, lentamente.",
            "edifici": "Edifici scolpiti nella roccia viva. Finestre vuote. Era una città, una vera città. Quanti vi abitarono? Dove sono andati?",
            "scrigno": "Uno scrigno di metallo nero chiuso da un lucchetto a quattro rotelle. Sopra ogni rotella, simboli misteriosi: pianeti, geometrie, numeri romani. La combinazione giusta lo apre.",
        },
    },
    "via_titani": {
        "nome": "Via dei Titani",
        "descrizione": (
            "Un viale lungo come una via romana, fiancheggiato da statue di pietra alte "
            "venti metri. I Titani — antichi guardiani — siedono o stanno in piedi, "
            "ognuno con un'arma diversa: una lancia, un martello, un libro, un sigillo. "
            "Sotto i piedi, lastre lisce di ossidiana, ognuna con un simbolo intarsiato.\n\n"
            "All'estremità del viale, un portale circolare di pietra. Chiuso. Sopra, "
            "tre incavi: uno triangolare, uno quadrato, uno pentagonale."
        ),
        "descrizione_breve": "Viale di statue colossali. Portale circolare con tre incavi.",
        "uscite": {"ovest": "agora_perduta"},
        "uscite_bloccate": {"dentro": {"condizione": "flag:portale_aperto",
                                        "messaggio": "Il portale è chiuso. I tre incavi sopra di esso aspettano qualcosa."}},
        "oggetti": ["occhio_titano"],
        "npcs": [],
        "esaminabili": {
            "titani": "Otto statue, otto Titani. Ognuno regge un oggetto-simbolo. Forse dicono qualcosa, insieme.",
            "ossidiana": "Lastre di ossidiana levigata, ognuna con un simbolo: stelle, occhi, mani, semi. Calpestate da migliaia di pellegrini.",
            "portale": "Portale circolare di pietra dolomite. Non si apre. Sopra, tre incavi geometrici: triangolo, quadrato, pentagono.",
            "incavi": "Triangolo, quadrato, pentagono. Tre forme. Tre oggetti che probabilmente le riempiono.",
        },
    },
    "abisso": {
        "nome": "L'Abisso",
        "descrizione": (
            "Una crepa enorme nel mondo. Sotto di te, l'abisso scende oltre lo sguardo, "
            "respira un vento freddo che sa di pietra antica. Un ponte sospeso di assi e "
            "funi attraversa il vuoto verso una piattaforma sull'altro lato — ma le funi "
            "principali sono spezzate, due assi mancano, e il ponte oscilla pericolosamente "
            "ad ogni alito.\n\n"
            "Sotto di te, lontano lontano, intravedi un puntino di luce viva — qualcosa "
            "lo abita. La Radice del Mondo, forse."
        ),
        "descrizione_breve": "Voragine attraversata da un ponte rotto. Sotto, un puntino di luce.",
        "uscite": {"ovest": "agora_perduta"},
        "uscite_bloccate": {"est": {"condizione": "flag:ponte_riparato",
                                     "messaggio": "Il ponte è troppo danneggiato per essere attraversato. Cadresti nel vuoto."}},
        "oggetti": ["muschio_blu", "cristallo_radice"],
        "npcs": [],
        "esaminabili": {
            "ponte": "Ponte sospeso. Le funi maestre sono spezzate; due assi del piano mancano. Servirebbero funi metalliche e un'asse di ferro per ripararlo.",
            "vuoto": "Lo guardi e ti gira la testa. Sotto, un puntino di luce viva. Qualcosa di vivo si muove laggiù.",
            "vento": "Il vento sale dall'abisso e profuma di pietra calda. Non è solo aria: è il respiro di qualcosa.",
        },
    },
    # ─── STANZE ATMOSFERICHE (no item, solo mood + lore) ───
    "cimitero_marino": {
        "nome": "Cimitero Marino",
        "descrizione": (
            "Una cala remota dove il mare ha radunato i resti di un secolo di naufragi. "
            "Decine di scafi spezzati arrugginiscono sulla sabbia nera, alcuni col nome "
            "ancora leggibile sulla prua. Le onde sussurrano fra le ossa di legno, e ogni "
            "tanto un metallo cigola, come se qualcosa si svegliasse sotto.\n\n"
            "Non c'è nulla da raccogliere qui. Solo da ascoltare. Solo da ricordare che "
            "non sei il primo a essere arrivato — solo il primo a essere ancora vivo."
        ),
        "descrizione_breve": "Cala remota piena di relitti antichi. Solo silenzio e ruggine.",
        "uscite": {"nord": "scogliere_sud"},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "relitti": "Decine di scafi spezzati. Su uno: 'AURIGA - 1873'. Su un altro: 'PALINURO - 1924'. Una nave moderna: 'Capricho II - 2019'. Tutti finiti qui. Nessuno è mai ripartito.",
            "ossa_legno": "Ossa di legno. Le navi sono creature, e queste sono le loro carcasse. La marea le sposta lentamente, come per pietà.",
            "metallo_cigolante": "Da uno dei relitti più grandi, un cigolio ritmico. Non vento, non onda. Qualcosa di più lento. Qualcosa di paziente.",
            "sabbia_nera": "Sabbia di basalto, fine come polvere. Sulle dune si formano disegni geometrici quando il vento gira. Le tue impronte si cancellano in pochi secondi.",
        },
    },
    "bivio_giungla": {
        "nome": "Bivio degli Antichi",
        "descrizione": (
            "Un crocevia naturale nella giungla profonda, dove tre sentieri si incontrano "
            "attorno a un totem di pietra alto due metri, scolpito con figure di animali "
            "che non riconosci: un uccello dal becco a gancio, un pesce con quattro occhi, "
            "una creatura che è metà uomo e metà polipo.\n\n"
            "Non puoi proseguire da qui — i sentieri secondari portano solo a vicoli ciechi "
            "fitti di rovi. Ma questo posto ha qualcosa. Una presenza."
        ),
        "descrizione_breve": "Crocevia di sentieri attorno a un totem antico.",
        "uscite": {"nordovest": "giungla_profonda"},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "totem": "Pietra di basalto scolpita con maestria che non hai mai visto. Le tre figure si guardano in cerchio, come se aspettassero che qualcuno completasse il quartetto.",
            "uccello_becco": "L'uccello ha un becco a gancio e occhi profondi. Sotto la sua figura, un'iscrizione: «chi vola vede tutto, ma non torna».",
            "pesce_quattro_occhi": "Un pesce con quattro occhi disposti in cerchio. Iscrizione: «chi nuota nel buio non ne ha paura».",
            "uomo_polipo": "La figura più inquietante: metà uomo, metà polipo. Iscrizione: «chi unisce due mondi non appartiene a nessuno».",
            "sentieri_morti": "Tre sentieri secondari si addentrano nella vegetazione, ma dopo pochi metri sono inghiottiti da rovi. Servirebbe il machete e mezza giornata. Non vale la pena.",
        },
    },
    "corridoio_perduto": {
        "nome": "Corridoio Perduto",
        "descrizione": (
            "Un corridoio basso e dimenticato, scoperto per caso fra le ombre della "
            "cripta meccanica. Il soffitto gocciola di una condensa che brilla appena, e "
            "le pareti sono coperte di nomi — migliaia di nomi — incisi nel metallo da mani "
            "diverse, in epoche diverse.\n\n"
            "Sono i nomi di tutti i Costruttori che sono scesi prima di te. Quelli che non "
            "sono mai più risaliti. Il corridoio finisce in un muro liscio: nessuna porta, "
            "solo un'iscrizione finale, in alto, troppo in alto per leggerla bene."
        ),
        "descrizione_breve": "Corridoio dimenticato pieno di nomi incisi.",
        "uscite": {"sud": "cripta_meccanica"},
        "uscite_bloccate": {},
        "oggetti": [],
        "npcs": [],
        "esaminabili": {
            "nomi": "Migliaia di nomi. Alcuni in caratteri che riconosci, altri in alfabeti che non hai mai visto. Tutti incisi con cura, alcuni con tremore. Una è una bambina: 'Mira, sette anni, scesa con la mamma.'",
            "iscrizione_alta": "L'iscrizione in cima al muro: 'NOI ABBIAMO SCELTO. VOI CHE LEGGETE: ANCHE VOI POTETE.' Sotto, in piccolo: 'Non per forza. Mai per forza.'",
            "condensa_brillante": "Le gocce dal soffitto brillano debolmente. Cadono lentamente, sempre nello stesso ritmo, come se contassero qualcosa.",
            "pareti": "Metallo nero lavorato a freddo. Levigato da migliaia di mani che lo hanno toccato per leggere i nomi nel buio.",
        },
    },
    "cunicolo_nascosto": {
        "nome": "Cunicolo Nascosto",
        "descrizione": (
            "Hai abbattuto la parete della cripta col piccone, e quello che si è aperto è "
            "un cunicolo basso, asciutto, perfettamente intatto. Polvere antichissima posata "
            "su un altarino di pietra. Sopra l'altare, sotto una cupola di vetro intatto, "
            "una piccola lampada di rame brilla ancora di luce calda — accesa da chissà "
            "quando, alimentata da chissà cosa.\n\n"
            "L'aria odora di mirra. Sul retro dell'altarino, un'incisione: «alla luce che "
            "non conosce alba né tramonto»."
        ),
        "descrizione_breve": "Cunicolo segreto con un'antica lampada eterna.",
        "uscite": {"sud": "cripta"},
        "uscite_bloccate": {},
        "oggetti": ["lampada_eterna"],
        "npcs": [],
        "esaminabili": {
            "altare": "Un altarino in calcare bianco. La superficie superiore è levigata da secoli di offerte invisibili.",
            "cupola_vetro": "Una cupoletta di vetro soffiato, vecchia di millenni, ancora perfettamente trasparente. Tecnologia che non sai spiegare.",
            "lampada": "La lampada di rame brilla con una fiamma piccola e perfettamente ferma. Non consuma olio, non emette fumo. Brilla da prima che tu nascessi.",
            "polvere": "Polvere finissima, posata uniformemente. Le tue impronte sono le prime in millenni.",
        },
    },
    "radice_mondo": {
        "nome": "La Radice del Mondo",
        "descrizione": (
            "Hai disceso, hai attraversato, hai aperto. Ora sei al centro.\n\n"
            "Una sala sferica, perfetta, di cristallo nero. Al centro, sospeso a mezz'aria "
            "senza supporto, c'è un albero di luce — non un albero vero, ma una struttura "
            "ramificata di pura luce verde-azzurra, le radici che scendono e i rami che "
            "salgono, infiniti in entrambe le direzioni. È il cuore dell'isola, la sorgente "
            "di ogni mistero che hai incontrato.\n\n"
            "Davanti all'albero, un piedistallo di pietra. Sopra, una corona di metallo "
            "annerito: la Corona Titanica. Vuota. In attesa di essere completata."
        ),
        "descrizione_breve": "Sala sferica con l'Albero di Luce. Corona Titanica sul piedistallo.",
        "uscite": {"ovest": "abisso", "su": "via_titani"},
        "uscite_bloccate": {},
        "oggetti": ["radice_madre", "corona_titanica"],
        "npcs": [],
        "esaminabili": {
            "albero": "Un albero fatto di pura luce. Non emette calore, ma sentirla cantare nelle ossa. È vivo. È stato vivo da prima dell'isola, da prima di tutto.",
            "piedistallo": "Pietra grezza con un avvallamento per ricevere la corona. Sotto, un'iscrizione: 'CHI INDOSSA, NON RITORNA QUALE ERA.'",
            "corona_vuota": "Una corona di metallo nero. Otto punte vuote. Ogni punta sembra fatta per ricevere un cristallo o una stella.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────
# OGGETTI — 16 nuovi
# ─────────────────────────────────────────────────────────────────────
def make_item(nome, completo, desc, alias=None):
    return {"nome": nome, "nome_completo": completo, "descrizione": desc,
            "descrizione_terra": f"Trovi {completo.lower()} qui.",
            "portatile": True, "nascosto": False, "alias": alias or [nome]}

ITEMS = {
    "spore_lumino": make_item("spore", "Spore luminescenti",
        "Spore raccolte vicino al pozzo. Brillano di luce verde fredda, perfette per illuminare passaggi bui.", ["spore", "luce_spore"]),
    "ingranaggio": make_item("ingranaggio", "Ingranaggio di rame",
        "Un ingranaggio dentato di rame ben lavorato. Pesa nella mano. Sembra parte di un meccanismo più grande.", ["ingranaggio", "ruota_rame"]),
    "ruota_dentata": make_item("ruota_dentata", "Ruota dentata di ferro",
        "Una grande ruota dentata di ferro nero, più larga del palmo della tua mano. Si incastra perfettamente con altri ingranaggi.", ["ruota", "dentata"]),
    "binario_ferro": make_item("binario", "Binario di ferro",
        "Un'asse di ferro lunga come il tuo braccio, con cremagliera su un lato. Buona per riparare strutture o creare meccanismi.", ["binario", "asse_ferro"]),
    "martello_rame": make_item("martello", "Martello di rame",
        "Un martello con la testa di rame patinato, manico in legno scuro. Pesante, equilibrato, fatto per chi sa lavorare il metallo.", ["martello", "maglio"]),
    "pendolo_ottone": make_item("pendolo", "Pendolo di ottone",
        "Un pendolo dorato con un peso a forma di goccia rovesciata. Sulla cima, una flangia esagonale per fissarlo a un meccanismo.", ["pendolo", "ottone"]),
    "valvola_vapore": make_item("valvola", "Valvola del vapore",
        "Una valvola industriale di rame e ferro, con manopola circolare. Regola il flusso di vapore ad alta pressione.", ["valvola", "rubinetto"]),
    "ampolla": make_item("ampolla", "Ampolla di cristallo",
        "Un'ampolla di cristallo soffiato a mano. Stretta in cima, larga in fondo. Vuota, ma evidentemente concepita per contenere qualcosa di prezioso.", ["ampolla", "fiala"]),
    "catena_oro": make_item("catena", "Catena d'oro corta",
        "Una catena di anelli d'oro pesanti. Più gioiello che strumento, ma forte abbastanza per portare un peso considerevole.", ["catena", "filiera"]),
    "tavoletta_runica": make_item("tavoletta", "Tavoletta runica",
        "Una tavoletta di metallo sottile incisa con simboli che cambiano lentamente quando la guardi. L'Archivista la decifrerebbe.", ["tavoletta", "lastra"]),
    "funi_metalliche": make_item("funi", "Funi di metallo intrecciato",
        "Funi di filamenti metallici intrecciati. Forti, flessibili, perfette per riparare un ponte sospeso.", ["funi", "fune"]),
    "frammento_stella": make_item("frammento_stella", "Frammento di stella",
        "Un frammento minuscolo di un metallo che brilla di luce propria. È freddo, ma se lo guardi a lungo ti scalda dentro.", ["stella", "frammento"]),
    "occhio_titano": make_item("occhio_titano", "Occhio del Titano",
        "Un occhio di pietra dura, forse zaffiro, della dimensione del tuo pugno. Quando lo tieni in mano, hai la sensazione che qualcosa ti stia osservando.", ["occhio", "titano"]),
    "sigillo_re": make_item("sigillo_re", "Sigillo del Re",
        "Un sigillo a tampone di pietra nera, con il simbolo di una corona ottagonale. Autorità antica, scolpita in pietra.", ["sigillo", "regio"]),
    "muschio_blu": make_item("muschio", "Muschio bioluminescente",
        "Un muschio fluorescente che cresce nelle profondità. Emette una luce blu-verdognola che non scalda.", ["muschio", "muschio_blu"]),
    "cristallo_radice": make_item("cristallo_radice", "Cristallo della Radice",
        "Un cristallo verde-azzurro che pulsa lentamente, come un piccolo cuore. È caldo. Vive.", ["cristallo_radice", "verde_cristallo"]),
    "radice_madre": make_item("radice", "Radice Madre",
        "Una radice piccolissima dell'Albero di Luce. Pulsa nella tua mano, gentile come una creatura addomesticata.", ["radice_madre", "germoglio"]),
    "corona_titanica": make_item("corona_titanica", "Corona Titanica",
        "Una corona di metallo nero con otto punte vuote. Antica oltre ogni misura. Ha conosciuto teste che non potresti immaginare.", ["corona", "diadema"]),
    # Risultati di combinazioni
    "meccanismo_completo": make_item("meccanismo", "Meccanismo a ingranaggi",
        "Ingranaggio e ruota dentata uniti in un meccanismo funzionante. Pronto per essere montato.", ["meccanismo"]),
    "manovella_completa": make_item("manovella_completa", "Manovella completa",
        "Una manovella con il pendolo come pomello: pesa, gira, ruota dolcemente. Pronta per la piattaforma.", ["manovella"]),
    "funi_metalliche_intrecciate": make_item("ponte_riparato", "Kit di riparazione ponte",
        "Funi metalliche intrecciate con il binario di ferro: tutto il necessario per riparare un ponte sospeso.", ["ponte_riparato", "kit_ponte"]),
    "lente_smeraldo": make_item("lente", "Lente di smeraldo",
        "Lente verde tagliata da un singolo smeraldo. Quando ci guardi attraverso, la luce ordinaria diventa parlante.", ["lente", "smeraldo"]),
    "corona_attivata": make_item("corona_attivata", "Corona Titanica attivata",
        "La corona riempita dei tre simboli: stella, radice, occhio. Pulsa di luce dolce e fredda. Pronta a essere indossata.", ["corona_completa"]),
    "lampada_eterna": make_item("lampada_eterna", "Lampada Eterna",
        "Una lampada di rame con una fiamma piccola e perfettamente ferma. Brilla da prima che tu nascessi e brillerà dopo che sarai morto. Custodita per millenni in un cunicolo dimenticato.", ["lampada", "fiamma"]),
}

# ─────────────────────────────────────────────────────────────────────
# NPC — 2 nuovi
# ─────────────────────────────────────────────────────────────────────
CHARACTERS = {
    "archivista": {
        "nome": "L'Archivista",
        "descrizione": "Una figura di luce traslucida, vagamente femminile, fluttuante a un metro dal pavimento. Il suo volto è sereno e gli occhi, quando aperti, sono di un blu che hai visto solo nel cuore delle fiamme. Parla senza muovere le labbra, una voce che senti dentro più che fuori.",
        "alias": ["archivista", "donna_luce", "spirito"],
        "stanza": "archivio",
    },
    "re_automa": {
        "nome": "Il Re-Automa",
        "descrizione": "Un automa colossale alto quattro metri, di metallo patinato verde-rame. Il suo corpo è coperto di intarsi delicati, e la sua corona — quella che porta — è semplice, ferro grezzo. Il suo volto è una maschera di rame con due fessure per gli occhi: nelle fessure, una luce calma e antichissima.",
        "alias": ["re", "re_automa", "automa", "gigante"],
        "stanza": "agora_perduta",
    },
}

# ─────────────────────────────────────────────────────────────────────
# DIALOGHI
# ─────────────────────────────────────────────────────────────────────
DIALOGUES = {
    "archivista": [
        {
            "condizione": {"flag": "archivista_consultata"},
            "saluto": "L'Archivista riapre gli occhi blu.\n\n\"Sei tornato, viaggiatore. La conoscenza non si finisce mai. Cosa cerchi oggi?\"",
            "opzioni": [
                {"testo": "Parlami della Radice del Mondo",
                 "risposta": "\"L'Albero di Luce è la sorgente. Quando il primo seme cadde nelle profondità della pietra, da esso germogliò tutto: la nostra civiltà, la magia, il faro stesso. Per raggiungere la Radice devi attraversare l'Abisso, e per attraversare l'Abisso devi prima riattivare il Cuore della Macchina.\""},
                {"testo": "Come riattivo il Cuore della Macchina?",
                 "risposta": "\"Il Cuore vuole essere risvegliato dal pendolo. Trova il pendolo di ottone nella forgia. Combinalo con la manovella spezzata della piattaforma. Una volta completata, gira la manovella e la piattaforma si solleverà fino al Cuore.\""},
                {"testo": "Parlami del Re-Automa",
                 "risposta": "\"L'ultimo Re. Quando i nostri compresero che la fine era vicina, il Re scelse di farsi automa per attendere chi sarebbe venuto. Aspetta da quattromila anni. Ti aspettava.\""},
                {"testo": "Come si apre il portale dei Titani?",
                 "risposta": "\"I tre incavi vogliono i tre simboli della creazione: la stella (il cosmo), l'occhio (la coscienza), la radice (la vita). Trova un frammento di stella, l'occhio di un Titano, e una radice viva. Posizionali nelle nicchie giuste.\""},
                {"fine": True, "testo": "Grazie, Archivista. Tornerò."},
            ],
        },
        {
            "saluto": "La figura di luce apre gli occhi blu. Ti studia per un lungo momento — non con i sensi, ma con qualcosa di più profondo.\n\n\"Sei vivo. E sei sceso. Sono passati millenni dall'ultimo visitatore. Mi chiamo come mi chiamerai. Il mio nome è dimenticato, ma la mia funzione no: io sono l'Archivio. Cosa vuoi sapere, viaggiatore?\"",
            "opzioni": [
                {"testo": "Dove sono?",
                 "azione": {"tipo": "flag", "id": "archivista_consultata"},
                 "risposta": "\"Sotto l'isola. Sotto il faro. Sotto il mare. Questa è la Città dei Costruttori, l'ultima dimora del popolo che fabbricò il faro per chiamare i naviganti — non come SOS, ma come INVITO. Pochi rispondono. Tu sei uno.\""},
                {"testo": "Come faccio a procedere?",
                 "azione": {"tipo": "flag", "id": "archivista_consultata"},
                 "risposta": "\"Esplora. Raccogli. Riattiva il Cuore della Macchina nella sala a nord. Poi parla con il Re-Automa. Lui ti darà la chiave finale. Ma ricorda: chi raggiunge la Radice non torna mai uguale. Ti avverto.\""},
                {"testo": "Sei... viva?",
                 "azione": {"tipo": "flag", "id": "archivista_consultata"},
                 "risposta": "\"Sono ciò che resta di chi sono stata. Una funzione. Un ricordo che si è fatto strumento. Non è importante. Ciò che conta è che sono qui, e tu sei qui, e abbiamo qualcosa da fare insieme.\""},
                {"fine": True, "testo": "Devo andare."},
            ],
        },
    ],
    "re_automa": [
        {
            "condizione": {"flag": "re_completato"},
            "saluto": "Il Re-Automa china leggermente la testa. \"Hai indossato la corona. Sei il prossimo. Va', e regna gentilmente.\"",
            "opzioni": [
                {"fine": True, "testo": "Mi inchino. Addio, Re."},
            ],
        },
        {
            "condizione": {"oggetto": "corona_attivata"},
            "saluto": "Il Re-Automa solleva lo sguardo verso di te. Vede la corona attivata nelle tue mani. Una vibrazione di energia gli percorre il corpo metallico. La sua voce, quando arriva, è come il suono di un bronzo colpito da lontano:\n\n\"L'hai trovata. L'hai completata. Hai compreso. Vieni avanti, viaggiatore.\"",
            "opzioni": [
                {"testo": "Cosa devo fare ora?",
                 "azione": {"tipo": "flag", "id": "re_completato"},
                 "risposta": "\"Discendi nell'Abisso. Trova la Radice del Mondo. Lì, davanti all'Albero di Luce, indossa la Corona. La sceglierai. La sceglierà te. E saprai cosa devi essere.\""},
                {"testo": "E tu? Cosa ne sarà di te?",
                 "azione": {"tipo": "flag", "id": "re_completato"},
                 "risposta": "\"Io ho aspettato quattromila anni per consegnarti questo momento. Quando indosserai la corona, io potrò finalmente spegnermi. È il dono che mi farai.\"\n\nLa luce nei suoi occhi vacilla, e per un istante vedi qualcosa che somiglia a un sorriso."},
            ],
        },
        {
            "saluto": "Il Re-Automa solleva lentamente la testa. La sua voce arriva da molto lontano, come se attraversasse il tempo per raggiungerti:\n\n\"Sei venuto. Bene. Non sapevo se saresti riuscito ad arrivare fino qui. Adesso ti vedo, e capisco. Sì. Tu puoi farcela. Ma prima devi prepararti.\"",
            "opzioni": [
                {"testo": "Prepararmi a cosa?",
                 "risposta": "\"A indossare la Corona Titanica. La troverai nella Radice del Mondo, oltre l'Abisso. Ma per attivarla devi raccogliere tre simboli: una stella dal mio osservatorio, l'occhio di un Titano dal viale, e la radice viva dell'Albero. Posizionali nelle tre punte vuote più alte della corona.\""},
                {"testo": "Come passo l'Abisso?",
                 "risposta": "\"Il ponte è spezzato. Funi e binario lo riparano. Cerca nella biblioteca dell'Archivista, e nella sala degli ingranaggi.\""},
                {"testo": "Cosa c'è oltre la Radice?",
                 "risposta": "\"Non ciò che pensi. Non un'altra stanza, non un mondo nuovo. Una scelta. La Corona ti chiederà chi vuoi essere. Pensaci, viaggiatore. Pensa bene.\""},
                {"testo": "Chi siete voi? Chi eravate?",
                 "risposta": "\"Eravamo i Costruttori. Sapevamo molto, troppo. Quando la nostra civiltà comprese che eravamo la causa della nostra rovina, scegliemmo di scendere — di sigillarci sotto la pietra, di lasciare che il mondo guarisse senza di noi. Io sono l'ultimo. Aspettavo te.\""},
                {"fine": True, "testo": "Devo riflettere. Tornerò."},
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────
# RICETTE
# ─────────────────────────────────────────────────────────────────────
RECIPES = [
    {"ingredienti": ["ingranaggio", "ruota_dentata"], "risultato": "meccanismo_completo",
     "messaggio": "Incastri la ruota dentata sull'ingranaggio. Si parlano subito, denti e cave, e ruotano insieme con un click di soddisfazione meccanica. Hai un meccanismo completo."},
    {"ingredienti": ["pendolo_ottone", "manovella_temp"], "risultato": "manovella_completa",
     "messaggio": "Attacchi il pendolo all'asta della manovella. Pesa giusto. Ora la manovella ha il suo pomello — è completa, pronta per essere girata."},
    {"ingredienti": ["funi_metalliche", "binario_ferro"], "risultato": "funi_metalliche_intrecciate",
     "messaggio": "Intrecci le funi metalliche attorno al binario di ferro. Ora hai un kit per riparare il ponte: una struttura solida con le funi che la sostengono."},
    {"ingredienti": ["frammento_stella", "ampolla"], "risultato": "lente_smeraldo",
     "messaggio": "Inserisci il frammento di stella nell'ampolla di cristallo. La luce si concentra, si focalizza, si fa lente. Ora hai uno smeraldo che vede oltre l'apparenza."},
    {"ingredienti": ["corona_titanica", "frammento_stella"], "risultato": "corona_titanica_step1",
     "messaggio": "Posizioni il frammento di stella in una delle punte della corona. La punta si chiude attorno al frammento e brilla. Manca ancora qualcosa: l'occhio e la radice."},
    {"ingredienti": ["corona_titanica_step1", "occhio_titano"], "risultato": "corona_titanica_step2",
     "messaggio": "Posizioni l'Occhio del Titano in una seconda punta. La corona vibra. Manca ancora una cosa: la vita stessa, la radice."},
    {"ingredienti": ["corona_titanica_step2", "radice_madre"], "risultato": "corona_attivata",
     "messaggio": "Posizioni la Radice Madre nella terza punta. Le tre energie si parlano: stella, mente, vita. Le otto punte si illuminano una dopo l'altra in cascata. La Corona Titanica è ora ATTIVA. Pulsa, dolce e fredda, nelle tue mani."},
]

# Aggiungo manovella temporanea (oggetto fittizio rappresentato da un pickup nella sala_ingranaggi)
ITEMS["manovella_temp"] = make_item("manovella_temp", "Asta della manovella",
    "L'asta nuda della manovella, smontata. Aspetta un pomello da fissare in cima.", ["asta", "manovella_asta"])

# ─────────────────────────────────────────────────────────────────────
# AZIONI STANZA — usare oggetto su scenario
# ─────────────────────────────────────────────────────────────────────
ROOM_ACTIONS = {
    ("valvola_vapore", "cripta_meccanica"): {
        "messaggio": "Avviti la valvola al raccordo del corridoio. Il sibilo del vapore si calma in un respiro regolare. Il passaggio è ora sicuro.",
        "flag": "valvola_installata", "consuma": True,
    },
    ("manovella_completa", "sala_ingranaggi"): {
        "messaggio": "Avviti la manovella completa al perno della piattaforma. Ora ha presa: puoi girarla. Lo fai. La piattaforma si solleva con un rombo di ingranaggi che si svegliano. Sale fino al Cuore della Macchina, sospeso sopra di te.\n\nIl Cuore si illumina, lentamente, da nero a verde-azzurro pulsante. La porta a nord, nella stessa sala, scatta aperta.",
        "flag": "cuore_riattivato", "consuma": True,
    },
    ("funi_metalliche_intrecciate", "abisso"): {
        "messaggio": "Lavori per ore. Le funi vengono tese, il binario fa da nuovo asse, le assi mancanti vengono sostituite. Quando finisci, il ponte è solido. Puoi attraversarlo.",
        "flag": "ponte_riparato", "consuma": True,
    },
    ("lente_smeraldo", "osservatorio"): {
        "messaggio": "Inserisci la lente di smeraldo nella scanalatura sulla cima dell'astrolabio. Le stelle proiettate sul soffitto cambiano: si raggruppano, si allineano, formano un disegno chiaro — tre stelle in fila, perfettamente allineate col mosaico sul muro.\n\nC'è un click sotto i tuoi piedi: una porta nascosta si apre nel pavimento.",
        "flag": "stelle_allineate", "consuma": False,
    },
    ("corona_attivata", "radice_mondo"): {
        "messaggio": "Sollevi la Corona Titanica con entrambe le mani. Pesa più di quanto ti aspettassi: il peso del tempo. La avvicini lentamente alla testa.",
        "flag": "corona_indossata", "consuma": True,
    },
    ("meccanismo_completo", "via_titani"): {
        "messaggio": "Inserisci il meccanismo nei tre incavi del portale. Le tre forme — triangolo, quadrato, pentagono — combaciano perfettamente. Gli ingranaggi del meccanismo si parlano con quelli del portale, e per la prima volta dopo millenni la pietra circolare si schiude. Una via alternativa per la Radice del Mondo si apre.",
        "flag": "portale_aperto", "consuma": True,
    },
    # Piccone rompe la parete della cripta e rivela il cunicolo nascosto
    ("piccone", "cripta"): {
        "messaggio": "Sferri un colpo, due, tre. Le pietre allentate cedono una dopo l'altra. Polvere antichissima si solleva. Quando il muro crolla del tutto, ti trovi davanti a un piccolo cunicolo asciutto che si apre verso nord. La luce di una fiamma calda brilla in fondo.",
        "flag": "cunicolo_aperto", "consuma": False, "audio": "wall_break",
    },
    # Manovella temporanea: prendi l'asta dalla manovella della sala_ingranaggi usando il martello
    ("martello_rame", "sala_ingranaggi"): {
        "messaggio": "Con il martello di rame allenti il bullone alla base della manovella. L'asta nuda si stacca: ora puoi prenderla con te per montarla altrove.",
        "ottieni": ["manovella_temp"], "flag": "asta_estratta", "consuma": False,
    },
}

# ─────────────────────────────────────────────────────────────────────
# CONSEGNE
# ─────────────────────────────────────────────────────────────────────
DELIVERIES = {
    ("tavoletta_runica", "archivista"): {
        "messaggio": "Porgi la tavoletta runica all'Archivista. Lei la accetta delicatamente, e per la prima volta sorride davvero.\n\n\"Una tavoletta perduta. La leggo. Ah... è una mappa. Una mappa del Cuore della Macchina, e dei suoi tre punti deboli. Tienila, ora ti sarà più utile a te che a me.\"\n\nDopo un momento, dalla tunica di luce estrae un piccolo dono e te lo porge.",
        "rimuovi": [], "ottieni": ["lente_smeraldo"], "flag": "archivista_dono",
    },
    ("sigillo_re", "archivista"): {
        "messaggio": "L'Archivista riconosce subito il sigillo. \"Il segno del Re. Hai parlato con lui. Bene. Allora questa è tua.\"\n\nTi consegna una piccola tavoletta in cui sono incise le risposte a un enigma antico — un dono di conoscenza.",
        "ottieni": [], "flag": "archivista_riconosce_re",
    },
}

# ─────────────────────────────────────────────────────────────────────
# PUZZLES (interattivi, gestiti dal frontend)
# ─────────────────────────────────────────────────────────────────────
PUZZLES = {
    "lucchetto_scrigno": {
        "tipo": "lucchetto",
        "stanza": "agora_perduta",
        "trigger_examine": "scrigno",
        "testo": "Lo scrigno antico ai piedi del trono. Quattro rotelle, ognuna con simboli misteriosi. Una iscrizione: 'IL SOLE NASCE A ORIENTE, IL TRIANGOLO SACRO PUNTA AL CIELO, AL TERZO GIORNO IL RE GIUNSE, E LA TERRA, TERZO PIANETA DAL SOLE, LO ACCOLSE.'",
        "rotelle": [
            ["☉", "☽", "★", "✦"],
            ["▲", "■", "●", "◆"],
            ["I", "II", "III", "IV"],
            ["♁", "♆", "♅", "♄"],
        ],
        "soluzione": ["☉", "▲", "III", "♁"],
        "successo": "Le rotelle si allineano con uno schiocco di metallo. Lo scrigno si apre con un sibilo di aria che esce dopo millenni. Dentro, posato su un velo di seta antichissima, c'è il Sigillo del Re.",
        "fallimento": "Le rotelle scattano nelle posizioni errate. Lo scrigno resta chiuso.",
        "flag": "scrigno_aperto",
        "ottieni": ["sigillo_re"],
    },
    "stelle_osservatorio": {
        "tipo": "stelle",
        "stanza": "osservatorio",
        "trigger_examine": "mosaico",
        "testo": "Il mosaico di tre stelle pulsa in attesa. Sulla parete, un meccanismo con tre ruote di pietra corrisponde alle tre stelle proiettate. Allinea ognuna con il segno tratteggiato per completare la costellazione antica.",
        "targets": [90, 180, 270],
        "successo": "Le tre stelle si allineano perfettamente. Un clic risuona: sull'astrolabio centrale, una piccola apertura rivela un frammento di stella incastonato nell'ottone — in dono a chi ha saputo guardare il cielo giusto.",
        "fallimento": "Le stelle vibrano ma non sono allineate. Riprova.",
        "flag": "stelle_allineate_puzzle",
        "ottieni": ["frammento_stella"],
    },
    "pendolo_cuore": {
        "tipo": "pendolo",
        "stanza": "cuore_macchina",
        "trigger_examine": "pendolo",
        "testo": "Il pendolo gigante oscilla lento sopra di te. La sala lo accompagna con un battito preciso. Se lo segui col tuo ritmo per quattro battiti, il Cuore forse ti ascolterà.",
        "target_rhythm": [900, 900, 900, 900],
        "successo": "Hai seguito il tempo perfetto. Il Cuore sopra di te emette un bagliore breve ma netto — qualcosa si è predisposto. D'ora in poi, il Cuore risponderà più pronto al prossimo intervento meccanico.",
        "fallimento": "Il ritmo è sfasato. Il pendolo continua imperturbabile. Riprova quando avrai il giusto tempo dentro.",
        "flag": "pendolo_sintonizzato",
        "ottieni": [],
    },
}

# ─────────────────────────────────────────────────────────────────────
# Modifiche al mondo base: aggiungi al faro un'uscita "giu" verso pozzo_faro
# (verrà applicata da export_world.py via merge)
# ─────────────────────────────────────────────────────────────────────
ROOM_PATCHES = {
    "faro": {
        "uscite_bloccate_add": {
            "giu": {"condizione": "flag:faro_acceso",
                    "messaggio": "Il pavimento del faro è solido. Non ti aspetteresti di poter scendere oltre."}
        },
        "esaminabili_add": {
            "pavimento_faro": "Quando il faro è acceso, il pavimento di pietra si apre come un fiore di metallo. Sotto, un pozzo verticale scende nelle profondità.",
            "vibrazione": "Metti la mano sulla pietra del faro. Vibra, leggermente, come un cuore. Non nel ritmo di qualcosa di meccanico: nel ritmo di *qualcosa che ti conosce*. Ritiri la mano di colpo.",
        },
    },
    # Pulizia: rimuovi oggetti vicolo cieco dal mondo base
    "spiaggia": {
        "oggetti_remove": ["bottiglia"],
        "esaminabili_add": {
            "segno_sabbia": "C'è un disegno nella sabbia — uno spirale a tre bracci. L'onda lo sta cancellando. Per un istante, prima che scompaia del tutto, ti sembra di *averlo disegnato tu*. Poi il pensiero svanisce.",
            "tue_mani": "Le tue mani. Ti guardi i palmi, come se non li vedessi da sempre. C'è una piccola cicatrice lineare sul palmo destro — non ti ricordi di essertela fatta. Eppure è antica.",
        },
    },
    "radura":       {"oggetti_remove": ["fiori"]},
    "molo":         {"oggetti_remove": ["rete_pesca"]},
    "capanna_luna": {
        "oggetti_remove": ["erbe_secche"],
        "esaminabili_add": {
            "sguardo_luna": "Luna ti osserva più a lungo di quanto sia educato. Quando le tue pupille incrociano le sue, smette di fingere. «Non sei quello che sembri. Tu lo sai, in qualche parte di te. Lo saprai del tutto quando sarà il momento.» Poi sorride, e non dice più niente.",
        },
    },
    # Foreshadowing: riconoscimento simboli nella grotta
    "grotte": {
        "esaminabili_add": {
            "incisioni_familiari": "Le spirali sulla parete. Le guardi e *sai* in che ordine vanno lette — dall'esterno verso l'interno, poi fuori di nuovo. Come hai imparato? Non sapresti dirlo. Lo sai e basta.",
        },
    },
    # Cripta: aggiungi muro esaminabile + uscita bloccata verso cunicolo_nascosto
    "cripta": {
        "esaminabili_add": {
            "muro_screpolato": "Una crepa irregolare attraversa la parete nord. Pietre allentate sembrano nascondere un cunicolo dietro di sé. Servirebbe qualcosa di robusto per romperla.",
        },
        "uscite_bloccate_add": {
            "nord": {"condizione": "flag:cunicolo_aperto",
                     "messaggio": "Una parete di pietra blocca il passaggio verso nord. La superficie è screpolata."}
        },
    },
    # Pulizia: rimuovi catena_oro dal corridoio_vapore (Atto II)
    "corridoio_vapore": {"oggetti_remove": ["catena_oro"]},
    # Connessioni alle nuove stanze atmosferiche
    "scogliere_sud": {
        "uscite_add": {"sud": "cimitero_marino"},
        "esaminabili_add": {
            "calata_sud": "Una scala stretta, scolpita nella roccia, scende verso una cala remota. Da quassù non si vede il fondo, ma puoi sentire il vento che porta su un odore di legno fradicio e ruggine.",
        },
    },
    "giungla_profonda": {
        "uscite_add": {"sudest": "bivio_giungla"},
        "esaminabili_add": {
            "sentiero_sudest": "Verso sud-est, un sentiero stretto si addentra fra i tronchi più alti. Si intuisce un'apertura — forse un crocevia.",
        },
    },
    "cripta_meccanica": {
        "uscite_add": {"ovest": "corridoio_perduto"},
        "esaminabili_add": {
            "ombra_ovest": "Sulla parete ovest, un'ombra anomala. Avvicinandoti vedi che è in realtà l'imboccatura di un corridoio basso e dimenticato. Una sola lastra di metallo barriera, ma è caduta da tempo.",
        },
    },
}

BLOCKED_DESTS = {
    "faro::giu": "pozzo_faro",
    "pozzo_faro::giu": "cripta_meccanica",
    "cripta_meccanica::est": "corridoio_vapore",
    "sala_ingranaggi::nord": "cuore_macchina",
    "cuore_macchina::nord": "agora_perduta",
    "agora_perduta::nord": "abisso",
    "abisso::est": "radice_mondo",
    "via_titani::dentro": "radice_mondo",
    "osservatorio::dentro": "via_titani",
    "cripta::nord": "cunicolo_nascosto",
}

# ─────────────────────────────────────────────────────────────────────
# COLLEZIONABILI — 12 frammenti di lore
# ─────────────────────────────────────────────────────────────────────
COLLECTIBLES = {
    "conchiglia": {
        "nome": "Conchiglia spiralata",
        "lore": "Il mare ha una memoria propria. Avvicinala all'orecchio: senti il pianto antico di tutte le navi che non sono tornate.",
    },
    "perla_nera": {
        "nome": "Perla nera della laguna",
        "lore": "Si dice che le perle nere nascano nelle ostriche che hanno visto un omicidio. Questa ha visto qualcosa di peggio: un'intera civiltà sigillarsi sotto la pietra.",
    },
    "corona_corallo": {
        "nome": "Corona di corallo",
        "lore": "Una corona infantile, fatta di rametti di corallo intrecciati. Apparteneva a una bambina del popolo sommerso. Ha giocato a essere regina prima della fine.",
    },
    "frammento_mappa": {
        "nome": "Frammento di mappa antica",
        "lore": "Solo un quarto della carta originale. Mostra l'isola con un nome che non sai leggere e una croce sopra il faro. Sotto la croce, in piccolo: «la porta».",
    },
    "messaggio_bottiglia": {
        "nome": "Messaggio in bottiglia",
        "lore": "«Se leggi questo, sei l'undicesimo. I primi dieci sono diventati la luce del faro. Decidi tu se vuoi essere l'ultimo lume o se vuoi spegnerlo.» Firmato: il decimo.",
    },
    "diario_guardiano": {
        "nome": "Diario del Guardiano",
        "lore": "Pagine fitte di una grafia minuta. L'ultima riga, scarabocchiata di fretta: «Non eravamo dèi. Eravamo solo i primi a capire. Mi spiace, lettore. Tu adesso devi capire dopo di me.»",
    },
    "tavoletta_antica": {
        "nome": "Tavoletta cifrata",
        "lore": "Tre simboli si ripetono: un occhio, una stella, una radice. Sotto, la frase: «Quando i tre tornano insieme, il mondo respira di nuovo.»",
    },
    "sigillo_antico": {
        "nome": "Sigillo del tempio sommerso",
        "lore": "Il sigillo di un sacerdote del culto del faro. Sul retro, due parole: «accendi soltanto».",
    },
    "tridente": {
        "nome": "Tridente cerimoniale",
        "lore": "Le tre punte rappresentano i tre poteri del faro: olio, cristallo, gemma. Chi lo impugnava chiamava le navi. Chi lo impugnava le mandava anche a fondo.",
    },
    "cristallo_radice": {
        "nome": "Cristallo della Radice",
        "lore": "Pulsa al ritmo dell'Albero di Luce. Se lo tieni vicino al cuore, senti che il tuo battito si sincronizza al suo. Smetti di avere paura. Smetti di avere fretta.",
    },
    "muschio_blu": {
        "nome": "Muschio bioluminescente dell'Abisso",
        "lore": "Cresce solo dove la luce del sole non è mai arrivata e non arriverà mai. Eppure brilla. Lezione: la luce non viene sempre da fuori.",
    },
    "spore_lumino": {
        "nome": "Spore della soglia",
        "lore": "Le porte tra i mondi rilasciano spore quando si aprono. Queste sono le spore del pozzo del faro — la prima soglia che hai attraversato.",
    },
    "lampada_eterna": {
        "nome": "Lampada Eterna",
        "lore": "Una luce che brucia da sempre senza consumarsi. I Costruttori dicevano: «la luce vera non viene dal combustibile, viene dalla decisione di brillare». Tu adesso porti questa decisione con te.",
    },
}

# ─────────────────────────────────────────────────────────────────────
# POSIZIONI MAPPA — coordinate normalizzate (0..100) per il map view
# ─────────────────────────────────────────────────────────────────────
MAP_POSITIONS = {
    # Atto I — superficie
    "spiaggia":        {"x": 50, "y": 90, "atto": 1},
    "caletta":         {"x": 70, "y": 88, "atto": 1},
    "grotte":          {"x": 85, "y": 90, "atto": 1},
    "tempio_sommerso": {"x": 95, "y": 95, "atto": 1},
    "foresta":         {"x": 50, "y": 75, "atto": 1},
    "radura":          {"x": 60, "y": 70, "atto": 1},
    "scogliere_sud":   {"x": 30, "y": 92, "atto": 1},
    "cimitero_marino": {"x": 18, "y": 95, "atto": 1},
    "bivio_giungla":   {"x": 70, "y": 50, "atto": 1},
    "cunicolo_nascosto":{"x": 92, "y": 65, "atto": 1},
    "villaggio":       {"x": 38, "y": 65, "atto": 1},
    "molo":            {"x": 22, "y": 70, "atto": 1},
    "giungla":         {"x": 65, "y": 58, "atto": 1},
    "giungla_profonda":{"x": 75, "y": 55, "atto": 1},
    "capanna_luna":    {"x": 80, "y": 48, "atto": 1},
    "sentiero_montagna":{"x":78, "y": 38, "atto": 1},
    "cima_vulcano":    {"x": 78, "y": 25, "atto": 1},
    "scogliere":       {"x": 32, "y": 45, "atto": 1},
    "faro":            {"x": 22, "y": 38, "atto": 1},
    "rovine":          {"x": 78, "y": 60, "atto": 1},
    "sala_guardiano":  {"x": 84, "y": 65, "atto": 1},
    "cripta":          {"x": 90, "y": 70, "atto": 1},
    "laguna":          {"x": 12, "y": 78, "atto": 1},
    # Atto II — sotterranei (sotto al faro)
    "pozzo_faro":        {"x": 22, "y": 28, "atto": 2},
    "cripta_meccanica":  {"x": 22, "y": 22, "atto": 2},
    "corridoio_perduto": {"x": 14, "y": 26, "atto": 2},
    "sala_ingranaggi":   {"x": 35, "y": 18, "atto": 2},
    "corridoio_vapore":  {"x": 30, "y": 30, "atto": 2},
    "forgia_antica":     {"x": 38, "y": 32, "atto": 2},
    "archivio":          {"x": 22, "y": 14, "atto": 2},
    "osservatorio":      {"x": 48, "y": 14, "atto": 2},
    "cuore_macchina":    {"x": 50, "y": 22, "atto": 2},
    "agora_perduta":     {"x": 65, "y": 22, "atto": 2},
    "via_titani":        {"x": 78, "y": 18, "atto": 2},
    "abisso":            {"x": 80, "y": 30, "atto": 2},
    "radice_mondo":      {"x": 90, "y": 22, "atto": 2},
}

# ─────────────────────────────────────────────────────────────────────
# ZONE HOTSPOT — area suggerita (% scena) per oggetti e NPC per stanza
# Se assente: fallback a posizionamento a griglia
# ─────────────────────────────────────────────────────────────────────
ROOM_ZONES = {
    "spiaggia":         {"items": [(30,72),(50,80),(72,75),(40,68)], "npcs":[(50,55)]},
    "caletta":          {"items": [(28,78),(48,76),(72,80)], "npcs":[(50,55)]},
    "grotte":           {"items": [(25,72),(50,80),(75,72)], "npcs":[(50,55)]},
    "tempio_sommerso":  {"items": [(30,76),(55,82),(78,76)], "npcs":[(50,55)]},
    "foresta":          {"items": [(35,72),(60,78),(75,68)]},
    "radura":           {"items": [(28,75),(50,80),(72,72)]},
    "scogliere_sud":    {"items": [(40,75),(65,80)]},
    "cimitero_marino":  {"items": []},
    "bivio_giungla":    {"items": []},
    "corridoio_perduto":{"items": []},
    "cunicolo_nascosto":{"items": [(50,68)]},
    "villaggio":        {"items": [(28,75),(70,76)], "npcs":[(45,52),(60,55)]},
    "molo":             {"items": [(35,75),(60,82),(75,72)]},
    "giungla":          {"items": [(30,75),(55,80),(75,72)]},
    "giungla_profonda": {"items": [(28,72),(50,78),(72,75)]},
    "capanna_luna":     {"items": [(30,72),(50,80),(70,72)], "npcs":[(50,55)]},
    "sentiero_montagna":{"items": [(30,75),(55,80),(75,75)]},
    "cima_vulcano":     {"items": [(30,80),(55,72),(72,82)]},
    "scogliere":        {"items": [(28,75),(55,80)]},
    "faro":             {"items": [(45,80),(60,72)]},
    "rovine":           {"items": [(28,72),(50,80),(72,72)]},
    "sala_guardiano":   {"items": [(50,80)], "npcs":[(50,52)]},
    "cripta":           {"items": [(28,75),(55,82),(72,72)]},
    "laguna":           {"items": [(35,80),(60,75)]},
    # Atto II
    "pozzo_faro":       {"items": [(30,72),(70,75)]},
    "cripta_meccanica": {"items": [(28,75),(50,72),(72,80),(40,68)]},
    "sala_ingranaggi":  {"items": [(25,72),(45,80),(65,72),(78,80)]},
    "corridoio_vapore": {"items": [(35,72),(65,80)]},
    "forgia_antica":    {"items": [(28,75),(72,72)]},
    "archivio":         {"items": [(30,80),(50,72),(70,80)], "npcs":[(50,55)]},
    "osservatorio":     {"items": [(30,80),(72,75)]},
    "cuore_macchina":   {"items": []},
    "agora_perduta":    {"items": [(30,80)], "npcs":[(50,52)]},
    "via_titani":       {"items": [(28,75),(72,80)]},
    "abisso":           {"items": [(30,80),(50,72)]},
    "radice_mondo":     {"items": [(30,75),(70,75)]},
}

EPILOGO_SEGRETO = (
    "EPILOGO SEGRETO — Tutti i dodici frammenti raccolti.\n\n"
    "Hai trovato tutto. Le conchiglie, le perle, i diari, le tavolette: ogni voce dimenticata "
    "che l'isola e le sue profondità avevano nascosto. E ascoltandole tutte insieme, capisci.\n\n"
    "Non sei un naufrago. Non sei MAI stato un naufrago.\n\n"
    "Sei tornato. La tempesta che ti ha portato qui era il tuo modo di tornare — perché tu eri "
    "uno di loro, dei Costruttori, e quando la tua civiltà scese sotto la pietra tu non scendesti "
    "con loro. Restasti fuori. Ti dimenticasti di te. Vagasti per millenni in una vita umana dopo "
    "l'altra, finché finalmente la corrente ti ha riportato a casa.\n\n"
    "Adesso sai chi sei. E loro lo sanno da sempre."
)

FINAL_ATTO_II = (
    "Indossi la Corona Titanica.\n\n"
    "Per un istante, niente. Poi le otto punte si illuminano in cascata, e una luce dolce e fredda "
    "ti avvolge — non un fuoco, ma una luna piena fatta a corona. Sai tutto, di colpo. Sai chi furono "
    "i Costruttori, sai perché scelsero di scendere, sai cosa è l'Albero di Luce: la coscienza addormentata "
    "del mondo stesso, e tu sei il suo nuovo custode.\n\n"
    "L'Albero ti si apre davanti come un fiore. Tu non hai più paura. Tu non sei più solo.\n\n"
    "Da molto, molto in alto, sull'isola, il faro continua a brillare nella notte. Non chiama soccorso. "
    "Chiama il prossimo. Tra cento anni, tra mille, qualcuno lo vedrà, e si chiederà cosa significhi.\n\n"
    "Tu glielo dirai, quando arriverà.\n\n"
    "~ Fine ~"
)

# ─────────────────────────────────────────────────────────────────────
# Output
# ─────────────────────────────────────────────────────────────────────
def tk(d): return {"::".join(k): v for k, v in d.items()}

expansion = {
    "rooms": ROOMS,
    "items": ITEMS,
    "characters": CHARACTERS,
    "dialogues": DIALOGUES,
    "recipes": RECIPES,
    "room_actions": tk(ROOM_ACTIONS),
    "deliveries": tk(DELIVERIES),
    "puzzles_interactive": PUZZLES,
    "blocked_destinations": BLOCKED_DESTS,
    "room_patches": ROOM_PATCHES,
    "finale_atto_ii": FINAL_ATTO_II,
    "collectibles": COLLECTIBLES,
    "map_positions": MAP_POSITIONS,
    "room_zones": ROOM_ZONES,
    "epilogo_segreto": EPILOGO_SEGRETO,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(expansion, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"  rooms={len(ROOMS)} items={len(ITEMS)} npcs={len(CHARACTERS)} "
      f"recipes={len(RECIPES)} deliveries={len(DELIVERIES)} actions={len(ROOM_ACTIONS)} "
      f"interactive_puzzles={len(PUZZLES)}")
