# 如何共建 Grok Bot 中文资料库

欢迎补充可核查的官方能力变化、复现过的操作步骤、错误修复、中文用户使用经验、移动端和无障碍改进。本仓库讨论 xAI 官方 Grok Bot，不将第三方同名产品混入。

## 提交前准备

1. **先查重**：搜索已有 Issue，并说明目前困扰你的具体任务、失败环节、期望行为。
2. **标明证据级别**：①官方确认；②可重复独立实测（附遮敏运行记录）；③待验证的复用模板。不要把第三种写成真实客户成功案例。
3. **提供证据**：产品功能、价格、区域、授权流程须附官方 URL 和核对日期；界面截图须遮盖所有隐私信息。
4. **写出可复现步骤**：前置条件、账号/环境边界、输入样例、操作、预期输出、错误输出、可能副作用、撤销办法。
5. **隐私与安全**：禁止提交密码、Token、客户文件、私人邮件或未授权个人信息。PR 模板里用伪造的测试数据，而非生产数据。

## 修改和构建

正文的权威来源文件是 `scripts/build_content.py`；交互诊断和安全检查的内容来源是 `scripts/build_extras.py`。编辑对应生成器后，**按顺序**运行：

```bash
python3 scripts/build_content.py
python3 scripts/export_docs.py
python3 scripts/build_extras.py
python3 -m unittest discover -s tests -v
node --check app.js
node --check data/catalog.js
node --check data/extras.js
```

提交后确保所有生成的 `data/*.json`、`data/*.js` 和 `docs/COMPLETE-GUIDE.md`、`docs/PROMPT-LIBRARY.md` 随源文件一起更新；不要只修改生成文件。网站入口为根目录 `index.html`，Pages 自动部署流程位于 `.github/workflows/deploy-pages.yml`。

## 合并门槛

- **P0**：影响付费决策、隐私泄露、越权或有破坏性的操作，未修复一律不得发布。
- **P1**：关键路径不可复现、官方资料失效、有重大缺漏，修复或明确作为已知限制。
- **P2**：体验、解释、维护性问题，需要记录和验证计划。
- 涉及真实案例需符合 [`docs/CASE-STUDY-PROTOCOL.md`](docs/CASE-STUDY-PROTOCOL.md) 的脱敏和验证要求。
- 涉及权限、支付、发布、删除等动作，参照 [`docs/APPROVAL-RUNBOOK.md`](docs/APPROVAL-RUNBOOK.md) 并要求人工确认。

建议 PR 包含：变更目的、关联官方资料、前后差异、已运行的测试、哪些内容仍未实际验证。详见 [`docs/QUALITY-STANDARDS.md`](docs/QUALITY-STANDARDS.md) 与 [`docs/ADVERSARIAL-AUDIT.md`](docs/ADVERSARIAL-AUDIT.md)。

开源项目代码采用 MIT 许可，不代表官方认可，也不授予第三方内容及商标权利。
