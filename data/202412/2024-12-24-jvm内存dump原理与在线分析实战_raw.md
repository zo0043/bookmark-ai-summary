Title: JVM内存Dump原理与在线分析实战 ｜ 得物技术

URL Source: https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247489242&idx=1&sn=31e5c4a54b89963c7de19275c9560453&chksm=c1624385f615ca93c1f16dedea34a0d64ec2ecf193099b5c20826a27dd295c4d6df5587ca782&scene=178&cur_album_id=2474766602014670848

Markdown Content:
**1.前言**
--------

当前我们微服务容器化部署JVM 实例很多,常常需要进行JVM heap dump analysis,为了提升JVM 问题排查效率,得物技术保障团队研究了JVM内存Dump 原理与设计开发了JVM 内存在线分析。

常见的JVM  heap dump analysis 工具如: MAT,JProfile,最常用的功能是大对象分析。功能上本地分析工具更全面，在微服务架构下,成千上万的实例当需要一次分析的时候，于是我们思考如何提供更方便更快的在线分析方便研发人员快速排障。

<table data-ace-table-col-widths="100;187;171;388;"><colgroup><col width="100"><col width="187"><col width="171"><col width="388"></colgroup><tbody><tr><td><p><span>流程</span></p></td><td><p><span>传统</span></p></td><td><p><span>在线分析</span></p></td><td><p><span>相比</span></p></td></tr><tr><td><p><span>hprof 获取</span></p></td><td><p><span>jmap</span></p></td><td><p><span>jmap</span></p></td><td><p><span>相同</span></p></td></tr><tr><td><p><span>hprof 传输</span></p></td><td><p><span>1.上传ftp或对象存储。</span></p><p><span>2.生产环境涉及跨网脱敏。</span></p><p><span>3.跨网下载。</span></p></td><td><p><span>内网OSS(对象存储)传输。</span></p></td><td><p><span>目前jvm 基本进入G1 大内存时代。越大内存dump 效果越明显耗时降低(100倍耗时降低)为大规模dump分析打下基础。</span></p></td></tr><tr><td><p><span>hprof 分析</span></p></td><td><p><span>本地MAT 、JProfiler等分析工具</span></p></td><td><p><span>在线分析、在线分析报告</span></p></td><td><p><span>优点:</span></p><ol start="1"><li><p><span>不依赖任何软件。</span></p></li><li><p><span>操作简单，只需一键执行脚本。</span></p></li><li><p><span>分析耗时比本地工具更快。</span></p></li><li><p><span>不受内存限制，支持大内存dump 分析。</span></p></li><li><p><span>自研不受商业限制。</span></p></li><li><p><span>微服务环境多实例同时并发分析，不受单机资源限制。</span></p></li></ol><p><span>不足:</span></p><ol start="1"><li><p><span>MAT ,JProfile 功能更丰富</span></p></li></ol></td></tr></tbody></table>

**2.JVM 内存模型**
--------------

首先我们快速过一下Java 的内存模型, 这部分不必深入,稍微了解不影响第三部分 JVM 内存分析原理。可回过头来再看。

JVM 内存模型可以从共享和非共享理解，也可以从 stack,heap 理解。GC 主要作用于 heap 区， stack 的内存存在系统内存。

![Image 27](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kL0xbqGTb35KUl6zaRFWuPcRGsAX9vXBy591m0Twp6UQm1KYKodo0Kg/640?wx_fmt=png)

**2.1 Run-Time Data Areas**
---------------------------

Java 程序运行起来后,JVM 会把它所管理的内存划分为若干个不同的数据区域。其中一些数据区是在 Java 虚拟机启动时创建的，只有在 Java 虚拟机退出时才会销毁。其他数据区是每个线程。每线程数据区在创建线程时创建，并在线程退出时销毁。JVM 的数据区是逻辑内存空间，它们可能不是连续的物理内存空间。下图显示了 JVM 运行时数据区域：

![Image 28](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72ksIzJovPgwp6OZE3YofaCT9NkPo4v48CnMuctlwiapoJLtlM5r5G1VXw/640?wx_fmt=png)

*   #### **PC Register**
    

JVM 可以同时支持多个执行线程。每个 JVM 线程都有自己的 pc（程序计数器）寄存器。如果当前方法是 native方法则PC值为 undefined, 每个CPU 都有一个 PC,一般来说每一次指令之后,PC 值会增加,指向下一个操作指令的地址。JVM 使用PC 保持操作指令的执行顺序，PC 值实际上就是指向方法区(Method Area) 的内存地址。

*   #### **JVM Stacks**
    

每个 JVM 线程都有一个私有 JVM Stack（堆栈）， 用于存储 Frames(帧)。JVM Stack的每一Frame(帧)都存储当前方法的局部变量数组、操作数堆栈和常量池引用。

一个 JVM Stack可能有很多Frame(帧)，因为在线程的任何方法完成之前，它可能会调用许多其他方法，而这些方法的帧也存储在同一个 JVM Stack(堆栈)中。

JVM Stack 是一个先进后出(LIFO)的数据结构,所以当前的执行方法位于栈顶，每一个方法开始执行时返回、或抛出一个未捕获的异常，则次frame 被移除。

JVM Stack 除了压帧和弹出帧之外，JVM 堆栈从不直接操作，所以帧可能是堆分配的。JVM 堆栈的内存不需要是连续的。

*   #### **Native Method Stack**
    

Native 基本为C/C++ 本地函数,超出了Java 的范畴,就不展开赘述了。接入进入共享区域Heap 区。

### **2.2 Heap**

JVM 有一个在所有 JVM 线程之间共享的堆。堆是运行时数据区，从中分配所有类实例和数组的内存。

堆是在虚拟机启动时创建的。对象的堆存储由自动存储管理系统（称为垃圾收集器）回收；对象永远不会被显式释放。JVM 没有假设特定类型的自动存储管理系统，可以根据实现者的系统要求选择存储管理技术。堆的内存不需要是连续的。

*   #### **Method Area**
    

JVM 有一个在所有 JVM 线程之间共享的方法区。方法区类似于常规语言编译代码的存储区，或类似于操作系统进程中的“文本”段。它存储每个类的结构，例如运行时常量轮询、字段和方法数据，以及方法和构造函数的代码，包括在类和实例初始化和接口初始化中使用的特殊方法。

Method 区域是在虚拟机启动时创建的。尽管方法区在逻辑上是堆的一部分，但简单的实现可能会选择不进行垃圾收集或压缩它。方法区可以是固定大小，也可以根据需要进行扩展。方法区的内存不需要是连续的。

*   #### **Run-Time Constant Pool**
    

运行时常量池是方法区的一部分。Claas 文件中除了有类的版本、字段、方法、接口等描述信息外，还有一项信息是常量池(Constant Pool Table),用于存放编译期生成各种字面量和符号引用，这部分内容将在类加载后进入方法区的运行时常量池中存放。

### **2.3 Thread**

Java 程序最终运行的主体是线程，那么JVM 运行时数据区可以按线程间是否共享来划分:

*   单个线程内共享的区: PC Register、JVM Stacks、Native Method stacks。
    
*   所有线程共享的区: Heap、Method Area、Run-time Constant pool。
    

*   #### **Pre-Threads:**
    

*   JVM System Threads
    

*   Per Thread
    

*   Program Counter
    

*   Stack
    

*   Native Stack
    

*   Stack Restrictions
    

*   Frame
    

*   Local Variables Array
    

*   Operand Stack
    
*   Dynamic Linking
    

*   #### **JVM System Threads**
    

如果你使用jconsole或者其他任何debug工具，有可能你会发现有大量的线程在后台运行。这些后台线程随着main线程的启动而启动，即，在执行public static void main(String\[\])后，或其他main线程创建的其他线程，被启动后台执行。

Hotspot JVM 主要的后台线程包括：

*   VM thread: 这个线程专门用于处理那些需要等待JVM满足safe-point条件的操作。safe-point代表现在没有修改heap的操作发生。这种类型的操作包括：”stop-the-world”类型的GC，thread stack dump，线程挂起，或撤销对象偏向锁(biased locking revocation)
    

*   Periodic task thread: 用于处理周期性事件（如：中断）的线程
    

*   GC threads: JVM中，用于支持不同阶段的GC操作的线程
    

*   Compiler threads: 用于在运行时，将字节码编译为本地代码的线程
    
*   Signal dispatcher thread: 接受发送给JVM处理的信号，并调用对应的JVM方法
    

*   #### **Program Counter (PC)**
    

当前操作指令或opcode的地址指针，如果当前方法是本地方法，则PC值为undefined。每个CPU都有一个PC，一般来说，每一次指令之后，PC值会增加，指向下一个操作指令的地址。JVM使用PC保持操作指令的执行顺序，PC值实际上就是指向方法区(Method Area)中的内存地址。

*   #### **Stack**
    

每一个线程都拥有自己的栈（Stack），用于在本线程中正在执行的方法。栈是一个先进后出（LIFO）的数据结构，所以当前的执行方法位于栈顶。每一个方法开始执行时，一个新的帧（Frame)被创建（压栈），并添加到栈顶。当方法正常执行返回，或方法执行时抛出一个未捕获的异常，则此帧被移除（弹栈）。栈，除了压栈和弹栈操作外，不会被执行操作，因此，帧对象可以被分配在堆（Heap）内存中，并且不需要分配连续内存。

*   #### **Native Stack**
    

不是所有的JVM都支持本地方法，然而，基本上都会为每个线程，创建本地方法栈。如果JVM使用C-Linkage模型，实现了JNI（Java Native Invocation），那么本地栈就会是一个C语言的栈。在这种情况下，本地栈中的方法参数和返回值顺序将和C语言程序完全一致。一个本地的方法一般可以回调JVM中的Java方法（依据具体JVM实现而定）。这样的本地方法调用Java方法一般会使用Java栈实现，当前线程将从本地栈中退出，在Java栈中创建一个新的帧。

*   #### **Stack Restrictions**
    

栈可以使一个固定大小或动态大小。如果一个线程请求超过允许的栈空间，允许抛出StackOverflowError。如果一个线程请求创建一个帧，而没有足够内存时，则抛出OutOfMemoryError。

*   #### **Frame**
    

每一个方法被创建的时候都会创建一个 frame，每个 frame 包含以下信息:

*   本地变量数组 Local Variable Array
    

*   返回值
    

*   操作对象栈 Operand Stack
    

*   当前方法所属类的运行时常量池
    

*   #### **Local Variables Array**
    

本地变量数组包含所有方法执行过程中的所有变量，包括this引用，方法参数和其他定义的本地变量。对于类方法（静态方法），方法参数从0开始，然后对于实例方法，参数数据的第0个元素是this引用。

本地变量包括：

<table data-ace-table-col-widths="100;100;100;"><tbody><tr><td><p><span>基本数据类型</span></p></td><td><p><span>bits</span></p></td><td><p><span>bytes</span></p></td></tr><tr><td><p><span>boolean</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>byte</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>char</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>long</span></p></td><td><p><span>64</span></p></td><td><p><span>8</span></p></td></tr><tr><td><p><span>short</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>int</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>float</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>double</span></p></td><td><p><span>64</span></p></td><td><p><span>8</span></p></td></tr><tr><td><p><span>reference</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr><tr><td><p><span>reference</span></p></td><td><p><span>32</span></p></td><td><p><span>4</span></p></td></tr></tbody></table>

所有类型都占用一个数据元素，除了long和double，他们占用两个连续数组元素。（这两个类型是64位的，其他是32位的）

*   #### **Operand Stack**
    

在执行字节代码指令过程中，使用操作对象栈的方式，与在本机CPU中使用通用寄存器相似。大多数JVM的字节码通过压栈、弹栈、复制、交换、操作执行这些方式来改变操作对象栈中的值。因此，在本地变量数组中和操作栈中移动复制数据，是高频操作。

Frame 被创建时，操作栈是空的，操作栈的每个项可以存放JVM 的各种类型,包括 long/double。操作栈有一个栈深，long/double 占用2个栈深，操作栈调用其它有返回结果的方法时，会把结果push 到栈上。

下面举例说明，通过操作对象栈，将一个简单的变量赋值为0.

Java：

```
int i;编译后得到以下字节码：C： 0:        iconst_0        // 将0压到操作对象栈的栈顶 1:        istore_1        // 从操作对象栈中弹栈，并将值存储到本地变量1中Dyanmic Linking每个帧都包含一个引用指针，指向运行时常量池。这个引用指针指向当前被执行方法所属对象的常量池。当Java Class被编译后，所有的变量和方法引用都利用一个引用标识存储在class的常量池中。一个引用标识是一个逻辑引用，而不是指向物理内存的实际指针。JVM实现可以选择何时替换引用标识，例如：class文件验证阶段、class文件加载后、高频调用发生时、静态编译链接、首次使用时。然后，如果在首次链接解析过程中出错，JVM不得不在后续的调用中，一直上报相同的错误。使用直接引用地址，替换属性字段、方法、类的引用标识被称作绑定（Binding）,这个操作只会被执行一次，因为引用标识都被完全替换掉，无法进行二次操作。如果引用标识指向的类没有被加载（resolved），则JVM会优先加载（load）它。每一个直接引用，就是方法和变量的运行时所存储的相对位置，也就是对应的内存偏移量。Share Between ThreadsHeapMemory ManagementNon-Heap MemoryJust In Time(JIT) compicationMethod AreaClass File structureclassloaderFaster class LoadingWhere is the method areaRun Time Constant poolException TableSymbol TableInterned Strings（StringTable）
```

*   #### **Heap**
    

`` `堆用作为class实例和数据在运行时分配存储空间。数组和对象不能被存储在栈中，因为帧空间在创建时分配，并不可改变。帧中只存储对象或者数组的指针引用。不同于原始类型，和本地变量数组的引用，对象被存储在堆中，所以当方法退出时，这些对象不会被移除。这些对象只会通过垃圾回收来移除。```

*   `` `Young Generation，年轻代 - 在Eden 和 Survivor中来回切换```
    

*   `` `Old Generation (Tenured Generation)，老年代或持久带```
    
*   `` `Permanent Generation```
    

*   #### **Memory Management**
    

`` `对象和数据不会被隐形的回收，只有垃圾回收机制可以释放他们的内存。```

`` `典型的运行流程如下：```

`` `a.新的对象和数组使用年轻代内存空间进行创建```

`` `b.年轻代GC（Minor GC/Young GC）在年轻代内进行垃圾回收。不满足回收条件（依然活跃）的对象，将被移动从eden区移动到survivor区。```

`` `c.老年代GC（Major GC/Full GC）一般会造成应用的线程暂停，将在年轻代中依然活跃的对象，移动到老年代Old Generation (Tenured Generation)。```

`` `d.Permanent Generation区的GC会随着老年代GC一起运行。其中任意一个区域在快用完时，都会触发GC操作。```

*   #### **Non-Heap Memory**
    

`` `属于JVM内部的对象，将在非堆内存区创建。```

`` `非堆内存包括：```

*   `` `Permanent Generation - the method area，方法区 - interned strings，字符串常量```
    
*   `` `Code Cache，代码缓存。通过JIT编译为本地代码的方法所存储的空间。```
    

*   #### **Just In Time (JIT) Compilation**
    

`` `Java字节码通过解释执行，然后，这种方式不如JVM使用本地CPU直接执行本地代码快。为了提供新能，Oracle Hotspot虚拟机寻找热代码（这些代码执行频率很高），把他们编译为本地代码。本地代码被存储在非堆的code cache区内。通过这种方式，Hotspot VM通过最适当的方式，开销额外的编译时间，提高解释执行的效率。```

`` `java运行时数据区域可以按线程每个内部共享和所有线程是否共享来理解。```

*   #### **Method Area**
    

`` `方法区中保存每个类的的详细信息,如下:```

*   Classloader Reference
    
*   Run Time Constant Pool
    

*   Numeric constants
    
*   Field references
    
*   Method References
    
*   Attributes
    

*   Field data
    

*   Per field
    

*   Name
    
*   Type
    
*   Modifiers
    
*   Attributes
    

*   Method data
    

*   Per method
    

*   Name
    
*   Return Type
    
*   Parameter Types (in order)
    
*   Modifiers
    
*   Attributes
    

*   Method code
    

*   Per method
    

*   Bytecodes
    
*   Operand stack size
    
*   Local variable size
    
*   Local variable table
    

*   Exception table
    

*   Per exception handler
    
*   Start point
    
*   End point
    
*   PC offset for handler code
    
*   Constant pool index for exception class being caught
    

### **2.4** **`` `**Class File **数据结构```**

`` `Java：```

```
ClassFile {
```

*   magic, minor\_version, major\_version：JDK规范制定的类文件版本，以及对应的编译器JDK版本.
    
*   constant\_pool：类似符号表，但存储更多的信息。查看“Run Time Constant Pool”章节
    
*   access\_flags：class的修饰符列表
    

*   this\_class：指向constant\_pool中完整类名的索引。如：org/jamesdbloom/foo/Bar
    

*   super\_class：指向constant\_pool中父类完整类名的索引。如：java/lang/Object
    

*   interfaces：指向存储在constant\_pool中，该类实现的所有接口的完整名称的索引集合。
    

*   fields：指向存储在constant\_pool中，该类中所有属性的完成描述的索引集合。
    

*   methods：指向存储在constant\_pool中，该类中所有方法签名的索引集合，如果方法不是抽象或本地方法，则方法体也存储在对应的constant\_pool中。
    

*   attributes：指向存储在constant\_pool中，该类的所有RetentionPolicy.CLASS和RetentionPolicy.RUNTIME级别的标注信息。
    

### **2.5 JVM 运行时内存总结图**

![Image 29](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72ksw2fNvmzm5GLHmjmySZmESunjc0WAp1nsAmt1z1h4iaasia1wxrWjNCA/640?wx_fmt=png)

随着JDK 版本和不同厂商的实现,JVM 内部模型有些细微的不同,如JDK 1.8 永久代 -\> 元数据空间 等等，大体的 JVM 模型还是差不多。

**3.JVM 内存分析原理**
----------------

JVM 内存分析的总目的是希望能够清楚 JVM 各个部分的情况,然后完成TOP N 统计，给出一份 分析报告，方便快递定位判断问题根因。

我们一般使用 jmap 对正在运行的java 进程做 内存 dump形成 Hprof 文件,然后下载到本地离线分析。那么我们在线分析工具面临的第一个问题就是对 hprof 文件的解析。

**3.1 Hprof 数据结构**
------------------

当我们使用 jmap 生成 Hprof 文件,因为它是二进制文件直接打开如下:

![Image 30](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kpSueOIKqcQOeHjaqY9tVrrO3ZKAT67lju0I8TPfIGrUfoav08tQlLw/640?wx_fmt=png)

这种文件非常紧凑没有“分隔符”错一个字节，就会失败，通过 jvm 源码可以查到其有数据结构:

https://hg.openjdk.java.net/jdk/jdk/file/ee1d592a9f53/src/hotspot/share/services/heapDumper.cpp#l62

*   #### **hprof 总体结构**
    

c++：

```
HPRO_FILE{
```

*   **hprof record****总体结构**
    

`Bash：`

```
Record {
```

*   #### **hprof record tags 列表**
    

Record tags 列表比较长,可直接看在线源码:

https://hg.openjdk.java.net/jdk/jdk/file/ee1d592a9f53/src/hotspot/share/services/heapDumper.cpp#l87

Bash:

```
  TAG           BODY       notes
```

HPROF\_HEAP\_DUMP 内容较多，单独从上面抽出来:

https://hg.openjdk.java.net/jdk/jdk/file/ee1d592a9f53/src/hotspot/share/services/heapDumper.cpp#l175

Bash:

```
HPROF_HEAP_DUMP          内存dump 真正存放数据的地方
```

*   #### **HPROF tags**
    

#### Bash:

```
enum  tag {
```

*   #### **Hprof 解析**
    

现在我们知道 hprof 虽然是 二进制格式的文件，但其也有数据结构，就是一条一条 record 记录。那么解析就按照对应的格式来完成其格式解析。

核心解析伪代码:

Go:

```
for {
```

上面代码完成对 Hprof 文件的不停read bytes 并将其解析转换成 结构化的 record。当我们能完成对其转换成 record 记录之后，面临两个问题:一个存储问题，最简单直接存储在内存中，但这种方式依赖主机的物理内存，分析大内存dump 文件会受限制，一个是格式问题，最简单的是存储 record 的 json 格式，这种方式阅读性强，但弱点是数据量比较大，于是我们做了一下调研:

![Image 31](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kCN9GgRtpcHdE49qlKHJ8UNkoYCW5ATdaKqriaKrg1ibfpiabz7Le8wlfQ/640?wx_fmt=png)

*   1G heap dump 文件预计有1300W 条 record 记录。
    

*   2G heap dump 文件预计有2700W 条 record 记录。
    

*   3G heap dump 文件预计有4000W 条 record 记录。
    

*   12G heap dump 文件预计有1亿5千万 条 record 记录。
    

*   满足 insert 要求只能选择 LSM-tree 数据结构类型的 KV 数据库，淘汰了图数据库。
    
*   选用 存储编码后的二进制数据比存入json 格式数据，在耗时和大小上均有1倍以上的提升。
    

综合选择了 LSM-tree 数据结构类型的 KV 数据库leveldb 配合 proto3 进行二进制编码压缩。进过分析产出报告存入后台 mongo 。

**3.2 Hprof 分析**
----------------

当我们理解了 jvm 内存分布，理解并完成了 hprof 文件的解析、存储。那么剩下最后一个步完成对其分析，产出分析报告，这里我们举两个例子：1、线程分析 2、 大对象分析。

下面我们以下面这段代码做成 jar 运行，然后 jmap 生成 heap.hprof 文件进行分析。

Java：

```
# Main.Java
```

*   ### **线程信息分析**
    

我们本地数据库最终得到的是大量的 record 记录，那么这些 record 之间的关联关系，以及如何使用我们通过几个例子初步了解一下。(jstack 能获得更详细的线程信息，从 Heap dump 也能获得线程信息哦)，首先我们通过常用的三个线程来感受一下 record 的关系。

#### main 线程：

Java：

```
Root Thread Object:
```

通过上面例子个跟踪我们基本能获得 虽然都是 record 但是其不同的类型代表不一样的信息，而将他们关联的东西其实就是上面 JVM 运行时数据区里面的描述对应。有 class --\> object instance --\> primitive Array 等等。这里需要读者理解 JVM Run-time Data Areas 以及 CLassFile 的数据结构，来完成 record 的关系。

伪代码:

Go:

```
func (j *Job) ParserHprofThread() error {
```

获得效果图:

![Image 32](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kUYmtMoNH0vv5ykoDtjvsuZBTJfXRiaqChBjqRfIt6Npru6T86wbzg4g/640?wx_fmt=png)

### **3.3 大对象分析**

大对象分析思路分别获得 Instance、 PrimitiveArray 、ObjectArray 这三种对象数据进行 TOP N 排序。

伪代码:

Go:

```
func (a *Analysis) DoAnalysis(identifierSize uint32) ([]*DumpArray, uint64) {
```

效果图：

![Image 33](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72koiaMaribySO1Ynbw3xw8AFBQfOXx5BxfM38ykicXDes1XPurBsGEyrJvw/640?wx_fmt=png)

可以看见最大的对象就是 String 数组，与我们源码写的一致。

**4.JVM分析平台架构**
---------------

通过上面我们完成了对一个 jvm heap dump 文件的解析、存储、分析。于是我们更近一步完成工具平台化，支持在线分析、多JVM 同时分析、支持水平扩容、支持大内存dump 分析、在线开报告等等。

平台架构图:

![Image 34](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kXVOpNpAVs1IOKd0EQC5yB5wGa9y3FwChicQoEQlWxRDvOaDxPLMNp0g/640?wx_fmt=png)

（整体上也是微服务架构,前面网关后面跟各个模块,分析器单独运行,这样可以支持多个并发分析任务。）

使用流程图:

![Image 35](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72knyDEmjzsMekxko8YLaGgAibUSMbS2K4Fw6crpcicz5YpJsmAXckG3qsQ/640?wx_fmt=png)

(对应用户来说我们提供了一键命令执行,这张图介绍一键命令背后的逻辑关系。)

成品效果图:

![Image 36](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72k2n3aNlYNCuseyVzNrLKzpGZyXiaO2vFmD8aRpJuUJzyJS3e1E2f02mg/640?wx_fmt=png)

能看见各个分析任务的实时进度。

![Image 37](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74BpP2CbhkmWYdwcWUrvQ72kpyWwQPO45icNfLHutKu54SPjJTmR66tic2897l4reiaUHKVNicuKvZtjAQ/640?wx_fmt=png)

分析完成之后可查看详细分析报告。

**5.总结与展望**
-----------

本文主要介绍了得物技术保障团队在 Java 内存在线分析方案设计和落地的过程中遇到的问题以及解决方案，解决了研发人员对任何环境JVM实例进行快速内存Dump 和在线查看分析报告,免去一些列dump文件制作、下载、安装工具分析等等。

未来得物技术保障团队计划继续开发Java 线程分析,Java GC log 分析等等。形成对一个JVM 实例从内存、线程、GC 情况全方位分析，提升排查Java 应用性能问题效率。

**Reference:**

《Java 虚拟机规范(Java SE 8 版)》

《深入理解Java 虚拟机》

https://www.taogenjia.com/2020/06/19/jvm-runtime-data-areas/

https://wu-sheng.github.io/me/articles/JVMInternals.html

https://wu-sheng.github.io/me/articles/JVMInternals-p2.html

**\*文**/Bruce

 关注得物技术，每周一三五晚18:30更新技术干货  
要是觉得文章对你有帮助的话，欢迎评论转发点赞～

**活动推荐：**

**[云原生&数据库-得物技术沙龙，限时免费报名来啦](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247489128&idx=1&sn=0c59f42587f4dd089bb32fabe3f8c10a&chksm=c1624337f615ca213342a10ac352eabd5e16f575814358fc945e1459ac66552bad52e2f760c3&scene=21#wechat_redirect)  
**

得物技术公众号后台 回复「沙龙」进群，不迷路！  
报名方式：  
**云原生专场**：关注 InfoQ视频号  **7月9日13:50开播**  
**数据库专场**：关注51CTO技术栈视频号 **7月9日 13:50开播**
-------------------------------------------------------------------------------------------------------------------

或者 得物Tech视频号预约：
