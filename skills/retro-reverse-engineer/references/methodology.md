# Metodologie: bewysgedrewe rekonstruksie

## Inhoud
Doel en werkstrome; fasepad; inkremente; onsekerheid; hervatting.

## Drie werkstrome, een bewysketting

**A — Bronontleding:** bepaal wat die oorspronklike medium en program bevat. Lewer identifiseerbare bronne, onttrekkings, roetinekaarte en bronvoldoendeheid per komponent.

**B — Gedragsontleding:** bepaal wat die oorspronklike program doen. Lewer herhaalbare invoerreekse, toestandsoorgange, metings en toetsbare vereistes. Gebruik die bronweergawe uit A; moenie 'n video van 'n ander uitgawe as dieselfde orakel behandel nie.

**C — Rekonstruksie:** reproduseer goedgekeurde gedrag in nuwe logika. Lewer ontwerp, falende en slagende toetse, klein implementeringsinkremente en oorspronklike vergelykings. C mag nie ontbrekende kennis uit A of B met 'n geloofwaardige algoritme vul en dit oorspronklik noem nie.

Die metodologie is ook bruikbaar wanneer slegs 'n deel van die spel ontleed kan word. Benoem dan die gedekte funksies en uitgeslote komponente; 'n beperkte rekonstruksie is 'n geldige resultaat as die aansprake ooreenstem met die bewyse.

## Formele fasepad

Behoud die D00/D01-fasenommers in bestaande RETRORECON-projekte:

| Fase | Invoer | Uitset en toets | Volgende hek |
|---|---|---|---|
| Proefprojek 0 | Gebruikersdoel, beskikbare omgewing | Eerste klein geverifieerde bevinding; aparte beginnerbeoordeling | Uitvoeringsroete en hervatbaarheid |
| 0A / 0B | Doel, bronstatus, beperkings | Missie en kritiese beoordeling | Eienaar aanvaar omvang |
| 1A / 1B | Dokumentbasis en profiele | D01-konsep en verenigbaarheidsbeoordeling | Reëls en konflikbesluite |
| 2A / 2B | Oorspronklike bewyse | D02, F1–F5, toestandmodel, vereistes | Bewysdekking en toetsbaarheid |
| 3A / 3B | Goedgekeurde vereistes | Argitektuur, afwykings, uitvoeringsroete | Ontwerpbeoordeling |
| 4A / 4B | Ontwerp en afhanklikhede | Geprioritiseerde werkpakkette en toetsplan | Uitvoerbare inkrementplan |
| 5 | Goedgekeurde werkpakket | RED/GREEN/REFACTOR, regressie, differensiële resultate | Beoordeling per inkrement |
| 6 | Alle vrystellingsbewyse | Tegniese én gebruikersaanvaarding | Vrystellingsbesluit |

Bronvoldoendeheid is 'n dwarsliggende hek: herhaal dit wanneer die werkpakket of bronweergawe verander. Dit is nie een vroeë vinkie wat alle latere werk ontsluit nie. 'n Ontbrekende D01 blokkeer formele spelimplementering, maar nie 'n veilige lêerinventaris of die opstel van 'n D01-konsep nie.

## Klein inkremente

Kies 'n enkele waarneembare gedrag, byvoorbeeld die reaksie op een invoer in een bekende toestand. Identifiseer bron, waarneming, onsekerheid, vereiste en aanvaardingsgrens. Beoordeel die ontwerp en toets voor kodebou. Voer TDD uit, vergelyk met die oorspronklike, beoordeel daarna die verandering en werk die herstelrekord by.

Prioritiseer volgens getrouheidswaarde, beskikbare bewyse, bronvoldoendeheid, tegniese risiko, afhanklikhede, toetsbaarheid, gebruikerswaarde en leerwaarde. 'n Indrukwekkende titelskerm kry nie vanself voorkeur bo 'n onopgeloste invoer- of botsingsmodel nie.

## Onsekerheid en omvang

Hou 'n onbekenderegister met onderwerp, geraakte vereiste, ontbrekende bewys, ondersoekvoorstel, eienaar en herbeoordelingspunt. 'n Geen-resultaat-eksperiment moet die hipotese en waargenome beperking behou. Onderskei 'n mislukte meting van 'n negatiewe resultaat.

Vir onoplosbare gedrag: stel verdere ondersoek, 'n benoemde benadering of uitsluiting voor. Teken die eienaar se besluit, getrouheidsimpak en regressietoetse aan. Verlaag nooit toleransies om 'n reeds bekende fout stilweg te aanvaar nie.

## Hervatting

Lees die laaste status, goedkeurings, hashes en oop werk. Verifieer dat bronne en instrumente nog dieselfde is. Heropen geraakte bewyse wanneer iets verander het; moenie die vorige GO blindelings oordra nie. Die hervattingskaart moet die volgende toegelate handeling bevat, nie bloot 'n lys ambisies nie.
