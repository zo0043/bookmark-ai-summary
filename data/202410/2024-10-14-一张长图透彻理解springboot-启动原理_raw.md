Title: 一张长图透彻理解SpringBoot 启动原理，架构师必备知识，不为应付面试！全网独家，透彻解析Spring的启动原理， - 掘金

URL Source: https://juejin.cn/post/7308610896803659812

Markdown Content:
本文已经授权【稀土掘金技术社区】官方公众号独家原创发布。

虽然Java程序员大部分工作都是CRUD，但是工作中常用的中间件必须和Spring集成，如果不知道Spring的原理，很难理解这些中间件和框架的原理。

一张长图透彻解释 Spring启动顺序
-------------------

![Image 1: Timeout重构 (2).jpg](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f817d280732e42c18e342c2163f75011~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1213&h=2593&s=332656&e=jpg&b=fcf8f5)

测试对Spring启动原理的理解程度
------------------

我举个例子，测试一下，你对Spring启动原理的理解程度。

1.  Rpc框架和Spring的集成问题。Rpc框架何时注册暴露服务，在哪个Spring扩展点注册呢？init-method 中行不行？
    
2.  MQ 消费组和Spring的集成问题。MQ消费者何时开始消费，在哪个Spring扩展点”注册“自己？init-method 中行不行？
    
3.  SpringBoot 集成Tomcat问题。如果出现已开启Http流量，Spring还未启动完成，怎么办？Tomcat何时开启端口，对外服务？
    

SpringBoot项目常见的流量入口无外乎 Rpc、Http、MQ 三种方式。**一名合格的架构师必须精通服务的入口流量何时开启，如何正确开启**？最近我遇到的两次线上故障都和Spring启动过程相关。（[点击这里了解故障](https://juejin.cn/post/7302740437529296907 "https://juejin.cn/post/7302740437529296907")）

故障的具体表现是：Kafka消费组已经开始消费，已开启流量，然而Spring 还未启动完成。因为业务代码中使用的Spring Event事件订阅组件还未启动（订阅者还未注册到Spring），所以处理异常，出了线上故障。根本原因是————项目在错误的时机开启 MQ 流量，然而Spring还未启动完成，导致出现故障。

正确的做法是：项目在Spring启动完成后开启入口流量，然而我司的Kafka消费组 在Spring init-method bean 实例化阶段就开启了流量，导致故障发生。出现这样的问题，说明项目初期的程序员没有深入理解Spring的启动原理。

接下来，我再次抛出 11 个问题，说明这个问题————深入理解Spring启动原理的重要性。

1.  Spring还未完全启动，在 PostConstruct 中调用 `getBeanByAnnotation` 能否获得准确的结果？
2.  项目应该如何监听 Spring 的启动就绪事件？
3.  项目如何监听Spring 刷新事件？
4.  Spring就绪事件和刷新事件的执行顺序和区别？
5.  Http 流量入口何时启动完成？
6.  项目中在 init-method 方法中注册 Rpc 是否合理？什么是合理的时机？
7.  项目中在 init-method 方法中注册 MQ 消费组是否合理？ 什么是合理的时机？
8.  PostConstruct 中方法依赖ApplicationContextAware拿到 ApplicationContext，两者的顺序谁先谁后？是否会出现空指针!
9.  init-method、PostConstruct、afterPropertiesSet 三个方法的执行顺序?
10.  有两个 Bean声明了初始化方法。 A使用 PostConstruct注解声明，B使用 init-method 声明。Spring一定先执行 A 的PostConstruct 方法吗？
11.  Spring 何时装配Autowire属性，PostConstruct 方法中引用 Autowired 字段什么场景会空指针?

精通Spring 启动原理，以上问题则迎刃而解。接下来，请大家和五哥，一起学习Spring的启动原理，看看Spring的扩展点分别在何时执行。

一起数数 Spring启动过程的扩展点有几个？
-----------------------

Spring的扩展点极多，这里为了讲清楚启动原理，所以只列举和启动过程有关的扩展点。

1.  BeanFactoryAware 可在Bean 中获取 BeanFactory 实例
2.  ApplicationContextAware 可在Bean 中获取 ApplicationContext 实例
3.  BeanNameAware 可以在Bean中得到它在IOC容器中的Bean的实例的名字。
4.  ApplicationListener 可监听 ContextRefreshedEvent等。
5.  CommandLineRunner 整个项目启动完毕后，自动执行
6.  SmartLifecycle#start 在Spring Bean实例化完成后，执行start 方法。
7.  使用@PostConstruct注解，用于Bean实例初始化
8.  实现InitializingBean接口，用于Bean实例初始化
9.  xml 中声明 init-method 方法，用于Bean实例初始化
10.  Configuration 配置类 通过@Bean注解 注册Bean到Spring
11.  BeanPostProcessor 在Bean的初始化前后，植入扩展点！
12.  BeanFactoryPostProcessor 在BeanFactory创建后植入 扩展点！

通过打印日志学习Spring的执行顺序
-------------------

首先我们先通过 代码实验，验证一下以上扩展点的执行顺序。

1.  声明 `TestSpringOrder` 分别继承以下接口，并且在接口方法实现中，日志打印该接口的名称。

```
public class TestSpringOrder implements
      ApplicationContextAware,
      BeanFactoryAware, 
      InitializingBean, 
      SmartLifecycle, 
      BeanNameAware, 
      ApplicationListener<ContextRefreshedEvent>, 
      CommandLineRunner,
      SmartInitializingSingleton {
```

```
@Override
public void afterPropertiesSet() throws Exception {
   log.error("启动顺序:afterPropertiesSet");
}

@Override
public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
   log.error("启动顺序:setApplicationContext");
}
```

2.  `TestSpringOrder` 使用 PostConstruct注解初始化，声明 init-method方法初始化。

```
@PostConstruct
public void postConstruct() {
   log.error("启动顺序:post-construct");
}

public void initMethod() {
   log.error("启动顺序:init-method");
}
```

3.  新建 TestSpringOrder2 继承

```
public class TestSpringOrder3 implements
         BeanPostProcessor, 
         BeanFactoryPostProcessor {
   @Override
   public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
      log.error("启动顺序:BeanPostProcessor postProcessBeforeInitialization beanName:{}", beanName);
      return bean;
   }

   @Override
   public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
      log.error("启动顺序:BeanPostProcessor postProcessAfterInitialization beanName:{}", beanName);
      return bean;
   }

   @Override
   public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException {
      log.error("启动顺序:BeanFactoryPostProcessor postProcessBeanFactory ");
   }
}
```

执行以上代码后，可以在日志中看到启动顺序！

### 实际的执行顺序

```
2023-11-25 18:10:53,748 [main] ERROR (TestSpringOrder3:37) - 启动顺序:BeanFactoryPostProcessor postProcessBeanFactory 
2023-11-25 18:10:59,299 [main] ERROR (TestSpringOrder:53) - 启动顺序:构造函数 TestSpringOrder
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder:127) - 启动顺序: Autowired
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder:129) - 启动顺序:setBeanName
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder:111) - 启动顺序:setBeanFactory
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder:121) - 启动顺序:setApplicationContext
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder3:25) - 启动顺序:BeanPostProcessor postProcessBeforeInitialization beanName:testSpringOrder
2023-11-25 18:10:59,316 [main] ERROR (TestSpringOrder:63) - 启动顺序:post-construct
2023-11-25 18:10:59,317 [main] ERROR (TestSpringOrder:116) - 启动顺序:afterPropertiesSet
2023-11-25 18:10:59,317 [main] ERROR (TestSpringOrder:46) - 启动顺序:init-method
2023-11-25 18:10:59,320 [main] ERROR (TestSpringOrder3:31) - 启动顺序:BeanPostProcessor postProcessAfterInitialization beanName:testSpringOrder
2023-11-25 18:17:21,563 [main] ERROR (SpringOrderConfiguartion:21) - 启动顺序: @Bean 注解方法执行
2023-11-25 18:17:21,668 [main] ERROR (TestSpringOrder:58) - 启动顺序:SmartInitializingSingleton
2023-11-25 18:17:21,675 [main] ERROR (TestSpringOrder:74) - 启动顺序:start
2023-11-25 18:17:23,508 [main] ERROR (TestSpringOrder:68) - 启动顺序:ContextRefreshedEvent
2023-11-25 18:17:23,574 [main] ERROR (TestSpringOrder:79) - 启动顺序:CommandLineRunner
```

我通过在以上扩展点 添加 debug 断点，调试代码，整理出 Spring启动原理的 长图。过程省略…………

一张长图透彻解释 Spring启动顺序
-------------------

![Image 2: Timeout重构 (2).jpg](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f817d280732e42c18e342c2163f75011~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1213&h=2593&s=332656&e=jpg&b=fcf8f5)

### 实例化和初始化的区别

new TestSpringOrder()； new 创建对象实例，即为实例化一个对象；执行该Bean的 init-method 等方法 为初始化一个Bean。注意初始化和实例化的区别。

Spring 重要扩展点的启动顺序
-----------------

1.  **BeanFactoryPostProcessor**  
    BeanFactory初始化之后，所有的Bean定义已经被加载，但Bean实例还没被创建（不包括`BeanFactoryPostProcessor`类型）。Spring IoC容器允许BeanFactoryPostProcessor读取配置元数据，修改bean的定义，Bean的属性值等。
    
2.  **实例化Bean**
    
    Spring 调用java反射API 实例化 Bean。 等同于 new TestSpringOrder();
    
3.  **Autowired 装配依赖**
    
    Autowired是 借助于 AutowiredAnnotationBeanPostProcessor 解析 Bean 的依赖，装配依赖。如果被依赖的Bean还未初始化，则先初始化 被依赖的Bean。在 Bean实例化完成后，Spring将首先装配Bean依赖的属性。
    
4.  **BeanNameAware** setBeanName
    
5.  **BeanFactoryAware** setBeanFactory
    
6.  **ApplicationContextAware setApplicationContext**
    
    在Bean实例化前，会率先设置Aware接口，例如 BeanNameAware BeanFactoryAware ApplicationContextAware 等
    
7.  **BeanPostProcessor** postProcessBeforeInitialization
    
    如果我想在 bean初始化方法前后要添加一些自己逻辑处理。可以提供 BeanPostProcessor接口实现类，然后注册到Spring IoC容器中。**在此接口中，可以创建Bean的代理，甚至替换这个Bean。**
    
8.  **PostConstruct** 执行
    
    接下来 Spring会依次调用 Bean实例初始化的 三大方法。
    
9.  **InitializingBean** afterPropertiesSet
    
10.  **init-method** 方法执行
    
11.  **BeanPostProcessor** postProcessAfterInitialization
    
    在 Spring 对Bean的初始化方法执行完成后，执行该方法
    
12.  其他Bean 实例化和初始化
    
    Spring 会循环初始化Bean。直至所有的单例Bean都完成初始化
    
13.  所有单例Bean 初始化完成后
    
14.  SmartInitializingSingleton Bean实例化后置处理
    
    该接口的执行时机在 所有的单例Bean执行完成后。例如Spring 事件订阅机制的 EventListener注解，所有的订阅者 都是 在这个位置被注册进 Spring的。而在此之前，Spring Event订阅机制还未初始化完成。所以如果有 MQ、Rpc 入口流量在此之前开启，Spring Event就可能出问题！
    
    所以强烈建议 **Http、MQ、Rpc 入口流量在 SmartInitializingSingleton 之后开启流量。**
    

> Http、MQ、Rpc 入口流量必须在 SmartInitializingSingleton 之后开启流量。

15.  SmartLifecyle smart start 方法执行 Spring 提供的扩展点，在所有单例Bean的 EventListener等组件全部启动完成后，即Spring启动完成，则执行 start 方法。在这个位置适合开启入口流量！

> Http、MQ、Rpc 入口流量适合 在 SmartLifecyle 中开启

16.  发布 ContextRefreshedEvent 方法 该事件会执行多次，在 Spring Refresh 执行完成后，就会发布该事件！
    
17.  注册和初始化 Spring MVC
    
    SpringBoot 应用，在父级 Spring启动完成后，会尝试启动 内嵌式 tomcat容器。在此之前，SpringBoot会初始化 SpringMVC 和注册DispatcherServlet到Web容器。
    
18.  Tomcat/Jetty 容器开启端口
    
    SpringBoot 调用内嵌式容器，会开启并监听端口，此时Http流量就开启了。
    
19.  应用启动完成后，执行 CommandLineRunner
    
    SpringBoot 特有的机制，待所有的完全执行完成后，会执行该接口 run方法。值得一提的是，由于此时Http流量已经开启，如果此时进行本地缓存初始化、预热缓存等，稍微有些晚了！ 在这个间隔期，可能缓存还未就绪！
    
    所以预热缓存的时机应该发生在 入口流量开启之前，比较合适的机会是在 Bean初始化的阶段。虽然 在Bean初始化时 Spring尚未完成启动，但是调用 Bean预热缓存也是可以的。但是注意：不要在 Bean初始化时 使用 Spring Event，因为它还未完成初始化 。
    

回答 关于 Spring 启动原理的若干问题
----------------------

1.  init-method、PostConstruct、afterPropertiesSet 三个方法的执行顺序。

> 回答： PostConstruct，afterPropertiesSet，init-method

2.  有两个 Bean声明了初始化方法。 A使用 PostConstruct注解声明，B使用 init-method 声明。Spring一定先执行 A 的PostConstruct 方法吗？

> 回答：Spring 会循环初始化Bean实例，初始化完成1个Bean，再初始化下一个Bean。Spring并没有使用这种机制启动，即所有的Bean先执行 PostConstruct，再统一执行afterProperfiesSet。 此外，A、B两个Bean的初始化顺序不确定，谁先谁后不确定。无法保证 A 的PostConstruct 一定先执行。除非使用 Order注解，声明Bean的初始化顺序！

3.  Spring 何时装配Autowire属性，PostConstruct方法中引用 Autowired 字段是否会空指针?

> Autowired装配依赖发生在 PostConstruct之前，不会出现空指针！

4.  PostConstruct 中方法依赖ApplicationContextAware拿到 ApplicationContext，两者的顺序谁先谁后？是否会出现空指针!

> ApplicationContextAware 会先执行，不会出现空指针！但是当Autowired没有找到对应的依赖，并且声明了非强制依赖时，该字段会为空，有潜在 空指针风险。

11.  项目应该如何监听 Spring 的启动就绪事件。

> 通过SmartLifecyle start方法，监听Spring就绪 。适合在此开启入口流量！

13.  项目如何监听Spring 刷新事件。

> 监听 Spring Event ContextRefreshedEvent

15.  Spring就绪事件和刷新事件的执行顺序和区别。

> Spring就绪事件会先于 刷新事件。两者都可能多次执行，要确保方法的幂等处理，避免重复注册问题

16.  Http 流量入口何时启动完成。

> SpringBoot 最后阶段，启动完成Spring 上下文，才开启Http入口流量，此时 SmartLifecycle#start 已执行。所有单例Bean和SpringEvent等组件都已经就绪！

17.  项目中在 init-method 方法中注册 Rpc是否合理？什么是合理的时机？

> init 开启Rpc流量非常不合理。因为Spring尚未启动完成，包括 Spring Event尚未就绪！

18.  项目中在 init-method 方法中注册 MQ消费组是否合理？ 什么是合理的时机？

> init 开启 MQ 流量非常不合理。因为Spring尚未启动完成，包括 Spring Event尚未就绪！

22.  Spring还未完全启动，在 PostConstruct 中调用 getBeanByAnnotation能否获得准确的结果？

> 虽然未启动完成，但是Spring执行该getBeanByAnnotation方法时，会率先检查 Bean定义，如果Bean定义对应的 Bean尚未初始化，则初始化这些Bean。所以即便是Spring初始化过程中调用，调用结果是准确的。

源码级别介绍
------

### SmartInitializingSingleton 接口的执行位置

下图代码说明了，Spring在初始化全部 单例Bean以后，会执行 SmartInitializingSingleton 接口。 ![Image 3: image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1c28d31de79c47b48a7a87ac24f50245~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=2146&h=1836&s=548611&e=png&b=101020)

### Autowired 何时装配Bean的依赖

在Bean实例化之后，但初始化之前，`AutowiredAnnotationBeanPostProcessor` 会注入Autowired字段。 ![Image 4: image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3bc4f7da5f0d4839a7a60fc0d991b0d4~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1488&h=182&s=80934&e=png&b=4a463b)

### SpringBoot 何时开启Http端口

下图代码中可以看到，SpringBoot会首先启动 Spring上下文，完成后才启动 嵌入式Web容器，初始化SpringMVC，监听端口 ![Image 5: image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/28bd69883797447da7e1e4a030d9b819~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1514&h=702&s=181359&e=png&b=101020)

### Spring 初始化Bean的关键代码

下图我加了注释，Spring初始化Bean的关键代码，全在 这个方法里，感兴趣的可以自行查阅代码 。 AbstractAutowireCapableBeanFactory#initializeBean

![Image 6: image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/b3fb53bc84c24383ad37d54a99ba15bd~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1001&h=567&s=144349&e=png&b=101020)

### Spring CommandLineRunner 执行位置

Spring Boot外部，当启动完Spring上下文以后，最后才启动 CommandLineRunner。 ![Image 7: image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d10073a980944822b2a489ffeb667ef2~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1558&h=696&s=248095&e=png&b=101020) ![Image 8: image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a7ef17a4fff8427bb28b49b8a0326012~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp#?w=1286&h=198&s=65458&e=png&b=4a4840)

总结
--

SpringBoot 会在Spring完全启动完成后，才开启Http流量。这给了我们启示：**应该在Spring启动完成后开启入口流量**。Rpc和 MQ流量 也应该如此，所以建议大家 在 SmartLifecype 或者 ContextRefreshedEvent 等位置 注册服务，开启流量。

例如 Spring Cloud `Eureka` 服务发现组件，就是在 SmartLifecype中注册服务的！

整理 10 个小时写完本篇文章，希望大家有所收获。\[抱拳\]
