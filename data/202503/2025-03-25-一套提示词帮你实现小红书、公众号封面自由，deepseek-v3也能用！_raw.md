Title: 一套提示词帮你实现小红书、公众号封面自由，Deepseek V3也能用！

URL Source: https://mp.weixin.qq.com/s/OFCgFrXNQgIT2ho3V-4Oag

Markdown Content:
我前段时间写完网页生成的提示词之后一直想用类似的思路解决我发内容最大的一个难题：小红书&公众号的封面问题。

刚好上周六晚上看到了向阳桥木的文字分享卡片，就想着得干了。

本来以为很快就能搞定的，藏师傅吭哧瘪肚搞了两天才搞定这套 **帮你一键生成小红书&公众号封面的提示词，而且还是模块化设计**。

![Image 1: Image](https://mmbiz.qpic.cn/mmbiz_png/fbRX0iaT8EgexIlTX7NLzsYdaDGBqAwCLLYKs1rNSOr2JA2iceWEvjR6MaXo35WyNEZSx1vLQzKaiaiaalxIfOce9A/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

而且昨晚 Deepseek V3 0324 发布之后我发现这玩意的前端能力强的可怕。

所以就试了一下，发现 **V3 0324 也可以实现跟 Claude 3.7 差不多的效果**，这下更爽了，下面的风格示例部分我有放 V3 的效果。

另外微信公众号提示词生成的风格会一次性生成矩形和正方形的封面，你只需要一次上传就行，然后在公众号后台裁切选择合适的部分。

![Image 2: Image](https://mmbiz.qpic.cn/mmbiz_png/fbRX0iaT8EgexIlTX7NLzsYdaDGBqAwCLjYAY2P4icibrGqK74ey3Capq53KDEagFia0mcVDibJytIdNBHaVZghibKeg/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

提示词解析
-----

为了帮助大家理解我还画了两张图，这套提示词由四个部分组成：

*   角色设定（绿色）：主要设定 AI 的角色和主要任务；
    
*   基本要求（黄色）：这部分基本是约束画面比例和跟风格无关的排版的，我找了很多优质封面图总结了他们的共性放在了这里。
    
*   风格要求（紫色）：这部分是整套提示词的精华部分，两套提示词这部分是共享的，也就是说你探索出来的风格提示词两个封面都可以用，而且后面比如我们有了youtube 视频封面这种的时候，风格提示词依然可以共用。
    
*   用户输入内容（红色）：这部分就是你需要输入的内容，可以不按字数输入，AI 会帮你优化到合适的字数，如果有背景图和素材图也可以把链接放在这里，AI 会帮你放到封面里面。
    

![Image 3: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

**两套提示词除了风格的部分在这里：**

```
# 公众号封面提示词
```

```
# 小红书封面生成提示词
```

如何探索你喜欢的风格
----------

最后都是风格提示词的部分了，你只需要将这些风格提示词插入到上面的专业要求后面就可以了。

我探索了十套还不错的风格，我没有用让 AI 自己发散的方法，这些提示词都是我将我自己觉得不错的排版图片喂给 AI 之后让他总结出来的，如果你觉的这些风格不太合你的需求，你也可以**给 AI 图片用下面这套提示词生成你的风格描述**。

```
风格生成提示词：总结这几个小红书封面的风格，为他起一个名字，而且分设计风格、文字排版风格、视觉元素风格分开描述。
```

如果你觉得你探索的风格和结果不错也可以填写一下这个表单分享给大家：**https://go1coya2a7.feishu.cn/share/base/form/shrcn8PiYwUHyqh37XZKo0uutFF  
**

也可以在这里查看其他人填写的风格提示词：**https://go1coya2a7.feishu.cn/base/DY4wbU9U6a1rESsO2B2cfMfvnme?from=from\_copylink  
**

**这次的提示词真是很难搞，老说产品化方案，这下真是产品化方案了各位，要是产品化赚钱了别忘了藏师傅。**

最后贴一下最近朋友们的提示词玩法，有需求的可以看看：

歸藏：[](https://mp.weixin.qq.com/s?__biz=MzU0MDk3NTUxMA==&mid=2247487756&idx=1&sn=7855c80ee6e4dae521081745de90e95d&scene=21#wechat_redirect "为了让大家一键生成更漂亮的可视化网页，我写了个工具！")[为了让大家一键生成更漂亮的可视化网页，我写了个工具！](https://mp.weixin.qq.com/s?__biz=MzU0MDk3NTUxMA==&mid=2247487756&idx=1&sn=7855c80ee6e4dae521081745de90e95d&scene=21#wechat_redirect)

向阳乔木：[](https://mp.weixin.qq.com/s?__biz=MzAwODIyOTQ4Mw==&mid=2649442418&idx=1&sn=136b9127aa26b6a40a5e27efac226dbd&scene=21#wechat_redirect "一个提示词生成29种排版风格，秒杀80%人水平，附在线免费用网址")[一个提示词生成29种排版风格，秒杀80%人水平，附在线免费用网址](https://mp.weixin.qq.com/s?__biz=MzAwODIyOTQ4Mw==&mid=2649442418&idx=1&sn=136b9127aa26b6a40a5e27efac226dbd&scene=21#wechat_redirect)

汉青：[](https://mp.weixin.qq.com/s?__biz=Mzg5NTg0MzYxNw==&mid=2247484699&idx=1&sn=ee632befac2cd5dbf68267a8808f549f&scene=21#wechat_redirect "信息的AI可视化（1）：AI生成动态PPT的步骤分享")[信息的AI可视化（1）：AI生成动态PPT的步骤分享](https://mp.weixin.qq.com/s?__biz=Mzg5NTg0MzYxNw==&mid=2247484699&idx=1&sn=ee632befac2cd5dbf68267a8808f549f&scene=21#wechat_redirect)

orange.ai：[教程：](https://mp.weixin.qq.com/s?__biz=MzkwMzY5NzU2Nw==&mid=2247485689&idx=1&sn=76de6031dec364e34885b26327877a71&scene=21#wechat_redirect)[](https://mp.weixin.qq.com/s?__biz=MzkwMzY5NzU2Nw==&mid=2247485689&idx=1&sn=76de6031dec364e34885b26327877a71&scene=21#wechat_redirect "用 Figma 和 AI ，解锁文字卡片自由")[用 Figma 和 AI ，解锁文字卡片自由](https://mp.weixin.qq.com/s?__biz=MzkwMzY5NzU2Nw==&mid=2247485689&idx=1&sn=76de6031dec364e34885b26327877a71&scene=21#wechat_redirect)

**今天的教程就到这里了，后面全是风格的展示，如果觉得对你有帮助的话麻烦给个赞👍或者喜欢🩷**

十套精选风格提示词
---------

![Image 4: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 5: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 柔和科技卡片风
```

![Image 6: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 7: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 现代商务资讯卡片风
```

![Image 8: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 9: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 流动科技蓝风格
```

![Image 10: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 11: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 极简格栅主义封面风格
```

![Image 12: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 13: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 数字极简票券风
```

![Image 14: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 15: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 新构成主义教学风
```

![Image 16: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 17: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 奢华自然意境风
```

![Image 18: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 19: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 新潮工业反叛风
```

![Image 20: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 21: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 软萌知识卡片风
```

![Image 22: Image](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)![Image 23: Deepseeek V3 生成](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

Deepseek V3 生成

![Image 24: Claude 3.7 生成](blob:http://localhost/37d80127b73f829661c0d17b431e0b18)

```
# 商务简约信息卡片风
```

**如果觉得对你有帮助的话麻烦给个赞👍或者喜欢🩷，或者转发给需要的朋友们**
