---
layout: default
title: Ignition
---

# Ignition (Inductive Automation)

## 概述
Ignition 是开源授权的 SCADA/IIoT 平台，包含透视（Perspective）、边缘计算、MQTT 网关。

## 核心组件
| 组件 | 说明 |
|---|---|
| Ignition Gateway | 核心平台，Web 管理界面 |
| Perspective | 基于 Web 的 HMI 系统 |
| Vision | 传统 Java Swing HMI（已逐步淘汰） |
| MQTT Broker | 内置 MQTT，支持 QoS 0/1/2 |
| SQL Bridge | 数据库读写、批量操作 |
| Report Engine | 报告生成 |
| Tags | 标签体系（模拟、数字、批量） |

## 常用操作
- **标签查询**：`system.tag.readBlocking(['[System]Client/...'])`
- **MQTT 发布**：`system.mqtt.publish('broker','topic','payload',retain=False)`
- **SQL 查询**：`system.db.runQuery('SELECT...')`
- **脚本执行**：`system.util.invokeLater()`

## 常见问题
- 端口冲突：8080、8443、18600 被占用
- 许可证问题：检查 license 类型（标准/无限）
- 数据库连接：检查 ODBC/JDBC 驱动、连接池

## 参考链接
- [Ignition 官方文档](https://docs.inductiveautomation.com/display/DOC81/)
- [Ignition 社区](https://forum.automation.com/)
