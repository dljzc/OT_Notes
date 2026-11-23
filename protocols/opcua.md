# OPC UA 协议笔记

## 概述

OPC UA（Open Platform for Industrial Communications, Unified Architecture）是工业互联网的标准通信协议，由 OPC 基金会制定。OPC UA 基于服务器-客户端架构，定义了标准的服务和接口。

## 核心概念

### 客户端-服务器架构
- **客户端**：发起请求、接收响应（如 SCADA、HMI、MOM 系统）
- **服务器**：提供数据和服务（如 PLC、传感器、设备）

### 标准服务

| 服务 | 说明 |
|---|---|
| Discovery | 发现服务器、端点、接口 |
| Browse | 浏览服务器的节点层级 |
| Read | 读取节点属性（值、质量码、时间戳）|
| Write | 写入节点值 |
| Method Call | 调用服务器方法 |
| Subscription | 订阅节点变化通知 |
| MonitoredItem | 监视项，用于订阅和报警 |

## 节点 ID

节点 ID 格式：`ns=NAMESPACE;id=IDENTIFIER`
- `ns=0`：保留命名空间（标准节点）
- `ns>0`：用户定义命名空间
- `id`：节点标识符（数字或字符串）

## 服务端口

- **默认端口**：4481（TCP/UDP）
- **安全端口**：4483（HTTPS）

## OPC UA 安全

### 安全策略
- **None**：无安全
- **Simple**：基于证书的签名和加密
- **Advanced**：基于证书和策略的完整安全

### 证书管理
- 服务器证书：服务器身份认证
- 客户端证书：客户端身份认证
- 信任策略：哪些证书可信任

### 密钥管理
- 公钥基础设施（PKI）
- 证书吊销列表（CRL）

## 故障排查

| 现象 | 检查项 |
|---|---|
| 连接失败 | 端口 4481 是否开放、防火墙、网络连通性 |
| 证书错误 | 证书有效期、吊销状态、信任策略 |
| 权限错误 | 用户权限、访问控制列表 |
| 数据错误 | 节点 ID、数据类型、质量码 |

## 工具

- **UAM Client**：OPC 基金会的测试客户端
- **OPC UA Explorer**：图形化浏览工具
- **Wireshark**：OPC UA 二进制协议分析
- **Python OPC UA**：`opcua` 库

## 参考

- [OPC UA 官方规范](https://opcfoundation.org/)
- [OPC UA 1.1 规范](https://opcfoundation.org/developers/1-1/)
