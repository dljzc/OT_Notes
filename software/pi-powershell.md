---
layout: default
title: PI PowerShell (OSIsoft.PowerShell)
---

# PI PowerShell 笔记

`OSIsoft.PowerShell` 是 AVEVA PI 的官方 PowerShell 模块，封装了 PI Data Archive 和 AF 对象模型，覆盖 218 个 cmdlet。

## 硬前提

| 前提 | 说明 |
|---|---|
| 操作系统 | **Windows 仅支持** |
| PowerShell | **Windows PowerShell 5.1（64 位）**，即 `powershell.exe`。**不要用 `pwsh`** |
| 安装方式 | 安装 **PI System Management Tools (PISMT) 2015+**，勾选 "PowerShell Tools for the PI System" |
| 加载 | 通常自动加载；找不到则运行 `Import-Module OSIsoft.PowerShell` |

## 快速开始（5 步）

```powershell
Import-Module OSIsoft.PowerShell

# 连接
$piCon = Connect-PIDataArchive -PIDataArchiveMachineName "PISRV01" -AuthenticationMethod Windows
$afCon = Connect-AFServer        -AFServerMachineName "AFSRV01"

# 获取计数
(Get-PIPoint -Name "CDT*" -AllAttributes -Connection $piCon).Count
(Get-AFDatabase -Connection $afCon).Name

Disconnect-PIDataArchive ; Disconnect-AFServer
```

## cmdlet 分组（218 个）

- **AF 侧**：88 个（`AF*`）— AF 数据库、元素、模板、属性、事件框架、安全、XML 导出
- **PI Data Archive 侧**：128 个（`PI*`）— 点位管理、历史值查询、缓冲健康、许可证、集合
- **其他**：2 个

## 核心分类

| 目录 | 内容 |
|---|---|
| ch01 | 安装、连接、自检（`Connect-*`、`Get-*ConnectionConfiguration`） |
| ch02 | PI 点位管理（查询/创建/修改/重命名/删除） |
| ch03 | 读数据（快照/历史/插值/汇总/表达式） |
| ch04 | AF 资产框架（Server/DB/Element/Template/Attribute/EventFrame/Security/XML） |
| ch05 | 写值/删除/值操作（`Add-PIValue`/`Remove-PIValue`/属性写） |
| ch06 | 归档、备份、恢复、移位 |
| ch07 | 缓冲健康、点位错误、连接统计、线程、消息 |
| ch08 | 安全身份、映射、Trust、用户组、许可证、集合、调优参数 |
| ch09 | 全部 218 个 cmdlet 完整索引 |

## 红线

- 写值/删除值/删除点位/删除 AF 对象影响生产；**先 `-WhatIf` 确认再执行**
- 始终检查质量码（`IsGood`）；Bad/Questionable 值不能当有效数据
- `Get-PIValue` 返回的时间戳都是 UTC，不会自动转换本地时区

## 参考

- [OSIsoft.PowerShell 3.1.1 官方文档](https://docs.aveva.com/bundle/pi-powershell-3.1.1/page/html/N_OSIsoft_PowerShell.htm)
