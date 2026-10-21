(()=>{'use strict';
const G=window.GROK_GUIDE;
if(!G||!Array.isArray(G.chapters)||!Array.isArray(G.playbooks))return;
const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
// Public, no-account eligibility triage; copy reflects official docs as checked on 2026-10-21.
const PLAN_PATHS={
 'unsure': ['先核对','没必要急着买会员。','先登录官方账户后台确认套餐名称、Grok Bot 权益、每周用量，再决定是否订阅或关联已有账户。','https://cursor.com/help/grok-bot/plans'],
 'new-paid': ['官方显示包含','优先用同一账户登录。','新版 Premium、Super、Ultra 包含 Grok Bot。使用共享的每周用量池；再查看对应席位的实际可用额度与权限。','https://docs.x.ai/x-subscription/grok-bot'],
 'new-free': ['官方显示不包含','Plus / Free 不包含 Grok Bot。','如果目标是使用 Grok Bot，请先查看官方 Premium 及以上的权益说明，再根据预算决定。不要将普通 X Premium 当作替代品。','https://docs.x.ai/x-subscription/grok-bot'],
 'legacy-cursor': ['检查原账户','按旧版 Cursor 的访问方式登录。','旧版付费 Cursor 个人计划及自助 Teams 有访问路径；具体用量和后台政策需在原账户核实，企业额外需要管理员配置。','https://cursor.com/help/grok-bot/plans'],
 'legacy-link': ['需关联或核查','先检查原有订阅的关联条件。','符合条件的旧版 SuperGrok / X Premium+ 有对应关联流程；不要自行把旧版 X Premium 与 Premium+ 混淆。','https://cursor.com/help/grok-bot/plans'],
 'enterprise': ['组织权限','向管理员确认席位和政策。','企业访问可能由组织管理员开启，且 SSO、隐私和审批限制可能独立于个人套餐。不要借私人账号绕过组织授权。','https://docs.x.ai/grok-bot/teams-and-enterprises']
};
const planSelect=document.querySelector('#planPath');
if(planSelect){
 const updatePlan=()=>{const v=PLAN_PATHS[planSelect.value]||PLAN_PATHS.unsure;
  document.querySelector('#planStatus').textContent=v[0];
  document.querySelector('#planTitle').textContent=v[1];
  document.querySelector('#planDescription').textContent=v[2];
  document.querySelector('#planSource').href=v[3];
 };
 planSelect.addEventListener('change',updatePlan);updatePlan();
}

const K='grok-bot-handbook-v1';
let state={done:[],favorite:[],day:[]};
try{const s=JSON.parse(localStorage.getItem(K)||'{}');for(const k of Object.keys(state))if(Array.isArray(s?.[k]))state[k]=s[k].filter(v=>typeof v==='string');}catch(_){/* Storage may be restricted */}
const save=()=>{try{localStorage.setItem(K,JSON.stringify(state));}catch(_){}};
const has=(k,id)=>state[k].includes(id);
const toggle=(k,id)=>{state[k]=has(k,id)?state[k].filter(v=>v!==id):[...state[k],id];save();};
let chSearch='',chCategory='全部',chUndone=false,pSearch='',pCategory='全部',onlySaved=false,faqQuery='';
const toast=s=>{let t=$('#toast');t.textContent=s;t.hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>t.hidden=true,2200);};
async function copyText(s,msg){if(navigator.clipboard?.writeText){try{await navigator.clipboard.writeText(s);toast(msg);return;}catch(_){}}window.prompt('复制以下内容：',s);}
const chapterCategories=[...new Set(G.chapters.map(c=>c.category))];
$('#chapterFilter').innerHTML='<option value="全部">全部分类</option>'+chapterCategories.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
$('#chapterNav').innerHTML=['全部',...chapterCategories].map(c=>`<button type="button" data-chcat="${esc(c)}" class="${c==='全部'?'current':''}">${esc(c)}</button>`).join('');
function visibleChapters(){return G.chapters.filter(c=>(chCategory==='全部'||c.category===chCategory)&&(!chUndone||!has('done',c.id))&&[c.title,c.summary,c.category,c.why,...c.steps,c.pitfall].join(' ').toLowerCase().includes(chSearch.toLowerCase()));}
function renderChapters(){
const items=visibleChapters();$('#chapterCount').textContent=`显示 ${items.length} / ${G.chapters.length} 章`;
$('#chapterCards').innerHTML=items.length?items.map(c=>`<article class="lesson-card ${has('done',c.id)?'complete':''}"><div class="lesson-card-top"><span>${esc(c.category)}</span><span>CH ${String(c.num).padStart(2,'0')} · ${c.minutes} MIN</span></div><h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p><span class="evidence-line">官方资料编辑整理 · 非作者实测</span><div class="lesson-card-bottom"><button type="button" data-open-chapter="${c.id}">查看操作与验收 →</button><label><input aria-label="标记 ${esc(c.title)} 已学完" data-done="${c.id}" type="checkbox" ${has('done',c.id)?'checked':''}> 已学完</label></div></article>`).join(''):'<p class="result-count">没有匹配的教程，试试其他关键词或分类。</p>';
$('#chapterNav').querySelectorAll('[data-chcat]').forEach(b=>b.classList.toggle('current',b.dataset.chcat===chCategory));
const n=state.done.filter(x=>G.chapters.some(c=>c.id===x)).length;$('#courseProgressText').textContent=`${n} / ${G.chapters.length}`;$('#courseProgressBar').style.width=(n/G.chapters.length*100)+'%';
}
const promptCategories=['全部',...new Set(G.playbooks.map(p=>p.category))];
$('#promptCategories').innerHTML=promptCategories.map(c=>`<button type="button" data-pcat="${esc(c)}" class="${c==='全部'?'active':''}">${esc(c)}</button>`).join('');
function visiblePrompts(){return G.playbooks.filter(p=>(pCategory==='全部'||p.category===pCategory)&&(!onlySaved||has('favorite',p.id))&&[p.title,p.category,p.goal,p.requires,p.prompt,p.verify].join(' ').toLowerCase().includes(pSearch.toLowerCase()));}
function renderPrompts(){const items=visiblePrompts();$('#promptCount').textContent=`显示 ${items.length} / ${G.playbooks.length} 套任务模板`;
$('#promptCards').innerHTML=items.length?items.map(p=>`<article class="prompt-card"><div class="prompt-card-head"><span>${esc(p.category)} · ${p.id.toUpperCase()}</span><button type="button" class="favorite-btn ${has('favorite',p.id)?'active':''}" data-fav="${p.id}" aria-pressed="${has('favorite',p.id)}" title="${has('favorite',p.id)?'取消收藏':'收藏模板'}">${has('favorite',p.id)?'♥':'♡'}</button></div><h3>${esc(p.title)}</h3><p>${esc(p.goal)}</p><span class="evidence-line">模板 / 待实际验证</span><div class="prompt-preview">${esc(p.prompt.slice(0,92))}${p.prompt.length>92?'…':''}</div><div class="prompt-card-foot"><button type="button" data-copy-prompt="${p.id}">复制完整提示词 ↗</button><button class="expand" type="button" data-expand="${p.id}">查看全文 +</button></div><details id="detail-${p.id}"><summary>完整模板与使用提示</summary><pre>${esc(p.prompt)}</pre><dl><dt>需要准备</dt><dd>${esc(p.requires)}</dd><dt>如何验证</dt><dd>${esc(p.verify)}</dd><dt>风险与审批</dt><dd>${esc(p.risk)}</dd></dl></details></article>`).join(''):'<p class="result-count">没有匹配模板，试试清除搜索。</p>';
$('#promptCategories').querySelectorAll('[data-pcat]').forEach(b=>b.classList.toggle('active',b.dataset.pcat===pCategory));}
function renderRoadmap(){$('#roadmapCards').innerHTML=G.roadmap.map((d,i)=>`<article class="day-card ${has('day',String(i+1))?'checked':''}"><div class="day-tag">${esc(d.day)}</div><div><h3>${esc(d.title)}</h3><p>${esc(d.detail)}</p></div><label class="task-check"><input type="checkbox" data-day="${i+1}" ${has('day',String(i+1))?'checked':''}><span>完成</span></label></article>`).join('');}
function renderFaq(){let list=G.faq.filter(f=>[f.q,f.a].join(' ').toLowerCase().includes(faqQuery.toLowerCase()));$('#faqList').innerHTML=list.length?list.map(f=>`<details class="faq-item"><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p><a href="${esc(f.source)}" target="_blank" rel="noopener noreferrer">查看官方说明 ↗</a></details>`).join(''):'<p class="result-count">没有匹配项，可以查看官方 Troubleshooting。</p>';}
$('#sourcesList').innerHTML=G.sources.map(s=>`<a class="source-card" href="${esc(s.url)}" rel="noopener noreferrer" target="_blank"><span>↗</span><strong>${esc(s.title)}</strong><p>${esc(s.note)}</p></a>`).join('');
$('#statChapters').textContent=G.chapters.length;$('#statPrompts').textContent=G.playbooks.length;
function openChapter(id){const c=G.chapters.find(x=>x.id===id);if(!c)return;
$('#modalBody').innerHTML=`<div class="modal-kicker">CH ${String(c.num).padStart(2,'0')} / ${esc(c.category)} / ${c.minutes} 分钟</div><h2 id="modalTitle">${esc(c.title)}</h2><p class="dialog-summary">${esc(c.summary)}</p><div class="dialog-block"><h3>为什么要学这个？</h3><p>${esc(c.why)}</p></div><div class="dialog-block"><h3>照着做 · ${c.steps.length} 步</h3><ol>${c.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div><div class="dialog-block"><h3>怎样算做成了</h3><p>${esc(c.check)}</p></div><div class="dialog-block"><h3>证据等级</h3><p>官方功能说明与编辑整理；尚无作者亲自运行该功能的可复核记录。</p></div><div class="dialog-block"><h3>避坑提醒</h3><p>${esc(c.pitfall)}</p></div><div class="dialog-actions"><button type="button" class="btn btn-primary" data-modal-done="${c.id}">${has('done',c.id)?'✓ 已标记完成':'✓ 标记这一章完成'}</button><a href="${esc(c.source)}" target="_blank" rel="noopener noreferrer">核对官方文档 ↗</a></div><div class="dialog-mini-contact">做自己的 Bot 工作流遇到困难？微信 <strong>AIPMAndy</strong> <button type="button" data-copy-wechat>复制微信号</button> · <a href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">官网服务 ↗</a></div>`;
const d=$('#chapterDialog');if(!d.open)d.showModal();$('#closeDialog').focus();}
document.addEventListener('click',e=>{const t=e.target.closest('[data-open-chapter],[data-chcat],[data-pcat],[data-copy-prompt],[data-fav],[data-expand],[data-copy-wechat],[data-modal-done]');if(!t)return;
if(t.hasAttribute('data-open-chapter')){openChapter(t.dataset.openChapter);return;}
if(t.hasAttribute('data-chcat')){chCategory=t.dataset.chcat;$('#chapterFilter').value=chCategory;renderChapters();return;}
if(t.hasAttribute('data-pcat')){pCategory=t.dataset.pcat;renderPrompts();return;}
if(t.hasAttribute('data-fav')){toggle('favorite',t.dataset.fav);renderPrompts();return;}
if(t.hasAttribute('data-copy-prompt')){const p=G.playbooks.find(x=>x.id===t.dataset.copyPrompt);if(p)copyText(p.prompt,'已复制完整任务指令');return;}
if(t.hasAttribute('data-expand')){const d=document.getElementById('detail-'+t.dataset.expand);if(d){d.open=!d.open;}return;}
if(t.hasAttribute('data-copy-wechat')){copyText('AIPMAndy','微信号已复制：AIPMAndy');return;}
if(t.hasAttribute('data-modal-done')){const id=t.dataset.modalDone;if(!has('done',id))toggle('done',id);renderChapters();openChapter(id);toast('本章已完成');return;}
});
document.addEventListener('change',e=>{const t=e.target;if(t.hasAttribute('data-done')){toggle('done',t.dataset.done);renderChapters();}if(t.hasAttribute('data-day')){toggle('day',t.dataset.day);renderRoadmap();}});
$('#chapterSearch').addEventListener('input',e=>{chSearch=e.target.value.trim();renderChapters();});
$('#chapterFilter').addEventListener('change',e=>{chCategory=e.target.value;renderChapters();});
$('#chapterUndone').addEventListener('change',e=>{chUndone=e.target.checked;renderChapters();});
$('#promptSearch').addEventListener('input',e=>{pSearch=e.target.value.trim();renderPrompts();});
$('#savedOnly').addEventListener('change',e=>{onlySaved=e.target.checked;renderPrompts();});
$('#resetPrompts').addEventListener('click',()=>{pSearch='';pCategory='全部';onlySaved=false;$('#promptSearch').value='';$('#savedOnly').checked=false;renderPrompts();});
$('#faqSearch').addEventListener('input',e=>{faqQuery=e.target.value.trim();renderFaq();});
$('#closeDialog').addEventListener('click',()=>$('#chapterDialog').close());
$('#chapterDialog').addEventListener('click',e=>{if(e.target===$('#chapterDialog'))$('#chapterDialog').close();});
$('#exportProgress').addEventListener('click',()=>{const lines=['# Grok Bot 保姆级使用攻略｜个人学习记录','','导出日期：'+new Date().toLocaleDateString('zh-CN'),'','## 已完成章节',...G.chapters.filter(c=>has('done',c.id)).map(c=>'- '+c.title),'','## 已完成 7 天计划',...G.roadmap.filter((_,i)=>has('day',String(i+1))).map(d=>'- '+d.day+' '+d.title),'','## 收藏的指令模板',...G.playbooks.filter(p=>has('favorite',p.id)).map(p=>'- '+p.title),'','来源：https://github.com/AIPMAndy/grok-bot-handbook'];const content=lines.join('\n');const blob=new Blob([content],{type:'text/markdown;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='Grok-Bot-学习记录.md';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('学习记录已导出');});

// v2: Transparent diagnosis wizard and readiness preflight. Both are local-only tools.
const EXTRA=window.GROK_EXTRA;
if(EXTRA&&Array.isArray(EXTRA.diagnostics)&&Array.isArray(EXTRA.preflight)){
  const diagSelect=$('#symptomSelect');
  diagSelect.innerHTML=EXTRA.diagnostics.map(x=>`<option value="${esc(x.id)}">${esc(x.label)}</option>`).join('');
  function showDiagnostic(){
    const x=EXTRA.diagnostics.find(d=>d.id===diagSelect.value);if(!x)return;
    $('#diagnoseIntro').innerHTML=`<span class="diagnose-severity">处理优先级 · ${esc(x.severity)}</span><h3>${esc(x.action)}</h3><p>${esc(x.intro)}</p>`;
    $('#diagnoseSteps').innerHTML=x.steps.map((step,i)=>`<div class="diagnostic-step"><b>STEP ${String(i+1).padStart(2,'0')}</b><p>${esc(step)}</p></div>`).join('');
    $('#diagnoseSource').setAttribute('href',x.source);
  }
  diagSelect.addEventListener('change',showDiagnostic);
  showDiagnostic();
  const preflightIds=new Set();
  $('#preflightChecks').innerHTML=EXTRA.preflight.map(item=>`<label class="preflight-check"><input type="checkbox" data-preflight="${esc(item.id)}"><span>${esc(item.label)}</span></label>`).join('');
  function updatePreflight(){
    let count=preflightIds.size, total=EXTRA.preflight.length;
    $('#preflightCount').textContent=`${count} / ${total}`;
    $('#preflightBar').style.width=(count/total*100)+'%';
    $('#preflightAdvice').textContent=count===total?'前置检查全部勾选。仍需对实际任务做沙盒测试、人工审批与运行日志核验。':'还有 '+(total-count)+' 项未确认。建议只做只读任务或内部草稿，不启动无人值守外部写入。';
  }
  $('#preflightChecks').addEventListener('change',e=>{
    const id=e.target.dataset.preflight;
    if(!id)return;
    if(e.target.checked)preflightIds.add(id);else preflightIds.delete(id);
    updatePreflight();
  });
  updatePreflight();
}

renderChapters();renderPrompts();renderRoadmap();renderFaq();
})();
