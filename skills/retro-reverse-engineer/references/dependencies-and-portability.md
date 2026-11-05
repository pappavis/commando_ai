# Afhanklikhede, generiese paaie en verenigbaarheidsbeoordeling

## Projekbesluit en toepassing

Vir Commando geld [DEC-20261105-01–03](../review/owner-decisions.md): eksterne pakkette toegelaat, ontbrekende afhanklikhede outomaties opstel, ongepende pakketvereistes, afsonderlike oudiolêer toegelaat en alle installasiepaaie aanpasbaar. Vir ander projekte: lees eers die geldige projekbesluit; moenie hierdie eienaar se toestemming as universele installasiemagtiging behandel nie.

Hierdie verwysing is die kontrak vir die toekomstige projekopstelroete. Die skill se meesterprompt-generator installeer self geen pakkette nie. ’n Requirements-lêer alleen doen ook geen aflaai of installasie nie; die opstelprogram moet die installeerder werklik aanroep.

## Vereistes sonder vaste weergawes

Gebruik pakketname sonder presiese weergawes in die gebruikersgerigte requirements-lêer. Moenie `==1.1`, versteekte constraints, ’n verpligte ou lockfile of ’n stilweg geforseerde afgradering gebruik om hierdie besluit te omseil nie. Kies slegs biblioteke wat die funksie nodig het; die skill skryf geen universele grafika- of oudiobiblioteek voor nie.

Hou produksie- en toetsafhanklikhede herkenbaar. Die [toetsvereiste-sjabloon](../templates/requirements-dev.txt) bevat slegs pytest; dit is nie ’n volledige Commando-produksie-afhanklikheidslys nie. Meet en bewaar die werklik gebruikte weergawes in toets-/vrystellingsbewyse vir naspeurbaarheid; so ’n verslag is nie ’n installasiepennetjie nie.

Gebruik openbare ondersteunde API’s en vermy onnodige weergawekontroles en private biblioteekfunksies. Ongepende direkte pakkette beteken nie dat transitive pakkette geen eie verenigbaarheidsgrense het nie. Wanneer die jongste installeerbare stel breek, ondersoek en herstel die kode of verklaar die konkrete blokkering. Enige noodsaaklike uitsondering op die ongepende beleid word uitdruklik voorgestel, nooit versteek nie.

## Vereiste outomatiese opstelroete

Wanneer projekimplementering gemagtig is, lewer ’n eenvoudige opstel-/beginroete wat:

1. Die projekwortel en gekose Python-tolk bepaal; geen persoonlike pad of vaste Python-mikroweergawe aanneem nie.
2. ’n Reeds gekose projekomgewing respekteer of ’n plaaslike `.venv` skep wanneer geen omgewing gekies is nie. Gebruik die werklike bedryfstelsel se omgewingsuitleg.
3. Die verklaarde vereistes in daardie omgewing laat kontroleer en ontbrekende pakkette outomaties deur pip laat aflaai en installeer. Gebruik die gekose tolk se `-m pip`; moenie per ongeluk die globale pip gebruik nie. Moenie alle pakkette elke keer opgradeer bloot omdat die program begin nie.
4. Installasiemislukking, geen netwerk, ’n onondersteunde tolk of ontoeganklike pakket eerlik rapporteer en afhanklike uitvoering stop; geen oneindige herprobeer of skynsukses nie.
5. Die relevante toetse met dieselfde tolk laat loop en die werklike afsluitkode behou. Dokumenteer ook hoe die gebruiker ná opstel `pytest -v` binne die gekose omgewing uitvoer.

Gebruik argumentlyste vir prosesaanroepe en padobjekte vir lêerwerk; geen saamgeplakte dopopdrag met onbeheerde padteks nie. Geen installasie tydens toetsversameling of gewone module-invoer nie: opstel gebeur vóór toetsing, sodat toetse nie netwerktoegang of verborge omgewingsveranderinge benodig nie.

## Generiese paaie

Lei die projekwortel af van die opstelprogram se ligging, of neem ’n uitdruklike projekpad. Moenie op die huidige werkgids staatmaak sonder om dit te kontroleer nie. Hulpbronne gebruik projek-/pakketrelatiewe paaie; gebruikerdata gebruik ’n gekose skryfbare ligging; tydelike toetse gebruik unieke tydelike gidse.

Toets installasie in ’n ander gids, met spasies en Unicode, en uitvoering vanuit ’n ander werkgids. ’n Gebruiker hoef nie Michiel se volume, tuisgids of omgewingsnaam te hê nie. Historiese absolute paaie mag in broninventarisse bly, duidelik as historiese bewyse gemerk; hulle is nooit uitvoeringsvereistes nie.

Aktivering is slegs ’n gerief: ’n opstelprogram kan die virtuele omgewing se tolk direk gebruik. Gee afsonderlike toepaslike instruksies vir die gebruiker se dop/bedryfstelsel. Oudio- en GUI-adapters word per ondersteunde teiken getoets; padnormalisering alleen maak hulle nie draagbaar nie.

## Kodebeoordeling en toetspoort

Gebruik ’n beskikbare kodebeoordelingskill; registreer die werklike skill en beoordelaar. Kontroleer konkrete gedrag:

- Vars omgewing: verklaarde ongepende afhanklikhede installeer, ontbrekende pakkette word voorsien, tweede opstel beskadig niks nie.
- Bestaande omgewing: gekose tolk en pakkette word korrek gebruik; geen ongevraagde globale wysigings nie.
- Toetsversameling: al die verwagte toetse word versamel. Geen “geen toetse gevind”, kunsmatige skip/xfail, verwyderde assertions of ingeslukte foutkodes as sukses nie.
- Uitvoering: `pytest -v` slaag werklik vir die verklaarde omgewing; bewaar Python-, pakket- en OS-weergawes plus resultate.
- Verenigbaarheid: toets die huidige oplosbare ongepende stel in ’n vars omgewing en die ondersteunde omgewingsmatriks wanneer die projek dit kan uitvoer. Benoem ongetoetste teikens.
- Herstel: los die oorsaak van mislukkings op; herhaal die relevante toetse. Moenie oorspronklike spelgedrag of bewysvereistes verswak ter wille van groen toetse nie.

Kodebeoordeling verminder risiko; dit waarborg nie toekomstige derdepartyvrystellings nie. Die vrystellingshek aanvaar slegs werklike resultate en duidelik afgebakende ondersteunde omgewings.

## Primêre dokumentasie

Die pip-gebruikersgids beskryf requirements-installasie en die keuse van tolk: [pip User Guide](https://pip.pypa.io/en/stable/user_guide/). Die pytest-handleiding beskryf toetsaanroep: [pytest invocation](https://docs.pytest.org/en/stable/how-to/usage.html). Geraadpleeg 5 November 2026; bevestig die toepaslike gedrag weer wanneer die projek sy opstelkode implementeer.
