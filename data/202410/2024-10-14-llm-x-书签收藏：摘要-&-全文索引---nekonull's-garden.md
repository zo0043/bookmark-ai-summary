# LLM x 书签收藏：摘要 & 全文索引 - Nekonull's Garden
- URL: https://nekonull.me/posts/llm_x_bookmark/
- Added At: 2024-10-14 19:22:34
- [Link To Text](2024-10-14-llm-x-书签收藏：摘要-&-全文索引---nekonull's-garden_raw.md)

## TL;DR
作者通过GitHub存储库和插件管理网络收藏，但面临链接失效和查找不便问题。为此，建立新存储库并利用GitHub Actions自动生成摘要和全文备份。未来计划优化摘要质量、数据结构化及引入向量搜索。提供详细部署指南。

## Summary
1. **背景介绍**：
   - 作者在网上冲浪时喜欢收藏有趣的文章和网站。
   - 自2021年5月起，使用`osmos::memo`插件将收藏记录到公开的GitHub存储库。
   - 插件工作原理：设置GitHub token，点击收藏按钮后临时clone、追加条目、生成commit并推送回GitHub。
   - 已积累800+条目。

2. **存在的问题**：
   - 书签URL可能失效，成为死链接。
   - 记录项仅包含URL、标题和标签，查找不便。
   - 长文章内容易忘，查找和引用效率低。

3. **解决方案**：
   - 建立新存储库`bookmark-summary`，包含书签的Markdown全文、列表摘要、一句话总结。
   - 通过GitHub Actions联动现有书签存储库。
   - 工作流程：
     1. 新增书签条目。
     2. 触发`summarize`的GitHub Actions。
     3. Actions执行：
        - checkout书签和摘要存储库。
        - 执行`process_changes.py`：
          - 解析书签README.md，找到新增条目。
          - 将URL保存到Wayback Machine。
          - 使用[jina reader](https://jina.ai/reader/)获取Markdown全文。
          - 使用LLM生成列表摘要和一句话总结。
          - 保存摘要和总结到文件。
          - 更新摘要存储库的README.md。
     4. 提交变更到摘要存储库。
   - 主要代码由Claude和GPT4o编写，作者进行小调整。
   - 使用deepseek-chat生成摘要，成本低效果可。

4. **未来优化方向**：
   - 提升列表摘要质量，优化prompt或换用模型。
   - 数据结构化，考虑维护JSON格式。
   - 代码整理和重构，改进书签和摘要存储库的交互方式。
   - 引入向量搜索，使用embedding模型和数据库。
   - 自动生成每周周报（已完成）。
   - 改用更现代的工具链，如uv和PEP 723。

5. **部署指南**：
   - 初始化书签存储库，安装`osmos::memo`插件并连接GitHub。
   - 新建摘要存储库，添加`process_changes.py`并修改配置。
   - 在书签存储库添加`bookmark_summary.yml`并替换相关字段。
   - 新建PAT，配置权限并保存。
   - 在书签存储库添加密钥到环境变量（PAT、OPENAI_API_MODEL、OPENAI_API_KEY、OPENAI_API_ENDPOINT）。
   - 测试配置是否正常工作。
