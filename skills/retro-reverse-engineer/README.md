# retro-reverse-engineer

Volledige Afrikaanse hersieningspakket vir bewysgedrewe retrospeletjie-rekonstruksie.
Weergawe **0.1.1** · Vrystelling-ChatID **RRE-20261105-02**.

## Begin hier

Lees [SKILL.md](SKILL.md) vir die werksreëls en roetes. Lees [die konflikregister](review/document-conflicts.md) vóór toekomstige Commando-spelwerk. Die skill is in die projek se `skills/retro-reverse-engineer/` geplaas; outomatiese ontdekking deur elke AI-program word nie hiermee gewaarborg nie. Wys die agent na SKILL.md of gebruik `$retro-reverse-engineer` indien jou omgewing die skill reeds ontdek.

## Inventaris

- `references/`: metodologie, bronforensika, profiele, bewyse, funksionele spesifikasie, F1–F5, argitektuur/TDD, differensiële toetsing, beginnerbegeleiding, dokumentverenigbaarheid, generator, fasehekke en aanbiedings.
- `profiles/`: Commando-spelprofiel en C64-, ZX Spectrum-, Amiga- en algemene platformstarters.
- `templates/`: invulbare registers, matrikse, proef-/toets-/vrystellingsrekords en D00/D01/D02/meesterprompt-sjablone.
- `examples/`: Commando-gevallestudie en werklike generator-invoerformaat.
- `scripts/`: veilige meesterprompt-generator met Python se standaardbiblioteek.
- `tests/`: outomatiese generator-gedragstoetse en verdere skill-QA-scenario’s.
- `review/`: broninventaris, 12 naspeurbare konflik-/versoenbaarheidsbevindinge met huidige besluitstatus en toetsverslag.
- [RELEASE.md](RELEASE.md): weergawe, ChatID en vrystellingsgrense.

## Gebruik

Voorbeeldopdrag: “Lees hierdie SKILL.md en die bestaande projekdocs. Identifiseer bronvoldoendeheid en oop konflikte. Stel die volgende toegelate ondersoekstap voor.”

Vir nuwe D00/D01/D02-konsepte, volg [die generatorhandleiding](references/masterprompt-generator.md). Die voorbeeldkonfigurasie verwag hierdie skill se normale ligging onder `skills/retro-reverse-engineer/`; by 'n ander ligging moet die dokumentpaaie aangepas word. Die generator weier bestaande uitsetgidse en gee geen goedkeuring nie.

## Besluite en oorblywende hersiening

Die [besluite van 5 November 2026](review/owner-decisions.md) keur eksterne ongepende pakkette, outomatiese opstel van ontbrekende afhanklikhede, die afsonderlike oudiolêer en generiese paaie goed. Lees [die uitvoeringskontrak](references/dependencies-and-portability.md). Dit is skill-instruksies; ’n spelinstalleerder is nie met hierdie wysiging gebou nie.

Oop: oorspronklike spelbewyse, die formele D01-goedkeuringsrekord en praktiese toetsing oor ondersteunde omgewings. Die gebruiker kan later verdere argitektuur-uitsonderings toevoeg.

Bestaande projekdocs en speletjiekode bly onveranderd. Die ou v0.1.0-ZIP bly ’n historiese pakket; gebruik v0.1.1 vir die huidige besluite.
