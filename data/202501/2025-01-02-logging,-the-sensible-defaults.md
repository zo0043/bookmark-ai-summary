# Logging, the sensible defaults
- URL: https://gerlacdt.github.io/blog/posts/logging/
- Added At: 2025-01-02 02:35:22
- [Link To Text](2025-01-02-logging,-the-sensible-defaults_raw.md)

## TL;DR
日志对应用程序至关重要，应遵循现代实践，包括使用结构化日志、合理记录和聚合，避免不良实践，并参考相关资料。

## Summary
1. **日志重要性**：
   - 日志是应用程序设计的重要支柱，对开发、故障分析和调试至关重要。

2. **有效调试工具**：
   - 最有效的调试工具仍然是仔细思考和恰当地放置的打印语句。

3. **日志实践**：
   - 遇到许多代码库存在糟糕的日志实践，如无用日志、缺失上下文或过度日志。

4. **现代云原生应用日志特性**：
   - 日志是文本格式的事件流，通常流出到STDOUT。
   - 每个日志事件对应一行。
   - 使用结构化日志，如JSON格式，包含预定义属性（时间戳、环境、节点、集群、日志级别、应用名称、消息、请求ID）。
   - 优先使用静默日志，遵循Unix哲学中的“沉默规则”。
   - 仅记录可操作的事件。
   - 合理使用日志级别。
   - 记录错误时包含堆栈跟踪和其他上下文信息（用户ID、事务ID、请求ID）。
   - 在中央系统（如ElasticSearch或Datadog）中聚合日志，以实现强大的搜索、分析和异常检测。

5. **不良日志实践**：
   - 不要将日志记录到文件中。
   - 不要为单个日志事件记录多行。
   - 不要在生产环境中记录DEBUG信息。
   - 不要记录敏感数据，如用户相关数据和密码。
   - 不要将日志用作持久数据存储，将其视为具有定义保留期的临时事件流。

6. **参考资料**：
   - [Twelve Factor App](https://12factor.net/logs)
   - [Unix Philosophy](http://www.catb.org/esr/writings/taoup/html/ch01s06.html)
   - [Logging vs instrumentation](https://peter.bourgon.org/blog/2016/02/07/logging-v-instrumentation.html)
