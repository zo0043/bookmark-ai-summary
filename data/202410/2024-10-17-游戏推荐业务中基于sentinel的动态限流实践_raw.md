Title: 游戏推荐业务中基于sentinel的动态限流实践

URL Source: https://mp.weixin.qq.com/s/lFuXVBUW_PkrBp4NoAFTig

Markdown Content:
Weixin Official Accounts Platform
===============

             

 

![Image 1: cover_image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/4g5IMGibSxt4E6mIyMEEdoiaA8xWw0EcPNTYPacYB58rzXS5HgMbLbbkiaPBJicf0N2tcEVm0ZYEEHH1Shho7lxSWQ/0?wx_fmt=jpeg)

游戏推荐业务中基于sentinel的动态限流实践
========================

Original 服务器团队 [vivo互联网技术](javascript:void\(0\);)

_2024年10月16日 12:03_

作者：来自 vivo 互联网服务器团队- Gao Meng

本文介绍了一种基于 sentinel 进行二次开发的动态限流解决方案，包括什么是动态限流、为什么需要引入动态限流、以及动态限流的实现原理。

一、背景

1.1 当前的限流方案

随着互联网的发展及业务的增长，系统的流量和请求量越来越大，针对高并发系统，如果不对请求量进行限制，在流量突增时可能会导致系统崩溃或者服务不可用，影响用户体验。因此，系统需要引入限流来控制请求的流量，保证系统的可用性和稳定性。当前推荐业务使用公司vsentinel 限流工具，主要使用 **QPS 限流**和**热点参数限流**。

QPS 限流：对某个资源（通常为接口或方法，也可以自定义资源）的 QPS /并发数进行限流；  
热点参数限流：对某些具体的参数值进行限流，避免因为热点参数的过度访问导致服务宕机。

1.2 存在的问题

无论是 QPS 限流还是热点参数限流，都是对资源/参数的**定量限流**，即对某个资源/参数设置固定阈值，超过阈值则进行限流。

回到业务，游戏推荐系统作为游戏分发的平台，向公司内所有主要流量入口（包括游戏中心、应用商店、浏览器等）分发游戏、小游戏、内容和评论，具有大流量、高负载的业务特点。同时，游戏推荐系统对接的场景多（600+），单个性化接口有100+场景调用（场景可以理解为接口请求的一个基本请求参数）。当前的限流方案存在以下几个问题：

1.  参数级别的限流，600+场景，无法做到每个场景**精细化限流**；
    
2.  接口级别的限流，不会区分具体的场景，无法保证**核心场景**的可用性；
    
3.  如果场景流量有变更，需要及时调整限流阈值，不易**维护**；
    
4.  场景的流量会实时变化，无法做到根据流量变化的**动态限流。**
    

鉴于以上限流问题，推荐系统需要一个能够根据参数流量变化而**动态调整限流阈值**的**精细化限流**方案。

二、动态限流介绍

从配置方式上来看，动态限流和 QPS 限流、热点参数限流最大的不同之处在于，动态限流不是通过配置固定阈值进行限流，而是**配置每个参数的优先级，根据参数的优先级动态调整限流阈值。**

![Image 2](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFAr7wsuBa57W9dibBU4Yibm6xsibZZOiceYgbyDCjrUpu2iaVZgmlTxJ6icJw/640?wx_fmt=png&from=appmsg)

动态限流将资源和参数进行绑定，首先配置资源（一般是接口/方法）总的限流阈值，进而配置资源下具体参数的优先级，根据参数配置的优先级和实时流量，决定当前请求pass or block。

下图示例中，资源总的限流阈值为150，参数A、B、C、D的 QPS 均为100，且配置的参数优先级 A\>B\>C\>D。

*   参数A优先级最高，且 QPS(A) = 100 < 限流阈值150，所以A的流量全部通过；
    
*   参数B优先级仅次于参数A，且 QPS(A) = 100 < 限流阈值150、QPS(A)  + QPS(B)= 200 \> 限流阈值150，所以参数B部分流量通过，pass : 50，block：50；
    
*   参数C和其它参数的优先级低于参数B，且 QPS(A)  + QPS(B)= 200 \> 限流阈值150，所以参数C和其它参数均被限流。
    

![Image 3](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibF7aespRQ2JwDA8NIn6rFhMhAvggB8mQuQrsicNqxRd9RDP3Z1ibNHdxvQ/640?wx_fmt=png&from=appmsg)

如果此时参数值A的 QPS 变为200，B、C的 QPS 仍为100，通过动态限流实现：A请求部分通过，B请求全部拦截，C请求全部拦截；根据各参数值流量的变化，动态适配各参数值通过/拦截的流量，从而实现根据参数值动态限流的效果。

总结：动态限流本质上是**参数优先级限流**，**支持对参数值配置优先级，根据参数值的优先级进行动态流控**。当流量超过阈值后，优先保证高优先级参数通过，拦截优先级低的参数请求。

三、sentinel 介绍

由于动态限流是基于 sentinel 进行二次开发，且动态限流的实现算法是基于 sentinel QPS 限流的优化，这里首先介绍下 sentinel 实现原理和 sentinel QPS 限流的滑动窗口计数器限流算法。

3.1 sentinel 原理介绍

sentinel 是阿里开源的一款面向分布式、多语言异构化服务架构的流量治理组件。主要以流量为切入点，从流量路由、流量控制、流量整形、熔断降级、系统自适应过载保护、热点流量防护等多个维度来帮助开发者保障微服务的稳定性。(官网描述)

sentinel 主要通过责任链模式实现不同模式的限流功能，责任链由一系列 ProcessorSlot 对象组成，每个 ProcessorSlot 对象负责不同的功能。

ProcessorSlot  对象可以分为两类：一类是辅助完成资源指标数据统计的 slot，一类是实现限流降级功能的 slot。

辅助资源指标数据统计的  ProcessorSlot：

*   NodeSelectorSlot：负责收集资源路径，并将调用路径树状存储，用于后续根据调用路径来限流降级；
    
*   ClusterBuilderSlot：负责存储资源的统计信息以及调用者信息，例如该资源的 RT、QPS、线程数等等，作为多维度限流、降级的依据；
    
*   StatisticSlot：负责实现指标数据统计，从多个维度（入口流量、调用者、资源）统计响应时间、并发线程数、处理失败数量、处理成功数量等指标信息。
    

实现限流降级功能的 slot：

*   ParamFlowSlot：用于根据请求参数进行限流（热点参数限流），例如根据某个参数的 QPS 进行限流，或者根据某个参数的值进行限流；
    
*   SystemSlot：用于根据系统负载情况进行限流，例如 CPU 使用率、内存使用率等。
    
*   AuthoritySlot：用于根据调用者身份进行限流，例如根据调用者的 IP 地址、Token 等信息进行限流。
    
*   FlowSlot：用于根据 QPS 进行限流，例如每秒最多只能处理多少请求。
    
*   DegradeSlot：用于实现熔断降级功能，例如当某个资源出现异常时，可以将其熔断并降级处理。
    

![Image 4](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFp5X1JfS3WJXzmR2rZTtA909KnibgF1ggwdWuWaU1PYx1RPkPH437REQ/640?wx_fmt=png&from=appmsg)

除了上述原生 ProcessorSlot，sentinel 还支持 SPI 插件功能，通过实现 ProcessorSlot 接口自定义 slot，从而能实现个性化功能拓展。动态限流正是基于 sentinel SPI 插件方式实现。

3.2 滑动窗口计数器算法

sentinel 的 QPS 限流采用滑动窗口计数器算法，下面我们简单介绍下这个算法原理。

首先介绍一下计数器算法。

3.2.1 计数器

计数器算法：维护一个固定单位时间的计数器来统计请求数，在计数小于限流阈值时通过请求，计数到达限流阈值后拦截请求，直到下一个单位时间再重新计数。  
假设资源限制 1 秒内的访问次数不能超过 100 次。

*   维护一个计数器，每次有新的请求过来，计数器加 1；
    
*   收到新请求后，如果计数器的值小于限流值，并且与上一次请求的时间间隔还在 1秒内，允许请求通过，否则拒绝请求；如果超出了时间间隔，要将计数器清零。
    

![Image 5](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFqgqAQuUnRdXqjKqwkEyFpbEVV1hgJCoGhm1ZsjzwibAOOZevgEHZhWg/640?wx_fmt=png&from=appmsg)

计数器算法存在一个问题：窗口切换时可能会出现流量突刺（最高2倍）。  
极端情况下，假设每秒限流100，在第1s和第2s分别通100个请求，且第1s的请求集中在后半段，第2s的请求集中在前半段，那么其实在500ms到1500ms这个1s的时间段，通过了200个请求。

![Image 6](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFC5ZQ6CKojUibfvWvBJBMMpf7M5cYj71Qk7ibxym0RQ85MhnawiahfGagQ/640?wx_fmt=png&from=appmsg)

为了解决这个问题，引入了基于滑动窗口的计数器算法。

3.2.2 滑动窗口计数器

滑动窗口计数器算法是计数器算法的改进，解决了固定窗口的流量突刺问题。算法原理：

*   将时间划分为细粒度的区间，每个区间维持一个计数器，每进入一个请求则将计数器加1；
    
*   多个区间组成一个时间窗口，每到一个区间时间后，则抛弃最老的一个区间，纳入新区间；
    
*   若当前窗口的区间计数器总和超过设定的限制数量，则本窗口内的后续请求都被丢弃。
    

![Image 7](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFkGNWZJHUuMBd2I3Wfnev9MEqO6ib9SoAyyAXZibyQ9NBCSGnhhReCAnQ/640?wx_fmt=png&from=appmsg)

滑动窗口本质上是固定窗口更细粒度的限流，将单位时间划分多个窗口，划分的窗口越多，数据越精确。

四、基于 sentinel 的动态限流方案

动态限流是基于 sentinel 的二次开发，具体实现流程和 sentinel 的 QPS 限流类似，可以归纳为三步：数据统计、规则管理、流量校验。

*   数据统计：统计资源（接口/方法/参数）的流量；
    
*   规则管理：管理限流规则，维护资源的限流阈值及参数值优先级；
    
*   流量校验：对比统计到的流量和对应的限流规则，决定当前请求 pass or block。
    

4.1 数据统计

动态限流的数据统计同 sentinel 流量控制模块一样，使用滑动窗口计数器算法统计当前的流量。

具体来讲，sentinel 流量控制中的数据统计，是将1s的时间窗细分为多个窗口，按窗口维度统计资源信息，包括请求总数、成功总数、异常总数、总耗时、最小耗时、最大耗时等。

动态限流的数据统计，同样是将1s的时间窗细分为多个窗口，不同的是窗口的统计维度是各个参数值通过的总流量。

具体实现上，每个资源有唯一的 bucket，bucket 内维护一个固定数量的滑动窗口，窗口中的 value 是一个 hash 结构，hash key 为限流参数的参数值，value 为参数值在当前时间窗口的请求量。

![Image 8](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFbPnjA1VAzG0CXKqfWSyZIBRa6tJn0de4QKibQEnt1tiaO6icnbZ4czh9Q/640?wx_fmt=png&from=appmsg)

参数值流量统计流程：

1.  系统收到请求后，首先找到当前资源的 bucket；
    
2.  再根据当前时间戳对 bucket 内的窗口数量取余，定位到当前时间窗；
    
3.  当前时间窗内参数值的请求量+1。
    

4.2 规则管理

规则管理模块：配置和管理限流规则。

限流规则通过zk实现从后台到端上的同步。后台配置好限流规则后，将限流规则同步到zk；客户端监听zk消息变更，同步最新的限流规则。

![Image 9](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFgQTic7ibibgECvYPUaSiaIMdAC9o5ZERK07PicZgib8MU2UOkicBkE9IFwOpw/640?wx_fmt=png&from=appmsg)

4.3 流量校验

4.3.1  参数临界点

对于动态限流而言，参数的限流阈值不是固定的，只有参数优先级的概念，所以校验的第一步是要找到限流**阈值优先级的临界点。**

![Image 10](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFersq698K3owDOxIec5ia3oqlPYPn2Xo9icRF55XYa7TiaT5Rf1rDfQZgA/640?wx_fmt=png&from=appmsg)

如果参数优先级临界点已知，只需要判断流量参数的优先级大小。如果请求的优先级高于阈值参数的优先级，pass；反之，如果请求的优先级低于阈值参数的优先级，block；优先级相等，按接口阈值限流。

那么如何确认当前限流的优先级呢？

4.3.2 细分窗口

当前限流阈值配置一般为秒级别的限流，细分滑动窗口，就是将1s的窗口划分为N个更小的时间窗，只要N足够大，就可以将前N-1个窗口已经统计到的参数流量近似当做这一秒的流量，进而就可以计算出临界参数的优先级。  
具体来讲，每一个窗口中都记录了参数的请求数量，所以只要将前N-1个窗口的流量累加，就可以得到各个参数在当前这1s内的总请求量；之后按照参数的优先级从高到低，依次累加流量并与阈值比较，如果累加到某个参数时大于限流阈值，则这个参数对应的优先级即为限流阈值优先级的临界点。

![Image 11](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibF0Va3hh7b2VGukyWBdT8wfpyCv4U3Z7JTTxRsllNATfVEwhwKgx4zmQ/640?wx_fmt=png&from=appmsg)

上面分析都是基于最理想情况：将1s的窗口无限细分。考虑到滑动窗口粒度越小，统计数据计算的越准确，但同时占用的资源也越多，计算越复杂，时延也越高，所以在实际应用中，1s的窗口不可能无限细分，是否有更好的优化方案呢？

4.3.3 动态预测

上面是将1s的窗口划分为N个更小的时间窗，将前N-1个窗口近似看成1s，利用前N-1个窗口的统计数据，来判断当前窗口是否需要限流。

N-1→ N → 1s，N越大误差越小，反之N越小误差就越大，为了弥补N大小引起的计算误差，将统计窗口朝前挪一个，即用最近1s已有的统计数据，来判断当前窗口是否需要限流。

换一种说法：用最近1s已有的统计数据计算临界点参数，预测当前窗口的请求是否需要限流。如果当前请求参数的优先级高于临界点参数，pass；低于临界点参数，block；等于临界点参数，部分通过。

![Image 12](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFKRyjcicSvMe05Eoh4Qesic3e8BRI06icIbibFlkd3D0A7xPgtg5reODv8g/640?wx_fmt=png&from=appmsg)

综上：动态限流采用**细分窗口**+**动态预测**的方法计算当前限流参数的优先级阈值。

举例说明：对方法 method(String param) 配置动态限流，限流阈值为120，配置 param 具体参数值的优先级为A→ 1, B→ 2, C→ 3（按重要程度划分 A \> B \> C）；假设窗口大小为100ms，即1s细分为10个滑动窗口。  
每次开始新窗口流量计数时，先统计前10个窗口中各参数的请求量，继而按照优先级从高到低进行累加，确认优先级阈值；  
比如统计到前10个窗口中参数A, B, C的请求量均为100，因为A的流量100 < 阈值120，A + B的流量200 \> 阈值120，所以此时临界参数为B；  
窗口接收到新请求后，比较请求参数和临界参数的优先级，比如参数A的请求，因为A的优先级高于B, pass；参数B的临界参数请求，允许部分流量通过；参数C的优先级低于临界参数，block。

4.3.4 double check

经过上面的分析可知，通过滑动窗口+动态预测的方案就可以找到临界点参数，进而根据参数优先级决定当前请求 pass or block。但是在实际时间窗和统计时间窗之间，有一个时间 gap，在这个时间窗内的流量计算有一定的滞后性，比如上面的例子，在新窗口中A的请求全部 pass，如果此时A的流量突刺到1000，那么总体通过的流量就会超过阈值，如下图所示。

![Image 13](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFREafy4PagvfQcQ2P0sVacdtJCMfwbe3H79Siao56sUfbaBvq3btjSyw/640?wx_fmt=png&from=appmsg)

由上图可知，在流量突增的一个时间窗内，当前方案通过的流量会有突刺，为了解决流量突增带来的突刺问题，使用 double check 进行校验；check1 为细分窗口+动态预测方案，通过 check1 的流量可能会有突刺；增加 check2 对资源进行限流，保证被保护资源通过的总流量不超过阈值。

![Image 14](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFoUQwMFiadqwLjCaeHlR0pEuZWFdklQDuLz7LrUgNT5gDJxRZUaRfc8A/640?wx_fmt=png&from=appmsg)

double check 流量在应对流量突增时的流量情况：

![Image 15](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFP8I98a8f482Q9zRMHOEOLm9vCfU90RRA36UINr7OXukb5RlSDtSaJg/640?wx_fmt=png&from=appmsg)

4.4 整体架构

复用 sentinel 责任链+ SPI 架构，使用独立 SDK 打包方式嵌入动态限流模板，不影响原 sentinel 处理流程，按需引入。

![Image 16](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFvNazicZWI7yzia9XicNR3iamy87ZgtZtDfMjWRKdDfuNibB6iaIPyhBIWOQA/640?wx_fmt=png&from=appmsg)

4.5 实现效果

动态限流配置生效后，可通过监控查看各配置参数通过/拒绝的请求量，实现限流功能的可视化。

![Image 17](https://mmbiz.qpic.cn/sz_mmbiz_png/4g5IMGibSxt4LAkvHeRiaPMTCibW6LWPeibFnbhNnUao3Piac2TibvapkniabQPfict1Mfu4LWZ4Sw0k2jSUCKMYwKDnGA/640?wx_fmt=png&from=appmsg)

如上图所示，配置某个资源的单机限流阈值为50，这一秒内的总请求量为74，通过50个请求，拒绝14个请求（其中配置限流的参数 xx.scene.priority1、xx.scene.priority2、xx.scene.priority3 在这一秒通过的请求数量分别为2个、16个、2个；其它参数通过30个请求，拒绝14个请求）。

解释：在这一秒内，配置的三个参数总请求量为20（2+16+2），小于阈值50，全部通过；其它参数总流量为44，这一秒的总请求量为64（20+44），大于限流阈值50，所以其它参数共通过30个请求，拒绝14个请求。

五、总结

本文介绍了一种基于 sentinel 进行二次开发的动态限流解决方案，提供更细粒度、能够根据流量动态调整限流阈值的参数级限流方法，是对 sentinel 限流功能的补充和拓展。

*   对比 sentinel 的 QPS 限流，动态限流方案提供了更细粒度的参数级别的限流；
    
*   对比 sentinel 的热点参数限流，热点参数限流是对参数的定量限流，适用于参数大流量场景，比如对某个频繁请求的参数（id/商品）进行限流；  
    动态限流根据配置的参数优先级（重要程度）进行限流，限流的阈值参数会根据资源的流量动态调整，pass 高优参数，block 低优参数，限流重点是“保核心”。
    

综上，动态限流是对 sentinel 限流功能的补充，用户可以结合具体场景配置不同的限流方案。

END

猜你喜欢

[一次基于AST的大规模代码迁移实践](http://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247499353&idx=2&sn=3b0d7ac6dbe8c1b5ad87effa0df9d87f&chksm=ebdb8ecbdcac07dd7371f570cd73c12d11627e923cedf900400bb4386f50c4e5b8dd8e0100c2&scene=21#wechat_redirect)

[TimeWheel 算法介绍及在应用上的探索](http://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247499232&idx=1&sn=082488e84061c2414ebe67f7ad272c33&chksm=ebdb8d72dcac0464da939b232209344ef1a2c54cc5cfc1f7855ae44212b08ee47f9d157e2e33&scene=21#wechat_redirect)

[Cookie的secure属性引起循环登录问题分析及解决方案](http://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247499233&idx=1&sn=0203f83cd5b0ea8609ad428710bf61eb&chksm=ebdb8d73dcac046564f212fce42a1f1121de09f49615a21a7a5614dac198eac497db66d09fdf&scene=21#wechat_redirect)

  

预览时标签不可点

![Image 18](https://mp.weixin.qq.com/s/lFuXVBUW_PkrBp4NoAFTig)Scan to Follow

继续滑动看下一个

轻触阅读原文

![Image 19](http://mmbiz.qpic.cn/mmbiz_png/4g5IMGibSxt45QXJZicZ9gaNU2mRSlvqhQd94MJ7oQh4QFj1ibPV66xnUiaKoicSatwaGXepL5sBDSDLEckicX1ttibHg/0?wx_fmt=png)

vivo互联网技术

向上滑动看下一个

[Got It](javascript:;)

 

![Image 20](https://mp.weixin.qq.com/s/lFuXVBUW_PkrBp4NoAFTig) Scan with Weixin to  
use this Mini Program

[Cancel](javascript:void\(0\);) [Allow](javascript:void\(0\);)

[Cancel](javascript:void\(0\);) [Allow](javascript:void\(0\);)

× 分析

 : ， .   Video Mini Program Like ，轻点两下取消赞 Wow ，轻点两下取消在看 Share Comment Favorite
