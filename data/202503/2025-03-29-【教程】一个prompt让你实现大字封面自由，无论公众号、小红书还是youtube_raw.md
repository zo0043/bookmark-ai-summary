Title: 【教程】一个Prompt让你实现大字封面自由，无论公众号、小红书还是Youtube

URL Source: https://mp.weixin.qq.com/s/GtI2LZ0ltlTiVX4Ty7n9AQ

Markdown Content:
> 字数 1200，阅读大约需 6 分钟

做自媒体的朋友都知道。

**封面太重要了。**

![Image 1: Image](https://mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCU8iadQArArGI4k5rWOo6K3QB4QlaNlA13PMrHho6bGaWCyhzCA2Eic2Q97g4DcrY4UI58IdtxrkqiaQ/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

有些社交媒体平台，因内容展现形态原因，封面尤其重要，比如说小红书等。

从逻辑上讲，即便不为流量，平台为给读者好体验，也希望封面精美、漂亮。

我也常为设计封面发愁。

**针对此痛点，今天调了个牛逼Prompt。**

基于内容，AI 提炼 8个金句，并为每个金句生成5张风格不同的大字封面。

这样就有40个封面选，直接让你实现封面自由！

设计封面有多难？
--------

**说难也不难，说简单也不简单。**

懂点设计工具的，比如用PS或Figma，按平台要求的封面比例，自己排版设计。

不懂设计的，可以用Canva、稿定设计等在线设计网站，用别人的模版修改。

**为什么说难呢？**

真能设计一个既能吸睛，又有美感的封面，没点专业知识真的不行。

如视觉层次对比，色彩与情感，排版与空间，每条都是经验和学问。

像我们这种普通人，真弄不好。

跟AI讨论，它告诉我的一些知识  

![Image 2: Image](https://mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCU8iadQArArGI4k5rWOo6K3QsOfGK6MJY5ueFI79VNEo2avCAMDbAjV1l7VghsVZKlrg6pJfobJ1Tw/640?wx_fmt=png&from=appmsg)

为什么要做大字封面？
----------

干脆直接，吸睛，简单，能发挥大模型优势。

![Image 3: Image](https://mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCU8iadQArArGI4k5rWOo6K3QxSvIzxPGzej2IFa21xat1Jhwiawt1qfjK4ULTJESUlD3b8BzGF5xKkw/640?wx_fmt=png&from=appmsg)

看小红书上的封面画风，下面是本钓鱼佬的发现页：

![Image 4: Image](https://mmbiz.qpic.cn/mmbiz_jpg/jibL99tg2bCU8iadQArArGI4k5rWOo6K3Qo0eLcY517ImCcoUBeb4Dp2hEkgNhDdSSrS6aWjxSY1iaLzXCyQwEFjQ/640?wx_fmt=jpeg&from=appmsg)

虽然没数据支撑，但最拼封面设计地方，多数人的选择，应该不会错。

为什么不用稿定设计和Canva
---------------

一方面花钱，另一方面排版还是需要人工。

我们应该懒到极致，应用 AI First 原则：

> 一切工作，都优先让AI试试，看它能不能稿定。

![Image 5: Image](https://mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCU8iadQArArGI4k5rWOo6K3Q7SicvfkV4DWHLOXj5ayaicXAHdcEVIKlL4h5yDplDSYicmCDQEibRzdkNA/640?wx_fmt=png&from=appmsg)

AI果然没让我失望。
----------

居然全搞定了。

写了一段Prompt，发给Claude 3.7 sonnet，立即生成一个包含40张封面的网页。

我估计Deepseek V3也行，效果接近。

把生成的HTML后粘贴到

> https://www.32kw.com/

![Image 6: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

生成网址：

> https://www.32kw.com/view/cf156a3

查看选喜欢的封面，截图使用即可。

**效果演示**

![Image 7: Image](https://mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCU8iadQArArGI4k5rWOo6K3QPJHl0gJeOj8QeEsNB70gNyLeuJ0cQcSdymzEK4mwicVYOpKeTiaMAKug/640?wx_fmt=png&from=appmsg)

  

### Prompt 如下

```
你是一名专业的内容策展人和视觉设计师，擅长从复杂文本中提炼精华并创建视觉冲击力强的知识卡片。任务：从我提供的内容中，提取8个最有价值的金句，并为每个金句设计5种不同风格的知识卡片（每个金句有5个不同设计版本），适合社交媒体、自媒体平台和在线学习内容。第一步：内容分析与提炼- 识别最有价值、最具洞见的8个金句- 每个金句应代表核心思想，表达简练有力，具有启发性第二步：知识卡片设计- 为每个金句创建5个不同风格的设计版本：   - 2个宽屏版本（比例2.35:1），应并排放置  - 3个方形版本（比例1:1），应放在宽屏版本下方- 每个卡片最大高度为383px- 每个金句的5个版本应使用不同的设计风格，包括：   - 不同的色彩方案  - 不同的排版方式  - 不同的装饰元素  - 不同的视觉风格（极简、手绘、数字界面等）输出要求：- 提供一个完整HTML文件，包含所有卡片（8个金句 × 5个版本 = 40个卡片）- 使用HTML5、Tailwind CSS、Font Awesome和必要的JavaScript- 卡片应按金句分组展示，每组包含该金句的5个不同设计版本- 代码应优雅且符合最佳实践，CSS应体现对细节的极致追求- 避免出现超出卡片范围的元素，便于复制和印刷设计风格参考：- 色彩与背景：从明亮活泼的色彩到柔和的色调，包括纯色背景、渐变效果、纸张质感、网格纹理等- 字体与排版：黑体为主，辅以手写风格、描边效果和变形字体，灵活的排版方式- 装饰与互动元素：图标、手绘元素、标签与徽章、互动提示等- 多元化风格：极简主义、手绘风格、纸质模拟、数字界面风、涂鸦标记等请确保每个金句的5个版本设计风格各不相同，同时保持整体视觉一致性。待处理内容：{{你的内容}}
```

生成知识卡片的Prompt
-------------

前天还写了另一个Prompt，虽不适合做封面，但适合生成知识卡片传播。

![Image 8: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)
