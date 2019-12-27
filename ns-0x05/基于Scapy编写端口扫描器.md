# 基于 Scapy 编写端口扫描器

## 实验目的

- 掌握网络扫描之端口状态探测的基本原理

## 实验环境

- python + scapy
- 网络拓朴的搭建
  - 一个网关 Debian10-GW
    - 物理层的保证

        <img src="imgs/DebianGWNetwork.png" width=70%>
    - 第一张网卡：为了后面讨论`NAT和NAT Network在外网探测的显著区别`。
    - 第二张网卡：为了方便主机远程控制
    - 第三、四网卡：划分两个独立子网
  - 两台靶机 Kali-victim-1 Kali-victim-2
    - 主要只需要一个内部网络
    - 第二张为了方便主机远程控制
    - 确保两台靶机的网络是一致的，通信效果上这两个靶机在同一个局域网上

        <img src="imgs/VictimNetwork.png" width=70%>
  - 打开虚拟机进行查看机器的IP地址，物理层保障，`ip addr show eth0`仅查看某个网卡的信息

        <img src="imgs/phyensure.png" width=70%>
  - 验证内部网络的连通性。
- 网络拓朴做了调整
  - 扫描实验的方便，把攻击者主机和靶机放在同一个局域网中
- 待探测窗口可以自行设置 开放、关闭 和 过滤 状态

## 实验要求

- [x] 禁止探测互联网上的 IP ，严格遵守网络安全相关法律法规
- 完成以下扫描技术的编程实现
  - [ ] TCP connect scan / TCP stealth scan
  - [ ] TCP Xmas scan / TCP fin scan / TCP null scan
  - [ ] UDP scan
- 上述每种扫描技术的实现测试均需要测试端口状态为：开放、关闭 和 过滤 状态时的程序执行结果
- [ ] 提供每一次扫描测试的抓包结果并分析与课本中的扫描方法原理是否相符？如果不同，试分析原因；
- [ ] 在实验报告中详细说明实验网络环境拓扑、被测试 IP 的端口状态是如何模拟的
- [ ] （可选）复刻 nmap 的上述扫描技术实现的命令行参数开关

## 实验过程

### TCP端口扫描

#### TCP connect scan

#### TCP stealth scan

#### TCP Xmas scan

#### TCP fin scan

#### TCP null scan

### UDP端口扫描

## 实验问题与总结

1. 修改Kali的Hostname属性
    ```
    vi /etc/hostname
    vi /etc/hosts
    ```


## 参考资料



