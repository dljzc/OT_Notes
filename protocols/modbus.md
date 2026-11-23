# Modbus 协议笔记

## 概述

Modbus 是一种开放的工业通信协议，由 Modicon 公司（现 Schneider Electric）于 1979 年开发，广泛用于工业自动化领域。

## 三种实现形式

### Modbus RTU
- **传输介质**：串口（RS-232/RS-485）
- **编码方式**：二进制
- **校验方式**：CRC16
- **帧结构**：
  - Slave Addr (1 byte)
  - Function Code (1 byte)
  - Data (N bytes)
  - CRC (2 bytes)

### Modbus ASCII
- **传输介质**：串口
- **编码方式**：ASCII（每个 8 位字符用 2 个 ASCII 字符表示）
- **校验方式**：LRC
- **帧结构**：以 `:` 开头，以 `CRLF` 结尾

### Modbus TCP
- **传输介质**：以太网（TCP/IP）
- **帧结构**：MBAP 头 + PDU
  - MBAP 头（4 字节）：事务标识符（2 字节）、协议标识符（2 字节）、长度（2 字节）、单元地址（1 字节）
  - PDU：功能码（1 字节）+ 数据

## 功能码分类

| 功能码 | 名称 | 说明 |
|---|---|---|
| 01 (0x01) | Read Coil Status | 读线圈状态 |
| 02 (0x02) | Read Discrete Inputs | 读离散输入 |
| 03 (0x03) | Read Holding Registers | 读保持寄存器 |
| 04 (0x04) | Read Input Registers | 读输入寄存器 |
| 05 (0x05) | Force Single Coil | 置位单个线圈 |
| 06 (0x06) | Preset Single Register | 预置单个寄存器 |
| 15 (0x0F) | Force Multiple Coils | 置位多个线圈 |
| 16 (0x10) | Preset Multiple Registers | 预置多个寄存器 |
| 22 (0x16) | Masking Register | 掩码寄存器 |
| 23 (0x17) | Read/Write Multiple Registers | 读写多个寄存器 |
| 100 (0x64) | Read/Write Device Identification | 读写设备标识 |

## 异常码

| 异常码 | 名称 | 说明 |
|---|---|---|
| 01 (0x01) | ILLEGAL FUNCTION | 非法功能码 |
| 02 (0x02) | ILLEGAL DATA ADDRESS | 非法数据地址 |
| 03 (0x03) | ILLEGAL DATA VALUE | 非法数据值 |
| 04 (0x04) | SLAVE DEVICE FAILURE | 从站设备故障 |
| 05 (0x05) | ACKNOWLEDGE | 确认 |
| 06 (0x06) | SLAVE DEVICE BUSY | 从站忙 |
| 07 (0x07) | NEGATIVE ACKNOWLEDGE | 否定确认 |
| 08 (0x08) | GENERAL ERROR | 一般错误 |

## 工具与实践

### 常用工具
- **Modbus Poll**：Windows 下的 Modbus 测试工具
- **cmodbus**：C 语言的 Modbus 实现
- **pymodbus**：Python 的 Modbus 库
- **nmbc**：Python 的 Modbus 客户端
- **Wireshark**：Modbus TCP 协议分析

### Python 读写示例
```python
from pymodbus.client import ModbusSerialClient

# RTU 示例
client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
client.connect()
result = client.read_holding_registers(address=0, count=10)
if not result.isError():
    print(result.registers)
client.close()

# TCP 示例
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient(host='192.168.1.100', port=502)
client.connect()
result = client.read_holding_registers(address=0, count=10)
if not result.isError():
    print(result.registers)
client.close()
```

## 故障排查

| 现象 | 检查项 |
|---|---|
| 通信超时 | 波特率、数据位、奇偶校验、停止位是否一致 |
| 异常码 02 | 寄存器地址范围是否正确 |
| 异常码 03 | 写入的值是否在允许范围内 |
| 数据错误 | 字节序（Big Endian/Little Endian）、数据类型转换 |
| TCP 连接失败 | IP 端口、防火墙、从站是否支持 TCP |

## 参考

- [Modbus 官方文档](https://www.modbus.org/)
- [Modbus 组织规范](https://www.modbus.org/docs/DOC002)
