Title: 如何把你的 DeePseek-R1 微调为某个领域的专家？今天我们一起来聊聊大模型的进阶使用：“模型微调” ，也就是较大 - 掘金

URL Source: https://juejin.cn/post/7473309339294695460

Markdown Content:
> 本文视频教程：
> 
> [如何把你的 DeePseek-R1 微调为某个领域的专家？（理论篇）](https://link.juejin.cn/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1WQAUeVEuj%2F "https://www.bilibili.com/video/BV1WQAUeVEuj/")
> 
> [如何把你的 DeePseek-R1 微调为某个领域的专家？（实战篇）](https://link.juejin.cn/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1s2AUe2EBq%2F "https://www.bilibili.com/video/BV1s2AUe2EBq/")

大家好，我是 [ConardLi](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzk0MDMwMzQyOA%3D%3D%26mid%3D2247493407%26idx%3D1%26sn%3D41b8782a3bdc75b211206b06e1929a58%26chksm%3Dc2e11234f5969b22a0d7fd50ec32be9df13e2caeef186b30b5d653836b0725def8ccd58a56cf%23rd "https://mp.weixin.qq.com/s?__biz=Mzk0MDMwMzQyOA==&mid=2247493407&idx=1&sn=41b8782a3bdc75b211206b06e1929a58&chksm=c2e11234f5969b22a0d7fd50ec32be9df13e2caeef186b30b5d653836b0725def8ccd58a56cf#rd")。

前几天发了一篇本地部署大模型的教程文章：《[如何拥有一个无限制、可联网、带本地知识库的私人 DeepSeek？](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FqeKrwJXz_QJE6eNwUOhjsA%3Ftoken%3D1894055887%26lang%3Dzh_CN "https://mp.weixin.qq.com/s/qeKrwJXz_QJE6eNwUOhjsA?token=1894055887&lang=zh_CN")》深受大家喜爱。

![Image 1](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6e4cd400f5be47418ed953bb93c33ca8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=hzeoH%2BVr30vPrWNbavmRN%2Fxx0L8%3D)

同时我也收到了很多小伙伴的反馈，表示本地部署 + 知识库并不能很好的满足一些需求场景，另外我还看到很多同学对于大模型的理解还存在一些误解，以为本地模型+知识库就是在 “训练“ 自己的模型。为了解答大家的问题，今天我们一起来聊聊大模型的进阶使用：“模型微调” ，也就是较大家真正的 “调教“ 出一个能够满足特定需求场景、更贴合个人使用习惯的个性化模型。

最近 “大模型算命” 很火，我们今天的例子就以 “算命” 为主题，教大家微调出一个更专业的 “算命大师” 模型。

![Image 2](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e1b4a2ba126d4ff8afe0d9e1e143ccaa~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=eXOLvZ2tc564Dtjv5TssBKW9CWo%3D)

我们先看看微调前后的效果对比：

![Image 3](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a572de7e64a04addaa65614df0f970a9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=y8UdELf0jk5nL6ZzyRbAXOkz%2Fmg%3D)

![Image 4](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4c04e032fb1e4af89637237b577df122~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=MNC3GEOxlaXCxUsZO0hWaZpl3KE%3D)

> 相信很多同学看到 “微调” 这个概念就有点想劝退了，觉得这已经属于比较深度的技术了，但我想告诉大家，其实微调并不会有大家想象中那么复杂，尤其是在 DeepSeek 热潮开始后，AI 开源社区和工具已经越来越成熟和发达，即使是非专业的技术爱好者，也能做到轻松上手。

在开始这篇文章之前，建议大家先阅读：《[如何拥有一个无限制、可联网、带本地知识库的私人 DeepSeek？](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FqeKrwJXz_QJE6eNwUOhjsA%3Ftoken%3D1894055887%26lang%3Dzh_CN "https://mp.weixin.qq.com/s/qeKrwJXz_QJE6eNwUOhjsA?token=1894055887&lang=zh_CN")》，其中介绍的一些专业术语，在本文中不再特殊说明。

为什么需要微调？
--------

在开始学习微调之前，大家首先还是要搞清楚为什么要微调？在什么情况下需要微调？

我们平常接触到的大模型如 GPT、DeepSeek 等都是基于海量的通用数据训练而成的，它们具备非常强大的语言理解和生成能力，能够处理多种自然语言任务。但是，这些模型在某些特定领域或任务上的表现可能并不理想，或者说还能够做到表现的更好。下面是需要微调的几个主要原因：

**领域专业化：让模型掌握“行业黑话”**

*   **原因**：通用模型的训练数据覆盖面广，但难以深入垂直领域的知识体系和专业术语。例如医学诊断需理解病理特征，法律咨询需熟悉法条逻辑。当模型在专业领域认知不够时，会出现比较严重的幻觉问题，也就是胡乱回答，微调可以很好的解决这个问题
*   **典型场景**：
    *   **医学问答**：输入症状描述，模型需结合医学知识库输出可信的初步诊断建议。
    *   **法律咨询**：分析“未成年人合同效力”时，需准确引用《民法典》相关条款。

**任务适配：调整模型的“输出模式”**

*   **原因**：不同任务对模型能力的要求差异显著——分类任务需结构化输出，生成任务需语言创造力。
*   **典型场景**：
    *   **文案生成**：训练模型以幽默风格撰写广告文案（如“这杯咖啡，比老板的早安更提神”）。
    *   **心理咨询**：从“情绪识别”转向“疏导对话”，需调整输出为引导性提问而非结论性判断。

**能力纠偏：解决模型的“偏科问题”**

*   **原因**：通用模型可能对某些任务过度敏感（如政治倾向）或表现不足（如冷门领域的长尾问题）。
*   **典型场景**：
    *   **民俗推理**：输入生辰八字与手相特征时，模型需按传统命理逻辑生成连贯解释，而非套用通用话术。
    *   **边缘案例**：处理“宠物能否继承遗产”时，需结合继承法细则而非泛泛回答。

安全与成本：

*   **数据安全**：当训练数据涉及隐私（如患者病历、企业内部文档）时，本地化微调可避免云端传输风险。
*   **成本效率**：相比从头训练（需百万级算力），微调仅需少量领域数据即可显著提升任务表现，适合中小规模企业。

长文本 & 知识库 & 微调的区别
-----------------

现在各大模型都支持超长上下文，从最开始的 `4K` 到现在的 `200K`，我们不能用一个比较完善的提示词来解决这些问题吗？

现在各种知识库工具这么灵活，我们不能自己搭建一个非常全面的数据库来解决这些问题吗？

这可能会是很多小伙伴存在的疑问，下面我们就来看看长文本、知识库、微调究竟有什么区别，我们又该在什么场景下做什么样的选择呢？

为了方便大家理解，我们后面把模型回答一个问题类比为参加一场考试。

### 长文本

通俗理解：你参加了一场考试，题目是一篇超长的阅读理解。这篇文章内容很多，可能有几千字，你需要在读完后回答一些问题。这就像是“长文本”的任务。模型需要处理很长的文本内容，理解其中的细节和逻辑，然后给出准确的答案。比如，模型要读完一篇长篇小说，然后回答关于小说情节的问题。

![Image 5](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4f216077ff5e495088a72f200010e119~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=YE%2BdKoBvvSwaM3KJMDegc5NqRJs%3D)

优点：

*   连贯性强：能够生成或理解长篇幅的内容，保持逻辑和语义的连贯性。
*   适合复杂任务：适合处理需要深入理解背景信息的任务，比如长篇阅读理解或复杂的文章生成。

缺点：

*   资源消耗大：处理长文本需要更多的计算资源和内存，因为模型需要同时处理大量信息。
*   上下文限制：即使是强大的模型，也可能因为上下文长度限制而丢失一些细节信息。

适用场景：

*   写作助手：生成长篇博客、报告或故事。
*   阅读理解：处理长篇阅读理解任务，比如学术论文或小说。
*   对话系统：在需要长篇回答的场景中，比如解释复杂的概念。

### 知识库

通俗理解：你参加的是一场开卷考试，你可以带一本厚厚的资料书进去。考试的时候，你可以随时翻阅这本资料书，找到你需要的信息来回答问题。这就像是“知识库”的作用。知识库就像是一个巨大的资料库，模型可以在里面查找信息，然后结合这些信息来回答问题。比如，你问模型：“爱因斯坦的相对论是什么？”模型可以去知识库中查找相关内容，然后给出详细的解释。

![Image 6](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2f8e0124b0a24be29817522d7da69f2d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=WDOAHzdZwX5jTOfxxHvi%2FIuR4lc%3D)

优点：

*   灵活性高：可以随时更新知识库中的内容，让模型获取最新的信息。
*   扩展性强：不需要重新训练模型，只需要更新知识库，就能让模型回答新的问题。

缺点：

*   依赖检索：如果知识库中的信息不准确或不完整，模型的回答也会受影响。
*   实时性要求高：需要快速检索和整合知识库中的信息，对性能有一定要求。

适用场景：

*   智能客服：快速查找解决方案，回答用户的问题。
*   问答系统：结合知识库回答复杂的、需要背景知识的问题。
*   研究辅助：帮助研究人员快速查找相关文献或数据。

### 微调

通俗理解：你在考试之前参加了一个课外辅导班，专门学习了考试相关的知识和技巧。这个辅导班帮你复习了重点内容，还教你如何更好地答题。这就像是“微调”。微调是让模型提前学习一些特定的知识，比如某个领域的专业术语或者特定任务的技巧，这样它在考试（也就是实际任务）中就能表现得更好。比如，你让模型学习了医学知识，那么它在回答医学相关的问题时就能更准确。

![Image 7](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2a1a5a54744447f0bb8ba8aa698fba4c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=AzmuUUPnf8FyPKTB5mUhtJ7fZlE%3D)

优点：

*   性能提升：显著提升模型在特定任务或领域的表现。
*   定制化强：可以根据需求调整模型的行为，比如改变回答风格或优化任务性能。

缺点：

*   需要标注数据：需要准备特定领域的标注数据，这可能需要时间和精力。
*   硬件要求高：微调需要一定的计算资源，尤其是 GPU。

适用场景：

*   专业领域：如医疗、法律、金融等，让模型理解专业术语和逻辑。
*   特定任务：如文本分类、情感分析等，优化模型的性能。
*   风格定制：让模型生成符合某种风格的内容，比如幽默、正式或古风。

### 对比

| 对比维度 | 长文本处理 | 知识库 | 微调 |
| --- | --- | --- | --- |
| 核心目标 | 理解和生成长篇内容 | 提供背景知识，增强回答能力 | 优化模型在特定任务或领域的表现 |
| 优点 | 连贯性强，适合复杂任务 | 灵活性高，可随时更新 | 性能提升，定制化强 |
| 缺点 | 资源消耗大，上下文限制 | 依赖检索，实时性要求高 | 需要标注数据，硬件要求高 |
| 适用场景 | 写作助手、阅读理解 | 智能客服、问答系统 | 专业领域、特定任务、风格定制 |
| 额外数据 | 不需要，但可能需要优化上下文长度 | 需要知识库数据 | 需要特定领域的标注数据 |
| 重新训练 | 不需要，但可能需要优化模型 | 不需要，只需更新知识库 | 需要对模型进行进一步训练 |
| 技术实现 | 扩大上下文窗口 | 检索+生成（RAG） | 调整模型参数 |
| 数据依赖 | 无需额外数据 | 依赖结构化知识库 | 需要大量标注数据 |
| 实时性 | 静态（依赖输入内容） | 动态（知识库可随时更新） | 静态（训练后固定） |
| 资源消耗 | 高（长文本计算成本高） | 中（需维护检索系统） | 高（训练算力需求大） |
| 灵活性 | 中（适合单次长内容分析） | 高（可扩展多知识库） | 低（需重新训练适应变化） |

微调的基本流程
-------

以下是一个常见的模型微调的过程：

*   选定一款用于微调的预训练模型，并加载
*   准备好用于模型微调的数据集，并加载
*   准备一些问题，对微调前的模型进行测试（用于后续对比）
*   设定模型微调需要的超参数
*   执行模型微调训练
*   还使用上面的问题，对微调后的模型进行测试，并对比效果
*   如果效果不满意，继续调整前面的数据集以及各种超参数，直到达到满意效果
*   得到微调好的模型

![Image 8](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ab3d6e8993e54cd8b7cf63ccb0e35a56~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=iH4%2FVBJoVWSmBE%2Bhn3jQYCefml0%3D)

在这个流程里，有几个基本概念需要大家提前了解，我们还用上面考试的例子举例，微调模型的过程就像是给一个已经很聪明的学生“补课”，让他在某个特定领域变得更擅长。

### 概念1：预训练模型

预训练模型就是我们选择用来微调的基础模型，就像是一个已经受过基础教育的学生，具备了基本的阅读、写作和理解能力。这些模型（如 `GPT、DeepSeek` 等）已经在大量的通用数据上进行了训练，能够处理多种语言任务。选择一个合适的预训练模型是微调的第一步。 ![Image 9](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/18a36ee2a4d949a38e6aef5c55bcbf7e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=jjxF%2FVFDcBICN%2BQUjT5bIebbt8U%3D)

一般来说，为了成本和运行效率考虑，我们都会选择一些开源的小参数模型来进行微调，比如 `Mate` 的 `llama`、阿里的 `qwen`，以及最近爆火的 `DeepSeek`（蒸馏版）

![Image 10](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/78279a5c2584459ba3975b801822cda2~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=E5xMql90UwJmd%2BzoEjhhYeLFxPc%3D)

### 概念2：数据集

数据集就是我们用于模型微调的数据，就像是“补课”时用的教材，它包含了特定领域的知识和任务要求。这些数据需要经过标注和整理，以便模型能够学习到特定领域的模式和规律。比如，如果我们想让模型学会算命，就需要准备一些标注好的命理学知识作为数据集。

![Image 11](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b472ec31eb0748839943fcadd4a266ce~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=9lPpOBKthZrVcJ%2Fe0cfZFkzXx2w%3D)

一般情况下，用于模型训练的数据集是没有对格式强要求的，比如常见的结构化数据格式：JSON、CSV、XML 都是支持的。

数据集中的数据格式也没有强要求，一般和我们日常与 AI 的对话类似，都会包括输入、输出，比如下面就是一个最简单的数据集：

![Image 12](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/787c9d9bbadd4939adba8dbb518fbba7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=fsXgiUtQHFO2ZQ3rYPXQI2QtKUE%3D)

为了模型的训练效果，有时候我们也会为数据集添加更丰富的上下文，比如在下面的数据集中，以消息（messages）进行组织，增加了 System（系统消息，类似于角色设定），user（用户消息）、assistant（助手回复消息）的定义，这样就可以支持存放多轮对话的数据，这也是 OPEN AI 官方推荐的数据集格式：

![Image 13](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/26ae2cbd5cce45ab80d65ec655348260~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=EvWeK1n39dQYfVBse6lXGmg3iRY%3D)

大家练习或测试的话可以去网上找一些公开数据集，这里推荐两个可以获取公开数据集的网站：

第一个：`Hugging Face`（🪜），我们可以把 Hugging Face 平台比作 AI 领域的 `GitHub`，它为开发者提供了一个集中化的平台，用于分享、获取和使用预训练模型和数据集。就像 `GitHub` 是代码共享和协作的中心一样，`Hugging Face` 是 `AI` 模型和数据共享的中心。在后面的实战环节中我们还会用到它：

![Image 14: https://huggingface.co/datasets](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6256742e48a445aca0ae1809d80b6efb~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=Gos6Wf311Zry2E4NXl68h6UTAD4%3D)

如果你没有🪜，也可以退而求其次，选择国内的一些类似社区，比如 GitCode 的 AI 社区：

![Image 15: https://ai.gitcode.com/datasets](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/eacf20dd3666418b8fe61b26376460f5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=nUeEvdPh7iCiEMB0GEVR1xN0IN4%3D)

### 概念3：超参数

超参数就像是你在给模型 “补课” 之前制定的教学计划和策略。它们决定了你如何教学、教学的强度以及教学的方向。如果你选择的教学计划不合适（比如补课时间太短、讲解速度太快或复习策略不合理），可能会导致学生学习效果不好。同样，如果你选择的超参数不合适，模型的性能也可能不理想。

![Image 16](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/cbe3f68cbe344f739b5c193b952f36d7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=HAGE7befyK4IPxtPJBH3BcReoyU%3D)

一些关键的超参数的含义，我们将在后面的实战中继续讲解。

初识：通过平台微调大模型
------------

目前市面上很多 AI 相关平台都提供了在线微调模型的能力，比如我们以最近比较火的硅基流动为例：

![Image 17: https://docs.siliconflow.cn/cn/userguide/guides/fine-tune](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b450f907b1c144b2b0f04b331a36f781~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=Di9g1SankTbXOa%2B4RIDrvjqhLew%3D)

我们进入硅基流动后台的第二项功能就是模型微调：

![Image 18: https://cloud.siliconflow.cn/fine-tune](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/24cafd220de84a12aee86df41dac53ae~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=uvQCbkLeaP3RCb3BACbwGbbmqI0%3D)

### 选择预训练模型

我们尝试新建一个微调任务，可以看到目前硅基流动支持微调的模型还不是很多，而且也没看到 DeepSeek 相关模型，这里我们选择 `Qwen2.5-7B` 来测试一下：

![Image 19: 选择预训练模型](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0c78cb2059dd44fe86e7b14c53bde94f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=wwPH8l5tE7cgP8e3znWdNmyCAc8%3D)

### 准备数据集

下一步就是选择数据集：

![Image 20: 上传数据集](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6c6868e3e4a347a78b2990557c28cd5a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=6gkmAjruf6GbwGpzv2pchZGLkmc%3D)

我们目前硅基流动仅支持 .jsonl 格式的数据集：

`JSONL` 文件（JSON Lines）是一种特殊的 JSON 格式，每一行是一个独立的 JSON 对象，JSONL 文件是“扁平化”的，彼此之间没有嵌套关系。

![Image 21](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d76f26adefc44d9b903ef086e66631ca~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=EdnucjZ7tVInRkMJHsWNxj258B0%3D)

且需符合以下要求：

![Image 22: jsonl 格式说明](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/adaa397cd6f142cb97cab4ad4e056a3e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=vRcQf5NTyYMExvqQb%2B54CnCUh5E%3D)

看着挺复杂的，其实和我们上面介绍的 `OPEN AI` 官方推荐的数据集格式要求是一样的：

![Image 23](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/df0ec0e30d2346e286b83a1c9701c38f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=rGmnwwqEC5fKD8yuJInC8IRIn2g%3D)

对应 jsonl 的数据就是这样：

![Image 24](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3bdbc01cd6ff495aa101b6fbdc9db7aa~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=2Izf78cZSEPPnP130tr0Xq2jQa8%3D)

### 验证数据集

数据集上传完成后，下一步就是输入一个微调后模型的名字，以及设置验证数据集。

首先我们想要微调一个算命大师模型，那我们就以 fortunetelling 来命名：

![Image 25](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/995b887800b94c938f82aec80d5ea3c6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=17Mk8EXLn%2BXZlNhB7srikliclmw%3D)

然后就是验证数据集：

**验证数据集** 就是从我们的整体数据中划分出来的一部分数据。它通常占总数据的一小部分（比如 10%~20%）。这部分数据在训练过程中不会被用来直接训练模型，而是用来评估模型在未见过的数据上的表现。

简单来说，验证数据集就像是一个“模拟考试”，用来检查模型是否真正学会了知识，而不是只是“背诵”了训练数据。

这里我们选择默认的 `10%` 即可。

### 超参数设置

最后就是设置一些模型训练的 “超参数” 了，给出可以设置的参数非常多，我们这里只介绍最关键的三个参数：

![Image 26](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/bb38c1d45fbd4c09b51559df66db14c0~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=2EWt9tzCbA%2FQfTpUyY4PSNKazDE%3D)

为了方便理解，我们还以考试前复习的例子来进行讲解，假设你正在准备一场重要的考试，你有一本厚厚的复习资料书，里面有 1000 道题目。你需要通过复习这些题目来掌握考试内容。

**训练轮数（Number of Epochs）** Epoch 是机器学习中用于描述模型训练过程的一个术语，指的是模型完整地遍历一次整个训练数据集的次数。换句话说，一个 `Epoch` 表示模型已经看到了所有训练样本一次。

![Image 27](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/20eb31b4cfb74106afe382e42d3ccbec~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=7wbPdVpWCQMljQ8ME8gZjQZtihY%3D)

通俗来说，训练轮数就是我们从头到尾复习这本书的次数。

*   轮数少：比如你只复习一遍，可能对书里的内容还不是很熟悉，考试成绩可能不会太理想。
*   轮数多：比如你复习了 10 遍，对书里的内容就很熟悉了，但可能会出现一个问题——你对书里的内容背得很熟，但遇到新的、类似的问题就不会解答了，简单讲就是 “学傻了“，只记住这本书里的内容了，稍微变一变就不会了（**过拟合**）。

**学习率（Learning Rate）** 决定了模型在每次更新时参数调整的幅度，通常在 (0, 1) 之间。也就是告诉模型在训练过程中 “学习” 的速度有多快。学习率越大，模型每次调整的幅度就越大；学习率越小，调整的幅度就越小。

![Image 28](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/694e15d8a93b40c39ba745312f090c2c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=br32B6hCoV6YJICk6RDxCMgdAe4%3D)

通俗来说，学习率可以用来控制复习的“深度”，确保不会因为调整幅度过大而走偏，也不会因为调整幅度过小而进步太慢。如果你每次复习完一道题后，你会根据答案和解析调整自己的理解和方法。

*   学习率大（比如0.1）：每次做完一道题后，你会对解题方法进行很大的调整。比如，你可能会完全改变解题思路。优点是进步可能很快，因为你每次都在进行较大的调整。缺点就是可能会因为调整幅度过大而“走偏”，比如突然改变了一个已经掌握得很好的方法，导致之前学的东西都忘了。
*   学习率小（比如0.0001）：每次做完一道题后，你只对解题方法进行非常细微的调整。比如，你发现某个步骤有点小错误，就只调整那个小错误。优点是非常稳定，不会因为一次错误而“走偏”，适合需要精细调整的场景。缺点就是进步会很慢，因为你每次只调整一点点。

**批量大小（Batch Size）** 是指在模型训练过程中，每次更新模型参数时所使用的样本数量。它是训练数据被分割成的小块，模型每次处理一个小块的数据来更新参数。

![Image 29](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a1c5d9f1359d4354b73e0392e83ac5f2~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=iDpAh%2BHPC91tdZzsaX502n2avUU%3D)

通俗来说，批量大小可以用来平衡复习速度和专注度，确保既能快速推进复习进度，又能专注细节。假设你决定每次复习时集中精力做一定数量的题目，而不是一次只做一道题。

*   批量大（比如100）：每次复习时，你集中精力做100道题。优点是复习速度很快，因为你每次处理很多题目，能快速了解整体情况。缺点是可能会因为一次处理太多题目而感到压力过大，甚至错过一些细节。
*   批量小（比如1）：每次复习时，你只做一道题，做完后再做下一道。优点是可以非常专注，能仔细分析每道题的细节，适合需要深入理解的场景。缺点就是复习速度很慢，因为每次只处理一道题。

在实际的微调场景中，我们需要通过一次次的调整这些参数，最后验证对比模型效果，来产出效果最好的微调模型。当然，如果你是小白用户，这些参数简单理解就行了，刚开始不需要调整这些参数，默认推荐的一般可以满足大部分场景的需求。

### 微调后调用

微调完成后，我们可以得到一个微调后模型的标识符：

![Image 30](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3e297d4468ec4bf7b79bb6ccd4c2bdca~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=OqgZoj9Ir4xpTbrtfnPUli9RKJA%3D)

后续我们可以通过接口（/chat/completions）即可直接调用微调后的模型：

```
from openai import OpenAI
client = OpenAI(
    api_key="您的 APIKEY", # 从https://cloud.siliconflow.cn/account/ak获取
    base_url="https://api.siliconflow.cn/v1"
)

messages = [
    {"role": "user", "content": "用当前语言解释微调模型流程"},
]

response = client.chat.completions.create(
    model="您的微调模型名",
    messages=messages,
    stream=True,
    max_tokens=4096
)

for chunk in response:
    print(chunk.choices[0].delta.content, end='')
```

我们现在已经了解了模型微调需要的大部分基础概念，也通过硅基流动平台走完了一个完整的微调流程，但是在这个过程中我们发现有几个问题：

*   可以选择的基础模型太少了，没有我们想要的 DeepSeek 相关模型
*   模型训练过程中的 Token 消耗是要自己花钱的，对于有海量数据集的任务可能消耗比较大
*   微调任务触发不太可控，作者在测试的时候创建的微调任务，等了一天还没有被触发，当然这可能是硅基流动最近调用量太大，资源不足的问题，换成其他平台（比如 OPEN AI Platfrom）可能好一点，但是总归这个任务还是不太可控的。

为了解决这个问题，最终我们还是要使用代码来微调，这样我们就能灵活选择各种开源模型，无需担心训练过程中的 Token 损耗，灵活的控制微调任务了。

当然，看到这里，不会写代码的同学也不要放弃，因为前面大部分的概念我们已经了解过了，下面我会尽可能的让大家在不懂代码的情况下也能完整运行这个过程。

进阶：要了解的工具
---------

在开始实战之前，我们先了解后续模型微调过程中需要用到的两个核心工具 `Colab` 和 `unsloth`。

### Colab

`Colab` 是一个基于云端的编程环境，由 Google 提供。它的主要功能和优势包括：

*   免费的 GPU 资源：Colab 提供免费的 GPU，适合进行模型微调。虽然免费资源有一定时间限制，但对于大多数微调任务来说已经足够。
*   易于上手：Colab 提供了一个基于网页的 Jupyter Notebook 环境，用户无需安装任何软件，直接在浏览器中操作。
*   丰富的社区支持：Colab 上有许多现成的代码示例和教程，可以帮助新手快速入门。

![Image 31](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/499054c17d394f2aa3b26bce8bb884ce~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=YkXcAI3vVyg%2FDYhOl%2BNps1yZjPw%3D)

简单来说，有了 `Colab` ，可以让你没有在比较好的硬件资源的情况下，能够在线上微调模型，如果只是学习的话，免费的资源就够了。另外，市面上很多模型微调的 DEMO ，都是通过 `Colab` 给出的，大家可以非常方便的直接进行调试运行。

### unsloth

`Unsloth` 是一个开源工具，专门用来加速大语言模型（LLMs）的微调过程。它的主要功能和优势包括：

*   高效微调：Unsloth 的微调速度比传统方法快 2-5 倍，内存占用减少 50%-80%。这意味着你可以用更少的资源完成微调任务。
*   低显存需求：即使是消费级 GPU（如 RTX 3090），也能轻松运行 Unsloth。例如，仅需 7GB 显存就可以训练 1.5B 参数的模型。
*   支持多种模型和量化：Unsloth 支持 Llama、Mistral、Phi、Gemma 等主流模型，并且通过动态 4-bit 量化技术，显著降低显存占用，同时几乎不损失模型精度。
*   开源与免费：Unsloth 提供免费的 Colab Notebook，用户只需添加数据集并运行代码即可完成微调。

![Image 32](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e9d376235d314b1faf8b198c5ee9e050~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=2uzjYYUB8dbgWPk4eYLRV87y5Co%3D)

简单来说，`Unsloth` 采用了某些优化技术，可以帮助我们在比较低级的硬件设备资源下更高效的微调模型。在 `Unsloth` 出现之前，模型微调的成本非常高，普通人根本就别想了，微调一次模型至少需要几万元，几天的时间才能完成。

我们看到 `Unsloth` 官方提供了很多通过 `Colab` 提供的各种模型的微调案例，我们可以很方便的在 `Colab` 上直接运行这些案例：

![Image 33](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ab6d88ba0eba41c8bee278e1d3e91366~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=8ckpa78ohG9uiQZ2ipl5gZeY6Mg%3D)

但是在官方的示例中，我们没有找到 DeepSeek R1 模型的微调案例，不过我找到了官方的一段介绍：

![Image 34](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/55d1602370d249049860d1198a865d7a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=QWCh9CLGTstPzYjiqHAXCamrNUc%3D)

我们可以直接在现有案例中，直接将模型名称进行替换，就可以运行 `DeepSeek R1` 推理模型的微调，不过在实际运行中，我发现还需要调整数据集的格式以及一些参数，这个我们后面具体讲解。

下面我们就用一个实际的例子（微调算命大师模型）来带大家走一遍这个过程，大家只需要跟随我把每个步骤里的代码复制到自己的 `Colab` 里运行即可，期间大家只需要自己调整一些关键的部分，例如数据集和测试问题等等。

实战：使用 unsloth 微调算命大师模型
----------------------

在开始前我们再回顾下前面我们总结的微调的基本流程，在下面的案例中流程基本也是一样的：

![Image 35](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b63d570438f740408dca60cd4dca0e46~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=4sPzAL%2FpcENwtxnCVn4WlvS7Te4%3D)

### 第一步：创建环境、安装依赖

这里推荐大家创建一个自己的空白 `Colab` 环境来一步步将我的代码贴进去执行。

大家可以访问这个链接（需要🪜）：

[colab.research.google.com/#create=tru…](https://link.juejin.cn/?target=https%3A%2F%2Fcolab.research.google.com%2F%23create%3Dtrue "https://colab.research.google.com/#create=true")

然后我们更改一下运行时类型（在 Colab 中用于执行代码的计算资源类型，其决定了你的代码运行时会使用哪种硬件支持）。

![Image 36](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/cf8a906ddc2a4960895329c3ea5bd696~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=Jq6dfOYFjAjyt629DMEgbzhOUAc%3D)

将运行时类型改为 T4 GPU（`NVIDIA` 推出的一款高性能 GPU，特别适合深度学习任务）：

![Image 37](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1ab0e7fff2c145a0ae67bd8459feaf4a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=E4I%2FzrtwE%2FuP8hHJudTwPnPILZ0%3D)

然后我们执行第一段最简单的代码，主要功能是安装一些 Python 包和库，这些库是运行 AI 模型微调任务所必需的工具。

![Image 38](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7ba5732257fb4864a70be629e2aa3e87~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=tdh8oeCWS80Unu3vDS3O%2BkAvi9A%3D)

### 第二步：加载预训练模型

下一步就是要加载一个预训练模型，可以看到这里的参数是 `model_name`，然后我们选择的是 `DeepSeek-R1-Distill-Llama-8B`（基于 Llama 的 DeepSeek-R1 蒸馏版本，80 亿参数），如果大家想更换成其他的模型，直接改这个参数即可，比如可以改成：`unsloth/DeepSeek-R1-Distill-Qwen-7`，然后运行代码我们可以看到模型的拉取日志：

![Image 39](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/8c973ac1fe514dc596c61d60cbcd81cc~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=ONeWaEK%2F7Fb9ND%2F76QXNceHecdQ%3D)

> 选择了解：4bit 量化（4bit Quantization）：一种技术，通过减少模型的精度来节省内存，就像把一个大箱子压缩成一个小箱子，方便携带。

### 第三步：微调前测试

在开始微调之前，我们先用一个算命相关的问题来测试一下，方便我们在训练完后进行对比。

首先我们定义问题（这里大家可以自行更改，比如你想要训练一个医学相关大模型，那这里就改成看病相关的问题）：

![Image 40](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f77bc8d9b8e04cd7be6fd0287db00248~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=pLoNpR8MmC3FKuDtsoP3Vvl3a9I%3D)

然后我们调用模型进行推理，并打印出推理结果（这里完全不需要大家改，照搬就行）：

![Image 41](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/878597d8510d4ba98c70f9d2eb548ec1~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=YpRu6tfOx5u%2BNSksCPqjjmXe4WI%3D)

微调前输出的结果：

![Image 42](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/72d345db9c3147768e71734ba3a3138c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=koYNB0MlUxl5gToD%2BUqeUNCsWrM%3D)

可以看到，现在模型给的结果比较简单，也没有 “大师” 的语气风格。

### 第四步：加载数据集

首先我们把这个数据集预期要训练出来的模型风格定义出来（这里大家也可以自行更改，比如你想要训练一个医学相关大模型，那这里就改成专业医生相关的描述）：

![Image 43](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e97a2afdeb6f484e952a807b0df49fb6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=MuVKj7sHsksiiiJ99jRvR6Vn7UQ%3D)

下面我们要准备一个用于微调的数据集，大家可以去前面提到的 `HuggingFace` 上搜索符合自己需求的数据集，命理相关的数据集比较少，这里我自己生成了一些，然后上传到 `HuggingFace` 了，大家有需要的可以自取：

![Image 44: https://huggingface.co/datasets/Conard/fortune-telling/viewer/default/train](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d0804808b9074db085ca7e05bae3a417~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=mOMXUytIhmsZvo2psbZD2Rf%2FQ3Y%3D)

需要注意的是，这里字段格式和前面提到的格式略有区别，除了包含基本的问题（Question）、回答（Response），还包含了模型的思考过程（Complex\_CoT），因为我们现在要训练的是一个推理模型，所以数据集中最好也要包含模型的思考过程，这样训练出来的推理模型效果更好。

下面我们看看加载数据集的代码，我们把数据集加载进来，然后打印出数据集包含的字段名：

![Image 45](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/dd99fe0545c44dec81975629c0e799aa~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=%2FMXqsgJ%2FGit9IubzkdV4IfmxmwQ%3D)

这里重点关注 `load_dataset` 函数的几个参数，数据集的名称（默认会从 HuggingFace 拉取），数据集的语言以及取数据集的哪部分数据用作训练。

然后我们对数据集进行一些格式化，再打印一条出来看看：

![Image 46](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5793fe001b6f496082392e46f2fef6c3~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=M43b91oGe83svulo2KzrdFhUGZA%3D)

目前所有准备工作已经完成，下一步就是开始微调训练。

### 第六步：执行微调

在这一步，我们需要设置各种关键参数，我们把关键代码分为三段：

第一段（模型微调准备）：

![Image 47](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/bda8b364923a4871b800a3b9f1517299~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=rR%2BVzSd0c5%2FTPQSWieyCpmrZY2c%3D)

这段代码是通过 LoRA 技术对预训练模型进行了微调准备，使其能够在特定任务上进行高效的训练，同时保留预训练模型的大部分知识。LoRA 我们在这篇文章中不做深度讲解，大家先了解即可，参数也先不用改。

第二段（配置微调参数）：

![Image 48](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/70e4da0931ad465f97b6cba1cbbaca18~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=hwx5oz0oei7lswuJZsBg5MTN5Ic%3D)

在这段代码中，包括一大堆参数，不需要大家都理解，我们只需要关注上面我们已经介绍过的三个参数：

*   学习率（Learning Rate）：通过 `TrainingArguments` 中的 `learning_rate` 参数设置的，这里的值为 `2e-4`（即 0.0002）。
    
*   批量大小（Batch Size）：由两个参数共同决定（实际的批量大小：`per_device_train_batch_size * gradient_accumulation_steps`，也就是 `2 * 4 = 8`）：
    
    *   `per_device_train_batch_size`：每个设备（如 GPU）上的批量大小。
    *   `gradient_accumulation_steps`：梯度累积步数，用于模拟更大的批量大小。
*   训练轮数（Epochs）：通过 `max_steps`(最大训练步数) 和数据集大小计算得出，在这段代码中，最大训练 70 步，每一步训练 8 个，数据集大小为 200，那训练论数就是 `70 * 8 / 200 = 3`
    

我们来看最后一段代码（执行训练）：

![Image 49](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/864b79c3e2d149deb08bed5353f1f845~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=ZUHd684ubv31c2Kf95Kao3zuQbc%3D)

这段代码非常简单，就一行，我们执行后可以看到一些关键参数，比如训练轮数、批量大小等，也可以看到每一步训练的进度。

### 第七步：微调后测试

微调训练完成后，我们测试运行一下，还使用和之前一模一样的问题：

![Image 50](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/401e7a6d12d24e92a003ad99c22196e8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=qHn1u4cyVCm73dovU%2FuACRBkq9Q%3D)

回答效果：

![Image 51](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/38df4af55c64498a9d40450b2d53f69b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=UMhKDMKDA2tlQd9hGipd4Kjbt3s%3D)

可以发现，回答效果专业了很多，说明本次训练是有效果的。

实战：本地运行微调后的算命大师模型
-----------------

现在，我们已经在 Colab 上完成了完整的模型微调训练过程，下一步就是使用我们微调后的模型了，在之前的文章中我们学习了如何使用 `Ollama` 运行 `Ollama` 平台上的开源模型，其实 `Ollama` 也是可以支持直接从 `Hugging Face` 上拉取并运行模型了，所以我们可以把刚刚训练好的模型上传到 `Hugging Face` 上。

> 如果大家还没读过本地部署这篇文章，建议先阅读一下：《[如何拥有一个无限制、可联网、带本地知识库的私人 DeepSeek？](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FqeKrwJXz_QJE6eNwUOhjsA%3Ftoken%3D1894055887%26lang%3Dzh_CN "https://mp.weixin.qq.com/s/qeKrwJXz_QJE6eNwUOhjsA?token=1894055887&lang=zh_CN")》

### 第八步：将微调后的模型保存为 GGUF 格式

将微调后的模型上传到 `Hugging Face Hub` 之前，我们先将它转换为 GGUF 格式。

`GGUF` 是一种高效的格式，它支持多种量化方法（如 4 位、8 位、16 位量化），可以显著减小模型文件的大小，便于存储和传输，适合在资源受限的设备上运行模型，例如在 Ollama 上部署时。量化后的模型在资源受限的设备上运行更快，适合边缘设备或低功耗场景。

转换的代码大家不用做任何更改：

![Image 52](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b10b19cdd8fe47119ec1ca57980a66dc~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=e0MhWM6me0SW2DdYpZPpWZzJn48%3D)

这里还有一个需要大家关注，就是设置 `HuggingFace` 的 `Access Token`，因为我们要直接调用 `HuggingFace` 的 API 把模型上传到我们自己的 `HuggingFace` 仓库，这个 Token 就是用来做权限校验的。

我们可以到 `HuggingFace` 的 `Settings - Access Tokens` 下创建一个自己的 Token：

![Image 53: https://huggingface.co/settings/tokens](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/24906ea59c03425b9962cd7561d04836~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=%2F6iVQ6l52C0IUxD7JsP%2BXLGu20c%3D)

注意一定要配置为写权限，不然后面没有权限创建仓库：

![Image 54](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a349d3ea51df47de8cfb0e8016668d50~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=5X1SnZLcm%2Bhtrn%2FezYVUaGldYq4%3D)

然后我们将这个 Token 复制到 Colab 左侧的 `Secret` 下，创建一个名为 `HUGGINGFACE_TOKEN` 的 `Secret` ：

![Image 55](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f8d3f3d621054f1a8d59448421fd8387~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=0B1IlkHdrKB3W4sozTUYhj3dHts%3D)

### 第九步：将微调后的模型上传到 HuggingFace

下面就是使用上面配置好的 Token，调用 HuggingFace 的 API，创建一个新的模型仓库，然后把我们刚刚微调训练好的模型推送上去：

![Image 56](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2c9e3424a8a043dd9042084847a0aaad~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=MH8cPs4tW6M7uQ5lGXVhx8S%2FQPE%3D)

注意这里大家可以把仓库名称改为自己的「用户名+模型名」，然后大功告成，我们去 `HuggingFace` 上查看一下：

![Image 57: https://huggingface.co/Conard/fortunetelling](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e285443faf2a4fe3b007fd3280d5c808~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=mh1UPv3phufXwJy99AGP5UGofBQ%3D)

### 第十步：使用 Ollama 运行 HuggingFace 模型

`Ollama` 支持直接从 `Hugging Face` 拉取模型，格式如下：

```
ollama run hf.co/{username}/{repository}
```

![Image 58: ollama run hf.co/Conard/fortunetelling](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2a802816800249638f25173d1352aa3b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=8xDnzBGZ6iC3SsZnkxQUuqWdXac%3D)

下载完成后我们尝试运行一下：

![Image 59](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/508b6ebbb27841e29a5f9a72cc980998~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=3NBylqELGIbctJ4WMRHZ90n7p2I%3D)

我们也可在 `Chatbox、Anything LLM` 这些工具下使用：

![Image 60](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/03d36c6d37894c7cb80411bf05f9742f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgQ29uYXJkTGk=:q75.awebp?rk3s=f64ab15b&x-expires=1741065333&x-signature=fYCM1ZLhERxOAgH%2FhrUHzx0WQHw%3D)

最后
--

大家有任何问题，欢迎在评论区留言。

抖音前端架构团队目前放出不少新的 HC ，有看机会的小伙伴可以看看这篇文章：[抖音前端架构团队正在寻找人才！ FE/Client/Server/QA](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzk0MDMwMzQyOA%3D%3D%26mid%3D2247499434%26idx%3D1%26sn%3D8c7497876efc458dca19b6f6a27cadd4%26chksm%3Dc2e10b81f5968297533fcfced9ebad6eba072f6436bf040eaa8920256577258ef1077d1f122a%26token%3D1091255868%26lang%3Dzh_CN%23rd "https://mp.weixin.qq.com/s?__biz=Mzk0MDMwMzQyOA==&mid=2247499434&idx=1&sn=8c7497876efc458dca19b6f6a27cadd4&chksm=c2e10b81f5968297533fcfced9ebad6eba072f6436bf040eaa8920256577258ef1077d1f122a&token=1091255868&lang=zh_CN#rd")，25 届校招同学可以直接用内推码：`DRZUM5Z`，或者加我微信联系。

为了方便大家交流学习，我准备组建一个 AI 交流群，本文中微调案例中使用到的完整代码，我也会发到群里，想要在群里和大家一起讨论 AI 技术的小伙伴可以添加我的个人微信 [ConardLi](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzk0MDMwMzQyOA%3D%3D%26mid%3D2247493407%26idx%3D1%26sn%3D41b8782a3bdc75b211206b06e1929a58%26chksm%3Dc2e11234f5969b22a0d7fd50ec32be9df13e2caeef186b30b5d653836b0725def8ccd58a56cf%23rd "https://mp.weixin.qq.com/s?__biz=Mzk0MDMwMzQyOA==&mid=2247493407&idx=1&sn=41b8782a3bdc75b211206b06e1929a58&chksm=c2e11234f5969b22a0d7fd50ec32be9df13e2caeef186b30b5d653836b0725def8ccd58a56cf#rd")（备注 AI），拉你进群：

`点赞`、`评论`、`关注` 是最大的支持 ⬇️❤️⬇️
