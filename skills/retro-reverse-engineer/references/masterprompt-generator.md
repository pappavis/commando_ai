# Meesterprompt-generator

## Wat dit doen

`scripts/generate_masterprompt.py` is ’n Python-standaardbiblioteekhulpmiddel. Dit skep ’n nuwe MASTERPROMPT, D00, D01 en D02, ’n broninventaris, konflikregister, ondersteunende verwysings en ’n hashmanifest in ’n nuwe gids. Alle dokumente bly hersieningskandidate. Dit voer geen spelkode uit en verander geen bestaande docs nie.

Die generator kombineer drie lae: vaste metodologiekern, platformprofiel en spel-/projekprofiel. Die invoer bevat ook behoue projekreëls, bestaande dokumentweergawes, oop konflikte en projekspesifieke vereistes.

## Invoerprosedure

1. Lees die bestaande docs volledig en maak die semantiese vergelyking volgens document-compatibility.md.
2. Vul die profiele en `project_rules` met die bestaande geldige reëls. Moenie ’n ontbrekende eienaarbesluit as APPROVED invul nie.
3. Registreer elke bekende konflik. ’n Leë konfliklys beteken slegs dat die invoer geen konflikte bevat nie; dit beteken nie dat daar geen konflikte bestaan nie.
4. Vul `requirements` met bewysgekoppelde vereistes of uitdruklike UNKNOWN-ondersoekvrae.
5. Voer die generator uit met die voorbeeldkonfigurasie as formaatgids. Die ouergids van die uitset moet bestaan; die uitsetgids self mag nie bestaan nie.
6. Lees die gegenereerde D00/D01/D02. Vergelyk elke bestaande normatiewe reël met die kandidaat. Kontroleer skakels, profiele, bronhashes en konflikdekking. Bied die betekenisvolle verskille aan voordat vervanging voorgestel word.

## Opdragte

Vanuit die skill-gids, met ’n beskikbare Python 3-tolk:

```sh
python3 scripts/generate_masterprompt.py --config examples/commando-config.json --output /tmp/commando-konsep-nuut
python3 -m unittest discover -s tests -p 'test_*.py'
```

`/tmp/commando-konsep-nuut` is ’n voorbeeldpad; kies ’n nuwe pad op die werklike bedryfstelsel. Vir Windows kan die tolk `py -3` wees indien dit daar beskikbaar is. Geen tolk of pakket word outomaties geïnstalleer nie.

## JSON-kontrak

Verpligte teksvelde: `project`, `version`, `release_chat_id`, `game_profile`, `platform_profile`, `requirements`.

`project_rules`: nie-leë lys teksreëls. `documents`: lys met `path`, `label`, `version`, `status`; paaie is relatief tot die konfigurasielêer of absoluut. Die generator lees en hash die werklike lêers. `conflicts`: lys met `id`, `description`, `status`, `affected_work`. Bekende OPEN-items bly in alle kandidaatdokumente sigbaar.

’n Ontbrekende dokument, profiel of ongeldige konflikrekord lewer ’n fout vóór uitset geskryf word. ’n Bestaande gids of simboliese skakel word geweier. Ingevoegde teks word nie as kode uitgevoer of weer as sjabloon verwerk nie.

## Eerlike beperking

Die hulpmiddel doen deterministiese samestelling en invoerkontrole; dit verstaan nie outomaties alle teenstrydighede in natuurlike taal nie. Dit lees bronbytes vir leesbaarheid en hashes, maar die AI/beoordelaar moet die inhoudelike vergelyking en volledigheid uitvoer. Dit kan daarom nie self “geen konflikte”, “alle oorspronklike reëls behou” of “meesterprompt goedgekeur” sertifiseer nie.

Ondersteunende voorbeelde in die uitset is verwysingsmateriaal, nie die nuwe projek se bewyse nie. Die skill se Commando-historiese register mag nie as ’n ander speletjie se huidige konflikregister gebruik word nie.
