Title: 对话即服务：Spring Boot整合MCP让你的CRUD系统秒变AI助手引言 随着人工智能的飞速发展，大语言模型(LL - 掘金

URL Source: https://juejin.cn/post/7483454392979570700

Markdown Content:
引言
--

随着人工智能的飞速发展，大语言模型(LLM)正在革命性地重塑用户与软件的交互范式。想象一下这样的场景：用户无需钻研复杂的API文档或者在繁琐的表单间来回切换，只需通过自然语言直接与系统对话——"帮我查找所有2023年出版的图书"、"创建一个新用户叫张三，邮箱是[zhangsan@example.com](https://link.juejin.cn/?target=mailto%3Azhangsan%40example.com "mailto:zhangsan@example.com")"。这种直观、流畅的交互方式不仅能显著降低新用户的学习曲线，更能大幅削减B端系统的培训成本和实施周期，让企业应用变得更为简单和高效。

这正是**Model Context Protocol (MCP)** 协议在应用层面所带来的价值体现。

认识MCP
-----

我这里不粘贴官方的定义，用大白话给大家解释下：MCP就像是AI世界的"万能适配器"。想象你有很多不同类型的服务和数据库，每个都有自己独特的"说话方式"。AI需要和这些服务交流时就很麻烦，因为要学习每个服务的"语言"。

**MCP**解决了这个问题 - 它就像一个统一的翻译官，让AI只需学一种"语言"就能和所有服务交流。这样开发者不用为每个服务单独开发连接方式，AI也能更容易获取它需要的信息。

如果你是一个后端同学，那么应该接触或听说过**gRPC**。**gRPC**通过标准化的通信方式可以实现不同语言开发的服务之间进行通信，那么**MCP**专门为AI模型设计的"翻译官和接口管理器"，让AI能以统一方式与各种应用或数据源交互。

我们假设开发了一个天气服务，用户想要查询深圳的天气，这里分别以传统**API**方式和**MCP**方式进行对比：

![Image 1: 1.png](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ec9ecda9d6a246c9be269758778dd305~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Yir5oO5Q0M=:q75.awebp?rk3s=f64ab15b&x-expires=1743168782&x-signature=yRVthJ3AIqk7l0wVt3ZcBX4%2B7V4%3D)

对现有Spring Boot服务改造
------------------

这里为了演示，先准备好一个图书管理服务，图书实体字段如下：

```
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PastOrPresent;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


import java.time.LocalDate;

@Entity
@Table(name = "books")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Book {
  
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotBlank(message = "书名不能为空")
  @Column(nullable = false)
  private String title;

  @NotBlank(message = "分类不能为空")
  @Column(nullable = false)
  private String category;

  @NotBlank(message = "作者不能为空")
  @Column(nullable = false)
  private String author;

  @NotNull(message = "出版日期不能为空")
  @PastOrPresent(message = "出版日期不能是未来日期")
  @Column(nullable = false)
  private LocalDate publicationDate;

  @NotBlank(message = "ISBN编码不能为空")
  @Column(nullable = false, unique = true)
  private String isbn;
  
  }
```

为这个服务编写了2个测试方法：

```
import com.example.entity.Book;

import java.util.List;

public interface BookService {

  // 根据作者查询
  List<Book> findBooksByAuthor(String author);

  // 根据分类查询
  List<Book> findBooksByCategory(String category);
}
```

现在我们要将这个SpringBoot服务改造成MCP服务，需要以下步骤：

### 1.导入依赖

在**pom.xml**中引入相关依赖，这里提示一下anthropic的访问需要代理，否则会提示403。

```
<!-- Spring AI 核心依赖 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-core</artifactId>
</dependency>

<!-- Anthropic 模型支持 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-anthropic-spring-boot-starter</artifactId>
</dependency>

<!-- MCP 服务器支持 - WebMVC版本 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-mcp-server-webmvc-spring-boot-starter</artifactId>
</dependency>
```

由于目前这些依赖还是预览版本，所以在**Maven**中央仓库中是找不到的，需要我们额外引入仓库地址。

```
<repositories>
    <repository>
        <id>spring-milestones</id>
        <name>Spring Milestones</name>
        <url>https://repo.spring.io/milestone</url>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </repository>
    <repository>
        <id>spring-snapshots</id>
        <name>Spring Snapshots</name>
        <url>https://repo.spring.io/snapshot</url>
        <releases>
            <enabled>false</enabled>
        </releases>
    </repository>
    <repository>
        <name>Central Portal Snapshots</name>
        <id>central-portal-snapshots</id>
        <url>https://central.sonatype.com/repository/maven-snapshots/</url>
        <releases>
            <enabled>false</enabled>
        </releases>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
    </repository>
</repositories>
```

关于项目中代理的配置可以参考我这段配置：

```
import jakarta.annotation.PostConstruct;
import org.springframework.context.annotation.Configuration;


@Configuration
public class ProxyConfig {

  // 代理设置
  private final String PROXY_HOST = "127.0.0.1";
  private final int PROXY_PORT = 10080;

  @PostConstruct
  public void setSystemProxy() {
    // 设置系统代理属性，这会影响Spring Boot自动配置的HTTP客户端
    System.setProperty("http.proxyHost", PROXY_HOST);
    System.setProperty("http.proxyPort", String.valueOf(PROXY_PORT));
    System.setProperty("https.proxyHost", PROXY_HOST);
    System.setProperty("https.proxyPort", String.valueOf(PROXY_PORT));

    System.out.println("System proxy configured: http://" + PROXY_HOST + ":" + PROXY_PORT);
  }
}
```

### 2.引入配置

我们的目的是将一个Spring服务改造成MCP服务，所以这里不需要进行客户端的配置，同理，在引入依赖的时候也不用引入客户端的依赖。

```
# Spring AI api-key
spring.ai.anthropic.api-key=这里换成你的api-key

# MCP服务端开启
spring.ai.mcp.server.enabled=true

# MCP服务端配置
spring.ai.mcp.server.name=book-management-server
spring.ai.mcp.server.version=1.0.0
spring.ai.mcp.server.type=SYNC
spring.ai.mcp.server.sse-message-endpoint=/mcp/message
```

### 3.改造原服务方法

服务的改造有两种思路-分别是工具配置方式和函数Bean方式，这里对两种方式都做下简略说明： 工具配置方式在需要改造的实现类对需要改造的方法加上@Tool和@ToolParam注解分别标记方法和参数。

```
import com.example.entity.Book;
import com.example.repository.BookRepository;
import com.example.service.BookService;
import jakarta.annotation.Resource;
import lombok.RequiredArgsConstructor;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class BookServiceImpl  implements BookService {

  @Resource
  private BookRepository bookRepository;


  @Override
  @Tool(name = "findBooksByTitle", description = "根据书名模糊查询图书，支持部分标题匹配")
  public List<Book> findBooksByTitle(@ToolParam(description = "书名关键词") String title) {
    return bookRepository.findByTitleContaining(title);
  }

  @Override
  @Tool(name = "findBooksByAuthor", description = "根据作者精确查询图书")
  public List<Book> findBooksByAuthor(@ToolParam(description = "作者姓名") String author) {
    return bookRepository.findByAuthor(author);
  }

  @Override
  @Tool(name = "findBooksByCategory", description = "根据图书分类精确查询图书")
  public List<Book> findBooksByCategory(@ToolParam(description = "图书分类")String category) {
    return bookRepository.findByCategory(category);
  }
}
```

接着将这个实现类注册到MCP服务器配置上即可。

```
import com.example.service.BookService;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * MCP服务器配置类，负责注册MCP工具
 */
@Configuration
public class McpServerConfig {

  /**
   * 注册工具回调提供者，将BookService中的@Tool方法暴露为MCP工具
   *
   * @param bookService 图书服务
   * @return 工具回调提供者
   */
  @Bean
  public ToolCallbackProvider bookToolCallbackProvider(BookService bookService) {
    return MethodToolCallbackProvider.builder()
            .toolObjects(bookService)
            .build();
  }

}
```

此时在聊天客户端配置引入注册工具即可。

```
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


/**
 * 聊天客户端配置类
 */
@Configuration
public class ChatClientConfig {


  @Autowired
  private ToolCallbackProvider toolCallbackProvider;

  /**
   * 配置ChatClient，注册系统指令和工具函数
   */
  @Bean
  public ChatClient chatClient(ChatClient.Builder builder) {
    return builder
            .defaultSystem("你是一个图书管理助手，可以帮助用户查询图书信息。" +
                    "你可以根据书名模糊查询、根据作者查询和根据分类查询图书。" +
                    "回复时，请使用简洁友好的语言，并将图书信息整理为易读的格式。")
            // 注册工具方法
            .defaultTools(toolCallbackProvider)
            .build();
  }
}
```

除了上述的方式，还可以单独声明一个类将查询方法作为函数Bean导出。

```
import com.example.entity.Book;
import com.example.service.BookService;
import jakarta.annotation.Resource;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.function.Function;

/**
 * 图书查询服务，将查询方法作为函数Bean导出
 */
@Service
public class BookQueryService {

  @Resource
  private BookService bookService;

  /**
   * 根据书名查询图书的函数Bean
   */
  @Bean
  public Function<String, List<Book>> findBooksByTitle() {
    return title -> bookService.findBooksByTitle(title);
  }

  /**
   * 根据作者查询图书的函数Bean
   */
  @Bean
  public Function<String, List<Book>> findBooksByAuthor() {
    return author -> bookService.findBooksByAuthor(author);
  }

  /**
   * 根据分类查询图书的函数Bean
   */
  @Bean
  public Function<String, List<Book>> findBooksByCategory() {
    return category -> bookService.findBooksByCategory(category);
  }

}
```

采用这种方式在定义AI聊天客户端的时候需要显式地声明。

```
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 聊天客户端配置类
 */
@Configuration
public class ChatClientConfig {


  /**
   * 配置ChatClient，注册系统指令和工具函数
   */
  @Bean
  public ChatClient chatClient(ChatClient.Builder builder) {
    return builder
            .defaultSystem("你是一个图书管理助手，可以帮助用户查询图书信息。" +
                    "你可以根据书名模糊查询、根据作者查询和根据分类查询图书。" +
                    "回复时，请使用简洁友好的语言，并将图书信息整理为易读的格式。")
            // 注册工具方法，这里使用方法名称来引用Spring上下文中的函数Bean
            .defaultTools(
                    "findBooksByTitle",
                    "findBooksByAuthor",
                    "findBooksByCategory"
            )
            .build();
  }
}
```

### 4.接口测试

完成了服务开发后，我们就可以声明一个控制器对外暴露进行调用。

```
import com.example.model.ChatRequest;
import com.example.model.ChatResponse;
import jakarta.annotation.Resource;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 聊天控制器，处理AI聊天请求
 */
@RestController
@RequestMapping("/api/chat")
public class ChatController {

  
  @Resource
  private ChatClient chatClient;


  /**
   * 处理聊天请求，使用AI和MCP工具进行响应
   *
   * @param request 聊天请求
   * @return 包含AI回复的响应
   */
  @PostMapping
  public ResponseEntity<ChatResponse> chat(@RequestBody ChatRequest request) {
    try {
      // 创建用户消息
      String userMessage = request.getMessage();

      // 使用流式API调用聊天
      String content = chatClient.prompt()
              .user(userMessage)
              .call()
              .content();

      return ResponseEntity.ok(new ChatResponse(content));
    } catch (Exception e) {
      e.printStackTrace();
      return ResponseEntity.ok(new ChatResponse("处理请求时出错: " + e.getMessage()));
    }
  }
  
}
```

为了方便测试，我们开发一个数据初始化器，通过实现`CommandLineRunner`接口，它会在我们的应用程序启动时自动向数据库中加载这些测试数据。

```
import com.example.entity.Book;
import com.example.repository.BookRepository;
import jakarta.annotation.Resource;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

@Component
@RequiredArgsConstructor
public class DataInitializer  implements CommandLineRunner {

  @Resource
  private BookRepository bookRepository;

  @Override
  public void run(String... args) throws Exception {
    // 准备示例数据
    List<Book> sampleBooks = Arrays.asList(
            new Book(null, "Spring实战（第6版）", "编程", "Craig Walls",
                    LocalDate.of(2022, 1, 15), "9787115582247"),
            new Book(null, "深入理解Java虚拟机", "编程", "周志明",
                    LocalDate.of(2019, 12, 1), "9787111641247"),
            new Book(null, "Java编程思想（第4版）", "编程", "Bruce Eckel",
                    LocalDate.of(2007, 6, 1), "9787111213826"),
            new Book(null, "算法（第4版）", "计算机科学", "Robert Sedgewick",
                    LocalDate.of(2012, 10, 1), "9787115293800"),
            new Book(null, "云原生架构", "架构设计", "张三",
                    LocalDate.of(2023, 3, 15), "9781234567890"),
            new Book(null, "微服务设计模式", "架构设计", "张三",
                    LocalDate.of(2021, 8, 20), "9789876543210"),
            new Book(null, "领域驱动设计", "架构设计", "Eric Evans",
                    LocalDate.of(2010, 4, 10), "9787111214748"),
            new Book(null, "高性能MySQL", "数据库", "Baron Schwartz",
                    LocalDate.of(2013, 5, 25), "9787111464747"),
            new Book(null, "Redis实战", "数据库", "Josiah L. Carlson",
                    LocalDate.of(2015, 9, 30), "9787115419378"),
            new Book(null, "深入浅出Docker", "容器技术", "李四",
                    LocalDate.of(2022, 11, 20), "9787123456789")
    );

    // 保存示例数据
    bookRepository.saveAll(sampleBooks);

    System.out.println("数据初始化完成，共加载 " + sampleBooks.size() + " 本图书");
  }

}
```

接下来我们通过请求接口进行如下测试：

![Image 2: 2.png](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fd3fd591893f40af81933b7a3d97a215~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Yir5oO5Q0M=:q75.awebp?rk3s=f64ab15b&x-expires=1743168782&x-signature=t%2FHj%2Fo0vLJCtvGsGAbcPuk2WDUY%3D)

![Image 3: 3.png](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c1dbedc210c64fdbaa7999e01ed66d7c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Yir5oO5Q0M=:q75.awebp?rk3s=f64ab15b&x-expires=1743168782&x-signature=h1UTxIqehScRdL3OMatrPRdGguY%3D)

可以看到此时返回结果是数据库中的测试数据内容。这里是根据用户输入的问题，大模型会判断我们开放的工具方法中是否有匹配的，如果有则进行调用并返回。

小结
--

通过Spring Boot与MCP的整合，我们轻松实现了传统CRUD系统到智能AI助手的转变。MCP作为AI与服务之间的桥梁，极大简化了集成工作。未来随着MCP生态发展，"对话即服务"将可能成为应用的开发范式，让复杂系统变得更加易用。
