---
layout: default
title: Highbyte
---

# Highbyte 笔记

**来源**：Highbyte 官方文档（Highbyte 2.3+），结合个人实践。

## 一句话
Highbyte 是一款基于 Linux 容器（Docker）的轻量级工业 IoT 平台，提供 OPC UA 服务器、MQTT 网关、HTTP API、数据采集与可视化，面向工业边缘采集与边缘计算场景。

## 核心组件

| 组件 | 作用 | 说明 |
|---|---|---|
| **OPC UA Server** | 提供 OPC UA 标准服务，供外部客户端（如 Ignition、TIA Portal）读写 | 端口 4481，支持多端点 |
| **MQTT Client/Server** | MQTT 协议通信，支持设备数据上行与命令下行 | 支持 QoS、会话保持 |
| **HTTP API** | RESTful 接口，用于配置、监控、数据查询 | 默认端口 8080/8081 |
| **Tag System** | 标签系统，管理数据点、报警、历史 | 支持 UDT 类似结构 |
| **Dashboard** | Web 仪表盘，实时可视化 | 自定义组件、报警显示 |
| **Data Logger** | 历史数据采集与存储 | 支持本地文件、数据库 |

## 部署方式

### Docker 部署（推荐）
```bash
# 拉取镜像
docker pull highbyte/highbyte:latest

# 运行容器
docker run -d --name highbyte \
  -p 8080:8080 -p 4481:4481 \
  -v /opt/highbyte/data:/data \
  highbyte/highbyte:latest

# 查看日志
docker logs -f highbyte
```

### 配置文件
- 主配置：`/data/config.json` 或环境变量
- 标签配置：`/data/tags.json`
- MQTT 配置：环境变量或配置文件
- 历史数据：`/data/logs/`

## OPC UA 服务器

### 标签定义
```json
{
  "tags": [
    {
      "name": "Temperature",
      "type": "float",
      "address": "40001",
      "scanRate": 1000,
      "quality": "Good"
    }
  ]
}
```

### 读写
- 读：`opcua://Highbyte/Server/Tag/Temperature`
- 写：同路径，设置值

## MQTT 网关

### 配置
```json
{
  "mqtt": {
    "broker": "tcp://mqtt.broker:1883",
    "username": "admin",
    "password": "password",
    "topics": {
      "subscribe": ["#"],
      "publish": ["highbyte/+"]
    }
  }
}
```

### 数据格式
- 上行：`{"tag":"Temperature","value":25.5,"timestamp":"2024-01-01T00:00:00Z"}`
- 下行：`{"tag":"Temperature","value":30.0,"command":"write"}`

## HTTP API

### 基础端点
| 方法 | 路径 | 作用 |
|---|---|---|
| GET | /api/tags | 列出所有标签 |
| GET | /api/tags/{name} | 获取标签详情 |
| POST | /api/tags/{name} | 写入标签值 |
| GET | /api/mqtt/status | MQTT 连接状态 |
| GET | /api/system/status | 系统状态 |

### 认证
- 支持 API Key 认证
- 支持 JWT 认证
- 支持基本认证

## 数据采集与存储

### 历史数据
- 支持本地文件存储（CSV/JSONL）
- 支持外部数据库（InfluxDB、TimescaleDB 等）
- 采集间隔可配置

### 数据转发
- 支持 MQTT 转发到外部 Broker
- 支持 HTTP 转发到外部 API
- 支持 Kafka 转发

## 维护与故障排查

### 常见问题
| 现象 | 检查项 |
|---|---|
| OPC UA 连接失败 | 端口 4481 是否开放、防火墙、容器网络 |
| MQTT 无法连接 | Broker 地址、凭证、网络连通性 |
| 标签不更新 | 扫描频率、设备连通性、标签配置 |
| 历史数据缺失 | 存储空间、采集配置、数据库连接 |

### 日志
- 容器日志：`docker logs highbyte`
- 应用日志：`/data/logs/`
- 访问日志：HTTP 访问日志

## 性能调优

- **标签扫描率**：根据设备能力设置，避免过高频率
- **历史数据保留**：配置保留策略，避免磁盘满
- **MQTT 会话**：配置合理的会话保持时间
- **HTTP 并发**：根据容器资源调整并发限制

## 参考

- [Highbyte 官方文档](https://www.highbyte.com/docs/)
- [Highbyte GitHub](https://github.com/highbyte/highbyte)
