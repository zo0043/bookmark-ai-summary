Title: QiuMo JetBrains Help - JetBrains激活助手

URL Source: https://ide.mihuyo.cc/

Markdown Content:
欢迎使用 JetBrains 激活助手
-------------------

为您提供便捷的 JetBrains 产品激活解决方案，支持激活码和许可证服务器两种激活方式

许可证名称

未设置

被许可人

未设置

### 必备代理工具

激活前必须先下载并配置 ja-netfilter 代理工具

#### 配置步骤：

1

下载并解压 ja-netfilter 工具包

2

在 IDE 的 VM options 中添加以下配置：

-javaagent:插件解压路径\ja-netfilter\ja-netfilter.jar

--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED

 --add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED

3

重启 IDE 后即可使用激活功能

### 激活码激活

生成产品激活码直接激活

1

选择需要激活的产品或插件

2

设置许可证到期时间

3

生成激活码并在软件中输入

### 服务器激活

配置许可证服务器统一激活

1

下载并配置 ja-netfilter 代理

2

在软件中配置许可证服务器地址

3

启动软件自动获取许可证

许可证服务器地址：

### JRebel 专属激活

JRebel 仅支持服务器激活模式
