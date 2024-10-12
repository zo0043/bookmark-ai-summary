# 一张长图透彻理解SpringBoot 启动原理
- URL: https://juejin.cn/post/7308610896803659812
- Added At: 2024-10-12 07:52:24
- [Link To Text](2024-10-12-一张长图透彻理解springboot-启动原理_raw.md)

## TL;DR
文章深入剖析了SpringBoot启动原理，强调其对解决集成问题的重要性，通过故障案例、扩展点解析、启动顺序实验及源码解读，详细阐述了启动过程及关键步骤，最终总结在启动后开启流量的必要性。

## Summary
1. **SpringBoot启动原理重要性**：文章强调了深入理解SpringBoot启动原理对于Java程序员和架构师的重要性，特别是当涉及到中间件和框架的集成时。

2. **流量入口问题**：讨论了SpringBoot项目中的流量入口，如Rpc、Http、MQ，以及它们在Spring启动过程中的集成问题。

3. **线上故障案例**：通过线上故障案例，说明了在不正确的时机开启MQ流量可能会导致的问题，强调了对Spring启动过程深入理解的重要性。

4. **启动原理问题**：列举了11个问题，旨在测试读者对Spring启动原理的理解程度，并引出后续的详细解析。

5. **Spring启动扩展点**：详细介绍了Spring启动过程中的多个扩展点，包括BeanFactoryAware、ApplicationContextAware、BeanNameAware、ApplicationListener、CommandLineRunner、SmartLifecycle等。

6. **启动顺序实验**：通过实验代码展示了如何通过日志打印验证Spring启动过程中的执行顺序。

7. **实例化与初始化**：解释了实例化和初始化的区别，以及它们在Spring启动过程中的位置。

8. **Spring启动顺序**：详细解析了Spring启动过程中的各个步骤，包括BeanFactoryPostProcessor的执行、实例化Bean、Autowired装配依赖、BeanNameAware、BeanFactoryAware、ApplicationContextAware、BeanPostProcessor、PostConstruct、InitializingBean、init-method、BeanPostProcessor、SmartInitializingSingleton、SmartLifecyle、ContextRefreshedEvent、注册和初始化Spring MVC、Tomcat/Jetty容器开启端口、CommandLineRunner的执行等。

9. **问题解答**：针对之前提出的问题，给出了详细的解答和解释。

10. **源码级别介绍**：通过源码截图和解释，深入介绍了SmartInitializingSingleton接口、Autowired装配、SpringBoot开启Http端口、Spring初始化Bean的关键代码、Spring CommandLineRunner执行位置等内容。

11. **总结**：强调了在Spring启动完成后开启入口流量的重要性，并以Eureka服务发现组件为例进行了说明，最后总结了文章的主要内容。
