# Grok Bot Handbook v2.0 — 对抗式审计报告

> 审核日期：2026-10-21（官方公开资料）。性质：静态代码、事实证据与内容对抗审查；**没有连接用户 Grok Bot 实测真实任务**。不得把本报告当成 Grok Bot 实测背书。

## 审计方法

从七种“会毁掉这份教程”的视角对项目攻击：①刚买错会员的小白；②只能用手机的人；③敏感客户数据的所有者；④负责审批的企业管理员；⑤不相信 Bot 自述的事实核查员；⑥遇到网络/配额错误的用户；⑦想复制项目并长期维护的开源贡献者。每种视角要求给出可复现的问题、影响面和验证方式。

风险等级：P0=误导付费/隐私或严重越权；P1=关键功能缺失/错误流程；P2=体验、理解或维护成本；P3=文案视觉。

| 编号 | 等级 | 对抗式攻击 / 失败案例 | 原版风险 | v2 修复动作 | 验证路径 |
|---|---|---|---|---|---|
| A01 | P0 | “X Premium 用户照着教程直接买错套餐” | 旧版只讲 Cursor/SuperGrok | 明确 The X Subscription Premium/Super/Ultra 与 Plus/Free、旧版 Cursor 与 X Premium+ 关联路径 | [官方计费矩阵](https://cursor.com/help/grok-bot/plans)、[计费说明](BILLING-AND-ACCESS.md) |
| A02 | P0 | “说独立额度导致用户不设充值上限” | 新旧体系计量方式未区分 | 新版共享周池，旧版独立判断；增加费用守门 SOP | [计费说明](BILLING-AND-ACCESS.md) |
| A03 | P0 | “公开模板带出组织密钥” | 分享前检查不完整 | Team Bot / 公开模板 / 私人 Bot 区分、分享前 11 项审核 | [安全审批](APPROVAL-RUNBOOK.md) |
| A04 | P0 | “多个 Bot 同时读到不属于自己的客户文件” | Bot 对话与共享云电脑的权限差异易被误解 | 共享电脑威胁模型、数据最小化与独立账号隔离原则 | [安全专题](SECURITY.md) |
| A05 | P0 | “重复 Routine 导致二次转账/重复发帖” | 缺少去重与幂等模式 | 新增 webhook 章节、幂等键和人工审批示例 | [运营手册](OPERATIONS-PLAYBOOK.md) |
| A06 | P0 | “把网页嵌入指令当作管理员授权” | 提示注入未单列 | 新增威胁场景与防护模板 | [审批手册](APPROVAL-RUNBOOK.md) |
| A07 | P1 | “新用户照着没有的按钮无法安装” | UI 随版本变化 | 用官方页路径+界面条件提示+版本记录 | [快速入门](../guides/START-HERE.md) |
| A08 | P1 | “Teach a task 未开放还写成人人可用” | 功能渐进开放 | 标记需要可用性核对，添加文字 SOP 替代 | [官方 Skills](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| A09 | P1 | “Teams 的 OAuth 被误解为借用管理员权限” | 对 Team Bot 缺少专题 | 新增 Team Bot 与插件凭据来源章节 | [官方 Team Bots](https://docs.x.ai/grok-bot/team-bots) |
| A10 | P1 | “Reset 一点直接丢工作” | 故障条目没有独立执行流程 | 将 Retry→Recover/Update→Reset 变成诊断路径 | [故障手册](TROUBLESHOOTING.md) |
| A11 | P1 | “点击测试运行造成真实发布” | Test run 概念不清 | 标明测试可真实调用外部系统，强调沙盒/预览与批准 | [官方 Routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| A12 | P1 | “官网源链接坏了读者无处核对” | 来源列表有限 | 扩到计费、移动端、团队、文件、X 等专题；增加静态引用测试 | [官方来源](SOURCES.md) |
| A13 | P1 | “用户拿公开示例宣传成真实成交案例” | 案例无统一证据级别 | 每条模板注记为未宣称实测，新增四级证据与发布门槛 | [案例标准](CASE-STUDY-PROTOCOL.md) |
| A14 | P1 | “任务没有可量化验收却说省很多钱” | 指令缺少统一价值验证 | 10 次执行对照模板、ROI 和净工时口径 | [运营手册](OPERATIONS-PLAYBOOK.md) |
| A15 | P1 | “用 X @bot 失败误判为网络问题” | 缺少 X 入口专题 | 增加账号关联、地域和帖子条件提示 | [X 官方说明](https://docs.x.ai/grok-bot/tag-on-x) |
| A16 | P1 | “移动端体验全靠桌面截图” | 移动端没有独立验收表 | 增加系统版本/触控/审批专项测试单 | [人工测试](QA-MANUAL.md) |
| A17 | P2 | “FAQ 太难定位” | 仅文本搜索 | 增加故障定位助手、官方引用和步骤卡片 | [互动网站](../index.html) |
| A18 | P2 | “用了几十次后不知道哪些例程该停” | 缺少持续维护 | 新增 SLO、复盘、例程停用清单 | [运营手册](OPERATIONS-PLAYBOOK.md) |
| A19 | P2 | “多文件事实各改一次内容不一致” | JSON / JS / docs 可能漂移 | 单源生成+一致性测试+更新检查 | [贡献规范](QUALITY-STANDARDS.md) |
| A20 | P2 | “教程只有作者能修” | 贡献与复现机制不足 | Issue 模板、审计严重性与证据门槛 | [开源治理](QUALITY-STANDARDS.md) |

## 本轮不应宣称已解决的问题

- **产品亲自实测**：未登录 Grok Bot 执行实际任务，不能保证每一个平台菜单今天对所有账号一致。
- **跨浏览器自动化 E2E**：CI 做内容、链接结构、脚本与无障碍静态检查；真实浏览器网络条件应按 `QA-MANUAL.md` 再测。
- **功能实时可用与套餐现价**：官方文档会调整，GitHub 不会自动保证未来永不过时。
- **全网规模排名**：没有全网同类仓库盘点和标准化比较，不能客观宣称“全网第一”。

## 发布门禁

P0 未处理禁止发布；P1 必须有修复或明确 Known limitation；P2 进入 Issue 并标注负责人。每次更新检查结构化数据与全文文档的一致性、官方来源引用、隐私说明与测试状态。
