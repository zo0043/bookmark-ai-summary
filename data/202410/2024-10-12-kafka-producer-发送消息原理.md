# Kafka Producer 发送消息原理 
- URL: https://juejin.cn/post/7397024073228959778
- Added At: 2024-10-12 07:57:59
- [Link To Text](2024-10-12-kafka-producer-发送消息原理_raw.md)

## TL;DR
Kafka发送消息经历封装、序列化、分区计算、缓存和批量发送。RecordAccumulator缓存消息提高吞吐量，管理池化与非池化内存应对不同大小消息，优化性能和内存使用。

## Summary
1. **Kafka发送消息流程**：
   - **封装消息**：KafkaProducer将待发送消息封装成ProducerRecord。
   - **序列化**：对ProducerRecord进行序列化处理。
   - **分区计算**：基于分区算法，计算消息应发送到哪个TopicPartition，需获取集群元数据。
   - **缓存消息**：将消息缓存到RecordAccumulator中。
   - **批量发送**：由Sender子线程通过NIO机制批量发送消息到Broker节点。

2. **RecordAccumulator设计原因**：
   - **提高吞吐量**：避免每条消息触发一次发送请求，减少网络资源消耗。
   - **批量发送**：消息积累到一定大小或时间后批量发送，提高性能。

3. **RecordAccumulator工作机制**：
   - **消息缓存**：消息按TopicPartition维度缓存在不同的Deque<ProducerBatch>队列中。
   - **内存管理**：
     - **ProducerBatch大小**：由batch.size参数控制（默认16KB）。
     - **RecordAccumulator大小**：由buffer.memory参数控制（默认32MB）。
     - **内存申请与释放**：根据消息大小从池化或非池化内存中申请和释放内存。

4. **消息大小≤16KB的发送场景**：
   - **申请内存**：从空闲池化内存Deque<ByteBuffer> free中获取ByteBuffer。
   - **发送消息**：消息发送到不同分区的ProducerBatch，满或超时后由Sender子线程发送到Broker。
   - **释放内存**：释放ProducerBatch占用的内存，放回缓冲池队尾并清空数据。

5. **消息大小>16KB的发送场景**：
   - **申请内存**：从非池化内存nonPooledAvailableMemory中申请内存。
   - **发送消息**：将大消息发送到对应的ProducerBatch，随后发送到Broker。
   - **释放内存**：释放内存需经过JVM的GC处理。

6. **池化与非池化内存转换**：
   - **池化转非池化**：非池化内存不足时，从池化内存中释放ByteBuffer补充。
   - **非池化转池化**：池化内存不足时，从非池化内存中划拨内存到池化内存。

7. **总结**：
   - **内存池机制**：累积消息提高吞吐量。
   - **ByteBuffer存储**：避免JVM垃圾回收影响。
   - **非池化内存**：应对大消息场景。
