---
layout: default
title: AVEVA PI
---

# AVEVA PI 笔记

## 概述
AVEVA PI System 是工业数据 historian 平台，用于采集、存储和分析时间序列工业数据。

## 核心组件
| 组件 | 说明 |
|---|---|
| PI Server | 数据核心，存储和分析时间序列数据 |
| PI AF (Asset Framework) | 基于资产的建模框架 |
| PI Web API | RESTful API，访问 PI 数据 |
| PI SDK / PI Point | 传统 SDK 访问方式 |
| PI Tags | 数据点（PI Points） |
| PI ACE | Analytic Continuous Expression，在线计算 |
| PI Datalink | Excel 插件，直接访问 PI 数据 |
| PI Vision | 仪表板可视化 |

## 常用操作
- **查询数据**：`piwebapi/streams/{streamid}/records?start=&end=&count=...`
- **资产树查询**：`piwebapi/assetdatabases/{dbid}/assetcontainers`
- **创建 PI Point**：`piwebapi/pointlists/{listid}/points`
- **订阅数据**：WSAP / MQTT Bridge

## 常见问题
- 连接超时：检查 PI Web API 服务是否运行、防火墙端口
- 权限问题：Windows 认证、Kerberos 配置
- 数据缺失：检查采集通道、网络采集器、ODX 驱动

## 参考链接
- [AVEVA PI Web API 文档](https://developer.aveva.com/piserver-apis/piserver/piserver-api-reference/)
- [OSIsoft 知识库](https://techsupport.aveva.com/)
