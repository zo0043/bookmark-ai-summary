# Spring官方竟然真的支持Bean的异步初始化
- URL: https://juejin.cn/post/7370994785655701531
- Added At: 2024-10-31 11:06:24
- [Link To Text](2024-10-31-spring官方竟然真的支持bean的异步初始化_raw.md)

## TL;DR
Spring从早期不支持到6.2版支持Bean异步初始化，此特性旨在满足用户加速项目启动的需求，通过引入特定标识和线程池配置实现。

## Summary
1. **Bean异步初始化历史**：
   - **问题提出**：13年前，Spring官方首次讨论Bean异步初始化的可能性。
   - **官方态度**：早期官方认为并行化Bean初始化会增加复杂性和副作用，不支持。
   - **用户需求**：用户希望Spring支持异步初始化以加速项目启动。

2. **Spring 6.0官方回应**：
   - **官方立场**：Spring 6.0版本中，官方仍不优先考虑支持Bean的异步初始化。
   - **启动优化**：官方更关注本地用例的AOT功能以及启动时间的改进。

3. **Spring 6.2的新特性**：
   - **支持异步初始化**：Spring 6.2版本正式支持Bean的异步初始化。
   - **实现方式**：通过引入`backgroundInit`标识和`@Bean`中的`bootstrap=BACKGROUND`枚举来实现。

4. **Bean异步初始化实现细节**：
   - **覆盖getBean步骤**：在`preInstantiateSingletons`方法中覆盖标记为`BACKGROUND`的Bean的整个getBean步骤。
   - **线程池配置**：需要配置名为`bootstrapExecutor`的线程池来支持异步初始化。

5. **示例代码及调试**：
   - **创建Spring项目**：介绍了如何创建一个使用Spring 6.2.0-SNAPSHOT版本的Spring项目。
   - **Bean初始化示例**：提供了两个Bean的示例代码，其中Bean的初始化过程耗时较长。
   - **异步初始化配置**：如何使用`bootstrap = Bean.Bootstrap.BACKGROUND`注解来配置Bean的异步初始化。
   - **调试过程**：通过源码和日志来调试线程池配置问题。

6. **Spring支持异步初始化的原因**：
   - **用户需求**：Spring用户群体对异步初始化的需求增长，官方不得不重视这一需求。
   - **妥协与变化**：官方最终妥协，支持异步初始化，体现了软件开发中的需求和技术的变化。
