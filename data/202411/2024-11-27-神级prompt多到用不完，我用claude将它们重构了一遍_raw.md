Title: 神级Prompt多到用不完，我用Claude将它们重构了一遍

URL Source: https://mp.weixin.qq.com/s/JFghFwUud16fQfFsYBamvA

Markdown Content:
![Image 29](https://mmbiz.qpic.cn/mmbiz_gif/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6Zuc207aDbIgntCWQvzJrj8NEUbtZAFljzG6G5U28OOqAmWUqfibxiayxQ/640?wx_fmt=gif&from=appmsg)

**_每个神级 Prompt 都是一款产品，更代表了一种思想。_**

上周大火的神级 Prompt - Thinking Claude 🧠，通过拟人化的思维链，将 Claude 强化成了满血 o1。

尽管对于是否还原了 o1 的推理过程，我持有怀疑态度。

但不妨碍我记住了“拟人化思考”这个做题思路，

并开始应用在平时写提示语的过程。

是的，哪怕只是一句“你好，你是什么模型？”，也算是写提示语。所以每次输入都选择神级 prompt 显然是不合理的：

*   一方面，随着在手机端使用 AI 的频率上升，多次复制黏贴神级 Prompt 的时间都够我跟 AI 对话三四轮了。
    
*   另一方面，随着模型能力的更新，有些神级 Prompt 已经过时。打个比方，半年前提示语还是越复杂越好，而现在过长的提示语还会影响模型自主发挥。
    

所以我打算用 Claude 的几天前更新的功能：

**提示词优化 - Prompt Console**

来将神级 Prompt 们重构一遍！

![Image 30](https://mmbiz.qpic.cn/mmbiz_jpg/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6Zkic43haAOopcoOq0OJawjWlCfcgtQ0LbSux2iaPGjVCXzhZHtMz8B1aA/640?wx_fmt=jpeg&from=appmsg)

先放一段 Prompt Console 的操作步骤：

![Image 31](https://mmbiz.qpic.cn/mmbiz_gif/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZJBO9ficibGicrx9iaN0jhaxQgHroibK3Jc514EFhsl6rTfrWoVrLZjqHLHw/640?wx_fmt=gif&from=appmsg)

官方还主动公布了优化的具体步骤：

*   思维链：引导模型主动思考问题
    
*   数据增强：生成更多的样本数据
    
*   样本标准化：将所有样本统一转成XML格式
    
*   提示语重写：结构化提示语并纠正语法错误
    
*   预填充添加（Prefill addition）：规范模型的输出格式
    

（超前预告一下，用起来会发现没那么简单 🕶️）

这不就是 Anthropic 通过筛选和组合出一些长期有效的提示语优化技巧，再让 Claude 基于这些方法来优化普通提示语吗？

类比一下，

神级 Prompt 本身也是普通提示语经过反复优化后的产物。

**也就是说得到神级 Prompt 的优化思想后，就可以这些方法一口气追加到 Prompt Console 当中。**

不用担心要素过多，

![Image 32](https://mmbiz.qpic.cn/mmbiz_jpg/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6Zvibzds4SOCoMjZYFgpqO6PKjk8R2ibiboic4xkQSkM5gicL5tq6XfMjUe7Q/640?wx_fmt=jpeg&from=appmsg)

因为 Prompt Console 还支持反馈机制。我可以主动标注提示语中哪些部分对输出结果有效，Claude 会进一步优化提示词。

那下面让我来介绍一下我珍藏的神级提示语们：

除了火出圈的 Thinking-Claude、SuperPrompt、CO-STAR，以及各大模型和 AI 产品的 System Prompt 外，我还挑选出了论文领域和开源项目都在高频使用的技巧：（排名不分先后）

*   **LEAP**：从示例中学习任务的特定原则
    
*   **Re-reading (RE2)**：要求模型重新阅读提示，降低遗漏细节的可能性。
    
*   **Self-Ask**：将复杂的问题分解为子问题并逐步回答来提高LLM推理能力。
    
*   **Contrastive Chain-of-Thought**：通过结合正面和负面例子来增强LLM推理。
    
*   **SG-ICL**：通过模型生成与当前任务相关的示例，跟依赖外部示例相比获得更好的性能。
    
*   **CoT with Reflection**：让模型分步骤进行推理，还能在每个步骤后进行自我检查和调整。
    
*   **Rephrase and Respond** (RaR)：要求模型在回答之前重新表述提示语来提高推理准确性。
    
*   **Step-Back Prompting**：引导模型在处理具体细节前先生成高级概念和首要原则，防止中间步骤的推理错误。
    

超级无敌欢迎在评论区里补充更多的优化技巧👏👏

![Image 33](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZibSXaK8dibRq3NiaVibNImegEniaW8ujEHrN8WiajLicEnBBuVS4kOY8Gvyug/640?wx_fmt=png&from=appmsg)

本次遗憾落选的 Prompt 技巧们

优化技巧都备齐之后，就可以进行第一次优化了。

刚好前段时间我才总结过日常使用提示语的所有场景：翻译、总结、搜索、内容解释、代码生成。

[AI接管人类电脑的72小时里，我测出了Claude的上限](http://mp.weixin.qq.com/s?__biz=Mzg3MTk3NzYzNw==&mid=2247490299&idx=1&sn=5850717d18b4778a37b3b518abc7a345&chksm=cef71d31f9809427d9c31c54a40b2cedcd33fb7797db8615903b4153b7d1d9c7af4b1255ce3b&scene=21#wechat_redirect)

这次我打算把摘要总结的提示语“神化”一版，

我想象中的神级 Prompt 能一次性生成全面的摘要，能帮助我快速判断是否值得精读，还能直接输出一个适合分享到各大平台的格式。要能出一篇100K Views的帖子也算是人生里程碑了。

![Image 34](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZNtHH4h35icUXpLxjNT5BND63uj7u0oop2udgib5SvZgcsCtqB9OpW4KQ/640?wx_fmt=png&from=appmsg)

这是我的常用版本：

**写一个摘要，既要体现核心要点，又要能留下hook吸引人点击。**

这是实际的优化过程：

![Image 35](https://mmbiz.qpic.cn/mmbiz_gif/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZBEY3r5MkZ6qzHccj9SG7RYOYIkTomw82st0GVVFfVUNHAjSREg7uZQ/640?wx_fmt=gif&from=appmsg)

ps：篇幅受限，我在后面会直接贴出完整的提示语👇

从上面的操作实录里看，提示语优化的界面可以把整个过程拆成了五步：

前三步是**了解用户想要什么、生成执行的流程图、从样本里学习生成规则**、这时候会生成第一版提示语。我都没有输入样本，但 Claude 会主动去分析预期的样本会长什么样。

后三两步就更有意思了，值得单独拆开讲讲：

1.  补充执行步骤的细节：具体来说，执行步骤从阅读文本、确定信息点、列出要素、确定目标受众、分析原文语气和风格，给出合适的hook以及原因，最后还限制了句子数量。说实话这比我自己写推文的思路都详细。
    
2.  动态调整输入文本、样本、输出模块在整个提示语的顺序：打个比方，Claude 会主动推测总结的文章内容可能会比较长，这一part就会被移动到更前面。
    

完整的Prompt来了（长文预警），也可以直接滑到后面的部分，点个收藏方便复制👏

```
You are an expert content curator tasked with creating engaging summaries for social media sharing. Your goal is to craft a summary that captures the essence of an article while enticing readers to click and read more.Here is the article you need to summarize:

<article>  
{{article}}  
</article>

Before creating your final summary, work through your thought process inside <summary_analysis> tags. Follow these steps:

1. Re-read the article carefully, noting its structure (introduction, body, conclusion).  
2. Identify the core message and main points of the article.  
3. Extract 3-4 key sentences that best capture the article's essence. Quote these sentences.  
4. List the core points you've identified, numbering them.  
5. Identify the target audience of the article and note how this might influence your summary.  
6. Analyze the article's tone and style (e.g., formal, conversational, humorous) and how you might reflect this in your summary.  
7. Draft 3-4 potential hooks, numbering them (1., 2., 3., etc.). For each hook, note which social media platform (X/Twitter, Reddit, LinkedIn) it might be best suited for and why.  
8. Choose the best hook and explain your reasoning, considering its appeal across different platforms.  
9. Combine your chosen hook and core points into a rough draft of the summary.  
10. Refine the draft, ensuring it's concise yet informative. Count the number of sentences to ensure it's within the 3-5 sentence range.  
11. Re-read your summary and the original article to verify accuracy and completeness.After your analysis process, provide your final summary in <summary> tags. The summary should:  
- Start with the attention-grabbing hook you'

ve chosen  
- Include all core points from the original article  
- Be concise (aim for 3-5 sentences) yet informative  
- Be adaptable for multiple platforms (X/Twitter, Reddit, LinkedIn, etc.)  
- Reflect the article's tone and style appropriatelyRemember, your summary should balance being informative and intriguing, ensuring it captures the reader'

s interest while accurately representing the article's content.Here'

s an example of the desired output structure (note that this is a generic example and your actual summary should be based on the specific article provided):

<summary_analysis>  
1. Article structure: [Brief notes on introduction, body, conclusion]  
2. Core message: [Brief statement of the article's main idea]  
3. Key sentences:  
   - "[First key sentence from the article]"  
   - "[Second key sentence from the article]"  
   - "[Third key sentence from the article]"  
4. Core points:  
   1. [Point 1]  
   2. [Point 2]  
   3. [Point 3]  
5. Target audience: [Identified audience and how it influences the summary]  
6. Tone and style: [Notes on article's tone/style and how to reflect it]  
7. Potential hooks:  
   1. [First hook idea] - Best for [platform] because [reason]  
   2. [Second hook idea] - Best for [platform] because [reason]  
   3. [Third hook idea] - Best for [platform] because [reason]  
8. Chosen hook: [Number of chosen hook]  
   Reasoning: [Explanation of why this hook was chosen, considering cross-platform appeal]  
9. Rough draft: [Initial summary combining hook and core points]  
10. Refinement: [Notes on how the draft was improved, sentence count]  
11. Accuracy check: [Confirmation that the summary accurately reflects the article]  
</summary_analysis>

<summary>  
[Attention-grabbing hook] [2-3 sentences covering core points] [Final sentence that entices reader to learn more]  
</summary>

```

由于文章长度限制，我就不贴出多个优化版本了，直接来总结一下主动加入神级优化技巧的好处：

*   我最喜欢的一点是它的**精细程度**。从模型的执行步骤、到思考过程，再到输出部分，都被划分成了多个模块。就像玩乐高一样，我可以随时拆掉不需要的部分。
    
*   第二个惊喜点是，当我主动加入了多个神级技巧后，Claude没有把它们堆在一块，而是将它们**放置到理想的位置**，如 Re-reading (RE2) 会放在了执行步骤的第一步。
    
*   最后就是**足够规范的思维链输出**。思维链也是老熟人了。早期版本需要写下每一步，后来 `let's think step by step` 简化了这个过程，但后期处理起来很麻烦。模型会把思考过程和我实际想要的内容混杂在一起，放在 Web 界面用还行，但如果是 API 项目，那就是正则表达式噩梦了。
    

来看看实际运行的效果吧

输入是Claude这次更新的网页：https://www.anthropic.com/news/prompt-improver

![Image 36](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZjhhPev3vCv2Ta0WhyIR8M6cjlhiaHvS8k3jI9S9PF37zMb61mjGcDKQ/640?wx_fmt=png&from=appmsg)

是可以直接发到平台的程度

这里要额外吐槽一下，Prompt Console 存在一个大坑。

生成到最后一步时，当完整提示语还没有生成好，一定一定一定不要点击`Open in Workbench`，点了基本上是百分百会卡住。这时候要是刷新的话，钱是扣了，但得到提示语是个半成品。

![Image 37](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6Zg3kkXQuqnibGTIsibFNxzL7QHM5swoianxcvia75ic0wZca8G79mqOrzQgw/640?wx_fmt=png&from=appmsg)

看到底下这个圈就代表中奖了，我中奖了三回

接下来就是神级 Prompt 诞生的最后一步：

**样本收集**

将样本加到提示语里的好处非常明显，

![Image 38](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZSun4KH9p7RExHR7kT4huoxFic0CJEea3uDxJVFULtZicK5Vbx2l9BNMg/640?wx_fmt=png&from=appmsg)

样本自动生成，不需要手动收集

一是可以压缩提示语里非样本的部分，也就说样本足够有代表性的话，提示语里就不需要一堆规则了，模型可以直接从样本中“悟”出来。

![Image 39](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZibyeHSWCQl8MVqia8ROYDf7Rn2CTQ1EibWOaHjZjGvgNamLyxicWTJsCxA/640?wx_fmt=png&from=appmsg)

版本迭代

还有就是支持快速迭代。每次遇到想要好的摘要时，我可以直接加到工作台里，进行打分。Claude 就会加班加点，循环优化直到我满意为止，省去了还要给它解释为啥这个例子深得我心的麻烦。

按照这个思路，我把我常用的提示语们都“神化”了一遍。我还额外做了一版用来优化提示语的 Prompt，当作 Prompt Console 的免费平替。我把这个提示语放到文末彩蛋里了，Enjoy～

写在最后

看到这里，相信大家已经能给自己提示语安排上全套升级套餐了。

我的朋友们看到初稿的时候，表示已经对神级 Prompt “祛魅”了。

打造出自己的神级 Prompt 比想象中更简单，

以自己和 AI 聊天记录制造出来的神级 Prompt 天生就“懂”你。

更有意思的是，上手自己的神级 Prompt 后，我发现自己偶尔会染上 AI 味儿，

具体表现为上面提到12个优化技巧里，有一半都可以直接手敲出来的，根本不需要模型辅助。这时候写提示语就有一种晋江大神写小说的爽感。

提示语优化技巧的好记好用，其实也是大模型能力提升的体现。它们不再需要限制，而只需要引导。这一定位的改变，也让提示语们能组合使用，集成在长度有限的系统提示语里，成为大模型默认能力的一部分。

我有预感，有一天技巧们都会消失，

与 AI 沟通从文本转移到语音，甚至是脑机接口，

那时候的 AI 能出从零碎的思考过程里直接提取出我们想读的，想买的，想看的，想要的一切。

所以我很高兴能在通往 AGI 的路上见证到各式各样提示语，有种手办收藏的满足感。

我开始期待后面的新神Prompt

又会带来什么样的惊喜！

@ 作者 / 卡尔@ 动手学AI知识库 / learnprompt.pro

* * *

最后，感谢你看到这里👏如果喜欢这篇文章，不妨顺手给我们_点赞👍｜在看👀｜转发📪_更多的内容正在不断填坑中……

![Image 40](https://mmbiz.qpic.cn/mmbiz_png/YEhakvKZjXkISvpOV9JYuRgOjzWcdm6ZECp4JSGmhZh781t2j9fJHayTia3hP1qiaTUUByViaSl5jrDtAswSXMia6A/640?wx_fmt=png&from=appmsg)

今日份的彩蛋码是🎲🎲🎲 公众号发送`神级`
