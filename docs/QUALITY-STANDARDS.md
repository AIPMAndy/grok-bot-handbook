# 质量标准与维护制度

## v3 阻断式发布链

**禁止**在只做内容测试之后直接独立部署。`.github/workflows/deploy-pages.yml` 的 `deploy` 必须依赖 `verify`；`verify` 依次执行事实主张时效校验、构建确定性检查、单元测试与 JS 语法检查。

- 所有高风险事实更新先改 [`data/claims.json`](../data/claims.json) 的复核日期和主张文本，再核对对应官方文档。
- 自动过期拦截只限制后续**新发布**，不会自动修改已经上线的网页；站长仍需要主动维护。
- CI 不访问订阅者账号，也不能替代浏览器端的真实运行复现。

## 发布检查表

- [ ] 事实声明有一手官方来源，且标记“官方说明”“编辑整理”或“作者实测”。
- [ ] 新旧订阅计划、期限、资格、地区限制以当天官方页面核对。
- [ ] 每个章节具备目标、步骤、验收、常见误区和来源链接。
- [ ] 每个模板具备合法输入、完整指令、检验指标、风险边界。
- [ ] 更新 `scripts/build_content.py` 并重新生成 JSON/JS；Markdown 全文同步导出。
- [ ] 自动测试和 JS 语法检查全通过；移动端人工测试有记录。
- [ ] 关键链接不失效；无原文隐私、未授权截图和敏感凭据。
- [ ] 没有将示范流程写成真实完成的用户结果。
- [ ] 全部免费内容不用添加微信也能访问；商业服务清晰标记为可选。

## 变更频率

- **新版本更新时**：核实官方功能说明及产品变更记录。
- **每月一次**：核对计划/计费、登录界面、操作步骤、安卓与 iOS 适配。
- **每季度一次**：完整执行高风险场景、体验测试与案例证据抽样。
- **重大 P0**：尽可能当天修复或明确标注“内容待核实”，不得继续放任误导。

## Issue 模板要求

功能与事实问题均需：受影响网页/章节、操作系统及版本、账户套餐（不要上传凭据）、复现步骤、官方证据 URL、期望与实际、敏感信息已遮盖的截图（可选）。

## 维护规则

使用 `scripts/build_content.py` 作为教程和提示词的**唯一事实源**；`data/catalog.json` 和 `data/catalog.js` 不允许手工分别修改。每次更新必须跑：

```bash
python3 scripts/check_claims.py
python3 scripts/build_content.py
python3 scripts/export_docs.py
python3 scripts/build_extras.py
python3 -m unittest discover -s tests -v
node --check app.js
node --check data/catalog.js
node --check data/extras.js
```

静态校验只能保证文件及结构正确，不代表已在所有账号上真实操作成功。体验回归见 [QA-MANUAL](QA-MANUAL.md)。
