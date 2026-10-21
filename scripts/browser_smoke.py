#!/usr/bin/env python3
"""Optional real-browser QA for THIS SITE, not the Grok Bot product.

Requires playwright and Chromium; not part of dependency-free GitHub CI.
Usage: python3 scripts/browser_smoke.py
"""
from pathlib import Path
import json, subprocess, socket, time
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
# This runtime blocks loopback browser navigation; render exact local asset contents inline.
# This verifies browser interactions but not HTTP responses or reload persistence.
html=(R/'index.html').read_text(encoding='utf-8')
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+(R/'style.css').read_text(encoding='utf-8')+'</style>')
for path in ('data/catalog.js','data/extras.js','app.js'):
    html=html.replace('<script src="'+path+'"></script>','<script>'+(R/path).read_text(encoding='utf-8')+'</script>')
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    for name,w,h in [('mobile-320',320,750),('mobile-375',375,812),('mobile-390',390,844),('mobile-430',430,932),('tablet',768,1024),('desktop',1440,900)]:
        page=browser.new_page(viewport={'width':w,'height':h},accept_downloads=True)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(html,wait_until='load')
        assert page.locator('.lesson-card').count()==26
        assert page.locator('.prompt-card').count()==40
        assert page.locator('.faq-item').count()==36
        assert page.locator('.preflight-check').count()==7
        assert page.locator('#planPath option').count()==6
        # login/plan triage fact matching
        page.locator('#planPath').select_option('new-free')
        assert 'Plus / Free' in page.locator('#planTitle').inner_text()
        assert '不包含' in page.locator('#planStatus').inner_text()
        page.locator('#planPath').select_option('new-paid')
        assert '每周用量池' in page.locator('#planDescription').inner_text()
        page.locator('#planPath').select_option('legacy-cursor')
        assert '旧版' in page.locator('#planDescription').inner_text()
        page.locator('#planPath').select_option('unsure')
        # Search, modal, bookmark, export
        page.locator('#chapterSearch').fill('Routine')
        assert 0<page.locator('.lesson-card').count()<26
        page.locator('#chapterSearch').fill('')
        page.locator('.lesson-card [data-open-chapter]').first.click()
        assert page.locator('#chapterDialog').evaluate('(el)=>el.open')
        page.keyboard.press('Escape')
        assert not page.locator('#chapterDialog').evaluate('(el)=>el.open')
        page.locator('.prompt-card [data-fav]').first.click()
        page.locator('#savedOnly').check()
        assert page.locator('.prompt-card').count()==1
        page.locator('#savedOnly').uncheck()
        page.locator('#symptomSelect').select_option('routine')
        assert page.locator('#diagnoseSteps .diagnostic-step').count()>=3
        for el in page.locator('[data-preflight]').all(): el.check()
        assert page.locator('#preflightCount').inner_text()=='7 / 7'
        page.locator('.lesson-card [data-done]').first.check()
        assert page.locator('#courseProgressText').inner_text()=='1 / 26'
        with page.expect_download() as d:page.locator('#exportProgress').click()
        assert d.value.suggested_filename.endswith('.md')
        docw=page.evaluate('document.documentElement.scrollWidth')
        assert docw<=w+2,(name,'overflow',docw,w)
        assert not errors,(name,errors)
        if name in ('mobile-390','desktop'):
            page.screenshot(path=str(R.parent/f'grok-bot-v3-{name}.png'),full_page=True)
        results.append({'viewport':name,'width':w,'horizontal_overflow':docw>w+2,'javascript_errors':errors,'selector_options':6,'chapters':26,'playbooks':40,'faq':36,'render_mode':'inlined static HTML (no HTTP check)','behaviors':'PASS'})
        page.close()
    browser.close()
(R.parent/'grok-bot-v3-browser-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
