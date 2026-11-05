# Game Profiles en Platform Profiles

## Twee profiele plus 'n teikenomgewing

Die **Game Profile** bepaal watter spel, uitgawe en omvang bedoel word. Die **Platform Profile** bepaal hoe die oorspronklike stelsel ondersoek moet word. Die **teikenomgewing** bepaal waar die nuwe implementering loop. Moenie hierdie drie saamtrek nie: 'n C64-bron kan op Windows ondersoek word en 'n nuwe implementering kan op Linux loop.

Gebruik [spelprofiel](../templates/game-profile.md) en [platformprofiel](../templates/platform-profile.md). Elke tegniese waarde benodig 'n bron of status. 'n Lys moontlike hardewarekenmerke bewys nie dat die betrokke spel dit gebruik nie.

## Oorspronklike platform: minimum ondersoek

Registreer variant, streek, verwerker, bytevolgorde, geheue- en bankmodel, mediaformate, laaiproses, grafiese en oudiostelsels, invoer, tydbronne en resetgedrag. Identifiseer die gesaghebbende handleiding of instrumentdokumentasie vir presiese getalle wanneer hulle nodig is. Registreer publikasieweergawe en relevante afdeling; moenie ongeverifieerde presisie uit algemene modelkennis invul nie.

Kies instrumente op grond van werklike vermoëns: kan hulle die medium lees, die regte variant uitvoer, toestand stoor, invoer herhaal, registers inspekteer en metings uitvoer? Bevestig plaaslike beskikbaarheid voor opdragte of GUI-stappe gegee word.

## Profielstarters

Die pakket bevat ondersoekstarters vir [C64](../profiles/c64.md), [ZX Spectrum](../profiles/zx-spectrum.md), [Amiga](../profiles/amiga.md) en [ander platforms](../profiles/other-platforms.md). Hulle is vraaglyste, nie vooraf geverifieerde konfigurasies of verpligte gereedskapkeuses nie.

Vir Atari, MSX, 'n konsole of 'n onbekende platform: identifiseer eers die presiese model. Moenie 'n handelsmerk as volledige platformidentiteit gebruik nie. Ondersoek moontlike cartridge-mappers, firmware, RAM-uitbreidings en streekvariante slegs wanneer relevant.

## Taal- en argitektuurbeleid

Vir 'n nuwe projek mag die eienaar 'n teikentaal en argitektuur kies. Stel die keuse uitdruklik in die spelprofiel vas. Platformonafhanklikheid beteken nie dat bestaande goedgekeurde taalvereistes verdwyn nie.

Vir die huidige Commando-dokumentbasis is objekgeoriënteerde Python, aanvanklik een produksielêer en geen globale veranderbare speltoestand aangeteken. D00/D01 laat ondersteunende biblioteke toe, maar BOOTSTRAP beperk dit: die afhanklikheidsbeleid bly 'n oop konflik totdat 'n besluit bestaan. Geen outomatiese installasie of taalverandering volg uit hierdie skill nie.

## Moderne teiken en prestasie

Registreer bedryfstelsel, tolk/samesteller, grafika, oudio, invoer, skermskaal, verspreidingsformaat en prestasiebegroting. Meet op die benoemde omgewing: opdateringsduur, raamvariasie, invoervertraging, oudio-onderbrekings, geheuegebruik, laaityd en langdurige stabiliteit.

'n macOS-opdrag soos `afplay` is 'n platformadapter, nie 'n universele oudio-oplossing nie. 'n Alternatief vir 'n ander bedryfstelsel benodig sy eie toets; skryf nie PASS vir ongetoetste omgewings nie. Prestasie-optimalisering mag nie goedgekeurde spelgedrag stilweg verander nie.
