# 🌟《从一到二：基于Trae的多智能体合作Prompt自动生成迭代指南》#VibeCoding #Trae 刚接触LLM - 掘金
- URL: https://juejin.cn/post/7488013596523118601
- Added At: 2025-04-01 09:03:27
- [Link To Text](2025-04-01-🌟《从一到二：基于trae的多智能体合作prompt自动生成迭代指南》#vibecoding-#trae-刚接触llm---掘金_raw.md)

## TL;DR
文章介绍了基于Multi-agent和MCP的多智能体合作prompt生成系统，详细阐述了框架设计、方案实施及效果展示，展望前景并呼吁支持。

## Summary
1. **背景介绍**：
    - Multi-agent结合MCP成为新趋势。
    - 刚接触者常受“如何编写prompt”困扰。
    - 设计多智能体合作自动生成prompt迭代系统。

2. **框架和LLM部署方式选型**：
    - 采用langchain而非之前的langroid。
    - langchain更广泛使用，langroid更易用。
    - 支持远程大模型或本地部署的LLM模型。
    - 以Ollama部署本地模型为例。

3. **方案设计**：
    - 用户需求：设计prompt、提供预期输入输出。
    - Main Agent：生成初始Prompt，根据反馈迭代。
    - Validator Agent：读取prompt，对比预期输出。
    - Analysis Agent：分析Output差异，提供反馈。

4. **从头开始**：
    - 环境准备：部署本地LLM，安装langchain等依赖。
    - Coding：
        - 创建工作流，实现关键节点（generate_prompt, validate_prompt, generate_feedback, check_completion）。
        - 实现关键Agent处理逻辑（Main Agent, Validator Agent, Analysis Agent, Feedback Agent）。
        - 设计main函数入口，启动整个多agent合作的workflow。

5. **效果展示**：
    - 系统运行效果良好，用户可尝试。

6. **结语**：
    - 配合MCP/Function Calling以及RAG，前景广阔。
    - 呼吁点赞三连支持。
