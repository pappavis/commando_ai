# Differensiële toetsprotokol

## Doel en orakel

Vergelyk die oorspronklike program en die rekonstruksie onder benoemde vergelykbare omstandighede. 'n Eenheidstoets kan bewys dat kode sy eie kontrak volg; hierdie protokol ondersoek of die kontrak en implementering met die oorspronklike ooreenstem.

Registreer die orakel in [test-oracle-register.md](../templates/test-oracle-register.md): bron-ID en hash, oorspronklike program/uitgawe, vasleggingsmetode, instrumentweergawe, rou data, meetonsekerheid en beperkinge. 'n Golden file wat uit die nuwe implementering kom, is nie 'n onafhanklike oorspronklike orakel nie.

## Voorbereiding

1. Kies 'n FR-ID en toepaslike F-dimensies. Bevestig dat die toleransies vooraf goedgekeur is.
2. Leg emulator/hardeware, firmware indien relevant, streek, media, instellings en resetmetode vas. Leg die rekonstruksieweergawe, teikenomgewing en konfigurasie vas.
3. Stel ooreenstemmende beginvoorwaardes vas: modus, vlak, posisies, punte, lewens, timers, RNG en verborge toestand indien kenbaar. 'n Visueel identiese skerm alleen bewys nie gelyke interne toestand nie.
4. Definieer tydnul en die omskakeling tussen oorspronklike en nuwe koördinate, rame of simulasietikke. Bewaar die oorspronklike data.
5. Maak 'n invoerspoor met tyd/raam, handeling, duur en gelyktydige insette. Registreer herhalings en presiese monsterpunte.

## Uitvoering en vergelyking

Voer albei roetes met dieselfde benoemde stimulus uit. Leg tussentoestand én uitkomste vas. Vergelyk gebeurtenisvolgorde, posisies, botsings, lewens, punte, vlakke, animasie en oudio soos die vereiste bepaal. Benoem die eerste uiteenlopende monster; 'n eindtelling alleen kan vroeë foute verberg.

Bereken verskille in die oorspronklike eenhede waar moontlik. Hou normalisering en maskering in die verslag. Geen aanpassing mag stilweg drywing, ontbrekende vyande of verkeerde oudio verberg nie.

## Resultaat en diagnose

Gebruik [differensiële verslag](../templates/differential-report.md). `PASS` vereis werklike uitvoering, geldige orakel, geldige beginvoorwaardes en 'n geldige grens. `FAIL` beteken die uitgevoerde vergelyking oorskry die kontrak. `BLOCKED` benoem 'n ontbrekende voorwaarde; `NOT TESTED` beteken geen uitvoering nie.

By mislukking: skep DEV-ID, koppel FR-ID, beoordeel erns, ondersoek bronweergawe, toestand, sinchronisasie, normalisering en kode. Stel een toetsbare hipotese op. Herhaal ná regstelling; behou die mislukte rekord en koppel die hertoets.

## Nie-determinisme

Ondersoek of verskille uit reset, RNG, invoertyd of onbekende geheue kom. Gebruik beheerde herhalings waar moontlik. Waar identiese spore nie verantwoordbaar is nie, definieer statistiese of gedragskriteria vóór beoordeling, met steekproefmotivering en onsekerheid. Moenie 'n willekeurige verdraagsaamheidsgrens of een gunstige proef kies nie.

## Beperkte toegang

Wanneer oorspronklike uitvoering ontbreek, kan 'n bewaarde opname slegs die sigbare/as-hoorbare omvang ondersteun. Roetines en verborge toestand bly beperk. 'n Differensiële toetsplan is nuttig, maar bly NOT TESTED totdat albei relevante resultate bestaan.
