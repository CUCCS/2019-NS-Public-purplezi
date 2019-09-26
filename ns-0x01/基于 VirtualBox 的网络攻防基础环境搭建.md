# 基于 VirtualBox 的网络攻防基础环境搭建



## 实验目的

* 掌握VirtualBox虚拟机的安装与使用；
* 掌握VirtualBox的虚拟网络类型和按需配置；
* 掌握VirtualBox的虚拟硬盘多重加载



## 实验环境

以下是本次试验需要使用的网络节点说明和主要软件举例：

* VirtualBox虚拟机6.0
* 攻击者主机（Attacker）：Kali Rolling 64-Bit 2019.3
* 网关（Gateway，GW）：Debian Buster（老师提供的压缩包）
* 靶机（Victiom）： xp-sp3（老师提供的压缩包）



## 实验要求



### 1. 虚拟硬盘配置成多重加载

#### 		1.1 将虚拟硬盘由普通设置为多重加载

- 首先正常的虚拟硬盘是普通，配置成多重加载的好处：可以将虚拟镜像文件和加载点文件复制到其他电脑里面直接创建一个虚拟机，而不用再次装系统。

- 关闭虚拟机，打开虚拟介质管理，直接将对应的vdi改为多重加载后报错，原因是该虚拟硬盘仍然连接着一个虚拟机，还未释放虚拟硬盘。

  ![ErrorMultiAttack](ErrorMultiAttach.png)

- 右键vdi选择释放，由于我之前给我的虚拟机进行了备份，不能直接释放vdi，而要从备份开始一个个释放。

- 释放完毕后，右键vdi的属性，将类型修改为多重加载，选择应用。

  ![multiattach1](multiattach2.PNG)

* 将老师给的vdi设置为多重加载出错，我初步猜测是因为我将该vdi注册后，还未分配给某个虚拟机，而直接想修改为多重加载，所以报错。正确操作应先把它添加为一个虚拟机的虚拟硬盘，然后再释放，而后再改为多重加载。![error1](ErrorMultiAttach1.PNG)




#### 		1.2 复用多重加载的虚拟硬盘

* 将虚拟机原有的虚拟硬盘，改成多重加载的硬盘。右键虚拟机->设置->存储->控制器:SATA，添加虚拟硬盘到控制器->使用现有的虚拟盘，选择我们刚才设置好的多重加载的虚拟硬盘。![addmultiattach](multiattach.png)


* 新建一个虚拟机时，选择使用已有的虚拟硬盘文件，即设置过多重加载的vdi。

  ![new](new.PNG)


* 对没有盘片的疑惑：此处的控制器IDE有盘片，则每次开启虚拟机系统则会重新安装一遍系统，没有盘片相当于系统安装完毕后，光盘自动弹出的过程。



### 2.搭建满足如下拓扑图所示的虚拟机网络拓扑

![requiretopology](vb-exp-layout.png)


* 解释虚拟网络拓扑图：首先图示有三个网络，分别是内部网络intnet1和intnet2以及Nat网络，内部网络intnet1和intnet2分别有两个victim主机，Gateway和Attacker在Nat网络中。内部网络和Nat网络的通信传输通过网关Gateway作为跳板。图示的云朵应该是表示Nat网络。

* 由于电脑性能带不起，启动一个电脑主机都快得卡死，所以选择了如下的虚拟网络拓扑，而且将每个的虚拟内存设为512MB（若是1024MB，则启动的时候会报错电脑主机可用的内存不足）。

  <img src="topology.png" alt="topology" style="zoom: 67%;" />





### 3. 网卡及网络配置

依据是VirtualBox的基础设施保障，在设置虚拟机网络的时候，将网卡的连接方式和网络的界面名称设置为相同的，则可视为这些虚拟机在同一个局域网中。

#### 3.1 靶机（Victim）

* 靶机1：一块网卡，设置为内部网络（internal）模式，名称为‘intnet1’。

  ![victim](victim1.png)


* 靶机1的默认网关为Debian-Gateway。

  ![victim1-GW](victim1-GW.png)


* 靶机2：一块网卡，设置为内部网络（internal）模式，名称为‘intnet2’。

  ![victim2](victim2.png)


* 同理靶机2的默认网关为Debian-Gateway。

  ![victim2-GW](victim2-GW.png)


#### 3.2 网关（Gateway）

* 三个网卡，分别设置为NAT网络、内部网络intnet1和内部网络intnet2。（此处忽略host-only网络，用于别处）

  ![gateway](debian1.png)


* 在虚拟机全局设置，网络中NAT网络的设置如下。

  ![NATnetwork1](NATnetwork1.png)


#### 3.3 攻击者（Attacker）

* 一个网卡，设置为和网关相同的NAT网络。（此处也忽略host-only网络，用于别处）

  ![attacker](attacker.png)




#### 3.4 实验前的一些准备

可能是我的基础知识不扎实，所以出现了一些问题，在此做出说明。

* Kali-attack之前一直默认的是连接第二块网卡，所以用ifconfig等命令一直得不到第一块网卡的IP地址。处理：右键kali，进入settings的network，将eth0设置为connected。

  ![kali的网卡设置](kaliNetwork.png)


* 当网关未打开时，在靶机中执行ipconfig等命令，会发现无默认网关，而且IP地址为0.0.0.0，而后就会得到一个Autoconfiguration IP Address，即自动分配的IP地址。

  ![Autoconfiguration-IP-Address](autoconfigurationIPAddress.png)


* 靶机的防火墙注意要关闭，否则我出现了无法由网关ping通靶机的情况。



### 4. 完成以下网络连通性测试

#### 4.1 靶机可以直接访问攻击者主机

* 验证网络层的连通性，通过靶机ping攻击者主机实现。Kali-Attacker的ipv4地址为10.0.2.4，两个靶机都可以ping通攻击者主机。

  ![victim-ping-attacker](victim-ping-attacker.png)

  

#### 4.2 攻击者主机无法直接访问靶机

* 网络层的不连通性：通过ping命令，判断攻击者主机和两个靶机在网络层具有不连通性。

  ![attacker-ping-victim](attacker-ping-victim.png)

* 链路层的不连通性：通过arp表，判断攻击者主机和两个靶机不在同一个局域网中。

  * 两个靶机的arp表中只有网关的mac地址。

    ![victim1-arp](victim1-arp.png)


    ![victim2-arp](victim2-arp.png)


  * 攻击者主机的arp表中有网关的mac地址，而没有两个靶机的地址。
  
    ![attacker-arp](attacker-arp.png)
  
  
  * 附加查看网关的arp表，发现有攻击者主机的mac地址和两个靶机的mac地址。
  
    ![gw-arp](debian-arp.png)
  
    ![gw-victim-arp](victim-arp.png)
  
        
  
  * 上述证明，两个靶机不在同一个局域网中，但是他们分别和网关在同一个局域网中，他们都和攻击者主机不在同一个局域网中。攻击者主机和网关在同一个局域网中。
  
  

#### 4.3 网关可以直接访问攻击者主机和靶机

* 检验Debian-Gateway可以在网络层访问Kali-Attacker，通过ping命令。

  ![gw-ping-attacker](gw-ping-attacker.png)


* 检验Debian-Gateway可以直接访问两个victim，也通过ping命令。

  ![gw-ping-victim](gw-ping-victim.png)


#### 4.4 靶机的所有对外上下行流量必须经过网关

* 通过靶机ping网关，同时网关开始抓包，过滤只剩下icmp的包，发现icmp包中的request包中源地址是靶机的IP地址，目的地址是网关的IP地址，reply包的源地址是网关的IP地址，目的地址是靶机的IP地址。

  ![victim1-icmp](victim1-icmp.png)


  ![victim-2-icmp](victim2-icmp.png)


#### 4.5 所有节点均可以访问互联网

* 将4个虚拟机电脑ping百度的网址，都可以ping通。

  ![pingbaidu](pingbaidu.png)





## 参考资料

* [师姐的作业]([https://github.com/CUCCS/2018-NS-Public-jckling/blob/master/ns-0x01/%E5%9F%BA%E4%BA%8EVirtualBox%E7%9A%84%E7%BD%91%E7%BB%9C%E6%94%BB%E9%98%B2%E5%9F%BA%E7%A1%80%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA.md](https://github.com/CUCCS/2018-NS-Public-jckling/blob/master/ns-0x01/基于VirtualBox的网络攻防基础环境搭建.md))

