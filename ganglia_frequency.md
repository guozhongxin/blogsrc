title: Ganlia采样、统计及RRD记录周期（频次、间隔）的配置和更改
author: guozhongxin
date: 2014-10-15 22:00
category: ganglia
tags: ganglia,
slug: ganglia_frequency
summary: 更改Ganlia采样及统计周期（频次）的配置参数

##Ganglia & RRD
Ganglia是伯克利开发的一个集群监控软件。可以监视和显示集群中的节点的各种状态信息，比如如：cpu 、mem、硬盘利用率， I/O负载、网络流量情况等，同时可以将历史数据以曲线方式通过php页面呈现。

Ganglia监控系统的核心有两部分：gmond 和 gmetad：

* gmond在各个节点上运行，负责采集数据；
* gmetad在主节点上运行，负责接收gmond采集上来的数据并将之储存在RRD中。

RRD（Round-Robin Database）是一种固定大小的环形的数据库，一个RRD文件下可以有多个RRA，每个RRA是一个环，环上可以储存的数据个数是固定个，新的数据被记录时会覆盖最旧的那条数据，从而周而复始的记录。

![1](http://www.guozhongxin.com/images/RRD.jpg) 

Ganglia将监控数据以RRD的形式储存并通过php展示在web页面上。Ganglia默认的是15秒在RRD中记录一次数据，而RRD默认的格式为：

	RRAs "RRA:AVERAGE:0.5:1:244" "RRA:AVERAGE:0.5:24:244" "RRA:AVERAGE:0.5:168:244" "RRA:AVERAGE:0.5:672:244" "RRA:AVERAGE:0.5:5760:374"
	
这是Ganglia创建的RRD的默认形式，一个RRD文件有四个RRA用来记录数据。  

* 第一个RRA一共储存着244个数据，每插入一条数据储存一个数据，Ganglia默认的15s记录一次，这就意味着默认的这个RRA记录着最近61分钟的数据，这也就是在web上看到的一小时的图。

* 第二个RRA一共储存着244个数据，每插入24条数据取平均数，储存一个数据，15s * 24 = 360s，意味着6分钟储存一条数据。总共记录了 6min * 244 = 1464min = 24.4h 约为一天的数据。对应的是web上最近24h的数据图。
 
* 第三个RRA，每插入168条数据取平均数储存一条数据，15s * 168 = 42min，42分钟记录一条数据，总共记录 42min * 244 = 7.1d 约为一周的数据。
 
* 第四个RRA，记录最近四周的数据。对应web界面上Last month的数据。
* 第五个RRA记录最近一年的数据。

##为什么要更改Ganlia采样、统计及RRD记录的最小间隔
对于简单的集群监控，Ganglia的默认配置是足够的，能够满足集群管理员发现集群的性能表现和一些故障，并判断故障发生在哪里。  

但是在进行细致的作业分析时，15s的最小采样间隔是不能够满足需求的。

以笔者研究的spark作业的性能表现为例，对于40G的数据，在4节点、16GB per node、32 cores per node的Spark集群上进行wordcount，作业的总共运行时间平均为53s，而map stage中每个task的运行时间在10s左右，reduce&save stage中每个task的运行时间不过2-4s。

由于spark高效的执行效率，spark运行过程中占用集群资源的行为变化是迅速的，15s的记录间隔是无法察觉的。

因此，**为了让Ganglia能够更好的适应Spark的节奏，需要将Ganlia采样、统计及RRD记录的最小间隔由15s改到更小**，笔者直接选择在**1s**。

##更改Ganglia配置参数，以更改采样和记录的最小间隔
###停止Ganglia的运行
为了避免出现运行错误，在更改配置前关闭ganglia的运行。

在主节点上，使用命令：
	
	service gmetad stop
	
在各个节点上，使用命令：

	service gmond stop

###更改gmond配置（更改搜集数据的周期，以及传输传输周期）
gmond的配置在/etc/ganglia/gmond.conf中

对于只取一次值的metric，将`time_threshold`，因为这些值，如`mem_total`，会在web端php画图时用到，因为memory那张图中的`memory used`，并不是通过直接采集数据得到的，而是通过`mem_total`减去其他值计算得到的，因此，`mem_total`一开始就应该被获取，因此`time_threshold`需设为1（默认为1200）。

	collection_group {
	  collect_once = yes
	  time_threshold = 1
	  metric {
	    name = "cpu_num"
	    title = "CPU Count"
	  }
	  ...
	  metric {
	    name = "mem_total"
	    title = "Memory Total"
	  }
	  ...
	}

对于其他metric，如cpu group中的各个metric，采样与传输的时间也应设置为1（s）

	collection_group {
	  collect_every = 20
	  time_threshold = 90
	  /* CPU status */
	  metric {
	    name = "cpu_user"
	    value_threshold = "1.0"
	    title = "CPU User"
	  }
	  metric {
	    name = "cpu_system"
	    value_threshold = "1.0"
	    title = "CPU System"
	  }
	  ...
	}

即

	collect_every = 1
	time_threshold = 1



###更改gmetad配置（更改记录的最小间隔）
gmetad的配置在/etc/ganglia/gmetad.conf中
	
	# Format: 
	# data_source "my cluster" [polling interval] address1:port addreses2:port ...
	# The keyword 'data_source' must immediately be followed by a unique
	# string which identifies the source, then an optional polling interval in 
	# seconds. The source will be polled at this interval on average. 
	# If the polling interval is omitted, 15sec is asssumed. 
	
	
看到这里有关于`[polling interval]`的解释，即gmetad会根据从gmond搜集的数据，每一个间隔计算出这个间隔内的平均数将其写入rrd。  
而这个参数，是一个非必要的参数，如果用户不指定的话，每15s记录一次。

因此，为了将Ganglia记录最小间隔及RRD中数据的最小时间间隔改为1s，需要在master名称后添加一个参数：1

	data_source "my cluster" 1 localhost  my.machine.edu:8649 ...
	
为了让web依然能够顺利的画出一天、一周、一月、一年的图，还应该修改RRD的格式。

原来的采样间隔是15s，现在的采样间隔是1s，就要把每个RRA的容量扩充，或者将除了第一个RRA之外的RRA的记录间隔改大。

两种调整RRD格式的方法：

1.

	RRAs "RRA:AVERAGE:0.5:1:3660" "RRA:AVERAGE:0.5:24:3660" "RRA:AVERAGE:0.5:168:3660" "RRA:AVERAGE:0.5:672:3660"
	
2.

	RRAs "RRA:AVERAGE:0.5:1:3660" "RRA:AVERAGE:0.5:360:244" "RRA:AVERAGE:0.5:2520:244" "RRA:AVERAGE:0.5:10080:244"

因为我只需要近一小时的详细数据，因此，我采用第二种方式，RRD的文件会小一些。

###清除原有RRD
因为RRD的格式发生变化，和原有的RRD不同，因此，需要将原来的RRD删除，

RRD的文件储存位置的配置在gmetad.conf中：`rrd_rootdir`。

`rrd_rootdir`的默认位置在`/var/lib/ganglia/rrds`，将这个文件夹下的所有文件及文件夹删除即可。

###启动Ganglia

在主节点上，使用命令：
	
	service gmetad start
	
在各个节点上，使用命令：

	service gmond start
	
###查看更改之后的效果

	service httpd restart

在http://masterhost/ganglia中可以看到更改之后的变化：

![image](http://www.guozhongxin.com/images/ganglia_old.png)

![image](http://www.guozhongxin.com/images/ganglia_new.png)

![image](http://www.guozhongxin.com/images/ganglia_big.png)

最后一张图明显能看出更改之后统计的数据更细腻。