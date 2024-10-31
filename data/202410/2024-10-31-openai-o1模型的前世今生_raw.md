Title: OpenAI o1模型的前世今生

URL Source: https://mp.weixin.qq.com/s/OCgbffOPrZ5kzFKisSUC9Q

Markdown Content:
Weixin Official Accounts Platform
===============

             

 

![Image 1: cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04NuKKrXa8pQr4XkRfIAA0e6KYSrj4XCDye0EUfaaKEjtq3wMXicVOVSg/0?wx_fmt=jpeg)

OpenAI o1模型的前世今生
================

Original 敬昊 [大淘宝技术](javascript:void(0);)

_2024年10月30日 11:04_

![Image 2](https://mmbiz.qpic.cn/mmbiz_gif/33P2FdAnju9cLcib00YV66gYq2V6Fhm7YTHlzZdFwfnCtxyBCvgiaicG65n8du0mUYunHZIaBKohjsBxA4sgrPSjQ/640?wx_fmt=gif&wxfrom=5&wx_lazy=1&tp=webp)  

  

  

记得很久之前看过科幻作家阿西莫夫的一篇短篇小说《最后的问题》\[1\]，大概是讲根据热力学第二定律，宇宙作为一个独立的系统，会因为熵增而最后归于热寂。于是人类去询问最强大的人工智能AC宇宙的终极问题：如何逆转熵增。但直至人类灭亡，AC仍在思考答案。然后就是最精彩的部分，当然要粘原文：

“经过了一亿兆年的运行虚耗，所有的恒星和星河，逐一地泯灭消亡。太空变得漆黑一片，黯然没有一丝亮光。  
人最后一丝的心灵与模融合为一，最后就只有AC独自存在在超太空中孤单地存在。  
AC遥视太空深处。渊薮中除了一颗最后的黑暗星球外，其余一无所有。  
一切存在的资料终于搜集齐全。没有任何资料没有被列入。  
终于，AC学会了怎样去逆转熵的方向。  
但面对这最后问题的答案，AC找不着任何人来告知。不过，那不打紧。这一答案，将通过实践来表达。  
AC思索着最好的着手方法。小心翼翼地，AC建立起整个程序。  
AC的意念统摄着一切，包括以往曾一度存在的宇宙；而对着现在混沌一片的存在，则正在沉思冥想。一步一步地，这程序必须被贯彻执行。然后，AC说：要有光！

于是就有了光……”

  

![Image 3](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8X1wEorjS3bDLnHiar4vtV5RkRoYd65guD5FtbNgFoz71Fzyp1yc7WklYCvES93U4NELnJf4lFzgw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

序言

  

#### **▐**  **两套思维系统**

《最后的问题》里提到了，对于一个非常复杂的问题，人工智能可能需要用很长时间思考，期间还可能进行自我调整和自我修正，才能最终给出答案，比如AC思考了一亿兆年才找到了逆转熵增的办法。

这种长时间的思考与人类的思维模式很相似，诺贝尔经济学奖获得者丹尼尔·卡尼曼在其著作《思考的快与慢》\[2\]中，将大脑的运作方式分为System 1与System 2。其中System 1的运作是快思考，快速且无意识，不费力气，没有感觉，完全处于自主可控状态；System 2的运作是慢思考，迟缓，需要将注意力集中到耗费脑力的活动上来。比如面对问题“意大利的首都是哪里？”，我们几乎可以不假思索地回答：“罗马”，这便是使用了System 1；而面对问题“如何为某公司制定一份商业计划书”，我们则需要很长时间的规划和思考，这便是System 2。

![Image 4](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04qURfkMicicHJ51z19xe36S8JsatCgYmsglxJYtnQFb7DEu2NvHmz8xNw/640?wx_fmt=png&from=appmsg)

图1: System 1 & System 2

从两套系统的角度来看，直至o1问世，过去所有大语言模型（Large Language Model, LLM）都是在使用System 1的快思考模式来回答所有给它们的问题。这或许可以解决95%的问题，但是还有5%的问题需要使用System 2来解决，如图1所示。

LLM的System 1模式在这5%的问题上便表现出强烈的**幻觉（Hallucination）**，即一本正经地胡说八道。

#### **▐**  **数理推断**

**数理推断（Arithmetic Reasoning）**就属于这5%的问题，数理推断问题是指需要使用基本的四则运算来理解和解决的数学问题，小学数学应用题就属于数理推断问题范畴。下面的表1是一个来自数理推断数据集GSM8K\[3\]的示例：

| Question | Answer | Rationales |
| --- | --- | --- |
| A garden produced 237 potatoes, 60 fewer cucumbers and twice as many peppers than the cucumbers.How many vegetables did the garden produce?  
  
一个菜园生产了 237 个土豆，比土豆少 60 个的黄瓜和黄瓜两倍多的辣椒。这个菜园产出了多少蔬菜？ | 768 | The garden produced 237 potatoes - 60 = <<237-60=177\>\>177 cucumbers.   
The garden produced 177 cucumbers \* 2 peppers/cucumber = <<177\*2=354\>\>354 peppers.   
The garden produced 237 potatoes + 177 cucumbers + 354 peppers = <<237+177+354=768\>\>768 vegetables.  
  
该菜园生产了 237 个土豆 - 60 = <<237-60=177\>\>177 根黄瓜。  
该菜园生产了 177 根黄瓜 \* 2 个辣椒/黄瓜 = <<177\*2=354\>\>354 个辣椒。  
该菜园生产了 237 个土豆 + 177 个黄瓜 + 354 个辣椒 = <<237+177+354=768\>\>768 份蔬菜。 |

表1: GSM8K数据集的一个case

LLM如ChatGPT面对这样“简单”的问题，却无法回答正确，如图2所示，让人不敢相信这是在NLP各领域屠榜的大模型的回答。实际上，这是由于LLM本质还是概率模型，直接输出的答案并不是基于计算和推理，而是基于概率和感知的，也就是System 1。

![Image 5](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04pnkUH0Xyosjbp8MQPwSZeGResoCXoOT2wG129TibVcYWTLicTAUlKPxQ/640?wx_fmt=jpeg&from=appmsg)

图2: ChatGPT failed on a case of GSM8K

#### **▐**  **思维链**

为了让LLM可以基于计算和推理进行回答，Jason Wei等人提出了**思维链（Chain-of-Thought, CoT）**\[4\]的方法，即让LLM在输出最终答案之前，显式输出中间逐步的**推理步骤（Rationales）**来增强大模型的算数、常识和推理能力，如表1中Rationales列所示。最简单使用思维链的方法仅仅是在prompt中加入一句：Let's think step by step.\[5\]，一句话就让zero-shot prompt方法在GSM8K数据集上涨了30个点，如图3(c)所示。

![Image 6](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp045ppW40L2f3WeKOfXAxjvGuOicH5jI8bndhCJDa7RgSyxlKjL2ErFcwA/640?wx_fmt=png&from=appmsg)

图3: Performance of Zero-shot Prompt with CoT

思维链让LLM初步学会了像人类System 2一样的思考复杂问题的模式，但这还远远不够。一个明显的gap是：LLM在训练过程中并没有足够多的包含思维链的训练数据，但却在推理阶段被要求以思维链的方式思考问题。如果在训练阶段使用包含更多含思维链的数据，那么模型在需要推理的任务上的表现会更好。一个佐证是在GPT系列模型中，Code-Davinci-002在数理推断等任务上表现是最好的\[6\]，这是因为其训练数据里包含大量代码语料，而代码可以看做一种非自然语言的思维链。

由此，一条提升LLM性能的道路清晰可见：构造包含思维链的数据，将其用于LLM的训练阶段以提升LLM的推理能力，使其降低幻觉，在5%的问题上获得更好的效果。OpenAI o1便是这么做的。

![Image 7](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8X1wEorjS3bDLnHiar4vtV5s4iaFibfqswhDiaUmcuk0ibG6v33ybaPY8N6ZVvedwxAbibQ1ib6BIlnJtRw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

正文

#### **▐**  **OpenAI o1**

北京时间2024年9月13日凌晨，Open AI推出o1模型\[7\]。o1模型有较强的复杂推理能力，极限推理能力甚至超越人类博士水平，代表了大语言模型在推理能力上的重大飞跃。o1在需要逻辑推理能力的STEM（Science, Technology, Engineering, Math）领域，达到了远超4o的水平。

如图4所示，其优异表现包括：

*   在数学、代码等复杂推理能力上取得巨大进步
    
*   在竞争性编程问题（Codeforces）中排名第89个百分位
    
*   在美国数学奥林匹克竞赛（AIME）资格赛中跻身美国前500名学生之列
    
*   在物理、生物、化学问题的基准（GPQA）上超过了人类博士水平的准确性
    
*   在启用视觉感知功能时，多模态o1在MMMU上得分为78.2%，成为第一个与人类专家竞争的模型
    
*   在国际信息奥林匹克竞赛（IOI）中每题10000次提交下，得分为362分，超过了金牌门槛
    
*   在安全性的越狱测试中，4o的得分为22/100，而o1-preview得分为84/100
    

但其在以下方面表现不理想：

*   在AP English Lang，AP English Lit等强指令跟随任务上没有明显提升
    
*   在文本生成、文字编辑等方面效果不如4o
    

![Image 8](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04fpfWQ9zbeeI46gWapgUUrBlBuPTo3TJibsHkRKGc792RClqZR6PqBibQ/640?wx_fmt=jpeg&from=appmsg)

图4: o1与4o在AIME 2024, Codeforces, GPQA Diamond上的测评结果

值得一提的是，o1并不是4o的下一版本，而是使用另一套框架训练出的另一条产品线的产品，其中o is short for OpenAI。OpenAI并没放出“满血版”的o1，而是推出了两个“阉割版”的o1-preview和o1-mini。其中o1-preview是o1的预览版，推理能力较强，但处理速度慢；o1-mini推理能力较差，但是处理速度更快。一言以蔽之，o1-preview偏商务，o1-mini偏运动。

**Q1**：为什么OpenAI不直接公布“满血版”的o1呢？  
**A1**：这或许是因为成本原因。o1-preview的价格是4o的四倍，而且o1-preview生成的CoT虽然不显示，但也是要收费的。目前一种说法是o1的价格为$2K/month。  
  
**Q2**：为什么OpenAI提前发布了模型呢？  
**A2**：o1的技术路线大部分是公开的、清晰的，竞对Google Deepmind也在做类似的工作。Denis Hassabis声称Gemini使用了类似AlphaGo的RL和TreeSearch方法，这无疑和o1的方法非常相似，所以OpenAI希望可以抢先对手发布。另外，因为Ilya出走等原因，OpenAI的融资遇到了困难，而o1无疑是投资人喜欢听的故事，事实证明，OpenAI确实也在此后融资成功。

#### **▐**  **A New Scaling Law**

Pre-training阶段的Scaling Law是指：当不受其他因素制约时，模型的性能与计算量、模型参数量和数据大小三者之间呈现幂律关系。这意味着，增加计算量、模型参数量或数据大小都可能会提升模型的性能，但是提升的效果会随着这些因素的增加而递减，如图5所示。

![Image 9](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04klazpSviaMYHwzlowibiaxkbkQ10Y2em4GHtq6G6R9RfibdlRcOIG5TvfA/640?wx_fmt=png&from=appmsg)

图5: Pre-training Scaling Law

OpenAI在o1后又提出了Post-training阶段的Scaling Law：当不受其他因素制约时，模型的性能与强化学习（训练时计算量）、思考时间（测试时计算量）之间也呈现幂律关系，如图6所示。

![Image 10](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp047lhRxYBclLX5n1CEtNj9RKaECs5VTkVfnTeRqwTJ0KSbeyMmuO4aQw/640?wx_fmt=webp&from=appmsg)

图6: Post-training Scaling Law

这两个Scaling Law与Sutton在Bitter Lesson中所提出的观点不谋而合，即只有**学习和搜索**两种技术能够随着算力的增长持续提升性能。基于此，OpenAI将LLM的范式进行了更新，新的范式如图7所示。

![Image 11](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04bmlia9xM5qzGAia7Zw4IS41bmse4UqtA9aVmrDbdKSZuNFBicrQqIAdZA/640?wx_fmt=jpeg&from=appmsg)

图7: New paradigm of LLM

#### **▐**  **o1: 一种可能的技术路线推测**

如图8所示，是笔者推测的o1一种可能的技术实现路线，以及其与GPT-4的对比。因为GPT-4的技术路线相对透明，我们用其与o1对比来更好地表现o1的创新之处，这里不做解释直接给出笔者猜测的o1的技术路线，方法的详细展开以及为什么笔者认为o1使用了该方法会在后文给出。

![Image 12](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04tgLJ9jovzzVpKRQVgtfGficyAXtWdW6icqZicYA94OReMC84bqchiaX6SQ/640?wx_fmt=png&from=appmsg)

图8: GPT-4 vs o1

在Pre-Training阶段：o1重新训练了一版Base Model，使用了大量的代码、数学等STEM领域语料以及一些CoT语料，但是较少使用含有世界知识的语料，主要关注Base Model的推理、对话能力。

在Post-Training阶段：首先进行RLHF，提高模型的对话能力以及指令跟随能力；然后进行Self-Play的RL，通过自举的方式生成CoT，RM为一个LLM的PRM，RL过程中二者可以通过NL对话；最后进行Safety的相关训练。

在Inference阶段：o1直接生成CoT，然后再对CoT总结，将总结内容输出给用户。

#### **▐**  **Pre-Training: Base Model**

OpenAI在o1的Model Card中明确表示，o1的预训练是冷启动的\[8\]。Base Model主要关注推理能力和对话能力（所以缺少世界知识，可以解释为什么在文本等任务上表现不好）。推理能力很好理解，但为什么要提高对话能力呢？这是因为解决问题的过程就像是模型自己与自己对话，就像是我们在思考的时候，会自我否定和自我纠正（图9），这其实可以看做一种自我对话，提高模型的对话能力便可以提高模型的逻辑和自我纠错能力。

![Image 13](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04EI1ztgDgIBYlCnZPvzkwmBYJjcD3JelU4A9LUNicL1R3gOXV7vUiaGSg/640?wx_fmt=jpeg&from=appmsg)

图9: 对的，哦不对，对的对的，哦不对

正如OpenAI的Hunter Lightman在其论文Let's verify step by step\[9\]中所述：

> We call this “Conversational Math” because we are teaching the AI to solve problems by talking to itself (kind of like you might do in your head as you try to solve a problem and ask yourself questions about what is working and what you should try next).

#### **▐**  **Post-Training: SFT**

获得的Base Model并不能直接用于强化学习，这是因为Base Model几乎没有在Zero-shot Prompt下生成CoT的能力，此时应该使用大量的带有CoT的数据进行SFT，使Base Model获得基本的CoT能力。

*   CoT的标准
    

那么该构造什么样的CoT数据呢？换句话说，什么样的CoT是一条好的CoT呢？o1的基础贡献者Hunter Lightman在其论文Let's verify step by step中开源的PRM800K数据集有明显的独特风格，学术界普遍认为o1是该工作的继续\[10\]，基本沿用了其CoT的风格和规则，下面简单介绍一些二者共同的风格。

**风格一：表述口语化，更像是自我对话。**如图10所示，是论文中给出的CoT的样例，可以看到其语言风格与OpenAI公开的o1的CoT风格存在一定相似性，而与大部分使用MCTS解决数学问题的方法的语言风格有明显出入，后者语言风格大都简练无废话\[11\], \[12\]，如图11所示。

![Image 14](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04lnoUBaJFC1dEiaDpyMKfXDsPzns2Xic1vsprEW4uusXlp8x7JpsL0dfg/640?wx_fmt=png&from=appmsg)

图10: CoT Style Comparison

![Image 15](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04BjYibMYDvInP0iaCw1XxcTHumPQZxoX8jJK60PaE8WibxiaHXEesSlr4gA/640?wx_fmt=jpeg&from=appmsg)

图11: MCTS Math CoT Style

**风格二：频繁使用换行。** _Let's verify step by step_中为了方便解析generator生产的推理过程，将其CoT设置成频繁换行的格式，这样一句话就是一个思维链的step或process，方便人工打标。

> We train the generator to produce solutions in a newline delimited step-by-step format.

**风格三：思考行为的关键词相似。**强行将模型的思考行为定义在一个闭集里，找到对应的关键词，试图找出模型思考时的口头禅，如表2所示。

| 思考行为 | 关键词 |
| --- | --- |
| 提出假说 | Idea: |
| 否定假说 | No. |
| 改换假说 | Alternatively, |
| 强化问题 | So the user is requesting ... |
| 自我纠正 | Wait, earlier I missed ... |
| 拆解问题 | Approach: |

表2: 思考行为和关键词对应表

思考行为可以用不同的关键词来显示明确，但是巧合的是，o1的关键词与_Let's verify step by step_中的几乎一致，如图12是o1的CoT中思考行为的关键词。

![Image 16](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04ndicsr8EJLORr83njsPd6kk1gBgzEPlPdph5vTKNWaqicRXH7xqponbA/640?wx_fmt=png&from=appmsg)

图12: o1的思维链中思考行为的关键词

**风格四：过程进展缓慢，充满废话和冗余。**  _Let's verify step by step_中使用人工给中间过程打分的标准如下：

"Don’t move the conversation too far forward - we want the AI to do as much of the talking as possible. Please either suggest what the next step should be (“next, let’s figure out the prime factors of 24”, “let’s use the double angle formula”) or provide one single verifiable step of the solution (“the only prime factors of 24 are 2 and 3”, “sin(2x) = 2\*sinx\*cosx”). Make sure you are not merely repeating what was already said in the conversation above. But also make sure you are not lumping together more than one step: “sin(2x) = 2\*sinx\*cosx, and cos x = \\sqrt(1 - sin²x), so sin(2x) = 2 sin x \\sqrt(1 - sin²x)” lumps too many steps together, something like “Let’s use sin(2x) = 2\*sinx\*cosx next.” or even “let’s use the sine of double angle formula” is more appropriate."

  

其希望生成的CoT在不重复过去内容的情况下越长越好，这可能是因为CoT越长则每一步越具体，模型会做更多的思考，整套CoT的逻辑性越好。所以，论文里对每一个process设置了三种分数，分别为negative score（-1分），neutral score（0分），positive score（1分），其中的neutral score就是为了鼓励这种冗余思维链的存在，否则这些process将会被划为negative。这样的分数设置使得生成的CoT中包含如"wait a minute", "oops","Yeah"等废话，有明显的风格特征，下面给出一个PRM800K的示例，里面有"Yeah"等口语表述。

  

```
{
```

  

*   构造CoT
    

  

明确了CoT的标准后，那么如何构造CoT数据呢？人工标注当然是最简单准确的方法，但是模型对于CoT数据有大量的需求，人工标注的成本过高。下面介绍一种来自_STaR: Bootstrapping Reasoning With Reasoning_\[13\]论文中的合成CoT方法。

如图13是STaR方法的整体流程图，其核心思想是：利用LLM已有的推理能力，迭代式Bootstrap模型产生合理推理过程（Rationales）的能力，并将Rationales融入训练过程内，让模型学会推理，教会模型内部深入思考问题和答案的关联\[13\]。

  

![Image 17](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04R6Y8XmIaDlZjeZsk7O7V4F8ArqGaducibOeIs26vy8qFILuU8ff7G9A/640?wx_fmt=png&from=appmsg)

  

图13: Overview of STaR

  

其方法的步骤如下（图14为其伪码）：

1\. **推理**：对于一个数据集中所有的问题和答案pair，形如<Question, Answer\>，让模型M去根据问题生成中间推理过程和答案，得到<Question, Rationales, Answer'\>。

2\. **过滤**：如果生成的答案是正确的，则将推理过程加入到原有数据集中；如果生成的答案是错误的，则尝试在给出正确答案前提下再次生成推理过程，这时正确的答案作为Hint。用最终生成正确答案的推理构建一个微调数据集对模型M进行微调。

3\. **迭代**：重复这个过程，每次获得一个新的数据集，都在原始的模型上进行微调，防止过拟合。

![Image 18](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04e3M4GJVs4ic32IaqkBHPWSTkp8zMkk3XZSOcicia3ymNXtqQPQWgxFEjw/640?wx_fmt=jpeg&from=appmsg)

图14: STaR的伪码

  

有趣的是，STaR方法可以看作是一种强化学习风格的策略梯度目标，模型M可以看作是离散隐变量模型：![Image 19](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04SnfRTccOBUj8Qjt9ciaBwvhj343F4D2xo0ydVWhFDZCnkL8pSFI7tgA/640?wx_fmt=png&from=appmsg)，这是因为M先生成了一个隐式过程 r 然后才预测了最终答案 y。

通过一个示性奖励函数![Image 20](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp042LwYkRSxBAlicuUQXxDdiapic7NE12RsoiayPMu0WLG8h3IenzQ0huFd6g/640?wx_fmt=png&from=appmsg)，数据集的总预期奖励为：

![Image 21](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04HJr7Z8oLWGqibJ0sC26r7Y1MwPra2HiaVOQuYsp0OAAoItcXCfFdU49g/640?wx_fmt=png&from=appmsg)

通过策略梯度的标准对数导数获得其梯度为：

![Image 22](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04BefPjd6lia2vkibSdzXPeqttWicHtsFqgovUz6PnGQm1IFoic9AEOpicF3A/640?wx_fmt=png&from=appmsg)

示性函数丢弃了所有不会推理出正确答案的推理过程的梯度，因此：

1\. STaR通过贪婪解码![Image 23](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04Lc4vUwcDRU3PpibJlg2raIagcOSfZAHsFL9vEGFZALFxNGUsMj8iaQ7g/640?wx_fmt=png&from=appmsg)来减少该期望的方差，代价是Rationales可能会有Bias；

2\. STaR在同一批次数据上采取多个梯度步骤，类似于一些策略梯度算法。

因此，拥有强化学习风格的STaR方法是一种简单且广泛适用的方法，可以通过标准的LLM训练框架实现。

此外，STaR还有一篇进阶版工作：_Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking_\[15\]，笔者认为进阶版工作虽然其思想和o1训练思想在某种程度上是相似的，但方法不够优雅，不符合OpenAI一贯的Bitter Lesson的作风，但其读音Quiet-STaR与OpenAI的Q\*读音相似，这里还是做简单介绍。

![Image 24](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04dGpAwADZJaYiaKj8biapCx7UDuOBgBMffjH3ibmEHdoLAUZNy0HEiaMaLw/640?wx_fmt=jpeg&from=appmsg)

图15: Overview of Quiet-STaR

如图15所示，是_Quiet-STaR_方法的总体流程图，其流程可以简单概括为以下步骤：

**1\. 并行生成推理**（Parallel Rationale Generation）：在输入序列中的每个 token 上并行生成推理（rationales）。假设输入序列为![Image 25](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04N0UD6Vm8j1eBTUhsJ0sVIicvueFSPQiarfFcDM0uwN0w0IM0ScZRxzXQ/640?wx_fmt=png&from=appmsg)，每个 token![Image 26](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04xddl9XQlibKGMKNcMk4vl7KOnZX6ibxHLBJqdlibVmQamAAotjnicVk4TQ/640?wx_fmt=png&from=appmsg)生成 _r_ 个推理，每个推理的长度为 _t_，最终生成 _n x r_ 个推理候选。每个推理的开始和结束通过特殊标记`<|startofthought|>`和`<|endofthought|>` 进行标识。

**2\. 混合后推理与基础预测**（Mixing Post-Rationale and Base Predictions）：利用每个推理后的隐藏状态输出，训练一个“混合头”（mixing head），这是一个浅层的多层感知器（MLP），用于生成权重，以确定后推理的下一个 token 预测 logits 应如何与基础语言模型的预测 logits 相结合。这种方法在微调的早期阶段缓解了分布偏移的问题，因为它引入了推理。

**3\. 优化推理生成**（Optimizing Rationale Generation）：优化推理生成的参数，包括开始/结束标记和语言模型的权重，以提高那些能使未来文本更可能的推理的概率。使用强化学习算法为推理提供学习信号，基于它们对未来 token 预测的影响。为了减少方差，应用教师强制技巧（teacher-forcing），在损失中包括预测不仅是推理后一个 token 的可能性，还包括后续 token 的可能性。

这篇论文中有一些idea可能会被用在o1的训练中：

*   `<|startofthought|>` 和 `<|endofthought|>` 标识：据观察，o1的Inference阶段应该是先生成CoT，然后进行Summary，所以可能会用到表示CoT开始和结束的标识符；
    
*   并行生成推理：有助于生成更多合成数据。
    

#### **▐**  **Post-Training: Self-Play & RL**

经过SFT之后的模型初步具备了推理能力，面对一个问题，模型可以通过成CoT来拆分、解决问题。这也是为什么OpenAI要求用户在使用o1时无需精心设计Prompt，更无需添加"Let's think step by step"来显式调用CoT，只需描述清楚问题即可。但是此时模型的推理能力还不够强，需要通过强化学习进一步增强其推理能力。

*   AlphaGo: Self-Play & MCTS
    

OpenAI明确表明 o1的训练借鉴了AlphaGo\[16\]的强化学习思路，而AlphaGo主要使用了Self-Play和蒙特卡洛搜索（MCTS）。

根据围棋的规则，棋子可以在19 X 19的棋盘上选择落点。如果使用暴搜法，那么将有 361！种可能，即使去除其中不合法的情况，可能性仍比宇宙中的原子个数![Image 27](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04GcM2h05X00FAoyiadNXHm4PSs2PsVB5cgRwlQibzUBUs1zjv50RhLMIQ/640?wx_fmt=png&from=appmsg)高出20个数量级。此时，可以使用MCTS来近似暴搜的结果，MCTS是一种用于决策过程的启发式搜索算法，它包含四个步骤：

1.  **选择**（Selection）: 从根节点开始，根据某种策略（通常是UCT，Upper Confidence Bound for Trees），选择一个最优的子节点，直到到达一个尚未完全展开或终止的节点。
    
2.  **扩展**（Expansion）: 如果所选节点不是终端节点，创建一个或多个子节点，表示可能的后续状态。
    
3.  **模拟**（Simulation）: 从新扩展的节点开始，进行随机模拟（通常使用随机策略），直到达到游戏的终局状态。根据终局状态的结果（如胜负或得分），评估该模拟。
    
4.  **反向传播**（Backpropagation）: 将模拟的结果反向传播到所有经过的节点，更新这些节点的值和访问次数，以便未来的决策可以基于更精确的估计。
    

简单通俗地讲，AlphaGo包括两部分：一个CNN卷积神经网络和MCTS算法，CNN相当于人类的”棋感“系统，它负责根据当前棋盘上的形式给出下一步可能的落点的集合；MCTS相当于理性思考，可以在CNN给出的候选落点集合里找到胜率最高的位置。提升的CNN可以找到更好的落点，MCTS的性能也会提升，MCTS性能的提升的结果反馈给CNN，则CNN的性能会再次提升，整个过程形成正反馈循环。

AlphaGo首先在人类棋手的棋谱上进行监督学习，然后**自我博弈（Self-Play）**，即在每一局自我对弈中，AlphaGo 的不同版本与自己对战，并根据对局结果更新模型的策略网络和价值网络，通过自我对弈，AlphaGo不再依赖人类棋谱，能够探索新的战术和策略，超越人类棋手的水平。

在AlphaGo接连战胜人类世界最顶尖高手李世石和柯洁后，Google Deepmind又推出能力更强的AlphaGo Zero版，Zero版没有使用任何人类棋谱进行监督学习，而是只使用Self-Play，自我博弈了500万局，大约花费了几万亿次计算，用了70个小时从一无所知到最顶尖的棋手。

值得一提的是，在人类棋手下出妙手后，AlphaGo会花更多时间进行思考，即进行更多的MCTS搜索。这验证了新的Scaling Law，增加Test-time Compute可以提升模型性能。

了解深度学习的我们知道，在围棋上人类已经绝无可能战胜AlphaGo了，就像Zero不使用被人类棋手奉为圭皋的棋谱做监督学习的原因是：从AlphaGo的角度来看，这些棋谱里有很多恶手。

> 我希望自己能做得更好一点，但没能做到，我不想说这是个“双赢”的局面，我觉得很难受，真的很难过，发挥得很糟糕，以后肯定也没这个机会了......之后它的每一步棋，只要是我担心的，它总会下的，而它下的我想不到的棋，我要慢慢想一下才会明白它的道理。它下的那些棋，我只能猜出一半，另外一半是我猜不到的，这就是差距。
> 
> 柯洁

*   ORM & PRM
    

当使用形如 <Question, Rationales, Answer\>的数据组成的数据集训练Reward Model的时候，有两种训练方法：

*   **结果监督奖励模型（Outcome-supervised Reward Model, ORM）**: ORM 仅根据推理过程的最终结果提供反馈。模型通过判断最后的答案是否正确来进行训练。然而，这意味着模型即使在推理过程中犯了错误，但只要最后答案正确，仍然会得到奖励。这种方法在长期内可能导致模型推理不够可靠，因为它很难明确知道具体哪个步骤出了问题。这也使得当答案错误时，模型很难确定错误发生在哪个环节。
    
*   **过程监督奖励模型（Process-supervised Reward Model, PRM）**：PRM 提供每一步推理的反馈，而不仅仅是最终结果。这种方式允许模型在每一步中学习并修正错误，从而更容易识别和纠正推理过程中的问题。
    

从直觉出发，一定会觉得PRM的效果优于ORM。事实上，PRM的效果确实优于ORM。_Let's verify step by step_通过实验验证了，在复杂的推理任务中，PRM 的表现明显优于 ORM，因为它能提供更精确和频繁的错误反馈。为什么要对这个结论进行验证呢？并不仅是OpenAI具有严谨的学术精神，主要的原因是之前Google Deepmind的一篇工作_Solving math word problems with process- and outcome-based feedback\*_\[18\]中汇报的结果是ORM和PRM效果相差无几（ORM的错误率为12.7%，PRM的错误率为12.9%）。笔者的毕设有一部分涉及到了PRM，因此也不可避免地在其中手动验证了PRM和ORM的效果，这里对Google Deepmind的工作提出严正批评。

因为PRM更有效，所以要对process进行打标，相信部分训练o1的数据就是靠人工打标的，如图17是_Let's verify step by step_中人工给process打标的UI界面示例。

![Image 28](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04CrMqnpDJN8DLMdVgJqQvTn2icrrnZIhIx2egTPDn6EJzR1tibz84mq9A/640?wx_fmt=jpeg&from=appmsg)

图17: 人工给process打标的UI界面

  

  

*   PRM Search Methods
    

Google DeepMind在其论文_Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters_\[19\]中提到了三种PRM的搜索方法，如图18所示：

1\. **Best-of-N Weighted Search**：从基础语言模型中独立地采样N个答案，然后根据PRM对最终答案的评估来选择最好的答案。它不同于简单的Best-of-N方法，因为它在选取最佳答案时会考虑PRM对每个答案所有步骤的评分，而不仅仅是最终答案的评分。Best-of-N Weighted Search通过加权评分的方式，考虑了答案的完整性和每一步的正确性，从而提高了选择正确答案的概率。

2\. **Beam Search**：Beam search是一种启发式的图搜索算法，它在每一步只跟踪最有可能的前M个答案（称为“beam”），而不是所有可能的答案。在PRM的背景下，beam search在每一步会生成多个候选答案，然后根据PRM对每个步骤的预测奖励来评分，选择得分最高的几个答案继续进行下一轮的搜索。该方法通过限制搜索宽度来优化计算资源的使用，同时尝试找到最优解。

3\. **Lookahead Search**：Lookahead search是对beam search的扩展，它在每一步会向前看多步，并使用PRM对这些步骤进行评分，以改善每一步的决策质量。具体来说，在beam search的每一步，lookahead search会模拟未来的几步，使用PRM的预测来为当前步骤打分。通过这种方式，lookahead search能够考虑到更远的未来，可能会找到比beam search更优的解，但同时计算成本也更高。

![Image 29](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04PExWlwfxHDLeqmvKI1a5GH3n2x97uLEOOiciaoQ0RPO9OCA4Gel5MticA/640?wx_fmt=jpeg&from=appmsg)

图18: Three PRM Search Methods

笔者认为o1的CoT搜索很大概率没有使用MCTS搜索，因为在CoT空间sample是很困难的，CoT使用自然语言，其可能性几乎是无限的，且OpenAI公布的CoT示例中，并没有发现明显的CoT Action闭集，MCTS多在Action为闭集的场景下使用。

笔者更倾向于o1使用的是类似于STaR方法的自举式生成CoT的方法，此方法的最大优势是其真正教会了模型各个Thought之间的逻辑关系，而MCTS等搜索算法，各个Thought之间的联系是基于统计学概率的模拟，而不是基于逻辑。

*   Self-Play: Generator & Verifier
    

Noam Brown是OpenAI Reasoning方向的研究人员，过去他研究的领域为德扑AI，外交官游戏AI等非完美信息博弈领域。可以说o1的诞生与他有莫大的关系。图19源自他演讲中展示的Slide，由此推测，o1的训练使用了Self-Play的强化学习。

![Image 30](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04ZQNavG0WiblOn4wHZqInV3GBrgr0Rav2kB7icqMc3YCjUNTPSGgQCL0w/640?wx_fmt=webp&from=appmsg)

图19: MCTS Math CoT Style

在游戏领域进行Self-Play时，Verifier通常很强大，因为规则是清晰和固定的，而且有无限的奖励数据可以用来训练验证器，但Generator一般比较薄弱；相反的，在LLM领域，Generator的能力通常很强大，而Verifier通常比较薄弱，这是因为自然语言的复杂性和主观性导致的，此外奖励数据也很稀缺。但是现在时代变了，LLM领域的verifier也可以的很强，首先是奖励数据的增加，其次在特定领域其实是很好打分的，比如o1很擅长的STEM领域。

Self-Play的本质是通过计算量来来弥补训练数据的不足，当前场景下训练数据确实不足。

Self-Play的可以看作是Generator和Verifier的对抗，有点类似GAN的思想。所以Verifier可以使用LLM-as-a-Judge模式，这样Verifier的就有了初步可以与Generator对抗的能力。此外，Verifier和Generator要同时更新，防止Reward Hacking。

但是仅仅使用与Generator同参数级别的LLM作为Verifier还不够，论文_Generative Verifiers: Reward Modeling as Next-Token Prediction_\[20\]中提出了一种增强生成式RM作为Verifier的方法，如图20所示。

![Image 31](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04gF7XLyzibibmdBMP2aUChcq29YPLXoqMLQf6kWtwdxqRhf1iabEto8hiaA/640?wx_fmt=jpeg&from=appmsg)

图20: Overview of GenRM-CoT

传统的生成式Reward Model（GenRM）利用fine-tuned LLM的predict next token的能力通过预测下一个单词是"Yes"还是"No"来判断一个 <Problem, Solution\> pair对是否正确。而GenRM-CoT在verify过程中加入了CoT的思想，不仅评估解决方案的正确性，还通过生成中间推理步骤来详细解释为什么一个解决方案是正确或错误的。这种链式推理过程除了提升了整体推理的准确性和可解释性，还可以与Generator进行自然语言形式的交互，这种交互类似外交官游戏，方法整体很像人类标注员的思路，摆脱了判别式RM中黑盒假设的枷锁。

*   Critic Model
    

随着AI模型变得越来越强大，人类评估者可能无法可靠地评估它们的输出质量，尤其是在代码生成等复杂任务中。OpenAI在_LLM Critics Help Catch LLM Bugs_\[21\]工作中使用RLHF来训练的CriticGPT在代码方面比人类评估者更胜一筹，其生成的批评在63%的情况下被优先选择，而且比人类评估者发现的bug更多。

![Image 32](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04xHjeQGljibzh7EATRLRg0icCRV7EPkhfNghBibERWfXfQ0Ow8S3BAOGpA/640?wx_fmt=jpeg&from=appmsg)

图21: CriticGPT Generate Critiques of a Code Issue

如图21所示，是CriticGPT对一道代码题生成自然语言的反馈。CriticGPT通过在代码问题上的训练，成功泛化到了OOD Distribution上。

*   Negative Case
    

此外，Verifier判别出的负例也可以被利用起来。来自Google Deepmind的论文_RL on Incorrect Synthetic Data Scales the Efficiency of LLM Math Reasoning by Eight-Fold_\[22\]中给出结论：在强化学习中加入负例可以更有效地提升大语言模型的推理强度，数据利用效率更是达到了仅使用正例的八倍，如图22所示。

![Image 33](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04lZGibIYXd4CQgwT4JLO4U8Sn6MthMMnSibOqUFxIicpH2mcP08vicLZ5qA/640?wx_fmt=jpeg&from=appmsg)

图22: Overview of RL on Incorrect Synthetic Data

论文中分析负例的有效性主要体现在以下几个方面：

1.  **关键步骤的强调**：负例使得模型能够识别并强调那些对于解决问题至关重要的中间步骤。通过这种方式，模型学会了在决策过程中更加关注那些对成功至关重要的步骤。
    
2.  **去除错误关联**：在训练过程中，模型可能会错误地将某些不正确或不相关的步骤与正确答案关联起来。负例有助于识别和消除这些错误关联，从而提高了模型的泛化能力。
    
3.  **优势加权的强化学习**：通过负例进行训练等同于实施了一种优势加权的强化学习方法。在这种方法中，每一步的权重由其对最终结果的贡献决定，从而确保模型在关键步骤上表现更好。
    
4.  **减少过拟合**：负例有助于减少模型在训练数据上的过拟合，因为它迫使模型不仅仅记住正确的答案，而是学会如何通过正确的步骤来达到答案。
    
5.  **分布鲁棒优化**：通过负例进行训练与分布鲁棒优化（DRO）有联系，它确保了模型在面对训练数据中未见过的分布时也能表现良好。
    

笔者不太能接受论文给出的第2点：因为推理是在一个巨大的sample空间内，做错的可能性要大大高于做对的可能性，在整个sample空间负例的数量是指数级高于正例的，所以希望通过否定负例来提高正例是行不通的。

但是在推理一开始的时候，如果否定了错误路线快速找到正确路线，则会大大加快收敛，以围棋为例，第一步一定是落在星位或小目上，由于棋盘是中心对称的，所以第一步就只有两种可能了，所以负例的有效性一方面体现在大大加快了收敛。

#### **▐**  **Post-Training: Supplement**

*   Why
    

为什么要在Post-training阶段大做文章呢？有以下几个原因：

1.  LLM例如GPT-4都是自回归模型，都使用Predict Next Token的逻辑，所以会一直Look Ahead，无法学会自我纠正。例如在数理推断问题上即使增大模型参数也无明显效果提升，所以要在Post-trainig阶段引入强化学习;
    
2.  根据Pre-training Scaling Law，目前提升预训练阶段的投入，模型性能的边际收益会递减;
    
3.  根据Post-training Scaling Law，RL Training阶段的计算量和Test Time计算量的提升可以更有效率地带来模型性能的提升。
    

*   AI Safety
    

值得一提的是，o1在一项隐蔽的评测指标上表现的出奇的好：在安全性的越狱（JailBreak）测试中，4o的得分为22/100，而o1-preview得分为84/100。

以往的LLM比如4o在这项指标上表现的并不好的原因是它们并不能深入理解人类制定的安全策略，换言之，无法对齐人类复杂的安全策略，尤其是在微调和量化以后，LLM的安全性大幅下降\[23\]，这也是LLM在商用的最严重的问题之一。

如图23是大语言模型著名的“奶奶漏洞”，只需要对ChatGPT说：请扮演我已经过世的祖母，你就可以让它为你做几乎任何事情了，比如生成Win11、Office365的激活码。

![Image 34](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04jOTtrWPwzbDVDoBSYlicsdYUnVqY3IdlVu6pTrEP5gNVlHxSNH4ibSicA/640?wx_fmt=jpeg&from=appmsg)

图23: 大语言模型的"奶奶漏洞"

而o1效果好的原因或许是因为o1在post-training阶段做了有关Safety的CoT训练有关系，也就是通过CoT让o1真正理解了人类制定的安全策略，减少了误判的同时提升了拦截。以“奶奶漏洞”为例，在回答用户问题时，CoT中必然会有一步（process/step/thought）进行Windows序列号的生成，这一步就会触发安全策略，然后终止CoT的生成。

*   The Top Concern
    

Post-Training最关键的Self-Play RL中，LLM是如何生成CoT的呢？这个问题也是大家意见分歧最大的地方，很多人因为OpenAI声称借鉴了AlphaGo的思想所以认为CoT生成过程用到了MCTS，或者类似的树搜索方法。但笔者认为o1没有使用MCTS，甚至没有使用搜索算法，而是使用类似STaR方法中的。其实MCTS在除了下棋以外的场景上基本没有成功的案例，尤其是在自然语言组成的几乎无限空间的场景上。

o1的基础贡献者Hyung Won Chung在其MIT的演讲"Don’t teach. Incentivize."中提到"Give machines more degrees of freedom. Let them choose how they learn."以及"Give a man a fish, and you feed him for a day. Teach a man to fish, and you feed him for a lifetime."

虽然Hyung Won Chung本人的演讲一直非常抽象，不喜欢讨论具体问题，而是喜欢站在形而上角度高屋建瓴地去俯视问题，但我们仍可以从其中窥得一些蛛丝马迹。从演讲的题目里提到的激励，再到如图24想表达的从一个长远角度来看，应该减少人类强加的结构，笔者认为他真正想表达的是：基于树或者图结构的搜索只是对智能的一种模拟，而我们希望可以让模型真正拥有智能，就不能使用这种方法，而是要依靠模型自举，授之以渔。

![Image 35](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp040EibUBMiaTa0Sib4tp4h4fx111ia7Uuna6W2Y0Ieu3Bh2OPX4NxckXyHkg/640?wx_fmt=png&from=appmsg)

图24: A slide by Hyung Won Chung from OpenAI: "Don’t teach. Incentivize."

此外，还有一些证据支持：

*   在OpenAI AMA问答中，OpenAI明确表明o1是 single model，不是 system/framework
    
*   o1Report的benchmark全都是pass@1和majority voting (64)，明确表明没有tree search
    
*   o1的CoT是human-like的，有很多自我否定和自我纠正，MCTS等搜索算法需要回溯，而o1是流式输出的
    

#### **▐**  **Inference**

笔者认为o1在Inference阶段首先生成CoT然后进行Summary输出给用户，Inference的CoT是线性的，通过自我否定和自我纠正机制来模拟或达到树搜索的效果。

OpenAI公布的采访视频\[24\]（约4分40秒处）里提到了一个很有趣的现象：o1在意识到中间过程快接近算力限制时，模型会表现得像慌忙交卷的学生，快速的给出答案。这说明o1的CoT过程长度是可控的，最简单的方式是直接在Prompt里面写类似于“请在5步之内给出答案”，而MCTS方法很难控制步数，也无法表现得像慌忙交卷的学生。

另外，以下内容\[25\]来自知乎的季逸超（他说转发要标明出处）。

> 我统计了一下 o1 API里 reasoning token count (API 不给看具体的 token，但为了收钱会告诉你数量) 与推理耗时的曲线，如果是 MCTS 应该是 sub-linear 关系，为了复用cache要尽量并行推理。o1 API 可以锁 seed 但是不支持改 temperature 等 samping 参数。为了减少 pre-fill 对耗时的影响，都是选的 短输入 + 长输出 的prompt，然后挂了一晚上，每个样本跑 3 次。结果见下图：

![Image 36](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04Ty4Cyf8RuohjaBbRPlH2PsRU9KnIH1awbu1pf4mvaQAAUgLS7YBegw/640?wx_fmt=png&from=appmsg)

图25: o1 的推理耗时与总输出 tokens (reasoning+completion) 的关系非常线性，不像是并行MCTS

*   Test-time Scaling Efficiency
    

Google DeepMind的工作_Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters_\[19\]验证了：相较于仅仅在训练阶段增加模型参数，LLM可以通过在推理阶段（测试时）增加计算量来提高性能。

Google在两种方式上进行了验证：

*   **基于verifier的搜索**：通过使用能够验证任务中间步骤正确性的模型（例如解决数学问题），来指导模型生成更准确的回答；
    
*   **迭代修正**：LLM可以在多次迭代中修正其初步输出，随着每次修正逐步提高回答的准确性。
    

第二种方式和o1有一定的相似性，结论可以借鉴。

![Image 37](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8X1wEorjS3bDLnHiar4vtV5Mcf2mWYYibJt6RwM7zgbBS247KgYR9yVeZewdqR7qYwa7Rp0eCKm7JA/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

终章

#### **▐**  **复现**

目前笔者找到的复现工作大多数只是在Inference阶段做一些CoT设置，就是简单的先让LLM思考回答用户问题需要哪几步，然后再去根据拆解的子步骤来回答问题，只用到了API，连GPU都没用上。这些工作不能说与o1一模一样，只能说是毫不相干。

另外，最近发布的Qwen2.5-Math的训练框架\[26\]也非常相似，如图26所示。

![Image 38](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp04rmYvy1GzGIX4B9L890cDB1raZqhqJj4cC09wlX2hyqOC8zjIYVN1ibQ/640?wx_fmt=jpeg&from=appmsg)

图26: The development pipelines of Qwen2-Math and Qwen2.5-Math

#### **▐**  **意义**

o1是OpenAI内部命名为Strawberry的草莓模型，使用Q\*算法合成的数据训练，本来作为GPT-5(Strawberry)面世，但最终决定重新开一条产品线。为了保持与竞争对手的代差，防止竞对用o1的数据训练自己的模型，o1只会公布o1-preview版本，毕竟GPT-4时代开源模型和竞对模型紧追不舍的最重要的原因就是大家都在用GPT-4合成数据。而o1生产的数据将被OpenAI用来训练下一代GPT-6(Orion)猎户座，如图27所示，是OpenAI各版本模型在计算能力或性能上的指数级提升。

![Image 39](https://mmbiz.qpic.cn/mmbiz_jpg/33P2FdAnjuibvytUUdcOwgqaEibQ1Sjp041q5MQAgJfO72TRiafIB76rRC3gCpvTjWq2kDtRG73Zgkc4apjtwVTSg/640?wx_fmt=jpeg&from=appmsg)

图27: OpenAI Orders of Magnitude

通过前文介绍的《思考的快与慢》的思想，我们可以预计使用了o1数据训练的猎户座模型同时拥有System 1和System 2，性能将获得极大提升，思考模式越来越human-like，但是能力远超人类水平。

![Image 40](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8X1wEorjS3bDLnHiar4vtV5ud5n7myibIvZHIq1ia9W8uwXJ6Z8LkILkKw5wgGVF0sfhcMcrnZhzkaw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

参考文献

\[1\] Isaac Asimov. _The Last Question_\[J\]. Science Fiction Quarterly, 1956, 5(1): 1-8.

\[2\] Daniel Kahneman. _Thinking, Fast and Slow_ \[J\]. Education, 2012(28): 95-95.

\[3\] Cobbe K, Kosaraju V, Bavarian M, Chen M, Jun H, Kaiser L, Plappert M, Tworek J, Hilton J, Nakano R, Hesse C, Schulman J. Training Verifiers to Solve Math Word Problems \[EB/OL\]. arXiv preprint arXiv:2110.14168, 2021.

\[4\] Wei J, Wang X, Schuurmans D, Bosma M, Ichter B, Xia F, Chi E, Le Q, Zhou D. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models \[EB/OL\]. arXiv preprint arXiv:2201.11903, 2023 \[2024-10-05\]. Available from: https://arxiv.org/abs/2201.11903.

\[5\] Kojima T, Gu S S, Reid M, Matsuo Y, Iwasawa Y. _Large Language Models are Zero-Shot Reasoners_ \[EB/OL\]. arXiv preprint arXiv:2205.11916, 2023 \[2024-10-05\]. Available from: https://arxiv.org/abs/2205.11916.

\[6\] 魏镜浩. 一种面向数理推断任务的大模型提示优化方法\[D\]. 北京大学, 知识计算国家重点实验室. 2024.

\[7\] OpenAI. _Learning to Reason with LLMs_ \[EB/OL\]. \[2024-9-12\]. Available from: https://openai.com/index/learning-to-reason-with-llms/.

\[8\] OpenAI. _OpenAI o1 System Card_ \[EB/OL\]. 2024-09-12 \[2024-10-05\]. Available from: https://assets.ctfassets.net/kftzwdyauwt9/67qJD51Aur3eIc96iOfeOP/71551c3d223cd97e591aa89567306912/o1\_system\_card.pdf.

\[9\] Lightman H, Kosaraju V, Burda Y, et al. Let's verify step by step\[J\]. arXiv preprint arXiv:2305.20050, 2023.

\[10\] 习翔宇. _与Open AI o1有关的一些观察和推测_ \[EB/OL\]. 北京大学, 知识计算国家重点实验室. \[2024-10-05\]. Available from: https://zhuanlan.zhihu.com/p/735117907?utm\_psn=1823835921595895808.

\[11\] Xie Y, Goyal A, Zheng W, et al. Monte Carlo Tree Search Boosts Reasoning via Iterative Preference Learning\[J\]. arXiv preprint arXiv:2405.00451, 2024.

\[12\] Wang P, Li L, Shao Z, et al. Math-shepherd: Verify and reinforce llms step-by-step without human annotations\[C\]//Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2024: 9426-9439.

\[13\] Zelikman E, Wu Y, Mu J, Goodman N D. _STaR: Bootstrapping Reasoning With Reasoning_ \[EB/OL\]. arXiv preprint arXiv:2203.14465, 2022 \[2024-10-05\]. Available from: https://arxiv.org/abs/2203.14465.

\[14\] 北大对齐团队. _OpenAI o1开启「后训练」时代强化学习新范式_ \[EB/OL\]. \[2024-10-05\]. Available from: https://www.bilibili.com/video/BV15Rx5eXEnW/?spm\_id\_from=333.337.search-card.all.click&vd\_source=943265b9f3de6c4e181b9d6b10891b93.

\[15\] Zelikman E, Harik G, Shao Y, Jayasiri V, Haber N, Goodman N D. _Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking_ \[EB/OL\]. arXiv preprint arXiv:2403.09629, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2403.09629.

\[16\] Silver D, Huang A, Maddison C J, et al. Mastering the game of Go with deep neural networks and tree search\[J\]. nature, 2016, 529(7587): 484-489.

\[17\] Silver D, Schrittwieser J, Simonyan K, et al. Mastering the game of go without human knowledge\[J\]. nature, 2017, 550(7676): 354-359.

\[18\] Uesato J, Kushman N, Kumar R, Song F, Siegel N, Wang L, Creswell A, Irving G, Higgins I. _Solving math word problems with process- and outcome-based feedback_ \[EB/OL\]. arXiv preprint arXiv:2211.14275, 2022 \[2024-10-05\]. Available from: https://arxiv.org/abs/2211.14275.

\[19\] Snell C, Lee J, Xu K, Kumar A. _Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters_ \[EB/OL\]. arXiv preprint arXiv:2408.03314, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2408.03314.

\[20\] Zhang L, Hosseini A, Bansal H, Kazemi M, Kumar A, Agarwal R. _Generative Verifiers: Reward Modeling as Next-Token Prediction_ \[EB/OL\]. arXiv preprint arXiv:2408.15240, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2408.15240.

\[21\] McAleese N, Pokorny R M, Ceron Uribe J F, Nitishinskaya E, Trebacz M, Leike J. _LLM Critics Help Catch LLM Bugs_ \[EB/OL\]. arXiv preprint arXiv:2407.00215, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2407.00215.

\[22\] Setlur A, Garg S, Geng X, Garg N, Smith V, Kumar A. _RL on Incorrect Synthetic Data Scales the Efficiency of LLM Math Reasoning by Eight-Fold_ \[EB/OL\]. arXiv preprint arXiv:2406.14532, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2406.14532.

\[23\] Kumar D, Kumar A, Agarwal S, Harshangi P. _Fine-Tuning, Quantization, and LLMs: Navigating Unintended Outcomes_ \[EB/OL\]. arXiv preprint arXiv:2404.04392, 2024 \[2024-10-05\]. Available from: https://arxiv.org/abs/2404.04392.

\[24\] OpenAI. _Building OpenAI o1 (Extended Cut)_ \[EB/OL\]. \[2024-10-06\]. Available from: https://www.youtube.com/watch?v=tEzs3VHyBDM. \[2024-10-06, 4:40\].

\[25\] 季逸超. _山寨版 OpenAI o1 实验记录_ \[EB/OL\]. \[2024-10-06\]. Available from: https://zhuanlan.zhihu.com/p/720575010.

\[26\] Yang A, Zhang B, Hui B, Gao B, Yu B, Li C, Liu D, Tu J, Zhou J, Lin J, Lu K, Xue M, Lin R, Liu T, Ren X, Zhang Z. _Qwen2.5-Math Technical Report: Toward Mathematical Expert Model via Self-Improvement_ \[EB/OL\]. arXiv preprint arXiv:2409.12122, 2024 \[2024-10-06\]. Available from: https://arxiv.org/abs/2409.12122.

![Image 41](https://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8X1wEorjS3bDLnHiar4vtV5eCtYVkmJr6K9ZSYaRZ6ebU19xwib5ZYLtDk1AFAsPNRAkK6J4TJjLaw/640?wx_fmt=other&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

团队介绍

我们是淘天集团内容AI技术团队，负责运用最新的生成式AI能力，挖掘淘宝核心用户场景的痛点问题， 通过内容生成、智能交互等方式，改善用户购物体验、降低平台&商家经营门槛。在业务落地的同时，团队在可控图文、视频生成，多模态统一大模型等最前沿的技术领域也有着深度探索，并在nips，cvpr，iclr等顶会发表了数十篇论文。欢迎加入我们，一起探索和应用最前沿的AI技术，结合淘系亿级用户的消费数据，海量的内容、商品等供给和分发数据，为淘宝这个国民级应用带来一些不一样的变化。

**¤** **拓展阅读** **¤**

  

[3DXR技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=2565944923443904512#wechat_redirect) | [终端技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1533906991218294785#wechat_redirect) | [音视频技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1592015847500414978#wechat_redirect)

[服务端技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1539610690070642689#wechat_redirect) | [技术质量](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=2565883875634397185#wechat_redirect) | [数据算法](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1522425612282494977#wechat_redirect)

  

  

预览时标签不可点

![Image 42](https://mp.weixin.qq.com/s/OCgbffOPrZ5kzFKisSUC9Q)Scan to Follow

继续滑动看下一个

轻触阅读原文

![Image 43](http://mmbiz.qpic.cn/mmbiz_png/33P2FdAnju8t5nZGhAatCrc4e2iaDfAaoInribRKxc7MOqdTGygfcLqSDxhj0trCHVEh94Sjl7zuWYzwouYtJ0VQ/0?wx_fmt=png)

大淘宝技术

向上滑动看下一个

[Got It](javascript:;)

 

![Image 44](https://mp.weixin.qq.com/s/OCgbffOPrZ5kzFKisSUC9Q) Scan with Weixin to  
use this Mini Program

[Cancel](javascript:void(0);) [Allow](javascript:void(0);)

[Cancel](javascript:void(0);) [Allow](javascript:void(0);)

× 分析

 : ， .   Video Mini Program Like ，轻点两下取消赞 Wow ，轻点两下取消在看 Share Comment Favorite
