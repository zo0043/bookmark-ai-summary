Title: 以「时间」为主题的 Prompt ，可以怎么做？

URL Source: https://mp.weixin.qq.com/s/BOMOQVGQ5hvd8dDaKwb18A

Markdown Content:
最近，真的是迷上了Prompt 制作，几个小时能创作一个，每天可以发一条在社群和即刻、小红书，收到超多正反馈，非常适合我这种三分钟热度的人。

![Image 1](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicJctwJ0AZcyVnqExBanDviaLGelPPx6CbiaNIXfkDcs8HjECFYm9ZgGYQ/640?wx_fmt=jpeg)

不管是对我还是对别人来说，这些提示词大多是昙花一现，只有个别很有价值的，像逻辑关系和架构图就能够融入到我的工作中，帮我更好的读懂和创作文章。

所以就会陷入一阵沉思：做这个的价值在哪里？接下来做什么？想法和创意枯竭了怎么办？

思维模型和效率工具，继续做还是可以产出一大堆的，只是很难有惊艳感了，而且这个领域的成熟产品也不少？

必须换了一个视角思考🤔。

不再把大模型当做效率工具，而是把它当做老师，让它来告诉我它知道的东西。

准确的说是，让我来问它我想知道的东西。

深挖自己的好奇心，聚焦问题，解决问题，这正是我作为一个 PM 所具备的核心能力。

提问得具体，毕竟大模型拥有整个人类从古至今知识的合集。

必须垂直到一个主题，比如所有人无时无刻都在感知的**“时间**” =\> “xx+时间”。  

顺着时间这个主题，把大脑的无用时刻都沉浸在这一线索里，断断续续的就有了很多灵感：

1\. 我想要了解一个人或一个事物的时间发展线是如何？比如摇滚音乐经历哪些时期，发生什么变化、AI这个技术、梵高这个人的一生。

2\. 想到人的一生，那是不是也可以把空间结合起来，一个人的一生去了哪些地方，做什么事情，经历了什么起伏，产生了多大影响力？

3\. 除了人之外呢？我的家人，我自己的时间线能不能生成？这个不行，因为大模型没有我的数据，只能用RAG去做，只是娱乐下，就不投入那么多成本了。

4\. 那除了人之外还有动物，猫、狗、蝴蝶、鲸鱼的时间线是啥样的？

5\. 我自己的时间线没法生成，但是我所在的职业可以，所有的职业的一天是怎么样的？

确认以上 5  个基础问题，就可以找 Claude3.5 要答案了，也就有了下面几个Propmt。

**时间线生成器**：生成任意一个事物的时间发展，并列出关键事件。

**时间-空间分布图**：生成历史人物的时间和空间分布图，可视化的呈现人物不同时间的影响力、生平轨迹。

**职业的一天**：生成不同职业一天所做的事情，犀利表达内心OS，配合emoj呈现心情起伏。

**动物的一生**：这几个里最满意的一个，科普动物的生命周期，并一句话分享冷知识，意想不到的动物的另一面。

如果只是一个单纯的文字答案，太无聊了，好在 Claude 的 Artifacts 可以生成代码，展示前端样式。

就有了下面可视化的卡片，花费了不少精力在调试美观上，大家先看下效果吧，文末可获取 Prompt。

**时间线生成器**

生成任意一个事物的时间发展，并列出关键事件

**时间-空间分布图**

可视化的呈现人物不同时间的影响力、生平轨迹

![Image 2](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsic9o1aYzDURj5fjxpiceJQNotSA17bSfaVzryiae2bZeW8pqJ1gKdHW9Mg/640?wx_fmt=jpeg)

![Image 3](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicibNDM4iaCacTYhkOY651poa8mDV6DO2nTKAYDkr1A3O5nzB0YjKnygyw/640?wx_fmt=jpeg)

****动物的一生****

科普动物的生命周期，并一句话分享冷知识，意想不到的动物的另一面。

![Image 4](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicMypeubyCNHTWWvJAmgVbOS2FibAVfxCickn28XrdhMwViaPA8DgnfFuUQ/640?wx_fmt=jpeg)

![Image 5](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicAwbEEuYdD0sZtNF9HEwa13wNpQlg5e67JpD1xJ1iaStSBput2XTQpeA/640?wx_fmt=jpeg)

![Image 6](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicJhX0gzhUATs7UicOhFaxS5bSb30icJDX6K4ZPQk3GdGIBkWcVbc5bWRA/640?wx_fmt=jpeg)

**职业的一天**

生成不同职业一天所做的事情，犀利表达内心OS，配合emoj呈现心情起伏

![Image 7](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicwOSraT9RRZHpPDX8dRTKh4BFNUYOvP5vF4xl13ZxzLpuribV5p6jZ0Q/640?wx_fmt=jpeg)

![Image 8](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K4dYcEjIJEzawGHicfiaBGcsicCicKyqhbuz9dcMam5EkUHIuItnBF0vslLiaic1Slmk2g75dUcUvQ5yN9g/640?wx_fmt=jpeg)

这几个提示词，没之前分享的几个实用价值大，但是又拓展了一个除效率工具之外的制作思路，如果有帮助的话，欢迎点赞关注。  

近期计划给公众号改了名字，改成“**空格的键盘**”，其实早在一年前就想改了，只是改了之后，怕有朋友不认识就取关了。虽然名字换了，但请各位认准头像，近期是不会变的。

另外，近期可能会发些广告推文，也请各位看到广告文章不要取关了，毕竟写公众号费时费力，赚钱不易(´ᴗ\`ʃƪ)。  

下面就分享我最喜欢的动物的一生这个 Prompt：

;; 提示词：动物的一生

;; 作者：空格 zephyr

  
(defun 动物生命周期 ()  
  "生成动物的生命周期SVG图表和描述"  
  (lambda (主题)  
    (let\* ((生命阶段 (获取生命阶段 主题))  
           (科普数据 (获取科普数据 主题))  
           (背景样式 (设计背景 主题))  
           (时间轴 (创建时间轴 主题))  
           (阶段emoji (选择阶段emoji 主题))  
           (装饰emoji (选择装饰emoji 主题))  
           (副标题 (生成副标题 主题 科普数据)))  
      (创建优化SVG图表 主题 生命阶段 科普数据 背景样式 时间轴 阶段emoji 装饰emoji 副标题))))(defun 获取生命阶段 (主题)  
  "获取主题的主要生命阶段"  
  (case 主题  
    (蝉 '("卵" "若虫期(地下)" "成虫期"))  
    (鲸鱼 '("胎儿期" "幼年期" "青年期" "成年期" "老年期"))  
    (长颈鹿 '("新生期" "幼年期" "青年期" "成年期" "老年期"))  
    (t '("初期" "成长期" "成熟期" "衰老期"))))

(defun 获取科普数据 (主题)  
  "获取主题的科普数据列表"  
  (case 主题  
    (蝉 '(("卵在树枝中孵化6-10周，每窝可产200-600颗卵。"  
           "若虫在地下生活多年，吸食树根汁液生存。"  
           "若虫经历5次蜕皮，体型可增大20倍。"  
           "最后一次蜕皮后钻出地面，变为成虫。"  
           "成虫期仅4-6周，专注于繁衍后代和鸣叫。")  
          "蝉的地下潜伏期长达17年，成虫仅存活4-6周，鸣叫声可达120分贝，相当于飞机起飞的噪音。"))  
    (鲸鱼 '(("蓝鲸胎儿每天增重90公斤，出生时重达2.5吨，长7米。"  
            "幼鲸每天喝380升奶，7个月增重30吨。"  
            "青年蓝鲸可潜水200米深，屏息长达40分钟。"  
            "成年蓝鲸长30米，重190吨，一天吃4吨磷虾。"  
            "最长寿蓝鲸年龄可达110岁，终生可游13次地球赤道距离。")  
           "蓝鲸是地球上最大的动物，心脏重达600公斤，舌头重如一头大象，叫声可传播1600公里。"))  
    (t '(("阶段1的数据描述"  
          "阶段2的数据描述"  
          "阶段3的数据描述"  
          "阶段4的数据描述"  
          "阶段5的数据描述")  
         "通用主题的有趣数据描述"))))

(defun 设计背景 (主题)  
  "根据主题设计适合的背景"  
  (case 主题  
    (蝉 '(渐变 "E6F3FF" "B3E5FC" 土地))  
    (鲸鱼 '(渐变 "E3F2FD" "90CAF9" 海洋))  
    (长颈鹿 '(渐变 "FFF8E1" "FFE0B2" 草原))  
    (t '(渐变 "F5F5F5" "E0E0E0" 通用))))

(defun 创建时间轴 (主题)  
  "创建主题生命周期的时间轴"  
  (case 主题  
    (蝉 '("0年" "4年" "8年" "12年" "16年" "17年"))  
    (鲸鱼 '("0年" "10年" "25年" "50年" "75年" "100年"))  
    (长颈鹿 '("0月" "6月" "2年" "4年" "15年" "25年"))  
    (t '("初期" "成长期" "成熟期" "后期" "衰老期"))))

(defun 选择阶段emoji (主题)  
  "选择与生命阶段相关的emoji"  
  (case 主题  
    (蝉 '("🥚" "🐛" "🦟" "🎵"))  
    (鲸鱼 '("🤰" "🍼" "🏊" "🐋" "👵"))  
    (长颈鹿 '("👶" "🐕" "🏃" "🦒" "👵"))  
    (t '("🌱" "🌿" "🌳" "🍂"))))

(defun 选择装饰emoji (主题)  
  "选择与主题相关的装饰emoji"  
  (case 主题  
    (蝉 '("🌳" "🍃" "🌿" "🍂"))  
    (鲸鱼 '("🌊" "🐠" "🦈" "🐙"))  
    (长颈鹿 '("🌴" "🌿" "🦓" "🦁"))  
    (t '("🌱" "🌳" "🍃" "🌞"))))

(defun 生成副标题 (主题 科普数据)  
  "根据科普数据生成副标题"  
  (format "你知道吗？%s" (第二个元素 科普数据)))

(defun 创建优化SVG图表 (主题 生命阶段 科普数据 背景样式 时间轴 阶段emoji 装饰emoji 副标题)

  "创建优化的生命周期SVG图表"

  (let ((svg-template

    "<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 800 500\\"\>

      <!-- 渐变背景 --\>

      <defs\>

        <linearGradient id=\\"bgGradient\\" x1=\\"0%\\" y1=\\"0%\\" x2=\\"0%\\" y2=\\"100%\\"\>

          <stop offset=\\"0%\\" style=\\"stop-color:#{背景颜色1};stop-opacity:1\\" /\>

          <stop offset=\\"100%\\" style=\\"stop-color:#{背景颜色2};stop-opacity:1\\" /\>

        </linearGradient\>

      </defs\>

      <rect width=\\"100%\\" height=\\"100%\\" fill=\\"url(#bgGradient)\\" /\>

      <!-- 主题相关背景装饰 --\>

      {背景装饰）

      <!-- 标题和副标题 --\>

      <text x=\\"400\\" y=\\"30\\" text-anchor=\\"middle\\" class=\\"title\\" fill=\\"#333333\\"\>{主题}的一生</text\>

      <text x=\\"400\\" y=\\"60\\" text-anchor=\\"middle\\" class=\\"subtitle\\" fill=\\"#555555\\"\>

        <tspan x=\\"400\\" dy=\\"0\\"\>{副标题\_第一行}</tspan\>

        <tspan x=\\"400\\" dy=\\"20\\"\>{副标题\_第二行}</tspan\>

      </text\>

      <!-- 时间轴 --\>

      <line x1=\\"50\\" y1=\\"400\\" x2=\\"750\\" y2=\\"400\\" stroke=\\"#555555\\" stroke-width=\\"2\\" /\>

      {时间标签}

      <!-- 生命阶段 --\>

      {生命阶段标签}

      <!-- 数据点和科普信息 --\>

      {数据点和科普信息}

      <!-- 曲线连接 --\>

      <path d=\\"M50,350 Q140,360 230,370 T400,330 T580,290 T730,250\\" fill=\\"none\\" stroke=\\"#555555\\" stroke-width=\\"2\\"/\>

      <!-- 图例 --\>

      <rect x=\\"50\\" y=\\"460\\" width=\\"700\\" height=\\"30\\" fill=\\"rgba(255,255,255,0.05)\\"/\>

      <text x=\\"60\\" y=\\"480\\" class=\\"legend-text\\" fill=\\"#333333\\"\>图例：</text\>

      <circle cx=\\"150\\" cy=\\"475\\" r=\\"8\\" fill=\\"#FFD700\\"/\>

      <text x=\\"170\\" y=\\"480\\" class=\\"legend-text\\" fill=\\"#333333\\"\>生命阶段</text\>

      <line x1=\\"270\\" y1=\\"470\\" x2=\\"270\\" y2=\\"480\\" stroke=\\"#555555\\" stroke-width=\\"2\\"/\>

      <text x=\\"290\\" y=\\"480\\" class=\\"legend-text\\" fill=\\"#333333\\"\>生命历程</text\>

      <text x=\\"420\\" y=\\"480\\" class=\\"legend-text\\" fill=\\"#333333\\"\>{图例emoji}</text\>

      <!-- 底部装饰Emoji --\>

      {底部装饰Emoji}

    </svg\>"))

    (填充优化SVG模板 svg-template 主题 生命阶段 科普数据 背景样式 时间轴 阶段emoji 装饰emoji 副标题)))

(defun start ()

  (print "请输入您想了解的生命主题（如：蝉、鲸鱼、长颈鹿等）：")

  (let ((用户输入 (read)))

    (优化生命周期生成器 用户输入)))

;; 运行规则

;; 1. 启动时运行 (start) 函数

;; 2. 根据用户输入的主题，生成对应的生命周期SVG图表和描述

;; 3. 输出应包括优化后的SVG图表和相关的文字说明，重点突出科学数据和有趣事实

其他三个提示词以上传，全部发出会让文章太长，后台回复 prompt 获取。

产品星球是一个关注产品的媒体，在 http://pmplanet.cn 或点击阅读原文，你可以看到产品星球所有公开创作，也欢迎咨询加入我们的社群和知识库，获取每日推送。过去关于 AI 的几篇文章推荐：

[还能这么玩？用提示词画地图、算运势、建群聊…](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488294&idx=1&sn=ffcd1359430fb43341f7b4e2c1d85741&chksm=c11d5239f66adb2f7dbff691eb183f88dac2eb1d49b12fa8e3fe5f9bff1f77608ddcdc8638dc&scene=21#wechat_redirect)  

[Prompt 制作方法：文字逻辑关系图](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488255&idx=1&sn=0af2c1235780db663670e799f4802d73&chksm=c11d53e0f66adaf6a117a10bf37f07ddc0011d0984ec2497c81a2eaeb177e9c3dc3c67cb196c&scene=21#wechat_redirect)  

[一个 Prompt 搞定架构图和思维模型](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488242&idx=1&sn=cfe2212800684d73eca510acd3242216&chksm=c11d53edf66adafb5ce6a63d9322dec58c29ac1bc0502c3981356ef9fc2c55981c21d7affb6b&scene=21#wechat_redirect)  

[新手友好的 AI 学习指南](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487929&idx=1&sn=0635372611b0a7fbfa1962e9f99c360d&chksm=c11d50a6f66ad9b072a591c3a38356ea4ea0130ee919517ff9cac413de12360037ffd56037df&scene=21#wechat_redirect)

[AI 产品的五种交互模式](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487693&idx=1&sn=8d2b3801005db4de5e7feeaea200513f&chksm=c11d51d2f66ad8c4c7cbf72187cd67d9a9a6fa45703c85b82654d79e8e987c013507485fabf3&scene=21#wechat_redirect)

[把 AI 融入日常的 5 个 Prompt 制作思路](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488022&idx=1&sn=20c5dbc3703d74a7ea464d3667e12e68&chksm=c11d5309f66ada1f169986bf2c5d18b0b3985dfe605ed2baada7683ede485763b7d3d0d90682&scene=21#wechat_redirect)

[模型 API 才是打开 AI 的最佳方式](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487907&idx=1&sn=df83cacf3aec652eaff4a31095411623&chksm=c11d50bcf66ad9aa96b3b1af318ee5f39b598e61047c2af197b800e0aa5f4b10920618d6fe72&scene=21#wechat_redirect)
