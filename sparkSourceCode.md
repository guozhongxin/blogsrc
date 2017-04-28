title: Windows + IDEA + SBT 打造Spark源码阅读环境  
author: guozhongxin
date: 2014-10-15 11:00
tags: spark, 源码
category: spark
slug: spark_source_code

## Spark源码阅读环境的准备

Spark源码是有Scala语言写成的，目前，[IDEA](/http://www.jetbrains.com/idea/)对Scala的支持要比eclipse要好，大多数人会选在在IDEA上完成Spark平台应用的开发。因此，Spark源码阅读的IDE理所当然的选择了IDEA。

本文介绍的是Windows下的各项配置方法（默认已经装了java，JDK）。

下面列举搭建此环境需要的各个组件：

- [**IDEA**](http://www.jetbrains.com/idea/download/)，有两个版本：Ultimate Edition & Community Edition，后者是free的，而且完全能满足学习者所有的需求  
- [**Scala**](http://www.scala-lang.org/download/)，Spark是用Scala语言写成的，在本地编译执行需要这个包
- [**SBT**](http://www.scala-sbt.org/download.html)，scala工程构建的工具
- [**Git**](http://git-scm.com/download/)，IDEA自动下载SBT插件时可能会用到的工具
- [**Spark Source Code**](http://spark.apache.org/downloads.html)，Spark源码

下载各个安装包。

##Spark源码阅读环境的安装步骤

####安装[Scala](http://www.scala-lang.org/download/)。  
完成后，在windows命令行中输入`scala`，检查是否识别此命令。  
如果不识别，查看环境变量Path中是否有`....\scala\bin`（我的电脑右键，属性 -> 高级系统设置 -> 环境变量）,没有的手动将Scala文件夹下的bin目录的路径

####安装[SBT](http://www.scala-sbt.org/download.html)
运行SBT的安装程序，运行完成后，重新打开windows命令行，输入`sbt`，检查是否识别此命令。没有的话，手动配置环境变量，添加`...\sbt\bin`

运行完SBT的安装程序之后，并不意味着完成了sbt的安装，在windows命令放下输入`sbt`后，SBT会自动的下载安装它所需要的程序包，请耐心等待全部下载成功。

####安装[Git](http://git-scm.com/download/)
运行Git的安装程序，安装完成后，重新打开windows命令行，检查时候识别`git`命令。

####安装[IDEA](http://www.jetbrains.com/idea/download/)

####安装IDEA的Scala插件
打开IDEA，在‘Welcome to IntelliJ IDEA’界面的‘Quick Start’栏，点击`Configure`，选择`Plugins`。  

在弹出的窗口中可以看到已安装的插件，现在IDEA默认还没有Scala的插件。需要点击左下角的`Install JetBrains plugin...`，在搜索框中输入‘scala’，点击安装。安装完成后可能会要求重启一下IDEA。

####解压缩Spark Source Code包

##导入Spark工程
在欢迎界面‘Quick Start’栏或者是在主界面的菜单栏`File`下，选`Import Project`，找到解压之后的spark工程文件夹，`OK`。

选择`import project from external model`中的`SBT project`，（这个选项只有在安装了IDEA的Scala插件才会有）。

下一步，选择Project SDK为JDK，最好勾上`Use auto-import`，然后点击`Finish`。这时，**IDEA会自动下载安装SBT所需的各个包**，没有装Git的话可能会报错。

因为Spark是一个比较大的工程，所需的包也很多，这个过程也会特别慢，请耐心等待。

####导入完成
导入完成后，自动打开工程，要等一段时间，等待sbt对这个工程进行编译。