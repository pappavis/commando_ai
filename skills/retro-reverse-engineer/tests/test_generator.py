# Retro-reverse-engineer | 0.1.0 | RRE-20261105-01
"""Gedragstoetse vir veilige konsepgenerering; geen spelgetrouheidstoetse nie."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'generate_masterprompt.py'

class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.doc = self.root / 'D01.md'
        self.doc.write_text('Bestaande reël: een produksielêer.\n', encoding='utf-8')
        self.config = {'project':'Proefspel', 'version':'0.1.0', 'release_chat_id':'PROEF-01',
          'game_profile':'Uitgawe UNKNOWN; teikentaal Python.',
          'platform_profile':'Platform UNKNOWN; geen tydstap bevestig nie.',
          'project_rules':['Behou die bestaande enkellêerreël.'],
          'documents':[{'path':'D01.md','label':'D01','version':'1.2','status':'REVIEW CANDIDATE'}],
          'conflicts':[{'id':'CON-01','description':'Afhanklikheidsbeleid bots.','status':'OPEN','affected_work':'Installasie'}],
          'requirements':'FR-001: oorspronklike beweging UNKNOWN.'}
        self.cfg = self.root / 'config.json'
        self.save()
    def save(self):
        self.cfg.write_text(json.dumps(self.config),encoding='utf-8')
    def run_generator(self, output=None):
        self.assertTrue(SCRIPT.is_file(), 'Die generator moet bestaan voordat uitvoer gelewer kan word.')
        spec=importlib.util.spec_from_file_location('generator',SCRIPT)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module.generate(self.cfg, output or self.root/'konsep')
    def test_preserves_sources_and_open_conflicts(self):
        before=self.doc.read_bytes()
        self.run_generator()
        self.assertEqual(before,self.doc.read_bytes())
        self.assertIn('CON-01', (self.root/'konsep'/'D01_tech_Meesterprompt.md').read_text())
        self.assertIn('OPEN',(self.root/'konsep'/'CONFLICTS.md').read_text())
        self.assertIn(hashlib.sha256(before).hexdigest(),(self.root/'konsep'/'SOURCE_INVENTORY.md').read_text())
        self.assertIn('HERSIENINGSKANDIDAAT',(self.root/'konsep'/'D02_Functionele_specificaties.md').read_text())
    def test_existing_output_never_overwritten(self):
        out=self.root/'konsep';out.mkdir();sentinel=out/'behou.txt';sentinel.write_text('behou')
        with self.assertRaises(FileExistsError): self.run_generator(out)
        self.assertEqual(sentinel.read_text(),'behou')
    def test_missing_document_produces_no_output(self):
        self.doc.unlink()
        with self.assertRaises(FileNotFoundError): self.run_generator()
        self.assertFalse((self.root/'konsep').exists())
    def test_missing_profile_produces_no_output(self):
        del self.config['platform_profile'];self.save()
        with self.assertRaises(ValueError): self.run_generator()
        self.assertFalse((self.root/'konsep').exists())
    def test_no_conflicts_is_not_auto_approval(self):
        self.config['conflicts']=[];self.save();self.run_generator()
        s=(self.root/'konsep'/'CONFLICTS.md').read_text()
        self.assertIn('NIE OUTOMATIES BEVESTIG NIE',s)
    def test_invalid_conflict_rejected(self):
        self.config['conflicts']=[{'id':'CON-01'}];self.save()
        with self.assertRaises(ValueError): self.run_generator()
        self.assertFalse((self.root/'konsep').exists())
    def test_literal_template_like_input_is_preserved(self):
        self.config['project']='Spel {{VERSION}}';self.save();self.run_generator()
        self.assertIn('Spel {{VERSION}}',(self.root/'konsep'/'MASTERPROMPT.md').read_text())
    def test_output_symlink_rejected(self):
        out=self.root/'konsep';out.symlink_to(self.root/'ontbreek')
        with self.assertRaises(FileExistsError):self.run_generator(out)
    def test_compiled_profile_links_resolve(self):
        self.config['game_profile']='Sien [konflikte](../review/document-conflicts.md).';self.save();self.run_generator()
        import re
        out=self.root/'konsep'
        for p in out.glob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if ':' not in link and not link.startswith('#'):
                    self.assertTrue((p.parent/link).exists(),(p.name,link))

    def test_empty_documents_has_explicit_missing_basis(self):
        self.config['documents']=[];self.save();self.run_generator()
        self.assertIn('ONTBREEK',(self.root/'konsep'/'SOURCE_INVENTORY.md').read_text())

if __name__=='__main__': unittest.main()
