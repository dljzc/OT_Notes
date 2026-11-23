---
layout: default
title: Kepware OPC
---

# Kepware OPC 服务器笔记

## 平台对比

| | KEPServerEX (Windows) | Kepware IoT Platform |
|---|---|---|
| **OS** | Windows only | Linux, Windows, Docker, Kubernetes |
| **Protocol** | OPC DA, OPC AE, OPC UA, Modbus, Ethernet/IP, BACnet, etc. | OPC UA, MQTT, OPC DA, Modbus, HTTP, REST |
| **Config UI** | Windows GUI + XML files | Web UI + REST API + YAML |
| **Tags** | Channel → Device → Tags tree | Resources (Virtual Channels → Virtual Devices) |
| **Data Bridge** | Channel → Tag Bridge → Destination | Data Sharing / MQTT publish |
| **Architecture** | Monolithic Windows service | Microservices, containerized |

## 配置路径

**KEPServerEX (Windows)**:
```
C:\ProgramData\Kepware\KEPServerEX\V4\
├── _system/       - 系统配置 (通道、设备)
├── _tags/         - 标签定义
├── _data/         - 运行时数据、历史
└── KEPServerEX.dat - 主配置文件 (XML)
```

**警告**: 直接编辑 XML 有风险。优先通过 GUI 操作。

## 常用配置操作

### 添加通道 (Channel)
```
Configuration → Channel → Create Channel → 选择协议驱动 (如 OPC UA, Modbus TCP, Ethernet/IP)
```

### 添加设备 (Device)
```
Configuration → Channel → <device-name> → Device → Create Device
```

### 添加标签 (Tag)
```
Configuration → Channel → Device → Tags → Create Tag
```

### 数据桥接 (Tag Bridge)
```
Configuration → Bridge → Tag Bridge
```

输出目标：OPC UA Server、OPC DA Server、SQL Server、Ignition、DDE/CSV

## PowerShell COM 自动化

```powershell
# 连接服务器
$kps = New-Object -ComObject "Kepware.KEPServerEX.V4"
$kps.Connect()

# 列出通道
$kps.GetChannels() | ForEach-Object { $_.Name }

# 读取标签值
$channel = $kps.GetChannel("MyChannel")
$device = $channel.GetDevice("MyDevice")
$tag = $device.GetTag("MyTag")
$val = $tag.Read()   # 返回 Value, Quality, Timestamp

# 写入标签值
$tag.Write("NewValue")

# 断开
$kps.Disconnect()
```

## Docker 启动 (IoT Platform)

```bash
# 基础启动
docker run -d \
  --name kepware \
  -p 51234:51234 \
  -v kepware-data:/opt/kepserver \
  kepesdk/kepsvr:latest

# 带配置挂载
docker run -d \
  --name kepware \
  -p 51234:51234 \
  -v ./config:/opt/kepserver/config \
  kepesdk/kepsvr:latest
```

## Web UI
```
默认地址: https://<host>:51234
```

步骤：
1. 创建 Resource (Virtual Channel)
2. 在 Channel 下创建 Device
3. 在 Device 下创建 Tags
4. 配置 Data Sharing 输出到 MQTT/OPC UA

## REST API

```bash
# 查看资源列表
curl -k https://<host>:51234/api/v1/resources

# 读取标签值
curl -k https://<host>:51234/api/v1/resources/MyChannel/MyDevice/MyTag/value

# 写入标签值
curl -k -X PUT https://<host>:51234/api/v1/resources/MyChannel/MyDevice/MyTag/value \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '"NewValue"'
```

## 数据类型映射

| 协议类型 | Kepware Datatype | Python/通用类型 |
|----------|-----------------|-----------------|
| Modbus/OPC DA | Int16/Int32 | int |
| Modbus/OPC DA | Float32/Float64 | float |
| Modbus/OPC DA | Bool | bool |
| OPC UA | String | str |
| OPC UA | ByteString | bytes |

## 性能建议

- **Scan Rate**: 不要设置过低 (<100ms 可能影响性能)
- **Tag 数量**: 单通道建议 <10,000 个活跃标签
- **网络**: 使用专用 VLAN 隔离工业流量
- **备份**: 定期导出配置文件 (Export 按钮)

## 安全建议

- OPC UA: 启用 Certificate 验证 (Security Mode: SignAndEncrypt)
- MQTT: 启用 TLS + 用户名/密码
- Web UI: 更改默认端口，启用 HTTPS
- 网络: 限制仅允许受信任 IP 访问

## 常见问题排查

| 问题 | 排查步骤 |
|------|----------|
| 设备 Offline | Test-NetConnection <IP>；确认协议参数；检查防火墙 |
| 标签 Bad Quality | 检查地址映射；确认数据类型；查看驱动日志 |
| 连接超时 | 增加 Timeout；减少重试间隔；检查网络延迟 |
| 服务无法启动 | netstat -ano | findstr :<port>；确认 .NET 版本 |
| COM 调用失败 | 以管理员运行 PowerShell；确认 Kepware 服务运行中 |

## 日志位置

```
C:\ProgramData\Kepware\KEPServerEX\V4\_logs\
├── KepwareServer.log
├── <Channel>.log
└── <Device>.log
```

## 快速排查流程图

```
标签不更新?
├── 检查设备状态: Good/OFFLINE?
│   ├── OFFLINE → 检查网络连接、地址配置、防火墙
│   └── Good → 继续
├── 检查标签质量码: Good/Bad/Uncertain?
│   ├── Bad → 检查地址映射、数据类型、寄存器范围
│   ├── Uncertain → 检查校准、工程单位转换
│   └── Good → 标签在更新
├── 检查 Scan Rate: 是否过低?
├── 检查驱动日志: 是否有错误?
└── 检查数据桥接: 目的地是否可达?
```

## 参考

- KEPServerEX 文档: https://support.kepware.com
- Kepware IoT Platform 文档: https://learn.microsoft.com/en-us/azure/iot-hub/
- OPC Foundation: https://opcfoundation.org

## 控制脚本

详见 `scripts/` 目录下的 PowerShell 和 Python 脚本。
