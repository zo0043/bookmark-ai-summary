Title: 从零打造：基于实时 CPU 使用率的 Kubernetes 自定义调度器揭开Kubernetes调度的神秘面纱！本文通过

URL Source: https://juejin.cn/post/7427399875236528191

Markdown Content:
我是 LEE，老李，一个在 IT 行业摸爬滚打 17 年的技术老兵。

不知不觉中，我从一个周更的博主变成了一个月更的博主。这是为什么呢？因为我并不想随波逐流，去追逐那些浮华的"流量文章"。我坚持只分享真正有价值的内容，而不是为了更新而更新。我的目标是通过自己的学习和实践，将复杂的技术知识简单化，通过易于理解的代码示例和实际操作，让更多人能够进行实战学习，从而提高自己的技术水平。同时，我也希望在这个过程中能够结识一些志同道合的朋友，一起学习，共同进步。

前言
--

那么今天要分享的主题是什么呢？emmm...我们将深入探讨如何开发一个自定义的 Kubernetes 控制器。这个主题乍看之下可能显得颇具挑战性，涉及的理论也相当深奥。对于普通的技术爱好者来说，短时间内可能难以完全理解。但是，请不要担心！我会尽我所能将这个复杂的主题简化，通过浅显易懂的代码示例和实际操作步骤，力求让大家在阅读完这篇文章后能够轻松掌握以下关键知识点：

1.  Kubernetes 控制器的本质是什么？它的工作原理是怎样的？
2.  为什么我们需要开发自定义的 Kubernetes 控制器？它们在实际应用中有哪些场景？
3.  如何着手开发一个自定义的 Kubernetes 控制器？有哪些快速上手的方法和工具？

乍一看，这篇文章的立意似乎很高，内容也相当丰富。确实，我们要涵盖的知识点并不少。那么，如何在有限的篇幅内将这些内容清晰地呈现出来呢？这就需要我投入更多的时间和精力去梳理和编写了。我会采用"化繁为简"的方式，将这些看似复杂和深奥的知识点转化为易于理解和掌握的内容。我的目标是：**让我们一起把技术的复杂度降下来，让学习变得简单而有趣！**

接下来，让我们开始这段精彩的 Kubernetes 控制器开发之旅吧！我相信，通过本文的学习，你将能够掌握开发自定义 Kubernetes 控制器的基本技能，为你在云原生领域的技术探索打开一扇新的大门。

万事皆有因
-----

近期，我们公司进行了大规模的 Flink 计算任务迁移，从 Yarn 集群转向 Kubernetes 集群。在短短两个月内，我们成功迁移了 3000 多个 Flink 任务。这个过程涉及任务提交、监控以及图任务优化等多个方面，颇具挑战性。就像是在玩一场巨大的俄罗斯方块游戏，每个任务都是一块不同形状的方块，我们需要巧妙地将它们安排到合适的位置。

随着迁移任务的增多，我们遇到了 Kubernetes 集群资源分配的瓶颈。主要问题是局部节点过热，导致新调度到这些节点的 TaskManager Pod 性能下降。这就像是在一个拥挤的电梯里，每个人都想挤进去，结果大家都动弹不得。为解决这个问题，我们需要优化 TaskManager Pod 的调度策略。

**经过深入研究，我们发现了一些关键特点：**

1.  TaskManager Pod 的资源使用率会随数据量变化而波动，就像是一个贪吃的小胖子，胃口时大时小。
2.  每次任务提交都会生成全新的 TaskManager Pod，而非复用旧的。这就像是每次吃饭都要换一套全新的餐具，虽然干净卫生，但未免有些浪费。
3.  我们的 Flink 任务主要是图计算任务，TaskManager Pod 之间存在明确的依赖关系。这就像是一个复杂的亲戚关系网，每个 Pod 都有自己的"亲朋好友"。

这些特点使得优化调度变得复杂。尤其是当多个高资源消耗的任务集中在同一节点时，新任务的调度可能导致节点过载。就像是在一个已经很拥挤的派对上，突然又来了一群饥肠辘辘的客人。

### 案例展示：为 Flink 任务定制 TaskManager Pod 调度器

为了提高 Flink 任务在 Kubernetes 上的运行效率，我们考虑开发一个自定义的 Kubernetes 控制器来自动优化 TaskManager Pod 的调度。这不仅可以减少人工干预，还能显著提升任务性能。让我们来看看这个方案可以解决哪些问题，以及可能面临的挑战。

#### 1\. 现有问题

1.  Kubernetes 默认调度器无法充分理解 Flink 任务的特殊需求，这类似于非专业人士尝试安排高度专业化的工作。
2.  TaskManager Pod 分布不均会导致性能下降，这种情况可以比作资源分配的不平衡。
3.  手动调度不仅耗时，还容易出错，这种复杂性堪比手工进行大规模数据计算。
4.  某些节点的资源利用率过高，这种状况类似于系统中的某些组件超负荷运转。

#### 2\. 潜在挑战

1.  理解并实现复杂的调度规则，这个过程的复杂度可以类比为解决高难度的逻辑问题。
2.  动态监控和响应资源使用变化，这需要系统能够快速适应不断变化的环境。
3.  处理新提交任务的调度需求，这相当于在已经紧密排列的系统中找到合适的位置插入新元素。
4.  平衡任务性能和节点资源利用率，这需要在效率和资源优化之间找到最佳平衡点。
5.  支持不同类型 Flink 任务的调度需求，这要求系统具有高度的灵活性和适应性。
6.  实时监控集群资源和任务运行状态，这需要建立一个全面且持续的监控机制。

#### 3\. 实战效果

这个是我们根据 Kubernetes 节点 CPU 和内存使用情况，进行专门研究的调和算法。在 Kubernetes 节点不同的 CPU 和内存使用率下，我们如何给这个节点评分，从而影响 TaskManager Pod 的调度。

**评分算法展示** ![Image 1: custom-scheduler-2.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fdf4ae904fd74866b27a5c172e340133~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6Lev5Y-jSVTlpKflj5RfS1VNQQ==:q75.awebp?rk3s=f64ab15b&x-expires=1730035389&x-signature=4hdbWfaMCc8UQ5wnhAJGgaK16gI%3D)

**运行效果展示** ![Image 2: custom-scheduler-3.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7dd10f1ce733423a999d4415521cd5a7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6Lev5Y-jSVTlpKflj5RfS1VNQQ==:q75.awebp?rk3s=f64ab15b&x-expires=1730035389&x-signature=Z8%2F0q78vrUjlRJJxohdwrL5YegI%3D)

通过开发这个自定义 Kubernetes 控制器，我们为 Flink 任务创建了一个智能的"调度助手"，确保 TaskManager Pod 能够找到最合适的部署位置，从而提高任务性能并优化集群资源利用率。这就像是给每个 Pod 配备了一个私人管家，帮它们找到最舒适的"住处"。

自定义 Kubernetes 调度器的五大应用场景
-------------------------

我们不禁要问：这个"神奇的魔方"在现实世界中能解决哪些难题？让我们一起来揭开这个百宝箱，看看里面藏着哪些宝贝。

### 1\. 任务调度优化

自定义调度器就像是一个量身定制的私人裁缝，能够精准满足特定工作负载的独特需求：

*   **特定应用优化**：例如我们的 Flink 任务，自定义调度器可以考虑 TaskManager Pod 之间的依赖关系，优化图计算任务的性能。
*   **资源敏感型应用**：对于 CPU 密集型或内存密集型应用，调度器可以根据实时资源使用情况，选择最合适的节点。
*   **数据局部性**：对于大数据处理任务，调度器可以将计算任务调度到数据所在的节点，减少数据传输，提高处理效率。

### 2\. 资源利用率提升

自定义调度器堪比一个全能型体育教练，能够统筹兼顾各种资源，让每一分资源都物尽其用：

*   **多维度资源调度**：除了 CPU 和内存，还可以考虑网络带宽、磁盘 I/O 等因素，实现更精细的资源分配。
*   **动态负载均衡**：通过实时监控数据（如 Prometheus 指标），动态调整 Pod 分布，避免局部节点过热。
*   **资源预留与超售**：根据历史数据和预测模型，合理设置资源预留和超售策略，提高整体资源利用率。

### 3\. 高可用性保障

自定义调度器就像是一个未雨绸缪的风险管理专家，能够确保系统在面对各种突发状况时，依然能够稳如泰山：

*   **跨故障域分布**：将关键服务的 Pod 分散到不同的物理机、机架或可用区，提高系统整体可用性。
*   **亲和性与反亲和性**：通过精细控制 Pod 的分布，避免单点故障，同时确保相关服务的网络延迟最小化。
*   **灾难恢复优化**：在发生故障时，快速进行 Pod 重新调度，最小化服务中断时间。

### 4\. 业务场景定制

自定义调度器就像是一个通晓各行各业规则的法律顾问，能够满足各种特定行业或业务的独特需求：

*   **合规性要求**：对于金融、医疗等行业，调度器可以确保敏感数据只在符合特定安全标准的节点上处理。
*   **性能优化**：针对特定业务场景（如实时流处理、批量数据分析）优化调度策略，提升应用性能。
*   **成本优化**：在混合云或多云环境中，根据不同资源的成本和性能特性，优化工作负载分布，降低运营成本。

### 5\. 多租户资源隔离

自定义调度器可以化身为一个精明的资源管理大师，在多租户环境中实现公平、高效的资源分配：

*   **资源配额管理**：为不同租户设置资源使用上限，确保公平分配和避免资源争抢。
*   **优先级调度**：根据租户的服务等级协议（SLA），为不同优先级的任务分配合适的资源。
*   **安全隔离**：通过调度策略确保不同租户的工作负载运行在隔离的节点或命名空间中，增强安全性。

这些丰富多样的应用场景，充分展示了自定义 Kubernetes 调度器的强大潜力。无论是在复杂的企业环境中优化资源分配，还是在特定领域满足独特需求，它都能大显身手。

让我们开始吧
------

如果你也想跟我们一样能够开发一个自定义的 Kubernetes 控制器，那么你来对地方了。接下来，我将带领大家一步步实现一个类似的控制器（之前展示的案例是我们公司内部的自定义调度器，这里讲解是一个 Demo 案例），并详细讲解每个步骤的原理和实现方法。相信通过这个案例，你将对 Kubernetes 控制器的开发有更深入的理解，也能够为你的工作和学习带来更多的启发。

### I. Kubernetes 调度器 101

在开始开发自定义的 Kubernetes 控制器之前，我们有必要先了解一下 Kubernetes 的调度器是如何工作的。这样有助于我们更好地理解自定义控制器的作用和实现方式。就像是在学习开车之前，我们需要先了解汽车的基本构造和工作原理。

#### 1\. 调度器的作用

Kubernetes 调度器是 Kubernetes 集群中的一个核心组件，主要负责将 Pod 调度到合适的节点上运行。它的作用是根据用户定义的调度策略和节点资源情况，为每个 Pod 分配一个合适的节点，从而实现集群资源的高效利用。在某种程度上，调度器是 Kubernetes 集群的"大脑"，它决定了哪些 Pod 应该在哪些节点上运行，以及如何在这些节点上分配资源。就像是一个精明的房产经纪人，为每个"租客"（Pod）找到最合适的"房子"（节点）。

#### 2\. 调度器的工作流程

**调度器工作流程** ![Image 3: custom-scheduler-4.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ed805cab20ce4baea8c8c52a877d0966~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6Lev5Y-jSVTlpKflj5RfS1VNQQ==:q75.awebp?rk3s=f64ab15b&x-expires=1730035389&x-signature=gdDis8skAUBipZoJyoIpI4AUysY%3D)

Kubernetes 调度器的工作流程可以分为以下几个步骤：

1.  **Pod 列表获取**：调度器首先会获取所有待调度的 Pod 列表。这些 Pod 是已经创建但尚未分配到任何节点的。这个过程类似于学校为新生准备分配宿舍。
    
2.  **节点列表获取**：接下来，调度器会获取集群中所有可用节点的列表。这些节点相当于可供分配的宿舍楼。
    
3.  **过滤节点**：调度器会根据一系列预定义的过滤条件（如节点的可用资源、节点的标签、Pod 的亲和性和反亲和性规则等）筛选出一组合适的节点。这一步骤可以比作根据学生的特殊要求（如需要独立卫浴、靠近图书馆等）来筛选合适的宿舍。
    
4.  **优选节点**：在过滤后的节点中，调度器会根据一系列优选规则（如节点的负载均衡、Pod 的优先级等）为每个 Pod 选择最优的节点。这个过程类似于在符合基本要求的宿舍中，选择最适合学生的那一个。
    
5.  **绑定 Pod**：最后，调度器会将 Pod 绑定到选定的节点上，使其开始运行。这相当于学生最终入住分配好的宿舍。
    

#### 3\. 调度策略

Kubernetes 调度器支持多种调度策略，用户可以根据需求自定义调度策略。例如：

*   **资源请求和限制**：用户可以为 Pod 设置 CPU 和内存的请求和限制，调度器会根据这些设置选择合适的节点。
    
    例如，一个 Pod 请求了 2 个 CPU 和 4 GB 内存，调度器会寻找那些有足够资源的节点来运行该 Pod。这可以类比为为一个需要较大空间的学生寻找合适的宿舍。
    
*   **节点亲和性和反亲和性**：用户可以指定 Pod 应该调度到哪些节点或不应该调度到哪些节点。
    
    例如，某些工作负载可能需要运行在特定的硬件或地理位置的节点上，这时可以通过节点亲和性进行指定。这类似于某些学生可能需要住在特定的宿舍楼（如研究生宿舍）。
    
*   **Pod 亲和性和反亲和性**：用户可以指定 Pod 应该与哪些其他 Pod 一起调度或不应该一起调度。
    
    例如，为了高可用性，可以将相同类型的 Pod 分布到不同的节点上，避免单点故障。这种策略类似于避免将所有篮球队员安排在同一个宿舍，以防止他们一起感冒导致比赛无法进行。
    
*   **污点和容忍度**：通过在节点上设置污点（Taints），以及在 Pod 中设置容忍度（Tolerations），可以控制哪些 Pod 可以被调度到特定节点上。
    
    例如，某些节点可能专门用于高优先级任务，通过设置污点限制普通 Pod 被调度到这些节点。这可以比作设置特殊的宿舍楼，只有特定类型的学生（如运动员）才能入住。
    

#### 4\. 调度器内部机制

**调度器内部机制图示** ![Image 4: custom-scheduler-5.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/375d2a672e334734876408825f1e55c6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6Lev5Y-jSVTlpKflj5RfS1VNQQ==:q75.awebp?rk3s=f64ab15b&x-expires=1730035389&x-signature=4H4MdYaTzhjXj1o%2BWgmFNG%2Fo%2Fbo%3D)

##### 4.1 过滤器（Predicates）

过滤器就是调度器用来筛选出适合运行 Pod 的节点的条件。常见的过滤器包括：

*   **节点资源可用性**：检查节点是否有足够的 CPU、内存等资源来运行 Pod。就像是检查宿舍是否有足够的床位和桌椅。
*   **硬件/软件/策略要求**：例如，Pod 需要特定的 GPU，或者节点需要具备某些标签。这就像是检查宿舍是否配备了特定的设施（如空调、独立卫浴等）。
*   **拓扑约束**：确保 Pod 分布在不同的可用区、不同的物理主机等，以提高可靠性。这就像是将学生分散到不同的宿舍楼，以防止某栋楼出现问题影响所有学生。

##### 4.2 优选器（Priorities）

优选器用来在过滤后的节点中评分，并选择评分最高的节点。常见的优选策略包括：

*   **最小化资源浪费**：选择资源利用率最低的节点，以便更好地利用集群资源。这就像是优先选择人数较少的宿舍，以充分利用所有宿舍资源。
    
*   **负载均衡**：确保负载均匀分布到各个节点，避免某些节点过载。这就像是尽量让每个宿舍的入住率保持在一个合理的水平。
    
*   **亲和性/反亲和性优先级**：根据 Pod 的亲和性或反亲和性规则，为节点打分。这就像是根据学生的喜好和要求为宿舍评分。
    

##### 4.3 调度算法

Kubernetes 调度器采用的是"先过滤再优选"的算法流程。具体步骤为：

1.  **过滤阶段**：使用一系列过滤条件（Predicates）筛选出符合要求的节点。
2.  **优选阶段**：对筛选后的节点进行打分（Priorities），从中选择评分最高的节点。
3.  **绑定阶段**：将 Pod 绑定到选定的节点上。

这就像是先根据学生的基本要求筛选出合适的宿舍，然后根据各种因素为这些宿舍打分，最后选择得分最高的宿舍并安排学生入住。

#### 5\. 调度器的扩展性

Kubernetes 调度器设计为高度可扩展的，通过**调度器框架**（Scheduler Framework）允许用户自定义调度逻辑。后面我们将基于这个框架来开发自定义的调度器。这就像是学校提供了一个灵活的宿舍分配系统，允许管理员根据特定需求定制分配规则。

*   **调度器插件（Plugins）**：用户可以编写自定义插件，插入到调度流程中的不同阶段，以实现特定的调度需求。就像是在宿舍分配系统中添加自定义的筛选和评分模块。
    
*   **调度器策略**：通过配置不同的调度策略，可以灵活地调整调度行为，以适应不同的应用场景。这就像是根据不同类型的学生（如本科生、研究生、留学生）制定不同的宿舍分配策略。
    
*   **调度器扩展（Scheduler Extenders）**：允许外部服务参与调度决策，提供更复杂的调度逻辑。这就像是引入外部专家来协助宿舍分配决策。
    

#### 6\. 实际应用场景举例

##### 示例场景

假设我们有一个 Kubernetes 集群，其中有三个节点：Node A、Node B 和 Node C。现在有一个待调度的 Pod，它需要 2 个 CPU 和 4 GB 内存。这就像是有一个学生需要一个双人间宿舍。

1.  **资源检查**：
    
    *   Node A 有 4 个 CPU 和 8 GB 内存可用。（相当于一个四人间）
    *   Node B 有 2 个 CPU 和 4 GB 内存可用。（相当于一个双人间）
    *   Node C 只有 1 个 CPU 和 2 GB 内存可用。（相当于一个单人间）
    
    调度器会首先排除 Node C，因为它的资源不足以满足 Pod 的需求。就像是单人间无法满足需要双人间的学生。
    
2.  **过滤节点**：
    
    *   Node A 和 Node B 通过了资源和其他基础过滤条件。
3.  **优选节点**：
    
    *   假设 Node A 当前负载较低，而 Node B 负载较高。
    *   调度器会优先选择 Node A 作为调度目标，以实现负载均衡。这就像是选择人数较少的宿舍楼，以平衡各个宿舍楼的入住率。
4.  **绑定 Pod**：
    
    *   Pod 被成功绑定到 Node A 上，并开始运行。这就像是学生最终被安排到了选定的宿舍。

##### 高级应用

在更复杂的场景中，假设某些 Pod 需要具备特定的硬件资源（如 GPU），调度器需要确保这些 Pod 被调度到具备 GPU 的节点上。此外，通过配置节点亲和性，可以确保关键服务分布在不同的物理主机上，以提高整体系统的可靠性。这就像是为特殊需求的学生（如需要无障碍设施的学生）安排特定的宿舍，同时确保重要的学生组织（如学生会）的成员分散在不同的宿舍楼，以防止突发事件影响整个组织的运作。

### II. 开发自己的 Kubernetes 控制器

在开发自定义的 Kubernetes 控制器之前，还有一个概念需要补充一下，那就是 Kubernetes 控制器分为：InTree 控制器和 OutOfTree 控制器。 这两种控制器的区别在于：InTree 控制器是直接内置在 Kubernetes 源码中的，而 OutOfTree 控制器是独立于 Kubernetes 源码之外的，可以单独开发和部署。而我们今天要开发的自定义控制器就是 OutOfTree 控制器。

#### 1\. 案例背景与目标

在深入理解了 Kubernetes 调度器的基本原理后，我们将开发一个自定义的 Kubernetes 控制器。本案例将展示如何创建一个基于 Prometheus 实时 CPU 使用率数据的自定义调度器。这个调度器将根据节点的实时资源使用情况，为 Pod 选择最优节点。

**本案例的关键步骤包括：**

1.  **Metrics 实时查询**：从 Prometheus 服务获取节点 CPU 使用率的实时数据。
2.  **调度器框架扩展**：利用 Kubernetes 调度器框架实现自定义调度器扩展。
3.  **智能调度算法**：编写基于 CPU 使用率的节点评分逻辑。
4.  **调度器部署与集成**：将自定义调度器部署到 Kubernetes 集群并进行集成测试。
5.  **实际应用指南**：演示如何在 Pod 配置中指定使用自定义调度策略。

#### 2\. 开发环境配置与依赖安装

这里当然使用 Go 作为开发语言，Kubernetes 提供了 Go 语言的客户端库，可以方便地与 Kubernetes 集群进行交互。 我用的是 **Go 1.21.13**。 Go 的安装教程以及与您的 IDE 集成的方法可以在伟大的互联网上都能找到详细教程。

接下来，让我们揭开 Kubernetes 控制器项目构建的神秘面纱，同时为您展示如何孕育出一个最最简单的 Kubernetes 控制器 —— 它可能看起来小巧玲珑，但潜力无限，就像是一颗等待绽放的种子。

**1\. 创建项目目录，并初始化 Go 项目：**

```
$ mkdir custom-scheduler
$ cd custom-scheduler
$ go mod init custom-scheduler
```

然后你能够在目录中看到类似的内容：

```
$ tree
.
└── go.mod
```

**2\. 安装 Kubernetes 客户端库：**

手搓这个 `go.mod` 文件，然后执行 `go mod download` 命令，这样就会自动安装 Kubernetes 客户端库。记得 Kubernetes 的依赖环境非常多，所以这个过程可能会比较慢 —— 就像是在一个拥挤的超市里采购一大堆杂货，你得有耐心。

这里最需要注意的是，Kubernetes 开发库的版本要和你的 Kubernetes 集群版本一致，同时必须要使用 `replace` 指令。还有，很多软件版本不要贪新 —— 别问我怎么知道的，反正我是在这个坑里摔得鼻青脸肿后才学会的。

**go.mod** 文件内容如下（我这里使用 Kubernetes 1.23.17 举例，就像是在时光机里选择了一个特定的时间点）：

```
package custom-scheduler

go 1.21

require (
	github.com/prometheus/client_golang v1.17.0
	github.com/prometheus/common v0.44.0
	github.com/stretchr/testify v1.8.4
	k8s.io/api v0.23.17
	k8s.io/apimachinery v0.23.17
	k8s.io/klog/v2 v2.90.1
	k8s.io/kubernetes v1.23.17
)

// 这里的 replace 测试重点内容，这里根据你的实际情况修改
replace (
	k8s.io/api => k8s.io/api v0.23.17
	k8s.io/apiextensions-apiserver => k8s.io/apiextensions-apiserver v0.23.17
	k8s.io/apimachinery => k8s.io/apimachinery v0.23.17
	k8s.io/apiserver => k8s.io/apiserver v0.23.17
	k8s.io/cli-runtime => k8s.io/cli-runtime v0.23.17
	k8s.io/client-go => k8s.io/client-go v0.23.17
	k8s.io/cloud-provider => k8s.io/cloud-provider v0.23.17
	k8s.io/cluster-bootstrap => k8s.io/cluster-bootstrap v0.23.17
	k8s.io/code-generator => k8s.io/code-generator v0.23.17
	k8s.io/component-base => k8s.io/component-base v0.23.17
	k8s.io/component-helpers => k8s.io/component-helpers v0.23.17
	k8s.io/controller-manager => k8s.io/controller-manager v0.23.17
	k8s.io/cri-api => k8s.io/cri-api v0.23.17
	k8s.io/csi-translation-lib => k8s.io/csi-translation-lib v0.23.17
	k8s.io/dynamic-resource-allocation => k8s.io/dynamic-resource-allocation v0.23.17
	k8s.io/kube-aggregator => k8s.io/kube-aggregator v0.23.17
	k8s.io/kube-controller-manager => k8s.io/kube-controller-manager v0.23.17
	k8s.io/kube-proxy => k8s.io/kube-proxy v0.23.17
	k8s.io/kube-scheduler => k8s.io/kube-scheduler v0.23.17
	k8s.io/kubectl => k8s.io/kubectl v0.23.17
	k8s.io/kubelet => k8s.io/kubelet v0.23.17
	k8s.io/legacy-cloud-providers => k8s.io/legacy-cloud-providers v0.23.17
	k8s.io/metrics => k8s.io/metrics v0.23.17
	k8s.io/mount-utils => k8s.io/mount-utils v0.23.17
	k8s.io/pod-security-admission => k8s.io/pod-security-admission v0.23.17
	k8s.io/sample-apiserver => k8s.io/sample-apiserver v0.23.17
)
```

让你的 go.mod 文件看起来像这样，记得是使用 `go mod download` 命令，而不是 `go mod tidy` 命令。 因为你现在还没有代码，所以 `go mod tidy` 命令会删除你的依赖。

**3\. 初始必要的文件：**

```
$ mkdir cmd
$ mkdir pkg
$ touch cmd/main.go
$ touch pkg/scheduler.go
$ tree
```

然后你能够在目录中看到类似的内容：

```
$ tree
.
├── cmd
│   └── main.go
├── go.mod
├── go.sum
└── pkg
    └── scheduler.go

3 directories, 4 files
```

**4\. 初始化代码内容**

**cmd/main.go** 文件内容如下：

```
package main

import (
	"flag"
	"os"

	"k8s.io/klog/v2"

	"k8s.io/kubernetes/cmd/kube-scheduler/app"
	plugin "custom-scheduler/pkg"
)

func main() {
	klog.InitFlags(nil)
	flag.Parse()
	defer klog.Flush()

	command := app.NewSchedulerCommand(
		app.WithPlugin(plugin.PluginName, plugin.New),
	)

	if err := command.Execute(); err != nil {
		klog.Errorf("Error executing scheduler command: %v", err)
		os.Exit(1)
		return
	}
}

```

**pkg/scheduler.go** 文件内容如下：

```
package pkg

import (
	"context"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/kubernetes/pkg/scheduler/framework"
)

const PluginName = "custom"

type CustomScheduler struct{}

var _ framework.FilterPlugin = &CustomScheduler{}
var _ framework.ScorePlugin = &CustomScheduler{}

func (hs *CustomScheduler) Name() string {
	return PluginName
}

func (hs *CustomScheduler) Filter(ctx context.Context, cycleState *framework.CycleState, pod *corev1.Pod, nodeInfo *framework.NodeInfo) *framework.Status {
	// 实现 Filter 逻辑
	return framework.NewStatus(framework.Success, "")
}

func (hs *CustomScheduler) Score(ctx context.Context, cycleState *framework.CycleState, pod *corev1.Pod, nodeName string) (int64, *framework.Status) {
	// 实现 Score 逻辑
	return 0, framework.NewStatus(framework.Success, "")
}

func (hs *CustomScheduler) ScoreExtensions() framework.ScoreExtensions {
	return nil
}

func New(_ runtime.Object, _ framework.Handle) (framework.Plugin, error) {
	return &CustomScheduler{}, nil
}

```

到此你就可以直接使用 `go build` 命令来构建你的项目了。 如果你构建失败的话，那么你可以检查一下你的 go.mod 文件，看看你的依赖是否正确。

**4\. 构建项目**

```
CGO_ENABLED=0 GOOS=linux GOPROXY=https://goproxy.cn,direct go build -ldflags="-w -s" -o build/custom-scheduler ./cmd/main.go
```

这里的 `-ldflags="-w -s"` 是为了去掉 Go 二进制文件的调试信息，减小二进制文件的体积。

然后你能够在目录中看到类似的内容：

```
$ tree build/
build/
└── custom-scheduler

0 directories, 1 file
```

#### 3\. 自定义调度器的设计与实现

有了上面的基础,我们就可以开始实现自定义调度器了。这次,我们将打造一个基于 Prometheus 实时 CPU 使用率数据的"超级调度员"。这位"调度员"将根据节点的实时资源使用情况,为每个 Pod 找到最适合它的"新家"。就像是一位精明的房产经纪人,不仅要考虑房子的大小,还要关注周边的环境和设施。

**1\. 实时 CPU 使用率数据获取**

要实现这个过程,我们需要一个能与 Prometheus 沟通的"翻译官"。这里,我们选择了 `github.com/prometheus/client_golang` 这个库作为我们的"翻译官"。幸运的是, 这位"翻译官"已经在我们的 `go.mod` 文件中安家落户了, 所以我们可以直接呼唤它为我们服务。

接下来, 让我们一起来编写一些代码,让这位"翻译官"能够准确地从 Prometheus 那里获取我们需要的 CPU 使用率数据。这就像是派遣一位得力助手去收集重要的情报, 为我们的"超级调度员"提供决策支持。准备好了吗? 让我们开始这段精彩的编码之旅吧!

```
$ touch pkg/prometheus.go
```

**pkg/prometheus.go** 文件内容如下：

```

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/api"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/common/model"
	"k8s.io/klog/v2"
)

// PrometheusQuerier 定义了 Prometheus 查询接口
type PrometheusQuerier interface {
	Query(ctx context.Context, query string, ts time.Time) (model.Value, error)
}

// PrometheusClient 实现了 PrometheusQuerier 接口
type PrometheusClient struct {
	client api.Client
	api    v1.API
}

// NewPrometheusClient 创建一个新的 PrometheusClient 实例
func NewPrometheusClient(address string) (*PrometheusClient, error) {
	client, err := api.NewClient(api.Config{
		Address: address,
		RoundTripper: http.RoundTripper(&http.Transport{
			IdleConnTimeout: time.Duration(120) * time.Second,
		}),
	})
	if err != nil {
		return nil, err
	}

	return &PrometheusClient{
		client: client,
		api:    v1.NewAPI(client),
	}, nil
}

// Query 执行 PromQL 即时查询并返回结果
func (pc *PrometheusClient) Query(ctx context.Context, query string, ts time.Time) (model.Value, error) {
	result, warnings, err := pc.api.Query(ctx, query, ts, v1.WithTimeout(defaultTimeout))
	if err != nil {
		return nil, err
	}

	if len(warnings) > 0 {
		klog.Warningf("Instant query: `%s`, returned warnings: %v", query, warnings)
	}

	return result, nil
}

```

这里我们实现了一个 Prometheus 客户端库，用于查询 Prometheus 服务的实时 CPU 使用率数据。这个库就像是一位精通多国语言的翻译官，能够与 Prometheus 进行无障碍沟通。它主要包含两个核心部分：

*   **PrometheusQuerier 接口**：这是我们的"翻译官"的工作说明书。它定义了一个 Query 方法，就像是给翻译官下达了"去问 Prometheus 一些问题"的指令。
*   **PrometheusClient 结构体**：这就是我们的"翻译官"本人了。它不仅知道如何与 Prometheus 对话（实现了 PrometheusQuerier 接口），还带着一个 NewPrometheusClient 方法，就像是一个"翻译官速成指南"，教你如何快速培养出一位称职的翻译官。

当然，这里的代码只是一个简单的示例，就像是翻译官的入门培训。在实际应用中，我们可能需要更复杂的查询逻辑和错误处理机制，就像是让翻译官应对各种复杂的外交场合。不过，这个示例已经足以展示如何与 Prometheus 服务进行基本的交流了。

接下来，我们要编写查询 Prometheus 实时 CPU 使用率数据的逻辑。这里我们使用了一个看似神秘的咒语 `rate(node_cpu_seconds_total{mode="idle"}[5m])`，这个 PromQL 查询语句用于查询节点的 CPU 空闲率。它就像是向 Prometheus 发出的一个精确指令，要求它汇报每个节点在过去一分钟内有多少时间在"偷懒"（idle）。通过解析这些数据，我们就能知道节点的实时 CPU 使用率了。

**2\. 自定义调度器的实现**

要实现这个过程，我们需要在之前的 `pkg/scheduler.go` 文件中实现 Filter 和 Score 逻辑。不过，这次我们要扮演一个公正的评委，主要关注打分逻辑，所以我们只实现 Score 逻辑。

需要实现的 **pkg/scheduler.go** 文件内容如下：

```
func (hs *CustomScheduler) Score(ctx context.Context, cycleState *framework.CycleState, pod *corev1.Pod, nodeName string) (int64, *framework.Status) {
	// 实现 Score 逻辑
	return 0, framework.NewStatus(framework.Success, "")
}
```

说到这里,让我们梳理一下思路。我们的目标是根据 Prometheus 实时 CPU 使用率数据为 Pod 选择最优节点。具体实现逻辑如下:

1.  **获取节点 CPU 使用率数据**: 调用 Prometheus 客户端库,查询节点的实时 CPU 使用率数据。
2.  **解析 CPU 使用率数据**: 解析 Prometheus 查询结果,获取节点的实时 CPU 使用率。
3.  **计算节点评分**: 根据 CPU 使用率计算节点的评分,返回给调度器。节点的 CPU 使用率越低,评分越高,调度器就越倾向于选择这个节点。由于 CPU 使用率是一个 0-100 的百分比值,我们可以简单地将其转换为 0-100 的评分值。

在开发自定义调度器之前,让我们深入了解一下 `Score` 方法的结构和作用。这个方法是 Kubernetes 调度框架中的关键组成部分,用于为每个可能的节点分配一个分数,从而帮助调度器做出最终的调度决策。

```
Score(ctx context.Context, state framework.CycleState, pod v1.Pod, nodeName string) (int64, framework.Status)
```

**参数详解：**

*   **ctx context.Context**：
    
    *   上下文对象，用于传递调度过程中的上下文信息。
    *   可用于处理超时、取消操作等场景。
*   **state \*framework.CycleState**：
    
    *   存储当前调度周期的状态信息。
    *   可以用来在不同的调度阶段之间共享数据。
    *   例如，可以在这里存储之前阶段计算的中间结果，以供后续阶段使用。
*   **pod \*v1.Pod**：
    
    *   待调度的 Pod 对象。
    *   包含 Pod 的完整规格，如资源需求、标签、注解等。
    *   可以根据 Pod 的特性来调整评分逻辑。
*   **nodeName string**：
    
    *   当前正在评分的节点的名称。
    *   用于标识要为哪个节点进行评分。

**返回值说明：**

*   **int64**：
    
    *   节点的评分，范围通常在 0 到 100 之间。
    *   分数越高，表示节点越适合运行该 Pod。
    *   调度器会选择得分最高的节点来部署 Pod。
*   **\*framework.Status**：
    
    *   表示评分过程的状态。
    *   如果评分成功完成，应返回 `framework.NewStatus(framework.Success, "")`。
    *   如果评分过程中遇到错误，可以返回包含错误信息的状态，如 `framework.NewStatus(framework.Error, "error message")`。

**注意事项：**

1.  评分逻辑应该是确定性的，即对于相同的输入应该总是产生相同的输出。
    
2.  评分计算应该尽可能高效，因为它会被频繁调用。
    
3.  可以利用 `CycleState` 来存储和共享计算结果，避免重复计算。
    
4.  评分逻辑应考虑到各种可能影响 Pod 运行的因素，如节点资源利用率、Pod 亲和性等。
    
5.  返回的分数应该在一个一致的范围内，通常是 0-100，以确保与其他评分插件的兼容性。
    

通过精心设计 `Score` 方法，我们可以实现高度定制化的调度逻辑，以满足特定的业务需求和优化目标。

最后，**pkg/scheduler.go** 文件内容如下：

```
package pkg

import (
	"context"
	"fmt"
	"time"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/kubernetes/pkg/scheduler/framework"
	"k8s.io/klog/v2"
)

const (
	PluginName     = "custom"
	PrometheusAddr = "http://prometheus-server.monitoring:9090" // 替换为实际的 Prometheus 地址
)

type CustomScheduler struct {
	prometheusClient *PrometheusClient
}

var _ framework.FilterPlugin = &CustomScheduler{}
var _ framework.ScorePlugin = &CustomScheduler{}

func (cs *CustomScheduler) Name() string {
	return PluginName
}

func (cs *CustomScheduler) Filter(ctx context.Context, cycleState *framework.CycleState, pod *corev1.Pod, nodeInfo *framework.NodeInfo) *framework.Status {
	// 实现 Filter 逻辑，这里我们不做过滤，直接返回成功
	return framework.NewStatus(framework.Success, "")
}

func (cs *CustomScheduler) Score(ctx context.Context, state *framework.CycleState, pod *corev1.Pod, nodeName string) (int64, *framework.Status) {
	// 查询 Prometheus 获取节点 CPU 使用率
	query := fmt.Sprintf("100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\",instance=\"%s\"}[5m])) * 100)", nodeName)
	result, err := cs.prometheusClient.Query(ctx, query, time.Now())
	if err != nil {
		klog.Errorf("Failed to query Prometheus: %v", err)
		return 0, framework.NewStatus(framework.Error, fmt.Sprintf("Failed to query Prometheus: %v", err))
	}

	// 解析查询结果
	var cpuUsage float64
	if result.Type().String() == "vector" {
		vector := result.(model.Vector)
		if len(vector) > 0 {
			cpuUsage = float64(vector[0].Value)
		}
	}

	// 计算评分：CPU 使用率越低，评分越高
	// 将 CPU 使用率 (0-100) 转换为评分 (0-100)
	score := int64((100 - cpuUsage) * 100 / 100)

	klog.Infof("Node %s CPU usage: %.2f%%, Score: %d", nodeName, cpuUsage, score)

	return score, framework.NewStatus(framework.Success, "")
}

func (cs *CustomScheduler) ScoreExtensions() framework.ScoreExtensions {
	return nil
}

func New(_ runtime.Object, _ framework.Handle) (framework.Plugin, error) {
	prometheusClient, err := NewPrometheusClient(PrometheusAddr)
	if err != nil {
		return nil, fmt.Errorf("failed to create Prometheus client: %v", err)
	}

	return &CustomScheduler{
		prometheusClient: prometheusClient,
	}, nil
}

```

此时，我们已经拥有了一个基于 Prometheus 实时 CPU 使用率数据的自定义调度器。这个调度器将根据节点的实时资源使用情况，为 Pod 选择最优节点。通过实现 `Score` 方法，我们可以根据节点的 CPU 使用率为节点打分，从而帮助调度器做出最终的调度决策。

接下来，我们可以使用以下构建指令来编译项目：

```
CGO_ENABLED=0 GOOS=linux GOPROXY=https://goproxy.cn,direct go build -ldflags="-w -s" -o build/custom-scheduler ./cmd/main.go
```

如果一切顺利，你应该能在 `build` 目录下看到生成的二进制文件。然而，仅有这个调度器的二进制文件还不足以部署到 Kubernetes 集群中。我们还需要将其打包成一个 Docker 镜像，然后才能部署到 Kubernetes 集群中。

**3\. 构建 Docker 镜像**

在项目根目录下创建一个 `Dockerfile` 文件，内容如下：

```
# 构建阶段
FROM golang:1.21 as builder

WORKDIR /app

# 复制源代码和 Makefile
COPY . .

# 安装依赖并构建
RUN CGO_ENABLED=0 GOOS=linux GOPROXY=https://goproxy.cn,direct go build -ldflags="-w -s" -o build/custom-scheduler ./cmd/main.go

# 最终阶段
FROM alpine:3.18

# 创建必要的目录
RUN mkdir -p /etc/kubernetes

# 设置工作目录
WORKDIR /app

# 从构建阶段复制编译好的主程序
COPY --from=builder /app/build/custom-scheduler .

# 设置入口点
ENTRYPOINT ["./custom-scheduler"]
```

然后执行以下命令构建 Docker 镜像：

```
$ docker build -t custom-scheduler:latest .
$ docker tag custom-scheduler:latest <your-docker-repo>/custom-scheduler:latest
$ docker push <your-docker-repo>/custom-scheduler:latest
```

最然就可以进入最后的环节了，部署到 Kubernetes 集群中。

**4\. 部署自定义调度器**

部署调度器到 Kubernetes 集群中，需要 RBAC 权限，所以需要创建一个 RBAC 资源清单文件，我一般都是直接使用 cluster-admin 权限的 ServiceAccount 来部署。

在项目根目录下创建一个 `rbac.yaml` 文件，内容如下：

```
apiVersion: v1
kind: ServiceAccount
metadata:
    name: custom-scheduler
    namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
    name: custom-scheduler-clusteradmin
subjects:
    - kind: ServiceAccount
      name: custom-scheduler
      namespace: kube-system
roleRef:
    kind: ClusterRole
    name: cluster-admin
    apiGroup: rbac.authorization.k8s.io
```

有了这个文件，自定调度器就可以监控和管理整个集群了。接下来，我们需要创建一个调度器配置文件，继续创建一个 `configmap.yaml` 文件，内容如下：

```
apiVersion: v1
kind: ConfigMap
metadata:
    name: custom-scheduler-config
    namespace: kube-system
data:
    scheduler-config.yaml: |
        apiVersion: kubescheduler.config.k8s.io/v1beta2
        kind: KubeSchedulerConfiguration
        leaderElection:
          leaderElect: false
          resourceNamespace: kube-system
          resourceName: custom-scheduler
        profiles:
          - schedulerName: custom-scheduler
            plugins:
              score:
                enabled:
                  - name: custom
```

**Tips:** 这里有几个非常重要的注意事项：

1.  `schedulerName: custom-scheduler` 这个名称必须与您的调度器名称一致。它不能与集群中其他调度器重名。此外，其他 Pod 配置中也需要使用这个名称。
2.  `name: custom` 这个名称是在 `pkg/scheduler.go` 文件中定义的。

有了 `configmap.yaml` 和 `rbac.yaml` 两个文件后，最后我们需要创建一个用于部署自定义调度器的 Deployment，继续创建一个 `deployment.yaml` 文件，内容如下：

```
apiVersion: apps/v1
kind: Deployment
metadata:
    name: custom-scheduler
    namespace: kube-system
    labels:
        component: custom-scheduler
spec:
    replicas: 1
    selector:
        matchLabels:
            component: custom-scheduler
    template:
        metadata:
            labels:
                component: custom-scheduler
        spec:
            serviceAccountName: custom-scheduler
            containers:
                - name: scheduler
                  image: <your-docker-repo>/custom-scheduler:latest
                  command:
                      - ./custom-scheduler
                      - --config=/etc/kubernetes/scheduler-config.yaml
                      - --v=5
                  volumeMounts:
                      - name: config
                        mountPath: /etc/kubernetes
            volumes:
                - name: config
                  configMap:
                      name: custom-scheduler-config
```

有了这个文件，我们就可以使用 `kubectl apply -f` 命令来部署自定义调度器了。

```
$ kubectl apply -f rbac.yaml -f configmap.yaml -f deployment.yaml
```

如果一切顺利，你应该能在 `kube-system` 命名空间下看到一个名为 `custom-scheduler` 的 Deployment。这个 Deployment 就是我们刚刚部署的自定义调度器。

**5\. 验证自定义调度器**

为了验证我们的自定义调度器是否生效，我们可以创建一个测试 Pod 并指定使用我们的自定义调度器。让我们一步步来完成这个验证过程。

1.  创建测试 Pod 配置文件

首先，我们创建一个名为 `test-pod.yaml` 的文件，内容如下：

```
apiVersion: v1
kind: Pod
metadata:
    name: test-pod
    namespace: default
spec:
    schedulerName: custom-scheduler
    containers:
        - name: nginx
          image: nginx:latest
          resources:
              requests:
                  cpu: 100m
                  memory: 128Mi
```

注意 `schedulerName: custom-scheduler` 这一行，它指定了使用我们的自定义调度器来调度这个 Pod。

2.  部署测试 Pod

使用以下命令部署测试 Pod：

```
kubectl apply -f test-pod.yaml
```

3.  验证 Pod 调度情况

部署 Pod 后，我们可以通过以下步骤验证调度情况：

a. 检查 Pod 状态：

```
kubectl get pod test-pod -o wide
```

这个命令会显示 Pod 的详细信息，包括它被调度到哪个节点。

b. 查看 Pod 的调度事件：

```
kubectl describe pod test-pod
```

在输出的 Events 部分，你应该能看到类似以下的信息：

```
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  30s   custom-scheduler   Successfully assigned default/test-pod to node-xyz
```

这表明 Pod 已经被我们的自定义调度器成功调度。

c. 检查自定义调度器日志：

```
kubectl logs -n kube-system deployment/custom-scheduler
```

在日志中，你应该能看到关于 Pod 调度的详细信息，包括节点评分和最终选择的节点。

4.  对比测试

为了进一步验证自定义调度器的效果，你可以创建多个 Pod，一些使用默认调度器，一些使用自定义调度器，然后比较它们的分布情况。

5.  性能测试

如果条件允许，你可以进行一些简单的性能测试，比如：

*   同时创建多个 Pod，观察调度速度。
*   在不同负载条件下测试调度结果。

通过这些步骤，你应该能够验证自定义调度器是否按照预期工作，并且能够根据 CPU 使用率做出合理的调度决策。如果发现任何异常或不符合预期的行为，可以回头检查代码实现或配置，进行必要的调整和优化。

课后思考
----

在深入学习了如何开发自定义 Kubernetes 控制器之后，让我们一起探讨几个值得深入思考的问题。这些问题不仅能帮助我们巩固所学知识，还能激发我们在实际项目中应用和优化自定义调度器的灵感。

### 1\. 扩展性与适应性

当前的调度器主要基于 CPU 使用率进行决策，但在实际应用中，我们需要考虑更多因素：

*   内存使用率
*   网络带宽
*   磁盘 I/O
*   特定硬件资源（如 GPU）

如何将这些指标有效地整合到调度决策中？这是一个值得深入研究的问题。此外，不同的业务场景对调度策略的要求也不尽相同。例如，实时数据处理与批量数据分析对资源的需求就大不相同。因此，设计一个能够动态调整调度策略的调度器，将大大提升其适应性和智能化水平。

### 2\. 性能与可扩展性

在大规模集群中，性能和可扩展性成为关键挑战：

1.  **查询优化**：如何减少对 Prometheus 的实时查询，降低性能开销？
    
    *   引入缓存机制
    *   采用数据聚合方法
2.  **分布式调度**：随着集群规模扩大，单点调度器可能无法满足高并发需求。如何设计分布式调度器？
    
    *   负载均衡策略
    *   数据一致性保证

### 3\. 容错与高可用

调度器在运行过程中可能遇到各种故障，我们需要考虑：

*   Prometheus 服务不可用时的备选方案
*   调度器自身异常的处理机制
*   多副本部署和热备份策略

这些措施能确保在部分实例失效时，系统依然能够正常运行。

### 4\. 安全性考虑

安全性是不容忽视的重要方面：

1.  权限管理：如何确保调度器遵循最小权限原则？
2.  数据保护：如何防止敏感数据泄露或篡改？
3.  抗攻击能力：如何设计调度器以抵御 DDoS 攻击等恶意行为？

### 5\. 监控与调优

为确保调度器长期有效运行，我们需要关注：

*   关键性能指标（KPI）的选择和监控
*   日志记录和分布式追踪机制的实现
*   基于监控数据的持续优化策略

通过这些措施，我们可以不断提升调度器的效率和智能化水平。

思考这些问题将帮助我们更全面地掌握 Kubernetes 控制器的开发与优化，为应对实际工作中的复杂挑战做好准备。

总结
--

在本文中，我们系统性地探讨了如何开发一个针对 Flink 任务的自定义 Kubernetes 控制器，特别是优化 TaskManager Pod 的调度。通过这个实际案例，我们不仅掌握了 Kubernetes 调度器的核心原理，还深入实践了如何根据特定需求定制调度逻辑，从而显著提升了集群资源利用率和任务性能。

### 1\. 主要收获

1.  **深入理解 Kubernetes 调度器**
    
    *   工作流程：从 Pod 列表获取到 Pod 绑定的全过程
    *   调度策略：资源请求、节点亲和性、污点容忍度等
    *   内部机制：过滤器、优选器和调度算法的具体实现
2.  **实际问题的解决方案** 我们成功解决了 Flink 任务在 Kubernetes 上运行时遇到的资源分配瓶颈问题。通过自定义调度器，我们优化了 TaskManager Pod 的分布，避免了节点过载现象，显著提升了任务的执行效率。基于 Prometheus 实时 CPU 使用率的数据，我们设计并实现了高效的节点评分逻辑，实现了精细化的资源调度。
    
3.  **自定义 Kubernetes 控制器的开发流程**
    
    *   调度器框架扩展
    *   调度逻辑插件的编写和集成
    *   部署与集成测试
    *   Pod 配置中指定自定义调度策略的方法
4.  **性能优化与扩展性设计** 我们探讨了通过缓存机制和并行调度提高调度器性能的方法，确保在大规模集群中依然保持高效。同时，我们设计了可扩展的调度器架构，支持未来业务需求的变化和多样化任务的调度需求。
    
5.  **监控与持续优化** 我们建立了调度器监控机制，实时追踪关键性能指标，帮助快速定位和解决问题。通过详细的日志记录和分布式追踪机制，我们能够有效地监控调度器的运行状态，并基于监控数据制定持续优化策略。
    

### 2\. 展望与未来

开发自定义 Kubernetes 控制器是一项具有深远意义的技术实践。随着云原生技术的不断发展，定制化控制器将成为优化和管理复杂分布式系统的重要工具。未来，我们可以进一步探索以下方向：

1.  **更加复杂的调度策略**：结合更多业务场景和性能需求，设计出更加智能和灵活的调度策略。
    
2.  **跨集群与多云调度**：实现跨集群的资源调度和任务分配，提升整体资源利用率。
    
3.  **机器学习驱动的调度决策**：引入机器学习算法，基于历史数据和预测模型，实现更加前瞻性的调度决策。
    
4.  **全面的安全与合规性**：在调度器设计中全面考虑安全与合规性，确保系统在各种环境下的可靠性和安全性。
    

通过不断学习和实践，我们不仅能够在 Kubernetes 生态系统中发挥更大的作用，还能推动技术创新，实现更高效、更智能的云原生应用部署与管理。希望这篇文章能够激发你的兴趣，帮助你在 Kubernetes 控制器开发的道路上迈出坚实的一步，开启更加广阔的技术探索之旅。

感谢你阅读本文，希望你不仅掌握了开发自定义 Kubernetes 控制器的核心技能，还获得了应对实际项目挑战的信心和方法。技术的世界充满了无限的可能性，愿你在未来的学习和工作中，不断探索、持续成长，创造出更多令人惊叹的成果！
