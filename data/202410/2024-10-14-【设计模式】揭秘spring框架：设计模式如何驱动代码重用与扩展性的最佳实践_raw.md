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

    public static 
```
