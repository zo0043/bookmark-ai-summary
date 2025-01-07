Title: IO模型介绍（select、poll、epoll）

URL Source: https://mp.weixin.qq.com/s/wvggAQmWLjfVUpwAc0nckQ

Markdown Content:
**什么是IO？  
**

IO中的I就是input，O就是output,IO模型即输入输出模型,而比较常听说的便是磁盘IO,网络IO。

**什么是操作系统的IO?**
---------------

我们如果需要对磁盘进行读取或者写入数据的时候必须得有主体去操作，这个主体就是应用程序。应用程序是不能直接进行一些读写操作(IO)的,因为用户可能会利用此程序直接或者间接的对计算机造成破坏,只能交给底层软件—操作系统.也就是说应用程序想要对磁盘进行读取或者写入数据,只能通过操作系统对上层开放的API来进行。在任何一个应用程序里面,都会有进程地址空间,该空间分为两部分,一部分称为用户空间(允许应用程序进行访问的空间),另一部分称为内核空间（只能给操作系统进行访问的空间，它受到保护）。

**应用程序想要进行一次IO操作分为两个阶段:**
-------------------------

•**IO调用**：应用程序进程向操作系统内核发起调用【1】。

•**IO执行**：操作系统内核完成IO操作【2】。

**操作系统完成一次IO操作包括两个过程:**
-----------------------

•数据准备阶段：内核等待I/O设备准备好数据(从网卡copy到内核缓冲区【3】。

•数据copy阶段：将数据从内核缓冲区copy到用户进程缓冲区【4】。

应用程序一次I/O流程如下：

![Image 23](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzuoy4uYBhnMiawR7kQZWnbslwUuPrEI2PAc1GnHDTetydKBWWcrl1x6vg/640?wx_fmt=png&from=appmsg)

一个完整的IO过程包括以下几个步骤：

1.应用程序进程向操作系统发起IO调用请求。

2.操作系统准备数据，外部设备的数据通过网卡加载到内核缓冲区。

3.操作系统拷贝数据，即将内核缓冲区的数据copy到用户进程缓冲区。

```
而一次IO的本质其实就是: 等待 + 拷贝
```

**IO模型有哪些？**
------------

**1.阻塞式 IO：**
-------------

服务端为了处理客户端的连接和数据处理：

伪代码具体如下：

```
listenfd = socket();   // 打开一个网络通信套接字
```

上面的伪代码中我们可以看出，服务端处理客户端的请求阻塞在两个地方，一个是 accept、一个是 read ，我们这里主要研究 read 的过程，可以分为两个阶段：等待读就绪（等待数据到达网卡 & 将网卡的数据拷贝到内核缓冲区）、读数据。

阻塞IO流程如下：

![Image 24](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzuUf5av2EqCUt4nHRKacdjcqNID5IZGSLgibNbhlX6wIx9tPZ7RKv8HyQ/640?wx_fmt=png&from=appmsg)

**2.非阻塞式 IO：**

非阻塞式 IO 我们应该让操作系统提供一个非阻塞的 read() 函数，当第一阶段读未就绪时返回 -1 ，当读已就绪时才进行数据的读取。

非阻塞IO往往需要程序员循环的方式反复尝试读写文件描述符, 这个过程称为轮询(for(connfd : arr)). 这对CPU来说是较大的浪费, 一 般只有特定场景下才使用.

伪代码具体如下：

```
arr = new Arr[];
```

所谓非阻塞 IO 只是将第一阶段的等待读就绪改为非阻塞，但是第二阶段的数据读取还是阻塞的，非阻塞 read 最重要的是提供了我们在一个线程内管理多个文件描述符的能力

非阻塞具体流程如下：

![Image 25](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzuFthmcHictM5Rt6UY5MdhUGb7nNxgJKV8nPxA7k8XYte6L9sKfYm1PJg/640?wx_fmt=png&from=appmsg)

**3\. IO多路复用（select、poll、epoll）：**

上面的实现看着很不错，但是却存在一个很大的问题，我们需要不断的调用 read() 进行系统调用，这里的系统调用我们可以理解为分布式系统的 RPC 调用，性能损耗十分严重，因为这依然是用户层的一些小把戏。

多路复用就是系统提供了一种函数可以同时监控多个文件描述符的操作，这个函数就是我们常说到的select、poll、epoll函数，可以通过它们同时监控多个文件描述符，只要有任何一个数据状态准备就绪了，就返回可读状态，这时询问线程再去通知处理数据的线程，对应线程此时再发起read()请求去读取数据。实际上最核心之处在于IO多路转接**能够同时**等待多个文件描述符的就绪状态,来达到不必为每个文件描述符创建一个对应的监控线程，从而减少线程资源创建的目的。

### **select：**

select 是操作系统提供的系统函数，通过它我们可以将文件描述符发送给系统，让**系统内核帮我们遍历检测是否可读**，并告诉我们进行读取数据。

伪代码如下：

```
arr = new Arr[];
```

流程简图：

![Image 26](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzuLL8of9Y2HSmMZDC3dZ56596nxoeSDX46RnJb93c67jjURNLHibjx9QA/640?wx_fmt=png&from=appmsg)

**优点：**

1.减少大量系统调用。

2.系统内核帮我们遍历检测是否可读。

#### **存在一些问题：**

• 每次调用需要在用户态和内核态之间拷贝文件描述符数组，但高并发场景下这个拷贝的消耗是很大的。

• 内核检测文件描述符可读还是通过遍历实现，当文件描述符数组很长时，遍历操作耗时也很长。

• 内核检测完文件描述符数组后，当存在可读的文件描述符数组时，用户态需要再遍历检测一遍。

### **poll：**

• poll 和 select 原理基本一致，最大的区别是去掉了最大 1024 个文件描述符的限制。

• select 使用固定长度的 BitsMap，表示文件描述符集合，而且所支持的文件描述符的个数是有限制的，在 Linux 系统中，由内核中的 FD\_SETSIZE 限制， 默认最大值为 1024，只能监听 0~1023 的文件描述符。

• poll 不再用 BitsMap 来存储所关注的文件描述符，取而代之用动态数组，以链表形式来组织，突破了 select 的文件描述符个数限制，当然还会受到系统文件描述符限制。

### **epoll：**

epoll 主要优化了上面三个问题实现：

```
1.每次调用需要在用户态和内核态之间拷贝文件描述符数组，但高并发场景下这个拷贝的消耗是很大的。
```

epoll 基于高效的红黑树结构，提供了三个核心操作：epoll\_create、epoll\_ctl、epoll\_wait。

#### **epoll\_create：**

   用于创建epoll文件描述符，该文件描述符用于后续的epoll操作，参数size目前还没有实际用处，我们只要填一个大于0的数就行。

![Image 27](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzu8DYNTh7cw5NEbtbvbqkaIwYPVfYvv7QrNkhhZ4mdl5nFDZ3vPCMcNw/640?wx_fmt=png&from=appmsg)

**epoll\_ctl:**

epoll\_ctl函数用于增加，删除，修改epoll事件，epoll事件会存储于内核epoll结构体红黑树中.

![Image 28](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzubKOqLribWT7uVwiafS26RUb4iaQiaRNENCSgGfND5PvygGKicjUBMXTFicZA/640?wx_fmt=png&from=appmsg)

**epoll\_wait函数：**

epoll\_wait用于监听套接字事件，可以通过设置超时时间timeout来控制监听的行为为阻塞模式还是超时模式。

![Image 29](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzu9lyarPj3IvicLlaDfRYXe7P7bTKzZibagDiaQuMbYfXFcFicZbIYxCFl5g/640?wx_fmt=png&from=appmsg)

整体运转如下：

![Image 30](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BU7YqVSw3nCRXqEW09XVyzuEXLaic7HAe8thOh1AqjLonRlf4pEFiaMnZ7icCevGdRMRYhiaLYYmnRYPg/640?wx_fmt=png&from=appmsg)

﻿﻿伪代码如下：

```
listenfd = socket();   // 打开一个网络通信套接字
```

#### **LT模式和ET模式：**

##### **LT模式：水平触发：**

1.socket读触发：socket接收缓冲区有数据，会一直触发epoll\_wait EPOLLIN事件，直到数据被用户读取完。

2.socket写触发：socket可写，会一直触发epoll\_wait EPOLLOUT事件。

##### **ET模式：边缘触发：**

1.socket读触发：当被监控的 Socket 描述符上有可读事件发生时，服务器端只会从 epoll\_wait 中苏醒一次，即使进程没有调用 read 函数从内核读取数据，也依然只苏醒一次，因此我们程序要保证一次性将内核缓冲区的数据读取完。

2.socket写触发：socket可写，会触发一次epoll\_wait EPOLLOUT事件。

##### **epoll为什么高效：**

1.红黑树红黑树提高epoll事件增删查改效率。

2.回调通知机制:当epoll监听套接字有数据读或者写时，会通过注册到socket的回调函数通知epoll，epoll检测到事件后，将事件存储在就绪队列（rdllist）。

3.就绪队列：epoll\_wait返回成功后，会将所有就绪事件存储在事件数组，用户不需要进行无效的轮询，从而提高了效率。

**信号驱动IO:**
-----------

   多路转接解决了一个线程可以监控多个fd的问题，但是select采用无脑的轮询就显得有点暴力，因为大部分情况下的轮询都是无效的，所以有人就想，别让我总去问数据是否准备就绪，而是等你准备就绪后主动通知我,这边是信号驱动IO。

   信号驱动IO是在调用sigaction时候建立一个SIGIO的信号联系，当内核准备好数据之后再通过SIGIO信号通知线程,此fd准备就绪，当线程收到可读信号后，此时再向内核发起recvfrom读取数据的请求，因为信号驱动IO的模型下,应用线程在发出信号监控后即可返回，不会阻塞，所以一个应用线程也可以同时监控多个fd。

**异步 IO：**
----------

应用只需要向内核发送一个读取请求,告诉内核它要读取数据后即刻返回；内核收到请求后会建立一个信号联系，当数据准备就绪，内核会主动把数据从内核复制到用户空间，等所有操作都完成之后，内核会发起一个通知告诉应用，我们称这种模式为异步IO模型。

异步IO的优化思路是解决应用程序需要先后发送询问请求、接收数据请求两个阶段的模式，在异步IO的模式下，只需要向内核发送一次请求就可以完成状态询问和数拷贝的所有操作。

**同步和异步区别：**
------------

同步和异步关注的是消息通信机制.

同步：就是在发出一个调用时，自己需要参与等待结果的过程,则为同步,前面四个IO都自己参与了,所以也称为同步IO.

异步：则指出发出调用以后,到数据准备完成,自己都未参与,则为异步IO。

![Image 31](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXGicp40bMAicmX9DpEDjMlfPJT23acLpRzmuyiaguHv0VlmVDyEFGwd36gZYRShzhv0EPleicHyvk7KA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

扫一扫，加入技术交流群
