title: Spark安装：Spark集群及开发环境搭建
author: guozhongxin
date: 2014-09-26 23:00
category: spark
tags: spark, 开发环境,
slug: spark_installation
summary: 一步一步在集群上安装spark，搭建spark上运行作业的开发环境

##安装Spark准备

在准备安装spark之前，需要准备以下安装包，并完成以下预备动作。  

* scala安装包，可以在[scala官方网站](http://www.scala-lang.org/)下载
* spark安装包，可以在[spark官网](http://spark.apache.org/downloads.html)下载，用两种形式的安装包：
	* source code package
	* pre-build package
* 在主节点实现ssh免密码登陆其他节点。  

###install scala - scala安装download scala-2.10.4.tgz and unzip： 
	tar -zxf scala-2.10.4.tgz	vi ~/.bashrc		export SCALA_HOME=...   
		export PATH=$PATH:$SCALA_HOME/bin	source ~/.bashrc
###install spark. - spark安装There are two types of spark installation package, source package that you need build spark at first, and prebuild package.  
Spark的安装包有两种形式：源码包（用户需要自己下载后在平台上编译），以及已经编译打包好的安装包
To build source package, you should unzip the package and edit pom.xml in the directory, change <hadoop.version></hadoop.version> and some jars' version: protobuf, hbase, hive. Then, you can run this command :    
在用源码包安装时，你需要先解压缩安装包，然后修改文件夹中中pom.xml文件，将hadoop、protobuf、hbase、hive的版本号修改为当前环境的版本。之后在这个文件夹下运行这条命令：  	./make-distribution.sh --hadoop 2.4.0 --with-yarn --with-hive --with-tachyon --tgz --skip-java-test
If you choose prebuild package with the right hadoop version, you needn't build it by yourself.   
如果你选择了已经build好的安装包，以上步骤不需执行。
将自己编译或是下载的编译包解压缩，并配置环境变量：	
	tar -zxf spark-1.0.0-bin-2.2.0.tgz	vi ~/.bashrc		export SCALA_HOME=...  		export PATH=$PATH:$SCALA_HOME/bin:$SCALA_HOME/sbin	source ~/.bashrc

###Configure Spark cluster - Spark集群配置* edit `$SPARK_HOME/conf/slaves`, and input all node IP :  		masters  
	slave1  
	slave2  
	slave3 
 * create and edit `$SPARK_HOME/conf/spark_env.sh` 
	export HADOOP_HOME=/opt/apache/hadoop-2.4.0  	export HADOOP_CONF_DIR=/opt/apache/hadoop-2.4.0/etc/hadoop  	export JAVA_HOME=/usr/local/jdk1.7.0_60  	export SCALA_HOME=/home/yarn/scala-2.10.4  
	export SPARK_WORKER_MEMORY=16g  	export SPARK_WORKER_INSTANCES=1  	export SPARK_MASTER_IP=master
	实际上安装好之后`conf`文件夹下有一个`spark_env.sh`的模板，里边有各个变量的解释说明，在这不一一累述  

* Copy to other node 

要将各个节点上的这两个文件都进行配置

###Configure Spark App - Spark作业属性配置
对于作业执行的属性配置，spark提供了三种不同的配置方法  
1. create and edit `$SPARK_HOME/conf/spark_default.conf`  
	spark.master                    spark://master:7077  	spark.eventLog.enabled          true  	spark.eventLog.dir              hdfs://master:8020/sparklog  	spark.local.dir           		 ...  

2. 在通过$SPARK_HOME/bin/spark-submit这个脚本提交作业时，通过 
 
		$SPARK_HOME/bin/spark-submit  /
		--master spark://master:7077  /
		--conf spark.eventLog.enabled=true ...  /
		***.jar
		
3. 通过代码中对SparkContext来对这些属性赋值

这三种方法的优先级是：  
	3 高于 2 高于1  
 ###Tips1.	If you change SPARK_WORKER_INSTANCES, CHECK worker's process in every node  If old worker's process is still working , you can use this command to kill them:  
		ps -ef | grep Worker | grep -v grep | cut -c 9-15 | xargs kill -s 9  and restart Spark Cluster  
2.	if you want to start history server, you should assign logs' path:  

		$SPARK_HOME/sbin/start-historyserver.sh  $SPARK_HOME/logs  
		3.	If you wanna save a job's log, you should assign two properties:  
	spark.eventLog.enabled          true  	spark.eventLog.dir              hdfs://master:8020/sparklog  
