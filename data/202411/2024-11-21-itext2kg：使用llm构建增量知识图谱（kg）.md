# iText2KG：使用LLM构建增量知识图谱（KG）
- URL: https://mp.weixin.qq.com/s/0nTku_hyTLtQilCXGSd2AA
- Added At: 2024-11-21 02:35:30
- [Link To Text](2024-11-21-itext2kg：使用llm构建增量知识图谱（kg）_raw.md)

## TL;DR
`iText2KG`利用LLM从文本构建KG，实现零样本跨领域提取，支持增量更新，提高知识图谱构建的精度与灵活性。

## Summary
1. **框架概述**：
   - `iText2KG` 是一个基于 Python 的框架，利用大型语言模型（LLM）从文本文档中提取实体和关系，构建增量知识图谱（KG）。
   - 具有零样本能力，无需专门训练即可跨领域提取知识。

2. **模块功能**：
   - **文档提取器**：将文档转换为语义块，由LLM提取信息。
   - **增量实体提取器**：识别并解析语义块内的唯一实体。
   - **增量关系提取器**：检测语义上唯一的关系。
   - **Neo4j 图形集成器**：利用 Neo4j 可视化关系和实体。

3. **框架特点**：
   - **增量构建**：支持KG增量更新和扩展。
   - **零样本学习**：无需预定义集或外部本体即可运行。

4. **模型设置**：
   - 使用 OpenAI 的 `gpt-4o-mini` 模型和 HuggingFace 的 `bge-large-zh embedding` 模型。

5. **构建KG过程**：
   - 使用 `iText2KG` 从简历和职位描述中提取信息。
   - 确保节点和关系嵌入的维度在模型之间保持一致。
   - 使用 `DocumentDistiller` 提炼文档信息。

6. **参数解释**：
   - `llm_model`：用于提取实体和关系的语言模型。
   - `embeddings_model`：创建实体向量表示的嵌入模型。
   - `build_graph` 参数：如 `sections`、`existing_global_entities` 等。

7. **可视化与数据库**：
   - 使用 `GraphIntegrator` 对构建的知识图谱进行可视化。
   - 通过 Neo4j 图形数据库可视化关系和实体。

8. **总结**：
   - `iText2KG` 利用LLM构建KG，具有高精度和灵活性。
   - 解决了传统方法中存在的问题，如语义重复和未解决实体。
