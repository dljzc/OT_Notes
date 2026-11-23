---
layout: default
title: Kapware
---

# Kapware

## 概述
Kapware 是数据采集和边缘计算平台，支持多种工业协议，提供 OPC 服务器功能。

## 核心组件
| 组件 | 说明 |
|---|---|
| Kapware Server | 核心服务器，协议采集和数据处理 |
| OPC 服务器 | 支持 OPC DA / OPC UA / OPC HDA |
| 协议驱动 | Siemens S7、Modbus、OPC UA Client、BACnet 等 |
| 数据桥接 | 边缘到云数据推送（MQTT、Web API） |
| 数据记录 | 时间序列数据存储（.kdj 格式） |

## 支持的协议
| 协议 | 说明 |
|---|---|
| Siemens S7 | S7-200/300/400/1200/1500 |
| Modbus TCP/RTU | Modbus 主站/从站 |
| OPC UA Client | 作为 OPC UA 客户端连接服务器 |
| BACnet | HVAC 协议 |
| Fanuc FOCAS | 发那科 CNC 连接 |
| Allen-Bradley | EtherNet/IP |

## 常见问题
- 驱动加载失败：检查协议驱动是否安装
- 数据采集中断：检查 PLC 连接状态、网络
- 数据桥接失败：检查 MQTT/Web API 配置

## 参考链接
- [Kapware 官方文档](https://www.kineticautomation.com/kapware)
