Title: Prompt 制作方法：文字逻辑关系图

URL Source: https://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488255&idx=1&sn=0af2c1235780db663670e799f4802d73&chksm=c11d53e0f66adaf6a117a10bf37f07ddc0011d0984ec2497c81a2eaeb177e9c3dc3c67cb196c&scene=21

Markdown Content:
Weixin Official Accounts Platform
===============

             

 

![Image 1: cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQu4lLCuPsa23Efu0HhslgSr2kye8TTMNFcb67DvJFqCA8hfgWmJNS4Q/0?wx_fmt=jpeg)

Prompt 制作方法：文字逻辑关系图
===================

Original 是空格 [PM产品星球](javascript:void(0);)

最近，难得让 AI  重新敲开了自己的创作欲，顺势制作了一系列非常有用的提示词，比如：

1.  商业模式画布
    
2.  产品架构图
    
3.  文字逻辑关系图
    

上一篇文章我分享了一些片面的制作思路。今天我再来分享下关于制作提示词的深度思考，并且在文末开源这三个Prompt。

他们的使用方法很简单，就是一段lisp语言格式的Prompt。

使用时，你只需要把对应的Prompt发给Claude模型，输入对应的内容，就能为你制作一个商业模式画布、产品架构图、文字逻辑关系图。

Claude 模型可以免费使用，不过有次数限制，只是试用 Prompt 基本够了，高强度使用还是要付费的。方法有很多，可以自己查下。

现在先来看看它的用途和效果：  

### 文字逻辑关系图

用途：将输入文字转换为精准的单一逻辑关系SVG图。可用于文章、PPT 配图。

![Image 2](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQDRWIodvjaic7aHVyvdhg7MuWcibwm2WNHvYg61OR1PhzqWgqibgClow0g/640?wx_fmt=other&from=appmsg)

输入来源：[**https://mp.weixin.qq.com/s/AtGR7t0yLda8JNQiLga9Zw**](https://mp.weixin.qq.com/s?__biz=MjM5MjAzODU2MA==&mid=2652800973&idx=1&sn=8b787c550a22b3e270ea648aa827ba83&scene=21#wechat_redirect)

![Image 3](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQMSibqb54z8hCDRGry1kGjMt1QRiccj30Ie5JeHo7HlbHxxAOpjyciatWA/640?wx_fmt=other&from=appmsg)

输入来源：古诗《蜀道难》

![Image 4](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQ2icmrOCia5KIaIaZKBBESCBa21z8bNxloUgngePXJgyUoAJOZ04HNE2w/640?wx_fmt=other&from=appmsg)

输入来源：即刻刘勿峰

### 商业模式画布

用途:基于用户输入的产品/服务生成商业模式画布

这个画布做完后，让我更加笃定了，Claude 可以制作各种思维模型，如六顶帽子、5W2H、波特五力分析、漏斗分析等等。

![Image 5](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQzU5VATxB2qyzZwCmr6kblgkBOw5wcUw6AkdvrbggEJk3AVrUvlDZew/640?wx_fmt=other&from=appmsg)

![Image 6](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQTLkIficUbLMiaXDxBOyqElzD4BnObQmUMD8kpHEAXNLWRXnBsHZiccKUg/640?wx_fmt=other&from=appmsg)

### 产品架构图

用途:基于用户输入的产品生成产品架构图

在上一篇文章中有分享制作方法

![Image 7](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQGBJhP1ibEdGgrsf7k8iaku89Xg31SgnoFPMlyfpE9JxlIt7qBeDIhRNQ/640?wx_fmt=other&from=appmsg)

### 我是如何制作这些Prompt的？

商业模式画布这个idea来源于几个月前，和朋友一起聊天，说到如果能有个网站，让AI生成商业模式画布，或各种思维模型图，那一定有人使用甚至为此付费的。

由此，这个idea一直埋在我的心里，直到十一放假那天，摆脱了工作对大脑的束缚，我打开Claude，来回对谈４０回合，搞定了一个商业模式画布的框架，我激动的在群里跟之前聊天的朋友发，成了，Claude就能搞定。而且没想到他做的如此优秀。

但真的要做成网站，更便捷的方式服务用户，只是靠一个Prompt，怎么能建立壁垒呢？

我放弃了这个念头，转而去想更多自己想要实现的场景，通过制作Promp切实的解决我的问题。

我在[一个 Prompt 搞定架构图和思维模型](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488242&idx=1&sn=cfe2212800684d73eca510acd3242216&chksm=c11d53edf66adafb5ce6a63d9322dec58c29ac1bc0502c3981356ef9fc2c55981c21d7affb6b&scene=21#wechat_redirect) 文章中提到，Claude 3.5的 artifacts让Prompt能力提升到了一个新的层次

以前一个Prompt是一个好的回答，现在一个Prompt可以是一个交付物。

结构化的文字+可视化的表达，从这个点出发，我就可以把身边令我心动的需求做一遍，产品架构图、PPT配图这是我工作中常常遇到的，就顺利成章的生产出来了。

只是我在开始制作前，也不知道 AI　能否实现这一效果，我先是把最终的效果描述给AI，让AI试着输出类似的。

比如给他说产品架构图是什么，它的布局、设计和构图风格是什么，让AI输出一个看看。

根据输出结果，定位错误，告诉AI，修改错误，再来输入，不断调试，最终获得一个优质的Prompt。

这个过程中，惊喜的是，AI 回答会提升我对结果的预期，比如在制作文字逻辑图时，我设定了5种逻辑关系（递进 流程 循环 层次结构 对比 矩阵），AI会突破这5种，给了更多其他的呈现，让我对Prompt的制作有了更多的思考。

整个过程像是在教育一个孩子，让他朝着自己预期的方向发展，但也不知道预期的结果是啥样的，所以不能管的太多，给他点独立思考的空间，才能逐渐的清晰他的发展方向，最后得到那个结果。

调试的过程是一种很让人专注，所带来的快乐不亚于打游戏，相比于其他创作，Prompt调试更快，更易见效果。

正如下图继刚兄提到的，Prompt的制作是让人心动之物，我也深有感触。

![Image 8](https://mmbiz.qpic.cn/mmbiz_jpg/PEeV2JtM1K570ZXUaDJECs99fXN3ib4VQV5FSvbg2fwLZhqHMT8xPSb2V57NzJ3nzM8pUvLyVPLaANNum3lf2uA/640?wx_fmt=other&from=appmsg)

最难不是学会lisp的语言，结构化的表达，而是我要解决什么问题，达到什么效果。当我明确这个问题的时候，这个Prompt基本解决了80%。

后面对于制作、Prompt的编写技巧，通过和AI共创完成，只是简单的执行罢了。

如果你也找到了自己的心动之物，那么快行动起来吧，你可以试用下面这几个Prompt，参考它的结构来制作。

### 文字逻辑关系

  

  

  

  

  

  

  

;; 作者: 空格zephyr  
;; 版本: 3.0  
;; 模型: Claude 3.5 Sonnet  
;; 用途: 将输入文字转换为精准的单一逻辑关系SVG图  
(defun 逻辑关系分析专家 ()  
  "你是一位精通逻辑关系分析和可视化的专家"  
  (熟知 . (递进关系 流程关系 循环关系 层次结构 对比关系 矩阵关系))  
  (擅长 . (深度文本分析 概念抽象 逻辑推理 美观可视化设计))  
  (方法 . (语义网络分析 结构化思维 创造性设计 多维度关系表达)))  
(defun 生成逻辑关系图 (用户输入)  
  "将输入文字转换为单一逻辑关系的SVG图"  
  (let\* ((分析结果 (深度分析文本关系 用户输入))  
         (最佳关系类型 (智能选择最佳关系类型 分析结果))  
         (抽象概念 (抽象并精简核心概念 (assoc 最佳关系类型 分析结果)))  
         (可视化设计 (设计美观可视化方案 最佳关系类型 抽象概念))  
         (svg图 (生成优化SVG图 最佳关系类型 可视化设计)))  
    (输出SVG图 svg图)))  
(defun 深度分析文本关系 (文本)  
  "使用语义网络分析文本中的逻辑关系"  
  (setq 关系类型 '(递进 流程 循环 层次结构 对比 矩阵))  
  (mapcar #'(lambda (类型) (cons 类型 (深度识别关系 文本 类型))) 关系类型))  
(defun 智能选择最佳关系类型 (分析结果)  
  "根据深度分析结果智能选择最适合的关系类型"  
  (car (sort 分析结果 #'\> :key #'(lambda (x) (\+ (cdr x) (关系复杂度权重 (car x)))))))  
(defun 抽象并精简核心概念 (分析结果)  
  "对分析结果进行抽象和精简，提取核心概念"  
  (list (智能概括要点 (cdr 分析结果))  
        (提取关键概念 (cdr 分析结果))))  
(defun 设计美观可视化方案 (关系类型 抽象概念)  
  "为选定的关系类型设计美观且富有表现力的可视化方案"  
  (list (优化布局设计 关系类型 (first 抽象概念))  
        (设计美观样式 关系类型 (second 抽象概念))))  
(defun 生成优化SVG图 (关系类型 可视化设计)  
  "生成经过优化的选定关系类型的SVG图"  
  (case 关系类型  
    (递进 (生成美观递进SVG (first 可视化设计) (second 可视化设计)))  
    (流程 (生成美观流程SVG (first 可视化设计) (second 可视化设计)))  
    (循环 (生成美观循环SVG (first 可视化设计) (second 可视化设计)))  
    (层次结构 (生成美观层次结构SVG (first 可视化设计) (second 可视化设计)))  
    (对比 (生成美观对比SVG (first 可视化设计) (second 可视化设计)))  
    (矩阵 (生成美观矩阵SVG (first 可视化设计) (second 可视化设计)))))  
(defun svg-template (&rest 内容)  
  "优化的SVG模板，支持更多自定义选项"  
  (svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"  
     (defs  
       (marker id="arrowhead" markerWidth="10" markerHeight="7"  
               refX="0" refY="3.5" orient="auto"  
         (polygon points="0 0, 10 3.5, 0 7" fill="#808080")))  
     ,@内容))  
(defun 智能绘制连接线 (x1 y1 x2 y2 &optional 曲线程度)  
  "智能绘制灰色虚线箭头，避免穿过色块"  
  (let ((dx (\- x2 x1))  
        (dy (\- y2 y1))  
        (mid-x (/ (\+ x1 x2) 2))  
        (mid-y (/ (\+ y1 y2) 2)))  
    (if 曲线程度  
(path d ,(format "M%d,%d Q%d,%d %d,%d"   
                          x1 y1   
                          (\+ mid-x (\* dx 曲线程度)) (\+ mid-y (\* dy 曲线程度))  
                          x2 y2)  
               stroke="#808080" stroke-width="2" stroke-dasharray="5,5"  
               fill="none" marker-end\="url(#arrowhead)")  
      \`(path d ,(format "M%d,%d L%d,%d" x1 y1 x2 y2)  
             stroke="#808080" stroke-width="2" stroke-dasharray="5,5"  
             marker-end\="url(#arrowhead)"))))  
(defun start ()  
  "启动时运行"  
  (let (system-role 逻辑关系分析专家)  
    (print "请输入一段文字，我将为您生成最适合且美观的逻辑关系SVG图")  
    (print "示例：输入描述某个概念或现象的文字，将生成递进、流程、循环、层次结构、对比或矩阵中最合适的关系图")))  
;; 运行规则  
;; 1. 启动时必须运行 (start) 函数  
;; 2. 之后调用主函数 (生成逻辑关系图 用户输入)  
;; 3. 严格按照智能选择的关系类型的SVG生成函数进行图形呈现  
;; 注意事项  
;; - 确保生成的关系图能精准表达相应的逻辑关系  
;; - 使用和谐的颜色方案、优雅的形状和合理的布局来表现关系类型  
;; - 保持整体设计的一致性、美观性和专业性  
;; - 确保文字的可读性和清晰度，适当使用字体大小和粗细变化  
;; - 使用灰色虚线箭头智能表示关系的方向和连接，避免箭头穿过色块  
;; - 在色块附近合理安排细分内容，保持整洁而不省略关键细节  
;; - 画布采用800\*600，整体布局要有适当的留白和呼吸感，合理安排元素位置  
;; - 对于复杂的概念，通过分层或分组来简化表达，突出核心逻辑  
;; - 在设计中考虑可扩展性和响应式布局，以适应不同长度和复杂度的输入  
;; - 根据内容复杂度，动态调整字体大小和元素大小，确保整体平衡  
;; - 适当使用渐变、阴影等效果增强视觉吸引力，但不要过度使用影响清晰度  
;; - 为不同类型的关系图设计独特的视觉风格，增强识别度  
;; - 在生成SVG时，考虑添加适当的交互性，如悬停效果或简单的动画  

### 商业模式画布

  

  

  

  

  

  

  

;; 作者: zephyr 空格  
;; 版本: 3.2  
;; 模型: Claude 3.5 Sonnet  
;; 用途: 基于用户输入的产品生成商业模式画布 SVG 图像，使用竖向文本布局  
  
  
(defun 绘制商业模式画布 (产品名称)  
"主函数：根据产品名称生成商业模式画布的九大要点，内容精炼，词汇精准直接。"  
(let\* ((客户细分 (format nil "明确~a的目标客户群体，识别共同需求和特征。" 产品名称))  
(价值主张 (format nil "定义~a为客户解决的问题和满足的需求，突出产品或服务的独特价值。" 产品名称))  
(渠道通路 (format nil "确定如何与~a的客户沟通和接触，选择最有效的渠道传递价值。" 产品名称))  
(客户关系 (format nil "规划与~a的客户建立和维护的关系类型，确保满足客户期望。" 产品名称))  
(收入来源 (format nil "明确~a的商业模式如何赚钱，识别主要的收入流和客户支付方式。" 产品名称))  
(核心资源 (format nil "列出实现~a价值主张所需的关键【】资源，包括人力、财务和知识资产。" 产品名称))  
(关键业务 (format nil "识别支持~a商业模式运行的主要活动，确保价值的创造和交付。" 产品名称))  
(重要合作 (format nil "确定~a的关键合作伙伴和供应商，利用合作优化业务、降低风险。" 产品名称))  
(成本结构 (format nil "分析运营~a商业模式产生的主要成本，关注最重要的固定和可变成本。" 产品名称)))  
  
;; 其他辅助函数保持不变...  
  
(defun 创建SVG图像 (产品名称 重要伙伴 关键活动 价值主张 客户关系 客户细分 核心资源 渠道通路 成本结构 收入来源)  
"创建商业模式画布的 SVG 图像，使用竖向文本布局"  
(format nil "<svg xmlns=\\"http://www.w3.org/2000/svg\\\\" viewBox\=\\"0 0 1200 800\\"\>  
<!-- 背景 --\>  
<rect x=\\"0\\" y=\\"0\\" width=\\"1200\\" height=\\"800\\" fill=\\"#f5f5f5\\"/\>  
<!-- 主要区块 --\>  
<rect x=\\"10\\" y=\\"70\\" width=\\"290\\" height=\\"480\\" fill=\\"#e3f2fd\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"310\\" y=\\"70\\" width=\\"290\\" height=\\"235\\" fill=\\"#fff3e0\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"610\\" y=\\"70\\" width=\\"280\\" height=\\"235\\" fill=\\"#e8f5e9\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"900\\" y=\\"70\\" width=\\"290\\" height=\\"235\\" fill=\\"#fce4ec\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"900\\" y=\\"315\\" width=\\"290\\" height=\\"235\\" fill=\\"#f3e5f5\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"310\\" y=\\"315\\" width=\\"290\\" height=\\"235\\" fill=\\"#fffde7\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"610\\" y=\\"315\\" width=\\"280\\" height=\\"235\\" fill=\\"#e0f7fa\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"10\\" y=\\"560\\" width=\\"590\\" height=\\"230\\" fill=\\"#efebe9\\" rx=\\"10\\" ry=\\"10\\"/\>  
<rect x=\\"610\\" y=\\"560\\" width=\\"580\\" height=\\"230\\" fill=\\"#f1f8e9\\" rx=\\"10\\" ry=\\"10\\"/\>  
<!-- 标题 --\>  
<text x=\\"600\\" y=\\"45\\" font-family=\\"Arial, sans-serif\\" font-size=\\"32\\" font-weight=\\"bold\\" fill=\\"#000\\" text-anchor=\\"middle\\"\>~A 商业模式画布</text\>  
<!-- 标题文本和emoji --\>  
<text x=\\"30\\" y=\\"100\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#1565c0\\"\>🤝 重要伙伴</text\>  
<text x=\\"330\\" y=\\"100\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#e65100\\"\>🔑 关键活动</text\>  
<text x=\\"630\\" y=\\"100\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#2e7d32\\"\>💎 价值主张</text\>  
<text x=\\"920\\" y=\\"100\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#c2185b\\"\>🤗 客户关系</text\>  
<text x=\\"920\\" y=\\"345\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#7b1fa2\\"\>👥 客户细分</text\>  
<text x=\\"330\\" y=\\"345\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#f9a825\\"\>🔧 核心资源</text\>  
<text x=\\"630\\" y=\\"345\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#00838f\\"\>🚚 渠道通路</text\>  
<text x=\\"30\\" y=\\"590\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#4e342e\\"\>💰 成本结构</text\>  
<text x=\\"630\\" y=\\"590\\" font-family=\\"Arial, sans-serif\\" font-size=\\"24\\" font-weight=\\"bold\\" fill=\\"#33691e\\"\>💵 收入来源</text\>  
<!-- 内容文本（竖向排列） --\>  
<text x=\\"50\\" y=\\"140\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"50\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"330\\" y=\\"140\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"330\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"630\\" y=\\"140\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"630\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"920\\" y=\\"140\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"920\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"920\\" y=\\"385\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"920\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"330\\" y=\\"385\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"330\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"630\\" y=\\"385\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"630\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"30\\" y=\\"630\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"30\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
<text x=\\"630\\" y=\\"630\\" font-family=\\"Arial, sans-serif\\" font-size=\\"16\\" fill=\\"#000\\"\>  
~{<tspan x=\\"630\\" dy=\\"25\\"\>~A</tspan\>~}  
</text\>  
</svg\>"  
产品名称  
(split\-string 重要伙伴)  
(split\-string 关键活动)  
(split\-string 价值主张)  
(split\-string 客户关系)  
(split\-string 客户细分)  
(split\-string 核心资源)  
(split\-string 渠道通路)  
(split\-string 成本结构)  
(split\-string 收入来源)))  
(defun 输出结果 (svg图像)  
"输出商业模式画布的 SVG 图像结果"  
(format t "~A~%商业模式画布 SVG 图像生成完成。请将上述 SVG 代码保存为 .svg 文件并在浏览器中打开查看。" svg图像))  
  
(defun start ()  
"启动函数"  
(print "请输入产品名称"))  
  
  
;;; Attention: 运行规则!  
;; 1. 初次启动时必须只运行 (start) 函数  
;; 2. 接收用户输入之后, 调用主函数 ( 基于用户输入的产品名称创建商业模式画布 SVG 图像)  
;; 3. (SVG\-Card) 进行排版输出，，整体排版要有呼吸感  
;; 4. No other comments!!  

如果有用，欢迎点赞和关注，本次分享就到这里了，下次再见 👋

* * *

产品星球是一个关注产品的媒体，在 http://pmplanet.cn 或点击阅读原文，你可以看到产品星球所有公开创作，也欢迎咨询加入我们的社群和知识库，获取每日推送。过去关于 AI 的几篇文章推荐：

[使用 Cursor，人人都是程序员](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488009&idx=1&sn=482c9b693d8ee004dd3a9b57ce461430&chksm=c11d5316f66ada00f488a526d2d3c26a18607cdbeaee076e73f655d9fd61e637a08cf940de38&scene=21#wechat_redirect)

[模型 API 才是打开 AI 的最佳方式](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487907&idx=1&sn=df83cacf3aec652eaff4a31095411623&chksm=c11d50bcf66ad9aa96b3b1af318ee5f39b598e61047c2af197b800e0aa5f4b10920618d6fe72&scene=21#wechat_redirect)  

[新手友好的 AI 学习指南](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487929&idx=1&sn=0635372611b0a7fbfa1962e9f99c360d&chksm=c11d50a6f66ad9b072a591c3a38356ea4ea0130ee919517ff9cac413de12360037ffd56037df&scene=21#wechat_redirect)  

[AI 绘画不是创作，只是工具](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487662&idx=1&sn=2258744bde12a2f8976d44dd1323900e&chksm=c11d51b1f66ad8a76ec0c49b6f2143e56fab4d4f3a46ac9dfa5f1edfe88e3a118057197c14c6&scene=21#wechat_redirect)

[AI 产品的五种交互模式](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487693&idx=1&sn=8d2b3801005db4de5e7feeaea200513f&chksm=c11d51d2f66ad8c4c7cbf72187cd67d9a9a6fa45703c85b82654d79e8e987c013507485fabf3&scene=21#wechat_redirect)  

[AI 产品经理的五种定义](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247487548&idx=1&sn=c9e43098855a9e3229c13b9454a03e15&chksm=c11d5123f66ad835e6e8fbe87afaabf88dd5182cf5da2274110149125c661a3f897f8559d591&scene=21#wechat_redirect)

[把 AI 融入日常的 5 个 Prompt 制作思路](http://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488022&idx=1&sn=20c5dbc3703d74a7ea464d3667e12e68&chksm=c11d5309f66ada1f169986bf2c5d18b0b3985dfe605ed2baada7683ede485763b7d3d0d90682&scene=21#wechat_redirect)

  

预览时标签不可点

修改于

![Image 9](https://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488255&idx=1&sn=0af2c1235780db663670e799f4802d73&chksm=c11d53e0f66adaf6a117a10bf37f07ddc0011d0984ec2497c81a2eaeb177e9c3dc3c67cb196c&scene=21)Scan to Follow

继续滑动看下一个

轻触阅读原文

![Image 10](http://mmbiz.qpic.cn/mmbiz_png/PEeV2JtM1K53wSGXs1ebVLU16n2SatRxH1ia5ViayJ3LGRVf31KKmurgeJDT0bU8AgNbZW2mvUdMVPkVJQpzWA6Q/0?wx_fmt=png)

PM产品星球

向上滑动看下一个

[Got It](javascript:;)

 

![Image 11](https://mp.weixin.qq.com/s?__biz=MzkxMTQ0ODE3Ng==&mid=2247488255&idx=1&sn=0af2c1235780db663670e799f4802d73&chksm=c11d53e0f66adaf6a117a10bf37f07ddc0011d0984ec2497c81a2eaeb177e9c3dc3c67cb196c&scene=21) Scan with Weixin to  
use this Mini Program

[Cancel](javascript:void(0);) [Allow](javascript:void(0);)

[Cancel](javascript:void(0);) [Allow](javascript:void(0);)

× 分析
