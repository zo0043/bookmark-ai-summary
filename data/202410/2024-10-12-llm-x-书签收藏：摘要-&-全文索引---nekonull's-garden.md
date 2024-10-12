# LLM x 书签收藏：摘要 & 全文索引 - Nekonull's Garden
- URL: https://nekonull.me/posts/llm_x_bookmark/
- Added At: 2024-10-12 07:56:38
- [Link To Text](2024-10-12-llm-x-书签收藏：摘要-&-全文索引---nekonull's-garden_raw.md)

## TL;DR
作者使用osmos::memo插件将书签记录到Github，但存在死链接和查找不便问题。为此建立新存储库，通过Github Actions自动生成书签摘要和全文备份，提升查找效率。未来计划优化摘要质量、数据结构化等，并已实现自动生成周报。提供详细部署指南。

## Summary
1. **背景介绍**：
   - 作者在网上冲浪时经常遇到有趣的文章或网站，有收藏的冲动。
   - 自2021年5月起，使用[osmos::memo](https://github.com/osmoscraft/osmosmemo)书签插件，将收藏记录到公开的Github存储库。
   - 插件工作原理：设置Github token，点击收藏按钮后临时clone，追加条目，生成commit并提交。

2. **存在问题**：
   - 书签指向的URL可能不再存在，成为死链接。
   - 记录项仅包含URL、标题和可选标签，查找不便。
   - 书签多为长文章，时间久后忘记内容，查找和引用效率低。

3. **解决方案**：
   - 建立新存储库[bookmark-summary](https://github.com/jerrylususu/bookmark-summary)作为辅助数据。
   - 包含新增书签的Markdown格式全文、列表摘要、一句话总结，与现有存储库通过Github Actions联动。
   - 工作流程：
     1. 通过书签插件新增条目。
     2. 提交触发`summarize`的Github Actions。
     3. Actions执行：
        - checkout书签和摘要存储库。
        - 执行[process_changes.py](https://github.com/jerrylususu/bookmark-summary/blob/main/process_changes.py)：
          - 解析书签README.md，找到新增条目。
          - 将URL保存到Wayback Machine。
          - 使用[jina reader](https://jina.ai/reader/) API获取Markdown全文。
          - 使用LLM生成列表摘要和一句话总结。
          - 保存到对应文件，更新README.md。
     4. 提交变更到摘要存储库。

4. **技术实现**：
   - 主要代码由Claude和GPT4o编写，人肉调整。
   - 使用deepseek-chat生成摘要，成本低效果可。
   - 逐步修复bug，感受LLM对生产力的提升。

5. **未来优化方向**：
   - **列表摘要质量**：优化prompt或换用模型。
   - **数据结构化**：考虑额外维护JSON格式。
   - **代码整理和重构**：重构+补充测试，改进存储库交互方式。
   - **向量搜索**：考虑接入embedding模型，存入数据库。
   - **自动生成周报**：已完成，见[Releases](https://github.com/jerrylususu/bookmark-summary/releases)。
   - **工具链现代化**：使用uv，依赖写在代码头部。

6. **部署指南**：
   - 初始化书签存储库，安装插件并连接Github。
   - 新建摘要存储库，添加[process_changes.py](https://github.com/jerrylususu/bookmark-summary/blob/main/process_changes.py)。
   - 添加[bookmark_summary.yml](https://github.com/jerrylususu/bookmark-collection/blob/main/.github/workflows/bookmark_summary.yml)到书签存储库。
   - 新建PAT，添加密钥到环境变量。
   - 配置完成后，测试工作流和摘要生成。
