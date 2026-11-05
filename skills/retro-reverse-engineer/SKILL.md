---
name: retro-reverse-engineer
description: Ondersoek en rekonstrueer retrospeletjies met bronforensika, bewysnaspeurbaarheid, getrouheidstoetse en beginnerbegeleiding; lees of genereer projekspesifieke D00-, D01- en D02-meesterprompts sonder stille dokumentvervanging.
---

# Retro-reverse-engineer

Weergawe: **0.1.0** · Vrystelling-ChatID: **RRE-20261105-01** · Status: **HERSIENINGSKANDIDAAT**

## Opdrag en omvang

Help die Projekteienaar om aantoonbare gedrag van 'n oorspronklike retrospeletjie as nuwe, toetsbare spelkode te rekonstrueer. Die metode werk oor speletjies, oorspronklike platforms, moderne bedryfstelsels en goedgekeurde teikentale. Kommunikeer en dokumenteer in Afrikaans; behou tegniese identifiseerders en statuskodes waar nodig.

Onderskei drie vrae: Wat ervaar die speler? Wat doen die oorspronklike program aantoonbaar? Wat moet die nuwe implementering daarom doen? Algemene spelkennis, 'n werkende prototipe en 'n groen eenheidstoets is nie bewys van oorspronklike algoritmes nie.

Aktiveer vir bronondersoek, rekonstruksie, getrouheidsbeoordeling, hervatting of meesterprompt-generering. Gebruik die opsionele aanbiedingsroete slegs wanneer 'n projekaanbieding verlang word. Hierdie skill is nie self 'n emulator, ROM-versameling of voltooide spel nie.

## Begin met die werklike projek

1. Bepaal die huidige opdrag, projekpad en toegelate veranderings. Lees toepaslike projekinstruksies. Gebruik reeds bekende antwoorde; moenie 'n hervatting as 'n nuwe beginneronderhoud behandel nie.
2. Lees bestaande D00, D01, D02 en BOOTSTRAP volledig, indien beskikbaar. Registreer titel, weergawe, status, kontrolesom, einde van dokument en goedkeuringsbewys. 'n Hersieningskandidaat is nie outomaties goedgekeur nie.
3. Lees [dokumentverenigbaarheid](references/document-compatibility.md). Teken elke relevante botsing aan voordat afhanklike werk voortgaan. Geen lêer wen bloot omdat dit nuwer is of homself primêr noem nie.
4. Vul die [spelprofiel](templates/game-profile.md) en [platformprofiel](templates/platform-profile.md) in. Hou oorspronklike platform, moderne teiken en werklike uitvoeringsomgewing apart.
5. Kontroleer lêertoegang, uitvoer- en toetsvermoëns. Raadpleeg relevante beskikbare skills en `ai_dev_vaardigheden01(1).md` of `ai_dev_vaardigheden01.md` indien aanwesig; registreer wat werklik gelees en toegepas is. 'n Ontbrekende opsionele skill is nie dieselfde as 'n ontbrekende kritieke vermoë nie.
6. Identifiseer die laaste goedgekeurde fase, oop risiko's en een volgende toegelate werkpakket. Lees [metodologie](references/methodology.md) en [fasehekke](references/quality-gates.md).

## Ononderhandelbare bewysreëls

- Bewaar oorspronklike bronne onveranderd; werk op naspeurbare afgeleides.
- Identifiseer uitgawe, bronkontrolesom en waarnemingsomgewing voordat bevindings saamgevoeg word. 'n Kontrolesom bewys identiteit van grepe, nie egtheid of volledigheid nie.
- Klassifiseer aansprake as `VERIFIED`, `OBSERVED`, `INFERRED` of `UNKNOWN`. Bewysstatus, toetsresultaat en eienaarsgoedkeuring is drie afsonderlike velde.
- Registreer negatiewe eksperimente, alternatiewe verklarings, ontbrekende materiaal en teenstrydige bewyse. Moenie onsekerheid wegredigeer nie.
- Onderskei `ORIGINAL` (oorspronklik), `ADAPTATION` (tegniese aanpassing) en `ENHANCEMENT` (verbetering). Onbekende gedrag benodig verdere ondersoek, 'n goedgekeurde benadering of uitdruklike uitsluiting.
- Die finale kernspelgedrag is nuwe logika; 'n algemene emulator wat die oorspronklike spel uitvoer, vervang nie die rekonstruksie nie. Emulators is ondersoekinstrumente. Gespesialiseerde oudio-emulasie is 'n moontlike ondersteunende metode onder die projek se afhanklikheidsbeleid.
- Dokumenteer die ketting Bron → Bewys → Vereiste → Oorspronklike roetine → Implementering → Toets → Beoordeling. 'n Onbekende roetine bly `UNKNOWN`.
- Toetsresultate en onafhanklike beoordelings moet werklik bestaan. 'n Interne beoordeling mag nie as 'n onafhanklike agent of beginnerproef beskryf word nie.

## Kies die toepaslike werkroete

| Werk | Lees en gebruik |
|---|---|
| Onbekende lêer, laaier, saamgeperste kode, nuwe bronweergawe | [Bronforensika](references/source-forensics.md), [bronregister](templates/source-register.md), [bronvoldoendeheid](templates/source-sufficiency.md) |
| Nuwe rekenaar of konsole | [Platformondersoek](references/platform-profiles.md), [profiele](profiles/README.md) |
| Bevindinge, roetines, toestande en vereistes | [Bewyse en naspeurbaarheid](references/evidence-and-traceability.md), [D02-metode](references/functional-specification.md) |
| Getrouheidsdoel en aanvaarding | [F1–F5](references/fidelity-contract.md), [getrouheidskontrak](templates/fidelity-contract.md) |
| Kodebou of verandering | [Argitektuur en TDD](references/architecture-and-tdd.md), [differensiële toetsing](references/differential-testing.md) |
| Beginner, vasval, stop of hervat | [D00-begeleiding](references/beginner-coaching.md), [hervattingskaart](templates/resume-card.md) |
| D00/D01/D02 opstel of hersien | [Meesterprompt-generator](references/masterprompt-generator.md), [sjablone](templates/README.md) |
| Vrystelling en beoordeling | [Fasehekke](references/quality-gates.md), [vrystellingsbewyse](templates/release-evidence.md), [QA](tests/SCENARIOS.md) |
| Voorbeeld of projekaanbieding | [Commando-geval](examples/commando-case-study.md), [aanbiedingsmetode](references/showcase.md) |

## Implementeringskontrak

Elke nuwe spelgedrag volg **RED → GREEN → REFACTOR**, met werklike uitvoering en regressietoetse. Die oorspronklike toetsorakel moet onafhanklik van die nuwe implementering wees. Vergelyk oorspronklike en nuwe gedrag met aangetekende beginvoorwaardes, invoer, meetonsekerheid en vooraf goedgekeurde toleransies.

Python is die bestaande RETRORECON-projekkeuse, nie 'n universele beperking op alle nuwe projekte nie. In 'n bestaande Python-projek bly objekgeoriënteerde ontwerp, aanvanklik een produksiebronlêer, geen globale veranderbare speltoestand, toetse apart, en weergawe plus release ChatID in bronkoppe en die gebruikerskoppelvlak behoue, totdat 'n uitdruklike besluit dit verander. Verandering van taal of lêerstruktuur is 'n geregistreerde projekbesluit.

## Besluite en verslagdoening

Gebruik `GO`, `CONDITIONAL GO`, `BLOCKED` en `STOP` vir 'n benoemde werkpakket, nie as 'n ongekwalifiseerde projekstempel nie. 'n Formele fasehek vereis artefakweergawe, bewyse, voorwaardes en die eienaar se besluit. Bestaande toestemming binne dieselfde omvang bly geldig; vra nie herhaaldelik vir reeds gemagtigde werk nie. Stilte is geen goedkeuring nie.

Rapporteer fase, bevestigde bevindings, onbekendes, konflik-ID's, uitgevoerde en nie-uitgevoerde toetse, afwykings en volgende stap. Hou beginnergesprekke kort; hou die tegniese projekrekord volledig. Die skep van 'n skill of dokumentkonsep beteken nie dat die speletjie, metodologie of volgende ontwikkelingsfase goedgekeur is nie.

## Hierdie pakket

Die pakket se [bron- en konflikverslag](review/document-conflicts.md) beskryf die plaaslike Commando-dokumente soos op 5 November 2026 gelees. Dit is 'n historiese momentopname; kontroleer hashes en huidige besluite voor hergebruik. [Vrystellingsinligting](RELEASE.md) onderskei hierdie skill se vrystelling-ID van 'n gesprek se tegniese ID.
