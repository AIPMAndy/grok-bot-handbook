"""Deterministic quality gates: public guide is not a substitute for product account E2E."""
import json, unittest, re
from pathlib import Path
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/catalog.json').read_text(encoding='utf-8'))
E=json.loads((R/'data/extras.json').read_text(encoding='utf-8'))
OFFICIAL=('https://docs.x.ai/grok-bot/','https://cursor.com/help/grok-bot/','https://x.ai/')

class DOM(HTMLParser):
 def __init__(self):
  super().__init__(); self.ids=[];self.refs=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if tag in ('script','link','img'):
   url=d.get('src') or d.get('href')
   if url and not (url.startswith('https:') or url.startswith('#') or url.startswith('data:')):self.refs.append(url)

class ContentTest(unittest.TestCase):
 def test_core_counts(self):
  self.assertEqual([len(D[x]) for x in ('chapters','playbooks','faq','roadmap','sources')],[26,40,36,7,19])
  self.assertEqual([len(E[x]) for x in ('diagnostics','preflight')],[10,7])
 def test_uniq_ids(self):
  for key in ('chapters','playbooks','diagnostics','preflight'):
   rows=D[key] if key in D else E[key]
   ids=[x['id'] for x in rows]
   self.assertEqual(len(ids),len(set(ids)),key)
 def test_chapter_fields(self):
  for i,c in enumerate(D['chapters'],1):
   self.assertEqual(c['num'],i)
   for k in ('id','title','category','why','summary','steps','check','pitfall','source','evidence'):self.assertTrue(c.get(k),f'{c["id"]} {k}')
   self.assertGreaterEqual(len(c['steps']),3)
   self.assertTrue(c['source'].startswith(OFFICIAL))
   self.assertTrue('未宣称作者实测' in c['evidence'])
 def test_prompts_inputs_safety_validation(self):
  for p in D['playbooks']:
   for k in ('id','title','category','requires','prompt','verify','risk','evidence'):self.assertTrue(p.get(k),f'{p["id"]} {k}')
   self.assertGreater(len(p['prompt']),45)
   self.assertIn('未声明实测',p['evidence'])
 def test_faq_sources_real_official(self):
  self.assertTrue(all(f['source'].startswith(OFFICIAL) for f in D['faq']))
 def test_official_source_list(self):
  urls=[s['url'] for s in D['sources']]
  self.assertEqual(len(urls),len(set(urls)))
  self.assertTrue(all(x.startswith(OFFICIAL) for x in urls))
  self.assertIn('https://cursor.com/help/grok-bot/plans',urls)
  self.assertIn('https://docs.x.ai/grok-bot/team-bots',urls)
  self.assertIn('https://docs.x.ai/grok-bot/tag-on-x',urls)
 def test_js_matches_source_json(self):
  for name,var,expected in [('catalog','GROK_GUIDE',D),('extras','GROK_EXTRA',E)]:
   txt=(R/f'data/{name}.js').read_text(encoding='utf-8').strip()
   self.assertTrue(txt.startswith(f'window.{var} = '))
   self.assertEqual(json.loads(txt[len(f'window.{var} = '):-1]),expected)
 def test_html_resources_and_dom_integrity(self):
  h=(R/'index.html').read_text(encoding='utf-8')
  dom=DOM();dom.feed(h)
  self.assertEqual(len(dom.ids),len(set(dom.ids)),'duplicate HTML IDs')
  for src in dom.refs:self.assertTrue((R/src).is_file(),src)
  script=(R/'app.js').read_text(encoding='utf-8')
  requested=set(re.findall(r"\$\('#([^']+)'\)",script))
  self.assertFalse(requested-set(dom.ids),f'Missing DOM ids: {requested-set(dom.ids)}')
  for n in ('data/catalog.js','data/extras.js','style.css','app.js'):self.assertIn(n,h)
 def test_content_facing_counts_match(self):
  readme=(R/'README.md').read_text(encoding='utf-8')
  h=(R/'index.html').read_text(encoding='utf-8')
  for num in ('26','40','36'):self.assertIn(num,readme);self.assertIn(num,h)
  doc=(R/'docs/COMPLETE-GUIDE.md').read_text(encoding='utf-8')
  prompt=(R/'docs/PROMPT-LIBRARY.md').read_text(encoding='utf-8')
  self.assertEqual(len(re.findall(r'^## \d+\. ',doc,re.M)),26)
  self.assertEqual(len(re.findall(r'^## \d+\. ',prompt,re.M)),40)
 def test_billing_correction_propagated(self):
  text='\n'.join([(R/p).read_text(encoding='utf-8') for p in ('README.md','docs/BILLING-AND-ACCESS.md','index.html')])
  self.assertIn('The X Subscription',text)
  self.assertIn('Premium',text)
  self.assertIn('Plus',text)
  self.assertIn('共享',text)
 def test_safe_commercial_links(self):
  h=(R/'index.html').read_text(encoding='utf-8')
  self.assertIn('AIPMAndy',h);self.assertIn('https://metaver.vip/',h);self.assertIn('https://metaver.vip/services',h)
  self.assertIn('免费',h)
 def test_no_sensitive_private_keys(self):
  for p in R.rglob('*'):
   if not p.is_file() or p.suffix.lower() in ('.png','.jpg','.jpeg','.zip','.pyc','.svg') or '__pycache__' in p.parts:continue
   data=p.read_text(encoding='utf-8-sig')
   # Detect long accidental key-shaped strings; human examples with small placeholders are fine.
   self.assertNotRegex(data,r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
 def test_local_markdown_links_exist(self):
  files=list(R.glob('*.md'))+list((R/'docs').glob('*.md'))+list((R/'guides').glob('*.md'))+list((R/'templates').glob('*.md'))
  for file in files:
   text=file.read_text(encoding='utf-8')
   for dest in re.findall(r'(?<!\!)\[[^\]]+\]\(([^)]+)\)',text):
    if dest.startswith(('https://','http://','#','mailto:')):continue
    path=unquote(dest.split('#')[0]);
    self.assertTrue((file.parent/path).is_file(),f'{file.relative_to(R)} -> {dest}')
 def test_diagnostics_sources_and_preflight(self):
  for x in E['diagnostics']:
   self.assertTrue(x['source'].startswith(OFFICIAL));self.assertGreaterEqual(len(x['steps']),3)
   for k in ('label','intro','severity','action'):self.assertTrue(x.get(k))
  for x in E['preflight']:self.assertTrue(x['label'])
 def test_pages_workflow(self):
  y=(R/'.github/workflows/deploy-pages.yml').read_text(encoding='utf-8')
  for item in ('actions/deploy-pages@v4','pages: write','id-token: write','on:','workflow_dispatch'):self.assertIn(item,y)
 def test_docs_and_governance_exist(self):
  for file in ('docs/ADVERSARIAL-AUDIT.md','docs/CASE-STUDY-PROTOCOL.md','docs/BILLING-AND-ACCESS.md','docs/QA-MANUAL.md','docs/OPERATIONS-PLAYBOOK.md','docs/CAPABILITY-MATRIX.md','docs/QUALITY-STANDARDS.md','docs/APPROVAL-RUNBOOK.md','templates/TEST-RUN-LOG.csv','.github/ISSUE_TEMPLATE/fact_check.yml'):
   self.assertTrue((R/file).is_file(),file)

 def test_claim_ledger_exists_and_is_current(self):
  import sys
  from datetime import date
  sys.path.insert(0,str(R/'scripts'))
  from check_claims import validate
  errors,n=validate(date(2026,10,21))
  self.assertEqual(n,12)
  self.assertFalse(errors,errors)
 def test_claim_ledger_expires_high_risk_assertions(self):
  import sys
  from datetime import date
  sys.path.insert(0,str(R/'scripts'))
  from check_claims import validate
  errors,n=validate(date(2026,11,30))
  self.assertTrue(any('STALE' in x for x in errors))
 def test_pages_publish_blocked_by_failed_tests(self):
  wf=(R/'.github/workflows/deploy-pages.yml').read_text(encoding='utf-8')
  self.assertRegex(wf,r'(?m)^  deploy:\n    needs: verify')
  for x in ('git diff --exit-code','scripts/check_claims.py','unittest discover','node --check app.js'):self.assertIn(x,wf)
 def test_first_step_selector_accessible_and_all_paths(self):
  h=(R/'index.html').read_text(encoding='utf-8')
  js=(R/'app.js').read_text(encoding='utf-8')
  for elt in ('id="first-step"','id="planPath"','id="planResult"','id="planStatus"','id="planSource"','role="status"'):
   self.assertIn(elt,h)
  for key in ('new-paid','new-free','legacy-cursor','legacy-link','enterprise','unsure'):
   self.assertIn(f"'{key}':",js)
  self.assertIn('textContent=v[2]',js)
 def test_no_javascript_fallback_and_static_counter(self):
  h=(R/'index.html').read_text(encoding='utf-8')
  self.assertIn('<noscript>',h)
  self.assertIn('docs/COMPLETE-GUIDE.md',h)
  self.assertIn('id="courseProgressText">0 / 26',h)
 def test_social_preview_raster_asset(self):
  h=(R/'index.html').read_text(encoding='utf-8')
  self.assertIn('assets/social-preview.png',h)
  self.assertIn('summary_large_image',h)
  p=R/'assets/social-preview.png'
  self.assertTrue(p.is_file())
  from struct import unpack
  header=p.read_bytes()[:24]
  self.assertTrue(header.startswith(b'\x89PNG\r\n\x1a\n'))
  self.assertEqual(unpack('>II',header[16:24]),(1200,630))
 def test_code_identifier_safe_in_markup(self):
  import re
  for key in ('chapters','playbooks'):
   for item in D[key]:
    self.assertRegex(item['id'],r'^[a-zA-Z0-9_-]+$')
 def test_explicit_testing_limits_in_docs(self):
  t=(R/'docs/V3-ADVERSARIAL-AUDIT.md').read_text(encoding='utf-8')
  self.assertIn('不能证明“全网第一”',t)
  self.assertIn('真实账号',t)
if __name__=='__main__':unittest.main()
