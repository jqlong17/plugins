---
name: workflow-bootstrap
description: Initialize a reusable workflow folder with numbered research, design, TDD execution, and testing documents plus global rules in 00-rule.
---

# Workflow Bootstrap

## Use this skill when

- The user says `请初始化这个项目`
- The user says `新建一个协作工作流`
- The user asks for a workflow folder, collaboration scaffold, or project initialization based on their standard process

## What this skill does

1. Treat the current working directory as the target project root unless the user explicitly gives another path.
2. Inspect whether a `workflow/` directory already exists.
3. Run the plugin script:

```bash
python3 ../../scripts/init_workflow.py <target-project-root>
```

4. If `workflow/` already exists, do not initialize or patch files by default. Instead, return the script's modification suggestions and ask the user whether they want a merge or a manual adjustment plan.
5. After generation, briefly summarize:
   - which files were created
   - whether the run was blocked because an existing workflow was detected
   - what follow-up project-specific documents should be filled first, especially:
     - `01-调研` for codebase research, external project research, topic pre-research, and experience notes
     - `02-设计` for architecture design, page/product design, data model design, and technology selection

## Operating rules

- `README.md` is the index and must remain unnumbered.
- Every other generated Markdown file must use a numeric prefix such as `00-`, `01-`, `02-`.
- Global rules belong under `workflow/00-rule/`.
- `workflow/01-调研/` is for early-stage research artifacts, including this project's code research, external project research, domain/topic pre-research, and experience retrospectives. Files in this directory should also keep chronological numbering such as `01-`, `02-`.
- `workflow/02-设计/` is for higher-level design artifacts, including architecture design, product/page design, data model design, technology-stack selection, test design, and acceptance criteria.
- Execution planning under `workflow/03-执行/` must enforce TDD with `Red -> Green -> Refactor`.
- Testing under `workflow/04-测试/` must require:
  - unit tests first
  - regression tests
  - E2E tests
  - a lightweight verification loop for fast iteration
  - persistent logs
  - reproducible commands
  - traceable case IDs
  - a health report
  - coverage target `>= 85%`
- Prefer mature testing tools already used in the target stack. If none are visible, recommend stable mainstream tools in the generated documents instead of inventing custom frameworks.
- Prefer a lightweight verification rhythm for small and medium-sized projects instead of heavyweight enterprise-only gates.

## Notes

- The script is conservative by default: if `workflow/` already exists, it produces suggestions and writes nothing.
- Only allow writing into an existing `workflow/` when the user explicitly asks for a merge or overwrite.
