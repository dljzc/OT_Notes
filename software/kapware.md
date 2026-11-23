# Kapware 详细笔记

## 一句话
Kapware 是一个全面的工业 IoT 平台，提供 MES（制造执行系统）、SCADA、报警管理、历史数据、分析与可视化，支持 OPC UA、MQTT、HTTP 等多种协议，面向制造业数字化转型。

## 核心模块

| 模块 | 作用 | 说明 |
|---|---|---|
| MES | 制造执行系统，管理生产工单、状态、质量 | 工单管理、状态跟踪、质量检测 |
| SCADA | 监控数据采集与可视化 | 实时显示、历史趋势、报警 |
| 报警管理 | 报警系统，支持 escalation 与通知 | 报警配置、通知路径、升级 |
| 历史数据 | 时间序列数据库，支持高频采集 | 数据存储、查询、分析 |
| 分析工具 | 数据分析与报告 | 趋势分析、统计报告、预测 |
| 可视化 | Web 仪表盘与报表 | 自定义仪表盘、移动端支持 |

## 协议支持

### OPC UA

- 客户端与服务器支持
- 支持标准 OPC UA 1.02/1.03
- 支持安全策略与证书
- 端口 4481（默认）

### MQTT

- 客户端与 Broker 支持
- 支持 QoS 0/1/2
- 支持会话保持与遗嘱
- 端口 1883（默认）

### HTTP/REST

- RESTful API，支持 JSON 格式
- 支持认证与授权
- 支持 Webhook
- 端口 8080/443（默认）

### 其他

- Modbus、Profibus、Ethernet/IP 等现场总线
- 数据库（SQL Server、Oracle、MySQL 等）

## 部署方式

### Windows 部署（传统）

1. 安装 Kapware 服务器
2. 配置数据库（SQL Server 等）
3. 配置网络与安全
4. 启动服务
5. 配置标签和数据源
6. 配置报警和通知

### Docker 部署（新版）

```bash
# 拉取镜像
docker pull kapware/kapware:latest

# 运行容器
docker run -d --name kapware \
  -p 8080:8080 -p 4481:4481 \
  -v /opt/kapware/data:/data \
  kapware/kapware:latest

# 查看日志
docker logs -f kapware
```

## 标签系统

### 标签定义

- 标签是数据点的逻辑名称
- 支持类型：数值、布尔、字符串、日期等
- 支持属性：单位、描述、报警阈值、历史保留
- 支持层级：文件夹、UDT（用户定义类型）

### 标签绑定

- 绑定外部数据源（OPC UA、Modbus、数据库等）
- 绑定内部计算（公式、逻辑）
- 支持触发器与事件

### 示例

```json
{
  "tags": [
    {
      "name": "Temperature",
      "type": "float",
      "source": "opcua://opcua.server:4481/ns=2;i=1001",
      "unit": "°C",
      "alarmHigh": 80.0,
      "alarmLow": 20.0
    },
    {
      "name": "Pressure",
      "type": "float",
      "source": "opcua://opcua.server:4481/ns=2;i=1002",
      "unit": "bar",
      "alarmHigh": 10.0,
      "alarmLow": 1.0
    }
  ]
}
```

## 报警与通知

### 报警配置

- **阈值报警**：基于标签值的阈值判断
- **趋势报警**：基于变化率的判断
- **模式报警**：基于设备模式的判断
- **事件报警**：基于事件触发

### 通知渠道

- 邮件：SMTP 邮件通知
- 短信：短信通知
- Webhook：HTTP 回调通知
- 系统通知：系统内通知
- 事件日志：写入事件日志

### Escalation

- 升级通知路径：操作员 → 主管 → 经理
- 时间延迟：等待一段时间后升级
- 重复通知：多次通知
- 升级条件：阈值持续时间、确认状态

## 历史数据与分析

### 数据存储

- 支持本地数据库（SQL Server、SQLite 等）
- 支持外部数据库（InfluxDB、TimescaleDB 等）
- 数据保留策略可配置
- 数据压缩支持

### 查询与分析

- 时间范围查询
- 聚合函数（avg/min/max/sum/count/stdev）
- 趋势分析、异常检测
- 报告生成（PDF、Excel、HTML）
- 导出数据（CSV、JSON）

### 示例查询

```sql
-- 查询温度历史数据
SELECT timestamp, value FROM temperature_data
WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-02'
ORDER BY timestamp;

-- 聚合查询
SELECT AVG(value) as avg_temp, MAX(value) as max_temp
FROM temperature_data
WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-02';
```

## 维护与故障排查

### 常见问题

| 现象 | 检查项 |
|---|---|
| 标签无法读取 | 数据源连接、网络、防火墙、标签配置 |
| 报警不触发 | 阈值配置、触发器条件、标签质量码 |
| 历史数据缺失 | 存储配置、保留策略、数据库空间 |
| 仪表盘加载失败 | 服务状态、浏览器兼容性、脚本错误 |
| 报警通知失败 | 邮件服务器、短信网关、Webhook URL |

### 日志

- 服务器日志：Kapware 安装目录下的 logs 文件夹
- 数据库日志：数据库自己的日志
- 应用日志：Kapware 应用日志
- 标签日志：标签提供器日志

## 性能调优

- **标签扫描率**：根据设备能力设置合理扫描率
- **历史数据保留**：配置合理的保留期限，避免磁盘满
- **查询优化**：使用索引，避免全表扫描
- **并发控制**：根据资源调整并发读写
- **数据库优化**：优化查询和索引

## 参考

- [Kapware 官方文档](https://www.kapware.com/support/)
- [Kapware 产品文档](https://www.kapware.com/products/)
