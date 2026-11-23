---
layout: default
title: AVEVA PI
---

# AVEVA PI 笔记

## 八件事的分工（先确认你要做哪件事）

| 你要做的事 | 用什么 | 在哪 |
|---|---|---|
| 读/写位号与 AF 属性的**数据**（实时值、历史值、插值、汇总、事件框架） | **AF SDK**（.NET，进程内） | 本文件 + `scripts/pi.ps1` |
| PI Vision **显示（仪表盘）**的导出/导入、文件夹、访问权限 | **PI Vision REST API**（HTTP + JSON） | `references/pivision-api.md` |
| 给 PI Vision 加**新的符号类型 / 工具面板** | **文件部署**（往安装目录放 `sym-*.js/html/css`），**没有 API** | `references/pivision-extensibility.md` |
| 把 PI ACE 的计算改成自研服务 | **AF SDK** 的 `AFDataCache` + 观察者模式 | `references/afsdk-custom-calculations.md` |
| **批量管点位配置 / 查许可证 / 备份 / 缓冲 / 集合 / 安全** | **官方 `OSIsoft.PowerShell` 模块**（PISMT 自带，227 cmdlet） | 本 skill **未实现**，见 `pi-powershell.md` |
| **把没有现成接口的数据源灌进本地 PI**（自建模板+点位+时序） | **OMF + PI Web API**（HTTP + JSON，`POST /piwebapi/omf`） | 见 `references/aveva-omf-pi-web-api.md` |
| **把数据上云**（CONNECT data services / OMF / Edge Data Store） | **REST / OMF**（云端或边缘，另一套体系） | 见 `references/aveva-cloud-connect.md` |
| **把数据采进 PI**（选 Interface 还是 Connector？缓冲/故障转移/健康点怎么配？） | **PI Interface（UniInt+ICU） / PI Connector（DCM+Relay） / Adapter（OMF）** 三代并存 | 见 `references/aveva-data-collection.md` |
| **在 Excel 看 PI 数据 / 手工录入 / 做合规报表 / 搬 ProcessBook 显示** | **PI DataLink / PI Manual Logger / RtReports / 迁移工具** | 见 `references/aveva-pi-client-tools.md` |

关键区别：

- **PI Vision API 不取数据。** 它只搬运仪表盘定义，读不到任何位号的值。想要数据，回 AF SDK。
- **AF SDK 管不了仪表盘。** 它没有 PI Vision 显示的概念。
- **扩展性没有 API。** 自定义符号是往安装目录拷文件 + 回收应用池。
- **官方 PowerShell 模块 ≠ 本 skill。** 那个模块偏**管理员视角**（点位配置、安全、备份、缓冲、许可证），做**数据读写**时不如 AF SDK 直接。
- **OMF 是反方向。** AF SDK 读写**已有**的点/属性；OMF 是**先建模板和点位、再灌时序值**。
- **云侧不在本 skill 范围内。** CONNECT data services / OMF / Edge Data Store 是另一套体系（HTTP + OAuth 2.0）。
- **"数据怎么进来"是另一个世界。** PI 的数据采集有**三代并存**的技术（Interface / Connector / Adapter），加上 PI System Connector 做 PI→PI 复制。

## 硬性前提（不满足则完全跑不起来）

| 前提 | 说明 |
|---|---|
| 操作系统 | **仅 Windows**。.NET Framework 版 AF SDK 没有 Linux/macOS 版本 |
| 运行时 | 本机已安装 **PI AF Client**（AF SDK 随它分发，不是独立安装包） |
| 程序集 | 必须引用 `AF\PublicAssemblies\4.0\OSIsoft.AFSDK.dll`（程序集版本 `4.0.0.0`，RDA） |
| PowerShell | **Windows PowerShell 5.1（64 位）**，即 `powershell.exe`。**不要用 `pwsh`** |
| 网络与身份 | 能连到 AF Server / PI Data Archive；域账号或已配置的 PI 映射账号 |
| 权限 | PI Identity + AF 安全配置，读写权限分离 |

## 快速开始

```powershell
# 1. 环境自检
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/pi.ps1 doctor

# 2. 列出可访问的 AF Server 与数据库
... -File scripts/pi.ps1 systems
... -File scripts/pi.ps1 databases -System PIAF01

# 3. 当前值（快照），支持多个位号
... -File scripts/pi.ps1 snapshot -Tags "CDT158,SINUSOID"

# 4. 历史原始值（PI 时间语法）
... -File scripts/pi.ps1 recorded -Tags "CDT158" -Start "*-8h" -End "*" -MaxCount 500

# 5. 等间隔插值 / 趋势压缩 / 汇总
... -File scripts/pi.ps1 interpolated -Tags "CDT158" -Start "t" -End "*" -Interval "15m"
... -File scripts/pi.ps1 plot         -Tags "CDT158" -Start "t" -End "*" -Intervals 200
... -File scripts/pi.ps1 summary      -Tags "CDT158" -Start "t" -End "*" -Summary Average,Minimum,Maximum,PercentGood

# 6. AF 侧：按路径取属性、浏览元素、搜事件框架
... -File scripts/pi.ps1 attributes  -Path "\\PIAF01\NuGreen\Plant1\Reactor01"
... -File scripts/pi.ps1 elements    -Path "\\PIAF01\NuGreen\Plant1"
... -File scripts/pi.ps1 eventframes -System PIAF01 -Database NuGreen -Start "*-7d" -End "*"

# 7. 模糊找位号 / 元素
... -File scripts/pi.ps1 search -Kind points   -Query "CDT*" -Server PIDATA01
... -File scripts/pi.ps1 search -Kind elements -Query "template:'Compressor'" -System PIAF01 -Database NuGreen
```

所有命令默认输出 **JSON**，加 `-Format table` 可切换成人类可读表格。

## 命令一览

| 命令 | 作用 | 关键参数 |
|---|---|---|
| `doctor` | 环境自检与诊断 | — |
| `systems` / `databases` | 列出 AF Server / AF 数据库 | `-System` |
| `search` | 模糊查找位号或元素 | `-Kind points|elements`、`-Query` |
| `snapshot` | 当前值（多点批量） | `-Tags` 或 `-Path` |
| `recorded` | 原始历史值 | `-Start -End -MaxCount -Boundary` |
| `interpolated` | 等间隔插值 | `-Interval`（如 `15m`、`1h`） |
| `plot` | 趋势图压缩数据 | `-Intervals` |
| `summary` | 区间汇总 | `-Summary Average,Minimum,Maximum,StdDev,Total,Count,PercentGood,Range` |
| `elements` / `attributes` | 浏览 AF 层级 | `-Path` |
| `eventframes` | 事件框架查询 | `-Start -End -Query -Mode -InProgress -LongerThan` |
| `write` | **写值（需显式授权）** | 见 `scripts/pi-write.ps1` |

## 配置

优先级：**命令行参数 > 环境变量 > `assets/config.json`**。

```powershell
$env:PI_AF_SYSTEM = "PIAF01"        # 默认 AF Server
$env:PI_DATA_SERVER = "PIDATA01"    # 默认 PI Data Archive
$env:PI_AF_DATABASE = "NuGreen"     # 默认 AF 数据库
$env:PI_AFSDK_PATH  = "C:\Program Files\PIPC\AF\PublicAssemblies\4.0\OSIsoft.AFSDK.dll"
```

## 必须记住的语义

- **PI Point vs AF Attribute**：`-Tags` 走 Data Archive 裸点，只有值和单位；`-Path` 走 AF，带资产上下文、模板、分析计算值。
- **时间语法**：`*`（现在）、`t`（今日零点）、`y`（昨日零点）、`*-1h`、`*-7d`。不带时区的时间按服务器时区解释。
- **质量码必须看**：每条值都带 `quality` / `isGood`。`Questionable` 和 `Bad` 的值不能当有效数据用。
- **工程单位**：`uom` 字段是原始工程单位。做跨点计算前先确认单位一致。
- **取数粒度**：原始历史可能极密。超过几千点就用 `interpolated` / `plot` / `summary`，别硬拉 `recorded`。
- **性能**：多点取数已走 `AFAttributeList` / `PIPointList` 批量路径，不要改成循环单点调用。

## 写操作红线

写入是**独立脚本 + 显式授权**，默认 `-DryRun`：

```powershell
# 先干跑看将要写入什么
... -File scripts/pi-write.ps1 -Tags "CDT158" -Value 42 -Timestamp "*" -DryRun
# 确认后再实际写
... -File scripts/pi-write.ps1 -Tags "CDT158" -Value 42 -Timestamp "*" -AllowWrite
```

- PI 是**生产历史库**，写入不可逆，且可能影响下游分析、报表、控制回路。
- 写入前必须确认：**位号、值、时间戳、更新模式**。
- 默认 `AFUpdateOption.Replace`（同时间戳覆盖）。`Insert` 会报重复，`Remove` 是删除。

## 排错速查

| 现象 | 首查 |
|---|---|
| `无法加载文件或程序集 OSIsoft.AFSDK` | 没装 PI AF Client，或用 `pwsh` 跑了。跑 `doctor` |
| `Class not registered` / 32/64 位不匹配 | 用 64 位 `powershell.exe`；确认 `PIPC` 路径下程序集位数 |
| 脚本报一堆 `Unexpected token` 语法错误 | **编码问题**：脚本被改成了无 BOM 的 UTF-8。跑 `scripts/fix-encoding.ps1` |
| 连接超时 | 防火墙 5450（PI Data Archive）/ 5457、5459（AF） |
| 认证失败 | 账号是否有 PI Identity 映射；Kerberos 双跳问题 |
| 位号找不到 | 大小写、拼写；用 `search -Kind points` 模糊查 |
| 取数超时 | 缩小时间范围，或改用 `interpolated` / `plot` / `summary` |

## 参考

- [AVEVA PI 官方文档](https://docs.aveva.com/bundle/pi-server-system-manual-2024-r2/page/pi-server-system-manual-2024-r2.html)
- [AF SDK 开发文档](https://developer.aveva.com/bundle/af-sdk/page/af-sdk.html)
- [PI Web API 文档](https://developer.aveva.com/bundle/pi-web-api/page/pi-web-api.html)
- [PI Vision 文档](https://docs.aveva.com/bundle/pi-vision/page/pi-vision.html)
