from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/catalog.json').read_text(encoding='utf8'))
md=[f"# Grok Bot 保姆级使用攻略｜{len(d['chapters'])} 章完整文字版",'', '> 官方 Grok Bot（x.ai/bot）中文整理。2026-10-21 对照公开官方资料核对；界面和订阅资格以官方最新说明为准。','', '官方入口：https://x.ai/bot','']
for c in d['chapters']:
 md.extend([f"## {c['num']:02d}. {c['title']}",'',f"**分类：** {c['category']}　**预计学习：** {c['minutes']} 分钟　**难度：** {c['level']}",'',c['summary'],'','### 为什么要做','',c['why'],'','### 操作步骤',''])
 md.extend(f'{i}. {v}' for i,v in enumerate(c['steps'],1))
 md.extend(['','### 验收标准','',c['check'],'','### 常见误区','',c['pitfall'],'',f"**官方参考：** {c['source']}",'','---',''])
(R/'docs/COMPLETE-GUIDE.md').write_text('\n'.join(md)+'\n',encoding='utf8')
md=[f"# Grok Bot {len(d['playbooks'])} 套复制即用的实战指令",'', '> 需要用 `{花括号}` 替换为真实值。提示词仅为可尝试的模板，未声称这些操作已替用户实际执行。','', '外发消息、购买、公开发布、删除、权限更改等任务，默认先给本人审批；遵守平台政策与个人信息保护要求。','']
for p in d['playbooks']:
 md.extend([f"## {p['id'][1:]}. {p['title']}",'',f"**场景：** {p['category']}　**目标：** {p['goal']}",'',f"**使用前准备：** {p['requires']}",'','### 完整提示词','','```text',p['prompt'],'```','','**验收标准：** '+p['verify'],'','**风险与边界：** '+p['risk'],'','---',''])
(R/'docs/PROMPT-LIBRARY.md').write_text('\n'.join(md)+'\n',encoding='utf8')
md=['# 7 天 Grok Bot 上手计划','', '> 先安全交付、再复用、最后自动化。用每一天的现实成果做证据，别用打卡次数衡量价值。','']
for row in d['roadmap']:
 md.extend([f"## {row['day']}｜{row['title']}",'',row['detail'],'','**今日成果记录：**','', '- [ ] 完成操作','- [ ] 记录来源/结果','- [ ] 记录错误或待审批项','','---',''])
(R/'guides/7-DAY-PLAN.md').write_text('\n'.join(md)+'\n',encoding='utf8')
md=['# 官方来源索引','', '> 最后整理：2026-10-21。文档会更新；时效性规则请以官方实时页面为准。','']
for i,s in enumerate(d['sources'],1):md.extend([f"{i}. [{s['title']}]({s['url']}) — {s['note']}"])
md.extend(['','## 来源原则','','- 不把官方 Grok Bot 与同名第三方开源项目混为一谈。','- 不静态承诺订阅价格、额度、地区可用性或运行效果。','- 任何自动外发、付款、删除、权限与生产更改均建议人工审批。','- 官方页面描述产品能力不等同于本作者已经实测所有功能。',''])
(R/'docs/SOURCES.md').write_text('\n'.join(md),encoding='utf8')
print('Docs exported')
