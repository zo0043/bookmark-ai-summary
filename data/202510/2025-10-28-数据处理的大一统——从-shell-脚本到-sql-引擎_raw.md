Title: 数据处理的大一统——从 Shell 脚本到 SQL 引擎

URL Source: https://www.qtmuniao.com/2023/08/21/unify-data-processing/

Published Time: 2023-08-21T07:44:11.000Z

Markdown Content:
“工业流水线” 的鼻祖，[福特 T 型汽车](https://www.youtube.com/watch?v=As0lqsd2-NI)的电机装配，将组装过程拆成 29 道工序，将装备时间由平均二十分钟降到五分钟，效率提升四倍 ，下图[图源](https://www.motor1.com/features/178264/ford-model-t-factory-cutaway-kimble/)。

![Image 1: T-model-car.png](https://s2.loli.net/2023/08/21/BrMe3j9oapmX8f2.png)

这种流水线的思想在数据处理过程中也随处可见。其核心概念是：

1.   **标准化的数据集合**：对应待组装对象，是对数据处理中各个环节输入输出的一种**一致性抽象**。所谓一致，就是一个任意处理环节的输出，都可以作为任意处理环节的输入。
2.   **可组合的数据变换**：对应单道组装工序，定义了对数据进行变换的一个**原子**操作。通过组合各种原子操作，可以具有强大的表达力。

则，数据处理的本质是：**针对不同需求，读取并标准化数据集后，施加不同的变换组合**。

_作者：木鸟杂记 [https://www.qtmuniao.com/2023/08/21/unify-data-processing](https://www.qtmuniao.com/2023/08/21/unify-data-processing) 转载请注明出处_

[](https://www.qtmuniao.com/2023/08/21/unify-data-processing/#Unix-%E7%AE%A1%E9%81%93 "Unix 管道")Unix 管道
-------------------------------------------------------------------------------------------------------

Unix 管道是一项非常伟大的发明，体现了 Unix 的一贯哲学：

> 程序应该只关注一个目标，并尽可能把它做好。让程序能够互相协同工作。应该让程序处理文本数据流，因为这是一个通用的接口。

> — Unix Pipe 机制发明者 Malcolm Douglas McIlroy

上述三句话哲学正体现了我们提到的两点，标准化的数据集合 —— 来自**标准输入输出**的**文本**数据流，可组合的数据变换 —— 能够协同工作的程序（如像 sort, head, tail 这种 Unix 自带的工具，和用户自己编写的符合管道要求的程序）。

让我们来看一个使用 Unix tools 和管道来解决实际问题的例子。假设我们有一些关于服务访问的日志文件（`var/log/nginx/access.log` ，例子来自 [DDIA](https://ddia.qtmuniao.com/) 第十章），日志的每一行格式如下：

1

2

3

4

5 216.58.210.78 - - [27/Feb/2015:17:55:11 +0000] "GET /css/typography.css HTTP/1.1" 

200 3377 "http://martin.kleppmann.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) 

AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36"

我们的需求是，统计出日志文件中最受欢迎的五个网页。使用 Unix Shell ，我们会写出类似的命令：

1

2

3

4

5

6 cat /var/log/nginx/access.log | 

 awk '{print $7}' | 

 sort | 

 uniq -c | 

 sort -r -n | 

 head -n 5

可以看出上述 Shell 命令有以下几个特点：

1.   每个命令实现的功能都很简单（高内聚）
2.   所有命令通过**管道**进行组合（低耦合），当然这也要求可组合的程序只面向标准输入、标准输出进行编程，无其他副作用（比如输出到文件）
3.   输入输出面向文本而非二进制

此外，Unix 的管道的另一大优点是 —— 流式的处理数据。也即所有程序中间结果并非都计算完成之后，才送入下一个命令，而是边算边送，从而达到多个程序并行执行的效果，这就是流水线的精髓了。

当然，管道也有缺点 —— 只能进行**线性**的流水线排布，这也限制了他的表达能力。

[](https://www.qtmuniao.com/2023/08/21/unify-data-processing/#GFS-%E5%92%8C-MapReduce "GFS 和 MapReduce")GFS 和 MapReduce
-----------------------------------------------------------------------------------------------------------------------

MapReduce 是谷歌 2004 年的论文 [MapReduce: Simplified Data Processing on Large Clusters](https://research.google.com/archive/mapreduce-osdi04.pdf) 提出的，用以解决大规模集群、并行数据处理的一种算法。GFS 是与 MapReduce 配套使用的基于磁盘的分布式文件系统。

MapReduce 算法主要分为三个阶段：

1.   **Map**：在不同机器上并行的对每个数据分区执行用户定义的 `map() → List<Key, Value>` 函数。
2.   **Shuffle**：将 map 的输出结果（KV 对）按 key 进行重新分区，按 key 聚集送到不同机器上， `Key→ List<Value>`。
3.   **Reduce**：在不同机器上并行地对 map 输出的每个 key 对应的 `List<Value>` 调用 reduce 函数。

（下图源 DDIA 第十章）

![Image 2: mapreduce.png](https://s2.loli.net/2023/08/21/vWfR7J5pUTub89i.png)

每个 MapReduce 程序就是对存储在 GFS 上的数据集（标准化的数据集）的一次变换。理论上，我们可以通过组合多个 MapReduce 程序（可组合的变换），来满足任意复杂的数据处理需求。

但与管道不同的是，每次 MapReduce 的输出都要进行 “**物化**”，即完全落到分布式文件系统 GFS 上，才会执行下一个 MapReduce 程序。好处是可以进行任意的、非线性的 MapReduce 程序排布。坏处是代价非常高，尤其考虑到 GFS 上的文件是多机多副本的数据集，这意味着大量的跨机器数据传输、额外的数据拷贝开销。

但要考虑到历史上开创式的创新，纵然一开始缺点多多，但会随着时间迭代而慢慢克服。GFS + MapReduce 正是这样一种在工业界开创了在大规模集群尺度上处理海量数据的先河。

[](https://www.qtmuniao.com/2023/08/21/unify-data-processing/#Spark "Spark")Spark
---------------------------------------------------------------------------------

Spark 便是为了解决 MapReduce 中每次数据集都要落盘的一种演进。

首先，Spark 提出了标准的数据集抽象 ——[RDD](https://www.qtmuniao.com/2019/11/14/rdd/)，这是一种通过**分片**的形式分散在**多机**上、**基于内存**的数据集。基于内存可以使得每次处理结果不用落盘，从而处理延迟更低。基于分片可以使得在机器宕机时，只用恢复少量分片，而非整个数据集。逻辑上，我们可以将其当做一个整体来进行变换，物理上，我们使用多机内存承载其每个分片。

其次，基于 RDD，Spark 提供了多种可灵活组合的算子集，这相当于对一些常用的变换逻辑进行 “**构件化**”，可以让用户开箱即用。（下面图源 [RDD 论文](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)）

![Image 3: rdd-operators.png](https://s2.loli.net/2023/08/21/wTIi7SbOnRmMpZX.png)

基于此，用户可以进行任意复杂数据处理，在物理上多个数据集（点）和算子（边）会构成一个复杂的 DAG （有向无环图）执行拓扑：

![Image 4: rdd-dag.png](https://s2.loli.net/2023/08/21/xuYijZW6GoqSMFd.png)

[](https://www.qtmuniao.com/2023/08/21/unify-data-processing/#%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93 "关系型数据库")关系型数据库
------------------------------------------------------------------------------------------------------------------------------------

关系型数据库是数据处理系统的集大成者。一方面，它对外提供强大的声明式查询语言 ——SQL，兼顾了灵活性和易用性。另一方面，他对内使用紧凑、索引友好的存储方式，可以支撑高效的数据查询需求。关系型数据库系统同时集计算和存储于一身，又会充分利用硬盘，甚至网络（分布式数据库）特点，是对计算机各种资源全方位使用的一个典范。本文不去过分展开关系型数据库实现的各个环节，而是聚焦本文重点 —— 标准的数据集和可组合的算子。

关系型数据库对用户提供的数据基本组织单位是 —— 关系，或者说表。在 SQL 模型中，这是一种由行列组成的、强模式的二维表。所谓强模式，可以在逻辑上理解为表格中每个单元所存储的数据必须要符合该列 “表头” 的类型定义。针对这种标准的二维表，用户可以施加各种关系代数算子（选择、投影、笛卡尔乘积）。

一条 SQL 语句，在进入 RDBMS 之后，经过解析、校验、优化，最后转化成算子树进行执行。对应的 RDBMS 中的逻辑单元，我们通常称之为 —— **执行引擎**，[Facebook Velox](https://github.com/facebookincubator/velox) 就是专门针对该生态位的一个 C++ 库。

传统的执行引擎多使用火山模型，一种属于拉（ pull-based ）流派的执行方式。其基本概念就是以树形的方式组织算子，并从根节点开始，自上而下的进行递归调用，算子间自下而上的以行（row）或者批（batch）的粒度返回数据。

![Image 5](https://pic.imgdb.cn/item/64e31c15661c6c8e549fa073.png)

近些年来，基于推（push-based）的流派渐渐火起来了，DuckDB、Velox 都属于此流派。类似于将递归转化为迭代，自下而上，从叶子节点进行计算，然后推给父亲节点，直到根节点。每个算子树都可以拆解为多个可以并行执行的算子流水线（下图源，[Facebook Velox 文档](https://facebookincubator.github.io/velox/develop/task.html)）

![Image 6: pipeline-break.png](https://s2.loli.net/2023/08/21/RUnOCV2wEtHxFW4.png)

我们把上图顺时针旋转九十度，可以发现他和 Spark 的执行方式如出一辙，更多关于 velox 机制的解析，可以参考我写的[这篇文章](https://zhuanlan.zhihu.com/p/614918289)。

但无论推还是拉，其对数据集和算子的抽象都符合本文一开始提出的理论。

[](https://www.qtmuniao.com/2023/08/21/unify-data-processing/#%E5%B0%8F%E7%BB%93 "小结")小结
----------------------------------------------------------------------------------------

考察完上述四种系统之后，可以看出，数据处理在某种角度上是大一统的 —— **首先抽象出归一化的数据集，然后提供施加于该数据集之上的运算集，最终通过组合的形式表达用户的各种数据处理需求**。

* * *

本文来自我的小报童付费专栏《系统日知录》，专注分布式系统、存储和数据库，有图数据库、代码解读、优质英文播客翻译、数据库学习、论文解读等等系列，欢迎喜欢我文章的朋友订阅👉[专栏](https://xiaobot.net/p/system-thinking)支持，你的支持对我持续创作优质文章非常重要。下面是当前文章列表：

**图数据库系列**

*   [图数据库资料汇总](https://xiaobot.net/post/fb4ca748-53d9-495c-99ca-4049332ad695)
*   [译： Factorization & Great Ideas from Database Theory](https://xiaobot.net/post/6914a8f6-b506-4a37-8b55-849185439d15)
*   [Memgraph 系列（二）：可串行化实现](https://xiaobot.net/post/656d8d73-f8ed-4604-9f14-f77797e877b0)
*   [Memgraph 系列（一）：数据多版本管理](https://xiaobot.net/post/2e8091a0-8363-498f-b609-ce8e23110c9e)
*   [【图数据库系列四】与关系模型的 “缘” 与 “争”](https://xiaobot.net/post/b40fdc23-12a9-4a85-8d3a-e35f6d1b1b0c)
*   [【图数据库系列三】图的表示与存储](https://xiaobot.net/post/66075ce9-fc76-4e35-a91c-90cd611fc732)
*   [【图数据库系列二】 Cypher 初探](https://xiaobot.net/post/77572ed4-723d-4dfd-ba16-5b136ff9a7a3)
*   [【图数据库系列一】属性图模型是啥、有啥不足](https://xiaobot.net/post/23f0bf11-e167-4f80-8415-2eb4ab1797b5)[🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)

**数据库**

*   [译：数据库五十年来研究趋势](https://xiaobot.net/post/af3dc3a7-8d2e-42a8-95c1-3fcc3e6e7045)
*   [译：数据库中的代码生成（Codegen in Databas…](https://xiaobot.net/post/9824cb9f-2289-4895-a938-430d55ba1eba)
*   [Facebook Velox 运行机制解析](https://xiaobot.net/post/ca020297-0901-45d1-8acc-1d884bf1cc84)
*   [分布式系统架构（二）—— Replica Placement](https://xiaobot.net/post/1747d648-0b0d-43f3-b484-c992ad9f6e25)
*   [【好文荐读】DuckDB 中的流水线构建](https://xiaobot.net/post/3327107b-0912-4d7d-9d94-343954f56d5d)
*   [译：时下大火的向量数据库，你了解多少？](https://xiaobot.net/post/20379c9d-0b07-41d7-99aa-3b3900632f53)
*   [数据处理的大一统 —— 从 Shell 脚本到 SQL 引擎](https://xiaobot.net/post/32d80aea-3466-4596-b068-a7115bb7cbaa)
*   [Firebolt：如何在十八个月内组装一个商业数据库](https://xiaobot.net/post/22ffcb53-1cd2-41a5-8307-a28a0d6d6fa6)
*   [论文：NUMA-Aware Query Evaluation Framework 赏析](https://xiaobot.net/post/8cf94d43-a91c-4fe3-b831-615eac8c9e3a)
*   [优质信息源：分布式系统、存储、数据库](https://xiaobot.net/post/28e03032-e09f-4905-8dba-559180b16c00)[🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)
*   [向量数据库 Milvus 架构解析（一）](https://xiaobot.net/post/f778c9db-1b9e-444a-9d67-d40b7af349e4)
*   [ER 模型背后的建模哲学](https://xiaobot.net/post/23a491da-17f8-4df7-9e8a-29a788956b41)
*   [什么是云原生数据库？](https://xiaobot.net/post/29ff61fd-25e2-4104-9446-6ccb702bcf5a)

**存储**

*   [存储引擎概述和资料汇总](https://xiaobot.net/post/f74e36b2-191a-472f-b073-1bcd1404fc38)[🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)
*   [译：RocksDB 是如何工作的](https://xiaobot.net/post/71cf9733-ee74-4ebb-aa27-f63d72af6716)
*   [RocksDB 优化小解（二）：Prefix Seek 优化](https://xiaobot.net/post/6fdd959e-9629-4f7a-ab97-c1a5c42f5ed2)
*   [RocksDB 优化小解（三）：Async IO](https://xiaobot.net/post/e0696c4c-7faf-444a-be40-ba22801c97ff)
*   [大规模系统中使用 RocksDB 的一些经验](https://xiaobot.net/post/7ccc3a71-0c59-4ef3-a54b-1126b321cfd1)

**代码 & 编程**

*   [影响我写代码的三个 “Code”](https://xiaobot.net/post/750e08f9-f667-4459-9d94-53f38c0529dc)[🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)
*   [Folly 异步编程之 futures](https://xiaobot.net/post/6c2cf37c-b7e3-49bc-881e-bf44eba6bcae)
*   [关于接口和实现](https://xiaobot.net/post/46c118ef-90cb-4868-ba10-560459c6fa2a)
*   [C++ 私有函数的 override](https://xiaobot.net/post/df56cd32-27e8-4cc9-bb42-2ff363513499)
*   [ErrorCode 还是 Exception ？](https://xiaobot.net/post/9d8f493d-8eff-42ce-873c-1e81ed6e1cc4)
*   [Infra 面试之数据结构（一）：阻塞队列](https://xiaobot.net/post/84860561-ba56-4de4-ade8-b7320d158586)
*   [数据结构与算法（四）：递归和迭代](https://xiaobot.net/post/edfdbb18-2bb1-49d3-b07f-dd2a2f562929)

**每天学点数据库系列**

*   [【每天学点数据库】Lecture #06：内存管理](https://xiaobot.net/post/a492299e-dd0e-469e-8706-2836e20f81f0)
*   [【每天学点数据库】Lecture #05：数据压缩](https://xiaobot.net/post/819c0294-0ed4-4161-b3c6-8a623136fa62)
*   [【每天学点数据库】Lecture #05：负载类型和存储模型](https://xiaobot.net/post/05ea2cf6-4b3d-416a-924a-3c1f7ad37a1e)
*   [【每天学点数据库】Lecture #04：数据编码](https://xiaobot.net/post/7e6957d6-4fee-42db-a51d-d72f284e2733)
*   [【每天学点数据库】Lecture #04：日志构型存储](https://xiaobot.net/post/5e34ee0f-8fa3-4c7e-9b09-21287e0da639)
*   [【每天学点数据库】Lecture #03：Data Layout](https://xiaobot.net/post/23d6f499-eee7-41b2-b8de-55fb00007cd4)
*   [【每天学点数据库】Lecture #03: Database and OS](https://xiaobot.net/post/b3ad8154-2e29-4ec1-a627-fd3288b5d2a9)
*   [【每天学点数据库】Lecture #03：存储层次体系](https://xiaobot.net/post/ae2e1e35-3dcc-4fbd-9f6b-39e645e99065)
*   [【每天学点数据库】Lecture #01：关系代数](https://xiaobot.net/post/a6e5f976-0e99-4111-a1e9-c0ea853b22bb)
*   [【每天学点数据库】Lecture #01：关系模型](https://xiaobot.net/post/1d3e98a8-0dee-4b79-93d4-a96409413253)
*   [【每天学点数据库】Lecture #01：数据模型](https://xiaobot.net/post/c44168cf-9c3b-4c53-b49e-a3e51e8576ad)

**杂谈**

*   [数据库面试的几个常见误区 🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)
*   [生活工程学（一）：多轮次拆解](https://xiaobot.net/post/2e7835a5-4ad5-45b0-9ebc-d12945e866f1)[🔥](https://xiaobot.net/post/10f4f784-8bb1-4ca3-a635-ee9fb14e3b1d)
*   [系统中一些有趣的概念对](https://xiaobot.net/post/d58eb2fa-fc3d-4a6e-a9fd-b8541dfa51be)
*   [系统设计时的简洁和完备](https://xiaobot.net/post/efe6c74d-f6dc-494c-847b-5fd2138c0f05)
*   [工程经验的周期](https://xiaobot.net/post/34dc3c4b-dd3d-4ca2-8ecc-1efab5ecf709)
*   [关于 “名字” 拿来](https://xiaobot.net/post/de2cc529-0a7e-4186-97e1-ab514ec916cb)
*   [Cache 和 Buffer 都是缓存有什么区别？](https://xiaobot.net/post/664720a5-b943-4568-a810-e278bc6c173c)

* * *

我是青藤木鸟，一个喜欢摄影、专注大规模数据系统的程序员，欢迎关注我的公众号：“**木鸟杂记**”，有更多的分布式系统、存储和数据库相关的文章，欢迎关注。 关注公众号后，回复 “**资料**” 可以获取我总结一份分布式数据库学习资料。 回复 “**优惠券**” 可以获取我的大规模数据系统付费专栏《[系统日知录](https://xiaobot.net/p/system-thinking)》的八折优惠券。

我们还有相关的分布式系统和数据库的群，可以添加我的微信号：qtmuniao，我拉你入群。加我时记得备注：“分布式系统群”。 另外，如果你不想加群，还有一个分布式系统和数据库的论坛（点[这里](https://distsys.cn/)），欢迎来玩耍。

![Image 7: wx-distributed-system-s.jpg](https://s2.loli.net/2021/12/08/Gus9ditcmZo3Ukw.jpg)
