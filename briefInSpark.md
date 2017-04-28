title: Spark简介
date: 2014-10-12 21:00
author: guozhongxin
category: Python
slug: a_brief_in_spark
tags: spark, 
summary: 介绍spark的计算模型、架构、功能模块、配置

#目录：
* Spark综述
* Spark计算模型：RDD，算子，stage，
* Spark架构及工作流程
* Spark组件
* Spark配置

#Spark综述--Spark是什么
* 基于内存的分布式并行计算框架
* 一种粗粒度数据并行（data parallel）的计算范式（相对于 task parallel）
* 以RDD(弹性分布式数据集)为计算对象
* 核心代码两万行，轻量级分布式系统
* 支持Hadoop2.0，支持HDFS
* 支持内存计算、多迭代批量处理、即席查询、流处理和图计算  


#Spark计算模型

###弹性的分布数据集(RDD) 

* 分布式对象集合能够跨集群在内存中保存。多个并行操作，失败自动恢复。
* A list of partitions;
* A function for computing each split
* A list of dependencies on other RDDs: HadoopRDD，ShuffledRDD，PartitionPruningRDD…  

###算子  

算子，即对数据集RDD进行操作的函数。  
Spark计算模型中，总共涉及四种算子。    

* 输入算子：val lines = sc.textFile("data.txt")
* 缓存算子：lines.cache(), lines.persist()
* 变换算子(Transformations)： create a new dataset from an existing one，由一个（或多个）已存在的RDD转换成另外一个RDD：map(), filter(), group(), flatmap()…
* 行动算子(Actions)： return a value to the driver program after running a computation on the dataset，由RDD转换成：reduce(), count()…  

下图可以较为清楚的理解四种算子：  
![1](http://www.guozhongxin.com/images/suanzi.png)  

####>>算子的执行
 
从RDD到RDD的变换算子序列，一直在RDD空间发生。这里很重要的设计是`lazy evaluation`：计算并不实际发生，只是不断地记录到元数据。元数据的结构是`DAG`（有向无环图），其中每一个“顶点”是RDD（包括生产该RDD 的算子），从父RDD到子RDD有“边”，表示RDD间的依赖性。Spark给元数据DAG取了个很酷的名字，`Lineage`（世系）。  

Lineage一直增长，直到遇上行动（action）算子（图1中的绿色箭头），这时 就要evaluate了，把刚才累积的所有算子一次性执行。行动算子的输入是RDD（以及该RDD在Lineage上依赖的所有RDD），输出是执行后生 成的原生数据，可能是Scala标量、集合类型的数据或存储。当一个算子的输出是上述类型时，该算子必然是行动算子，其效果则是从RDD空间返回原生数据 空间。

另一个要点是一旦行动算子产生原生数据，就必须退出RDD空间。因为目前Spark只能够跟踪RDD的计算，原生数据的计算对它来说是不可见的（除非以后 Spark会提供原生数据类型操作的重载、wrapper或implicit conversion）。

####>>shuffle（重排）

涉及重排，称为shuffle类操作。

* 对单个RDD重排，如sort、partitionBy（实现一致性的分区划分，这个对数据本地性优化很重要，后面会讲）；
* 对单个RDD基于key进行重组和reduce，如groupByKey、reduceByKey；
* 对两个RDD基于key进行join和重组，如join、cogroup。

###宽依赖与窄依赖

![2](http://www.guozhongxin.com/images/dependency.png)  

左侧为窄依赖，右侧为宽依赖  

宽依赖与窄依赖的最主要区别在于，宽依赖关系涉及到shuffle过程，而窄依赖不涉及shuffle。  

###Stage

Stage是Spark对DAG的划分，以此作为对作业的进行任务（task）划分和调度的依据。  
可以这样理解Stage不需要shuffle是可以随意并发的, 所以stage的边界就是需要shuffle的地方。

下图是一个stage例子。
![3](http://www.guozhongxin.com/images/stage.png) 

###共享变量（Shared Variables）

* 广播变量：  
	允许程序员保留一个只读的变量，缓存在每一台机器上，而非每个任务。被创建后，它能在集群运行的任何函数上，需要被再次传递到这些结点上。
	通过SparkContext.broadcast(v)方法创建。
	对象v不能在被广播后修改，是只读的。
* 累加器：  
	通过调用SparkContext.accumulator(V)方法来创建。
	运行在集群上的任务，可以使用+=来加值。然而，它们不能读取计数器的值。
	当Driver程序可以使用.value方法读取该值


#Spark架构

先给一个概况图：  
![4](http://www.guozhongxin.com/images/jiagou.png) 

1. 构建Spark Application运行环境；  
	在Driver Program中新建SparkContext（包含sparkcontext的程序称为Driver Program）；
	Spark Application运行的表现方式为：在集群上运行着一组独立的executor进程，这些进程由sparkcontext来协调；
2. SparkContext向资源管理器申请运行Executor资源，并启动StandaloneExecutorBackend，executor向sparkcontent申请task；
	集群通过SparkContext连接到不同的cluster manager(standalone、yarn、mesos)，cluster manager为运行应用的Executor分配资源；一旦连接建立之后，Spark每个Application就会获得各个节点上的Executor（进程）；每个Application都有自己独立的executor进程；Executor才是真正运行在WorkNode上的工作进程，它们为应用来计算或者存储数据；
3. SparkContext获取到executor之后，Application的应用代码将会被发送到各个executor；
4. SparkContext构建RDD DAG图，将RDD DAG图分解成Stage DAG图，将Stage提交给TaskScheduler，最后由TaskScheduler将Task发送给Executor运行；
5. Task在Executor上运行，运行完毕后释放所有资源；

Spark通用的使用方式主要有两种：standalone、spark on yarn

###standalone

基于standalone的Spark架构与作业执行流程（Driver运行在客户端上）：  

![5](http://www.guozhongxin.com/images/standalone.png) 

作业执行流程描述：  

1. 客户端启动后直接运行用户程序，启动Driver相关的工作：DAGScheduler和BlockManagerMaster等。
2. 客户端的Driver向Master注册。
3. Master还会让Worker启动Exeuctor。Worker创建一个ExecutorRunner线程，ExecutorRunner会启动ExecutorBackend进程。
4. ExecutorBackend启动后会向Driver的SchedulerBackend注册。Driver的DAGScheduler解析作业并生成相应的Stage，每个Stage包含的Task通过TaskScheduler分配给Executor执行。
5. 所有stage都完成后作业结束。

###Spark on Yarn  

基于Yarn的Spark架构与作业执行流程：  
![6](http://www.guozhongxin.com/images/taobao.png) 

基于YARN的Spark作业首先由客户端生成作业信息，提交给ResourceManager，ResourceManager在某一NodeManager汇报时把AppMaster分配给NodeManager，NodeManager启动 SparkAppMaster，SparkAppMaster启动后初始化作业，然后向ResourceManager申请资源，申请到相应资源后 SparkAppMaster通过RPC让NodeManager启动相应的SparkExecutor，SparkExecutor向 SparkAppMaster汇报并完成相应的任务。此外，SparkClient会通过AppMaster获取作业运行状态。

Spark on Yarn这种模式因为淘宝技术部在内部平台上的应用而被许多其他使用者模仿，其实根据笔者的感受来讲，绝大多数类型的任务spark着standalone的模式下就能很好的运行，并有不次于Spark on Yarn的执行效率。   


#Spark组件
###DAGScheduler

DAGScheduler主要功能如下：  

* 接收用户提交的job;
* 将job根据类型划分为不同的stage，记录哪些RDD、Stage被物化，并在每一个stage内产生一系列的task，并封装成TaskSet；
* 决定每个Task的最佳位置(任务在数据所在的节点上运行)，并结合当前的缓存情况；将TaskSet提交给TaskScheduler;
* 重新提交Shuffle输出丢失的Stage给TaskScheduler；

注：一个Stage内部的错误不是由shuffle输出丢失造成的，DAGScheduler是不管的，由TaskScheduler负责尝试重新提交task执行；

###TaskScheduler

TaskScheduler是一个可插拔任务调度接口，主要功能如下：  

* 一个TaskScheduler只为一个SparkContext服务，接收DAGScheduler提交过来的一组组的TaskSet；
* TaskScheduler将task提交到集群中并执行，如果其中某个Task执行失败则重试之；TaskScheduler将TaskSet对应的执行结果返回DAGScheduler；
* 处理straggle任务；（比如：100个任务运行，其中99个任务快，1个任务慢，需要在另外一个节点上开启一个相同的任务来运行，谁先完成取用谁）；
* 遇到shuffle输出丢失则汇报给DAGScheduler；
* 为每个TaskSet维护一个TaskSetManager追踪本地性(resourceOffer-->findTask)及错误信息；

###Storage模块

主要分为两层：

* 通信层：storage模块采用的是master-slave结构来实现通信层，master和slave之间传输控制信息、状态信息，这些都是通过通信层来实现的。
* 存储层：storage模块需要把数据存储到disk或是memory上面，有可能还需replicate到远端，这都是由存储层来实现和提供相应接口。

其他模块若要和storage模块进行交互，storage模块提供了统一的操作类BlockManager，外部类与storage模块打交道都需要通过调用BlockManager相应接口来实现

#Spark配置
###Spark集群配置

配置文件：$SPARK_HOME/conf/spark-env.sh
主要的配置参数有：

* SPARK_MASTER_IP, to bind the master to a different IP address or hostname
* SPARK_WORKER_CORES, to set the number of cores to use on this machine
* SPARK_WORKER_MEMORY, to set how much total memory workers have to give executors (e.g. 1000m, 2g)
* SPARK_WORKER_INSTANCES, to set the number of worker processes per node

举例：一共5台机器，每台24个cpu cores，每台机器上有90GB内存：
	export SPARK_WORKER_MEMORY=30000m
	export SPARK_WORKER_CORES=8
	export SPARK_WORKER_INSTANCES=3
另外还有一些关于Hadoop的配置参数，这是为了Spark on Yarn的工作模式提供的，如果你只使用Standalone模式，则不需要配置。

###[Saprk执行作业属性](http://spark.apache.org/docs/latest/configuration.html)
####>>配置方式
在Spark1.0.x提供了3种方式的属性配置：  

* SparkConf方式，在代码中配置各个参数；
* 命令行参数方式
	使用spark-submit或spark-shell提交应用程序时用命令行参数提交；
* 文件配置方式
	在$SPARK_HOME/conf/spark_default.conf里进行配置；该方式是将属性配置项以键值对方式写入文本文件中，一个配置项占一行；

优先权：  
	SparkConf方式 > 命令行参数方式 >文件配置方式

####>>查看Spark属性配置
在应用程序执行过程中，通过应用程序的webUI（地址http://<driver>:4040）可以查看Spark属性配置，从而检查属性配置是否正确；  
只是显示通过上面三种方式显式指定的属性配置，对于其他属性可以假定使用默认配置；  
对于大多数内部控制属性，系统已经提供了合理的默认配置。  

####>>Spark日志属性配置

Spark日志：log4j，配置文件：$SPARK_HOME/conf/log4j.properties

Spark job(Application)日志，计数器：通过刚才提到的三种方式中的任意一种，对一下Spark Conf进行配置：

	spark.eventLog.enabled=true;  
	spark.eventLog.dir=hdfs:\\...
