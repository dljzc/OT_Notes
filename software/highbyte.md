---
layout: default
title: Highbyte
---

# Highbyte 笔记

## 概述
Highbyte 是工业数据平台，专注于边缘到云的连接、资产建模和数据管道，基于 Ignition 构建。

## 核心组件
| 组件 | 说明 |
|---|---|
| Highbyte Edge | 边缘数据处理和预处理 |
| Highbyte Cloud | 云端数据聚合和分析 |
| Asset Builder | 可视化资产建模工具 |
| Data Pipeline | 数据管道配置（源 → 转换 → 目标） |
| OPC UA Client | 从设备采集数据 |
| MQTT Client | 发布数据到 MQTT Broker |

## 典型架构
```
设备/PLC → OPC UA/MQTT → Highbyte Edge (预处理) → Cloud (聚合/分析)
```

## 常用配置
- **资产建模**：在 Asset Builder 中定义资产层级
- **数据管道**：在 Pipeline 中配置源和目标
- **自定义脚本**：在 Transformation 中写 JavaScript/Python

## 常见问题
- 连接失败：检查 OPC UA 服务器地址、端口、证书
- 数据延迟：检查边缘到云网络、数据管道配置
- 许可证：检查 Edge 和 Cloud 的授权状态

## 参考链接
- [Highbyte 文档](https://docs.highbyte.com/)
