---
layout: default
title: OT 安全
---

# OT 安全

## 网络分区
- **Level 0**: 传感器/执行器
- **Level 1**: PLC/RTU
- **Level 2**: HMI/SCADA
- **Level 3**: 工程站/历史库
- **Level 4**: 企业网 (DMZ)
- **Level 5**: ERP/MES

## 加固实践
- 禁用未用端口/服务
- 密码管理: 定期更换、最小权限
- 补丁管理: 测试后再部署
- 网络分段: 防火墙/工业交换机隔离

## 威胁检测
- **IDS**: Zeek / Snort / Suricata
- **NDR**: 基线分析、异常流量
- **日志**: Syslog / SIEM 集成

## 事件响应
- **预案**: 隔离受影响区域、切换备用系统
- **取证**: 抓包保存、日志取证
- **恢复**: 从备份恢复、验证后上线

> 参考: ISA/IEC 62443 / NIST SP 800-82
