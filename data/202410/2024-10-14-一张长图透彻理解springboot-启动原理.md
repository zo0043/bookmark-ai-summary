# 一张长图透彻理解SpringBoot 启动原理
- URL: https://juejin.cn/post/7308610896803659812
- Added At: 2024-10-14 16:59:02
- [Link To Text](2024-10-14-一张长图透彻理解springboot-启动原理_raw.md)

## TL;DR
文章深入剖析SpringBoot启动原理，强调其对开发者的重要性，通过实际案例和源码解析，阐述Spring启动过程及扩展点执行顺序，解答常见问题，建议合理时机开启流量入口，提升应用稳定性。

## Summary
1. **SpringBoot启动原理的重要性**：文章强调了深入理解SpringBoot启动原理对于Java程序员和架构师的重要性，尤其是在集成中间件和框架时。

2. **流量入口问题**：文章指出，SpringBoot项目常见的流量入口包括Rpc、Http、MQ三种方式，并强调了正确开启流量入口的重要性。

3. **线上故障案例**：文章通过实际线上故障案例，说明了错误开启MQ流量导致的Spring未启动完成的问题。

4. **深入理解Spring启动原理的重要性**：文章通过11个问题，进一步阐述了深入理解Spring启动原理的重要性。

5. **Spring启动过程的扩展点**：文章列举了与Spring启动过程相关的扩展点，包括BeanFactoryAware、ApplicationContextAware、BeanNameAware、ApplicationListener、CommandLineRunner、SmartLifecycle、@PostConstruct、InitializingBean、init-method、Configuration配置类、BeanPostProcessor、BeanFactoryPostProcessor等。

6. **通过打印日志学习Spring的执行顺序**：文章通过代码实验，验证了以上扩展点的执行顺序，并通过日志输出了实际的执行顺序。

7. **实例化和初始化的区别**：文章解释了实例化和初始化的区别，并指出new创建对象实例为实例化，而执行init-method等方法为初始化。

8. **Spring重要扩展点的启动顺序**：文章详细介绍了Spring重要扩展点的启动顺序，包括BeanFactoryPostProcessor、实例化Bean、Autowired装配依赖、BeanNameAware、BeanFactoryAware、ApplicationContextAware、BeanPostProcessor、PostConstruct、InitializingBean、init-method、BeanPostProcessor、其他Bean实例化和初始化、所有单例Bean初始化完成后、SmartInitializingSingleton、SmartLifecyle smart start方法、发布ContextRefreshedEvent方法、注册和初始化Spring MVC、Tomcat/Jetty容器开启端口、应用启动完成后执行CommandLineRunner等。

9. **关于Spring启动原理的若干问题**：文章回答了关于Spring启动原理的若干问题，包括init-method、PostConstruct、afterPropertiesSet三个方法的执行顺序、两个Bean声明了初始化方法的执行顺序、Spring何时装配Autowire属性、PostConstruct方法中引用Autowired字段是否会空指针、PostConstruct中方法依赖ApplicationContextAware拿到ApplicationContext的顺序、项目中如何监听Spring的启动就绪事件、项目中如何监听Spring刷新事件、Spring就绪事件和刷新事件的执行顺序和区别、Http流量入口何时启动完成、项目中在init-method方法中注册Rpc是否合理、项目中在init-method方法中注册MQ消费组是否合理、Spring还未完全启动时在PostConstruct中调用getBeanByAnnotation能否获得准确的结果等。

10. **源码级别介绍**：文章通过源码级别介绍了SmartInitializingSingleton接口的执行位置、Autowired何时装配Bean的依赖、SpringBoot何时开启Http端口、Spring初始化Bean的关键代码、Spring CommandLineRunner执行位置等。

11. **总结**：文章总结了SpringBoot启动完成后开启Http流量的启示，并建议在SmartLifecype或者ContextRefreshedEvent等位置注册服务，开启流量。
