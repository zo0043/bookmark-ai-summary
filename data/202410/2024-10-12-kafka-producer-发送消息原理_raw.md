Title: Kafka Producer 发送消息原理 - RecordAccumulator1. Kafka发送消息大致流程 Ka

URL Source: https://juejin.cn/post/7397024073228959778

Markdown Content:
1.  KafkaProducer 首先将待发送的消息封装成 ProducerRecord。
2.  紧接着对 ProducerRecord 进行序列化。
3.  基于某种分区算法，计算把消息发送到哪个 TopicPartition，此时需要获取集群的元数据信息，以便或知应该将消息发送到哪个 Broker 节点。
4.  需要先把消息缓存到 RecordAccumulator 中，然后再把消息分批发送出去。
5.  最后由 Sender 子线程，通过 NIO 机制将批量消息发送到 Broker 节点。

![Image 1: kafka_send.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/83eabda60b904681985840e839ceea66~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=cQGKRrTUqmkGBFB%2BaZw35I3hUO8%3D)

**Kafka 为什么要设计一个 RecordAccumulator 缓冲池?**

> 原因就是，如果每一条消息都触发一次发送请求，由于网络请求需要消耗一定的资源，每次只发送条消息的吞吐量未免太低。所以，Kafka 就设计了一个 RecordAccumulator 缓冲池。由 main 线程负责把消息发送到缓冲池后就立即返回;当消息积累到 Produceratch 大小或者 linger.ms 时长时，会通过 NIO机制将消息批量的发送到 Broker 端。

2\. RecordAccumulator
---------------------

Kafka 为了提高 Producer 客户端发送消息的吞吐量，选择先将消息暂时缓存起来，等到满足一定的 条件再进行批量发送。这样做可以减少网络的请求次数，从而提高发送消息的性能。而负责将消息缓存起 来的 Java 类就是 RecordAccumulator.java 。

![Image 2: ac123.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7afe8920e55945babf9d5913052420a8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=MjUR3SP%2F5%2FKzDG3LfoyiAOxQhbY%3D)

当消息序列化之后，经过分区器计算出应该将消息发送到哪个TopicPartition。针对每条消息，会按照 TopicPartition 维度把他们放在不同的 Deque< ProducerBatch \>队列里面。只要消息的 TopicPartition相同，就会被缓存在相同的 Deque< ProducerBatch \>里面。

1.  每个 ProducerBatch 的大小由参数 batch.size 控制(默认 16384，16KB)，而 RecordAccumulator 的大小由参数 buffer.memory 控制(默认 33554432，32MB)。
2.  如果申请的内存大小是 ProducerBatch 大小(16KB)，并且已分配内存不为空，则直接取出一个 ByteBuffer 返回。
3.  如果释放的内存是一个 ProducerBatch 的大小是 16KB，就直接将内存添加到 Deque< ByteBuffer \>free 队列即可，**这样就可以避免生产者客户端将一个 ProducerBatch 发送出去之后需要等待 JVM 的垃圾回收。**
4.  但是如果申请的 ProducerBatch \> 16KB，就需要通过 JVM 的垃圾回收才能回收内存

3\. 消息大小 <\= 16KB 的发送场景
-----------------------

### 3.1 申请内存

我们假设发送的消息大小是 5KB，因此这里申请的 ProducerBatch 是 16KB，会从空闲的池化内存Deque< ByteBuffer \> free 的队首获取一块 ByteBuffer 使用。

然后生产者就会将消息发送到不同分区的 ProducerBatch 中，这样当一个 ProducerBatch 被写满消息或者 linger.ms 时间触达的时候。就会由 Sender 子线程负责把 ProducerBatch 发送到 Broker 端。

![Image 3: browse.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c94a872b4a1943cb827aa08bfd8d96d5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=kHwqVuhpRvl71v3h58t380yTNd4%3D)

### 3.2 释放内存

当把消息批量发送到 Broker 后，就会释放 ProducerBatch 占用的空间，会把 ProducerBatch 占用的内存放到缓冲池 Deque< BvteBuffer \> free 的队尾，并调用 BvteBuffer.clear() 清空数据以便下次重复使用。

![Image 4: release.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/858e5a2d23bf490e97bd67c6ad24c967~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=xtyK5bxpx2DKwWz2FjJITkVRY0s%3D)

4\. 消息大小\>16KB 的发送场景
--------------------

### 4.1 申请内存

我们假设发送的消息大小是 24KB，因此这里申请的 ProducerBatch 大小就是 24KB，此时就只能从非池化内存 nonPooledAvailableMemory 中申请内存。如果整个内存池的可用空间比要申请的内存大(this.nonPooledAvailableMemory + freeListSize \>\= size)，就可以直接从 nonPooledAvailableMemory中申请内存。并从 nonPooledAvailableMemory 去掉申请的那一块内存。

![Image 5: sendBig.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2cf7f5f03176480c93555b47e32fa96b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=6AxmpfzFpHxwmG4%2FTzmqgBEmGRY%3D)

当申请到 24KB 的 ProducerBatch 之后，生产者就可以把大小等于 24KB 的消息发送到该ProducerBatch。随后就会将消息发送到 Broker 端。

### 4.2 释放内存

当把消息批量发送到 Broker 后，就会释放 ProducerBatch 占用的空间，并非仅仅是在非池化内存(nonPooledAvailableMemory)中加上刚刚释放的 ProducerBatch=24KB 内存，**该过程需要经过JVM的GC，才能释放内存**

![Image 6: biggerRelease.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5c86c6519f2a4851b443876b967ea3b3~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgSzBuOUQxS3VB:q75.awebp?rk3s=f64ab15b&x-expires=1728947622&x-signature=PkLWautUbvjD7jaKXyaD%2FEfxbi8%3D)

5.池化内存和非池化内存相互转换
----------------

### 5.1，池化内存转化为非池化内存

假如，我们现在需要发送的消息的大小是 32KB，因此我们要创建一个32KB 的 ProducerBatch。因为 ProducerBatch 的大小超过了 16KB，所以只能从非池化内存 nonPooledAvailableMemory 中申请内存。但不巧的是，非池化内存中的可用内存已不足 32KB，或者没有剩余内存了。

这个时候就会尝试从池化内存 Deque< ByteBuffer \>free 中，将一部分 ByteBuffer 转换到nonPooledAvailableMemory 中。释放第一个 ByteBuffer=16KB，不够再释放第二个 ByteBuffer，一直到可用的内存达到 32KB。当 nonPooledAvailableMemory 有足够的内存时，就可以创建大小是 32KB 的ProducerBatch 了.

### 5.2，非池化内存转化为池化内存

虽然我们现在需要发送的消息的大小是 5KB，需要创建大小是 16KB 的 ProducerBatch。但此时Deque< ByteBufer \>free 中已经没有足够的内存，这时就会从 nonPooledAvailableMemory 中划走一部分内存到池化内存中，Deque< ByteBuffer \> free 会将申请到的内存放到 free 队列的头部，然后会从空闲的池化内存 Deque< ByteBuffer \>free 的队首获取一块 ByteBuffer，用于创建 ProducerBatch。

然后生产者就会将消息发送到不同分区的 ProducerBatch 中，这样当一个 ProducerBatch 被写满消息或者 linger.ms 时间触达的时候。就会由 Sender 子线程负责把,ProducerBatch 发送到 Broker 端。

当把消息批量发送到 Broker 后，就会释放 ProducerBatch 占用的空间，会把 ProducerBatch 占用的内存放到缓冲池 Deque< ByteBufer \>free 的队尾，并调用 ByteBufer.clear() 清空数据以便下次重复使用。因此，池化内存的空间不但会增加，而且该过程也不会触发 JVM 的 GC。

6\. 总结
------

kafka通过实现了一个内存池来累积将要发送的消息（增加吞吐量），同时使用bytebuffer来存储消息（通过bytebuffer可以避免JVM垃圾回收带来的影响），最后还使用了一块非池化空间（旨在应对消息大于 16KB 的场景）。
