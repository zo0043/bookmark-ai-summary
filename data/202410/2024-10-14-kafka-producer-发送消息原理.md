# Kafka Producer 发送消息原理 
- URL: https://juejin.cn/post/7397024073228959778
- Added At: 2024-10-14 16:19:57
- [Link To Text](2024-10-14-kafka-producer-发送消息原理_raw.md)

## TL;DR
Kafka发送消息经封装、序列化、分区计算后缓存于RecordAccumulator，批量发送提高吞吐量。内存池机制优化内存使用，池化与非池化内存灵活转换应对不同消息大小，减少JVM垃圾回收影响。

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

3. **RecordAccumulator细节**：
   - **消息缓存**：消息按TopicPartition维度缓存在不同的Deque<ProducerBatch>队列中。
   - **内存控制**：
     - **ProducerBatch大小**：由参数batch.size控制（默认16KB）。
     - **RecordAccumulator大小**：由参数buffer.memory控制（默认32MB）。
   - **内存分配**：
     - **小于等于16KB**：从空闲池化内存Deque<ByteBuffer> free获取。
     - **大于16KB**：从非池化内存nonPooledAvailableMemory申请，需JVM垃圾回收。

4. **消息大小≤16KB的发送场景**：
   - **申请内存**：从空闲池化内存获取ByteBuffer。
   - **释放内存**：发送后释放内存到缓冲池队尾，并清空数据。

5. **消息大小>16KB的发送场景**：
   - **申请内存**：从非池化内存申请。
   - **释放内存**：发送后释放内存，需经过JVM垃圾回收。

6. **池化与非池化内存转换**：
   - **池化转非池化**：非池化内存不足时，从池化内存释放ByteBuffer。
   - **非池化转池化**：池化内存不足时，从非池化内存划拨。

7. **总结**：
   - **内存池机制**：累积消息提高吞吐量。
   - **ByteBuffer存储**：避免JVM垃圾回收影响。
   - **非池化空间**：应对大于16KB的消息场景。
