# Inductive Ignition 详细笔记

## 一句话
Inductive Ignition 是一套跨平台（Windows/Linux）的 SCADA / HMI / MOM / Web 应用开发平台，核心是 **OPC UA Server** + **Ignition Gateway**（工业 4.0 数据流），通过 **Gateway Scope** 和 **Web Scope** 两种模式完成设备连接与数据采集。

## 两大入口模式

### Gateway Scope
Gateway Scope 通过 Ignition Gateway 直接连接现场设备（PLC、传感器等），通过 OPC UA 把现场数据推进 Ignition Gateway 上的 OPC UA 服务器，然后由 Ignition 本地客户端消费。

```
Gateway Scope 数据流：
  现场设备 → OPC UA → Ignition Gateway → Ignition OPC UA 客户端 → Ignition 本地
```

**适用场景**：
- 单台设备、离线边缘采集
- 快速连接、简单部署
- 不需要分布式数据流的场景

### Web Scope
Web Scope 通过 Ignition Gateway 连接设备，数据经 MQTT / Kafka / AMQP 推到 Ignition Edge Broker，再由 Ignition 本地客户端消费。

```
Web Scope 数据流：
  现场设备 → Ignition Gateway → MQTT/Kafka → Ignition Edge Broker → Ignition 本地
```

**适用场景**：
- 大规模、分布式部署
- 跨网段数据流
- 与 IT 系统集成
- 需要数据同步到云端或数据库

## 核心组件

### OPC UA Server
Ignition Gateway 上提供 OPC UA 服务器，供 Ignition 消费。

- **默认端口**：4481（TCP/UDP）
- **安全策略**：None / 简单 / 高级（证书、策略）
- **节点结构**：文件夹、变量节点、方法

### Ignition Gateway
边缘网关，处理设备连接、数据采集、协议转换。

- **设备驱动**：支持多种工业设备驱动（PLC、传感器、仪表等）
- **标签映射**：将设备数据映射为 Ignition 标签
- **触发器**：基于条件触发数据采集或动作
- **历史数据**：将采集的数据存储到数据库

### Ignition Edge Broker
MQTT/Kafka 代理，实现 Web Scope 数据流。

- **Broker 配置**：MQTT/Kafka 服务器地址、认证、主题
- **数据格式**：JSON、二进制等
- **安全策略**：TLS、认证、授权

### Perspective（现代 Web UI）
Ignition 8.x 的现代 Web UI 框架，基于 React 和 Web 技术。

- **视图**：页面/容器，用于组织 UI
- **容器**：视图、导航、表格、表单等 UI 组件
- **绑定**：标签 ↔ UI 组件（双向绑定）
- **事件**：点击、输入、定时器等交互事件
- **脚本**：Python（Jython），在事件/绑定中执行

### Alarm Management
报警系统，支持报警配置、通知、升级。

- **报警配置**：标签绑定、报警阈值、状态变化触发
- **通知**：邮件、短信、Webhook
- **Escalation**：升级通知路径（操作员 → 主管 → 经理）

### Audit Trail
操作审计，记录谁、何时、做了什么。

- **审计配置**：哪些操作需要审计
- **日志存储**：数据库或文件
- **报告生成**：审计报表

### Tag System
标签系统是 Ignition 的数据点核心。

- **内部标签**：Ignition 内部使用（系统、历史等）
- **外部标签**：连接外部设备（OPC UA、Modbus、数据库等）
- **UDT（用户定义类型）**：把重复的标签结构封装为类型
- **质量码**：Good / Bad / Uncertain
- **时间戳**：最后更新时间

## 标签系统详细

### 标签分类

| 类型 | 说明 |
|---|---|
| 内部标签 | Ignition 内部使用（系统、历史等） |
| 外部标签 | 连接外部设备（OPC UA、Modbus、数据库等） |

### 标签属性

| 属性 | 说明 |
|---|---|
| 值 | 当前值 |
| 质量码 | Good / Bad / Uncertain |
| 时间戳 | 最后更新时间 |
| 元数据 | 描述、单位、报警阈值等 |

### UDT（用户定义类型）

UDT 把重复的标签结构封装为类型，实例化时可继承 UDT 的结构，支持参数化，便于批量创建相似设备的标签。

**示例**：
```
UDT: Motor
  - Start (Boolean)
  - Stop (Boolean)
  - Speed (Float)
  - Status (Integer)

Instance: Motor_01
  - Start: false
  - Stop: false
  - Speed: 0.0
  - Status: 0
```

## OPC UA 连接详细

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

## Perspective 详细

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

### 脚本示例

```python
# 点击按钮事件脚本
import system

# 读取标签值
temp = system.tag.readBlocking(['[Tag]Temperature'])[0].value

# 写入标签值
system.tag.writeBlocking(['[Tag]Temperature'], [25.5])

# 触发报警
system.alarm.activate('High Temp')
```

## 报警与审计详细

### 报警系统

- **报警配置**：
  - 标签绑定：绑定到特定标签
  - 报警阈值：高/低阈值
  - 状态变化触发：从 Good 到 Bad 触发

- **通知**：
  - 邮件：SMTP 邮件通知
  - 短信：短信通知
  - Webhook：HTTP 回调通知

- **Escalation**：
  - 升级通知路径：操作员 → 主管 → 经理
  - 时间延迟：等待一段时间后升级
  - 重复通知：多次通知

### 审计日志

- **操作审计**：记录谁、何时、做了什么
- **日志存储**：数据库或文件
- **报告生成**：审计报表
- **审计策略**：哪些操作需要审计

## 安全与权限

### 用户角色

| 角色 | 权限 |
|---|---|
| Administrator | 系统配置、用户管理 |
| Operator | 操作设备、下发命令 |
| Viewer | 只读查看 |
| Engineer | 配置参数、修改程序 |

### 资源权限

- 标签权限：读、写、配置
- 视图权限：查看、编辑
- 报警权限：确认、屏蔽
- 系统权限：全权管理

### 认证方式

- 本地数据库：Ignition 内部用户数据库
- LDAP：LDAP 服务器认证
- Active Directory：AD 认证
- SAML：SAML 单点登录

### SSL/TLS

- Gateway 与客户端之间的加密通信
- 证书管理：服务器证书、客户端证书
- 信任策略：哪些证书可信任

## 维护与故障排查

### 常见问题

| 现象 | 检查项 |
|---|---|
| 标签无法读取 | OPC UA 连接、设备网络、防火墙、证书 |
| Perspective 视图加载失败 | Gateway 服务状态、浏览器兼容性、脚本错误 |
| 报警不触发 | 阈值配置、标签质量码、触发器条件 |
| 历史数据缺失 | 历史记录配置、数据库空间、采集间隔 |
| 证书错误 | 证书有效期、吊销状态、信任策略 |

### 日志

- Gateway 日志：`$IGNITION_HOME/gateway/logs/`
- Ignition 本地日志：`$IGNITION_HOME/ignition/logs/`
- 标签日志：Gateway 上的标签提供器日志
- 历史数据日志：数据库日志

## 性能调优

- **标签扫描频率**：根据设备能力设置合理扫描率（不宜过高）
- **历史数据采集**：按需采集，避免过多历史点影响性能
- **视图渲染**：优化 Perspective 视图，减少不必要的绑定和脚本
- **网络带宽**：Web Scope 模式下注意 MQTT/Kafka 带宽消耗
- **数据库优化**：优化历史数据存储和查询

## 参考

- [Inductive Ignition 官方文档](https://docs.inductive.com/manual/ignition/8.1/)
- [Ignition Gateway 文档](https://docs.inductive.com/manual/ignition-gateway/)
- [Perspective 文档](https://docs.inductive.com/manual/perspective/)
- [OPC UA 官方规范](https://opcfoundation.org/)
