---
layout: default
title: OPC UA 协议分析
---

# OPC UA 协议分析

## 架构
- **信息模型**: Object / Variable / Method / ReferenceType
- **通信模型**: Publisher-Subscriber (UDP) / Client-Server (TCP)
- **安全**: Certificate-based (Basic256Sha256/Aes128_Sha256_RsaPss)

## 抓包分析
- 抓包工具: Wireshark 过滤器 `opc.tcp`
- 解析: OpenSecureChannel / CreateSession / Read / Write
- 异常: BadSecurityRejectedNoCertificates / BadCertificateTimeInvalid

## 常见问题
- 证书问题: 检查 CA 签名、证书有效期
- 访问权限: 检查 UserToken / ReadWrite rights

> 参考: OPC Foundation 规范
