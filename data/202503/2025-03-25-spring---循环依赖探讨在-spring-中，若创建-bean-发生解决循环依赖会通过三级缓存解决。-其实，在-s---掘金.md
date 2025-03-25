# Spring---循环依赖探讨在 Spring 中，若创建 Bean 发生解决循环依赖会通过三级缓存解决。 其实，在 S - 掘金
- URL: https://juejin.cn/post/7483329722496581658
- Added At: 2025-03-25 03:54:09
- [Link To Text](2025-03-25-spring---循环依赖探讨在-spring-中，若创建-bean-发生解决循环依赖会通过三级缓存解决。-其实，在-s---掘金_raw.md)

## TL;DR
文章介绍了Spring框架中循环依赖的解决机制、可能导致启动报错的原因、从5.3版本开始默认禁用循环依赖支持的情况，以及如何开启循环依赖支持的方法。

## Summary
1. **Spring 循环依赖解决机制**：
   - Spring 在创建 Bean 时，若遇到循环依赖，会通过三级缓存来解决问题。
   - 三级缓存包括：
     - `singletonObjects`（一级缓存）：存放完整的 Bean 对象。
     - `earlysingletonObjects`（二级缓存）：存放 Bean 的早期（early）对象。
     - `singletonFactories`（三级缓存）：存放 Bean 的工厂（Factory）对象。

2. **Spring 循环依赖导致启动报错**：
   - 应用在启动时可能因循环依赖报错，例如在 pay 模块中，PayApplicationService 依赖 PayChannelServiceFactory，而 PayChannelServiceFactory 依赖 MockPayChannelService，最终又回到 PayApplicationService。

3. **Spring 对循环依赖的支持变更**：
   - 从 Spring Framework 5.3 开始，Spring 默认禁用了对循环依赖的支持。
   - 在 Spring 2.6 中，这一行为得到进一步明确和强化。

4. **开启循环依赖支持的方法**：
   - 在配置文件中加入 `spring.main.allow-circular-references=true`。
   - 使用 `@Lazy` 注解，在 `@Autowired` 地方增加即可，例如 `@Autowired @Lazy private PayChannelServiceFactory payChannelServiceFactory;`。
