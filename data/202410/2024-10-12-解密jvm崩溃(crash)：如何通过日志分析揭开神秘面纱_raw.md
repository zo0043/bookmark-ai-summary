Title: 解密JVM崩溃(Crash)：如何通过日志分析揭开神秘面纱｜得物技术

URL Source: https://mp.weixin.qq.com/s/_DOQGBmhfV-LUzb03RcTCQ

Markdown Content:
Weixin Official Accounts Platform
===============

             

 

![Image 1: cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYUwbCPdacChrOD8o8ec2ZUMy5lL4ZQBKX0Voshp7ic1nibRv15j7Q8aJQ/0?wx_fmt=jpeg)

解密JVM崩溃(Crash)：如何通过日志分析揭开神秘面纱｜得物技术
==================================

Original 财神 [得物技术](javascript:void\(0\);)

_2024年08月14日 10:31_

![Image 2](https://mmbiz.qpic.cn/mmbiz_gif/AAQtmjCc74DZeqm2Rc4qc7ocVLZVd8FOASKicbMfKsaziasqIDXGPt8yR8anxPO3NCF4a4DkYCACam4oNAOBmSbA/640?wx_fmt=gif)

**目录**

一、前言

二、什么是崩溃？

三、一个例子

四、崩溃日志详解

1\. 文件路径

2\. 信息摘要

五、core文件

1. 问题调用栈

2. 帧快照

3. 汇编源码还原

4. 内存映射

六、一些经验

1\. 虚拟机崩溃的原因分类

2. 留意JNI

3. 敢于怀疑

七、写在最后

**一**

**前言**

当使用Java来构建一个复杂的软件系统时，系统偶发性崩溃（也会被称为**Crash**）是一个不小的挑战。这种情况不出现则已，一出现可能会对系统的稳定性和可靠性产生相当大的负面影响，同时也会给终端用户带来不良体验。在本文中，我们将基于崩溃的现场进行深入探讨以及如何通过技术手段来识别、调试和解决这些问题。同时我们将深入研究如何利用现代开发工具和最佳实践来减少系统崩溃的可能性，进而提高系统的稳定性和可靠性。

**二**

**什么是崩溃？**

**简而言之，就是我们常说的 - 系统挂了，进程消失了。**

当发生一般的问题情况时，研发人员就像是消防员一样，需要火速赶到现场，分析日志，检查堆栈，然后试图重现并解决问题。这个过程就像一场紧急救援任务，需要迅速、果断的行动，同时也需要谨慎对待，以避免引入更多问题。

但偶发性崩溃会更难处理。因为系统留给我们可用于排查的信息并不够多，甚至于重启后这样的崩溃再也不会发生。这个解决问题的过程就像是一场复杂的推理游戏，需要耐心和技巧。幸运的是，虚拟机还是给我们留下了一点蛛丝马迹供我们来进行深入的定位和跟踪。

**三**

**一个例子  
**

为了更进一步深入的探寻虚拟机崩溃背后的细节，我尝试给出一段异常代码：

```
import sun.misc.Unsafe;
```

Unsafe类是一种非常强大且危险的工具，它提供了直接操作内存和执行低级别代码的能力。这个类通常被用于开发高性能的并发框架和底层操作系统相关的功能。由于使用Unsafe类可以绕过Java语言的一些安全检查，因此需要非常小心地使用，否则可能会导致严重的内存错误和安全漏洞。如上代码所示，我们尝试在一个非法的内存区域读取数据。当执行完成后我们立刻会在控制台看到如下输出：

![Image 3](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYmWEg47VMlPfZTIJibwx2wwS5gPevbSwVFiaXsxQN9EXj2eQA4AmWLXdg/640?wx_fmt=png&from=appmsg)

好了，我们的程序此刻已经崩溃了。虚拟机在也在崩溃的控制台日志清楚的提示我们**“A fatal error has been detected by the Java Runtime Environment.”**

**四**

**崩溃日志详解**

上述控制台日志只是对于当前虚拟机崩溃的一个概要说明。在崩溃时虚拟机会帮我们生成两份日志文件。一份是进程的coredump文件，由操作系统负责生成；另一份是Java虚拟机自己在崩溃时生成。这两部分日志对我们问题的排查都有极大的作用。这里我们着重介绍Java虚拟机生成的这部分日志的细节。

**文件路径**

当Java程序崩溃时，默认情况下会在当前进程运行目录来生成形如**`hs_err_pid%p.log`** 的文件。这里的**`%p`**为通配符，系统会自动转化为当前的进程PID。例如Java进程编号为1941生成的文件名即为**`hs_err_pid1941.log`**。同时，虚拟机还提供了**`-XX:ErrorFile`**选项来帮助我们自定义文件的生成位置。比如我们想要把文件存储到系统任意指定目录下，可以指定启动参数形如：**`-XX:ErrorFile=/home/admin/hs_err_pid%p.log`**。需要注意的是，如果由于一些异常原因在工作目录无法存储(比如写入权限不足)，则该文件会被存储在操作系统的临时目录下。在Linux操作系统环境下，这个地址是**`/tmp`**。

**信息概要**

崩溃日志包含在系统崩溃发生时获取到的相关信息，具体包括如下（包括但不限于）：

*   导致进程崩溃的操作异常或信号
    
*   版本和配置信息
    
*   导致进程崩溃的线程的详细信息和线程的堆栈跟踪
    
*   正在运行的线程列表及其状态
    
*   关于堆的摘要信息
    
*   加载的本地库列表
    
*   命令行参数
    
*   环境变量
    
*   关于操作系统和CPU的详细信息
    

而在Java虚拟机崩溃时，生产的崩溃日志文件默认会分为4大部分内容：

*   提供崩溃简要描述的头部信息
    
*   线程信息
    
*   进程信息
    
*   系统信息
    

为了方便查阅，以下的章节中，我在认为相对关键的地方都打上了星号(※)，用来表示该小节内容在问题排查时要多留意，是日志能给出线索的相对高发地点。

**头部信息**

![Image 4](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYLo61rZRtd4SRRCqWIVFw7hJC8I7BGoyXWzRR26Z56vgvGhkjuxeLxg/640?wx_fmt=png&from=appmsg)

一个示例：虚拟机收到意外信号发生崩溃

如上所示，崩溃日志的开始部分其实就是我们在控制台刚才看到的那部分内容，崩溃日志文件的头部用简明扼要的方式描述了Java进程崩溃的根本原因。在这个区域我们暂时只需要关心3个信息。

※ **崩溃原因**

崩溃的具体原因可见图中第二行，这里一般会给出系统崩溃的原因。我们可以简单的分析为下图：

```
   SIGSEGV (0xb) at pc=0x417789d7, pid=21139, tid=1024
```

这里有三个信息极为重要：**信号名称、程序计数器、线程ID**。它会是我们后续排查问题用到的前置信息，在此先按下不表，下文中会陆续说明。

※ **问题帧栈**

第二个关键的点是出问题的帧栈，这等于是告诉了我们代码是运行在什么地方触发了上面的崩溃原因。比如下方的示例，我们可以看到是执行到了虚拟机内部代码(用大写字母V来表示)的函数**Unsafe\_GetNativeInt**进而触发了系统崩溃。

```
# Problematic frame:
```

**栈帧(frame)**表示程序运行时函数调用栈中的某一帧。简单来说可以理解为调用某个方法。

这里帧栈前面的大写字母也有特定含义。

![Image 5](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYzK594yxJluMnicyXc7gQFvF44s4z5FHygTU2MC9g0Qpiaibm92LkMaHTQ/640?wx_fmt=png&from=appmsg)

※ **核心转储文件**

头部信息里有一句话也很重要。

![Image 6](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYtcnAoEGc4znyRVwvToibwHqrwFQbww0vz6S0bpwLwU9BameyLsKElMQ/640?wx_fmt=png&from=appmsg)

这意味着进程在崩溃的时候顺便帮我们生成了核心转储文件(coredump)。关于核心转储文件，它是操作系统在进程收到某些信号而终止运行时，将此时进程地址空间的内容以及有关进程状态的其他信息写入一个磁盘文件。相比Java本身的崩溃文件，他后续还可以使用诸如gdb的工具进行调试。核心转储文件对于问题调试还是非常有用的：

*   **完整性和全局视角**：操作系统的coredump包含了整个进程的内存转储，包括了JVM 本身的内存以及 JVM 进程所依赖的操作系统资源的状态。这提供了更全面的视角，有助于诊断问题的根源。
    
*   **内存信息**：操作系统的coredump包含了进程的完整内存镜像，包括了堆和栈的信息，这对于分析内存状态以及发现内存相关的问题非常重要。
    
*   **操作系统资源状态**：coredump还可以提供操作系统级别的资源状态信息，例如打开的文件、网络连接等。这些信息可以帮助诊断和解决一些与操作系统资源相关的问题。
    
*   **与调试器的兼容性**：一些调试器可能更喜欢使用操作系统的coredump进行分析和调试。在某些情况下，使用coredump可能更容易进行深入的调试和分析。
    

**线程信息**

这部分包含了刚刚崩溃的线程的信息，大部分情况下，这里是我们需要核心关注的点。虚拟机从线程视角清晰的描绘了当系统崩溃的那一时刻的数据情况。

**※ 线程概要**

![Image 7](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYJRVaAgujAuibDoe9D7PLvcHyd48vCmq1Z27OTnoKpJqwUblLrVicn7Qg/640?wx_fmt=png&from=appmsg)

虚拟机开门见山的给出了线程的基本信息。我们可以用下方的图示来简要说明：

```
7feed0009800 JavaThread "main" [_thread_in_vm, id=37696, stack]
```

上述线程信息我们可以主动先尝试忽略部分内容(比如线程内存指针是指向虚拟机内部线程结构的指针，大部分情况下我们排查问题都用不到)，我们这里可以优先关注2个内容，以上图为例：

※ **线程类型**

如上图所示，我们的线程类型是**`JavaThread`**。在Hotspot虚拟机中，线程的类型有很多种：

*   **`JavaThread`**
    
*   **`VMThread`**
    
*   **`CompilerThread`**
    
*   **`GCTaskThread`**
    
*   **`WatcherThread`**
    
*   **`ConcurrentMarkSweepThread`**
    
*   **`JvmtiAgentThread`**
    
*   **`ServiceThread`**
    
*   **`CodeCacheSweeperThread`**
    
*   ...
    

它们有的负责Java代码的编译、有的负责GC的执行、有的负责缓存的清理，最终各司其职完成了虚拟机内部的各种操作。上述例子中的**`JavaThread`**我们暂时可以认为他是一个标准的Java代码启动的线程。

**※ 线程状态**

上述信息里还有一个关键信息是**`_thread_in_vm`**，它表示了线程当前所处的状态。

![Image 8](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYT9jozBwuukQsJaXcNNC6FJsK9iaPm0tparwk2fibP3L9kZFY75WrwuKg/640?wx_fmt=png&from=appmsg)

这些状态基本上和我们熟知的线程状态所对应。在一些比较极限的场景下，还会有一些瞬时的“中转”状态。

![Image 9](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYXxSgMGD93BD35JHCpmgwsHC0ibBu2NsdBPp2ekCicFeib6ZZY4TuWKjeQ/640?wx_fmt=png&from=appmsg)

Hotspot虚拟机在这里将线程的状态划分的更为清楚，便于技术人员第一时间知道线程到底处于一种什么样的状态下，进而可以更快速的定位到具体的问题。

**※ 信号量概要**

接下来，虚拟机在这里描述了导致进程终止的意外信号。

![Image 10](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYQFdSxLBLUX8kkjbYibwAvs7qSicfyJ8XL6GZnsibVvhOrgZWalwwmnjZA/640?wx_fmt=png&from=appmsg)

在本文的示例中，异常码是11，它对应的信号量是**`SIGSEGV`**，这是崩溃时最为常见的一种信号量，意味着当前进程正在从非法内存值读取内容(si\_addr)。简单来说，每个进程所能读写的内存是有一定范围的，如果超出这个范围进行内存读写是会被操作系统认为是非法的操作。**`SIGSEGV`**同时下面有2种不同的si\_code，分别是**`SEGV_MAPERR`**(未映射的地址)、**`SEGV_ACCERR`**(无效的访问许可)。

我们知道了信号量的概念后，再聊点题外话，**`SIGSEGV`**的本质是内存的非法访问，这其实是非常严重的错误。所以很多语言碰到类似问题会默认让系统崩溃(因为非法访问的后果谁也不知道，所以干脆崩了算了避免更意外的情况)，Java虚拟机当然也遵从了这个约定。但是在Java虚拟机内部，有两种特殊的场景本质也是内存非法访问且接收到了**`SIGSEGV`**，但系统并没有崩溃且还能继续运行：

*   **`NullPointerException`**
    
*   **`StackoverflowError`**
    

这种例外情况我们需要特殊说明。我们先来看看一个标准的**`SIGSEGV`**信号到来时进程的时序：

*   进程正常执行指令
    
*   内存非法访问
    
*   进程收到操作系统发来的SIGSEGV信号量
    
*   **若进程注册了信号回调函数，则执行，否则默认结束进程**
    

上面的关键就在最后的**回调函数**。如果进程主动注册了信号回调函数，则可以在注册的函数内部选择性的忽略指定信号(这样系统就不会挂了)，来提升整体的代码稳定性和健壮性。Java虚拟机内部的处理源码感兴趣的可以见下方：

```
==================== os_linux_x86.cpp ==================== 
```

**※ 寄存器**

![Image 11](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYPJzx9EDib0FxEd6bEIvm10sbetW80XjwSsJX16dpBaEPFaG3Vg8VyOQ/640?wx_fmt=png&from=appmsg)

错误日志中的下一个信息显示了致命错误发生时的寄存器上下文。这个输出的确切格式取决于处理器。当与\[指令上下文\]这一节结合来看时，寄存器的数值可能会很有用。在当前基本都是x86-64的架构下，寄存器的简单描述如下：

![Image 12](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYQ4icDNd6TExvSDNWL8iaYlEPh5jnFMYwicZocwibyTezG06mDrW70dCATA/640?wx_fmt=png&from=appmsg)

但我们这里如果单纯记每个寄存器的作用的话未免过于枯燥和乏味，我们需要的是找到系统崩溃的原因。除了和指令结合使用，这里也可以优先关注下**通用寄存器**中的内存值，很多时候是个初步的突破口。

![Image 13](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYvBJia3nBicJgVG2qojrUOk98yQ58P7CfoD7PYpd8wsIH38E1mqqLgW6g/640?wx_fmt=png&from=appmsg)

以上图为例，64位操作系统下用户空间地址范围为**\[0-0x00007FFFFFFFF000\]****，**我们对照上述寄存器内的数据来看很快便发现R12寄存器的地址是**`0xffffffffffffffff`**。这显然不是一个合法的地址，从而也进一步的印证了日志开头给出的**`SIGSEGV`**错误。

**栈地址**

![Image 14](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYIkQvSZP2hGQCHZG2tUzZjAXjiaDc4IBNINkpPh7Dia9KCfa0CmcSs1QA/640?wx_fmt=png&from=appmsg)

进一步的，虚拟机给出了出问题的线程的帧栈地址数据，如果不考虑后面的core文件分析的情况下，大多数场景下这些密密麻麻的字符对我们来说可参考的意义并不大，可以简短了解即可。

*   虚拟机给出了sp指针指向的地址，这会和上面的rsp寄存器(栈顶)位置对应。
    
*   X86-64的机器上，每一行对应了16个字节，后续两列每一列的内容16进制输出。
    

**※ 指令上下文**

![Image 15](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYLscFNMwZhlZ3JHOticC95QZRBUB3R6Gp1QCNCtSV4ne1CrT3jV7GnPg/640?wx_fmt=png&from=appmsg)

指令上下文输出了出问题前后的64字节的操作码。这在一些比较难以排查的问题场景下还是很有极大作用的。简单来说，虽然我们处在Java的语言环境里，但和操作系统的背后交互其实还是一条条毫无感情的机器码。而上述地址对应的指令数据就是背后要执行的机器码。但因为机器码过于晦涩，我们的前人才搞出了汇编语言这么个东西让开发的过程变得不那么繁琐。而这些操作码可以通过反汇编器进行解码，以生成崩溃位置附近的指令。

上述pc地址对应的汇编是(网上有很多在线反汇编解码工具)：

```
0x00007faaf1397702:  45 8B 24 24             mov r12d, dword ptr [r12]
```

由于我们已经已知R12的地址有问题，无法读取自己管控内存地址之外的数据。所以我们很快可以初步判定是这一行汇编的问题：**`mov r12d, dword ptr [r12]`**。它的含义是从R12寄存器取双字读取32位的值，然后保存在R12寄存器的低位中。在结合上下文函数帧知道出错的地方是unsafe的getInt方法，而getInt方法的入参的含义本身就需要传入准确的地址信息，那么这个问题的答案就基本已经付出水面了。

**※ 寄存器内容**

![Image 16](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYCCmNVXThBH3V84lfOepYWJO7ISqaDYae54aVJnicWCC7Cwer855BhLQ/640?wx_fmt=png&from=appmsg)

这部分可以看做是对于之前的寄存器那一节的具体说明。之前相对晦涩的地址，在这里虚拟机给出了当前地址代表的具体内容，以截图为例：

*   RAX、RBX、R15是线程
    
*   RCX、R11指向动态链接库中
    
*   RDX、RSP、RBP、R14均指向线程中
    
*   R8、R13指向某个具体方法
    
*   R10指向解释模式中的某个代码片段
    
*   RSI、RDI、R9、R12均指向一个未知的值(an unknown value)
    

这里还是要说明，未知的值并不一定是问题，但是如果地址本身就是一个非法地址则是需要重点关注的事情。

**※ 帧栈明细**

![Image 17](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY0qB3RCXZGggB072tPiaFN6kxNgSuBfyeMgCicNT8f7iapvtWhl4ibZv3cg/640?wx_fmt=png&from=appmsg)

按照顺序，接下来的输出是线程帧栈的细节，如上所示。

首先给出的是问题栈的区间和栈顶地址以及剩余的空间，接着，如果可能的话会打印堆栈帧且最多打印 100 个帧。对于 C/C++ 帧，可能还会打印库名称。

然后为了更清楚的看到调用帧的明细，虚拟机把这里的内容分成了两部分：

*   **Native frames**
    
*   **Java frames**
    

简单来说他们的区别是Native帧没有考虑到由运行时编译器内联的Java方法，而Java帧会考虑内联。同时Native帧会打印线程的所有函数调用，相对Java帧会更详细。

**进程信息**

**※ 进程里的线程**

首先映入眼帘的是进程内的线程信息，这里展示了虚拟机内部的Java线程以及其它线程信息。特别需要注意的是“=\>”这个符号，它标识了哪个线程是当前的线程。

![Image 18](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYMSkx5X5ZBUIYRy7QupAH5RmVJp16pYibg6gIGXudlBZibPuRiakPaZcLg/640?wx_fmt=png&from=appmsg)

具体线程的描述过程在线程信息这一节已经说过，在此不做赘述。

**※ 虚拟机安全状态**

接下来的内容是虚拟机的安全点状态信息。注意这里的状态描述 **` not at safepoint`**。

![Image 19](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYwLyMecccERUhyM6mIaqOhWCXh3lJkMPEibyP4knIxnW0HFTianugrLEA/640?wx_fmt=png&from=appmsg)

这里的虚拟机状态可分为3种情况：

*   not at safepoint (正常情况)
    
*   at safepoint (所有线程处于安全点等待VM进行一些重要的操作。如GC、Debug等)
    
*   synchronizing (这是个一个**瞬时的状态**。VM等待所有线程到达safepoint，已经达到safepoint的线程会挂起)
    

很自然的，如果你看到这里的VM state显示的如果是at safepoint，那就要稍微留意一下和GC相关的细节(虽然safepoint并不代表一定有GC)。关于safepoint更多的细节，可见之前我写的一篇文章[Java程序陷入时间裂缝：探索代码深处的神秘停顿｜得物技术](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247525463&idx=1&sn=78d614e3e45c0b461110affb38ca8714&chksm=c1613108f616b81e44dcd159a1e1910c46f656f70efcb13b0a011823bb3d4bc50491a6857459&scene=21#wechat_redirect)

**锁&监视器**

![Image 20](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYvFzoMrtYSEJNxIdSSUTyiamz3YQjlic0lW05Lia7BZ5TuHaeSLaBehU7w/640?wx_fmt=png&from=appmsg)

接下来，虚拟机给出了当前线程拥有的互斥锁**`Mutex`**和监视器**`Monitor`**列表。**特别需要注意的是：这些互斥锁和监视器是虚拟机内部的锁和监视器，而不是与Java对象相关的锁和监视器。**所以绝大多数的崩溃文件下，这里的输出都是None。

**※ 内存使用摘要**

![Image 21](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYd5Dv5ibFcWMVeYm9Mcibl5cjHiaZbowWly4iaONAfFdJv78MqrSGzayNrw/640?wx_fmt=png&from=appmsg)

这里是虚拟机堆区的内容，对于Java程序员来说，这块内容看着就熟悉多了。我们逐一来分析看看。

**内存基础模型**

*   **heap address: 0x00000006c0000000**
    
*   **size: 4096 MB**
    

这里交代了内存的基本信息，**`heap address`** 说明了当前我们进程的虚拟内存地址的起始地址。而**`size`**则表示当前进程预留(申请)了多大的内存，如图所示为4096MB，即4G。这些信息得记下来，如果遇到诸如物理内存不足的问题，这些都是关键的上下文信息。

*   **Compressed Oops mode: Zero based**
    
*   **Oop shift amount: 3**
    

这里的 **`  Compressed Oops mode `** 稍微有点难懂，它表示了虚拟机在内部对于对象的压缩模式(也称之为压缩指针技术)。在32位系统上，对象指针通常占用4个字节（32位），而在64位系统上，对象指针通常需要8个字节（64位）。**这意味着在64位系统上，对象指针的大小会比在32位系统上大**。但因为我们现在基本上都在使用64位的系统，为了节省内存空间，JVM引入了压缩指针技术。这种技术通过在64位系统上使用更小的指针来表示对象的引用，从而减小了对象指针的大小。在压缩指针模式下，JVM会将对象指针压缩为32位，然后通过一些额外的计算来还原成对应的64位地址。在大内存服务场景下，带来的收益会相当可观。然后在Hotspot内部定义了四种模式分为四种 UnscaledNarrowOop(32位)、**ZeroBasedNarrowOop(无基址的32位压缩)**、DisjointBaseNarrowOop(分离基址压缩指针)、HeapBasedNarrowOop(指定基地址的32位压缩，可以用-XX:HeapBaseMinAddress来指定)。可以看到我们系统默认时会使用压缩指针来完成空间的节省。

再来看看**`Oop shift amount`**，它实际上代表了内存对象压缩的偏移算法。在讲这个之前要提一下当前Hotspot虚拟机的一个重要基础：**HotSpot虚拟机的内存模型要求对象起始地址和对象大小必须是8字节的整数倍，换句话说就是任何对象的大小都必须是8字节的整数倍，如果大小不足会强制填充(向上对齐)到8字节的整数倍。**比如一个对象实际大小为12字节，那么实际在Hotspot内部存储会被对齐为16字节。这个基础的前提极为重要，虚拟机内部的多处优化都是因为有这个内存限制的前提才得以进行。

我们继续说回**`Oop shift amount`**。它的值是3，虚拟机采用的对象压缩方式是地址右移，所以它的根本意思就是内存需要右移3位来存储，内存真正使用时按照左移3位来使用。**由于对象和内存起始地址都是按照8字节对齐，所以内存地址的后3位必然是0，该过程不会丢失任何信息。**所以一个完整的内存换算公式如下所示：

**`<narrow-oop-base> + (<narrow-oop> << 3) + <field-offset>`**

以上述截图中的地址0x00000006c02bb8e8来举例，它实际经过压缩后在虚拟机内部存储的地址是

**`0 + (0x00000006c02bb8e8<<<3) = 0xd805771d。`**

*   **Narrow klass base: 0x0000000000000000**
    
*   **Narrow klass shift: 3**
    

和之前类似，只不过前面说的是对象，这里说的是klass(类的元数据)。和对象相比，元数据的基地址默认从0开始，存储位置位于我们熟知的Metaspace空间内。其他语义类似，在此不做赘述。

*   **Compressed class space size: 1073741824**
    
*   **Address: 0x00000007c0000000**
    

继续看细节。这里的 **`  Compressed class space size `** 便是我们熟悉的Metaspace区域大大小。这里的1073741824换算过来就是1GB。这也是未配置该区域大小时Hotspot给出的默认值。Address代表了Metaspace的大小是从内存地址0x00000007c0000000开始。

**内存使用明细**

这里虚拟机描述的很清楚了，大多数信息不用解释大家也看的明白。这里唯一需要提一下的是这个内存边界表达，比如from区域的内存被描述为\[0x00000006c4450000, 0x00000006c4450000, 0x00000006c4cd0000)。它的含义是内存区域从0x00000006c4450000开始，到0x00000006c4cd0000结束，0x00000006c4450000是当前已使用的标记位置。大多数情况下，如果下次有内存分配将会从0x00000006c4450000处开始继续分配。但需要注意的是，我的示例采用了cms垃圾回收，如果采用g1模型，那这块内容的输出会稍有不同。

虽然这个图描述的已经足够清晰，但是我还是画一个图来描述下上述内存区域的具体使用情况，会更直观：

![Image 22](https://mmbiz.qpic.cn/mmbiz_jpg/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY6VDXwWEia9abL43icRA6cicHJmwlX1sIjv6qdXficDRAic7WlXa85mtsmLg/640?wx_fmt=jpeg&from=appmsg)

**GC辅助模型**

![Image 23](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYu9bxc1qicI4g2XMZZhXuM4YlAo4WS7icJaOVsM1eib34OPMa8Ov7a1CVg/640?wx_fmt=png&from=appmsg)

这里的内容依然和GC相关，但对于问题的排查相关性都不大，在这里只简单说明下卡表(Card table byte\_map):

卡表是一个标准的空间换时间的解决方案。卡表通常在 JVM 中实现为单字节数组。当我们把 JVM 划分成不同区域的时候，每一个区域（通常是4k字节）就得到了一个标志位。每一位为 1 的时候，表明这个区域为 dirty，持有新生代对象，否则这个区域不持有新生代对象。这样，新生代垃圾收集器在收集live set 的时候，可以通过以下两个操作：

*   从栈/方法区出发，进入新生代扫描。
    
*   从栈/方法区出发，进入老年代扫描，且只扫描 dirty 的区域，略过其他区域。
    

**polling page**

![Image 24](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY0xcsbtLInn6bwK9A4SWAvHicUDDoSvwTzQTt7lgWyJnjPskVdNKNwKg/640?wx_fmt=png&from=appmsg)

这里的Polling page其实对我们的问题排查并无多大意义，但确实是一个有意思的知识点，它和我们熟知的JIT下的GC有关系。简单来说：

*   JIT下虚拟机在指定代码位置完成安全点代码的放置，代码的内容是读取一小块内存(就是这里的polling page)
    
*   GC时设置这块内存不可读
    
*   其他线程代码运行到安全点发现代码不可读，操作系统层面抛出SIGSEGV信号
    
*   虚拟机在启动是就完成SIGSEGV信号注册，来监听本次SIGSEGV的内存代码是否是polling page位置
    
*   如果是，进程不终止，当前线程进入安全点，线程挂起为后续GC做准备
    

可以看到，一个很细小的功能，虚拟机也是花费了很大精力，这里回头可以总结一篇文章来深入聊聊。

**CodeCache**

![Image 25](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYtd4OiafUw3N3t4u3t9dW4iaeOH2QcfPJD7Hp7pm4VpLpRjT9y1VUO9Aw/640?wx_fmt=png&from=appmsg)

关于CodeCache是什么这里就不多做赘述。这里稍微解释下日志里出现的部分内容。

首先日志给出了整个CodeCahe的使用情况，第一行给出了总大小(**245760kb**)，已使用(**1080kb**)，空闲(**244679kb**)。第二行用更直观的方式给出了内存上下界(**bounds**)。以上图为例，这里的0x00007faadcbc0000代表了CodeCache内存区域的下界，对应的0x00007faaebbc0000则是内存上界，0x00007faadce30000代表的是已使用内存的边界(可以理解这个边界就是已使用的指针)。

CodeCache内部本质上是各种大小不一的内存块。有的是方法经由JIT编译后的代码，有的是动态生成的元数据等等。当前系统一共有253个内存块，其中10个JIT编译过的方法，以及160个adapters。这些adapters其实是虚拟机内部在解释模式和编译模式下的一种适配，所有方法的默认入口都是解释模式，虚拟机内部会判断当前方法是否已经编译过了，如果已编译则基于adapter路由到已编译的方法，否则继续解释执行。整体如下图所示。

![Image 26](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYvDxNLTwXJEicpToxAqBr8EAZquhdL0FvfhOYz0ic8GYRiaiaWc16PW0A8w/640?wx_fmt=png&from=appmsg)

**事件分析**

**※ 编译事件(Compilation events)**

![Image 27](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYeGYonW0yC4xeXT7c4Du3H4sMibyAB0ia64zLuxNiccgoDrdyWJxaEpesQ/640?wx_fmt=png&from=appmsg)

Compilation events 显示了最近10次从Java字节码编译为机器码的方法。这里有一个需要关注的点：**如果你的机器多次崩溃看到的编译事件都相同，可能意味着JVM正在错误的编译当前方法。**如果不明白为何虚拟机会出现这种错误，你可以尝试重写方法将其简化、拆分等，这将有助于你避免相关的崩溃问题。或者也可以利用虚拟机提供的命令来禁止指定方法的编译，比如：

**`-XX:CompileCommand="exclude java.util.ArrayList::add"`**

**GC历史事件(GC Heap History)**

![Image 28](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYBicc9jukxapxjLk3oqv6QzzcCeYxpEibyFrOHFJXO81QuicRPHtOgNawA/640?wx_fmt=png&from=appmsg)

这里列举出了系统在崩溃时出现的近10次GC。这里的堆的输出模型和之前章节讲述的模型类似，在此就不再做过多说明。

**※ 逆优化事件(Deoptimization events)**

![Image 29](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYxibneJgBYLdgym5P0g7KibmUlLlSggAB6HHkCn6ibbMI4jrQKblyd1pMA/640?wx_fmt=png&from=appmsg)

关于逆优化简而言之，就是JIT基于特定条件和假设完成代码编译后，在一些场景下，虚拟机突然发现当前的特定条件和假设不满足，当前编译好的方法如果继续执行会发生一些意料之外的情况，此时虚拟机就会触发自动逆优化，针对已经编译好的方法做特定处理，确保整体运行准确。

我们来简单基于日志分析下当前的事件内容：

首先能看到的是触发本次逆优化的原因(**`reason`**)，在Hotspot虚拟机内部可能的共有32种。限于篇幅我们不可能全部拿出来在这里进行说明，我们可以选一些有代表性的：

*   Reason\_null\_check(虚拟机看到了预期之外的null值)
    
*   Reason\_range\_check(虚拟机看到了预期之外的数组下标)
    
*   Reason\_class\_check(虚拟机看到了预期之外的对象类型)
    
*   Reason\_unstable\_if(分支预测失效，比如一个if始终返回false，突然一次返回了true)
    

其次我们看到的是Hotspot对于这些触发的场景的针对动作(**`action`**)，一共5种：

*   Action\_none(直接切换到之前的解释模式执行方法，保留之前JIT编译好的方法)
    
*   Action\_maybe\_recompile(JIT重新编译当前方法)
    
*   Action\_reinterpret(临时切回解释模式执行方法，废弃之前JIT编译的方法然后内部再决策是否需要重新编译)
    
*   Action\_make\_not\_entrant(JIT立即重新编译且废弃之前JIT编译好的方法，下次调用就会使用新的编译结果)
    
*   Action\_make\_not\_compilable(直接切换到之前的解释模式执行方法，废弃之前JIT编译好的方法且不再编译)
    

可以看到虚拟机基于不同的逆优化给出了各种解决方案，确保程序的正常运行。

最后，method给出了具体涉及本次逆优化的方法，如上图所示的"java.util.Matcher.match()" 。

和前文所说的编译事件(Compilation events)类似，**如果你的机器多次崩溃看到的逆优化事件都相同，可能意味着JVM正在错误的逆优化当前方法**。对应的解决方案也是相同的：**如果不明白为何虚拟机会出现这种错误，你可以尝试重写方法将其简化、拆分或者使用指令****`-XX:CompileCommand`****。**

**※ 类重定义事件(Classes redefined)**

![Image 30](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYbHkKMkrvmcvKa1pibgdMyI1KMnKiaaHVh10ODdOIzWLWRwMLdZXjEgTw/640?wx_fmt=png&from=appmsg)

这里列举出了当前Java进程中类被重定义(**`redefined`**)的相关信息。上述时间可以简单的理解为：**`Crash`**这个类在应用启动的第18.707秒被重新定义，当前类总计被重定义1次。这里有个小细节，**`java.lang.Class`**中会保存一个类被重定义的次数到它的实例元数据中，可见**`java.lang.Class#classRedefinedCount`**。

上面说的重定义是JDK5中引入的**`Instrument`**接口提供的一种在运行时修改Java类文件的机制，以实现类的重新定义。我们熟知的Arhtas、Byteman、Greys、Skywalking、Pinpoint等都是基于**`Instrument`**机制来完成了各种强大的监控功能。但尽管**`Instrument`**接口当前已经被如此的广泛运用，但它仍然存在一些潜在的问题和坏处：

*   **难以调试**：由于动态修改类文件会改变程序的行为，可能会导致调试困难，不利于排查问题。
    
*   **兼容性问题**：重新定义类可能会影响现有代码的兼容性，导致原有功能无法正常运行。
    
*   **不稳定性**：对类进行重新定义可能会导致系统不稳定，产生意外的行为(如系统崩溃)。
    

因此，尽管**`Instrument`**接口提供了强大的功能，但大多时候我们建议在生产环境使用时还需要慎重考虑，确保当前使用的组件足够成熟，否则带来的后果会非常严重。以我们常见的Arthas为例，导致线上应用崩溃的问题很常见：

*   https://github.com/alibaba/arthas/issues/1589
    
*   https://github.com/alibaba/arthas/issues/915
    

**内部异常事件(Internal exceptions)**

![Image 31](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYyWVf86cTia8gs7fZeiblbhO1WPEK48Hy9m0aiaoP4ia5wVFEeNxwF5NYUg/640?wx_fmt=png&from=appmsg)

这里透出了虚拟机内部的异常事件，这些事件包括了虚拟机内部的各种异常诸如生成OopMap的异常、jni调用相关的异常、虚拟机内部执行的逆优化问题、JIT相关的NPE等等等等。需要特别注意“内部”这两个字。这意味着我们业务代码层面的异常抛出是不会在这里出现的，所以这里我们可暂时无需过多关注。

**通用事件(Events)**

![Image 32](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYhSNiclm1ofBGjJJzn6EsxIvaoyu4icJEnurhDJNr3OTicOPdicicITUUn0g/640?wx_fmt=png&from=appmsg)

这里的日志输出稍微有点迷惑，初看会给人一种所有事件汇总在一起的感觉。但这个区域实际的含义是：A log for generic messages that aren't well categorized。即通用未分类的事件内容都在这里，是个事件的大杂烩。包括但不限于如下场景：

*   类加载(如上图所示)
    
*   新增线程
    
*   GC后的内存整理
    
*   虚拟机线程执行重要的操作(VMOperation)
    
*   JIT方法废弃的内存清理
    
*   ...
    

总之，这里依然是一个可以用来了解虚拟机在做什么事情，但是大多数情况对于我们问题的排查起不到太大作用的信息区域。

**内存映射明细**

![Image 33](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY7icAWNkaZGMwUN5PibYbiaiakbDqZYgmJ8qYgGFsN9O665w0J1VKyvEOoQ/640?wx_fmt=png&from=appmsg)

这里其实就是当前进程在临"死"前，**`pmap -d pid`**命令输出的结果。我们关注一些重要的列：

*   **\[第1列\]显示内存区域的起始地址。每个区域代表进程的不同内存映射。**
    
*   **\[第2列\]内存映射区域的访问权限。这里的p代表的是(private)**
    
*   **\[第5列\]指实际在内存中占用的字节数。**
    
*   **\[第6列\]显示内存区域的映射信息，通常包括文件名或其他标识符。如果是匿名内存（未映射到文件），则会显示类似 \[****`heap`****\]、\[****`stack`****\]、\[****`anon`****\] 这样的标识。**
    

但在系统崩溃的情况下，当前内存映射明细大多时候都帮不上忙。但在排查内存泄漏问题时，内存映射的输出还是很有用(如上所示利用pmap命令可以实时输出)，可以通过输出看到是否有大段的连续内存占用、过多的匿名内存块、异常的文件映射等等。

**启动参数&环境变量**

![Image 34](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYHmjFERayR9awVAxwGicBRCxlLMJkciaf9DiaLxyRUZkYgicspY9VicSzVjg/640?wx_fmt=png&from=appmsg)

Java进程的启动参数以及系统环境变量，这里不过多展开。

**信号处理**

![Image 35](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYiamzZ8FgBXIxIrgHZajHyXZ4YNKfzpwv5Y6XdMUOfxdibKr9ySMicMPiaQ/640?wx_fmt=png&from=appmsg)

在信号量概要一节里有简单聊过，虚拟机对于**`SIGSEGV`**信号注册了信号回调函数，这意味着当发生SIGSEGV内存异常方位，Java进程未必会崩溃结束。但实际上，虚拟机对于很多信号也注册了回调函数，他们同样的会在程序崩溃前再检查一把是否需要杀掉进程，从而确保系统的整体稳定性。

**系统信息**

**系统信息概要**

![Image 36](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY9gC4Ea4zxbqxPXKCfbHTtia2iaNDLh8CdaAVK57HMdz0talKmUF97qpw/640?wx_fmt=png&from=appmsg)

这块内容主要描述了操作系统的基本信息，包括系统相关信息，比如主机名、内核版本号、硬件架构等等。 输出的内容基本可以和下列命令的含义相同。

*   **`cat /etc/os-release`**
    
*   **`uname -a`**
    
*   **`ldd --version`**
    
*   **`ulimit -a`**
    
*   **`w`**
    

如果是公司的机器的话，这块不必过多关心。大多数情况出现问题我们要关注的是差异性问题，而公司一般会配有对应的SRE来管理应用配置，相关的配置也会有基线，相同应用的机器配置均会相同。

**系统内存概括**

![Image 37](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY3eCQusIwF4u1068BBMKRvdqOS0UA05vjlV4awb2nSU1nI64ic40XA3Q/640?wx_fmt=png&from=appmsg)

这些内容其实就是系统崩溃瞬时**`cat /proc/meminfo`**的输出明细。**`/proc/meminfo`**是了解Linux系统内存使用状况的主要接口(需要注意的是在当前的MacOS开发环境并不适用)，我们最常用的**`free`**、**`vmstat`**等命令就是通过它获取数据的 ，但一般来说在排查一些内存泄漏问题，利用meminfo的输出还是非常有帮助，但是遇到进程崩溃这种情况其实有帮助的信息不多，这里不做过多介绍。

**CPU信息概况**

![Image 38](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYiaTK0tvDwe0TP0IfZvMtwiad29XqwK848E5eruxqyLXJa0cerfBoDibug/640?wx_fmt=png&from=appmsg)

这里其实就是命令**`cat /proc/cpuinfo`**的输出明细，给出了当前机器的CPU型号、CPU制造商、产品代号、主频、二级缓存、浮点运算单元等信息，这些对于系统崩溃问题排查一般来说帮助不大，可以暂不关注。

**其他信息**

![Image 39](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYHlWLQhYRTouhov9WAwocFNuLgF5wsbEicnsX12OZHOxYB0MIXknHPyQ/640?wx_fmt=png&from=appmsg)

日志的结尾给出了内存，虚拟机版本等内容，但大多和之前重合，这里有一个有用的信息是elapsed time，它反映了从应用启动到崩溃一共耗时多久(我的例子里直接启动就主动让虚拟机立刻崩溃了所以这里是0)。

**五**

**core文件**

好了，到这里我们介绍完了Java虚拟机提供的错误文件。但当Java虚拟机如上描述崩溃时，会同时生成在当前目录生成一个叫core的文件。假设我的进程崩溃之前进程id为29296，那么core文件的名称默认会是**`core.29296`**(这里会根据用户的个人配置不同文件名称和路径可能稍有差异)。这个core文件里记录了程序在崩溃时的内存状态，在有些时候崩溃文件不能给我们进一步信息的情况下，可以进一步的打开我们的思路，发现一些意想不到的结果。

分析core文件最常见的工具便是gdb。使用gdb打开core文件后常用的命令可以简要介绍如下：

**问题调用栈**

![Image 40](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaY1MH1KKeCOiapwMlF4Y2HOIPrTiaTLCUibLeWOQMSoFGlmFkFvUnJ3F2TQ/640?wx_fmt=png&from=appmsg)

**`bt`**（backtrace）命令是 GDB 中用于查看当前调用堆栈的重要工具，可以说是问题排查的首要命令。通过当前命令，开发者可以显示程序在崩溃或暂停时的函数调用历史，了解执行状态和调用关系。输出包含每个函数的名称、源文件及行号，以及参数信息，且从最近的调用开始逐步追溯。该命令还支持限制输出的帧数（例如 **`bt 5`** 显示最近的 5 个调用帧）。如上图所示可以看到我们进程崩溃的帧栈明细。通过前文的日志信息，我们很快能发现这里的第7个调用帧便是实际出问题的地方。

**帧快照**

![Image 41](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYyyfeic5ib8XkoEgbEYj88qMWlrTdGzGISpTAJI7JpbQKZXMAKJiaueticQ/640?wx_fmt=png&from=appmsg)

当锁定到第7个函数帧时，我们可以利用命令**`frame 7`**来定位到这里。这表示我们已经切换到编号为7的调用帧。调用帧代表函数调用的上下文，我们后续可以进一步看到函数的参数、局部变量和调用位置等信息。进一步的我们输入**`i r`**(info registers的缩写)，代表我们需要查看此刻寄存器中的内容。自然的，我们会发现这里和之前Java虚拟机给出的错误日志的寄存器的每个值都相同。

为了更清楚的还原出问题的上下文，我们可以进一步探究：

![Image 42](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYBAIxRNIlhzOicaqeMWAicumhWqbApojsrYJbmB8QHuXPbQa8l4cRI04Q/640?wx_fmt=png&from=appmsg)

*   第一行查看当前指令正在做什么操作，**发现这和我们前文【指令上下文】中推出的结果是相同的**！(这里需要注意汇编的语法有2种**\-INTEL和AT&T**。gdb当前这里指AT&T语法，和上文中的格式稍有不同。)
    
*   第二行看下当前r12寄存器的地址(当然最开始的截图已经有了)。
    
*   第三行尝试范围r12寄存器的地址对应的值，被提示内存无法访问(和最开始的SIGSEGV对应)。
    

**汇编代码还原**

![Image 43](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYLS7BibXMLh0Va5UTMFsSqzK5pc1xTxcGtmtiaXztp8BOooJKWibLJAM4A/640?wx_fmt=png&from=appmsg)

对于更为复杂的问题，我们可能要深入到对应的C++层面的方法去深入探究(比如JIT编译出了bug，编译出了一个有问题的方法导致程序崩溃之类)。此时我们需要深入到指定方法的机器码层面，此时基于gdb的调试可以利用disas命令完整还原出当前的汇编执行过程(如果我们当前的帧左边有一个箭头“=\>”来表示)。

**内存映射**

![Image 44](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYpdvmb1yqxnIibMWvpG24FcWiciam3DHGJkxNwxaicFCs16ZbAEol8uibzfQ/640?wx_fmt=png&from=appmsg)

最后介绍的指令是i proc m(是info proc mappings的缩写)。这里输出含义跟上面提到的【内存映射明细】 类似。就不过多赘述了，总之还是告诉了开发者内存的上下范围界及其对应映射的文件在哪里。

**六**

**一些经验**

**虚拟机崩溃的原因分类**

虽然系统崩溃的原因千奇百怪，但是大多数情况下，我们都可以将错误原因都可分为2种情况：

*   内存非法访问
    
*   物理内存不足
    

内存非法访问最为常见，如本文中介绍的例子就是这样一种严重的错误情况。其次还有一种场景比较重要，那就是**物理内存不足**。当系统物理内存耗尽时它的错误原因大概长相如下图所示：

![Image 45](https://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYATpZDRdrbFzcAwZzMibVK5eAdAW9yWPNtNMwcZKDvpHzyS6VWDglaQw/640?wx_fmt=png&from=appmsg)

物理内存不足系统崩溃虚拟机给出的原因及其解决方案

物理内存的崩溃类型相比内存非法访问会更友好，它直接给出了研发可能的解决方案。

**留意JNI**

**`JNI（Java Native Interface）`**是Java与C语言之间进行交互的重要机制，但进行有效的JNI编程并不简单。开发者必须深入理解Java虚拟机的内部工作原理，以避免潜在的错误和问题。尤其是对于那些主要从事C语言开发的人员来说，缺乏对JVM原理的了解可能会导致程序在运行时出现意外的崩溃。

在之前的章节中，我们提到了NullPointerException的机制。其本质是虚拟机拦截SIGSEGV信号并抛出异常而不终止进程。然而，如果第三方C语言组件在没有充分理解Java虚拟机的情况下，错误地注册了SIGSEGV信号处理回调函数，那么在Java进程出现NullPointerException时，系统会因为SIGSEGV的回调被覆盖导致进程崩溃。因此，在使用JNI时(包括应用依赖的第三方JNI组件)，开发者必须特别注意，确保对JVM的工作原理有充分的认识，以维护系统的稳定性和可靠性。

**敢于怀疑**

Java**虚拟机自身bug**虽然相对概率小，但是在出现极端问题时也要适当考虑，毕竟大家都是人，写个bug么在所难免。避免持续性的陷入bug自证的死结中。可以来_https://bugs.openjdk.org/projects/JDK/issues/_ 利用你崩溃时的关键字尝试找找是否已经有人提出过类似的系统崩溃问题，有时候可能会事半功倍。

**七**

**写在最后**

在深入探讨JVM崩溃的各种细节及其解决方案后，我们可以看到，理解和掌握JVM的内在机制不仅对开发者至关重要，也对整个应用的稳定性和性能有着深远的影响。通过合理的配置、监控工具的使用和适当的调优策略，我们可以有效地降低JVM崩溃的风险。

然而，面对复杂的系统，完全避免所有崩溃是困难的。关键在于具备快速诊断和恢复的能力，这要求我们在日常开发和运维中，持续关注系统的健康状态，并及时进行故障排查。希望本文能够为你在JVM的使用和维护上提供一些有价值的见解与帮助。

**往期回顾**

1. [得物App白屏优化系列｜图片库篇](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247528615&idx=1&sn=e595b66ef5a0d1bf90638843f112aa65&chksm=c16125f8f616acee9c0156928acc2b35ad1030c69f0d7d5576881552e1639709c383a05780eb&scene=21#wechat_redirect)

2. [基于MySQL内核的SQL限流设计与实现｜得物技术](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247528032&idx=1&sn=0b81ad6fb88dd2a199b020143cba822c&chksm=c1613b3ff616b22942e3cebe0b9267b78eb8ac5ee3c55a8d3ac74130e8264beff5b4e97711eb&scene=21#wechat_redirect)

3. [得物Flink内核探索实践](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247528003&idx=1&sn=e472382b4d3cb47f3faa62f8627dabb5&chksm=c1613b1cf616b20a5782a7f8d0782770060c70864b47a5225e713299c83cc192f0cd6b4ba8f8&scene=21#wechat_redirect)

4. [链路级资损防控之资损字段防控实践｜得物技术](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247527972&idx=1&sn=24fea420cd6d981b3bba7c6d9bd7da9f&chksm=c1613b7bf616b26df9d51705e58f99568d9aa81d06a91c3cfa7e2eb9250686146c134725ec76&scene=21#wechat_redirect)

5. [B端常用交互方式的量化及优化实践和指引｜得物技术](http://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247527932&idx=1&sn=5fd72c05eec90d5286f3e859427e53a4&chksm=c16138a3f616b1b572bacbe4e9430899d2c21bcff5b5fed7caaee37d5f2312037edbe8972c44&scene=21#wechat_redirect)

文 / 财神

关注得物技术，每周一、三更新技术干货

要是觉得文章对你有帮助的话，欢迎评论转发点赞～

未经得物技术许可严禁转载，否则依法追究法律责任。

“

**扫码添加小助手微信**

如有任何疑问，或想要了解更多技术资讯，请添加小助手微信：

![Image 46](https://mmbiz.qpic.cn/mmbiz_jpg/AAQtmjCc74CLDfqwIn9RVCch7icbhfsiaYvFibP1cakNWYqJCZVOjjmEoibkjcaWrcg0DofxIQibB4EOh2dQSntWCRw/640?wx_fmt=jpeg&from=appmsg)

预览时标签不可点

![Image 47](https://mp.weixin.qq.com/s/_DOQGBmhfV-LUzb03RcTCQ)Scan to Follow

继续滑动看下一个

轻触阅读原文

![Image 48](http://mmbiz.qpic.cn/mmbiz_png/AAQtmjCc74AlsHDtoVyU8hqzNTGS26fV9PmHAcZ8uib1GWNJibIuBiavPdAXw9IOzjlEAYRJUNjOEme5geMNPoZ1Q/0?wx_fmt=png)

得物技术

向上滑动看下一个

[Got It](javascript:;)

 

![Image 49](https://mp.weixin.qq.com/s/_DOQGBmhfV-LUzb03RcTCQ) Scan with Weixin to  
use this Mini Program

[Cancel](javascript:void\(0\);) [Allow](javascript:void\(0\);)

[Cancel](javascript:void\(0\);) [Allow](javascript:void\(0\);)

× 分析

 : ， .   Video Mini Program Like ，轻点两下取消赞 Wow ，轻点两下取消在看 Share Comment Favorite
