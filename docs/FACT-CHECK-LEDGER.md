# 官方事实主张台账｜v3

> 核验日：2026-10-21。来源：当时可访问的产品官方公开说明，**不等于**作者本人持账号复现。机器可读原始台账：[`data/claims.json`](../data/claims.json)。

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
| C-003 | legacy-access | high | 14 天 | [官方页面](https://cursor.com/help/grok-bot/plans) |
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
