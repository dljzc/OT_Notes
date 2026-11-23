# 工程工具笔记

## 扫描与探测工具

### Nmap

Nmap 是一种网络扫描和安全审计工具，用于发现网络上的主机和服务。

#### 常用命令
```bash
# 主机发现
nmap -sn 192.168.1.0/24

# 端口扫描
nmap -p 1-1000 192.168.1.100

# 服务版本识别
nmap -sV 192.168.1.100

# OS 指纹
nmap -O 192.168.1.100

# 脚本扫描
nmap -sC 192.168.1.100

# 输出 XML
nmap -oX scan.xml 192.168.1.100
```

#### 工业网络注意事项
- 避免在生产网络进行激进扫描（可能导致设备停机）
- 使用 `-T` 限制扫描时间
- 使用 `--min-rate` 限制扫描速率
- 优先扫描已知重要设备

### Masscan

Masscan 是一种快速的端口扫描工具，适合大规模网络扫描。

#### 常用命令
```bash
# 快速扫描
masscan -p 80,443,502,4481 192.168.1.0/24

# 输出结果
masscan -p 80,443,502,4481 192.168.1.0/24 -oL results.txt
```

### FFUF

FFUF 是一种 Web 目录和参数 fuzzing 工具。

#### 常用命令
```bash
# 目录爆破
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/seclists/SecLists-usernames.txt

# 参数 fuzz
ffuf -u http://target.com/api/FUZZ -w /usr/share/wordlists/seclists/SecLists-usernames.txt

# 输出 JSON
ffuf -u http://target.com/FUZZ -w wordlist.txt -o results.json
```

## 脚本与自动化

### PowerShell

PowerShell 是 Windows 平台的强大自动化工具，广泛用于工业自动化和数据处理。

#### 常用用途
- AF SDK 与 PI 数据交互
- 工业设备配置管理
- 日志收集与分析
- 自动化报告生成

#### 示例
```powershell
# 列出进程
Get-Process

# 获取服务状态
Get-Service | Where-Object {$_.Status -eq 'Running'}

# 读取文件内容
Get-Content C:\data\report.txt

# 发送 HTTP 请求
Invoke-RestMethod -Uri http://api.example.com -Method Get
```

### Python

Python 是跨平台的通用编程语言，适合数据处理、自动化脚本和工具开发。

#### 常用库
- **pandas**：数据处理与分析
- **numpy**：数值计算
- **requests**：HTTP 请求
- **pymodbus**：Modbus 通信
- **opcua**：OPC UA 通信
- **scapy**：网络包操作

#### 示例
```python
import pandas as pd
import requests

# 读取 CSV 数据
df = pd.read_csv('data.csv')

# 发送 HTTP 请求
response = requests.get('http://api.example.com')
print(response.json())
```

### Bash

Bash 是 Linux 平台的默认 shell，适合系统自动化和命令行操作。

#### 常用命令
```bash
# 文件操作
ls -la
cat file.txt
grep 'pattern' file.txt

# 系统信息
ps aux
df -h
free -m

# 自动化脚本
for i in {1..10}; do echo $i; done
```

## 网络分析工具

### Wireshark

Wireshark 是一种网络协议分析器，用于捕获和分析网络流量。

#### 常用用途
- 工业协议分析（Modbus、DNP3、OPC UA 等）
- 网络故障排查
- 安全审计
- 流量分析

#### 过滤表达式
```bash
# Modbus TCP 流量
tcp.port == 502

# DNP3 流量
tcp.port == 19999

# OPC UA 流量
tcp.port == 4481
```

### tcpdump

tcpdump 是命令行的网络包捕获工具，适合脚本集成和自动化分析。

#### 常用命令
```bash
# 捕获特定端口流量
tcpdump -i any -n port 502

# 保存到文件
tcpdump -i any -n port 502 -w capture.pcap

# 读取文件
tcpdump -r capture.pcap
```

### Nuclei

Nuclei 是一种基于 YAML 模板的漏洞扫描工具。

#### 常用命令
```bash
# 扫描目标
nuclei -u http://target.com

# 使用特定模板
nuclei -u http://target.com -t cves/

# 输出结果
nuclei -u http://target.com -o results.txt
```

## 实践建议

### 工具选择

- **网络扫描**：Nmap（详细）、Masscan（快速大规模）
- **Web 测试**：FFUF（目录/参数）、Nuclei（漏洞）
- **网络分析**：Wireshark（图形）、tcpdump（命令行）
- **自动化**：Python（跨平台）、PowerShell（Windows）
- **工业协议**：专用工具（Modbus Poll、UAM Client 等）

### 安全使用

- 只在授权范围内扫描
- 避免在生产网络进行激进扫描
- 保存扫描结果作为证据
- 定期更新工具和规则

## 参考

- [Nmap 官方文档](https://nmap.org/docs/)
- [Wireshark 官方文档](https://www.wireshark.org/docs/)
- [Nuclei 官方文档](https://docs.projectdiscovery.org/nuclei/)
