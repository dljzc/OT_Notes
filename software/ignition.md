---
layout: default
title: Inductive Ignition
---

# Inductive Ignition 笔记

**来源**：Inductive Ignition 8.x 官方文档（Ignition 8.1 线），结合个人实践。

## 一句话
Inductive Ignition 是一套跨平台（Windows/Linux）的 SCADA / HMI / MOM / Web 应用开发平台，核心是 **OPC UA Server** + **Ignition Gateway**（工业 4.0 数据流），通过 **Gateway Scope** 和 **Web Scope** 两种模式完成设备连接与数据采集。

## 两大入口模式

| 模式 | 连接方式 | 数据走向 | 适用场景 |
|---|---|---|---|
| **Gateway Scope** | Ignition Gateway 直接连 PLC / 传感器，通过 OPC UA 把现场数据推进 Ignition Gateway 上的 OPC UA 服务器 | Gateway → Ignition 本地 | 单台设备、离线边缘采集、快速连接 |
| **Web Scope** | Ignition Gateway 连设备，数据经 **MQTT / Kafka / AMQP** 推到 Ignition Edge Broker，再由 Ignition 本地客户端消费 | Gateway → MQTT/Kafka → Ignition | 大规模、分布式、跨网段、与 IT 系统集成 |

## 核心组件

| 组件 | 作用 | 关键配置 |
|---|---|---|
| **OPC UA Server** | Gateway 上提供 OPC UA 服务，供 Ignition 消费 | 端口 4481（默认）、安全策略、证书 |
| **Ignition Gateway** | 边缘网关，处理设备连接、数据采集、协议转换 | 设备驱动、标签映射、触发器、历史数据 |
| **Ignition Edge Broker** | MQTT/Kafka 代理，实现 Web Scope 数据流 | Broker 配置、主题、安全策略 |
| **Perspective** | Ignition 8.x 的现代 Web UI 框架 | 视图、绑定、脚本、事件 |
| **Alarm Management** | 报警系统 | 报警配置、通知、 escalation |
| **Audit Trail** | 操作审计 | 审计配置、日志、报告 |
| **Tag System** | 标签系统（数据点核心） | UDT（用户定义类型）、文件夹、质量码 |

## 标签系统（核心）

### 标签分类
- **内部标签**：Ignition 内部使用（系统、历史等）
- **外部标签**：连接外部设备（OPC UA、Modbus、数据库等）

### 标签属性
- **值**：当前值
- **质量码**：Good / Bad / Uncertain
- **时间戳**：最后更新时间
- **元数据**：描述、单位、报警阈值等

### UDT（用户定义类型）
- 把重复的标签结构封装为类型
- 实例化时可继承 UDT 的结构
- 支持参数化，便于批量创建相似设备的标签

## OPC UA 连接

### Gateway Scope（直接连接）
```
1. 创建 OPC UA 服务器连接
   - 端口：4481（Ignition Gateway 默认 OPC UA 端口）
   - 安全：None / 简单 / 高级（证书、策略）
2. 浏览 OPC UA 服务器层级
   - 文件夹 → 文件夹 → 变量节点
3. 绑定标签
   - 标签名 → OPC UA 节点路径
4. 读写测试
   - 读标签值，确认连通性
```

### Web Scope（MQTT/Kafka 推送）
```
1. Ignition Gateway 上配置 MQTT 客户端
   - Broker 地址、用户名、密码
   - 主题：设备数据上行、命令下行
2. 数据格式
   - JSON：{"tag": "Temperature", "value": 25.5, "timestamp": "2024-01-01T00:00:00Z"}
3. Ignition 本地消费
   - MQTT 工具 → 标签绑定
```

## Perspective（现代 Web UI）

### 基本概念
- **视图**：页面/容器
- **容器**：视图、导航、表格、表单等
- **绑定**：标签 ↔ UI 组件（双向绑定）
- **事件**：点击、输入、定时器等
- **脚本**：Python（Jython），在事件/绑定中执行

### 常见组件
| 组件 | 用途 |
|---|---|
| Label / Text Field | 显示/输入文本 |
| Numeric / LED | 数值显示/指示灯 |
| Button | 触发动作 |
| Tank / Gauge | 工业仪表盘 |
| Table | 数据表格 |
| Form | 表单 |
| Navigation | 页面导航 |

## 报警与审计

### 报警系统
- 报警配置：标签绑定、报警阈值、状态变化触发
- 通知：邮件、短信、Webhook
- Escalation：升级通知路径

### 审计日志
- 操作审计：谁、何时、做了什么
- 日志存储：数据库/文件
- 报告生成：审计报表

## 安全与权限

- **用户角色**：Administrator、Operator、Viewer 等
- **资源权限**：标签、视图、报警等资源的访问控制
- **认证方式**：本地数据库、LDAP、Active Directory
- **SSL/TLS**：Gateway 与客户端之间的加密通信

## 维护与故障排查

### 常见问题
| 现象 | 检查项 |
|---|---|
| 标签无法读取 | OPC UA 连接、设备网络、防火墙、证书 |
| Perspective 视图加载失败 | Gateway 服务状态、浏览器兼容性、脚本错误 |
| 报警不触发 | 阈值配置、标签质量码、触发器条件 |
| 历史数据缺失 | 历史记录配置、数据库空间、采集间隔 |

### 日志
- Gateway 日志：`$IGNITION_HOME/gateway/logs/`
- Ignition 本地日志：`$IGNITION_HOME/ignition/logs/`
- 标签日志：Gateway 上的标签提供器日志

## 性能调优

- **标签扫描频率**：根据设备能力设置合理扫描率（不宜过高）
- **历史数据采集**：按需采集，避免过多历史点影响性能
- **视图渲染**：优化 Perspective 视图，减少不必要的绑定和脚本
- **网络带宽**：Web Scope 模式下注意 MQTT/Kafka 带宽消耗

## 参考

- [Inductive Ignition 官方文档](https://docs.inductive.com/manual/ignition/8.1/)
- [Ignition Gateway 文档](https://docs.inductive.com/manual/ignition-gateway/)
- [Perspective 文档](https://docs.inductive.com/manual/perspective/)
