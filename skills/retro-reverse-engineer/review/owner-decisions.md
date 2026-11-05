# Eienaarsbesluite — 5 November 2026

Bron: die Projekteienaar se direkte opvolg in hierdie gesprek, ná die 0.1.0-hersiening. Hierdie is uitdruklike besluite, nie ’n aanname uit dokumentdatums nie.

## DEC-20261105-01 — Eksterne afhanklikhede

Status: GOEDGEKEUR. Eksterne Python-biblioteke word vir Commando toegelaat. Die projek se opstelroete moet ontbrekende verklaarde pakkette outomaties aflaai en installeer in die gekose projekomgewing. Die verspreide vereistes gebruik pakketname sonder vaste weergawepennetjies. Gebruik slegs werklik nodige pakkette; pytest is ’n toetsafhanklikheid.

Die doel is dat `pytest -v` op die ondersteunde, behoorlik opgestelde omgewing slaag. Kodebeoordeling en werklike toetse moet dit kontroleer. Geen waarborg dat alle toekomstige biblioteekweergawes, Python-weergawes of bedryfstelsels sal werk, word uit dié doel afgelei nie. Moenie toetse verswak, ignoreer of stilweg oorslaan om ’n groen resultaat af te dwing nie.

CON-02: BESLUIT GENEEM; oorspronklike dokumente nog nie aangepas nie. Die huidige besluit vervang die historiese verbod vir hierdie projek. Implementering van ’n spelinstalleerder is nie in hierdie skill-wysiging uitgevoer nie.

## DEC-20261105-02 — Afsonderlike oudiolêer

Status: GOEDGEKEUR BINNE OMVANG. Die huidige afsonderlike oudiolêer is toegelaat. Die gebruiker kan later verdere uitsonderings toevoeg. Dit is geen onbeperkte voorafgoedkeuring vir enige toekomstige verdeling van produksiekode nie. Behou die eenvoudige struktuur en registreer verdere uitsonderings met omvang en rede.

CON-03: BESLUIT GENEEM vir die oudiolêer; die historiese dokumentteks bly onveranderd. Hierdie besluit keur geen oudio-outentisiteits- of F5-aanspraak goed nie.

## DEC-20261105-03 — Generiese paaie

Status: GOEDGEKEUR. Persoonlike absolute paaie in BOOTSTRAP, insluitend die voorbeeld vir aktivering van ’n plaaslike virtuele omgewing, is voorbeelde. Hulle is nie vereiste installasieliggings nie. Enige gebruiker moet die projek in sy eie gids en ondersteunde omgewing kan aflaai, opstel en toets.

Bepaal die projekwortel uit ’n uitdruklike opsie of die werklike lêerligging; laat ’n gekose omgewing toe en gebruik anders ’n projekplaaslike virtuele omgewing. Hanteer spasies, Unicode en verskillende bedryfstelsels. Geen persoonlike gebruikersnaam, volume of vaste tolkweergawe mag nodig wees nie.

CON-08: PADBELEID BESLUIT; werklike Windows/Linux/macOS-ondersteuning, oudio-adapters en toegangsvermoëns moet steeds getoets word. ’n Generiese pad maak `afplay` nie platformonafhanklik nie.

## Wat oop bly

Oorspronklike spelbewyse, F1–F5-metings, D01 se algemene goedkeuringsstatus en ander konflikitems is nie deur hierdie antwoorde opgelos nie. Bestaande projekdocs en speletjiekode bly buite die wysigingsomvang van hierdie skill-opdrag.
