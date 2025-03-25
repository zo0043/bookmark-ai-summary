Title: 信息的AI可视化（1）：AI生成动态PPT的步骤分享

URL Source: https://mp.weixin.qq.com/s?__biz=Mzg5NTg0MzYxNw==&mid=2247484699&idx=1&sn=ee632befac2cd5dbf68267a8808f549f&scene=21

Markdown Content:
![Image 1: Image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/CoshmfW6Ul9OMJWv6YFkAXaTHZtEiblPkzHJyzF8sFwHXrVe6zBNmAfNJJa8QK9joibE7E55Z0v4U1se6KlPr0OA/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

PPT对大部分朋友的的价值不言而喻。我在日常做商业咨询时也需要大量PPT做交付，所以从年初开始，我尝试让AI来完成商业PPT的生成和设计。目前效果大致如下：

![Image 2: Image](https://mmbiz.qpic.cn/sz_mmbiz_png/CoshmfW6Ul9OMJWv6YFkAXaTHZtEiblPkGNiaAUmMCB3Rg8Ks3apCO2KKdKsytPZKrwAwGvmtlGMbuCeib3D19XGQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![Image 3: Image](https://mmbiz.qpic.cn/sz_mmbiz_png/CoshmfW6Ul9OMJWv6YFkAXaTHZtEiblPkFo0CeibJiaU6WcywN8C3NSYx1o1G59ANojVtO0pGXibriczfWIX05K0FOA/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![Image 4: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 5: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 6: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 7: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

视觉效果是有点超出我的预期的。而且从可读性、图形化、信息整理几个角度来说，这些结果已经完全够用了。同时这些生成的PPT可以是动态的：

在完成调教后，生成PPT的流程如下：给AI一段文字描述，包含任意数据，观点，或者你想表达的主题，它可以直接生成带动态的PPT。好处不言而喻：

1.  节省制作时间
    
2.  优秀的视觉风格
    
3.  快速归纳整理信息
    
4.  用图形代替文字枯燥的表达
    

比如：给AI一段数据，直接可视化展示PPT

![Image 8: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 9: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

比如：让它描述信息媒介的进化史

让我惊艳的是这个例子，根据一句话就清晰地描述出了媒介的进化历程，并且配好了ICON（建议放大看一下）！

![Image 10: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 11: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

再比如：让它直接总结文章全文

你甚至可以直接复制一篇文章给它，帮你自动把核心数据进行可视化：

![Image 12: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 13: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

接下来我来分享一下实现这种效果的思路和步骤，在开始前，先延续我泼冷水的传统：

请别指望有一段提示词，复制就能得到满意的结果。这是一个和AI互动的过程，而非取之即用的“交付”。即便套用相同提示词，在死板的流程下也未必有好结果，AI目前还达不到科幻小说的级别，请各位理解。

所以请保持耐心，在找到最佳状态前，你需要反复尝试。在下分享的是思路，而不是123的任务清单。

同时，使用AI生成“PPT”，实际上是基于模型的HTML输出能力，而并非真的PPT格式，它目前无法实现在PPT里的二次深度编辑，这一点我在最后会展开来说说看法。

模型选择

目前只推荐Claude3.7 Sonnet，您当然可以使用Deepseek等模型进行尝试，但效果会打折扣很多（实际上是非常多）。原因是Anthropic对Claude在编程和美学方面的深度优化目前在市面上是最好的，尤其是3.7。

使用Claude的方法很多，最直接的是使用官方web，但即便是pro用户，token也经常遇到限制，因为上下文对话的每次修改消耗都是很大的，所以我目前通过POE来调用Claude，还有很多其他方式，可自行搜索。

![Image 14: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

接下来就进入和AI的交互流程，大致有4个阶段：

![Image 15: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

阶段1 主观描述

这个阶段的目标是通过文字聊天，让Claude领悟你大致想要的视觉风格。比如在我的例子中，我希望他模仿类似TheVerge网站的科技风格，那么我先简单和他描述我的需求。

注意，很多朋友会希望AI理解最简单的描述，比如“我要TheVerge网站的科技风格的PPT”，这种做法大概率会失败，和AI的沟通我不建议偷懒，尽量具体一点，比如这样的描述：

帮我生成数据可视化PPT

*   类似theverge这样的科技风格，强烈的颜色对比
    
*   深色底色，以明亮的绿色和紫色作为高亮颜色，符合数学规律的配色
    
*   带有淡淡的网格线，体现科技感
    
*   使用16:9的画布，不能有元素溢出画布，保证布局的合理性
    
*   简洁的几何图形化作为装饰，所有装饰需要和内容相关，并且尽可能少使用
    
*   使用英文
    

模拟2个PPT的版式或者数据可视化，来测试效果（这里也可以换成一个明确的任务，不重要，因为我们的目标是得到一个模板）

![Image 16: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

如何描述取决于你想要的风格，你也可以使用截图+grok/gemini/deepseek等方式帮你总结网站和参考物的美学特征，但不要太长。并且务必告诉Claude画布的比例是16:9，或者你希望的PPT尺寸。

但是一般情况下，单次沟通后你得不到完美的效果。比如我看到的PPT在视觉风格上有一定的相似性，但颜色的精确性，和字体的风格方面差距很大，还有一些细节完全不到位：

![Image 17: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

这个时候你需要的是：耐心。

很多人认为和AI的交互应该是简单几句话就能搞定的，这才是AI的价值，然后发现效果不好，就下个结论“AI还是不行”。我觉得这种想法多少陷入了一些误区。

AI能实现技术杠杆的前提是要在前期投入一定的精力和他“沟通”，这有点类似于你管理一个员工，无论他多么优秀，如果你不和他沟通清楚想要什么，都会导致结果的失控。

追求AI的杠杆，不代表你可以懒惰。

因此，和Claude反复聊天来获得一个你满意的PPT样式是完全必要的，在前期付出较高的沟通成本后，量产时就会觉得很爽。在沟通的过程中，我们要尽量清晰简洁的描述你想要的具体要求，然后让他“模拟2个PPT模板”来观察效果。以下是我的一些沟通示例，它非常类似你在和一个员工布置任务：

![Image 18: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 19: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 20: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

一般来说，在5次对话内我们可以得到一个理想模版。

注意，在主观描述阶段，我们的目标是得到模板，所以不要纠结于细节。

比如局部没有对齐，局部文字的大小，这些可以在后续调整。否则你的上下文token消耗会非常大。如果超过5次效果依然差很远，建议清除上下文或者从头开启一轮新对话。

大概在3-4次对话后，Claude给我的模板基本接近了我的需求。此时就可以继续下一个阶段了。

![Image 21: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

阶段2 抽象风格样式（可选）

这是一个可选择的阶段，有两条路可以往下走：

1\. 和Claude说：非常好，记住这个风格，后面都使用它，然后直接进入第三阶段。

2\. 让Claude把这个模版抽象成一种它能理解风格

第一种选择的好处是快，如果就是想临时出几页PPT，接着说要求就可以了。但AI的上下文特征决定了在生成一定数量的PPT之后，它会改变对风格的认知，很难一直保证精确性，同时在单次对话下多次生成对token的消耗是极大的。

所以开启新对话在大部分情况下几乎是必然，那么我们就需要一个方式让它在新对话中尽量准确的还原刚才的风格。这也是我建议采用方式2的原因。

让AI总结当前的美学风格，并且记下来。这等于是你和他努力沟通后的提示词资产，是你付出努力后的成果。它通常会总结成一段文字，你也可以让它同时生成一个CSS样式同时保存。

非常棒，记录下来这个风格，后面全部使用它

![Image 22: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

中英文都可以，道理是一样的：

Visual Style Documentation for Future Presentations  
Color Palette

Primary Neon Green: #73FBB4  
Primary Purple: #AB6BFF  
Secondary Purple: #BF55EC  
Dark Background: #0a0a14  
Accent Color: White

Layout & Structure

16:9 aspect ratio  
Dark background with subtle grid pattern (40px × 40px)  
Title positioned at top-left (5% from edges)  
Subtitle in neon green below title  
Content organized in layered structure with 3D perspective  
Geometric decorative elements with subtle glow effects

Typography

Sans-serif font family (Segoe UI, Roboto, Oxygen, Ubuntu)  
Clean title without text effects (2.5vw size)  
Subtle glow effects only on supporting text elements  
Layer numbers: bold, large (3vw) with slight transparency  
Layer titles: medium (1.8vw) with light shadow  
Descriptions: smaller (1vw) with slight transparency

Visual Elements

Grid background pattern in very light teal (rgba(64, 224, 208, 0.05))  
Geometric shapes with thin borders in purple  
Flow lines with gradient transparency  
Soft glow effects in key areas (not on main title)  
Custom icons with both solid and outline elements  
Slight 3D rotation (5deg on X-axis)  
Hover effects that enhance the 3D perspective

Animation/Interaction (if implemented)

Subtle hover effects moving elements forward in 3D space  
Potential for sequential appearance of layers in presentations

Special Effects

Drop shadows for depth  
Subtle glow on icons and accent elements  
Transform-style: preserve-3d for true 3D rendering  
Light translucency in gradients for depth

This comprehensive visual style creates a modern, tech-forward presentation with mathematics-inspired precision and futuristic neon aesthetics that will provide a consistent and professional appearance across all future presentations.

生成后大致看一下，可以做一些微调，然后粘贴在一个记事本里就行，方便以后再用。

阶段3 量产复用

这个阶段就比较简单了，用任意的方法告诉AI你想要什么就可以。最直接的就是文字描述，可以是一句话，一个概念，一组数据，原则还是：尽可能简洁清晰的表达你要的东西。

比如我想要一个演讲的标题页：

![Image 23: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 24: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

用文字告诉它你想修饰的细节，比如：

让1.1这个数字通过字体的变化显得很大，同时，中文的 letter-spacing为10px，增加整体的间距，突出呼吸感

![Image 25: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

当你需要一组样式一致的页面时，最好一次性生成所有页面，因为在间隔几个其他任务后，再去生成标题页样式可能略有不同，建议一次搞定：

![Image 26: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 27: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

数据可视化的页面，你可以用文字粘贴一大段要表现的数据，或者直接粘贴文章，这两种方式都是在文章一开始我展示过的。

理论上，附件形式的表格也手机可以支持的，同时Claude已经支持了网页搜索，但读取文章链接应该也是可以的，我没有自己试，道理上是类似的，你可以选择输入信息的方式。

![Image 28: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 29: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

堆积图、柱状图，任意图形他都能搞定：

![Image 30: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 31: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

表示逻辑的层级示意图：

![Image 32: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 33: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

阶段4 唤醒

最后是怎么让AI“想起来”你需要的风格。

因为上下文长度和token成本的问题，我们不可能在一个对话中让Claude无限生成。这就造成困扰：上次的效果很好，但聊太久或新开一个对话后，那些风格它就忘了。

老实说目前没有很完美的方案，我自己采用几种方式来唤醒Claude对视觉的记忆，再做微调，基本可用，就是麻烦一点。

1\. 用前文总结的美学风格唤醒

![Image 34: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

2\. 用之前生成的PPT截图或者HTML文件唤醒

![Image 35: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

![Image 36: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

这几种方式可以混用，目的都是用各种方式还原回之前的理想状态。但切记不要太纠结细节，只要在大风格上和之前保持一致就行了。AI生成PPT的逻辑并不是严格遵循某种规范，而是按照一个人机互动的脉络去持续衍生，如果追求100%的严格复用，不如直接手动去搞了。

如何把HTML变成PPT

目前没有办法直接导出PPT的格式，因为本质上它是用HTML在模拟PPT的格式而已。我一般的处理方式是截图后粘贴到PPT，但无法实现在PPT里的二次深度编辑。

![Image 37: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

其实AI的信息可视化的目标并不是制作PPT，而是快速生成具有类似PPT展示效果的信息可视化资产，你把比例变成3:4，就可以发小红书，变成9:16，就可以发抖音。你甚至完全可以用HTML的页面组来完成整个演讲。

AI带来的是信息可视化的可能性，不是生成PPT的可能性。长远来说，PPT只是做演示的工具，但做演示不一定只能依靠PPT。

以上工作流的优缺点

优点：

1.  将冗长信息数据的快速视觉化
    
2.  量产标准化页面
    
3.  优秀的视觉效果（需调试）
    
4.  数据信息图表的快速补充
    

缺点：

1.  HTML无法进入原生PPT工作流
    
2.  局部调整时可能非常浪费时间
    
3.  成本不低（按Claude的token计算）
    
4.  缺乏样式稳定性
    

推荐阅读

几个朋友近期都写过关于信息可视化的文章，我们每个人的观察和覆盖角度并不相同，推荐也阅读一下他们的内容，能获得不同的信息和视角。

橘子orange.ai - 关于用Figma 和 AI 解锁卡片自由的教程

[教程：用 Figma 和 AI ，解锁文字卡片自由](https://mp.weixin.qq.com/s?__biz=MzkwMzY5NzU2Nw==&mid=2247485689&idx=1&sn=76de6031dec364e34885b26327877a71&scene=21#wechat_redirect)

歸藏 - 一键生成可视化网页工具

[为了让大家一键生成更漂亮的可视化网页，我写了个工具！](https://mp.weixin.qq.com/s?__biz=MzU0MDk3NTUxMA==&mid=2247487756&idx=1&sn=7855c80ee6e4dae521081745de90e95d&scene=21#wechat_redirect)

向阳 - 生成网站、PPT等内容的提示词
--------------------

[【教程】必须收藏的 4 段 Prompt 提示词，生成PPT、生成3D动画，生成网站，生成万物...](https://mp.weixin.qq.com/s?__biz=MzAwODIyOTQ4Mw==&mid=2649442252&idx=1&sn=869b13365a62ab0451c094b379a8b40a&scene=21#wechat_redirect)
--------------------------------------------------------------------------------------------------------------------------------

![Image 38: 图片](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

我是汗青，AI.TALK创始人，一个6岁开始学美术的AI创作者，也是厮混互联网圈16年的产品经理。我在这里分享对AI技术与媒介的思考。

我的愿景是寻找新技术与媒介艺术的结合方式。如果你同样对这个话题感兴趣，欢迎关注我的公众号和视频作品。

*   商务合作：aitalkgina
    
*   频道视频号：AI.TALK
    
*   个人视频号：汗青HQ
