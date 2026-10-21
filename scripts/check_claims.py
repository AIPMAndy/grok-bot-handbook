#!/usr/bin/env python3
"""Audit critical assertions: official provenance, local traceability, and review staleness.

This check validates a curated ledger; it cannot verify truth in real-time or user accounts.
"""
import json, sys
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
R=Path(__file__).resolve().parents[1]
F=R/'data/claims.json'
DOMAINS={'docs.x.ai','cursor.com','x.ai','help.x.com'}
REQUIRED={'subscription','billing','legacy-access','isolation','approval','authentication','routines','team-bots','data-deletion','automation-safety'}

def validate(today=None):
 today=today or date.today()
 obj=json.loads(F.read_text(encoding='utf-8'))
 claims=obj['claims']; errors=[]; ids=set(); topics=set()
 for item in claims:
  ref=item.get('id','?')
  if ref in ids: errors.append(f'{ref}: duplicate ID')
  ids.add(ref); topics.add(item['topic'])
  url=urlparse(item['official_url'])
  if url.scheme!='https' or url.hostname not in DOMAINS or url.username or url.password:
   errors.append(f'{ref}: non-official or unsafe source')
  try:
   stamp=date.fromisoformat(item['last_verified'])
   age=(today-stamp).days
   if age<0:errors.append(f'{ref}: review timestamp in the future')
   if age>item['max_age_days']:errors.append(f'{ref}: STALE ({age} days; maximum {item["max_age_days"]})')
  except (ValueError,TypeError,KeyError): errors.append(f'{ref}: invalid review date')
  if item.get('evidence_level')!='L1_official_documentation' or item.get('product_account_tested') is not False:
   errors.append(f'{ref}: ungrounded evidence level / account test claim')
  if not item.get('local_documents'):errors.append(f'{ref}: no local document')
  for name in item.get('local_documents',[]):
   path=R/name
   if not path.is_file() or name.startswith('/') or '..' in Path(name).parts:errors.append(f'{ref}: invalid local document: {name}')
 if not REQUIRED.issubset(topics):errors.append('Critical claims missing: '+str(sorted(REQUIRED-topics)))
 return errors, len(claims)

if __name__=='__main__':
 issues,n=validate()
 print(f'Claim ledger: {n} assertions audited, {len(issues)} issue(s).')
 for issue in issues:print('ERROR:',issue,file=sys.stderr)
 sys.exit(bool(issues))
