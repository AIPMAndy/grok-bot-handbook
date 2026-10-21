# Grok Bot 故障排查手册

遵循「最小破坏 → 检查状态 → 安全恢复」顺序。下面步骤整理自 [官方 Troubleshooting](https://docs.x.ai/grok-bot/troubleshooting)，请以应用当前选项为准。

| 症状 | 优先检查 | 可尝试的安全动作 | 不建议 |
| --- | --- | --- | --- |
| 登录一直循环 | 浏览器是否完成 Cursor 登录，账号是否有 Grok Bot 资格 | 回到客户端，重新走登录；检查 SSO | 直接在聊天里发密码 |
| 提示 Privacy Mode | 账号数据设置是否允许云端存储 | 先阅读官方隐私条款再决策 | 不理解影响就强行关闭保护 |
| 云电脑一直初始化 | App 是否最新、电脑状态是否推进 | 重试、重启、更新云电脑 | 立刻 Reset |
| Bot 卡住 | CAPTCHA、审批、登录、当前任务是否等待交互 | 查看计算机视图，按需要真人 Take over | 绕过网站验证 |
| 网站要求反复登录 | 浏览器登录状态、MFA 或会话过期 | Take over 自己登录，再交回 Bot | 粘贴密码/验证码到对话 |
| 额度不足 | Usage & Billing / 账号资格 | 以实时计费页核对重置与限制 | 根据旧教程猜价格 |
| Routine 不执行 | 是否启用、时区、拥有者、连接器、计算机状态与额度 | 检查最近运行日志、用安全数据 Test run | 将真实发送任务当“无风险测试” |
| 审批卡住 | 规则匹配和目标参数 | 检查 Ask first、重建准确操作 | 建议“允许浏览器全部动作” |
| @bot 未回复 X | 区域开放、视频帖、是否同时提及 @grok 等规则 | 查看官方 X Tag Bot 文档 | 批量重复刷提及 |
| 共享数据不放心 | 哪些 Bot 共享登录和文件 | 最小授权，必要时独立账号，撤销不用的权限 | 把 Bot 名称当安全隔离 |

## 提交故障报告前记录

客户端版本、系统版本、发生时间及时区、错误原文、Bot / Routine 名称、操作步骤、重试结果。日志或截图须去除 Token、密码、客户姓名与验证信息。

官方来源：[故障排查](https://docs.x.ai/grok-bot/troubleshooting) ｜ [账户与访问](https://docs.x.ai/grok-bot/get-started) ｜ [安全审批](https://docs.x.ai/grok-bot/approvals-security-and-privacy)。
