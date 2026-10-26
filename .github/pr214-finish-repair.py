"""One-shot PR214 repair; removed with the temporary workflows before handoff."""
from __future__ import annotations
import copy, hashlib, json, subprocess
from pathlib import Path
from scripts.publication_projection import project_documents, is_policy_scan_field, is_absolute_destination
from scripts.content_safety_policy import scan_host_policy, scan_action_text
from scripts.check_chapter05_contract import relations as relations05
from scripts.check_chapter06_contract import relations as relations06
ROOT=Path.cwd()
BASE='aaabfd1f7af3fb04f9b345802f9c10f97758fff1'
OUT=ROOT/'.tmp/pr214-restoration'
changes=[]
def base(p): return subprocess.check_output(['git','show',f'{BASE}:{p}'])
def sha(raw): return hashlib.sha256(raw).hexdigest()
def compact(obj): return sha(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def load(p): return json.loads((ROOT/p).read_text())
def save(p,d): (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def fix(p,old,new):
 text=(ROOT/p).read_text()
 if text.count(old)!=1: raise ValueError(f'ambiguous replacement: {p}: {old[:80]}')
 (ROOT/p).write_text(text.replace(old,new))
def field_id(f): return [f.field_type,f.element_kind,f.attribute,f.metadata_value('level'),f.text,f.location]

# Preserve historical source-review statements byte-for-byte; the dated addendum
# describes only the new migration and does not alter earlier verification dates.
NOTES={
 '06':'references/ch06-source-review-2026-09-12.md',
 '16':'references/ch16-source-review-2026-09-21.md',
 '18':'references/ch18-source-review-2026-09-22.md',
 '21':'references/ch21-source-review-2026-09-25.md',
 '26':'references/ch26-source-review-2026-09-28.md',
}
addition='''
## 2026-10-26: ATT&CK移行の追記

上記は記載日の確認履歴であり、当時の版・取得条件・採用範囲を保持する。現行本文のATT&CK参照は、[第5章の新しい確認記録](ch05-source-review-2026-10-26.md)に従って20.0へ移行した。固定commitとbundle digest、八Objectと一関係の差分は新しい確認記録を正とする。本章は行動と観測の語彙を参照し、対応付けをCoverage、統制の有効性、主体帰属の証明へ転用しない。

NIST、IETF、OASIS、FIRST等の既存資料を今回再監査したという記録ではない。合成Caseの状態、観測、権限、未配達、判断期限を変更しない。
'''
for ch,p in NOTES.items():
 original=base(p)
 (ROOT/p).write_bytes(original+addition.encode())
 assert (ROOT/p).read_bytes().startswith(original)
# The Part I review explicitly binds a past baseline; never overwrite its v19.2 claim.
p='PART_I_REVIEW.md'
(ROOT/p).write_bytes(base(p)+'''
## 2026-10-26: 後続のATT&CK移行

本記録のbaselineと当時の版は保持する。後続の現行参照への移行は[第5章Source Review](references/ch05-source-review-2026-10-26.md)を参照する。本記録を最新mainへの再承認として読み替えない。
'''.encode())
# Keep the historical source snapshot addressable, in addition to the v20 input.
p='tests/fixtures/attack/ch05-v19.2.json'
(ROOT/p).write_bytes(base(p))
# Keep old Registry notes verbatim, then clearly separate the v20 scope.
registry=load('references/sources.json')
old_registry=json.loads(base('references/sources.json'))
old_sources={s['id']:s for s in old_registry['sources']}
for s in registry['sources']:
 if s['id'] in {'SRC-ATTACK-001','SRC-ATTACK-T1671-001'}:
  s['notes']='Historical record before 2026-10-26 (retained verbatim): '+old_sources[s['id']]['notes']+' Current migration, checked 2026-10-26: '+s['notes']
save('references/sources.json',registry)
subprocess.run(['python3','scripts/render_reference_baseline.py'],check=True)
# Regression data follows the new current identity but retains all historical
# mismatches as negative cases; URL and date must agree, no weakening/skips.
p='scripts/chapter05_regressions.py'
fix(p,'for date, valid in (("2026-08-05", True), ("2026-08-06", False), (None, False)):','for date, valid in (("2026-10-13", True), ("2026-08-05", False), ("2026-08-06", False), (None, False)):')
old='''    for date, valid in (
        (None, True),
        ("2026-08-05", False),
        ("2026-08-06", False),
        ("2026-04-28", False),
    ):
        record = {
            "url": "https://attack.mitre.org/resources/versions/",
            "publishedAt": date,
        }
        check(
            (not framework_publication_date_errors(record)) is valid,
            f"CH05-SRC-PUB-002 live page versus release/update {date}",
        )'''
new='''    release_url = "https://github.com/mitre/cti/releases/tag/ATT%26CK-v20.0"
    history_url = "https://attack.mitre.org/resources/versions/"
    for url, date, valid in (
        (release_url, "2026-10-13", True),
        (release_url, None, False),
        (release_url, "2026-08-05", False),
        (history_url, None, False),
        (history_url, "2026-10-13", False),
        (history_url, "2026-08-05", False),
        (history_url, "2026-08-06", False),
        (history_url, "2026-04-28", False),
    ):
        record = {"url": url, "publishedAt": date}
        check(
            (not framework_publication_date_errors(record)) is valid,
            f"CH05-SRC-PUB-002 fixed release versus live page {url} {date}",
        )'''
fix(p,old,new)
# Only the deliberately migrated source edition changed in Chapter21's data.
current=load('cases/fixtures/ch21-control-validation.json')
previous=json.loads(base('cases/fixtures/ch21-control-validation.json'))
expected=copy.deepcopy(previous); expected['threat']['attackVersion']='20.0'
assert current==expected, 'Unexpected Chapter21 authored-data change'
p='tests/fixtures/chapter21/publication-contract.json'; c=load(p)
assert c['authoredInputs']['threat']==compact(previous['threat'])
c['authoredInputs']['threat']=compact(current['threat']); save(p,c)
# Correct the inherited narrative date without changing any parent's deadline.
p='cases/ch05-attack-behavior-example.md'
fix(p,'本章の2026-09-20は教材Mapの再評価日であり、親Decisionの期限を更新するものではない。','本章の2026-10-26はATT&CK参照版を移行した教材Mapの再評価日であり、親Decisionの期限を更新するものではない。')
fix(p,'Review dateは2026-09-20、','Review dateは2026-10-26、')

# Reproject only the modified publication surfaces through the pinned shared
# renderer. Unchanged documents retain their existing contract entries.
paths=[*NOTES.values(),'cases/ch05-attack-behavior-example.md']
projection=project_documents({p:(ROOT/p).read_text() for p in paths})
assert not projection.diagnostics, str(projection.diagnostics)
projected={d.document_id:d for d in projection.documents}
def host_provenance(d):
 return [field_id(f) for f in d.fields if (is_policy_scan_field(f) or (f.field_type=='destination' and is_absolute_destination(f.normalized_text))) and scan_host_policy(f.normalized_text,location=f.location)]
# Chapter06: use the unchanged historical contract for the unchanged historical
# prefix, and explicitly bind only the new dated addendum fields and destinations.
p='tests/fixtures/chapter06/publication-contract.json'; c=load(p)
old_c=json.loads(base(p)); note=NOTES['06']; spec=copy.deepcopy(old_c['documents'][note]); d=projected[note]
spec['headings']=[[f.metadata_value('level'),f.text] for f in d.fields if f.field_type=='reader_visible_text' and f.element_kind=='heading' and type(f.metadata_value('level')) is int and f.metadata_value('level')<=2]
old_lines=len(base(note).decode().splitlines())
for f,relation in relations06(d):
 if f.line<=old_lines: continue
 if f.field_type=='reader_visible_text' and f.element_kind in {'heading','p'}: spec['required'].append(relation)
 # Text is the explicitly reviewed, non-operative addendum above. Exceptions
 # remain exact-field-bound and cardinality-checked; no host wildcards.
 for kind,findings in (
  ('action',scan_action_text(f.normalized_text,location=f.location) if is_policy_scan_field(f) else []),
  ('host',scan_host_policy(f.normalized_text,location=f.location) if is_policy_scan_field(f) else []),
  ('destination',scan_host_policy(f.normalized_text,location=f.location) if f.field_type=='destination' and is_absolute_destination(f.normalized_text) else []),
 ):
  if findings: spec['exceptions'][kind].append({'relation':relation,'reason':'Reviewed dated source-migration addendum; exact field, no operation or exercise target.'})
c['documents'][note]=spec; save(p,c)
# Chapter05 case: table data unchanged except reviewed migration metadata.
p='tests/fixtures/chapter05/publication-contract.json'; c=load(p); d=projected['cases/ch05-attack-behavior-example.md']
relations=[r for _,r in relations05(d)]
spec=c['documents'][d.document_id]
for req in spec['required']:
 req['field'][3]=req['field'][3].replace('Review dateは2026-09-20、','Review dateは2026-10-26、')
for entries in spec['exceptions'].values():
 for entry in entries:
  entry['relation']['field'][3]=entry['relation']['field'][3].replace('Review dateは2026-09-20、','Review dateは2026-10-26、')
for req in c['documents'][d.document_id]['required']:
 assert relations.count(req)==1, 'Chapter05 required case relation drift'
save(p,c)
# Other note surfaces are complete projected-field snapshots.
for ch in ('16','18','21','26'):
 p=f'tests/fixtures/chapter{ch}/publication-contract.json'; c=load(p); note=NOTES[ch]; d=projected[note]; f=[field_id(x) for x in d.fields]; spec=c['documents'][note]
 if ch in ('16','18'): spec['fields']=f
 else:
  spec['fieldCount']=len(f); spec['projectionSha256']=compact(f)
  spec['headings']=[[x.metadata_value('level'),x.text] for x in d.fields if x.field_type=='reader_visible_text' and x.element_kind=='heading' and type(x.metadata_value('level')) is int]
 spec['hostProvenance']=host_provenance(d)
 save(p,c)
# Only the five reviewed ATT&CK source identities may change; retain key order.
sources={s['id']:s for s in registry['sources']}
for ch in ('06','16','18','21','26'):
 p=f'tests/fixtures/chapter{ch}/publication-contract.json'; c=load(p)
 for sid,identity in c.get('sourceIdentity',{}).items():
  if sid.startswith('SRC-ATTACK-'):
   c['sourceIdentity'][sid]={k:sources[sid][k] for k in identity}
 save(p,c)

# Explicit parent-byte bindings affected by the migration. Rebinding source bytes
# never changes state/evidence/authority assertions or removes negative probes.
PARENTS={
 '06':['manuscript/05-attack-behavior.md','cases/fixtures/ch05-attack-behavior.json'],
 '07':['cases/ch05-attack-behavior-example.md','cases/fixtures/ch05-attack-behavior.json'],
 '08':['cases/ch05-attack-behavior-example.md','cases/fixtures/ch05-attack-behavior.json'],
 '09':['cases/ch05-attack-behavior-example.md','cases/fixtures/ch05-attack-behavior.json'],
 '12':['manuscript/06-observable-systems.md'],
 '13':['manuscript/06-observable-systems.md'],
 '14':['manuscript/06-observable-systems.md'],
 '15':['manuscript/06-observable-systems.md'],
 '16':['manuscript/05-attack-behavior.md','cases/ch05-attack-behavior-example.md','cases/fixtures/ch05-attack-behavior.json','manuscript/06-observable-systems.md'],
 '18':['manuscript/16-telemetry-evidence-readiness.md'],
 '19':['manuscript/16-telemetry-evidence-readiness.md','manuscript/18-threat-hunting.md'],
 '20':['manuscript/16-telemetry-evidence-readiness.md'],
 '21':['manuscript/16-telemetry-evidence-readiness.md'],
 '22':['manuscript/16-telemetry-evidence-readiness.md','manuscript/18-threat-hunting.md','manuscript/21-purple-team-validation.md','cases/fixtures/ch21-control-validation.json'],
 '23':['manuscript/16-telemetry-evidence-readiness.md'],
}
for ch,parents in PARENTS.items():
 p=f'tests/fixtures/chapter{ch}/publication-contract.json'; c=load(p)
 for parent in parents:
  assert parent in c['parentDigests'], (ch,parent)
  old=c['parentDigests'][parent]; new=sha((ROOT/parent).read_bytes())
  assert old in {sha(base(parent)),new,sha(subprocess.check_output(['git','show',f'85e0936094a80c2f31eac71c15de56204cfe93b4:{parent}']))}, (ch,parent)
  c['parentDigests'][parent]=new
  if old!=new: changes.append({'contract':p,'parent':parent,'old':old,'new':new})
 save(p,c)
# Chapter29's two method-reference rows need byte bindings, not new observation
# evidence. Preserve all documentary observations, dates, native states and flags.
p='tests/fixtures/chapter29/parent-contract.json'; bindings=load(p)
data_path='cases/fixtures/ch29-capstone-portfolio.json'; data=load(data_path)
old_data=copy.deepcopy(data)
replacements={}
for parent in ('cases/ch05-attack-behavior-example.md','cases/fixtures/ch05-attack-behavior.json','cases/ch21-control-validation-example.md','cases/fixtures/ch21-control-validation.json'):
 old=bindings['parents'][parent]; assert old==sha(base(parent)); new=sha((ROOT/parent).read_bytes()); bindings['parents'][parent]=new; replacements[old]=new
for rows in (bindings['artifacts'],data['artifacts']):
 for row in rows:
  if row['artifactId'] in ('ART-15','ART-27'):
   assert row['use']=='method-reference' and row['evidenceTransfer'] is False and row['authorityTransfer'] is False
   row['versionSha256']=bindings['parents'][row['canonicalPath']]
assert data['documentaryEvidence']==old_data['documentaryEvidence']
for old,new in zip(old_data['artifacts'],data['artifacts']):
 assert {k:v for k,v in old.items() if k!='versionSha256'}=={k:v for k,v in new.items() if k!='versionSha256'}
save(p,bindings); save(data_path,data)
case_path='cases/ch29-capstone-portfolio-example.md'; text=(ROOT/case_path).read_text()
for old,new in replacements.items():
 if old in text:
  assert text.count(old)==1, 'Duplicate capstone hash occurrence'
  text=text.replace(old,new)
(ROOT/case_path).write_text(text)
p='tests/fixtures/chapter29/publication-contract.json'; c=load(p)
for input_path in (data_path,'tests/fixtures/chapter29/parent-contract.json'):
 c['inputDigests'][input_path]=sha((ROOT/input_path).read_bytes())
d=project_documents({case_path:text}).documents[0]; assert not d.diagnostics
fields=[field_id(f) for f in d.fields]; spec=c['documents'][case_path]
spec['fieldCount']=len(fields); spec['sha256']=sha(json.dumps(fields,ensure_ascii=False,separators=(',',':')).encode()); spec['hostProvenance']=host_provenance(d)
save(p,c)
(OUT/'parent-rebinding.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
# Preserve historical versions at their canonical paths, not merely in git history.
for p in ('manuscript/25-structured-analysis-attribution.md','references/ch05-source-review-2026-09-06.md','tests/fixtures/attack/ch05-v19.2.json'):
 assert (ROOT/p).read_bytes()==base(p), p
for p in (*NOTES.values(),'PART_I_REVIEW.md'):
 assert (ROOT/p).read_bytes().startswith(base(p)), p
for observation in data['documentaryEvidence']:
 assert sha((ROOT/observation['path']).read_bytes())==observation['sourceSha256']
(OUT/'repairs.patch').write_bytes(subprocess.check_output(['git','diff','--binary']))
print('History preservation, scoped bindings and regression migration prepared; runtime checks still required')
