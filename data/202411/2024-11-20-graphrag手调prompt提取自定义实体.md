# GraphRAG手调Prompt提取自定义实体
- URL: https://juejin.cn/post/7397597730631417892
- Added At: 2024-11-20 13:13:55
- [Link To Text](2024-11-20-graphrag手调prompt提取自定义实体_raw.md)

## TL;DR
本文介绍了GraphRAG实体提取问题，通过Prompt-Tune微调Prompt，手动调整实体提取效果，实现索引、可视化和检索功能的优化。

## Summary
1. **GraphRAG实体提取问题**：GraphRAG在使用Prompt-Tune根据领域自动生成的实体不理想，需要手动调整。

2. **Prompt-Tune使用说明**：
   - Prompt-Tune可以自动微调Prompt以适配输入文件的领域，但自动生成的实体列表可能不一致。
   - 使用命令微调提示词Promt时，生成了三个文件：`community_report.txt`、`entity_extraction.txt`和`summarize_descriptions.txt`。

3. **实体提取任务格式**：
   - 任务目标：识别文本中的实体及其关系。
   - 步骤：识别实体，提取实体信息，识别实体间关系，提取关系信息。

4. **手动调整Prompt**：
   - 了解输入文章的实体。
   - 使用ChatGPT生成Example，并修改`entity_extraction.txt`中的任务说明、Example中的`entity_types`和Real Data部分的`entity_types`。
   - 使用DeepSeeker输出example，确保格式正确。

5. **索引与可视化**：
   - 使用`poetry run poe index --root .`进行索引。
   - 可视化结果。

6. **查询功能**：
   - 使用`poetry run poe query --method global`和`poetry run poe query --method local`进行查询。

7. **总结**：
   - 通过手动调整Prompt，可以生成更符合设定的实体。
   - 优化后的实体提取Prompt在索引、可视化和检索方面有显著的提升。
