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



		export PATH=$PATH:$SCALA_HOME/bin







	tar -zxf spark-1.0.0-bin-2.2.0.tgz


	slave1  
	slave2  
	slave3 
 




* Copy to other node 

要将各个节点上的这两个文件都进行配置

###Configure Spark App - Spark作业属性配置
对于作业执行的属性配置，spark提供了三种不同的配置方法  



2. 在通过$SPARK_HOME/bin/spark-submit这个脚本提交作业时，通过 
 
		$SPARK_HOME/bin/spark-submit  /
		--master spark://master:7077  /
		--conf spark.eventLog.enabled=true ...  /
		***.jar
		
3. 通过代码中对SparkContext来对这些属性赋值

这三种方法的优先级是：  
	3 高于 2 高于1  
 



		$SPARK_HOME/sbin/start-historyserver.sh  $SPARK_HOME/logs  
		
