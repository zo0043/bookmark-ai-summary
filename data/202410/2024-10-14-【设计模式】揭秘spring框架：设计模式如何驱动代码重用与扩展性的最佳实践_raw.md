Title: 【设计模式】揭秘Spring框架：设计模式如何驱动代码重用与扩展性的最佳实践在现代软件开发中，设计模式不仅优化了代码结构 - 掘金

URL Source: https://juejin.cn/post/7424904499666501632

Markdown Content:
> **作者：后端小肥肠**
> 
> 🍇 我写过的文章中的相关代码放到了gitee，地址：[xfc-fdw-cloud: 公共解决方案](https://link.juejin.cn/?target=https%3A%2F%2Fgitee.com%2Fu_ncle%2Fxfc-fdw-cloud "https://gitee.com/u_ncle/xfc-fdw-cloud")
> 
> 🍊 有疑问可私信或评论区联系我。
> 
> 🥑  创作不易未经允许严禁转载。
> 
> **姊妹篇：**
> 
> [【设计模式】万字详解：深入掌握五大基础行为模式-CSDN博客](https://link.juejin.cn/?target=https%3A%2F%2Fblog.csdn.net%2Fc18213590220%2Farticle%2Fdetails%2F142432297%3Fspm%3D1001.2014.3001.5501 "https://blog.csdn.net/c18213590220/article/details/142432297?spm=1001.2014.3001.5501")
> 
> [【设计模式】（万字总结）深入理解Java中的创建型设计模式\_java设计模式创建-CSDN博客](https://link.juejin.cn/?target=https%3A%2F%2Fblog.csdn.net%2Fc18213590220%2Farticle%2Fdetails%2F140751369 "https://blog.csdn.net/c18213590220/article/details/140751369")
> 
> [【设计模式】结构型模式全攻略:从入门到精通的万字实战指南\_结构型模式代理模式详解-CSDN博客](https://link.juejin.cn/?target=https%3A%2F%2Fblog.csdn.net%2Fc18213590220%2Farticle%2Fdetails%2F141066406 "https://blog.csdn.net/c18213590220/article/details/141066406")

1\. 前言
------

在现代软件开发中，设计模式不仅优化了代码结构，还提升了应用的灵活性与可维护性。特别是在Spring框架中，设计模式的应用成为了实现其强大功能的基石。本文将深入探讨Spring框架如何通过工厂模式以及其他设计模式来优化对象的生产和管理，强化了框架的功能并简化了开发者的编码工作。通过具体的代码示例和详细的分析，我们将揭示这些设计模式在Spring中的实际运用，帮助开发者更好地理解和运用Spring框架，从而打造出更高效、更稳定的应用。

2\. Spring中工厂模式的应用
------------------

**Spring的设计理念**

*   Spring是面向Bean的编程（BOP：Bean Oriented Programming），Bean在Spring中才是真正的主角。Bean在Spring中作用就像Object对OOP的意义一样，没有对象的概念就像没有面向对象编程，Spring中没有Bean也就没有Spring存在的意义。Spring提供了IoC 容器通过配置文件或者注解的方式来管理对象之间的依赖关系。
*   控制反转（Inversion of Control，缩写为IoC），是面向对象编程中的一种设计原则，可以用来减低代码之间的耦合度。其中最常见的方式叫做依赖注入（Dependency Injection，简称DI），还有一种方式叫“依赖查找”（Dependency Lookup）。通过控制反转，对象在被创建的时候，由一个调控系统内所有对象的外界实体，将其所依赖的对象的引用传递给它。

### 2.1. Spring中的Bean组件

Bean组件定义在Spring的**org.springframework.beans**包下，解决了以下几个问题：

这个包下的所有类主要解决了三件事：

*   Bean的定义
*   Bean的创建
*   Bean的解析

Spring Bean的创建是典型的工厂模式，它的顶级接口是BeanFactory。

![Image 1: 137.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ece6f593dbf247559068d1b25e459e4f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=eyWJgCa%2F1Zc2DeWyQwFxhkPzlzA%3D)

BeanFactory有三个子类：`ListableBeanFactory`、`HierarchicalBeanFactory`和`AutowireCapableBeanFactory`。目的是为了**区分Spring内部对象处理和转化的数据限制**。

但是从图中可以发现最终的默认实现类是`DefaultListableBeanFactory`，它实现了所有的接口

### 2.2. Spring中的BeanFactory

Spring中的BeanFactory就是简单工厂模式的体现，根据传入一个唯一的标识来获得Bean对象

BeanFactory，以Factory结尾，表示它是一个工厂(接口)， 它负责生产和管理bean的一个工厂。在Spring中，BeanFactory是工厂的顶层接口，也是IOC容器的核心接口，因此BeanFactory中定义了**管理Bean的通用方法**，如 **getBean** 和 **containsBean** 等.

它的职责包括：实例化、定位、配置应用程序中的对象及建立这些对象间的依赖。

BeanFactory只是个接口，并不是IOC容器的具体实现，所以Spring容器给出了很多种实现，如 **DefaultListableBeanFactory**、**XmlBeanFactory**、**ApplicationContext**等，其中XmlBeanFactory就是常用的一个，该实现将以XML方式描述组成应用的对象及对象间的依赖关系。

**1) BeanFactory源码解析**

```
public interface BeanFactory {
    
    /**
        对FactoryBean的转移定义,因为如果使用bean的名字来检索FactoryBean得到的是对象是工厂生成的对象,
        如果想得到工厂本身就需要转移
    */
    String FACTORY_BEAN_PREFIX = "&";

    //根据Bean的名字 获取IOC容器中对应的实例
    Object getBean(String var1) throws BeansException;

    
    //根据Bean的名字和class类型得到bean实例,增加了类型安全验证机制
    <T> T getBean(String var1, Class<T> var2) throws BeansException;

    Object getBean(String var1, Object... var2) throws BeansException;

    <T> T getBean(Class<T> var1) throws BeansException;

    <T> T getBean(Class<T> var1, Object... var2) throws BeansException;

    <T> ObjectProvider<T> getBeanProvider(Class<T> var1);

    <T> ObjectProvider<T> getBeanProvider(ResolvableType var1);

    
   //查看Bean容器中是否存在对应的实例,存在返回true 否则返回false
    boolean containsBean(String var1);

    //根据Bean的名字 判断这个bean是不是单例
    boolean isSingleton(String var1) throws NoSuchBeanDefinitionException;

    boolean isPrototype(String var1) throws NoSuchBeanDefinitionException;

    boolean isTypeMatch(String var1, ResolvableType var2) throws NoSuchBeanDefinitionException;

    boolean isTypeMatch(String var1, Class<?> var2) throws NoSuchBeanDefinitionException;

    //得到bean实例的class类型
    @Nullable
    Class<?> getType(String var1) throws NoSuchBeanDefinitionException;

    @Nullable
    Class<?> getType(String var1, boolean var2) throws NoSuchBeanDefinitionException;

    
    //得到bean的别名
    String[] getAliases(String var1);
}

```

**BeanFactory的使用场景**

1.  从IOC容器中获取Bean(Name or Type)
2.  检索IOC容器中是否包含了指定的对象
3.  判断Bean是否为单例

**2) BeanFactory的使用**

```
public class User {

    private int id;

    private String name;

    private Friends friends;

    public User() {
    }

    public User(Friends friends) {
        this.friends = friends;
    }

    //get set......
}

public class Friends {

    private List<String> names;

    public Friends() {
    }

    public List<String> getNames() {
        return names;
    }

    public void setNames(List<String> names) {
        this.names = names;
    }
}
```

**配置文件**

```
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:p="http://www.springframework.org/schema/p"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:task="http://www.springframework.org/schema/task"
       xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans-4.2.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context-4.2.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc-4.2.xsd
        http://www.springframework.org/schema/task
        http://www.springframework.org/schema/task/spring-task-4.2.xsd">
    
    <bean id="User" class="com.example.factory.User">
        <property name="friends" ref="UserFriends" />
    </bean>
    <bean id="UserFriends" class="com.example.factory.Friends">
        <property name="names">
            <list>
                <value>"LiLi"</value>
                <value>"LuLu"</value>
            </list>
        </property>
    </bean>
</beans>
```

**测试**

```
public class SpringFactoryTest {

    public static void main(String[] args) {
        ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("bean.xml");
        User user = ctx.getBean("User", User.class);

        List<String> names = user.getFriends().getNames();
        for (String name : names) {
            System.out.println("FriendName: " + name);
        }

        ctx.close();
    }
}
```

### 2.3. Spring中的FactoryBean

首先FactoryBean是一个Bean，但又不仅仅是一个Bean，这样听起来矛盾，但为啥又这样说呢？其实在Spring中，所有的Bean都是由BeanFactory（也就是IOC容器）来进行管理的。但对FactoryBean而言，**这个FactoryBean不是简单的Bean，而是一个能生产或者修饰对象生成的工厂Bean,它的实现与设计模式中的工厂方法模式和修饰器模式类似**

**1) 为什么需要FactoryBean?**

1.  在某些情况下，实例化Bean过程比较复杂，如果按照传统的方式，则需要在中提供大量的配置信息。配置方式的灵活性是受限的，这时采用编码的方式可能会得到一个简单的方案。Spring为此提供了一个`org.springframework.bean.factory.FactoryBean`的工厂类接口，用户可以通过实现该接口定制实例化Bean的逻辑。FactoryBean接口对于Spring框架来说占用重要的地位，Spring自身就提供了70多个FactoryBean的实现。它们隐藏了实例化一些复杂Bean的细节，给上层应用带来了便利。
2.  由于第三方库不能直接注册到spring容器，于是可以实现`org.springframework.bean.factory.FactoryBean`接口，然后给出自己对象的实例化代码即可。

**2 ) FactoryBean的使用特点**

1.  当用户使用容器本身时，可以使用转义字符"&"来得到FactoryBean本身，以区别通过FactoryBean产生的实例对象和FactoryBean对象本身。
    
2.  在BeanFactory中通过如下代码定义了该转义字符：
    
    ```
     StringFACTORY_BEAN_PREFIX = "&";
    ```
    
3.  举例
    
    ```
    如果MyObject是一个FactoryBean，则使用&MyObject得到的是MyObject对象，而不是MyObject产生出来的对象。
    ```
    

**3) FactoryBean的代码示例**

```
@Configuration
@ComponentScan("com.example.factory_bean")
public class AppConfig {
}

@Component("studentBean")
public class StudentBean implements FactoryBean {

    //返回工厂中的实例
    @Override
    public Object getObject() throws Exception {
        //这里并不一定要返回MyBean自身的实例，可以是其他任何对象的实例。
        return new TeacherBean();
    }

    //该方法返回的类型是在IOC容器中getBean所匹配的类型
    @Override
    public Class<?> getObjectType() {
        return StudentBean.class;
    }

    public void study(){
        System.out.println("学生学习......");
    }
}

public class TeacherBean {

    public void teach(){
        System.out.println("老师教书......");
    }
}

public class Test01 {

    public static void main(String[] args) {

        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
        //StudentBean studentBean = (StudentBean)context.getBean("studentBean");

        //加上&符号,返回工厂中的实例
//        StudentBean studentBean = (StudentBean)context.getBean("&studentBean");
//        studentBean.study();

        TeacherBean teacherBean = (TeacherBean) context.getBean("studentBean");
        teacherBean.teach();
    }
}
```

**3) FactoryBean源码分析**

```
public interface FactoryBean<T> {
    String OBJECT_TYPE_ATTRIBUTE = "factoryBeanObjectType";

    /**
    getObject()方法: 会返回该FactoryBean生产的对象实例,我们需要实现该方法,以给出自己的对象实例化逻辑
    这个方法也是FactoryBean的核心.
    */
    @Nullable
    T getObject() throws Exception;

    /**
    getObjectType()方法: 仅返回getObject() 方法所返回的对象类型,如果预先无法确定,返回NULL,
    这个方法返回类型是在IOC容器中getBean所匹配的类型
    */
    @Nullable
    Class<?> getObjectType();

    //该方法的结果用于表明 工厂方法getObject() 所生产的 对象是否要以单例形式存储在容器中如果以单例存在就返回true,否则返回false
    default boolean isSingleton() {
        return true;
    }
}
```

FactoryBean表现的是一个工厂的职责,如果一个BeanA 是实现FactoryBean接口,那么A就是变成了一个工厂,根据A的名称获取到的实际上是工厂调用getObject()方法返回的对象,而不是对象本身,如果想获取工厂对象本身,需要在名称前面加上 '&'符号

*   getObject('name') 返回的是工厂中工厂方法生产的实例
*   getObject('&name') 返回的是工厂本身实例

**使用场景**

*   FactoryBean的最为经典的使用场景,就是用来创建AOP代理对象,这个对象在Spring中就是 ProxyFactoryBean

**BeanFactory与FactoryBean区别**

*   他们两个都是工厂,但是FactoryBean本质还是一个Bean,也归BeanFactory管理
*   BeanFactory是Spring容器的顶层接口,FactoryBean更类似于用户自定义的工厂接口

**BeanFactory和ApplicationContext的区别**

*   BeanFactory是Spring容器的顶层接口,而ApplicationContext应用上下文类 他是BeanFactory的子类,他是Spring中更高级的容器,提供了更多的功能
    
    *   国际化
    *   访问资源
    *   载入多个上下文
    *   消息发送 响应机制
*   两者的装载bean的时机不同
    
    *   BeanFactory: 在系统启动的时候不会去实例化bean,只有从容器中拿bean的时候才会去实例化(懒加载)
        
        *   优点: 应用启动的时候占用的资源比较少,对资源的使用要求比较高的应用 ,比较有优势
    *   ApplicationContext:在启动的时候就把所有的Bean全部实例化.
        
        *   lazy-init= true 可以使bean延时实例化
        *   优点: 所有的Bean在启动的时候就加载,系统运行的速度快,还可以及时的发现系统中配置的问题.

3\. Spring中观察者模式的应用
-------------------

### 3.1. 观察者模式与发布订阅模式的异同

**观察者模式它是用于建立一种对象与对象之间的依赖关系,一个对象发生改变时将自动通知其他对象,其他对象将相应的作出反应.**

> 在观察者模式中发生改变的对象称为**观察目标**,而被通知的对象称为**观察者**,一个观察目标可以应对多个观察者,而且这些观察者之间可以没有任何相互联系,可以根据需要增加和删除观察者,使得系统更易于扩展.

观察者模式的别名有发布-订阅(Publish/Subscribe)模式, 我们来看一下观察者模式与发布订阅模式结构上的区别

*   在设计模式结构上，发布订阅模式**继承**自观察者模式，是观察者模式的一种实现的变体。
*   在设计模式意图上，两者**关注点**不同，一个关心数据源，一个关心的是事件消息。

![Image 2: 134.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3159391792e24abf9ebf11d870e6cf48~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=hyX%2FK8YZfKaT8L7oBvJFLmiocoo%3D)

> 观察者模式里，只有两个角色 —— 观察者 + 被观察者; 而发布订阅模式里，却不仅仅只有发布者和订阅者两个角色，还有一个管理并执行消息队列的 “经纪人Broker”
> 
> 观察者和被观察者，是松耦合的关系;发布者和订阅者，则完全不存在耦合

*   观察者模式：**数据源直接通知订阅者发生改变。**
*   发布订阅模式：**数据源告诉第三方（事件通道）发生了改变，第三方再通知订阅者发生了改变。**

### 3.2. Spring中的观察者模式

Spring 基于观察者模式，实现了自身的事件机制也就是事件驱动模型，事件驱动模型通常也被理解成观察者或者发布/订阅模型。

spring事件模型提供如下几个角色

*   **ApplicationEvent**
*   **ApplicationListener**
*   **ApplicationEventPublisher**
*   **ApplicationEventMulticaster**

**1) 事件：ApplicationEvent**

*   是所有事件对象的父类。ApplicationEvent 继承自 jdk 的 EventObject, 所有的事件都需要继承 ApplicationEvent, 并且通过 source 得到事件源。
    
    ```
    public abstract class ApplicationEvent extends EventObject {
        private static final long serialVersionUID = 7099057708183571937L;
        private final long timestamp = System.currentTimeMillis();
    
        public ApplicationEvent(Object source) {
            super(source);
        }
    
        public final long getTimestamp() {
            return this.timestamp;
        }
    }
    ```
    
*   Spring 也为我们提供了很多内置事件:
    
    *   ContextRefreshEvent，当ApplicationContext容器初始化完成或者被刷新的时候，就会发布该事件。
    *   ContextStartedEvent，当ApplicationContext启动的时候发布事件.
    *   ContextStoppedEvent，当ApplicationContext容器停止的时候发布事件.
    *   RequestHandledEvent，只能用于DispatcherServlet的web应用，Spring处理用户请求结束后，系统会触发该事件。

![Image 3: 133.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/859acb598b894d35960089d22677d637~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=eJYexgHdu0vxTHrHwD%2FxnDhQpJ8%3D)

**2) 事件监听：ApplicationListener**

*   ApplicationListener(应用程序事件监听器) 继承自jdk的EventListener,所有的监听器都要实现这个接口,这个接口只有一个onApplicationEvent()方法,该方法接受一个ApplicationEvent或其子类对象作为参数
    
*   在方法体中,可以通过不同对Event类的判断来进行相应的处理.当事件触发时所有的监听器都会收到消息,如果你需要对监听器的接收顺序有要求,可是实现该接口的一个实现`SmartApplicationListener`,通过这个接口可以指定监听器接收事件的顺序.
    
    ```
    @FunctionalInterface
    public interface ApplicationListener<E extends ApplicationEvent> extends EventListener {
        void onApplicationEvent(E var1);
    }
    ```
    
*   实现了ApplicationListener接口之后，需要实现方法onApplicationEvent()，在容器将所有的Bean都初始化完成之后，就会执行该方法。
    

**3) 事件源：ApplicationEventPublisher**

*   事件的发布者，封装了事件发布功能方法接口，是Applicationcontext接口的超类
    
    > 事件机制的实现需要三个部分,事件源,事件,事件监听器,在上面介绍的ApplicationEvent就相当于事件,ApplicationListener相当于事件监听器,这里的事件源说的就是ApplicationEventPublisher.
    
    ```
    public interface ApplicationEventPublisher {
        default void publishEvent(ApplicationEvent event) {
            this.publishEvent((Object)event);
        }
    	//调用publishEvent方法,传入一个ApplicationEvent的实现类对象作为参数,每当ApplicationContext发布ApplicationEvent时,所有的ApplicationListener就会被自动的触发.
        void publishEvent(Object var1);
    }
    ```
    
*   我们常用的`ApplicationContext`都继承了`AbstractApplicationContext`,像我们平时常见`ClassPathXmlApplicationContext`、`XmlWebApplicationContex`也都是继承了它,`AbstractApplicationcontext`是`ApplicationContext`接口的抽象实现类,在该类中实现了`publishEvent`方法:
    
    ```
       protected void publishEvent(Object event, @Nullable ResolvableType eventType) {
            Assert.notNull(event, "Event must not be null");
    
            if (this.earlyApplicationEvents != null) {
                this.earlyApplicationEvents.add(applicationEvent);
            } else {
              //事件发布委托给applicationEventMulticaster
              this.getApplicationEventMulticaster().multicastEvent((ApplicationEvent)applicationEvent, eventType);
            }
        }
    ```
    
    在这个方法中,我们看到了一个getApplicationEventMulticaster().这就要牵扯到另一个类ApplicationEventMulticaster.
    

**4) 事件管理：ApplicationEventMulticaster**

*   用于事件监听器的注册和事件的广播。监听器的注册就是通过它来实现的，它的作用是把 Applicationcontext 发布的 Event 广播给它的监听器列表。
    
    ```
    public interface ApplicationEventMulticaster {
        
        //添加事件监听器
        void addApplicationListener(ApplicationListener<?> var1);
    
        //添加事件监听器,使用容器中的bean
        void addApplicationListenerBean(String var1);
    
        //移除事件监听器
        void removeApplicationListener(ApplicationListener<?> var1);
    
        void removeApplicationListenerBean(String var1);
    
        //移除所有
        void removeAllListeners();
    
        //发布事件
        void multicastEvent(ApplicationEvent var1);
    
        void multicastEvent(ApplicationEvent var1, @Nullable ResolvableType var2);
    }
    ```
    
*   在AbstractApplicationcontext中有一个applicationEventMulticaster的成员变量,提供了监听器Listener的注册方法.
    
    ```
    public abstract class AbstractApplicationContext extends DefaultResourceLoader
            implements ConfigurableApplicationContext, DisposableBean {
    
    　　private ApplicationEventMulticaster applicationEventMulticaster;
        
    　　protected void registerListeners() {
            // Register statically specified listeners first.
            for (ApplicationListener<?> listener : getApplicationListeners()) {
                getApplicationEventMulticaster().addApplicationListener(listener);
            }
            // Do not initialize FactoryBeans here: We need to leave all regular beans
            // uninitialized to let post-processors apply to them!
            String[] listenerBeanNames = getBeanNamesForType(ApplicationListener.class, true, false);
            for (String lisName : listenerBeanNames) {
                getApplicationEventMulticaster().addApplicationListenerBean(lisName);
            }
        }
    }
    ```
    

### 3.3. 事件监听案例

实现一个需求：当调用一个类的方法完成时，该类发布事件，事件监听器监听该类的事件并执行的自己的方法逻辑

假设这个类是Request、发布的事件是ReuqestEvent、事件监听者是ReuqestListener。当调用Request的doRequest方法时，发布事件。

代码如下

```
/**
 * 定义事件
 * @date 2022/10/24
 **/
public class RequestEvent  extends ApplicationEvent {

    public RequestEvent(Object source) {
        super(source);
    }
}

/**
 * 发布事件
 * @date 2022/10/24
 **/
@Component
public class Request {

    @Autowired
    private ApplicationContext applicationContext;

    public void doRequest(){
        System.out.println("调用Request类的doRequest方法发送一个请求......");
        applicationContext.publishEvent(new RequestEvent(this));
    }
}

/**
 * 监听事件
 * @date 2022/10/24
 **/
@Component
public class RequestListener implements ApplicationListener<RequestEvent> {

    @Override
    public void onApplicationEvent(RequestEvent requestEvent) {
        System.out.println("监听到RequestEvent事件,执行本方法");
    }
}

public class SpringEventTest {

    public static void main(String[] args) {
        ApplicationContext context =
                new AnnotationConfigApplicationContext("com.xfc.pubsub");

        Request request = (Request) context.getBean("request");

        //调用方法发布事件
        request.doRequest();
    }
}

//打印日志
调用Request类的doRequest方法发送一个请求......
监听到RequestEvent事件,执行本方法
```

### 3.4. 事件机制工作流程

上面代码的执行流程

![Image 4: 146.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/faf169a2458842bfa6f7b076b334d24f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=bm7dAstLfqUwi7XNi0unBzFmKRE%3D)

1.  监听器什么时候注册到IOC容器
    
    注册的开始逻辑是在AbstractApplicationContext类的refresh方法，该方法包含了整个IOC容器初始化所有方法。其中有一个registerListeners()方法就是注册系统监听者(spring自带的)和自定义监听器的。
    
    ```
    public void refresh() throws BeansException, IllegalStateException {
        			//BeanFactory准备工作完成后进行的后置处理工作
                    this.postProcessBeanFactory(beanFactory);
        
        			//执行BeanFactoryPostProcessor的方法；
                    this.invokeBeanFactoryPostProcessors(beanFactory);
        
        			//注册BeanPostProcessor（Bean的后置处理器），在创建bean的前后等执行
                    this.registerBeanPostProcessors(beanFactory);
        	
        			//初始化MessageSource组件（做国际化功能；消息绑定，消息解析）；
                    this.initMessageSource();
        
        			//初始化事件派发器
                    this.initApplicationEventMulticaster();
        
        			////子类重写这个方法，在容器刷新的时候可以自定义逻辑；如创建Tomcat，Jetty等WEB服务器
                    this.onRefresh();
        
                        //注册应用的监听器。就是注册实现了ApplicationListener接口的监听器bean，这些监听器是注册到ApplicationEventMulticaster中的
                    this.registerListeners();
        
        			//初始化所有剩下的非懒加载的单例bean
                    this.finishBeanFactoryInitialization(beanFactory);
        
        			//完成context的刷新
                    this.finishRefresh();
        }
    ```
    
    看registerListeners的关键方法体，其中的两个方法`addApplicationListener和addApplicationListenerBean`，从方法可以看出是添加监听者。
    
    ```
    protected void registerListeners() {
        Iterator var1 = this.getApplicationListeners().iterator();
    
        while(var1.hasNext()) {
            ApplicationListener<?> listener = (ApplicationListener)var1.next();
            this.getApplicationEventMulticaster().addApplicationListener(listener);
        }
    
        String[] listenerBeanNames = this.getBeanNamesForType(ApplicationListener.class, true, false);
        String[] var7 = listenerBeanNames;
        int var3 = listenerBeanNames.length;
    
        for(int var4 = 0; var4 < var3; ++var4) {
            String listenerBeanName = var7[var4];
            this.getApplicationEventMulticaster().addApplicationListenerBean(listenerBeanName);
        }
    }
    ```
    
    那么最后将监听者放到哪里了呢？就是ApplicationEventMulticaster接口的子类
    

![Image 5: 135.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1a54e00b4fff437e8232fc2f39a040c3~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=xS4qiYxLC6Hj6JhjDb3Jj0MPtVU%3D)

该接口主要两个职责，维护ApplicationListener相关类和发布事件。

实现在默认实现类AbstractApplicationEventMulticaster，`最后将Listener放到了内部类ListenerRetriever两个set集合中`

```
private class ListenerRetriever {
        public final Set<ApplicationListener<?>> applicationListeners = new LinkedHashSet();
        public final Set<String> applicationListenerBeans = new LinkedHashSet();
}
```

ListenerRetriever被称为监听器注册表。

2.  Spring如何发布的事件并通知监听者
    
    **这个注意的有两个方法**
    
    **1) publishEvent方法**
    
    *   `AbstractApplicationContext`实现了`ApplicationEventPublisher` 接口的`publishEvent`方法
    
    ```
    protected void publishEvent(Object event, @Nullable ResolvableType eventType) {
        Assert.notNull(event, "Event must not be null");
        Object applicationEvent;
        
        //尝试转换为ApplicationEvent或者PayloadApplicationEvent，如果是PayloadApplicationEvent则获取eventType
        if (event instanceof ApplicationEvent) {
            applicationEvent = (ApplicationEvent)event;
        } else {
            applicationEvent = new PayloadApplicationEvent(this, event);
            if (eventType == null) {
                eventType = ((PayloadApplicationEvent)applicationEvent).getResolvableType();
            }
        }
    
       
        if (this.earlyApplicationEvents != null) {
             //判断earlyApplicationEvents是否为空(也就是早期事件还没有被发布-说明广播器还没有实例化好)，如果不为空则将当前事件放入集合
            this.earlyApplicationEvents.add(applicationEvent);
        } else {
            //否则获取ApplicationEventMulticaster调用其multicastEvent将事件广播出去。本文这里获取到的广播器实例是SimpleApplicationEventMulticaster。
            this.getApplicationEventMulticaster().multicastEvent((ApplicationEvent)applicationEvent, eventType);
        }
    	
        //将事件交给父类处理
        if (this.parent != null) {
            if (this.parent instanceof AbstractApplicationContext) {
                ((AbstractApplicationContext)this.parent).publishEvent(event, eventType);
            } else {
                this.parent.publishEvent(event);
            }
        }
    
    }
    ```
    
    **2) multicastEvent方法**
    
    继续进入到`multicastEvent方法`，该方法有两种方式调用invokeListener，通过线程池和直接调用，进一步说就是通过异步和同步两种方式调用.
    
    ```
    public void multicastEvent(ApplicationEvent event, @Nullable ResolvableType eventType) {
        
        //解析事件类型
        ResolvableType type = eventType != null ? eventType : this.resolveDefaultEventType(event);
        
        //获取执行器
        Executor executor = this.getTaskExecutor();
        
        // 获取合适的ApplicationListener，循环调用监听器的onApplicationEvent方法
        Iterator var5 = this.getApplicationListeners(event, type).iterator();
    
        while(var5.hasNext()) {
            ApplicationListener<?> listener = (ApplicationListener)var5.next();
            if (executor != null) {
                //如果executor不为null，则交给executor去调用监听器
                executor.execute(() -> {
                    this.invokeListener(listener, event);
                });
            } else {
                //否则，使用当前主线程直接调用监听器；
                this.invokeListener(listener, event);
            }
        }
    
    }
    ```
    
    **3) invokeListener方法**
    
    ```
    // 该方法增加了错误处理逻辑，然后调用doInvokeListener
    protected void invokeListener(ApplicationListener<?> listener, ApplicationEvent event) {
        ErrorHandler errorHandler = this.getErrorHandler();
        if (errorHandler != null) {
            try {
                this.doInvokeListener(listener, event);
            } catch (Throwable var5) {
                errorHandler.handleError(var5);
            }
        } else {
            this.doInvokeListener(listener, event);
        }
    ​
    }
    ​
    private void doInvokeListener(ApplicationListener listener, ApplicationEvent event) {
        //直接调用了listener接口的onApplicationEvent方法
        listener.onApplicationEvent(event);  
    }
    ```
    

4\. 结合设计模式自定义SpringIOC
----------------------

### 4.1. Spring IOC核心组件

**1) BeanFactory**

BeanFactory作为最顶层的一个接口，定义了IoC容器的基本功能规范

![Image 6: 137.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/57fa057139464cf6888011cecdec7c3a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=jOKVvB9xLCqIILeQjq13awTXNao%3D)

从类图中我们可以发现最终的默认实现类是DefaultListableBeanFactory，它实现了所有的接口。那么为何要定义这么多层次的接口呢？ 每个接口都有它的使用场合，主要是为了区分在Spring内部操作过程中对象的传递和转化，对对象的数据访问所做的限制。

例如，

*   ListableBeanFactory接口表示这些Bean可列表化。
*   HierarchicalBeanFactory表示这些Bean 是有继承关系的，也就是每个 Bean 可能有父 Bean
*   AutowireCapableBeanFactory 接口定义Bean的自动装配规则。

这三个接口共同定义了Bean的集合、Bean之间的关系及Bean行为。

在BeanFactory里只对IoC容器的基本行为做了定义，根本不关心你的Bean是如何定义及怎样加载的。正如我们只关心能从工厂里得到什么产品，不关心工厂是怎么生产这些产品的。

**2 ) ApplicationContext**

BeanFactory有一个很重要的子接口，就是ApplicationContext接口，该接口主要来规范容器中的bean对象是非延时加载，即在创建容器对象的时候就对象bean进行初始化，并存储到一个容器中。

```
//延时加载
BeanFactory factory = new XmlBeanFactory(new ClassPathResource("bean.xml"));

//立即加载
ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("bean.xml");
User user = context.getBean("user", User.class);
```

ApplicationContext 的子类主要包含两个方面：

*   `ConfigurableApplicationContext` 表示该 Context 是可修改的，也就是在构建 Context 中用户可以动态添加或修改已有的配置信息
*   `WebApplicationContext` 顾名思义，就是为 web 准备的 Context 他可以直接访问到 ServletContext，通常情况下，这个接口使用少

要知道工厂是如何产生对象的，我们需要看具体的IoC容器实现，Spring提供了许多IoC容器实现，比如：

*   `ClasspathXmlApplicationContext` : 根据类路径加载xml配置文件，并创建IOC容器对象。
*   `FileSystemXmlApplicationContext` ：根据系统路径加载xml配置文件，并创建IOC容器对象。
*   `AnnotationConfigApplicationContext` ：加载注解类配置，并创建IOC容器。

![Image 7: 138.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/81ffae0f86ff497e881c6d1070aef63e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=sl1ufx7aPaGakqWxoWOYHYSizTY%3D)

总体来说 ApplicationContext 必须要完成以下几件事：

*   标识一个应用环境
*   利用 BeanFactory 创建 Bean 对象
*   保存对象关系表
*   能够捕获各种事件

**3) Bean定义：BeanDefinition**

这里的 BeanDefinition 就是我们所说的 Spring 的 Bean，我们自己定义的各个 Bean 其实会转换成一个个 BeanDefinition 存在于 Spring 的 BeanFactory 中

```
public class DefaultListableBeanFactory extends AbstractAutowireCapableBeanFactory
        implements ConfigurableListableBeanFactory, BeanDefinitionRegistry, Serializable {
	//DefaultListableBeanFactory 中使用 Map 结构保存所有的 BeanDefinition 信息
    private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256); 
}   
```

**BeanDefinition** 中保存了我们的 Bean 信息，比如这个 Bean 指向的是哪个类、是否是单例的、是否懒加载、这个 Bean 依赖了哪些 Bean 等等。

**4) BeanDefinitionReader**

Bean的解析过程非常复杂，功能被分得很细，因为这里需要被扩展的地方很多，必须保证足够的灵活性，以应对可能的变化。Bean的解析主要就是对Spring配置文件的解析。

这个解析过程主要通过BeanDefinitionReader来完成，看看Spring中BeanDefinitionReader的类结构图，如下图所示。

![Image 8: 140.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/98e678faf8c943e0a070afc024b58403~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=M4mES34%2FMCM4ieBwrg9aOuba7wA%3D)

BeanDefinitionReader接口定义的功能

```
public interface BeanDefinitionReader {

	/*
		下面的loadBeanDefinitions都是加载bean定义，从指定的资源中
	*/
	int loadBeanDefinitions(Resource resource) throws BeanDefinitionStoreException;
	int loadBeanDefinitions(Resource... resources) throws BeanDefinitionStoreException;
	int loadBeanDefinitions(String location) throws BeanDefinitionStoreException;
	int loadBeanDefinitions(String... locations) throws BeanDefinitionStoreException;
}
```

**5) BeanFactory后置处理器**

后置处理器是一种拓展机制，贯穿Spring Bean的生命周期

后置处理器分为两类：

**BeanFactory后置处理器：BeanFactoryPostProcessor**

实现该接口，可以在spring的bean创建之前，修改bean的定义属性

![Image 9: 141.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ee8677ca0274492890ef2f778a37f55f~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=g4W6J1wCoNM5RqIIktpmg%2FGdqPM%3D)

```
public interface BeanFactoryPostProcessor {

    /*
     *  该接口只有一个方法postProcessBeanFactory，方法参数是ConfigurableListableBeanFactory，通过该
        参数，可以获取BeanDefinition
    */
    void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException;
}
```

**6) Bean后置处理器：BeanPostProcessor**

BeanPostProcessor是Spring IOC容器给我们提供的一个扩展接口

实现该接口，可以在spring容器实例化bean之后，在执行bean的初始化方法前后，添加一些处理逻辑

![Image 10: ec51548d8fd231991a603771a114b7ed.jpeg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e628653380d2417184013e92efc9dcd1~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=qcDfGoHXvfmx846lkl7cva8icjw%3D)

```
public interface BeanPostProcessor {
    //bean初始化方法调用前被调用
    Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException;
    //bean初始化方法调用后被调用
    Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException;
}
```

### 4.2. IOC流程图

![Image 11: d09e79e71bb191a06aba33c59dacd5d0.jpeg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f5b3e98cbc774037a058a17f895fedc6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=%2Fk6FyL%2BUsiwIX9tIrvYhEir%2FSGo%3D)

1.  容器环境的初始化(系统、JVM 、解析器、类加载器等等)
2.  Bean工厂的初始化(IOC容器首先会销毁旧工厂,旧Bean、创建新的工厂)
3.  读取：通过BeanDefinitonReader读取我们项目中的配置（application.xml）
4.  定义：通过解析xml文件内容，将里面的Bean解析成BeanDefinition（未实例化、未初始化）
5.  将解析得到的BeanDefinition,存储到工厂类的Map容器中
6.  调用 BeanFactoryPostProcessor 该方法是一种功能增强，可以在这个步骤对已经完成初始化的 BeanFactory 进行属性覆盖，或是修改已经注册到 BeanFactory 的 BeanDefinition
7.  通过反射实例化bean对象
8.  进入到Bean实例化流程,首先设置对象属性
9.  检查Aware相关接口,并设置相关依赖
10.  前置处理器,执行BeanPostProcesser的before方法对bean进行扩展
11.  检查是否有实现initializingBean 回调接口,如果实现就要回调其中的AftpropertiesSet() 方法,(通过可以完成一些配置的加载)
12.  检查是否有配置自定义的init-method ,
13.  后置处理器执行BeanPostProcesser 的after方法 --\> AOP就是在这个阶段完成的, 在这里判断bean对象是否实现接口,实现就使用JDK代理,否则选择CGLIB
14.  对象创建完成,添加到BeanFactory的单例池中

### 4.3. 自定义SpringIOC

对下面的配置文件进行解析，并自定义SpringIOC, 对涉及到的对象进行管理。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans>
    <bean id="courseService" class="com.xfc.service.impl.CourseServiceImpl">
        <property name="courseDao" ref="courseDao"></property>
    </bean>
    <bean id="courseDao" class="com.xfc.dao.impl.CourseDaoImpl"></bean>
</beans>
```

1.  创建与Bean相关的pojo类

*   **PropertyValue类**: 用于封装bean的属性，体现到上面的配置文件就是封装bean标签的子标签property标签数据。

```
package com.xfc.framework.beans;

/**
 * 该类用来封装bean标签下的property子标签的属性
 *      1.name属性
 *      2.ref属性
 *      3.value属性: 给基本数据类型及string类型数据赋的值
 * @date 2022/10/26
 **/
public class PropertyValue {

    private String name;

    private String ref;

    private String value;

    public PropertyValue() {
    }

    public PropertyValue(String name, String ref, String value) {
        this.name = name;
        this.ref = ref;
        this.value = value;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRef() {
        return ref;
    }

    public void setRef(String ref) {
        this.ref = ref;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
```

*   **MutablePropertyValues类**: 一个bean标签可以有多个property子标签，所以再定义一个MutablePropertyValues类，用来存储并管理多个PropertyValue对象。

```
package com.xfc.framework.beans;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

/**
 * 该类用来存储和遍历多个PropertyValue对象
 * @date 2022/10/26
 **/
public class MutablePropertyValues implements Iterable<PropertyValue>{

    //定义List集合,存储PropertyValue的容器
    private final List<PropertyValue> propertyValueList;

    //空参构造中 初始化一个list
    public MutablePropertyValues() {
        this.propertyValueList = new ArrayList<PropertyValue>();
    }

    //有参构造 接收一个外部传入的list,赋值propertyValueList属性
    public MutablePropertyValues(List<PropertyValue> propertyValueList) {
        if(propertyValueList == null){
            this.propertyValueList = new ArrayList<PropertyValue>();
        }else{
            this.propertyValueList = propertyValueList;
        }
    }

    //获取当前容器对应的迭代器对象
    @Override
    public Iterator<PropertyValue> iterator() {

        //直接获取List集合中的迭代器
        return propertyValueList.iterator();
    }

    //获取所有的PropertyValue
    public PropertyValue[] getPropertyValues(){
        //将集合转换为数组并返回
        return propertyValueList.toArray(new PropertyValue[0]); //new PropertyValue[0]声明返回的数组类型
    }

    //根据name属性值获取PropertyValue
    public PropertyValue getPropertyValue(String propertyName){
        //遍历集合对象
        for (PropertyValue propertyValue : propertyValueList) {
            if(propertyValue.getName().equals(propertyName)){
                return propertyValue;
            }
        }

        return null;
    }

    //判断集合是否为空,是否存储PropertyValue
    public boolean isEmpty(){
        return propertyValueList.isEmpty();
    }

    //向集合中添加
    public MutablePropertyValues addPropertyValue(PropertyValue value){
        //判断集合中存储的propertyvalue对象.是否重复,重复就进行覆盖
        for (int i = 0; i < propertyValueList.size(); i++) {
            //获取集合中每一个 PropertyValue
            PropertyValue currentPv = propertyValueList.get(i);

            //判断当前的pv的name属性 是否与传入的相同,如果相同就覆盖
            if(currentPv.getName().equals(value.getName())){
                propertyValueList.set(i,value);
                return this;
            }
        }

        //没有重复
        this.propertyValueList.add(value);
        return this;  //目的是实现链式编程
    }

    //判断是否有指定name属性值的对象
    public boolean contains(String propertyName){
        return getPropertyValue(propertyName) != null;
    }
}
```

*   **BeanDefinition类**: 用来封装bean信息的，主要包含id（即bean对象的名称）、class（需要交由spring管理的类的全类名）及子标签property数据。

```
/**
 * 封装Bean标签数据的类,包括id与class以及子标签的数据
 * @date 2022/10/27
 **/
public class BeanDefinition {

    private String id;

    private String className;

    private MutablePropertyValues propertyValues;

    public BeanDefinition() {
        propertyValues = new MutablePropertyValues();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public MutablePropertyValues getPropertyValues() {
        return propertyValues;
    }

    public void setPropertyValues(MutablePropertyValues propertyValues) {
        this.propertyValues = propertyValues;
    }
}
```

2.  创建注册表相关的类

BeanDefinition对象存取的操作, 其实是在BeanDefinitionRegistry接口中定义的,它被称为是BeanDefinition的注册中心.

```
//源码
public interface BeanDefinitionRegistry extends AliasRegistry {

	void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
			throws BeanDefinitionStoreException;

	void removeBeanDefinition(String beanName) throws NoSuchBeanDefinitionException;

	BeanDefinition getBeanDefinition(String beanName) throws NoSuchBeanDefinitionException;

	boolean containsBeanDefinition(String beanName);

	String[] getBeanDefinitionNames();
    
	int getBeanDefinitionCount();
    
	boolean isBeanNameInUse(String beanName);
}
```

BeanDefinitionRegistry继承结构图如下：

![Image 12: 03eeed0e1ed0cd0c2b5a96ab87ed344e.jpeg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ba2a462cf1b0425a9577de1b16fd99da~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=%2FvJAL4MN9IUwdVvpZ7FvxBfx63k%3D)

BeanDefinitionRegistry接口的子实现类主要有以下两个：

*   DefaultListableBeanFactory
    
    在该类中定义了如下代码，就是用来注册bean
    
    ```
    private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(256);
    ```
    
*   SimpleBeanDefinitionRegistry
    
    在该类中定义了如下代码，就是用来注册bean
    
    ```
    private final Map<String, BeanDefinition> beanDefinitionMap = new ConcurrentHashMap<>(64);
    ```
    

*   自定义BeanDefinitionRegistry接口定义了注册表的相关操作，定义如下功能：

```
public interface BeanDefinitionRegistry {

    //注册BeanDefinition对象到注册表中
    void registerBeanDefinition(String beanName, BeanDefinition beanDefinition);

    //从注册表中删除指定名称的BeanDefinition对象
    void removeBeanDefinition(String beanName) throws Exception;

    //根据名称从注册表中获取BeanDefinition对象
    BeanDefinition getBeanDefinition(String beanName) throws Exception;

    //判断注册表中是否包含指定名称的BeanDefinition对象
    boolean containsBeanDefinition(String beanName);

    //获取注册表中BeanDefinition对象的个数
    int getBeanDefinitionCount();

    //获取注册表中所有的BeanDefinition的名称
    String[] getBeanDefinitionNames();
}
```

*   SimpleBeanDefinitionRegistry类, 该类实现了BeanDefinitionRegistry接口，定义了Map集合作为注册表容器。

```
public class SimpleBeanDefinitionRegistry implements BeanDefinitionRegistry {
​
    private Map<String, BeanDefinition> beanDefinitionMap = new HashMap<String, BeanDefinition>();

    @Override
    public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition) {
        beanDefinitionMap.put(beanName,beanDefinition);
    }

    @Override
    public void removeBeanDefinition(String beanName) throws Exception {
        beanDefinitionMap.remove(beanName);
    }

    @Override
    public BeanDefinition getBeanDefinition(String beanName) throws Exception {
        return beanDefinitionMap.get(beanName);
    }

    @Override
    public boolean containsBeanDefinition(String beanName) {
        return beanDefinitionMap.containsKey(beanName);
    }

    @Override
    public int getBeanDefinitionCount() {
        return beanDefinitionMap.size();
    }

    @Override
    public String[] getBeanDefinitionNames() {
        return beanDefinitionMap.keySet().toArray(new String[1]);
    }
}
```

3.  创建解析器相关的类

BeanDefinitionReader接口

*   BeanDefinitionReader用来解析配置文件并在注册表中注册bean的信息。定义了两个规范：
    
*   获取注册表的功能,让外界可以通过该对象获取注册表对象
    
*   加载配置文件,并注册bean数据
    

```
/**
 * @date 2022/10/28
 **/
public interface BeanDefinitionReader {

    //获取注册表对象
    BeanDefinitionRegistry getRegistry();

    //加载配置文件并在注册表中进行注册
    void loadBeanDefinitions(String configLocation) throws Exception;
}
```

XmlBeanDefinitionReader类

*   XmlBeanDefinitionReader是专门用来解析xml配置文件的。该类实现BeanDefinitionReader接口并实现接口中的两个功能。

```
/**
 * 该类是对XML文件进行解析的类
 * @date 2022/10/28
 **/
public class XmlBeanDefinitionReader implements BeanDefinitionReader {

    //声明注册表对象(将配置文件与注册表解耦,通过Reader降低耦合性)
    private BeanDefinitionRegistry registry;

    public XmlBeanDefinitionReader() {
        registry = new SimpleBeanDefinitionRegistry();
    }

    @Override
    public BeanDefinitionRegistry getRegistry() {
        return registry;
    }

    //加载配置文件
    @Override
    public void loadBeanDefinitions(String configLocation) throws Exception {
        //使用dom4j解析xml
        SAXReader reader = new SAXReader();

        //获取配置文件,类路径下
        InputStream is = XmlBeanDefinitionReader.class.getClassLoader().getResourceAsStream(configLocation);

        //获取document文档对象
        Document document = reader.read(is);

        Element rootElement = document.getRootElement();
        //解析bean标签
        parseBean(rootElement);
    }

    private void parseBean(Element rootElement) {

        //获取所有的bean标签
        List<Element> elements = rootElement.elements();

        //遍历获取每个bean标签的属性值和子标签property
        for (Element element : elements) {

            String id = element.attributeValue("id");
            String className = element.attributeValue("class");

            //封装到beanDefinition
            BeanDefinition beanDefinition = new BeanDefinition();
            beanDefinition.setId(id);
            beanDefinition.setClassName(className);

            //获取property
            List<Element> list = element.elements("property");

            MutablePropertyValues mutablePropertyValues = new MutablePropertyValues();

            //遍历,封装propertyValue,并保存到mutablePropertyValues
            for (Element element1 : list) {
                String name = element1.attributeValue("name");
                String ref = element1.attributeValue("ref");
                String value = element1.attributeValue("value");
                PropertyValue propertyValue = new PropertyValue(name,ref,value);
                mutablePropertyValues.addPropertyValue(propertyValue);
            }

            //将mutablePropertyValues封装到beanDefinition
            beanDefinition.setPropertyValues(mutablePropertyValues);

            System.out.println(beanDefinition);
            //将beanDefinition注册到注册表
            registry.registerBeanDefinition(id,beanDefinition);
        }
    }
}
```

4.  创建IOC容器相关的类

**1) BeanFactory接口**

在该接口中定义IOC容器的统一规范和获取bean对象的方法。

```
/**
 * IOC容器父接口
 * @date 2022/10/28
 **/
public interface BeanFactory {

    Object getBean(String name)throws Exception;

    //泛型方法,传入当前类或者其子类
    <T> T getBean(String name ,Class<? extends T> clazz)throws Exception;
}

```

**2) ApplicationContext接口**

该接口的所有的子实现类对bean对象的创建都是非延时的，所以在该接口中定义 `refresh()` 方法，该方法主要完成以下两个功能：

*   加载配置文件。
*   根据注册表中的BeanDefinition对象封装的数据进行bean对象的创建。

```
/**
 * 定义非延时加载功能
 * @date 2022/10/28
 **/
public interface ApplicationContext extends BeanFactory {

    //进行配置文件加载,并进行对象创建
    void refresh();
}
```

**3) AbstractApplicationContext类**

*   作为ApplicationContext接口的子类，所以该类也是非延时加载，所以需要在该类中定义一个Map集合，作为bean对象存储的容器。
*   声明BeanDefinitionReader类型的变量，用来进行xml配置文件的解析，符合单一职责原则。
*   BeanDefinitionReader类型的对象创建交由子类实现，因为只有子类明确到底创建BeanDefinitionReader哪儿个子实现类对象。

```
/**
 * ApplicationContext接口的子实现类
 *      创建容器对象时,加载配置文件,对bean进行初始化
 * @date 2022/10/28
 **/
public abstract class AbstractApplicationContext implements ApplicationContext {

    //声明解析器变量
    protected BeanDefinitionReader beanDefinitionReader;

    //定义存储bean对象的Map集合
    protected Map<String,Object> singletonObjects = new HashMap<>();

    //声明配置文件类路径的变量
    protected String configLocation;

    @Override
    public void refresh() {

        //加载beanDefinition对象
        try {
            beanDefinitionReader.loadBeanDefinitions(configLocation);
            //初始化bean
            finishBeanInitialization();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    //bean初始化
    protected  void finishBeanInitialization() throws Exception {
        //获取对应的注册表对象
        BeanDefinitionRegistry registry = beanDefinitionReader.getRegistry();

        //获取beanDefinition对象
        String[] beanNames = registry.getBeanDefinitionNames();
        for (String beanName : beanNames) {
            //进行bean的初始化
            getBean(beanName);
        }
    };
}
```

**4) ClassPathXmlApplicationContext类**

该类主要是加载类路径下的配置文件，并进行bean对象的创建，主要完成以下功能：

*   在构造方法中，创建BeanDefinitionReader对象。
*   在构造方法中，调用refresh()方法，用于进行配置文件加载、创建bean对象并存储到容器中。
*   重写父接口中的getBean()方法，并实现依赖注入操作。

```
/**
 * IOC容器具体的子实现类,加载XML格式配置文件
 * @date 2022/10/28
 **/
public class ClassPathXmlApplicationContext extends AbstractApplicationContext{

    public ClassPathXmlApplicationContext(String configLocation) {
        this.configLocation = configLocation;
        //构建解析器对象
        this.beanDefinitionReader = new XmlBeanDefinitionReader();

        this.refresh();
    }

    //跟据bean的对象名称获取bean对象
    @Override
    public Object getBean(String name) throws Exception {
        //判断对象容器中是否包含指定名称的bean对象,如果包含就返回,否则自行创建
        Object obj = singletonObjects.get(name);
        if(obj != null){
            return obj;
        }

        //自行创建,获取beanDefinition对象
        BeanDefinitionRegistry registry = beanDefinitionReader.getRegistry();
        BeanDefinition beanDefinition = registry.getBeanDefinition(name);

        //通过反射创建对象
        String className = beanDefinition.getClassName();
        Class<?> clazz = Class.forName(className);
        Object beanObj = clazz.newInstance();

        //CourseService与UserDao存依赖,所以要将UserDao一同初始化,进行依赖注入
        MutablePropertyValues propertyValues = beanDefinition.getPropertyValues();
        for (PropertyValue propertyValue : propertyValues) {
            //获取name属性值
            String propertyName = propertyValue.getName();
            //获取Value属性
            String value = propertyValue.getValue();
            //获取ref属性
            String ref = propertyValue.getRef();

            //ref与value只能存在一个
            if(ref != null && !"".equals(ref)){
                //获取依赖的bean对象,拼接set set+Course
                Object bean = getBean(ref);
                String methodName = StringUtils.getSetterMethodFieldName(propertyName);

                //获取所有方法对象
                Method[] methods = clazz.getMethods();
                for (Method method : methods) {
                    if(methodName.equals(method.getName())){
                        //执行该set方法
                        method.invoke(beanObj,bean);
                    }
                }
            }

            if(value != null && !"".equals(value)){
                String methodName = StringUtils.getSetterMethodFieldName(propertyName);
                //获取method
                Method method = clazz.getMethod(methodName, String.class);
                method.invoke(beanObj,value);
            }
        }

        //在返回beanObj之前 ,需要将对象存储到Map容器中
        this.singletonObjects.put(name,beanObj);


        return beanObj;
    }

    @Override
    public <T> T getBean(String name, Class<? extends T> clazz) throws Exception {
        Object bean = getBean(name);
        if(bean == null){
            return null;
        }

       return clazz.cast(bean);
    }
}
```

5.  自定义IOC容器测试

第一步: 将我们写好的自定义IOC容器项目,安装到maven仓库中,使其他项目可以引入其依赖

```
//依赖信息
<dependencies>
    <dependency>
        <groupId>com.xfc</groupId>
        <artifactId>user_defined_springioc</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>
</dependencies>
```

第二步: 完成代码编写

*   dao

```
public interface CourseDao {
    public void add();
}

public class CourseDaoImpl implements CourseDao {

    //value注入
    private String courseName;

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public CourseDaoImpl() {
        System.out.println("CourseDaoImpl创建了......");
    }

    @Override
    public void add() {
        System.out.println("CourseDaoImpl的add方法执行了......" + courseName);
    }
}
```

*   service

```
public interface CourseService {

    public void add();
}

public class CourseServiceImpl implements CourseService {

    public CourseServiceImpl() {
        System.out.println("CourseServiceImpl创建了......");
    }

    private CourseDao courseDao;

    public void setCourseDao(CourseDao courseDao) {
        this.courseDao = courseDao;
    }

    @Override
    public void add() {
        System.out.println("CourseServiceImpl的add方法执行了......");
        courseDao.add();
    }
}
```

*   applicationContext.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans>
    <bean id="courseService" class="com.xfc.test_springioc.service.impl.CourseServiceImpl">
        <property name="courseDao" ref="courseDao"></property>
    </bean>
    <bean id="courseDao" class="com.xfc.test_springioc.dao.impl.CourseDaoImpl">
        <property name="courseName" value="java"></property>
    </bean>
</beans>
```

*   Controller

```
public class CourseController{

    public static void main(String[] args) {
        //1.创建Spring的容器对象
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");

        //2.从容器对象中获取CourseService对象
        CourseService courseService = context.getBean("courseService", CourseService.class);

        //3.调用UserService的add方法
        courseService.add();
    }
}
```

6.  案例中使用到的设计模式

*   `工厂模式`。这个使用工厂模式 + 配置文件的方式。
*   ` 单例模式`。Spring IOC管理的bean对象都是单例的，此处的单例不是通过构造器进行单例的控制的，而是spring框架对每一个bean只创建了一个对象。
*   `模板方法模式`。AbstractApplicationContext类中的finishBeanInitialization()方法调用了子类的getBean()方法，因为getBean()的实现和环境息息相关。
*   `迭代器模式`。对于MutablePropertyValues类定义使用到了迭代器模式，因为此类存储并管理PropertyValue对象，也属于一个容器，所以给该容器提供一个遍历方式。

5\. 结语
------

通过本文的分析，我们可以看到，Spring框架的设计充分利用了多种设计模式，尤其是工厂模式，不仅加强了框架的灵活性和扩展性，也极大地提升了代码的可重用性和可维护性。Spring通过其IOC容器，利用工厂模式等设计模式自动管理对象的生命周期和依赖关系，极大地解放了开发者从繁琐的配置管理任务中。掌握这些设计模式并理解它们在Spring中的应用，将帮助开发者更加高效地使用Spring框架，从而开发出响应快速、易于维护的应用。

![Image 13: 结语3.jpg](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d29fa6da61484904aabccf80cb0f1f07~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZCO56uv5bCP6IKl6IKg:q75.awebp?rk3s=f64ab15b&x-expires=1729397151&x-signature=BzB2%2BuzU%2FN%2B%2BqZI2VpMoGpxWO18%3D)
