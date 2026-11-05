#!/usr/bin/env python3
# Retro-reverse-engineer | 0.1.1 | RRE-20261105-02
"""Skep hersieningskonsepte in 'n nuwe gids; verander nooit brondokumente nie."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]

def required_text(data, key):
    value=data.get(key)
    if not isinstance(value,str) or not value.strip():
        raise ValueError('Ontbrekende of ongeldige teksveld: '+key)
    return value

def render(template, values):
    # Een vervangingspass: ingevoegde data word nie weer as sjabloon ontleed nie.
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: values[m[1]], template)

def generate(config_path, output):
    config_path=Path(config_path).resolve()
    output=Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise FileExistsError('Die uitsetpad bestaan reeds; kies ’n nuwe gids: '+str(output))
    data=json.loads(config_path.read_text(encoding='utf-8'))
    if not isinstance(data,dict): raise ValueError('Die konfigurasie moet ’n JSON-objek wees.')
    fields=['project','version','release_chat_id','game_profile','platform_profile','requirements']
    for key in fields: required_text(data,key)
    for key in ['documents','conflicts','project_rules']:
        if not isinstance(data.get(key),list):raise ValueError('Lys benodig: '+key)
    if not data['project_rules'] or any(not isinstance(x,str) or not x.strip() for x in data['project_rules']):
        raise ValueError('project_rules benodig minstens een uitdruklike projekreël of onbekendestatus.')
    inventory=[]
    for doc in data['documents']:
        if not isinstance(doc,dict):raise ValueError('Ongeldige dokumentrekord.')
        for key in ['path','label','version','status']:required_text(doc,key)
        source=Path(doc['path'])
        if not source.is_absolute():source=config_path.parent/source
        raw=source.read_bytes()
        raw.decode('utf-8') # Bevestig leesbaarheid; geen uitvoer van dokumentinhoud nie.
        inventory.append(f"- {doc['label']} · weergawe {doc['version']} · status {doc['status']}\n  - Invoerpad: `{doc['path']}`\n  - SHA-256: `{hashlib.sha256(raw).hexdigest()}`; grepe: {len(raw)}.")
    source_text='\n'.join(inventory) or 'DOKUMENTBASIS ONTBREEK — nuwe konsep; geen bestaande reëls of goedkeuring kan afgelei word nie.'
    conflict_lines=[]
    for conflict in data['conflicts']:
        if not isinstance(conflict,dict):raise ValueError('Ongeldige konflikrekord.')
        for key in ['id','description','status','affected_work']:required_text(conflict,key)
        conflict_lines.append(f"- {conflict['id']} [{conflict['status']}]: {conflict['description']} Geraakte werk: {conflict['affected_work']}.")
    conflict_text='\n'.join(conflict_lines) or 'Geen konflikte in die invoer aangeteken nie; volledigheid is NIE OUTOMATIES BEVESTIG NIE.'
    conflict_text+='\n\nSemantiese bronvergelyking en behoud van alle bestaande vereistes moet deur ’n beoordelaar bevestig word. Die generator verleen geen goedkeuring nie.'
    values={'PROJECT':data['project'],'VERSION':data['version'],'CHAT_ID':data['release_chat_id'],
        'GAME':data['game_profile'],'PLATFORM':data['platform_profile'],
        'RULES':'\n'.join('- '+x for x in data['project_rules']),
        'CONFLICTS':conflict_text,'SOURCES':source_text}
    sections={
        'd00':['beginner-coaching.md','document-compatibility.md'],
        'd01':['methodology.md','source-forensics.md','evidence-and-traceability.md','platform-profiles.md','dependencies-and-portability.md','architecture-and-tdd.md','differential-testing.md','quality-gates.md'],
        'd02':['functional-specification.md','fidelity-contract.md']}
    names={'d00':'D00_Bootstrap_masterprompt.md','d01':'D01_tech_Meesterprompt.md','d02':'D02_Functionele_specificaties.md'}
    files={'MASTERPROMPT.md':render((ROOT/'templates/masterprompt.md').read_text(encoding='utf-8'),values),
           'SOURCE_INVENTORY.md':'# Dokumentbasis\n\n'+source_text+'\n',
           'CONFLICTS.md':'# Konflikte\n\n'+conflict_text+'\n'}
    for kind,refs in sections.items():
        local=dict(values)
        local['METHOD']='\n\n'.join((ROOT/'references'/name).read_text(encoding='utf-8') for name in refs)
        local['SPECIFIC']=data['requirements'] if kind=='d02' else 'Huidige fase en geldige goedkeurings: PENDING — bevestig teen die projekrekord.'
        files[names[kind]]=render((ROOT/'templates'/f'{kind}.md').read_text(encoding='utf-8'),local)
    # Valideer alles vóór enige uitset geskryf word. Geen skoonmaak van bestaande gidse nie.
    output.mkdir(parents=False,exist_ok=False)
    try:
        # Verwysings en sjablone bly beskikbaar vir relatiewe skakels in die saamgestelde inhoud.
        for folder in ['references','templates','profiles','examples','review']:
            if (ROOT/folder).is_dir():shutil.copytree(ROOT/folder,output/folder)
        for name,content in files.items():
            # Saamgestelde verwysings was oorspronklik een vlak dieper.
            for folder in ['references','templates','profiles','examples','review']:
                content=content.replace('](../'+folder+'/', ']('+folder+'/')
            (output/name).write_text(content,encoding='utf-8')
        hashes={str(p.relative_to(output)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.rglob('*')) if p.is_file()}
        (output/'MANIFEST.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except Exception:
        shutil.rmtree(output)
        raise
    return output

def main():
    parser=argparse.ArgumentParser(description='Skep D00/D01/D02-hersieningskonsepte sonder oorskryf.')
    parser.add_argument('--config',required=True,help='JSON-konfigurasielêer')
    parser.add_argument('--output',required=True,help='Nuwe uitsetgids; ouergids moet bestaan')
    args=parser.parse_args()
    try:
        result=generate(args.config,args.output)
    except (OSError,ValueError,KeyError) as exc:
        print('Kon nie konsepte skep nie: '+str(exc),file=sys.stderr)
        return 1
    print('Hersieningskonsepte geskep: '+str(result))
    return 0
if __name__=='__main__':sys.exit(main())
