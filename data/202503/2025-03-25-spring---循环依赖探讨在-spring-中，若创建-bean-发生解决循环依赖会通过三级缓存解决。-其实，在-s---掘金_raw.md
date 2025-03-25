Title: Spring---循环依赖探讨在 Spring 中，若创建 Bean 发生解决循环依赖会通过三级缓存解决。 其实，在 S

URL Source: https://juejin.cn/post/7483329722496581658

Markdown Content:
Spring---循环依赖探讨在 Spring 中，若创建 Bean 发生解决循环依赖会通过三级缓存解决。 其实，在 S - 掘金
===============
     

 [![Image 6: 稀土掘金](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/e08da34488b114bd4c665ba2fa520a31.svg) ![Image 7: 稀土掘金](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/6c61ae65d1c41ae8221a670fa32d05aa.svg)](https://juejin.cn/)

*   首页
    
    *   [首页](https://juejin.cn/)
    *   [AI Coding NEW](https://juejin.cn/aicoding)
    *   [沸点](https://juejin.cn/pins)
    *   [课程](https://juejin.cn/course)
    *   [直播](https://juejin.cn/live)
    *   [活动](https://juejin.cn/events/all)
    *   [AI刷题](https://juejin.cn/problemset)
    
    [APP](https://juejin.cn/app?utm_source=jj_nav)
    
    [插件](https://juejin.cn/extension?utm_source=jj_nav)
    

*   *   搜索历史 清空
        
    *   创作者中心
        
        *   写文章
            
        *   发沸点
            
        *   写笔记
            
        *   写代码
            
        *   草稿箱
            
        
        创作灵感 查看更多
        
*   ![Image 8: vip](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ffd3e238ee7f46eab42bf88af17f5528~tplv-k3u1fbpfcp-image.image#?w=25&h=26&s=5968&e=svg&a=1&b=dacbbc)
    
    会员
    
*   登录
    
    注册
    
    首次登录 / 注册免费领取
    -------------
    
    登录 / 注册
    

![Image 9](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/close.7ba0700.png)

   

 

  

Spring---循环依赖探讨
===============

[后端程序员Aska](https://juejin.cn/user/4389699570630893/posts)

2025-03-19 3,498 阅读1分钟

专栏： 

走进springboot细节

关注

![Image 10](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/banner.a5c9f88.jpg)

✅Spring 循环依赖细节
--------------

在 Spring 中，若创建 Bean 发生解决循环依赖会通过三级缓存解决。

1.  `singletonObjects`（一级缓存）：存放 **完整** 的 Bean 对象；
2.  `earlysingletonObjects`（二级缓存）：存放 Bean 的 **早期**（early）对象；
3.  `singletonFactories`（三级缓存）：存放 Bean 的 **工厂**（Factory）对象；

![Image 11: image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/22a9f18d745f4aa689a45e0ed16f0b5d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv56iL5bqP5ZGYQXNrYQ==:q75.awebp?rk3s=f64ab15b&x-expires=1742955888&x-signature=DGQ3TowRCEZguz25uMBG9Rv3DYE%3D)

✅Spring 循环依赖导致启动报错
------------------

我们应用的 pay 这个模块，在启动时候会报错。报错信息提示如下：

![Image 12](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/817715c8fc0e491894e6a56327cb4ea7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv56iL5bqP5ZGYQXNrYQ==:q75.awebp?rk3s=f64ab15b&x-expires=1742955888&x-signature=65cs%2BSvaG66gH7jfHfEGckv0tK4%3D)

提示是有一个循环依赖的问题，即 PayApplicationService -\> PayChannelServiceFactory -\> MockPayChannelService -\> PayApplicationService.

Spring不是引入了三级缓存，解决了循环依赖的问题吗？那为啥启动还报错呢？

### Spring 2.6 开始，默认已经不开启对循环依赖的支持了

**从 Spring Framework 5.3 开始，Spring 默认禁用了对循环依赖的支持，而在 Spring 2.6 中，这一行为得到了进一步的明确和强化**

如果想要开启对循环依赖的支持，需要在配置文件中加入

java

 体验AI代码助手

 代码解读

复制代码

```
spring.main.allow-circular-references=true
```

或者，如果不想加配置的话，也可以用`@Lazy` 注解，在`@Autowired` 地方增加即可：

java

 体验AI代码助手

 代码解读

复制代码

```
@Autowired
@Lazy
private PayChannelServiceFactory payChannelServiceFactory;
```

标签：

[后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF)[架构](https://juejin.cn/tag/%E6%9E%B6%E6%9E%84)

话题：

[我的技术写作成长之路](https://juejin.cn/theme/detail/7215101716402798596?contentType=1)

本文收录于以下专栏

![Image 13: cover](https://p26-juejin-sign.byteimg.com/tos-cn-i-k3u1fbpfcp/95414745836549ce9143753e2a30facd~tplv-k3u1fbpfcp-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv56iL5bqP5ZGYQXNrYQ==:q75.awebp?rk3s=f64ab15b&x-expires=1743479658&x-signature=I6BGdP0f3vbnXliNMFjogMb0MGk%3D)

走进springboot细节

专栏目录

spring springboot 等等springboot源码细节

8 订阅

·

4 篇文章

订阅

上一篇

mybatis+springboot+MySQL批量插入 1w 条数据——探讨

评论 13

![Image 14: avatar](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/58aaf1326ac763d8a1054056f3b7f2ef.svg)

0 / 1000

标点符号、链接等不计算在有效字数内

Ctrl + Enter

发送

登录 / 注册 即可发布评论！

最热

最新

[![Image 15: 大剑者兰特的头像](https://p9-passport.byteacctimg.com/img/user-avatar/4073c1a69b1f4faede021b4b19df991b~50x50.awebp)](https://juejin.cn/user/864658271255646)

[大剑者兰特](https://juejin.cn/user/864658271255646)

安利

5天前

点赞

评论

*   屏蔽作者：大剑者兰特
    
*   举报
    

[![Image 16: 动漫里的人物的头像](https://p6-passport.byteacctimg.com/img/user-avatar/9a80ec881264dea5c0723226004fd58a~50x50.awebp)](https://juejin.cn/user/4277542078648477)

[动漫里的人物](https://juejin.cn/user/4277542078648477)

值得去一读

5天前

点赞

评论

*   屏蔽作者：动漫里的人物
    
*   举报
    

[![Image 17: 开不了口506的头像](https://p3-passport.byteacctimg.com/img/user-avatar/f3f217e43bffa9a1f7b2aea62bf69143~50x50.awebp)](https://juejin.cn/user/1603529467772024)

[开不了口506](https://juejin.cn/user/1603529467772024)

内容精彩

5天前

点赞

评论

*   屏蔽作者：开不了口506
    
*   举报
    

查看全部 13 条评论

![Image 18](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/c12d6646efb2245fa4e88f0e1a9565b7.svg) 64

![Image 19](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/336af4d1fafabcca3b770c8ad7a50781.svg) 13

![Image 20](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/3d482c7a948bac826e155953b2a28a9e.svg) 收藏

加个关注，精彩更新不错过~

![Image 21: avatar](https://p6-passport.byteacctimg.com/img/user-avatar/4c5b6ad1cf830524646e3c023478e89b~40x40.awebp)

关注

[![Image 22: avatar](https://p6-passport.byteacctimg.com/img/user-avatar/4c5b6ad1cf830524646e3c023478e89b~100x100.awebp) 后端程序员Aska ![Image 23: 创作等级LV.5](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8584543d8535435a9d74c1fbf7901ac7~tplv-k3u1fbpfcp-jj:0:0:0:0:q75.avis) 高级Java后端开发 @海底捞-供应链 作者榜No.1 优秀作者](https://juejin.cn/user/4389699570630893/posts)

[81 文章](https://juejin.cn/user/4389699570630893/posts)[226k 阅读](https://juejin.cn/user/4389699570630893/posts)[315 粉丝](https://juejin.cn/user/4389699570630893/followers)

加个关注，精彩更新不错过~

关注

已关注

[私信](https://juejin.cn/notification/im?participantId=4389699570630893)

目录

收起

*   [✅Spring 循环依赖细节](https://juejin.cn/post/7483329722496581658#heading-0 "✅Spring 循环依赖细节")
    
*   [✅Spring 循环依赖导致启动报错](https://juejin.cn/post/7483329722496581658#heading-1 "✅Spring 循环依赖导致启动报错")
    
    *   [Spring 2.6 开始，默认已经不开启对循环依赖的支持了](https://juejin.cn/post/7483329722496581658#heading-2 "Spring 2.6 开始，默认已经不开启对循环依赖的支持了")
        

相关推荐

[死磕设计模式---状态模式 5.1k阅读 · 80点赞](https://juejin.cn/post/7482753184654737458 "死磕设计模式---状态模式")[设计模式在Springboot都用在哪些地方呢 288阅读 · 3点赞](https://juejin.cn/post/7483127098352943115 "设计模式在Springboot都用在哪些地方呢")[Redis---RDB\_AOF\_混合持久化 3.1k阅读 · 43点赞](https://juejin.cn/post/7481863661129039899 "Redis---RDB_AOF_混合持久化")[CompletableFuture使用的6个坑 674阅读 · 11点赞](https://juejin.cn/post/7481840315047591988 "CompletableFuture使用的6个坑")[Redis---配置文件详解 568阅读 · 27点赞](https://juejin.cn/post/7481600472109547558 "Redis---配置文件详解")

精选内容

[前端打包优化举例 拉不动的猪 · 74阅读 · 0点赞](https://juejin.cn/post/7485200128730365963 "前端打包优化举例")[WXT浏览器插件开发中文教程(3)----WXT全部入口项详解 倔强青铜三 · 38阅读 · 1点赞](https://juejin.cn/post/7485214929995120679 "WXT浏览器插件开发中文教程(3)----WXT全部入口项详解")[Tauri（十五）——多窗口之间通信方案 雨夜寻晴天 · 55阅读 · 1点赞](https://juejin.cn/post/7485201976050188323 "Tauri（十五）——多窗口之间通信方案")[WXT浏览器插件开发中文教程(2)----WXT项目目录结构详解 倔强青铜三 · 31阅读 · 0点赞](https://juejin.cn/post/7485239620579180555 "WXT浏览器插件开发中文教程(2)----WXT项目目录结构详解")[WXT浏览器插件开发中文教程(1)----安装WXT 倔强青铜三 · 36阅读 · 0点赞](https://juejin.cn/post/7485199344943382569 "WXT浏览器插件开发中文教程(1)----安装WXT")

找对属于你的技术圈子

回复「进群」加入官方微信群

![Image 24](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/qr-code.4e391ff.png)

为你推荐

*   [跳出源码地狱，Spring巧用三级缓存解决循环依赖-原理篇](https://juejin.cn/post/6876297755757641735 "跳出源码地狱，Spring巧用三级缓存解决循环依赖-原理篇")
    
    [........](https://juejin.cn/post/6876297755757641735)
    
    *   [源码学徒](https://juejin.cn/user/289926802834734)
        
    *   4年前
        
    *   1.8k
    *   13
    *   5
    
    [Spring](https://juejin.cn/tag/Spring "Spring")
    
    ![Image 25: 跳出源码地狱，Spring巧用三级缓存解决循环依赖-原理篇](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8ce6a0148e934de3a435ed8500bc19c6~tplv-k3u1fbpfcp-jj:108:72:0:0:q75.avis)
    
*   [Spring基础-009-依赖循环](https://juejin.cn/post/7469686784207634482 "Spring基础-009-依赖循环")
    
    [9.1 什么是Bean的依赖循环 A对象中有B属性 . B属性中有A属性 . A和B如果需要完全被定义就需要依赖对方 这就是依赖循环, 9.2singleton下的set注入产生的依赖循环 首先给两个](https://juejin.cn/post/7469686784207634482)
    
    *   [Athel](https://juejin.cn/user/1687088509511403)
        
    *   1月前
        
    *   16
    *   点赞
    *   评论
    
    [Spring](https://juejin.cn/tag/Spring "Spring")
    
*   [spring循环依赖-不仅仅是八股文](https://juejin.cn/post/7028190876807462943 "spring循环依赖-不仅仅是八股文")
    
    [一.前言 hello，everyone。 spring的循环依赖问题是面试的时候经常会碰到的问题。相信很多朋友都看相关spring使用三级缓存解决循环依赖的博文。面试官问你的时候除了想要了解你对spr](https://juejin.cn/post/7028190876807462943)
    
    *   [柏炎](https://juejin.cn/user/4089838987914456)
        
    *   3年前
        
    *   2.5k
    *   77
    *   6
    
    [后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF "后端") [Spring Boot](https://juejin.cn/tag/Spring%20Boot "Spring Boot")
    
*   [秃头系列-Spring循环依赖](https://juejin.cn/post/7065166881354678285 "秃头系列-Spring循环依赖")
    
    [「这是我参与2022首次更文挑战的第18天，活动详情查看：2022首次更文挑战」Spring循环依赖](https://juejin.cn/post/7065166881354678285)
    
    *   [L\_Denny](https://juejin.cn/user/4195392104706718)
        
    *   3年前
        
    *   83
    *   点赞
    *   评论
    
    [面试](https://juejin.cn/tag/%E9%9D%A2%E8%AF%95 "面试")
    
*   [3.1 spring5源码系列--手写循环依赖](https://juejin.cn/post/6996721915020722183 "3.1 spring5源码系列--手写循环依赖")
    
    [这是我参与8月更文挑战的第14天，活动详情查看：8月更文挑战 本次博客的目标 手写spring循环依赖的整个过程 spring怎么解决循环依赖 为什么要二级缓存和三级缓存 spring有没有解决构造函](https://juejin.cn/post/6996721915020722183)
    
    *   [summerSunShine](https://juejin.cn/user/2815164945035064)
        
    *   3年前
        
    *   383
    *   7
    *   评论
    
    [后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF "后端")
    
*   [3.4 spring5源码系列--循环依赖的设计思想](https://juejin.cn/post/6997996083934658596 "3.4 spring5源码系列--循环依赖的设计思想")
    
    [这是我参与8月更文挑战的第18天，活动详情查看：8月更文挑战 前面已经写了关于三篇循环依赖的文章, 这是一个总结篇 第一篇: 3.1 spring5源码系列--循环依赖 之 手写代码模拟spring循](https://juejin.cn/post/6997996083934658596)
    
    *   [summerSunShine](https://juejin.cn/user/2815164945035064)
        
    *   3年前
        
    *   324
    *   5
    *   评论
    
    [后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF "后端") [Spring](https://juejin.cn/tag/Spring "Spring")
    
*   [Spring系列4-循环依赖](https://juejin.cn/post/7146563426603663373 "Spring系列4-循环依赖")
    
    [循环依赖 什么是循环依赖 解决循环依赖 原理 Spring之所以能够解决循环依赖主要是采用了一种置换原则，也就是俗称的三级缓存，其实就是三个Map。 简单说下原理： 原理分析完了，看下具体实现，在Sp](https://juejin.cn/post/7146563426603663373)
    
    *   [写完就吃饭](https://juejin.cn/user/686511727584510)
        
    *   2年前
        
    *   195
    *   1
    *   评论
    
    [后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF "后端")
    
*   [Spring三级缓存-解决循环依赖](https://juejin.cn/post/7201047960833359930 "Spring三级缓存-解决循环依赖")
    
    [前言 Spring中使用三级缓存来解决单例模式下属性的循环依赖问题（对于多例Bean和Prototype作用域的Bean循环依赖问题不能使用三级缓存手机解决） 一、什么是循环依赖 指在类与类之间存在相](https://juejin.cn/post/7201047960833359930)
    
    *   [miracle丶](https://juejin.cn/user/3931509311940797)
        
    *   2年前
        
    *   92
    *   1
    *   评论
    
    [Java](https://juejin.cn/tag/Java "Java")
    
*   [day06-springBean循环依赖](https://juejin.cn/post/7056361792842235911 "day06-springBean循环依赖")
    
    [「这是我参与2022首次更文挑战的第6天，活动详情查看：2022首次更文挑战」。 什么是循环依赖？ 在我们的开发中，会不可避免的遇到Bean之间循环依赖的，所谓循环依赖，就是两个或者两个以上的Bean](https://juejin.cn/post/7056361792842235911)
    
    *   [不会起名的小张](https://juejin.cn/user/1372661123923070)
        
    *   3年前
        
    *   91
    *   5
    *   评论
    
    [后端](https://juejin.cn/tag/%E5%90%8E%E7%AB%AF "后端")
    
*   [Spring IoC - 依赖注入 源码解析](https://juejin.cn/post/6844903968313884686 "Spring IoC - 依赖注入 源码解析")
    
    [本篇文章中，我们继续介绍Spring IoC 依赖注入的过程和源码解读。 还是如之前一样，为大家梳理一下步骤流程，以便于大家能在心里有个大概的脉络，更容易读懂源码，更容易抓住重点。 ... 上一章最后一节，容器初始化的倒数第二步，finishBeanFactoryInitial…](https://juejin.cn/post/6844903968313884686)
    
    *   [Richard\_Yi](https://juejin.cn/user/3562073406314311)
        
    *   5年前
        
    *   7.3k
    *   18
    *   评论
    
    [Java](https://juejin.cn/tag/Java "Java")
    
*   [Spring5源码9-循环依赖源码分析](https://juejin.cn/post/7135039627043274759 "Spring5源码9-循环依赖源码分析")
    
    [Spring解决循环依赖源码分析，三级缓存的产生原理分析，不能解决构造函数的循环依赖和多实例的循环依赖](https://juejin.cn/post/7135039627043274759)
    
    *   [hsfxuebao](https://juejin.cn/user/3034307826031246)
        
    *   2年前
        
    *   1.2k
    *   4
    *   2
    
    [Spring](https://juejin.cn/tag/Spring "Spring") [Java](https://juejin.cn/tag/Java "Java")
    
*   [Spring源码分析---单例模式下循环依赖的解决](https://juejin.cn/post/6844903762872516616 "Spring源码分析---单例模式下循环依赖的解决")
    
    [这版有错误 递归依赖加载并不是在这个循环里面，而是在填充属性的时候进行加载的。 在spring的启动过程中，有时候会出现bean之间的循环依赖，那什么是循环依赖呢？就是A依赖B，B依赖A，在A未加载完成的情况下，同时B开始了加载，这个时候又要注入A，这样就会出现问题。 spri…](https://juejin.cn/post/6844903762872516616)
    
    *   [bobobobo66415](https://juejin.cn/user/976022055947288)
        
    *   6年前
        
    *   549
    *   点赞
    *   评论
    
    [Spring](https://juejin.cn/tag/Spring "Spring")
    
*   [Spring-bean的循环依赖](https://juejin.cn/post/7264387737276219449 "Spring-bean的循环依赖")
    
    [一、循环依赖（循环引用）的概念 循环依赖其实就是循环引用，也就是一个或多个Bean互相持有对方，最终形成闭环。比如：A依赖于B，B依赖与A。 以下都属于循环引用 二、三级缓存解决循环依赖 循环依赖会带](https://juejin.cn/post/7264387737276219449)
    
    *   [用户9381691255360](https://juejin.cn/user/3485906645565271)
        
    *   1年前
        
    *   63
    *   点赞
    *   评论
    
    [Spring](https://juejin.cn/tag/Spring "Spring")
    
*   [手写Spring---DI依赖注入（2）](https://juejin.cn/post/6844903826932121613 "手写Spring---DI依赖注入（2）")
    
    [接上一篇《手写Spring---IOC容器(1)》继续更新一、DI分析Q1：那些地方会有依赖？Q2：依赖注入的本质是什么？Q3：参数值，属性值，可能是什么值？Q4：直接赋予的值会有哪几种类型？结论:无](https://juejin.cn/post/6844903826932121613)
    
    *   [说出你的愿望吧](https://juejin.cn/user/1574156381468286)
        
    *   5年前
        
    *   2.0k
    *   33
    *   14
    
    [Java](https://juejin.cn/tag/Java "Java")
    
*   [看穿面试题-Spring循环依赖-背后的秘密](https://juejin.cn/post/6844904166351978504 "看穿面试题-Spring循环依赖-背后的秘密")
    
    [一、面试题循环依赖问题背后的秘密二、基础知识准备1. Java 引用传递还是值传递?2. Bean创建的几个关键点3. AOP的原理4. getBean()5. 三个缓存三、解析循环依赖1.一个缓存能解决不？2.两个缓存能解决不？3.为什么需要三个缓存代理的存在Spring 是…](https://juejin.cn/post/6844904166351978504)
    
    *   [享学源码](https://juejin.cn/user/4283353032046622)
        
    *   4年前
        
    *   3.2k
    *   19
    *   10
    
    [Java](https://juejin.cn/tag/Java "Java")
    

收藏成功！

已添加到「」， 点击更改

*   微信
    
    ![Image 26](https://juejin.cn/post/7483329722496581658)微信扫码分享
    
*   新浪微博
*   QQ

![Image 27: image](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/cartoon.31472f0.png)

AI代码助手上线啦

选中代码，体验AI替你一键快速解读代码

立即体验

APP内打开

 *    ![Image 28: 下载掘金APP](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2ad212d53ccd44569d10317171664bae~tplv-k3u1fbpfcp-jj:90:0:0:0:q75.avis) 下载APP
    
    下载APP
*    ![Image 29: 微信扫一扫](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9f4933cc8fdb411cba89904f14a3ec0a~tplv-k3u1fbpfcp-jj:90:0:0:0:q75.avis) 微信扫一扫
    
    微信公众号
*   [新浪微博](https://weibo.com/xitucircle)

 

![Image 30](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/MaskGroup.13dfc4f.png) 选择你感兴趣的技术方向

后端

前端

Android

iOS

人工智能

开发工具

代码人生

阅读

跳过

上一步

至少选择1个分类

温馨提示

当前操作失败，如有疑问，可点击申诉

前往申诉 我知道了

![Image 31](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/8867e249c23a7c0ea596c139befc04d7.svg)

沉浸阅读

确定屏蔽该用户

屏蔽后，对方将不能关注你、与你产生任何互动，无法查看你的主页

取消 确定
