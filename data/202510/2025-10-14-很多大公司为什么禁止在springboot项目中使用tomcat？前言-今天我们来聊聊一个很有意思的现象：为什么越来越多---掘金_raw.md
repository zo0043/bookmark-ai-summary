Title: 很多大公司为什么禁止在SpringBoot项目中使用Tomcat？

URL Source: https://juejin.cn/post/7554402481913905152

Published Time: 2025-09-28T00:44:45+00:00

Markdown Content:
前言
--

今天我们来聊聊一个很有意思的现象：为什么越来越多的大公司禁止SpringBoot项目使用默认的Tomcat，而强制要求使用Undertow？

有些小伙伴在工作中可能已经发现了这个趋势，但背后的原因你真的清楚吗？

[最近准备面试的小伙伴，可以看一下这个宝藏网站（Java突击队）：www.susan.net.cn，里面：面试八股文、场景设计题、面试真题、7个项目实战、工作内推什么都有](https://link.juejin.cn/?target=http%3A%2F%2Fwww.susan.net.cn%3Frefer%3Djuejin "https://link.juejin.cn/?target=http%3A%2F%2Fwww.susan.net.cn%3Frefer%3Djuejin")。

一、SpringBoot的默认选择与现状
--------------------

SpringBoot作为Java领域最流行的开发框架，其默认内嵌的Web容器是Tomcat。

这让我们很多开发者养成了"开箱即用"的习惯，但大公司却在生产环境中纷纷转向Undertow。

这背后到底隐藏着什么秘密？

![Image 1](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/db743d07cdd146b8b46d143fe5dda0fd~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1760829284&x-signature=YcqLcTRKUqKHXaRjqcn3x%2FF%2Bmoc%3D)

从上图可以看出，虽然Tomcat是默认选择，但Undertow在高性能场景下更具优势。

二、性能对比
------

### 2.1 内存占用对比

让我们先看一组实际测试数据。在相同条件下部署SpringBoot应用：

| 容器 | 启动内存 | 堆内存占用 | 非堆内存占用 | 线程内存 |
| --- | --- | --- | --- | --- |
| Tomcat | 120MB | 80MB | 25MB | 15MB |
| Undertow | 85MB | 60MB | 15MB | 10MB |
| **优化比例** | **-29%** | **-25%** | **-40%** | **-33%** |

从数据可以看出，Undertow在内存占用方面有明显优势。

对于大规模部署的微服务架构，这种内存节省会累积成巨大的成本优势。

### 2.2 并发处理能力

在并发性能测试中，Undertow同样表现优异：

```
// 性能测试代码示例
@SpringBootTest
class WebContainerPerformanceTest {
    
    @Test
    void testConcurrentPerformance() {
        // 模拟1000并发用户持续请求30秒
        LoadTest loadTest = LoadTest.configure()
            .threads(1000)
            .duration(30, TimeUnit.SECONDS)
            .build();
            
        // Tomcat测试结果
        TomcatResult tomcatResult = loadTest.runWithTomcat();
        
        // Undertow测试结果  
        UndertowResult undertowResult = loadTest.runWithUndertow();
        
        // 结果对比
        System.out.println("QPS - Tomcat: " + tomcatResult.getQps());
        System.out.println("QPS - Undertow: " + undertowResult.getQps());
        System.out.println("平均响应时间 - Tomcat: " + tomcatResult.getAvgResponseTime());
        System.out.println("平均响应时间 - Undertow: " + undertowResult.getAvgResponseTime());
    }
}
```

典型测试结果：

*   **Tomcat**：QPS 8500，平均响应时间 15ms
*   **Undertow**：QPS 12000，平均响应时间 8ms

三、底层架构差异
--------

### 3.1 Tomcat的架构设计

Tomcat采用传统的BIO/NIO连接器架构：

![Image 2](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f586825f53cd485b8a5b7cfd36044777~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1760829284&x-signature=qCncoS%2BEcN1kqOSt5RN%2FBk471AA%3D)

Tomcat的架构相对重量级，每个层次都有明确的职责划分，但也带来了额外的开销。

### 3.2 Undertow的架构设计

Undertow采用更加现代的XNIO基础架构：

![Image 3](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4a0cb35030b24cc1bdb15c3720a90f44~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1760829284&x-signature=NPZF3ePRt%2BqBoCGjydUNRH%2BU%2FYY%3D)

Undertow的核心特点：

1.   **IO线程与工作线程分离**：IO线程处理网络IO，工作线程处理业务逻辑
2.   **事件驱动架构**：基于回调的事件处理机制
3.   **零拷贝能力**：支持直接缓冲区，减少内存拷贝

四、内存管理
------

### 4.1 直接内存使用

Undertow在内存管理上更加高效，大量使用直接内存（Direct Buffer）：

```
// Undertow的内存管理示例
public class UndertowMemoryManagement {
    
    // 使用直接缓冲区处理请求
    public void handleRequest(HttpServerExchange exchange) {
        // 获取直接缓冲区
        ByteBuffer buffer = exchange.getConnection().getBufferPool().allocate();
        
        try {
            // 直接操作缓冲区，避免拷贝
            readRequestData(exchange, buffer);
            processRequest(buffer);
            writeResponse(exchange, buffer);
        } finally {
            // 释放缓冲区
            exchange.getConnection().getBufferPool().free(buffer);
        }
    }
    
    // Tomcat通常需要多次内存拷贝
    public void tomcatHandleRequest(Request request, Response response) {
        // 从输入流读取数据（内存拷贝）
        byte[] inputData = readInputStream(request.getInputStream());
        
        // 处理数据（可能再次拷贝）
        byte[] outputData = processData(inputData);
        
        // 写入输出流（又一次拷贝）
        response.getOutputStream().write(outputData);
    }
}
```

这种零拷贝的设计在大文件传输和高并发场景下优势明显。

### 4.2 连接池优化

Undertow的连接管理更加精细：

```
# Undertow配置示例
server:
  undertow:
    # 线程池配置
    threads:
      worker: 16
      io: 4
    # 缓冲区配置
    buffer-size: 1024
    direct-buffers: true
    # 连接配置
    max-connections: 10000
    max-http-post-size: 10485760
```

对比Tomcat的配置：

```
# Tomcat配置示例
server:
  tomcat:
    # 连接器配置
    max-connections: 10000
    max-threads: 200
    min-spare-threads: 10
    # 其他配置
    max-http-post-size: 10485760
    connection-timeout: 20000
```

最近为了帮助大家找工作，专门建了一些工作内推群，各大城市都有，欢迎各位HR和找工作的小伙伴进群交流，群里目前已经收集了不少的工作内推岗位。加苏三的微信：li_su223，备注：掘金+所在城市，即可进群。

五、并发模型
------

### 5.1 Undertow的XNIO架构

Undertow基于JBoss的XNIO库，采用更加现代的并发模型：

```
// XNIO工作线程模型示例
public class XNIOWorkerModel {
    
    public void demonstrateWorkerModel() {
        // 创建Worker实例
        XnioWorker worker = Xnio.getInstance().createWorker(
            OptionMap.create(Options.THREAD_DAEMON, true)
        );
        
        // IO线程处理网络事件
        worker.getIoThread().execute(() -> {
            // 处理IO就绪事件
            handleIOReadyEvents();
        });
        
        // 工作线程处理业务逻辑
        worker.getWorkerThreadPool().execute(() -> {
            // 执行业务处理
            executeBusinessLogic();
        });
    }
}
```

这种设计的优势在于：

1.   **IO线程专注网络**：不被业务逻辑阻塞
2.   **工作线程池弹性**：根据业务需求动态调整
3.   **事件驱动高效**：基于事件回调，减少线程切换

### 5.2 Tomcat的线程模型对比

Tomcat的传统线程模型：

![Image 4](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e8fb769a852945b18e3aa9d2e05d8dc8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1760829284&x-signature=3sVyX2%2Fxms3p76T0FyPtZoCXcnU%3D)

Tomcat的线程模型在极高并发下会出现：

*   大量的线程上下文切换开销
*   线程阻塞等待资源
*   内存占用随线程数线性增长

六、配置灵活性
-------

### 6.1 精细化配置能力

Undertow提供了极其细致的配置选项，满足各种复杂场景：

```
@Configuration
public class UndertowConfig {
    
    @Bean
    public UndertowServletWebServerFactory undertowServletWebServerFactory() {
        UndertowServletWebServerFactory factory = new UndertowServletWebServerFactory();
        
        factory.addBuilderCustomizers(builder -> {
            // 配置HTTP/2
            builder.setServerOption(UndertowOptions.ENABLE_HTTP2, true);
            
            // 配置缓冲区
            builder.setSocketOption(Options.RECEIVE_BUFFER, 1024 * 16);
            builder.setSocketOption(Options.SEND_BUFFER, 1024 * 64);
            
            // 配置线程池
            builder.setIoThreads(Runtime.getRuntime().availableProcessors());
            builder.setWorkerThreads(200);
            
            // 配置连接数限制
            builder.setServerOption(UndertowOptions.MAX_CONNECTIONS, 10000);
        });
        
        return factory;
    }
}
```

### 6.2 处理器链机制

Undertow的处理器链机制允许深度定制请求处理流程：

```
public class CustomHandler implements HttpHandler {
    
    private final HttpHandler next;
    
    public CustomHandler(HttpHandler next) {
        this.next = next;
    }
    
    @Override
    public void handleRequest(HttpServerExchange exchange) throws Exception {
        long startTime = System.currentTimeMillis();
        
        try {
            // 前置处理：认证、日志等
            preHandle(exchange);
            
            // 调用下一个处理器
            next.handleRequest(exchange);
            
        } finally {
            // 后置处理：统计、清理等
            postHandle(exchange, startTime);
        }
    }
    
    private void preHandle(HttpServerExchange exchange) {
        // 认证检查
        if (!checkAuthentication(exchange)) {
            exchange.setStatusCode(401);
            exchange.endExchange();
            return;
        }
        
        // 请求日志记录
        logRequest(exchange);
    }
}
```

这种灵活的处理器链机制让Undertow在定制化需求面前游刃有余。

七、实战案例
------

### 7.1 某电商平台的容器迁移实践

某大型电商平台在高峰期面临严重的性能瓶颈，迁移到Undertow后的效果：

**迁移前（Tomcat）：**

*   单机QPS：8000
*   平均响应时间：25ms
*   内存占用：2GB
*   CPU使用率：85%

**迁移后（Undertow）：**

*   单机QPS：15000（+87%）
*   平均响应时间：12ms（-52%）
*   内存占用：1.2GB（-40%）
*   CPU使用率：65%（-23%）

### 7.2 配置优化示例

```
# 生产环境Undertow优化配置
server:
  undertow:
    # IO线程数（通常为CPU核心数）
    io-threads: 8
    # 工作线程数（根据业务调整）
    worker-threads: 200
    # 直接缓冲区
    direct-buffers: true
    buffer-size: 16384
    # 连接配置
    max-connections: 10000
    max-http-post-size: 10485760
    # 优雅关闭
    no-request-timeout: 60000
    drain-wait-time: 20000
    
  # JVM优化配合
  port: 8080
  compression:
    enabled: true
    mime-types: text/html,text/xml,text/plain,application/json
```

八、如何迁移？
-------

### 8.1 Maven配置调整

```
<!-- 排除Tomcat -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- 引入Undertow -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

### 8.2 迁移注意事项

有些小伙伴在迁移过程中可能会遇到以下问题：

1.   **Servlet API兼容性**：确保代码使用标准Servlet API
2.   **WebSocket配置**：Undertow的WebSocket配置与Tomcat不同
3.   **SSL配置**：证书和SSL配置可能需要调整
4.   **会话管理**：如果使用分布式会话，需要验证兼容性

总结
--

通过上面的详细分析，我们可以总结出大公司选择Undertow的主要原因：

### 1 性能优势明显

*   **更高的并发处理能力**：XNIO架构更适应高并发场景
*   **更低的内存占用**：直接内存和缓冲区优化减少内存使用
*   **更好的响应时间**：事件驱动模型减少处理延迟

### 2 资源利用高效

*   **精细化的资源控制**：线程池、缓冲区等可精细配置
*   **更好的可扩展性**：适应云原生和容器化部署
*   **更低的运维成本**：减少服务器数量和资源消耗

### 3 技术架构先进

*   **现代化的并发模型**：更适应现代硬件架构
*   **灵活的扩展机制**：处理器链支持深度定制
*   **更好的未来发展**：为HTTP/2、Quic等新协议做好准备

### 4 业务需求驱动

*   **大规模部署需求**：微服务架构下容器性能至关重要
*   **成本控制压力**：性能提升直接转化为成本降低
*   **技术竞争力**：保持技术栈的先进性和竞争力

有些小伙伴可能会说："我的项目并发量不大，用Tomcat也挺好"。

确实，对于小型项目或个人项目，Tomcat完全够用。

但对于大公司来说，技术选型要考虑的是规模化效应。

当你有成千上万个微服务实例时，每个实例节省几十MB内存，总体节省的资源就是天文数字。

> 我的建议是：**对于新项目，特别是预期有高并发需求的微服务项目，优先考虑使用Undertow。对于现有项目，如果遇到性能瓶颈，可以考虑迁移到Undertow。**

技术选型没有绝对的对错，只有适合与否。

最后说一句(求关注，别白嫖我)
---------------

如果这篇文章对您有所帮助，或者有所启发的话，帮忙关注一下我的同名公众号：苏三说技术，您的支持是我坚持写作最大的动力。

求一键三连：点赞、转发、在看。

关注公众号：【苏三说技术】，在公众号中回复：进大厂，可以免费获取我最近整理的10万字的面试宝典，好多小伙伴靠这个宝典拿到了多家大厂的offer。
