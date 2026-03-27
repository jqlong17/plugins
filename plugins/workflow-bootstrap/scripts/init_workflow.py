#!/usr/bin/env python3
"""Initialize a numbered workflow directory for collaborative delivery."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "workflow/README.md": """# Workflow

这是一个用于说明用户与 AI 如何协作推进项目的工作流目录。

`README.md` 作为总索引，不参与编号；其他 Markdown 文件统一按 `00`、`01`、`02` 的前缀方式命名，便于按时间和阶段浏览。

## 目录说明

- `00-rule`：全局规则、协作原则、质量门禁与默认约定。
- `01-调研`：背景、目标、约束、现状调研与风险识别。
- `02-设计`：方案、架构、目录设计、测试设计与验收口径。
- `03-执行`：严格按 TDD 进行的执行计划、任务拆分与交付记录。
- `04-测试`：测试策略、测试用例、回归测试、健康报告与日志归档。

## 默认协作闭环

1. 先在 `01-调研` 明确目标、约束与现状。
2. 再在 `02-设计` 形成清晰方案与测试设计。
3. 然后在 `03-执行` 以 `Red -> Green -> Refactor` 的方式推进实现。
4. 最后在 `04-测试` 记录验证结果、问题清单、回归状态与健康报告。

## 命名约束

- `README.md` 不编号。
- 其他 Markdown 文件必须编号，例如 `00-xxx.md`、`01-xxx.md`。
- 新增文档按同目录内时间顺序递增编号。
""",
    "workflow/00-rule/00-执行计划撰写原则.md": """# 00-执行计划撰写原则

> 适用范围：`workflow/03-执行/` 下全部执行计划  
> 目标：确保所有落地任务严格遵循 `TDD 驱动 + 模块解耦 + 可审计测试日志`

## 1. TDD 必须项

所有执行计划必须按 `Red -> Green -> Refactor` 组织，不允许先写功能再补测试。

每个执行单元至少包含：

1. `Red`：先定义失败测试、断言、输入输出与验收口径。
2. `Green`：只实现让当前测试通过的最小代码。
3. `Refactor`：在保持测试通过的前提下清理结构、提炼复用与去重。

## 2. 模块边界

每个模块都必须明确：

1. 输入
2. 输出
3. 依赖
4. 数据契约
5. 不做项

## 3. 产出要求

每个模块完成时必须同步产出：

1. 执行计划更新
2. 对应测试用例
3. 测试日志
4. 回归结果
5. 如有需要的回滚说明
""",
    "workflow/00-rule/01-协作与编号规则.md": """# 01-协作与编号规则

## 1. 总体约定

1. `README.md` 永远作为索引文件，不编号。
2. 其他 Markdown 文件统一使用两位编号前缀，例如 `01-`、`02-`、`03-`。
3. 同一目录下的新增文档必须按照时间顺序递增编号。
4. 长期稳定规则一律沉淀在 `00-rule`，不要散落到执行文档中。

## 2. 协作方式

1. 先调研，再设计，再执行，再测试。
2. 设计阶段必须包含测试设计，不允许把测试推迟到功能完成之后。
3. 每次较大变更都要能追溯到调研、设计、执行、测试中的对应文档。

## 3. 变更纪律

1. 新增规则优先补充到 `00-rule`。
2. 新增阶段性成果优先补充到对应阶段目录。
3. 所有测试日志必须保留命令、日期、环境、结果与结论。
""",
    "workflow/00-rule/02-测试与质量门禁规则.md": """# 02-测试与质量门禁规则

## 1. 测试优先

1. 所有功能点都必须先补测试设计，再开始实现。
2. 单元测试是默认起点；集成测试、回归测试和 E2E 测试按风险逐层补齐。

## 2. 可追溯要求

测试体系必须满足：

1. 可记录上下文
2. 可持久化日志
3. 可还原执行命令
4. 可追溯到功能点和用例编号
5. 可回看历史回归结果

## 3. 覆盖率门槛

1. 核心功能总覆盖率目标不低于 `85%`。
2. 新增核心模块若未达到门槛，必须在测试健康报告中写明原因、风险与补齐计划。

## 4. 必备测试层级

1. 单元测试
2. 集成测试
3. 回归测试
4. E2E 测试

## 5. 质量门禁

交付前必须同时满足：

1. 功能验收通过
2. 单元测试通过
3. 回归测试通过
4. E2E 关键路径通过
5. 测试日志已归档
6. 健康报告已更新
""",
    "workflow/01-调研/01-项目背景与目标.md": """# 01-项目背景与目标

## 1. 项目背景

- 项目名称：
- 业务背景：
- 当前阶段：

## 2. 目标

1. 本次协作要解决的问题：
2. 期望交付的结果：
3. 成功标准：

## 3. 约束

1. 技术约束：
2. 时间约束：
3. 协作约束：

## 4. 关键相关方

1. 用户：
2. 开发：
3. 测试：
4. 其他：
""",
    "workflow/01-调研/02-现状调研与风险清单.md": """# 02-现状调研与风险清单

## 1. 当前现状

1. 现有代码结构：
2. 已有测试基础：
3. 已知问题：

## 2. 外部依赖

1. 第三方服务：
2. 基础设施：
3. 关键包与组件：

## 3. 风险清单

| 编号 | 风险描述 | 影响 | 概率 | 应对策略 |
| --- | --- | --- | --- | --- |
| R-01 | 待补充 | 高/中/低 | 高/中/低 | 待补充 |

## 4. 调研结论

- 建议优先级：
- 需要进一步确认的问题：
""",
    "workflow/02-设计/01-技术方案与目录设计.md": """# 01-技术方案与目录设计

## 1. 方案目标

1. 明确功能范围
2. 明确模块边界
3. 明确代码目录与依赖关系
4. 明确测试切入点

## 2. 模块设计

| 模块 | 职责 | 输入 | 输出 | 依赖 | 不做项 |
| --- | --- | --- | --- | --- | --- |
| M1 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |

## 3. 目录设计

```text
待补充项目目录结构
```

## 4. 验收标准

1. 功能验收：
2. 接口或数据验收：
3. 测试验收：
""",
    "workflow/02-设计/02-测试策略与覆盖率设计.md": """# 02-测试策略与覆盖率设计

## 1. 测试目标

1. 所有核心功能点均有对应测试用例。
2. 覆盖率目标不低于 `85%`。
3. 测试结果可追溯、可复现、可归档。

## 2. 分层策略

1. 单元测试：覆盖纯逻辑、状态流转、边界分支。
2. 集成测试：覆盖模块协作、接口契约、数据流。
3. 回归测试：覆盖历史高频故障与关键功能路径。
4. E2E 测试：覆盖用户主链路。

## 3. 日志与上下文

每次测试执行至少记录：

1. 日期与执行人
2. 执行环境
3. 测试命令
4. 用例范围
5. 通过/失败统计
6. 失败现象与定位结论
7. 关联任务、提交或文档

## 4. 推荐工具

优先选择当前技术栈中成熟稳定的测试方案，例如：

1. 前端：`Vitest`、`Testing Library`、`Playwright`
2. Node 服务：`Vitest` 或 `Jest`、`Supertest`
3. Python 服务：`pytest`、`pytest-cov`

## 5. 覆盖率报告

1. 输出总覆盖率与关键模块覆盖率。
2. 对低于阈值的模块单独给出风险说明。
""",
    "workflow/03-执行/01-TDD执行计划.md": """# 01-TDD执行计划

## 1. 背景与目标

- 任务背景：
- 本次目标：

## 2. 模块边界与不做项

| 模块 | 输入 | 输出 | 依赖 | 不做项 |
| --- | --- | --- | --- | --- |
| M1 | 待补充 | 待补充 | 待补充 | 待补充 |

## 3. TDD 任务拆解

### 模块：M1

#### Red

1. 先写失败测试：
2. 定义断言：
3. 明确边界数据：

#### Green

1. 实现最小代码：
2. 让当前失败测试转绿：

#### Refactor

1. 去重与重构：
2. 保持测试通过：

## 4. 验收标准

1. 功能通过
2. 对应测试通过
3. 测试日志归档
4. 无阻断级问题

## 5. 风险与回滚

1. 风险：
2. 回滚策略：

## 6. 产出物

1. 代码变更
2. 测试用例
3. 测试日志
4. 回归记录
""",
    "workflow/04-测试/01-测试策略总览.md": """# 01-测试策略总览

## 1. 目标

建立一套可扩展、可记录上下文、可持久化日志、可追溯、可还原的测试体系。

## 2. 覆盖范围

1. 每个功能点必须存在对应测试用例。
2. 核心链路必须存在回归测试。
3. 用户主路径必须存在 E2E 测试。

## 3. 结果归档

1. 测试日志归档到 `workflow/04-测试/logs/<模块>/<YYYY-MM-DD>/`
2. 测试用例索引归档到 `workflow/04-测试/cases/`
3. 健康报告归档到 `workflow/04-测试/03-测试健康报告.md`

## 4. 交付口径

1. 测试命令可重复执行
2. 日志可还原执行现场
3. 用例与功能点一一对应
""",
    "workflow/04-测试/02-回归测试计划.md": """# 02-回归测试计划

## 1. 回归目标

确保历史高风险问题和核心业务路径在每次变更后仍保持稳定。

## 2. 回归范围

| 回归编号 | 功能点 | 风险来源 | 触发条件 | 执行方式 |
| --- | --- | --- | --- | --- |
| REG-01 | 待补充 | 历史缺陷/核心路径 | 每次发布前 | 自动/手动 |

## 3. 执行节奏

1. 每次关键功能合并前执行
2. 每次发布前完整执行
3. 缺陷修复后补充定向回归

## 4. 结果记录

回归结果必须同步到对应测试日志和健康报告。
""",
    "workflow/04-测试/03-测试健康报告.md": """# 03-测试健康报告

## 1. 总体状态

- 报告日期：
- 测试负责人：
- 当前版本：
- 总体健康度：绿 / 黄 / 红

## 2. 指标概览

| 指标 | 当前值 | 目标值 | 状态 | 说明 |
| --- | --- | --- | --- | --- |
| 总覆盖率 | 待补充 | >= 85% | 待定 | 待补充 |
| 单元测试通过率 | 待补充 | 100% | 待定 | 待补充 |
| 回归通过率 | 待补充 | 100% | 待定 | 待补充 |
| E2E 关键路径通过率 | 待补充 | 100% | 待定 | 待补充 |

## 3. 风险模块

| 模块 | 风险等级 | 问题描述 | 补救动作 | 负责人 |
| --- | --- | --- | --- | --- |
| 待补充 | 高/中/低 | 待补充 | 待补充 | 待补充 |

## 4. 结论

1. 是否允许继续发布：
2. 若不允许，阻断原因：
3. 下阶段补齐计划：
""",
    "workflow/04-测试/cases/01-功能测试用例总表.md": """# 01-功能测试用例总表

## 1. 用例约定

1. 每个功能点至少对应一个用例编号。
2. 所有用例都要能映射到调研、设计、执行与测试文档。
3. 用例编号建议按模块前缀管理，例如 `AUTH-01`、`API-01`。

## 2. 用例清单

| 用例编号 | 功能点 | 测试层级 | 前置条件 | 预期结果 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CASE-01 | 待补充 | 单元/集成/E2E | 待补充 | 待补充 | 待执行 |
""",
    "workflow/04-测试/logs/README.md": """# Test Logs

测试日志按模块和日期归档，推荐目录结构如下：

```text
workflow/04-测试/logs/
  <模块名>/
    YYYY-MM-DD/
      01-测试执行日志.md
      02-回归测试日志.md
      03-E2E测试日志.md
```

日志必须包含：

1. 日期与执行人
2. 环境信息
3. 执行命令
4. 范围与用例
5. 通过/失败统计
6. 定位结论
7. 关联变更
""",
}


def build_existing_workflow_advice(workflow_root: Path) -> str:
    existing_markdown_files = sorted(
        path.relative_to(workflow_root).as_posix()
        for path in workflow_root.rglob("*.md")
        if path.is_file()
    )

    numbered_issues = [
        path for path in existing_markdown_files
        if Path(path).name.lower() != "readme.md" and not Path(path).name[:2].isdigit()
    ]

    lines = [
        "Detected an existing workflow directory. No files were changed to avoid overwriting user data.",
        "",
        "Suggested review items:",
        "1. Confirm whether the current workflow structure should remain the source of truth.",
        "2. Compare existing subdirectories against the recommended baseline: 00-rule, 01-调研, 02-设计, 03-执行, 04-测试.",
        "3. Ensure README.md stays as the unnumbered index file in each workflow area.",
        "4. Move long-term collaboration rules into workflow/00-rule instead of scattering them across execution notes.",
        "5. Check whether execution plans explicitly follow Red -> Green -> Refactor.",
        "6. Check whether testing artifacts include cases, regression plans, health reports, and persistent logs.",
        "7. Verify that non-README markdown files use numeric prefixes for chronological browsing.",
        "",
        f"Existing markdown files found: {len(existing_markdown_files)}",
    ]

    if existing_markdown_files:
        lines.append("Markdown inventory:")
        lines.extend(f"- {path}" for path in existing_markdown_files[:50])
        if len(existing_markdown_files) > 50:
            lines.append(f"- ... and {len(existing_markdown_files) - 50} more")

    if numbered_issues:
        lines.extend([
            "",
            "Potential naming issues:",
        ])
        lines.extend(f"- {path}" for path in numbered_issues)

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a reusable workflow directory.")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project root. Defaults to current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    parser.add_argument(
        "--allow-existing-workflow",
        action="store_true",
        help="Allow writing into a project that already has a workflow directory.",
    )
    return parser.parse_args()


def write_file(path: Path, content: str, force: bool) -> str:
    existed = path.exists()
    if existed and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if existed and force:
        return "updated"
    return "created"


def initialize_workflow(target_root: Path, force: bool = False) -> dict[str, list[str]]:
    created: list[str] = []
    updated: list[str] = []
    skipped: list[str] = []

    for relative_path, content in TEMPLATES.items():
        file_path = target_root / relative_path
        already_exists = file_path.exists()
        status = write_file(file_path, content, force)
        if status == "created" and not already_exists:
            created.append(relative_path)
        elif status == "updated":
            updated.append(relative_path)
        else:
            skipped.append(relative_path)

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
    }


def main() -> None:
    args = parse_args()
    target_root = Path(args.target).expanduser().resolve()
    workflow_root = target_root / "workflow"

    if workflow_root.exists() and not args.allow_existing_workflow and not args.force:
        print(build_existing_workflow_advice(workflow_root), end="")
        return

    summary = initialize_workflow(target_root, force=args.force)

    print(f"Initialized workflow under: {target_root / 'workflow'}")
    print(f"Created: {len(summary['created'])}")
    print(f"Updated: {len(summary['updated'])}")
    print(f"Skipped: {len(summary['skipped'])}")

    for key in ("created", "updated", "skipped"):
        if summary[key]:
            print(f"{key.upper()}:")
            for item in summary[key]:
                print(f"  - {item}")


if __name__ == "__main__":
    main()
