---
layout: default
title: AI Skills
---

# AI Skills

可复用的 AI 提示词模板，直接粘贴给 AI 就能用。

## 使用方式
每个 skill 一个文件，顶部写用途、适用模型、输入输出格式。直接复制使用，不需要额外工具。

## 文件结构
```
skills/
├── prompt-xxxx.md    ← 按功能命名，如 prompt-plc-diagnose.md
└── README.md         ← 本文件
```

## Skill 模板
```markdown
---
layout: default
title: 技能名
---

# 技能名

## 用途
一句话说明这个技能做什么。

## 适用模型
- Claude / GPT / 本地模型

## 使用方法
直接复制下方 prompt 给 AI。

## 输入格式
- 提供什么信息
- 格式要求

## 输出格式
- AI 会返回什么

## 注意事项
- 边界/限制
```

## 已存 Skills
_暂无。添加 skill 后在此更新列表。_