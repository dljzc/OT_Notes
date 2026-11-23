# DNP3 协议笔记

## 概述

DNP3（Distributed Network Protocol）是电力行业用于远程监控与控制的标准协议，由 IEC 标准化（IEC 60870-5-104 是相关标准）。DNP3 主要用于电力系统的 SCADA 架构。

## 协议栈

DNP3 采用四层协议栈：

| 层级 | 名称 | 说明 |
|---|---|---|
| 应用层 | Application Layer | 定义应用层功能码（如读取、写入、中断）|
| 数据链路层 | Data Link Layer | 定义帧结构、确认机制、超时重传|
| 传输层 | Transport Layer | 串口、TCP/IP 等传输介质|
| 物理层 | Physical Layer | 电气接口、信号电平|

## 应用层功能码

| 功能码 | 名称 | 说明 |
|---|---|---|
| 0 | Response | 响应 |
| 1 | Request | 请求 |
| 2 | Unsol | 未请求响应 |
| 3 | Read | 读取 |
| 4 | Write | 写入 |
| 5 | Bit Change | 位变化 |
| 6 | Timed Command | 定时命令 |
| 7 | Freeze | 冻结 |
| 8 | Event | 事件 |
| 9 | Event Response | 事件响应 |
| 10 | Multiple Operation | 多操作 |
| 11 | Change Control | 变更控制 |
| 12 | Record Change | 记录变更 |
| 13 | Invalid Function Code | 非法功能码|

## 数据对象

| 对象类型 | 说明 |
|---|---|
| Binary Input | 二进制输入（如开关状态）|
| Binary Output | 二进制输出|
| Analog Input | 模拟输入（如电压、电流）|
| Analog Output | 模拟输出|
| Counter | 计数器|
| Frozen Counter | 冻结计数器|
| Octet String | 八位字符串|
| Time | 时间标签|

## 故障排查

| 现象 | 检查项 |
|---|---|
| 连接超时 | 波特率、数据位、奇偶校验、停止位 |
| 功能码错误 | 从站是否支持该功能码 |
| 数据错误 | 数据对象类型、量纹、偏移量 |
| 确认失败 | 确认超时、重传次数 |

## 参考

- [DNP3 官方规范](https://www.dnp.org/)
- [IEC 60870-5-104](https://webstore.iec.ch/standard/60870-5-104)
