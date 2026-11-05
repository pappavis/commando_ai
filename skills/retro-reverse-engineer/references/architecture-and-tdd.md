# Argitektuur en TDD RED → GREEN → REFACTOR

## Voor kodebou

Bevestig vereiste-ID, bronbewyse, F1–F5-kriteria, ontwerp, uitvoeringsroete en geldige toestemming. Beoordeel die vereiste en toetsplan vóór implementering. 'n Onbekende oorspronklike algoritme mag nie 'n produksievereiste word omdat dit maklik is om te implementeer nie.

Hou die kernspeltoestand toetsbaar sonder 'n grafiese venster, regte oudiotoestel of gebruiker se permanente lêers. Laat invoer, klok, RNG en berging waar nodig beheerbaar wees. Vermy 'n argitektuur met meer klasse as verantwoordelikhede; bewyse en die goedgekeurde ontwerp bepaal die struktuur.

## Bestaande RETRORECON-Python-kontrak

Objekgeoriënteerde Python; aanvanklik een produksiebronlêer; toetse en hulpbronne apart; geen globale veranderbare speltoestand. 'n Ander lêerstruktuur benodig rede, ontwerp, toetsimpak, beginnerimpak en geregistreerde goedkeuring. Hierdie beperkings geld nie outomaties vir elke nuwe teikentaal nie, maar mag nie stilweg uit 'n bestaande projek verdwyn nie.

Plaas projeknaam, weergawe en vrystelling-ChatID in bronkoppe, ook in toets- en hulpmiddelkode waar toepaslik. Vertoon weergawe en ChatID in 'n gebruikerskoppelvlak; toets die sigbare waarde waar uitvoerbaar. Verwar die etiket nie met 'n outomaties geverifieerde gesprek-ID nie.

## Afhanklikhede en omgewings

Lees [die opstel- en verenigbaarheidskontrak](../references/dependencies-and-portability.md). Vir Commando is die huidige afsonderlike oudiolêer goedgekeur; verdere uitsonderings kry eie besluite. Kontroleer ongepende afhanklikhede en generiese paaie met werklike toetse en kodebeoordeling.

## RED

Skryf 'n toets uit die vereiste en onafhanklike orakel. Gebruik 'n konkrete beginstaat en invoer. Voer dit uit; bewaar opdrag, omgewing, tyd, kodeweergawe en fout. Bevestig dat die fout die ontbrekende gedrag aantoon. 'n Sintaksisfout, ontbrekende pakket of verkeerde werkpad is nie die verlangde gedrags-RED nie; herstel eers die toetsomgewing.

## GREEN

Implementeer die kleinste verandering wat die vereiste bevredig. Laat die toets en relevante regressies loop. Bewaar werklike resultate en enige geblokkeerde toetse. Moenie die orakel uit die implementering terugbereken nie. 'n Verskil met die oorspronklike word ondersoek, nie opgelos deur die verwagte waarde by die nuwe kode aan te pas nie.

## REFACTOR

Verbeter struktuur, naamgewing of duplisering sonder verandering van goedgekeurde gedrag. Voer relevante toetse ná die verandering uit. Wanneer gedrag wel moet verander, behandel dit as 'n vereisteverandering met nuwe RED en bewys-/besluitkoppeling.

## Isolasie en reproduseerbaarheid

Stel toetsaanvang uitdruklik: titelmodus en aktiewe spel is verskillende toestande. 'n Toets vir beweging moet sy speeltoestand self bepaal. Gebruik unieke tydelike gidse vir hoëtellings en konfigurasie; 'n gedeelde vaste `/tmp`-lêer kan parallelle toetse besmet. Beheer saad en tyd slegs wanneer die oorspronklike se relevante toestand verstaan word.

Toets grenswaardes, gelyktydige insette, botsingsprioriteit, herstel, lewensverlies, tydsverloop en bronweergawe-regressies soos die vereiste dit nodig maak. Moenie blote kodevorm of elke private metode toets sonder waarneembare kontrak nie.

## Ná implementering

Voer 'n differensiële vergelyking uit waar die oorspronklike beskikbaar is. Beoordeel kode, bewysketting, toetse, afwykings en prestasie. Merk die beoordeling as onafhanklik, intern of gesimuleerde perspektief volgens wat werklik gebeur het. Sluit die taak eers met 'n bygewerkte projekrekord en toepaslike hekbesluit.

Historiese kode sonder 'n RED-log kry nie 'n uitgedinkte TDD-geskiedenis nie. Voeg karakteriseringstoetse by, rapporteer die beperking en gebruik TDD vir daaropvolgende gedragveranderinge.
