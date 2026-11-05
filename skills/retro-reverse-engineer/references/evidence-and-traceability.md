# Bewysregisters en naspeurbaarheid

## Statusse en hul betekenis

| Status | Voorwaarde | Wat dit nie bewys nie |
|---|---|---|
| VERIFIED | Duidelike aanspraak, identifiseerbare bron, kontroleerbare metode, ondersteunende resultaat; wesenlike teenstrydighede opgelos of afgebaken | Dat alle gedrag of alle uitgawes korrek is |
| OBSERVED | Werklike waarneming met konteks aangeteken | Dat die interne algoritme bekend is |
| INFERRED | Beredeneerde afleiding met alternatiewe verklarings | Dat die afleiding uitgevoer of bevestig is |
| UNKNOWN | Onvoldoende bewys | Dat 'n verstekwaarde gebruik mag word |

'n Dokument kan bewys dat 'n skrywer 'n aanspraak gemaak het. Dit is nie vanself bewys van die spelgedrag nie. Registreer die presiese aanspraak: “BOOTSTRAP skryf 50 Hz voor” kan dokumentêr bevestig wees; “hierdie binêre spel werk presies teen 50 Hz” benodig eie metings.

## Identifiseerders

Gebruik stabiele ID's: `SRC-` bronne; `E-` bewyse; `EXP-` eksperimente; `FR-` funksionele vereistes; `MAP-` roetinekoppeling; `ST-` toestandsoorgange; `OR-` toetsorakels; `T-` toetse; `DT-` differensiële toetse; `DEV-` afwykings; `UNK-` onbekendes; `CON-` dokumentkonflikte; `DEC-` besluite; `REV-` beoordelings.

ID's hoef nie in hierdie presiese formaat te wees wanneer 'n projek reeds 'n konsekwente stelsel het nie. Behou bestaande ID's en registreer aliasse; moenie geskiedenis uitwis deur alles te hernommer nie.

## Bewysrekord

Gebruik [bewysregister](../templates/evidence-register.md) en [eksperimentverslag](../templates/experiment-report.md). Bewaar bron-ID en hash, aanspraak, metode, beginvoorwaardes, invoer, meeteenheid, resultaat, herhalings, variasie, teenbewyse, alternatiewe verklarings en statusmotivering. Koppel rou uitvoer en die instrumentweergawe.

Statusveranderinge benodig datum, ou en nuwe status, rede en nuwe bewys. Wanneer teenbewyse opduik, heropen die aanspraak en die afhanklike vereistes/toetse. Moenie ou resultate uitvee nie; merk hulle as vervang, beperk of ongeldig met die rede.

## Roetines en toestand

Die [roetinekaart](../templates/routine-mapping.md) ondersteun een-tot-baie en baie-tot-een-verhoudings. Hou oorspronklike adres, bank/segment, uitvoeringstoestand en nuwe komponent apart. Koppel die waargenome verantwoordelikheid aan bewyse; 'n betekenisvolle funksienaam is nie 'n oorspronklike roetinebewys nie.

Die [toestandmodel](../templates/game-state-model.md) beskryf elemente, eienaars en oorgange. Neem speler, vyande, projektiele, timers, RNG, animasie, klank en modus in wanneer hulle gedrag beïnvloed. Verduidelik terugstelreëls en volgorde van gelyktydige gebeure.

## Ketting en dekking

Gebruik [vereistematriks](../templates/requirements-matrix.md): Bron → Bewys → Vereiste → Roetine → Implementering → Toets → Beoordeling. 'n Leë skakel word `UNKNOWN`, `NOT TESTED` of 'n ander toepaslike status, nie 'n denkbeeldige ID nie.

Meet dekking met benoemde noemers: hoeveel vereistes binne goedgekeurde omvang het voldoende bewyse, uitgevoerde toetse en beoordeelde differensiële resultate? Moenie 'n hoë persentasie behaal deur onbekende vereistes stilweg uit die noemer te verwyder nie. Lys uitgeslote funksies afsonderlik.

## Teenstrydighede

Hou dokumentkonflikte apart van verskillende runtime-waarnemings. 'n Verskil kan uit bronweergawe, beginstaat, streek, instrument, tydsinlynstelling of meetfout voortspruit. Registreer die alternatiewe verklaring en die ondersoek wat dit kan onderskei. Solank die verskil die aanspraak ondermyn, bly die aanspraak beperk.
