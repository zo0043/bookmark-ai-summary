Title: 13年过去了，Spring官方竟然真的支持Bean的异步初始化了！你好呀，我是歪歪。 两年前我曾经发布过这样的一篇文章《 - 掘金

URL Source: https://juejin.cn/post/7370994785655701531

Markdown Content:
你好呀，我是歪歪。

两年前我曾经发布过这样的一篇文章[《我是真没想到，这个面试题居然从11年前就开始讨论了，而官方今年才表态。》](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%2F-qzXuiE7fcGS7JXxFbu6jg "https://mp.weixin.qq.com/s/-qzXuiE7fcGS7JXxFbu6jg")

文章主要就是由这个面试题引起：

> Spring 在启动期间会做类扫描，以单例模式放入 ioc。但是 spring 只是一个个类进行处理，如果为了加速，我们取消 spring 自带的类扫描功能，用写代码的多线程方式并行进行处理，这种方案可行吗？为什么？

当时我也不知道问题的答案，所以我尝试着去寻找。

但是在找答案之前，我先大胆的猜一个答案：不可以。

为什么？

因为当时我看的是 Spring 5.x 版本的源码，在这个版本里面还是单线程处理 Bean。

对于 Spring 这种使用规模如此之大的开源框架来说，如果能支持 Bean 的异步多线程加载的话，肯定老早就支持了。

所以我先盲猜一个：不可以。

最后我找到了这样的一个 issue 链接：

> [github.com/spring-proj…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fspring-projects%2Fspring-framework%2Fissues%2F13410 "https://github.com/spring-projects/spring-framework/issues/13410")

![Image 1](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b05372af37634cc780a0c79b416ed23b~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=940&h=121&s=19268&e=png&b=ffffff)

题目翻译过来是“在启动期间并行的处理 Bean 的初始化”，紧扣我们的面试题。

注意看这个 issue 的创建时间：2011 年 10 月 12 号。

2022 年看到这个 issue 的时候，才 11 年时间，谁能想到，仅仅两年时间过去，就已经过去了近 13 年时间。（手动狗头

这个链接的关键内容我在前面提到的文章中已经进行过描述了，就不再多说了。

只说 2022 年我写这个话题的时候，最后一个回复是这样的：

![Image 2](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7de6637bf2b148ff8f8c8174a2f676d6~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=876&h=387&s=39710&e=png&b=fffefe)

回答的这个哥们，是 Spring 的官方人员，所以可以理解针对这个问题的官方回答。

这个哥们说了很长一段，我简单的翻译一下：

他说这个问题在最新的 6.0 版本中也不会被解决，因为它目前的优先级并不是特别高。

在处理真正的启动案例时，我们经常发现，时间都花在少数几个相互依赖的特定 bean 上。在那里引入并行化，在很多情况下并不能节省多少，因为这并不能加快关键路径。这通常与 ORM 设置和数据库迁移有关。

你也可以使用“应用程序启动跟踪功能”（application startup tracking）为自己的应用程序收集更多这方面的信息：可以看到启动时间花在哪里以及是如何花的，以及并行化是否会改善这种情况。

对于 Spring Framework 6.0，我们正专注于本地用例的 Ahead Of Time 功能，以及启动时间的改进。

所以，在 2022 年的时候，从这个回复中就可以看出，官方对于并行化处理 bean 的态度是：

![Image 3](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/572ccb779d9a4f4995e0bd144143ce18~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=604&h=588&s=214566&e=png&b=0b0b0b)

在这个 issue 里面也有人给出了一些非官方的解决方案，但是并没有被采纳。

当时这个话题就算是在这里打住了，所以当时对于这个面试题的回答应该是：

理论上是可行的，但是官方并不支持。因为官方觉得通过异步化初始 Bean 只是治标，并不治本。还是应该找到 Bean 初始化慢的原因，分析这些的原因进行针对化的优化。

反转
--

然而，前几天听到消息说 Spring 6.2 版本要发布了，所以我想着去看看里面到底有些啥新东西。

然后我就找到了 v6.2.0-M1 版本的更新日志：

> [github.com/spring-proj…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fspring-projects%2Fspring-framework%2Freleases%2Ftag%2Fv6.2.0-M1 "https://github.com/spring-projects/spring-framework/releases/tag/v6.2.0-M1")

![Image 4](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/2d22e3841dcf45108ec4a5519b65b008~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=782&h=551&s=62446&e=png&b=fffefe)

毕竟是大版本更新，New Features 可以说是非常的多，一眼望去好几十个，鼠标都得划好几下。

心想这么多新特性，得学到啥时候去啊。

![Image 5](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e62999483a9141a1bd71f45d0a3af0e2~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=440&h=391&s=269436&e=png&b=c8b8cb)

突然划到看到这个时候，我眼睛都直了：

![Image 6](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fb99d51428bc4fb58c14569015a0ce4a~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1034&h=235&s=33883&e=png&b=ffffff)

在服务启动时，异步初始化 beans。

不是说好不支持吗？怎么突然变卦了呢？

于是我点到这个 New Features 后面的链接，准备一探究竟：

> [github.com/spring-proj…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fspring-projects%2Fspring-framework%2Fissues%2F19487 "https://github.com/spring-projects/spring-framework/issues/19487")

![Image 7](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5d524eb0c7234f89b9d4ffe8337852f8~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=937&h=657&s=71488&e=png&b=ffffff)

这个 issue 是 2016 年提出来的，提问的这个哥们给出了一个自己实际的案例，然后还是想要官方能够支持 Bean 的异步初始化。

在今年 2 月的时候，这个下面有一个官方回答：

![Image 8](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5b3a1c0077984cea97f80093bf2dfd87~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=931&h=317&s=37676&e=png&b=fffefe)

把链接指引到了 13410 这个 issue 里面。

而 13410 就是我们前面提到的这个 2011 年提出的 issue：

![Image 9](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7e10d0a127b546818708d92cab6a1cda~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=940&h=121&s=19268&e=png&b=ffffff)

所以兜兜转转，还是回到了最开始的地方。

两年过去了，这个问题下最新的回答是 2024 年 2 月 28 日，也是来自官方的回答：

![Image 10](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e7c652c27d56472db63052ce25f377f3~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=937&h=547&s=75070&e=png&b=fffefe)

这个回答可以说非常关键了，是整个 Bean 的异步初始化的实现思路，我带你盘一下关键点，强烈建议你自己去看看，并且根据这部分的描述找到对应的代码。

在这个回答里面提到说会引入 backgroundInit 标识，以及在 @Bean 里面加入 bootstrap=BACKGROUND 枚举，通过这样的方式来支持 Bean 的异步初始化。

会在 preInstantiateSingletons 方法中，覆盖每个加了 BACKGROUND 的 Bean 的整个 getBean 步骤。

因为是异步处理，相应的 Future 会存储起来，这样依赖的 Bean 就会自动等待 Bean 实例完成。

此外，所有常规的后台初始化都会在 preInstantiateSingletons 结束时强制完成。只有被额外标记为 @Lazy 的 Bean 才允许稍后完成（直到第一次实际访问）。

最后这个回答中还强调了一点：因为是异步化操作，所以项目中还需要搞一个叫做 bootstrapExecutor 的线程池，来支持这个事情。

没有，那就异步化不了。

尝鲜
--

气氛都烘托到这里了，那高低得给你整一个 Demo 跑跑才行啊。

目前 Spring 6.2.0 版本还没正式发布，最新的 SpringBoot 里面也还没有集成 Spring 6.2.0 版本。

所以我们不能通过新建一个 SpringBoot 项目来尝鲜，得搞一个纯粹的 Spring 项目。

没想到歪师傅写到这里的时候遇到了一个卡点：怎么去创建一个 Spring 项目来着？

![Image 11](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7d3205b2cf4e4e6a976fd80d292390c4~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=418&h=418&s=143187&e=png&b=5c362f)

这几年要创建一个新的项目，都是直接使用 SpringBoot 的脚手架来搞了，这突然一下让我搞一个纯粹的 Spring 项目出来，还真的有点懵逼。

于是我还去网上搜索了一番。搜索的问题是：如何创建一个 Spring 项目。

这个问题，我当年刚入行的时候肯定也搜过。

要是放在几年前，徒手撸一个 Spring 项目的架子出来就像是呼吸一样简单。

这几年属于是被 SpringBoot 喂的太好了。

经过一番搜索，终于是搞定了。

首先，我们要指定 Spring 的版本为 6.2.0-SNAPSHOT：

![Image 12](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ac23f1b3f8634a8d823747ecba72be5c~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=451&h=408&s=34148&e=png&b=2b2b2b)

然后搞两个 Bean，在构造方法里面 Sleep 5s，模拟初始化比较耗时的情况：

![Image 13](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1cd5ecfc5dc7433eb4090681fbc19e54~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=939&h=619&s=79895&e=png&b=2b2b2b)

接着找个地方 @Bean，给 Spring 托管一下：

![Image 14](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/635cb348596f436cafbf01d1b79c864f~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=420&h=350&s=21953&e=png&b=2b2b2b)

最后搞个 Main 方法，启动 Spring 容器，同时 用 StopWatch 来统计一下时间：

![Image 15](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c0fda0d35dfa4611801250452b34990d~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=643&h=253&s=28160&e=png&b=2b2b2b)

启动之后，观察控制台：

![Image 16](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/cb3cfa40664e4373a5146b5fd55ede29~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=833&h=271&s=34010&e=png&b=2c2c2c)

可以看出两个 Bean 都是在主线程里面初始化的，由于是串行启动，耗费的时间为 10s。

基于我们这个案例，如果能异步初始化的话，那么理论上 5s 的时间就可以完成初始化。

那么我们怎么让它异步起来呢？

前面官方说了，要用 BACKGROUND 注解。

首先，我们要把 @Bean 的地方改造一下：

> @Bean(bootstrap = Bean.Bootstrap.BACKGROUND)

![Image 17](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3f6e3003910d4ea3a7939d1d60cf996d~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=437&h=334&s=29793&e=png&b=2c2c2c)

随便看一下这个 BACKGROUND 是啥情况：

![Image 18](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ca0dd0c9959349a9a7045da96dee6a28~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=760&h=513&s=39819&e=png&b=2c2c2c)

通过源码我们可以知道，在 6.2 之后，@Bean 注解里面提供了一个 Bootstrap 枚举，有两个取值。

DEFAULT，和原来一样，串行初始化，该值也是默认值：

![Image 19](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/76a6c3293cb74527a1dff5588fd85495~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=659&h=240&s=27845&e=png&b=2b2b2b)

BACKGROUND，表示这个 Bean 需要异步初始化。

那么加入 BACKGROUND 标识之后，是不是就代表改造完成，可以异步化了呢？

在这个时候，启动项目，我们可以看到这样的提示：

![Image 20](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f404e077aa7d4e46b93472c21d391b3d~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1101&h=161&s=16545&e=png&b=2b2b2b)

> Bean 'whyBean' marked for background initialization without bootstrap executor configured - falling back to mainline initialization

这波提示非常清晰，说 whyBean 这个 Bean 标注了需要异步初始化，但是却没有找到 bootstrap 线程池配置，所以回退到主线程初始化模式。

这也就是前面官方提到的这句话：

![Image 21](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/636157bdeef843cdb8b2789069a46c81~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=928&h=548&s=75348&e=png&b=fffefe)

也就是说我们还要搞个名字叫做 bootstrapExecutor 的线程池：

![Image 22](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5b94eb450f2d4e11bebfbd666e1aae5c~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=661&h=416&s=47512&e=png&b=2c2c2c)

再次启动，可以发现已经是在异步线程中初始化了，启动时间也来到了 5s：

![Image 23](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3d6153f87bb0406882f6403de8459d4f~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1082&h=282&s=38301&e=png&b=2c2c2c)

一个最简单的 Demo 就算是演示完成了。

就上面这个 Demo 你照着抄过去，应该花不了五分钟时间吧？

自己拿到本地去跑跑，翻翻源码，debug 一把，这不就是新知识 Get 吗？

然后再搞一点其他的稍微复杂的场景，比如 Bean 之间有依赖的情况。

异步的 Bean 里面依赖了同步的 Bean。

同步的 Bean 里面有异步的 Bean。

上面这些情况，Spring 是否支持，如果支持是怎么处理的，如果不支持会抛出什么样的异常。

这些就当是课后作业吧，我就不手摸手教学了。

主要是我看了一下这部分源码，真的是太好 debug 了，顺着源码往下看就行了。

这个“太好 debug” 具体体现在什么地方，我给你举一个简单的小例子。

比如刚刚我们提到的线程池，名称必须叫做 bootstrapExecutor，你改个名字就不灵了，比如这样：

![Image 24](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7ee827ec35b84ed591d1b5fcaa1fe47b~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=867&h=491&s=62977&e=png&b=2c2c2c)

你问为什么？

别问，源码之下无秘密。

你可以通过两个方式去找答案。

第一个是通过日志：

> \[main\] INFO org.springframework.beans.factory.support.DefaultListableBeanFactory - Bean 'whyBean' marked for background initialization without bootstrap executor configured - falling back to mainline initialization

通过上面这行日志，我们可以在对应类里面找到对应打印的地方：

![Image 25](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/49845d6798154de18f476a127b9a2717~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=968&h=423&s=58360&e=png&b=2c2c2c)

当 getBootstrapExecutor 返回为 null 的时候就会打印这个日志。

那么什么时候不为 null 呢？

可以看看 bootstrapExecutor 对应的 set 方法：

![Image 26](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/9cc2b43cd5bd4b3bb513be95cee43e8a~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1001&h=248&s=50067&e=png&b=363433)

只有一个地方在调用这个方法，这就是我说的“太好 Debug”的表现之一。

然后点过去一看，是要从 beanFactory 里面拿出一个叫做 bootstrapExecutor 的 bean 放进去：

![Image 27](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c22cdac77c344c288e5f5d698ef1c11c~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=920&h=518&s=73440&e=png&b=2d2d2d)

bootstrapExecutor，是写死在源码里面的，所以你换另外一个 xxxExecutor，源码也不识别啊。

另外一个方式就是正向去找。

首先我们知道 BACKGROUND 是我们的一个“抓手”，而这个抓手在源码中也只有一个地方被调用：

![Image 28](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/61c0d5180aa543179f23970ffb34950a~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=863&h=555&s=55375&e=png&b=2d2d2d)

点过去之后发现这里是把 backgroundInit 设置为 true：

![Image 29](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8a5ccbb89bcb400980ce638c841747cd~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=583&h=117&s=15083&e=png&b=2b2b2b)

然后看 backgroundInit 标识被使用的地方：

![Image 30](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/577e9231c75545428e2f0f1cef4dee01~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=970&h=313&s=47443&e=png&b=333131)

又可以找到这里来：

![Image 31](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/de45926679b24626af158b361ad8e56f~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=863&h=342&s=40131&e=png&b=2b2b2b)

这不就和前面呼吁上了。

这部分真的是太好 debug 了，我不骗你，你自己玩去吧。

思考
--

在大概摸清楚具体实现之后，歪师傅开始思考另外一个问题：Spring 为什么要支持 Bean 的异步初始化？

异步化，核心目标是为了加速项目启动，减少项目启动时间嘛。

按照官方最开始的说法，项目启动慢，应该是用户找到启动慢的根本原因，而不是想着异步化这个治标不治本的方法。

比如在前面的 issue 里面，有个老哥说：我这边有个应用启动花了 2 小时 30 分...

在 2011 年，官方是这样回复的：

![Image 32](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ae16895e0c624b5cb10d640e39e800af~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=885&h=542&s=339008&e=png&b=fefcfc)

他们的核心观点还是：在 Spring 容器中并行化 Bean 初始化的好处对于少数使用 Spring 的应用程序来说是非常重要的，而坏处是不可避免的 Bug、增加的复杂性和意想不到的副作用，这些可能会影响所有使用 Spring 的应用程序，恐怕这不是一个有吸引力的前景。

言外之意就是：我不改。

官方希望看到的是用户去寻找启动慢的真正原因。

用户希望的是官方提供一个异步化的方法先来解决当前的问题。

官方和用户都知道这是一个治标不治本的方案。

官方觉得没有必要，或者“太 low”，这样的代码不应该出现在我们的项目中，因为用户没有按照我的预期去使用对应代码。

用户觉得我不管治标还是治本，只要能解决问题就行。

这个时候就出现了分歧。

这个分歧甚至长达 13 年之久。在这期间官方和用户反复拉扯，都难以达成一致。

终于，在 6.2 版本里面，官方还是妥协了，Bean 的异步初始化终于还是落地了。

13 年的时间已经足够长了，长到 Spring 的用户群体已经爆炸式的增长，官方不得不足够重视用户反复提起的需求。

即使这个需求在官方看来是不合理的，这个解决方案看起来是不优雅的，但是由于用户需要，所以不得不提供。

你看这个场景像不像是你在工作中接到了一个自认为不合理的需求，但是却不得不去实施一样。

或者像不像在你精心搭建的系统中，必须加入一坨你觉得很难接受的代码。

就像你刚刚开始工作的时候，甚至有一点代码洁癖。

然后随着需求的叠加、时间的推移、日复一日的重复之后，开始变成“又不是不能用”。

没关系，都是会变的。
