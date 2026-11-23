# 官方事实主张台账｜v3

> 最近一次公开文档核验：**2026-11-24**（历史初稿 2026-10-21）。核验对象为 xAI / Grok Bot 的官方公开说明，**不等于**作者本人持账号复现。机器可读原始台账：[`data/claims.json`](../data/claims.json)。

## 怎么维护

1. 功能、权限、价格、隐私、自动化等高风险结论必须分配固定 `C-xxx` 编号。
2. 每条写明 `official_url`、对应本地文档、风险等级、`last_verified`、最大允许间隔 `max_age_days`。
3. 修改结论前打开官方原文；记录实际日期，更新文案、文档和台账。
4. CI 在超过验证窗口时阻止**新的**发布，不代表旧网页会自动下架或事实永远为真。
5. 真实账号测试必须另外填 [运行证据模板](../templates/TEST-RUN-LOG.csv)；不能把“官方有文档”当成自己做成了。
6. 链接访问状态需人工或通过在线脚本检查，**网址符合官方域名不等于链接真实存在**。

## 12 条关键主张

| 编号 | 主题 | 风险 | 复核间隔 | 官方证据 |
|---|---|---|---|---|
| C-001 | subscription | high | 14 天 | [官方页面](https://docs.x.ai/x-subscription/grok-bot) |
| C-002 | billing | high | 14 天 | [官方页面](https://docs.x.ai/x-subscription/grok-bot) |
| C-003 | legacy-access | high | 14 天 | [Grok Bot 官方 FAQ](https://docs.x.ai/grok-bot/faq) |
| C-004 | isolation | critical | 30 天 | [官方页面](https://docs.x.ai/grok-bot/computer-and-apps) |
| C-005 | approval | critical | 30 天 | [官方页面](https://docs.x.ai/grok-bot/approvals-security-and-privacy) |
| C-006 | authentication | critical | 30 天 | [官方页面](https://docs.x.ai/grok-bot/get-started) |
| C-007 | routines | high | 30 天 | [官方页面](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| C-008 | gradual-rollout | medium | 45 天 | [官方页面](https://docs.x.ai/grok-bot/skills-routines-and-automations) |
| C-009 | team-bots | high | 30 天 | [官方页面](https://docs.x.ai/grok-bot/team-bots) |
| C-010 | devices | medium | 45 天 | [官方页面](https://docs.x.ai/grok-bot/faq) |
| C-011 | data-deletion | critical | 30 天 | [官方页面](https://docs.x.ai/grok-bot/faq) |
| C-012 | automation-safety | critical | 30 天 | [官方页面](https://docs.x.ai/grok-bot/skills-routines-and-automations) |

## 证据分层

- **L0：未核实观点/示范模板**，不可宣称为产品事实。
- **L1：官方公开资料**，可引用能力与限制，但要注明核查日期。
- **L2：真实账号单次运行**，需记录套餐、客户端版本、输入、脱敏证据、预期与实际结果。
- **L3：跨次稳定运行**，至少记录连续多次真实任务及失败率，且说明样本条件。

项目当前关键官方主张为 L1，真实运行样本尚未达到 L2；商业案例不能跨级宣传。

## 2026-11-24 公开文档复核记录

逐项核对了 12 条主张对应的官方公开网页内容及其限制条件；这是 **L1 文档层面的复核**，未进行任何 L2 真实账户、地区套餐、桌面/手机 App 或 Bot 自动化运行测试。官网内容可能在复核后变化。

- C-001/C-002：以 [The X Subscription / Grok Bot](https://docs.x.ai/x-subscription/grok-bot) 公开条款为准，确认新版计划范围与每周共享使用池。不得推导某个人当前账户已获权益。
- C-003：旧的 `cursor.com/help/grok-bot/plans` 链接对本次读取返回 HTTP 403；改为可读的 [Grok Bot FAQ](https://docs.x.ai/grok-bot/faq) 核对旧 Cursor 计划与绑定 SuperGrok、X Premium+ 的区别。这不是对不可访问旧网页的核验。
- C-004：[云电脑与应用](https://docs.x.ai/grok-bot/computer-and-apps) 明确同一用户多个 Bot 共享浏览器登录、文件和命令行凭据。
- C-005：[审批、安全与隐私](https://docs.x.ai/grok-bot/approvals-security-and-privacy) 区分审批当前动作和逆转已执行动作，后者不成立。
- C-006：[官方入门](https://docs.x.ai/grok-bot/get-started) 区分密码安全表单与需要用户接管电脑的单点登录等特殊步骤；本轮已修订台账原先过度笼统的说法。
- C-007/C-008/C-012：[Skills 与 Routines](https://docs.x.ai/grok-bot/skills-routines-and-automations) 说明运行间隔/次数、Teach a task 渐进开放及 Test 可以进行真实外部操作。
- C-009：[Team Bots](https://docs.x.ai/grok-bot/team-bots) 明确共享 Bot 与个人聊天、团队凭据、配置分享不同的安全边界；本轮澄清主张措辞。
- C-010/C-011：[FAQ](https://docs.x.ai/grok-bot/faq) 说明设备支持和删除 Bot 后共享云电脑仍可能有文件/登录状态。

**发布与 PDF 边界**：2026-11-13 的 97 页 PDF 沿用原始出版物，未将本次官网复核直接宣称为 PDF 内容同步更新；其文内动态计费/安全细节需要下次从 Markdown 权威源重生成并完成逐页文本与人工视觉 QA。官方 L1 记录不能替代 iOS/Android 真机、VoiceOver/TalkBack 或产品账号实测。

[查看站内来源核验工作台](../source-audit.html)。
