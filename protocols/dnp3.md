---
layout: default
title: DNP3 协议分析
---

# DNP3 协议分析

## 报文结构
- **头部**: Start(0xC0), Addr, Len, Ctrl, Send/Recv Seq
- **数据块**: 对象头 (Class/Prefix), 数据值
- **对象组**: 010 (Binary Inputs), 012 (Analog Inputs), 030 (Binary Outputs)

## 抓包分析
- 抓包工具: Wireshark 过滤器 `tcp.port == 20000` 或 `dnp3`
- 解析: Request / Response / Unsolicited Response
- 异常: Timeout / Invalid CRC

## 常见问题
- 同步失败: 检查 CSE (Class Send Event) / CBE (Class Bit Event)
- 数据异常: 检查点表配置、覆盖范围

> 参考: DNP3.org 规范
