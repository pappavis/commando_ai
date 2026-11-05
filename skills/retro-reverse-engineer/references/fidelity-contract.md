# F1–F5-getrouheidskontrak

Getrouheid is 'n stel onafhanklike dimensies, nie 'n enkele persentasie nie. 'n Projek kan F2 goed ondersteun terwyl F3 onbekend bly. Gebruik [die kontraksjabloon](../templates/fidelity-contract.md).

| Dimensie | Wat vergelyk word | Moontlike orakel en meting | Belangrike beperking |
|---|---|---|---|
| F1 — Visueel | Palet, posisie, sprites, lae, animasies | Oorspronklike rame; genormaliseerde pixels, kenmerkposisies en raamvolgorde | Skalering en CRT-filters moet apart van die spelbeeld wees |
| F2 — Gedrag | Invoer, botsings, punte, lewens, vyande en oorgange | Invoerherhaling, toestandspore en gebeurtenisvolgorde | Dieselfde eindpunt kan verkeerde tussengedrag verberg |
| F3 — Algoritmies | Besluitreëls, berekenings, RNG, heelgetal- en oorloopgedrag | Roetineontleding en beheerde teenvoorbeelde | Swartboksooreenstemming alleen bewys nie algoritme-identiteit nie |
| F4 — Tyd | Opdatering, invoerreaksie, beweging, animasie en oorgange | Raam-/siklustellings of gekalibreerde tydmeting | CPU-klok, skermverversing en spelopdatering is verskillende groothede |
| F5 — Oudio | Brondata, note/kanale, effekte, menging en snellers | Registerspore, bronidentiteit, tydsbelynde opname en luisterbeoordeling | Klankgelykenis bewys nie oorspronklike komposisie of sintese nie |

## Kontrak vóór beoordeling

Elke item bevat bronweergawe, aanspraak, bewysstatus, meetmetode, eenheid, teiken, meetonsekerheid, toleransie, toets-ID en goedkeuringsbesluit. Gebruik `NOT MEASURED` en `NOT APPROVED` waar nodig. 'n Waarde uit 'n voorbeeld is nooit 'n standaardtoleransie nie.

Bepaal die grens uit oorspronklike metings, instrumentresolusie en eksplisiete tegniese kompromieë. Bevries die grens voor die kandidaat beoordeel word. Enige latere verandering kry 'n besluit-ID, rede en hertoets; dit mag nie 'n fout stilweg wegdefinieer nie.

## Vergelykbare metings

Vir beelde: bewaar rou rame; dokumenteer uitsnyding, skaal, palet en maskers. Maskers mag nie die fout wat ondersoek word verberg nie. Vergelyk animasieverloop en lae, nie net een gunstige skermbeeld nie.

Vir tyd: benoem tydnul, invoergrens, waarnemingspunt en eenheid. Onderskei simulasietyd van gasheerkloktyd. Meet lang genoeg om ophopende drywing te vind; rapporteer maksimum en verspreiding waar dit saak maak.

Vir oudio: teken die bron en sintesemetode, opnameformaat, beginpunt, duur, kanaalinstellings en normalisering aan. Bewaar rou opnames. 'n Nuwe melodie of prosedurele klank bly 'n vervanging totdat sy verhouding met die oorspronklike bewys is.

## Onvolledige of veranderlike getrouheid

Vir nie-determinisme: ondersoek verborge toestand en sade, herhaal metings, motiveer steekproefgrootte en vergelyk toepaslike verspreidings of invariantes. Geen vaste universele aantal herhalings is voldoende vir elke spel nie.

`N/A` is slegs geldig met 'n omvangsrede en besluit; ontbrekende oudio is nie outomaties N/A nie. Registreer afwykings per dimensie. Die vrystellingsverslag noem getoetste, mislukte, geblokkeerde en ongetoetste kriteria afsonderlik. Speelbaarheid, beginnerbruikbaarheid en F1–F5 bly afsonderlike aanvaardingsuitsprake.
