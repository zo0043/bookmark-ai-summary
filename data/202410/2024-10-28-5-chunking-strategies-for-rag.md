# 5 Chunking Strategies For RAG
- URL: https://blog.dailydoseofds.com/p/5-chunking-strategies-for-rag
- Added At: 2024-10-28 08:04:14
- [Link To Text](2024-10-28-5-chunking-strategies-for-rag_raw.md)

## TL;DR
文章探讨了RAG应用中五种文档分块策略（固定大小、语义、递归、结构化、LLM引导），分析其优缺点及适用场景，强调选择策略需考虑内容、模型和资源。最终目标是优化业务影响。

## Summary
1. **RAG应用工作流程**：
   - 存储附加信息作为向量。
   - 将输入查询与那些向量匹配。
   - 将最相似的信息与查询一起提供给LLM。

2. **文档分块的重要性**：
   - 确保文本适合嵌入模型的输入大小。
   - 提高检索步骤的效率和准确性，直接影响生成响应的质量。

3. **五种分块策略**：
   - **固定大小分块**：
     - 将文本分割成基于预定义的字符、单词或标记数量的统一段落。
     - 保持连续块之间的重叠以维护语义流。
     - 简化批处理，但可能破坏句子或想法的完整性。
   - **基于语义的分块**：
     - 基于有意义的单元（如句子、段落或主题部分）分段文档。
     - 为每个段创建嵌入。
     - 根据余弦相似度将段组合成块。
     - 维护自然语言流并保留完整想法，提高检索准确性。
   - **递归分块**：
     - 基于固有分隔符（如段落或部分）进行分块。
     - 如果块大小超过预定义限制，则进一步分割。
     - 维护自然语言流并保留完整想法，但实现和计算复杂度较高。
   - **结构化分块**：
     - 利用文档的固有结构（如标题、部分或段落）定义块边界。
     - 维护结构完整性，但假设文档具有清晰结构，可能不适用于所有文档。
   - **LLM引导分块**：
     - 利用LLM生成语义孤立且有意义的块。
     - 确保高语义准确性，但计算需求最高，需要处理LLM的有限上下文窗口。

4. **选择分块策略的考虑因素**：
   - 内容的性质。
   - 嵌入模型的功能。
   - 计算资源。

5. **其他相关主题**：
   - 图神经网络。
   - 量化技术以在小硬件上运行大型模型。
   - 预测区间的生成。
   - 因果关系的识别。
   - ML模型训练的扩展。
   - ML模型生产的测试。
   - 隐私优先的ML系统。
   - ML模型的压缩以降低成本。

6. **总结**：
   - 每种分块策略都有其优缺点，选择取决于具体应用场景。
   - 语义分块在许多情况下效果良好，但仍需测试验证。
   - 最终目标是产生业务影响，如降低成本、驱动收入和扩展ML模型。