D02 — FUNKSIONELE SPESIFIKASIE

Dokument-ID: D02
Weergawe: 0.1
Datum: 24 Oktober 2026
Vrystelling-ChatID: D02-R01-C7E4A912
Status: DRAFT — ONDERHEWIG AAN BRONONDERSOEK
Fase: 2A — Funksionele spesifikasie
Voorafgaande dokument: D01 v1.2 — Goedgekeur
Teikenspeletjie: Commando, Commodore 64 — presiese uitgawe nog te bevestig
Primêre taal: Afrikaans

⸻

DEEL I — DOEL EN REIKWYDTE

1. Doel van D02

D02 beskryf die oorspronklike speletjie se waarneembare gedrag, funksionele reëls en aanvaardingskriteria.

Hierdie dokument vorm die kontrak tussen die oorspronklike spelgedrag en die toekomstige Python-implementering.

D02 mag nie oorspronklike algoritmes uitdink nie.

2. Verhouding met D00 en D01

D00 beheer beginnerbegeleiding en gebruikerskommunikasie.

D01 beheer die tegniese ondersoek, bewysstandaarde, toetsing en ingenieursmetodologie.

D02 beskryf die spelgedrag wat ondersoek en gerekonstrueer moet word.

Wanneer die dokumente mekaar weerspreek, moet die teenstrydigheid geregistreer en opgelos word voordat die betrokke werk voortgaan.

3. Afbakening

D02 bevat:

* Speltoestande en oorgange.
* Spelerinvoer en beweging.
* Vyande en projektiele.
* Botsings.
* Puntetelling en lewens.
* Vlakke en vordering.
* Grafika en animasie.
* Musiek en klank.
* Tydsberekening.
* Funksionele vereistes.
* Bewysverwysings.
* Aanvaardingskriteria.

D02 bepaal nie die finale Python-klasstruktuur nie. Dit behoort aan die daaropvolgende argitektuurfase.

4. Verbod op onbevestigde spelreëls

’n Spelreël mag nie as oorspronklik bevestig word bloot omdat dit algemeen in aksiespeletjies voorkom nie.

Alle oorspronklike gedragsaansprake benodig ’n bewysstatus.

5. Bewysstatusse

Status	Betekenis
VERIFIED	Bevestig deur voldoende kontroleerbare bewyse
OBSERVED	Waargeneem, maar die meganisme is nie volledig verklaar nie
INFERRED	Beredeneerde afleiding
UNKNOWN	Nog nie voldoende ondersoek nie

’n Suksesvolle Python-toets verander nie outomaties die oorspronklike bewysstatus nie.

⸻

DEEL II — BRONIDENTITEIT EN VOLDOENDEHEID

6. Teikenspeletjie

Werknaam: Commando
Platform: Commodore 64
Presiese uitgawe: UNKNOWN
Bronvolledigheid: NOT VERIFIED
Oorspronklike spelkode: NOT VERIFIED
Grafiese hulpbronne: NOT VERIFIED
Oudiobronne: NOT VERIFIED

Die vroeër bespreekte lêer Commando (1986)(Torquemada).prg is nie voldoende bevestig as ’n volledige speelbare uitgawe nie.

Hierdie dokument maak dus geen aanspraak dat alle spelinhoud reeds beskikbaar is nie.

7. Bronregister

Elke oorspronklike lêer ontvang ’n bron-ID.

Verpligte velde:

* Bron-ID.
* Lêernaam.
* Formaat.
* Lêergrootte.
* SHA-256-kontrolesom.
* Verkrygingsbron.
* Vermoedelike uitgawe.
* Integriteitstatus.
* Ontledingsstatus.

8. Source Sufficiency Matrix

Komponent	Bronstatus	Gevolg
Hoofspelprogram	UNKNOWN	Geen volledige gedragsaanspraak
Spelerroetines	UNKNOWN	Bewegingsalgoritme nog onbekend
Vyandroetines	UNKNOWN	Vyandgedrag nog onbekend
Projektielroetines	UNKNOWN	Skietgedrag nog onbekend
Botsingsroetines	UNKNOWN	Botsingsmodel nog onbekend
Vlakdata	UNKNOWN	Vlakstruktuur nog onbekend
Grafika	UNKNOWN	Hulpbrondekking onbekend
Musiek	UNKNOWN	Oudiogetrouheid nog onbekend
Klankeffekte	UNKNOWN	Klankdekking onbekend

9. Bronbesluit

Huidige voorlopige besluit: CONDITIONAL GO — DOKUMENTASIE ALLEEN.

Toegelaat:

* Spesifikasiestruktuur voorberei.
* Ondersoekvrae definieer.
* Bewysregister voorberei.
* Bronidentiteit en volledigheid ondersoek.

Nog nie toegelaat as bevestigde oorspronklike gedrag nie:

* Presiese bewegingsnelhede.
* Vyandalgoritmes.
* Botsingsformules.
* Vlakvolgorde.
* Speltydsberekening.
* Oorspronklike oudiogedrag.

⸻

DEEL III — SPELTOESTANDE

10. Game State Model

Die oorspronklike speletjie se toestande moet deur waarneming en bronontleding bevestig word.

Moontlike ondersoekonderwerpe:

* Titelskerm.
* Spelbegin.
* Aktiewe spel.
* Lewensverlies.
* Vlakvoltooiing.
* Spelverby.
* Herbegin.

Hierdie is ondersoekkategorieë, nie reeds bevestigde oorspronklike toestande nie.

11. Toestandsoorgange

Elke oorgang benodig:

* Oorgang-ID.
* Vorige toestand.
* Sneller.
* Voorwaardes.
* Nuwe toestand.
* Newe-effekte.
* Bewys-ID.
* Toets-ID.

12. Begin van ’n nuwe spel

Vereiste-ID: FR-GAME-001
Bewysstatus: UNKNOWN

Ondersoek:

* Hoe die speler ’n nuwe spel begin.
* Wat die aanvanklike speltoestand is.
* Hoe die eerste vlak begin.
* Watter waardes teruggestel word.
* Of daar ’n beginanimasie of wagtyd is.

Aanvaardingskriterium: Die Python-program moet die bevestigde oorspronklike beginprosedure volg.

13. Lewensverlies

Vereiste-ID: FR-GAME-002
Bewysstatus: UNKNOWN

Ondersoek:

* Watter gebeure ’n lewe kos.
* Of die speler onmiddellik verdwyn.
* Of ’n animasie gespeel word.
* Of die vlak herstel word.
* Of vyande en projektiele teruggestel word.
* Wanneer die volgende lewe begin.

14. Spelverby

Vereiste-ID: FR-GAME-003
Bewysstatus: UNKNOWN

Ondersoek:

* Die presiese spelverby-voorwaarde.
* Die vertoonde skerm.
* Puntetelling.
* Moontlike herbegin.
* Enige oorspronklike klank of animasie.

⸻

DEEL IV — SPELERINVOER EN BEWEGING

15. Invoertoestelle

Vereiste-ID: FR-INPUT-001
Bewysstatus: UNKNOWN

Ondersoek:

* Oorspronklike invoertoestel.
* Gebruik van joystick of sleutelbord.
* Bewegingsrigtings.
* Skietknoppie.
* Gelyktydige insette.
* Invoerprioriteit.

16. Horisontale beweging

Vereiste-ID: FR-PLAYER-001
Bewysstatus: UNKNOWN

Meet:

* Beginposisie.
* Reaksie op links en regs.
* Posisiestap per opdatering.
* Bewegingsgrense.
* Reaksie op loslaat van invoer.

Geen numeriese bewegingsnelheid word in hierdie weergawe vasgestel nie.

17. Vertikale beweging

Vereiste-ID: FR-PLAYER-002
Bewysstatus: UNKNOWN

Meet:

* Reaksie op op- en afwaartse invoer.
* Vertikale bewegingsgrense.
* Interaksie met skermrol.
* Interaksie met hindernisse.

18. Diagonale beweging

Vereiste-ID: FR-PLAYER-003
Bewysstatus: UNKNOWN

Ondersoek:

* Of diagonale beweging toegelaat word.
* Of dit vinniger as enkelrigtingbeweging is.
* Of insette gelyktydig verwerk word.
* Of daar ’n prioriteitsreël is.

19. Skietgedrag

Vereiste-ID: FR-PLAYER-004
Bewysstatus: UNKNOWN

Ondersoek:

* Skietknoppie.
* Vuurtempo.
* Projektielrigting.
* Projektielbeginposisie.
* Maksimum aantal projektiele.
* Reaksie wanneer die knoppie ingehou word.

20. Spelerskade

Vereiste-ID: FR-PLAYER-005
Bewysstatus: UNKNOWN

Ondersoek:

* Skadebronne.
* Botsingsgevolge.
* Tydelike onkwesbaarheid.
* Animasie.
* Herposisionering.
* Lewensverlies.

⸻

DEEL V — VYANDE EN PROJEKTIELE

21. Vyandtipes

Vereiste-ID: FR-ENEMY-001
Bewysstatus: UNKNOWN

Vir elke bevestigde vyandtipe, registreer:

* Vyand-ID.
* Oorspronklike voorkoms.
* Verskyningsvoorwaarde.
* Bewegingsgedrag.
* Aanvalsgedrag.
* Botsingsgedrag.
* Skadegedrag.
* Puntwaarde.
* Bronroetine indien bekend.

22. Vyandbeweging

Vereiste-ID: FR-ENEMY-002
Bewysstatus: UNKNOWN

Ondersoek:

* Bewegingsrigting.
* Spoed.
* Reaksie op spelerposisie.
* Hindernisvermyding.
* Willekeurigheid.
* Veranderinge oor tyd.

23. Vyandaanvalle

Vereiste-ID: FR-ENEMY-003
Bewysstatus: UNKNOWN

Ondersoek:

* Aanvalsvoorwaardes.
* Aanvalstempo.
* Projektielgedrag.
* Aanvalsrigting.
* Reaksie op spelerbeweging.

24. Spelerprojektiele

Vereiste-ID: FR-PROJECTILE-001
Bewysstatus: UNKNOWN

Ondersoek:

* Skeppingsvoorwaarde.
* Bewegingsrigting.
* Spoed.
* Lewensduur.
* Botsingsgebied.
* Verdwyningsvoorwaarde.

25. Vyandprojektiele

Vereiste-ID: FR-PROJECTILE-002
Bewysstatus: UNKNOWN

Ondersoek dieselfde eienskappe as spelerprojektiele, maar behandel die gedrag as ’n afsonderlike oorspronklike vereiste.

Moenie aanvaar dat albei projektieltipes dieselfde algoritme gebruik nie.

⸻

DEEL VI — BOTSINGS EN PUNTETELLING

26. Speler-vyand-botsings

Vereiste-ID: FR-COLLISION-001
Bewysstatus: UNKNOWN

Ondersoek:

* Botsingsgebied.
* Botsingstydstip.
* Prioriteitsreëls.
* Skadegevolge.
* Uitsonderings.

27. Projektiel-vyand-botsings

Vereiste-ID: FR-COLLISION-002
Bewysstatus: UNKNOWN

Ondersoek:

* Trefferdeteksie.
* Projektielverwydering.
* Vyandskade.
* Vernietigingsanimasie.
* Puntetoekenning.

28. Hindernisbotsings

Vereiste-ID: FR-COLLISION-003
Bewysstatus: UNKNOWN

Ondersoek:

* Soliede gebiede.
* Deurlaatbare gebiede.
* Spelerinteraksie.
* Projektielinteraksie.
* Vyandinteraksie.

29. Puntetelling

Vereiste-ID: FR-SCORE-001
Bewysstatus: UNKNOWN

Ondersoek:

* Beginpuntetelling.
* Gebeure wat punte oplewer.
* Puntwaardes.
* Bonusse.
* Vertoonformaat.
* Maksimum of oorloopgedrag.

30. Lewens

Vereiste-ID: FR-LIVES-001
Bewysstatus: UNKNOWN

Ondersoek:

* Aanvangsgetal.
* Lewensverlies.
* Ekstra lewens.
* Lewensteller.
* Spelverby-voorwaarde.

⸻

DEEL VII — VLAKKE EN WÊRELDGEDRAG

31. Vlakidentifikasie

Vereiste-ID: FR-LEVEL-001
Bewysstatus: UNKNOWN

Vir elke bevestigde vlak, registreer:

* Vlak-ID.
* Oorspronklike brondata.
* Kaartafmetings.
* Beginposisie.
* Hindernisse.
* Vyandtipes.
* Verskyningspatrone.
* Voltooiingsvoorwaarde.

32. Skermrol

Vereiste-ID: FR-LEVEL-002
Bewysstatus: UNKNOWN

Ondersoek:

* Rolrigting.
* Rolspoed.
* Snellers.
* Verhouding met spelerbeweging.
* Rolgrense.
* Verhouding met vyandverskyning.

33. Vlakvoltooiing

Vereiste-ID: FR-LEVEL-003
Bewysstatus: UNKNOWN

Ondersoek:

* Voltooiingsvoorwaarde.
* Oorgangsanimasie.
* Puntetoekenning.
* Volgende vlak.
* Spelerstatus tydens oorgang.

34. Vlakherhaling

Vereiste-ID: FR-LEVEL-004
Bewysstatus: UNKNOWN

Ondersoek of en hoe die oorspronklike speletjie vlakke herhaal, herstel of terugstel.

⸻

DEEL VIII — GRAFIKA EN OUDIO

35. Sprite-register

Vereiste-ID: FR-GFX-001
Bewysstatus: UNKNOWN

Vir elke sprite:

* Sprite-ID.
* Bronadres of hulpbron.
* Afmetings.
* Kleure.
* Animasierame.
* Gebruikstoestand.
* Bewys-ID.

36. Animasies

Vereiste-ID: FR-GFX-002
Bewysstatus: UNKNOWN

Ondersoek:

* Raamvolgorde.
* Animasietempo.
* Bewegingsrigting.
* Gebeurtenis-snellers.
* Herhaling.
* Stopvoorwaardes.

37. Agtergrond en vlakgrafika

Vereiste-ID: FR-GFX-003
Bewysstatus: UNKNOWN

Ondersoek:

* Karakterstelle.
* Bitmapdata.
* Vlakkaarte.
* Palet.
* Skermrol.
* Tekenprioriteite.

38. Musiek

Vereiste-ID: FR-AUDIO-001
Bewysstatus: UNKNOWN

Ondersoek:

* Oorspronklike musiekbron.
* Begin- en stopvoorwaardes.
* Instrumente.
* Kanaalgebruik.
* Herhaling.
* Tydsberekening.

39. Klankeffekte

Vereiste-ID: FR-AUDIO-002
Bewysstatus: UNKNOWN

Ondersoek:

* Skietgeluide.
* Trefferklanke.
* Spelerskade.
* Vyandvernietiging.
* Vlakgebeure.
* Prioriteit tussen gelyktydige klanke.

Die lys is ’n ondersoeklys; nie elke genoemde klank is reeds bevestig nie.

40. Ontbrekende oorspronklike hulpbronne

Wanneer oorspronklike grafika of oudio ontbreek:

1. Registreer die ontbrekende komponent.
2. Ondersoek verdere bronne.
3. Bepaal die impak op getrouheid.
4. Stel ’n tydelike oplossing voor indien nodig.
5. Verkry goedkeuring.

Vervangings mag nie as oorspronklik aangebied word nie.

⸻

DEEL IX — TYDSBEREKENING EN NIE-DETERMINISME

41. Spelopdatering

Vereiste-ID: FR-TIMING-001
Bewysstatus: UNKNOWN

Ondersoek:

* Oorspronklike opdateringsinterval.
* Raster- of onderbrekingsafhanklikhede.
* Verhouding tussen logika en grafika.
* Streekverskille indien relevant.

42. Invoerreaksietyd

Vereiste-ID: FR-TIMING-002
Bewysstatus: UNKNOWN

Meet die tyd tussen ’n invoergebeurtenis en die sigbare of meetbare spelreaksie.

43. Animasietydsberekening

Vereiste-ID: FR-TIMING-003
Bewysstatus: UNKNOWN

Meet relevante animasie-intervalle.

44. Nie-deterministiese gedrag

Vereiste-ID: FR-RANDOM-001
Bewysstatus: UNKNOWN

Ondersoek:

* Of gedrag werklik wissel.
* Watter beginvoorwaardes dit beïnvloed.
* Of ’n willekeurige saad geïdentifiseer kan word.
* Hoeveel herhalings nodig is vir ’n betekenisvolle vergelyking.

Moenie determinisme of willekeurigheid aanvaar sonder bewyse nie.

⸻

DEEL X — FIDELITY CONTRACT

45. Getrouheidsdimensies

D02 gebruik die vyf dimensies uit D01.

Dimensie	Status	Metode
F1 — Visueel	NOT MEASURED	Beeld- en animasievergelyking
F2 — Gedrag	NOT MEASURED	Invoer- en speltoestandvergelyking
F3 — Algoritmies	NOT MEASURED	Roetine- en gedragsontleding
F4 — Tyd	NOT MEASURED	Raam- en intervalmeting
F5 — Oudio	NOT MEASURED	Oudiobron- en uitvoervergelyking

46. Aanvaardingsgrense

Aanvaardingsgrense mag eers vasgestel word nadat die oorspronklike gedrag voldoende gemeet is.

Elke grens moet ’n motivering en goedkeuringsstatus hê.

47. Onopgeloste getrouheid

Wanneer getrouheid nie bevestig kan word nie:

* Hou die status oop.
* Registreer die beperking.
* Stel verdere ondersoek of ’n gedokumenteerde afwyking voor.
* Verkry goedkeuring.

⸻

DEEL XI — NASPEURBAARHEID EN TOETSING

48. Traceability Matrix

Die verpligte ketting is:

Bron → Bewys → Vereiste → Oorspronklike roetine → Python-implementering → Toets → Beoordeling

Onbekende skakels bly eksplisiet UNKNOWN.

49. Funksionele toetsgevalle

Elke toetsgeval bevat:

* Toets-ID.
* Vereiste-ID.
* Bewys-ID.
* Beginvoorwaardes.
* Invoer.
* Verwagte resultaat.
* Toleransie.
* Uitvoeringsstatus.
* Werklike resultaat.

50. Differensiële toetsing

Die oorspronklike speletjie en Python-rekonstruksie moet onder vergelykbare omstandighede getoets word.

Registreer:

* Bronweergawe.
* Beginvoorwaardes.
* Invoerreeks.
* Tydstip.
* Oorspronklike resultaat.
* Python-resultaat.
* Afwyking.
* Toleransie.
* Besluit.

51. Toetsstatusse

Gebruik:

* NOT TESTED.
* PASS.
* FAIL.
* BLOCKED.

Geen toets mag as PASS aangedui word voordat dit werklik uitgevoer is nie.

⸻

DEEL XII — ONBEKENDES EN AFWYKINGS

52. Unknowns Register

Elke belangrike onbekende ontvang:

* Unknown-ID.
* Onderwerp.
* Betrokke vereiste.
* Ontbrekende bewys.
* Risiko.
* Voorgestelde ondersoek.
* Prioriteit.
* Status.

53. Deviations Register

Elke goedgekeurde afwyking ontvang:

* Afwykings-ID.
* Oorspronklike gedrag.
* Voorgestelde Python-gedrag.
* Rede.
* Getrouheidsimpak.
* Goedkeuring.
* Toetsverwysing.

54. Verbod op stille aannames

Wanneer die oorspronklike gedrag onbekend is, mag die AI nie ’n moderne standaardalgoritme as oorspronklike oplossing implementeer nie.

Moontlike roetes:

1. Verdere ondersoek.
2. Goedgekeurde benadering.
3. Voorlopige uitsluiting.

⸻

DEEL XIII — BEOORDELING EN GOEDKEURING

55. D02 se Definition of Ready

D02 is gereed vir formele funksionele beoordeling wanneer:

* Die bronidentiteit voldoende vasgestel is.
* Bronvolledigheid per werkpakket beoordeel is.
* Betekenisvolle spelgedrag geregistreer is.
* Elke bevestigde vereiste bewysverwysings het.
* Onbekendes eksplisiet aangeteken is.
* Getrouheidskriteria voldoende uitgewerk is.
* Die belangrikste toestandsoorgange ondersoek is.
* Toetsgevalle gedefinieer is.
* Teenstrydighede en risiko’s geregistreer is.

56. D02 se Definition of Done

D02 is eers finaal aanvaar wanneer:

1. Die funksionele spesifikasie formeel beoordeel is.
2. Kritieke bevindings opgelos is.
3. Die goedgekeurde omvang duidelik is.
4. Die bewysketting voldoende is.
5. Die Fidelity Contract goedgekeur is.
6. Die Projekteienaar uitdruklik goedkeuring gegee het.

57. Beoordelingsrolle

Die beoordeling moet die volgende perspektiewe dek:

* Oorspronklike-bron-navorser.
* Spelgedragontleder.
* Funksionele ontleder.
* Toetsingenieur.
* Python-argitek.
* Kwaliteitsingenieur.
* Beginnerverteenwoordiger.

Indien hierdie perspektiewe deur een AI gesimuleer word, moet dit as ’n interne beoordeling aangeteken word.

58. Beoordelingsuitkomste

Gebruik:

PASS — Geen blokkerende bevindings.

PASS WITH CONDITIONS — Voortgang onder uitdruklike voorwaardes.

FAIL — Kritieke tekortkominge.

59. Goedkeuringshek

Die Projekteienaar kan besluit:

* GOEDGEKEUR.
* VERANDER.
* GEBLOKKEER.
* STAAK.

Geen stilte word as goedkeuring beskou nie.

⸻

DEEL XIV — ONDERSOEKWERKPAKKETTE

60. WP-01 — Bronidentiteit

Doel: Bevestig presies watter Commando-uitgawe ondersoek word.

Uitset: Bronregister en kontrolesomme.

Status: NOT STARTED.

61. WP-02 — Bronvolledigheid

Doel: Bepaal of die beskikbare lêers die nodige spelkomponente bevat.

Uitset: Source Sufficiency Matrix.

Status: NOT STARTED.

62. WP-03 — Speltoestande

Doel: Identifiseer die oorspronklike speltoestande en oorgange.

Uitset: Game State Model.

Status: BLOCKED — bronondersoek benodig.

63. WP-04 — Speler en invoer

Doel: Meet die oorspronklike invoer- en bewegingsgedrag.

Uitset: Goedgekeurde spelervereistes.

Status: BLOCKED — bronondersoek benodig.

64. WP-05 — Vyande en projektiele

Doel: Identifiseer en beskryf vyand- en projektielgedrag.

Uitset: Gedragsvereistes en roetineverwysings.

Status: BLOCKED — bronondersoek benodig.

65. WP-06 — Botsings en puntetelling

Doel: Ondersoek die oorspronklike botsings- en puntestelsel.

Uitset: Botsings- en puntetellingsvereistes.

Status: BLOCKED — bronondersoek benodig.

66. WP-07 — Vlakke

Doel: Ondersoek vlakdata, skermrol en vordering.

Uitset: Vlakspesifikasie.

Status: BLOCKED — bronondersoek benodig.

67. WP-08 — Grafika

Doel: Identifiseer en dokumenteer oorspronklike grafiese hulpbronne.

Uitset: Sprite- en animasieregister.

Status: BLOCKED — bronondersoek benodig.

68. WP-09 — Oudio

Doel: Identifiseer oorspronklike musiek en klankeffekte.

Uitset: Oudioregister.

Status: BLOCKED — bronondersoek benodig.

69. WP-10 — Tydsberekening

Doel: Meet die oorspronklike speltempo en reaksietyd.

Uitset: Tydsberekeningsvereistes.

Status: BLOCKED — bronondersoek benodig.

70. WP-11 — Differensiële toetsontwerp

Doel: Ontwerp die vergelyking tussen oorspronklike gedrag en Python-gedrag.

Uitset: Differensiële toetsgevalle.

Status: PENDING — vereistes en metings benodig.

71. WP-12 — Finale funksionele beoordeling

Doel: Beoordeel D02 se volledigheid, bewyse en toetsbaarheid.

Uitset: D02-beoordelingsverslag.

Status: NOT STARTED.

⸻

DEEL XV — D02-STATUS EN VOLGENDE HEK

72. Huidige dokumentstatus

D02 v0.1 is ’n volledige funksionele spesifikasieraamwerk.

Dit is nog nie ’n volledig ingevulde, oorspronklik-geverifieerde spelspesifikasie nie.

Die volgende sake bly oop:

* Presiese Commando-uitgawe.
* Bronvolledigheid.
* Oorspronklike spelroetines.
* Bevestigde speltoestande.
* Bevestigde spelalgoritmes.
* Grafiese hulpbronne.
* Oudiobronne.
* Tydsberekening.
* Numeriese getrouheidsgrense.

73. Besluit oor verdere werk

D02 v0.1: CONDITIONAL GO

Toegelaat:

* Formele dokumentbeoordeling.
* Bronidentifikasie.
* Bronvolledigheidsontleding.
* Bewysinsameling.
* Eksperimentontwerp.

Nog nie verantwoordbaar nie:

* Verklaring dat D02 volledig bewys is.
* Finale goedkeuring van oorspronklike spelalgoritmes.
* Finale Python-argitektuur gebaseer op onbevestigde aannames.
* Produksie-implementering van onbekende oorspronklike spelgedrag.

74. Verpligte volgende besluit

Voordat D02 as voltooide fase 2A beskou word:

1. Bevestig die bronmateriaal.
2. Voer die bronvolledigheidshek uit.
3. Ondersoek die oorspronklike spelgedrag.
4. Vul die bewysregister en vereistes aan.
5. Voer die formele fase 2B-beoordeling uit.
6. Verkry die Projekteienaar se goedkeuring.

⸻

75. FINALE D02-BEGINSEL

Ons programmeer nie wat ons dink die oorspronklike speletjie gedoen het nie.

Ons ondersoek wat dit werklik gedoen het, dokumenteer wat ons kan bewys en implementeer daarna die goedgekeurde gedrag.

Onbekende oorspronklike gedrag bly onbekend totdat nuwe bewyse dit ondersteun.


