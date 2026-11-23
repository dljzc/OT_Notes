---
layout: default
title: PI JDBC Batch
---

# PI JDBC Batch 笔记

**来源**：OSIsoft vCampus 白皮书 "Batch Execution in PI JDBC 2010 R2" (v1.1.0.241)

## 何时使用

| 用户需求 | 走哪条路 |
|---|---|
| 用 Java + JDBC + SQL **批量灌数据到 PI**（高吞吐） | **本 skill**（PI JDBC + PI SQL DAS + PI OLEDB） |
| 用 .NET / AF SDK 写 PI 点位 / AF 属性 | `pi-write.ps1` in `aveva-pi-af` |
| 从 PI **读**数据（实时/历史/插值/汇总） | 读侧已有往返优化 |

## 核心框架

### 1. 往返优化是单向的 — 写侧需要独立优化
写侧的吞吐瓶颈是 **DAS 和 JDBC 客户端之间的网络往返次数**。批量执行（`addBatch` + `executeBatch`）把多次往返合并为一次。

### 2. 两种批量执行形式
- **`Statement.addBatch(query)` + `executeBatch()`**：在 Statement 对象中积累多条完整 SQL 字符串，一次性发送给 DAS。
- **`PreparedStatement.addBatch()`**：积累二维参数数组，作为单个对象传给 DAS 执行。**这是批量插入的正确方式**。

### 3. FLUSH 写缓存优化 — 最大杠杆
默认情况下，每条 UPDATE 语句**立即执行**，PI 归档**立即反映所有更改**——对写密集型应用是性能杀手。
- 在 UPDATE 语句后面加上 **`OPTION(NO FLUSH, NO REFRESH)`**，更改**不会立即可见**，直到连接关闭。
- 要显式刷出，执行 **`stmt.executeUpdate("FLUSH")`**。

### 4. 写方法三档（实测基准）
| 档次 | 方法 | 吞吐量（测试环境） |
|---|---|---|
| 传统 | 循环 1000 次参数化 `INSERT` + `executeUpdate()` | **237 events/second** |
| 批量 | `addBatch()` 累积后，一次 `executeUpdate()` | **598 events/second** |
| 批量 + 缓存 | `addBatch()` + `OPTION(NO FLUSH)` + 最终 `FLUSH` | **10309 events/second** |

### 5. 两个容易被忽略的提速方式
- **缓存 PI SDK 点位对象**：第二次及之后的 `executeUpdate()` 比第一次快 **2-3 倍**。
- **多 DAS 横向扩展**：使用两个 DAS 实例（同一台机器双端口，或两台机器各一个），可获得近似线性提升。

## 参考

- [Batch Execution in PI JDBC 2010 R2 白皮书](https://vcampus.osisoft.com/servlet/JiveServlet/download/3-5660/Batch-Execution-in-PI-JDBC-2010-R2.pdf)
