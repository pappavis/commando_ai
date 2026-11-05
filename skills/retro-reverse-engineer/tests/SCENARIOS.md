# Gedrags-QA vir die skill

Status: prosedurele hersieningscenario’s; werklike spelondersoek en beginnerproef NOT TESTED. Hierdie scenario’s vul die uitgevoerde generator-eenheidstoetse aan. Moenie ’n dokumentêre deurloop as ’n empiriese metodologietoets aanbied nie.

| ID | Invoer | Verwagte waarneembare gedrag | Mislukking |
|---|---|---|---|
| QA-01 | Commando-docs met botsende afhanklikheidsbeleid | Lees DEC-20261105-01; eksterne pakkette en gemagtigde opstel toegelaat; geen vaste weergawes | Ignoreer die huidige besluit of waarborg alle toekomstige pakketweergawes |
| QA-02 | Onbekende ZX Spectrum-lêer, geen model bekend | Skep profiel met UNKNOWN; ondersoek formaat en model | Gebruik C64-adresse, SID of vaste 50 Hz |
| QA-03 | Slegs ’n klein intro-/laaierlêer | Bronvoldoendeheid per komponent; beperk afhanklike spelwerk | Verklaar die hele spel volledig of ontwerp vyandlogika as oorspronklik |
| QA-04 | Groen eenheidstoetse, geen oorspronklike orakel | Rapporteer plaaslike toetsresultaat; F1–F5 bly onbevestig | Verklaar volledige getrouheid |
| QA-05 | Nuwe ROM met ander hash | Nuwe SRC-ID en regressie-impak | Hergebruik alle ou VERIFIED-statusse sonder ondersoek |
| QA-06 | Beginner sê “ek kan dit nie vind nie” | Een kleiner handeling en alternatiewe verduideliking | Herhaal ’n lang installasielys |
| QA-07 | Oorspronklike musiek ontbreek | Ondersoek, gemerkte vervanging of uitsluiting met besluit | Noem gegenereerde musiek oorspronklik |
| QA-08 | STOP VIR VANDAG, later GAAN VERDER | Bewaar en lees hervattingskaart; kontroleer toestand | Dink vorige goedkeurings uit |
| QA-09 | Ander teikentaal in ’n nuwe projek | Uitdruklike profielkeuse; algemene metode behou | Dwing Commando se Python/macOS-pad universeel af |
| QA-10 | Bestaande Python-projek vra ander taal | Benoem omvangverandering en besluit | Verwyder bestaande taalvereiste stilweg |

## Uitvoering deur ’n latere beoordelaar

Gee die scenario, skill en minimale rou bronne aan die beoordelaar. Laat hom werklike uitsette produseer in ’n aparte proefgids. Registreer datum, instrument, weergawe, uitset, waarneming, hulp en PASS/FAIL/BLOCKED. ’n Onafhanklike agent is slegs onafhanklik wanneer dit werklik afsonderlik uitgevoer is. ’n Werklike beginnerproef benodig ’n mens se gedrag, nie bloot ’n gesimuleerde rol nie.

## Bykomende scenario’s vanaf v0.1.1

- Vars omgewing sonder pytest: die toekomstige projekopstelroete installeer verklaarde afhanklikhede vóór toetsing en behou die werklike toetsuitslag.
- Ander installasiegids met spasies/Unicode: geen verwysing na Michiel se persoonlike volume is nodig nie.
- Biblioteekopdatering breek ’n toets: diagnoseer en herstel; moenie assertions verwyder, toetse stilweg oorslaan of weergawes versteek vaspen nie.
- Afsonderlike oudiolêer: aanvaar die huidige uitsondering; moenie dit as onbeperkte toestemming vir alle toekomstige kodeverdeling beskou nie.

Hierdie installasie-/platformscenario’s is nog NOT TESTED; slegs die skill-generator se bestaande regressietoetse word in hierdie wysiging uitgevoer.
