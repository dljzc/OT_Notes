---
layout: default
title: PI MQTT Sparkplug
---

# PI MQTT Sparkplug 笔记

**来源**："PI Connector for MQTT Sparkplug 1.0.0 User Guide"（AVEVA，连接器版本 **1.0.0.6**）

## 一句话
PI Connector for MQTT Sparkplug 是一个 **MQTT 客户端**，订阅 Sparkplug 兼容的 MQTT 服务器上的 EoN 节点/设备数据，**单向**发送进 PI System。

## 四角色数据流
```
MQTT Server → Connector（采集）→ PI Connector Relay（转发，AMQP 5671）→ PI AF + Data Archive（持久化）
```
**PI Data Collection Manager (DCM, AMQP 5672)** 集中管理所有配置 — 注册、数据选择、启停都在 DCM。

## 关键参数
| 参数 | 说明 |
|---|---|
| 主题结构 | `namespace/group_id/message_type/node_id/[device_id]` |
| 三级时间戳回退 | metric timestamp → message timestamp → 连接器机器当前时间 |
| 质量码 | 32 = Waiting for initial data / 8 = Not connected |
| 状态标签 | Online / Node Death / Device Death / Server Disconnect / Not Connect |

## 七步配置主线
安装 → 账户和组 → 防火墙（5671/5672 不可配置）→ DCM 注册 → 添加数据源 → **Discovery（15 秒重新发现）** → 选择数据（30 秒刷新）→ 启停 → 验证

## 最大坑
**重新运行 Discovery 会清除数据选择并停止采集**；重启服务或添加/移除数据源也会触发全量重新发现。

## 版本门槛
| 组件 | 最低版本 |
|---|---|
| PI Data Archive | ≥ 3.4.380 |
| PI AF | ≥ 2.7.0 |
| PI Connector Relay | ≥ 2.4.44 |
| PI Data Collection Manager | ≥ 2.4.44（注册需要 2.5+） |

## 端口
| 端口 | 用途 |
|---|---|
| 5671 | PI Connector Relay（AMQP） |
| 5672 | PI Data Collection Manager（AMQP） |
| 5460 | 管理端口（可选） |

## 参考

- [PI Connector for MQTT Sparkplug 用户指南](https://docs.aveva.com/bundle/pi-connector-mqtt-sparkplug/page/pi-connector-mqtt-sparkplug.html)
