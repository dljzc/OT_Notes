---
layout: default
title: Canary
---

# Canary 笔记

**来源**：Canary 官方文档（Canary 1.x/2.x），结合个人实践。

## 一句话
Canary 是一个轻量级的时间序列数据库（TSDB），专为工业 IoT 场景设计，支持高频数据采集、存储、查询与可视化，提供 HTTP API、MQTT 支持与多种数据源接口。

## 核心特性

- **时间序列数据库**：高性能写入与查询，适合工业传感器数据
- **HTTP API**：RESTful 接口，方便集成
- **MQTT 支持**：直接订阅/发布 MQTT 消息
- **数据源**：支持 OPC UA、Modbus、MQTT、HTTP 等多种数据源
- **可视化**：内置仪表盘与图表
- **报警**：基于阈值的报警与通知
- **历史数据**：支持数据保留与归档

## 部署方式

### Docker 部署
```bash
# 拉取镜像
docker pull canary/canary:latest

# 运行容器
docker run -d --name canary \
  -p 8080:8080 -p 1883:1883 \
  -v /opt/canary/data:/data \
  canary/canary:latest

# 查看日志
docker logs -f canary
```

### 配置文件
- 主配置：`/data/config.yaml` 或 `config.json`
- 数据源配置：`/data/datasources/`
- 标签配置：`/data/tags/`
- 历史数据：`/data/storage/`

## 数据模型

### 数据点结构
```json
{
  "tag": "Temperature",
  "value": 25.5,
  "timestamp": "2024-01-01T00:00:00Z",
  "quality": "Good",
  "metadata": {
    "unit": "°C",
    "source": "PLC-01"
  }
}
```

### 标签系统
- 标签是数据的逻辑名称
- 支持层级结构（如 `Machine.Temperature`）
- 支持标签属性（单位、描述、报警阈值等）

## 数据采集

### HTTP API 写入
```bash
curl -X POST http://localhost:8080/api/data \
  -H "Content-Type: application/json" \
  -d '[{"tag":"Temperature","value":25.5,"timestamp":"2024-01-01T00:00:00Z"}]'
```

### MQTT 订阅
- 主题：`canary/+/write`（写入数据）
- 格式：JSON，同 HTTP API 格式

### 外部数据源
- OPC UA：连接 OPC UA 服务器，读取标签
- Modbus：连接 Modbus 设备，读取寄存器
- MQTT：订阅外部 MQTT 主题
- HTTP：调用外部 HTTP API

## 查询与分析

### HTTP API 查询
| 方法 | 路径 | 作用 |
|---|---|---|
| GET | /api/tags | 列出标签 |
| GET | /api/tags/{name}/data | 查询标签历史数据 |
| GET | /api/query | 复杂查询（时间范围、聚合等） |
| GET | /api/stats | 统计信息 |

### 查询参数
- `start` / `end`：时间范围
- `aggregate`：聚合函数（avg/min/max/sum/count）
- `resolution`：数据分辨率
- `limit`：返回条数限制

## 存储与性能

### 存储策略
- **数据保留**：配置保留期限（如 30 天、1 年）
- **数据归档**：将历史数据移至归档存储
- **数据压缩**：对历史数据进行压缩存储

### 性能调优
- **写入批次**：批量写入提高吞吐量
- **索引优化**：按时间索引，提高查询速度
- **缓存策略**：热数据内存缓存，冷数据磁盘存储
- **并发控制**：根据资源调整写入并发

## 维护与故障排查

### 常见问题
| 现象 | 检查项 |
|---|---|
| 写入失败 | 网络连通性、API 凭证、存储空间 |
| 查询慢 | 索引状态、时间范围、数据量 |
| 数据丢失 | 保留策略、存储故障、网络中断 |
| 标签不更新 | 数据源连接、扫描频率、标签配置 |

### 日志
- 容器日志：`docker logs canary`
- 应用日志：`/data/logs/`
- 访问日志：HTTP 访问日志

## 参考

- [Canary 官方文档](https://www.canarydb.com/docs/)
- [Canary GitHub](https://github.com/canarydb/canary)
