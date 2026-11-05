# Fasehekke, beoordeling en vrystelling

## Besluitstatusse is nie uitruilbaar nie

`GO` / `CONDITIONAL GO` / `BLOCKED` / `STOP` beskryf uitvoerbaarheid vir 'n benoemde werkpakket. `PASS` / `PASS WITH CONDITIONS` / `FAIL` beskryf 'n beoordeling. `GOEDGEKEUR` / `VERANDER` / `GEBLOKKEER` / `STAAK` is die eienaar se besluit. `TESTED` beskryf uitvoering en is nie vanself PASS nie.

Gebruik [phase-gate.md](../templates/phase-gate.md). Elke hek benoem artefak, weergawe/hash, fase, omvang, verpligte bewyse, resultaat, oop risiko's, voorwaardes, eienaar en volgende toegelate stap. 'n Voorwaarde moet toetsbaar wees, met verantwoordelike persoon en herbeoordelingspunt.

## Hekvereistes

| Hek | Minimum bewys | Blokkerende voorbeeld |
|---|---|---|
| Dokumentbasis | D00/D01/D02-inventaris en konflikte | Onbekende reëls word as goedgekeur aangebied |
| Bronvoldoendeheid | Komponentmatriks vir die volgende werk | Slegs intro beskikbaar vir vyandlogika |
| Uitvoeringsvermoë | Werklike kode-/toetsroete | Geen manier om implementering te toets nie |
| Funksionele gereedheid | FR/E-koppeling, toestandmodel, F1–F5 en orakels | Onbekende waarde word as oorspronklike reël gebruik |
| Argitektuur | Vereistes, ontwerp, afhanklikhede, profiel en afwykings | Taal of lêerstruktuur stilweg verander |
| Inkrement | Voorbeoordeling, RED/GREEN/REFACTOR, regressie en nabeoordeling | Toetsuitslae word net verwag, nie uitgevoer nie |
| Bronweergawe | Impak op bewyse, toetse en roetines | Bewyse van ander uitgawe word blind oorgedra |
| Vrystelling | Bewyspakket, tegniese én gebruikersaanvaarding | Getrouheid word uit speelbaarheid afgelei |

## Beoordeling

Beoordeel vóór implementering die vereiste, bewyse, ontwerp, toetsplan en risiko. Beoordeel daarna die kode, werklike uitslae, oorspronklike vergelyking, regressies en naspeurbaarheid. Gebruik 'n afsonderlike beoordelaar waar beskikbaar en gemagtig; anders merk die beoordeling uitdruklik intern. 'n Rolspel met verskillende perspektiewe bly gesimuleerd.

Kritieke bevindings blokkeer die geraakte werk. Herstel en hertoets voordat dit gesluit word. Behou afgewese hipoteses en vorige mislukte toetse in die rekord.

## Vrystellingsbewyspakket

Gebruik [release-evidence.md](../templates/release-evidence.md). Sluit weergawe, vrystelling-ChatID, bronkodeweergawe, oorspronklike hashes, goedgekeurde vereistes, toets-/regressie-/differensiële resultate, beoordelings, F1–F5-status, prestasie, afwykings, risiko's en eienaarsbesluit in.

Die vrystelling-ChatID is 'n mensleesbare naspeurbaarheidsetiket. Registreer die werklike gesprek-ID apart indien beskikbaar; moenie 'n kort etiket as 'n stelselgegenereerde gesprek-ID voorgee nie.

Gebruik RELEASE APPROVED, RELEASE CONDITIONAL of RELEASE BLOCKED volgens die bewys en besluit. 'n ZIP wat korrek oopmaak is 'n verpakkingstoets, nie 'n metodologie- of spelgetrouheidstoets nie.

## Regte en verspreiding

Registreer die regtestatus van oorspronklike program, grafika, musiek en derdepartykomponente wanneer verspreiding ter sprake kom. 'n Tegniese onttrekking skep nie 'n bewys van verspreidingstoestemming nie. Hou onseker materiaal uit 'n publieke pakket totdat die toepaslike besluit bestaan. Hierdie skill bevat geen ROM's, oorspronklike spelgrepe of oudiobates nie.

## Drie afsonderlike aanvaardings

DOCUMENT APPROVED: inhoud beoordeel. BEGINNER PILOT PASSED: werklike beginnerproef met waarnemings. METHOD VALIDATED: genoeg relevante praktiese gevalle ondersoek. Geen van hierdie statusse volg outomaties uit die ander nie.
