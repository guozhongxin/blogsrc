title: 忙忙碌碌 我的2016
date: 2017-04-28 23:00
author: guozhongxin
category: summary
slug: summary2016
summary: 2016对于我是注定忙碌的一年。直到拿到dream offer前，手上同时都会有多方面的工作要做。第一研究生毕业所需要的小论文不能再拖了；第二，17年毕业的我要开始找实习，并准备找工作了；第三毕业设计也要在年底前完成所有工作；第四，实验室的项目，以及集群管理的日常工作都需要我一直参与。

## 2016

2016对于我是注定忙碌的一年。

直到拿到dream offer前，手上同时都会有多方面的工作要做。第一研究生毕业所需要的小论文不能再拖了；第二，17年毕业的我要开始找实习，并准备找工作了；第三毕业设计也要在年底前完成所有工作；第四，实验室的项目，以及集群管理的日常工作都需要我一直参与。


### 1.实习：和MSRA的第一段缘分

春节前学长内推我去微软亚洲研究院实习。面试的组正在做分布式计算的相关研究，要基于Spark源码做开发，面试的内容主要和Spark相关。当时面试官，也是后来的同事chenyang、gaoyanjie，拿了一个笔记本过来，直接对着Spark源码开始提问。整体上面试内容正合我胃口，也就有幸拿到了MSRA的实习机会。

在MSRA的前半段时间里，我参与到了TR-Spark的工作中来。简单来说，TR-Spark是在一种非常不稳定的云环境（`Transient Resource`）下，依然能稳定工作的分布式计算平台，是当时的代码在Spark 1.5.2版本上进行二次开发的。这种不稳定的云环境是一些非常廉价的云主机，会在其他租户申请资源时被主动释放掉，以供这些“高级”租户使用，虽然不稳定，但也相当廉价。TR-Spark在这种环境下，通过resource stability and data size reduction-aware scheduling，以及 lineage-aware checkpointing两大策略相结合，智能的备份Spark计算的中间结果（两个Stage之间进行shuffle时的`block`），从而提高了分布式平台在Transient Resource环境下的高可用性[1]。

之后，我的mentor，yanying转向了区块链`BlockChain`的研究。我还记得的最开始的时候，ying姐拉我到一个讨论室里“安利”我什么是BlockChain，这是我第一次听说这个技术，听得我云里雾里。紧接着，ying姐，chenyang带着我开始看各种相关BlockChain开源项目的白皮书，开始研究BlockChain到底是什么。刚接触新事物的我会比较迷茫，不知道从何看起，而且有时会get不到两位researcher的点。在ying姐的强有力的指导和push下，我们抽丝剥茧，一步步理解BlockChain技术核心。实际中我们是从BigchainDB源码开始，了解BlockChain运作的整个流程。并基于BigchainDB做了一个基于BlockChain的慈善系统（BlockChain for Charity），参加了微软的Hackathon。由于在不像大多数BlockChain上都是虚拟货币，在慈善系统中记录的可能是实际货币，甚至是物品，因此我在BigchainDB上做了一个tx receiver要进行确认的机制。在这个项目中，我们也发现BigchainDB的整体架构和主流的区块链项目有明显差异：BigchainDB是建立在一个分布式的数据库上，而不是各自节点分别maintain一个数据库，因此虽然不用考虑数据一致性的问题从而提高了Throughput，但是也给整个系统带来了安全上的风险。这一差异各有优劣。之后我们又开始研究Ethereum，一个主流的BlockChain项目，我重点关注了Smart Contract方面的问题。

从16年2月底到9月初，六个月多的时间过得很快，也很充实。最幸运的是有一个超级棒的mentor，在各个方面给我很多指导和机会，自己受益匪浅。实习期间合作的两位同事，Spark专家yanjie，博学的chenyang，还有老板Thomas，也都让我对MSRA充满了崇拜。

### 2.小论文：一波两折

到了16年我的小论文不能再拖了，春节期间把论文思路整理里一下，研二下学期开学回来就开始动笔了。

小论文主要研究内容是针对分布式计算平台的性能瓶颈进行分析、建模。所谓性能瓶颈主要是指分布式作业执行期间，集群资源的有限性对执行效率的影响。最初的点是IBM研究院实现时的mentor，巨伟提出的，我零零散散做了近一年的时间。首先是将性能瓶颈进行量化，把性能分析从定性分析问题变成量化指标。再通过计算平台log中的metrics对性能瓶颈指标进行建模，得到一个适用于不同集群、不同类型作业的性能瓶颈模型。

在小论文上，主要从一个和我自己导师有合作关系的老师那里得到了一些指导，但她对研究内容本身没有太多了解。第一版的论文写得很潦草，投了CIKM，等了两个月之后最后收到了4个review，两个accept、一个borderline、一个reject，最后得到chair的reject。一般cikm都是3个reviewer，看来在最开始的review中分歧较大，多加了一个。这些review很犀利，也很到位，不得不服。

在做了相对应的修改和调整后，我和导师就投稿会议产生了分歧，导师想让我投VLDB这样的顶会，我不思进取找个时间近的水会就要投，最后导师还是放了我一马，投了HPCC [2]。在修改论文时，我在MSRA实习的两位小伙伴youer和辰哥帮我修改英文表达，事实证明留学的博士就是强。感觉在MSRA认识的博士都非常让我佩服，洗刷了我对博士的naive的偏见，也后悔当时怎么没考虑读博呢。。

### 3.找工作：兜兜转转回到起点

主要过程记录在这篇博文里：[迟到的毕业求职总结：兜兜转转回到起点](http://guozhongxin.com/pages/2017/05/02/jobhunting.html)

### 4.毕业设计

我的毕设内容主要是分布式社交分析算法和实现，另外把我小论文的内容也给整合进去，包装成了一个系统。靠前半部分撑起工作量，后边的小论文撑点研究价值，整体比较水。毕设的主要工作也是和实验室项目密切相关的，但是为了使工作量丰满，在找工作的同时还在做一些整合性的工作。论文的正式动笔是10月中旬，到11月下旬攒了一个初稿，进行了中期答辩，之后进行了初步修改和完善。12.1向学校提交了初稿，进行论文盲审，之后就比较顺利了。

2016忙忙碌碌，也收获满满。以后每年的总结都要及时进行，不能拖这么久了。

[1]Yan Y, Gao Y, Chen Y, et al. TR-Spark: Transient Computing for Big Data Analytics[C]// ACM Symposium on Cloud Computing(SoCC). ACM, 2016:484-496.

[2]Guo Z, Hu Z, Zhang C, et al. Learning-Based Characterizing and Modeling Performance Bottlenecks of Big Data Workloads[C]//IEEE 18th International Conference on High Performance Computing and Communications(HPCC). IEEE, 2016: 860-867.