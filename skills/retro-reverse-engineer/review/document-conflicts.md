# Dokumentkonflikregister — plaaslike Commando-basis

Datum: 2026-11-05. Beoordeling: INTERNAL REVIEW. Oorspronklike status in v0.1.0: alle items OPEN. Huidige status: CON-02 en CON-03 het eienaarsbesluite; CON-08 se padbeleid is besluit, maar praktiese oordraagbaarheid bly oop. Die ander items bly OPEN; bestaande docs is nie gewysig nie. Erns geld vir toekomstige afhanklike spelwerk, nie vir die gemagtigde skep van hierdie hersieningspakket nie.

## CON-01 — Weergaweverskil

- Bron A: BOOTSTRAP §1 (reël 16).
- Bron B: D01 opskrif en slot.
- Verskil: BOOTSTRAP verwys na v1.1-RC; die plaaslike D01 is v1.2.
- Erns: MEDIUM. Geraakte werk: Tegniese dokumentbasis.
- Voorstel, nog nie besluit nie: Bevestig die bedoelde basis; stel later ’n gemagtigde verwysingsregstelling voor.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-02 — Normatiewe botsing

- Bron A: BOOTSTRAP §1 en §4 (reëls 18, 170).
- Bron B: D00 §3.1; D01 §5.2 en §36.
- Verskil: BOOTSTRAP verbied eksterne pip-afhanklikhede; D00/D01 laat ondersteunende biblioteke toe en D01 verkies pytest.
- Erns: HOOG. Geraakte werk: Afhanklikheidskeuse en installasie.
- Voorstel, nog nie besluit nie: Laat die eienaar die projekbeleid kies; geen installasie volg uit hierdie pakket nie.
- Besluitnemer: Projekteienaar. Besluit-ID: DEC-20261105-01, 2026-11-05. Status: BESLUIT GENEEM — eksterne ongepende pakkette en outomatiese opstel toegelaat; dokumentaanpassing nog uitstaande.
- Huidige besluit en omvang: sien [eienaarsbesluite](owner-decisions.md). Die voorstel hierbo is die historiese v0.1.0-voorstel.

## CON-03 — Argitektuurspanning

- Bron A: BOOTSTRAP Fase 2–3 (reëls 99–120).
- Bron B: D00 §33.2–33.3; D01 §31.
- Verskil: BOOTSTRAP begin met sound_effects.py én commando.py; D00/D01 vereis aanvanklik een produksiebronlêer tensy ’n uitsondering goedgekeur is. Geen sodanige besluit in die geleeste docs geïdentifiseer nie.
- Erns: HOOG. Geraakte werk: Produksielêerstruktuur.
- Voorstel, nog nie besluit nie: Soek die bestaande uitsonderingsbesluit of laat ’n konkrete uitsondering beoordeel.
- Besluitnemer: Projekteienaar. Besluit-ID: DEC-20261105-02, 2026-11-05. Status: BESLUIT GENEEM — huidige afsonderlike oudiolêer toegelaat; verdere uitsonderings apart.
- Huidige besluit en omvang: sien [eienaarsbesluite](owner-decisions.md). Die voorstel hierbo is die historiese v0.1.0-voorstel.

## CON-04 — Bewysgaping / statusverskil

- Bron A: BOOTSTRAP §2.1 en Fase 1.
- Bron B: D00 §47.1; D01 §64.1; D02 §6–9.
- Verskil: BOOTSTRAP noem ’n cracktro en ’n outentieke D64-spelvrag; D02 hou bronvolledigheid en spelkode onbevestig. Dit kan latere kennis wees, maar gekoppelde rou bewyse is nie in hierdie taak geverifieer nie.
- Erns: HOOG. Geraakte werk: Bronvoldoendeheid en oorspronklikheidsaansprake.
- Voorstel, nog nie besluit nie: Verifieer werklike lêers, hashes, onttrekking en laaiketting; dateer slegs ná besluit die geraakte rekords op.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-05 — Bewysgaping / funksionele spanning

- Bron A: BOOTSTRAP Fases 3–6.
- Bron B: D02 §12–44 en §72–74.
- Verskil: BOOTSTRAP skryf konkrete spelwaardes, vlakke, bonusse en nuwe funksies voor terwyl D02 dieselfde domeine UNKNOWN hou.
- Erns: HOOG. Geraakte werk: Spelimplementering en F2/F3.
- Voorstel, nog nie besluit nie: Klassifiseer elke reël met bewys of as goedgekeurde aanpassing/verbetering; geen numeriese waarde word hier opgelos nie.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-06 — Tydsberekeningspanning

- Bron A: BOOTSTRAP §1 en Fase 3 (50 Hz/20 ms).
- Bron B: D00 §25; D01 §24; D02 §41–46.
- Verskil: BOOTSTRAP stel ’n vaste tydstap; ander docs vereis bronmeting of ’n goedgekeurde ontwerpbesluit en hou tyd onbekend.
- Erns: HOOG. Geraakte werk: Spelklok en F4.
- Voorstel, nog nie besluit nie: Bevestig streek, tydbron, meting en enige goedgekeurde benadering; moenie 50 Hz as universele feit gebruik nie.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-07 — Oudio-bewysgaping

- Bron A: BOOTSTRAP §2.3 en Fase 2.
- Bron B: D01 §23 en §82; D02 §38–40.
- Verskil: BOOTSTRAP beskryf sintese en presiese musiekkenmerke stellig; oorspronklike bron-/oudiovergelyking is nie in hierdie taak uitgevoer nie.
- Erns: HOOG. Geraakte werk: F5 en oudio-outentisiteit.
- Voorstel, nog nie besluit nie: Koppel brondata en metings; merk moontlike vervanging as sodanig totdat getrouheid bewys is.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-08 — Omvang- en omgewingsverskil

- Bron A: BOOTSTRAP §2.2–2.3 en §4.
- Bron B: D00 §12 en §55; D01 §59 en §81; huidige platformonafhanklike opdrag.
- Verskil: BOOTSTRAP vereis ’n spesifieke Mac-tolkpad, afplay en ’n historiese BypassSandbox-vlag. Hierdie vereistes is nie universeel of as huidige vermoë bevestig nie.
- Erns: MEDIUM. Geraakte werk: Uitvoeringsroete en oordraagbaarheid.
- Voorstel, nog nie besluit nie: Behou dit as historiese Commando-konfigurasie; toets die werklike omgewing en gebruik huidige toegangsmeganismes.
- Besluitnemer: Projekteienaar. Besluit-ID: DEC-20261105-03, 2026-11-05. Status: GEDEELTELIK BESLUIT — absolute paaie is voorbeelde; platformuitvoering en oudio-adapters nog ongetoets.
- Huidige besluit en omvang: sien [eienaarsbesluite](owner-decisions.md). Die voorstel hierbo is die historiese v0.1.0-voorstel.

## CON-09 — Goedkeuringsstatus bots

- Bron A: D02 kop: Voorafgaande dokument D01 v1.2 — Goedgekeur.
- Bron B: D01 kop en slot: REVIEW CANDIDATE.
- Verskil: D02 beweer goedkeuring; D01 se eie status is ’n kandidaat. Die beslissende eienaarsrekord is nie in die geleeste dokumente geïdentifiseer nie.
- Erns: HOOG. Geraakte werk: Formele tegniese fase-oorgang.
- Voorstel, nog nie besluit nie: Verkry of identifiseer die besluitrekord; moenie een status stilweg kies nie.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-10 — Eksterne weergawe-onsekerheid

- Bron A: Vorige gesprek se ontwerpbeoordeling van 5 November 2026.
- Bron B: Plaaslike D02 opskrif v0.1.
- Verskil: Die gesprek verwys na ’n D02 v0.3 wat elders uitgewerk sou wees; daardie volledige artefak is nie in die beskikbare gesprekblad of projekdocs gevind nie.
- Erns: MEDIUM. Geraakte werk: Latere D02-vergelyking.
- Voorstel, nog nie besluit nie: Hou die plaaslike v0.1 as geleeste bron; verkry v0.3 slegs wanneer dit nodig is; moenie die inhoud rekonstrueer uit die verwysing nie.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-11 — Interne D00-spanning

- Bron A: D00 §44.1 en §72.
- Bron B: D00 §7.1 en §10.1; huidige opdrag.
- Verskil: Die vaste openingsvraag vra na die bedryfstelsel, terwyl D00 ook sê bekende antwoorde moet nie herhaal word nie. Die huidige gebruiker het reeds Mac, projekpad en taak verskaf.
- Erns: LAAG. Geraakte werk: Aktivering en beginnergesprek.
- Voorstel, nog nie besluit nie: In hierdie taak geld die huidige opdrag; vir toekomstige D00-hersiening stel ’n bekende-konteks-uitsondering voor.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## CON-12 — Omvanggeneralisering

- Bron A: D00 §33; D01 §30–34 en §89.
- Bron B: Huidige platformonafhanklike skill-opdrag.
- Verskil: Die bestaande metodologie se implementeringstaal is Python. Die nuwe skill laat ander tale vir nuwe projekte toe, maar dit mag nie die huidige Commando-kontrak stilweg vervang nie.
- Erns: MEDIUM. Geraakte werk: Profielkeuse en meesterprompt-generering.
- Voorstel, nog nie besluit nie: Behou Python in Commando se profiel; laat ander nuwe projekte hul eie taal kies; bestaande projekte benodig ’n besluit vir verandering.
- Besluitnemer: Projekteienaar. Besluit-ID: PENDING. Status: OPEN.

## Interpretasiegrense

Hierdie is ’n dokumentbeoordeling. Geen aanspraak dat die spelkode verkeerd is of dat historiese bevindings vals is, word hiermee gemaak nie. Die ontbrekende bewys-/besluitketting moet nagegaan word voordat getrouheids- of goedkeuringsaansprake oorgedra word. Die gebruiker se huidige opdrag magtig die skill en ZIP; die opvolg van 5 November keur slegs die bogenoemde afgebakende besluite goed. Spelbewyse bly oop.
