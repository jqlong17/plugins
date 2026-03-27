# Workflow Bootstrap

这个插件用于在任意项目根目录初始化一套统一的 `workflow/` 协作目录。

它固化以下约定：

- `README.md` 作为总索引，其他 Markdown 文档按 `00`、`01`、`02` 编号。
- `00-rule` 专门存放全局协作规则。
- `01-调研` 用于沉淀前期研究，包括本项目代码调研、外部项目调研、某个方向的前期研究，以及某次经验复盘或沉淀；目录内文档同样按时间顺序编号，例如 `01-`、`02-`。
- `02-设计` 用于沉淀总体设计内容，例如架构设计、产品页面设计、数据模型设计、技术栈选型等。
- `03-执行` 严格按 `Red -> Green -> Refactor` 的 TDD 方式编排执行计划。
- `04-测试` 内置测试策略、回归计划、健康报告、测试用例、轻量验证闭环与日志归档模板。
- 测试要求可追溯、可复现、可还原，并明确覆盖率门槛大于等于 85%。
- 更偏向中小项目的快速验证与迭代，不刻意引入过重的企业级流程负担。

## 使用方式

当 Codex 选中这个插件后，可以直接说：

- `请初始化这个项目的协作工作流`
- `新建一个协作工作流`
- `帮我初始化 workflow 目录`

插件会调用：

```bash
python3 ../../scripts/init_workflow.py <target-project-root>
```

脚本默认把当前工作目录视为目标项目根目录；如果检测到已存在的 `workflow/`，则默认只给建议、不直接覆盖。

## 主要入口

- Skill: `skills/workflow-bootstrap/SKILL.md`
- Script: `scripts/init_workflow.py`
- Tests: `tests/test_init_workflow.py`

## 插件目录

```text
workflow-bootstrap/
├── .codex-plugin/plugin.json
├── README.md
├── assets/
├── scripts/
├── skills/
└── tests/
```
