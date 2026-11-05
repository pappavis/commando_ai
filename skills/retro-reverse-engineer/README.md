# retro-reverse-engineer

Volledige Afrikaanse hersieningspakket vir bewysgedrewe retrospeletjie-rekonstruksie.
Weergawe **0.1.0** · Vrystelling-ChatID **RRE-20261105-01**.

## Begin hier

Lees [SKILL.md](SKILL.md) vir die werksreëls en roetes. Lees [die konflikregister](review/document-conflicts.md) vóór toekomstige Commando-spelwerk. Die skill is in die projek se `skills/retro-reverse-engineer/` geplaas; outomatiese ontdekking deur elke AI-program word nie hiermee gewaarborg nie. Wys die agent na SKILL.md of gebruik `$retro-reverse-engineer` indien jou omgewing die skill reeds ontdek.

## Inventaris

- `references/`: metodologie, bronforensika, profiele, bewyse, funksionele spesifikasie, F1–F5, argitektuur/TDD, differensiële toetsing, beginnerbegeleiding, dokumentverenigbaarheid, generator, fasehekke en aanbiedings.
- `profiles/`: Commando-spelprofiel en C64-, ZX Spectrum-, Amiga- en algemene platformstarters.
- `templates/`: invulbare registers, matrikse, proef-/toets-/vrystellingsrekords en D00/D01/D02/meesterprompt-sjablone.
- `examples/`: Commando-gevallestudie en werklike generator-invoerformaat.
- `scripts/`: veilige meesterprompt-generator met Python se standaardbiblioteek.
- `tests/`: outomatiese generator-gedragstoetse en verdere skill-QA-scenario’s.
- `review/`: broninventaris, 12 oop konflik-/versoenbaarheidsbevindinge en toetsverslag.
- [RELEASE.md](RELEASE.md): weergawe, ChatID en vrystellingsgrense.

## Gebruik

Voorbeeldopdrag: “Lees hierdie SKILL.md en die bestaande projekdocs. Identifiseer bronvoldoendeheid en oop konflikte. Stel die volgende toegelate ondersoekstap voor.”

Vir nuwe D00/D01/D02-konsepte, volg [die generatorhandleiding](references/masterprompt-generator.md). Die voorbeeldkonfigurasie verwag hierdie skill se normale ligging onder `skills/retro-reverse-engineer/`; by 'n ander ligging moet die dokumentpaaie aangepas word. Die generator weier bestaande uitsetgidse en gee geen goedkeuring nie.

## Hersieningsvrae

1. Watter afhanklikheidsbeleid moet vir Commando geld: ondersteunende biblioteke toegelaat, of slegs die standaardbiblioteek?
2. Bestaan daar reeds 'n goedgekeurde uitsondering op die enkellêerreël en 'n formele D01 v1.2-goedkeuringsrekord?
3. Watter BOOTSTRAP-spelreëls is reeds met oorspronklike bewyse bevestig, en watter is doelbewuste verbeterings?
4. Moet die volgende praktiese proef Commando-bronverifikasie, ’n onbekende platform of beginnerbegeleiding toets?

Hierdie vrae blokkeer nie die voltooide hersieningspakket nie. Hulle bepaal latere projekbesluite. Geen bestaande docs of spelkode is vir die skep van hierdie pakket gewysig nie.
