# Plugins

这是一个用于集中维护 Codex 插件的仓库。

当前约定：

- 所有插件统一放在 `plugins/<plugin-name>/`
- 每个插件都必须包含 `.codex-plugin/plugin.json`
- 仓库级 marketplace 放在 `.agents/plugins/marketplace.json`

## 当前插件

| 插件 | 说明 |
| --- | --- |
| `workflow-bootstrap` | 初始化一套可复用的 `workflow/` 协作目录，内置规则、TDD 执行模板和测试模板。 |

## 仓库结构

```text
plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── plugins/
│   └── workflow-bootstrap/
│       ├── .codex-plugin/
│       ├── scripts/
│       ├── skills/
│       └── tests/
├── .gitignore
├── LICENSE
└── README.md
```

## 安装方式

### 方式 1：按单个插件安装到本地 Home marketplace

适合“只安装某一个插件”的场景。

1. 把目标插件目录复制到本机的 `~/plugins/<plugin-name>/`
2. 在 `~/.agents/plugins/marketplace.json` 中加入对应入口

`workflow-bootstrap` 的示例条目：

```json
{
  "name": "workflow-bootstrap",
  "source": {
    "source": "local",
    "path": "./plugins/workflow-bootstrap"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

### 方式 2：直接把这个仓库当作插件集合仓库使用

适合统一维护多个插件。

1. clone 本仓库
2. 使用仓库内的 `.agents/plugins/marketplace.json`
3. 后续新增插件时，只需要继续往 `plugins/` 目录下添加，并同步更新 marketplace
