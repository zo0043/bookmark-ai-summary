Title: 如何理解 Spring 当中的 Bean？ - 知乎

URL Source: https://www.zhihu.com/question/47220912

Markdown Content:
1\. spring容器就是个hashmap

2\. 前置处理器就是准备好实例化类的条件

3\. 后置处理器就是把类按第2步的条件实例化以后放进hashmap，name或者你指定的名字是key，实例就是value。这个value也就是实例，就是你问的bean，跟你手动new出来的没有本质区别

4\. 依赖注入就是把hashmap里的类实例用name拿出来用

5\. aop就是允许在hashmap里面的实例使用的时候，在方法开始，进行，结束的时间点上搞一个回调函数

6\. 自定义starter就是在springBootApplication实例化的时候把指定目录下配置的类也放到前置处理器等待实例化

7\. 所谓观察者模式

首先你要先理解POJO, POJO（Plain Old Java Object，普通Java对象）是指一个简单的Java对象，不继承任何特殊的Java类，也不实现任何特殊的Java接口。POJO通常用来表示应用程序中的数据模型或业务逻辑。与其他Java组件相比，POJO具有以下特点和优势：

1.  简单性：POJO类通常具有简单的结构，只包含属性（成员变量）和相应的getter/setter方法。这使得POJO类容易理解和维护。
2.  松耦合：由于POJO类不依赖于特定的框架或库，因此它们可以在不同的环境中使用，实现了高度解耦。
3.  可测试性：POJO类的简单性和松耦合特点使得它们更容易进行单元测试。你可以独立于其
