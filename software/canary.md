---
layout: default
title: Canary
---

# Canary 笔记

## 概述
Canary 是工业数据枢纽平台，专注于工业数据集成和 MCP 服务，提供从 OT 到 IT 的连接。

## 核心组件
| 组件 | 说明 |
|---|---|
| Canary Hub | 数据集成核心，OPC UA/Plc4x 连接 |
| MCP Server | MCP（Model Context Protocol）服务，为 AI 提供数据访问 |
| Asset Model | 资产建模，设备 → 资产 → 数据点 |
| Data Bridge | 数据桥接（边缘到云） |

## MCP 集成
- Canary 提供 MCP 接口，允许 AI 助手直接访问工业数据
- 通过 MCP 查询实时数据、历史数据、资产模型
- 支持 MCP 协议的工具调用（tools/read、tools/write）

## 典型架构
```
PLC/SCADA → OPC UA/Plc4x → Canary Hub → MCP → AI 助手
```

## 常见问题
- MCP 连接失败：检查 MCP 端口、防火墙
- 数据查询延迟：检查 PLC 响应时间、轮询频率
- 协议兼容性：检查 OPC UA 服务器版本、Plc4x 驱动支持

## 参考链接
- [Canary GitHub](https://github.com/canary-ecad/eplan-mcp)（注意：此 repo 为 EPLAN MCP，Canary 数据平台需参考其官方文档）
