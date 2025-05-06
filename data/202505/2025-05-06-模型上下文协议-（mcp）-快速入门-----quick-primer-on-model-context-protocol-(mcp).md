# 模型上下文协议 （MCP） 快速入门 --- Quick Primer on Model Context Protocol (MCP)
- URL: https://www.polarsparc.com/xhtml/MCP.html
- Added At: 2025-05-06 02:59:40
- [Link To Text](2025-05-06-模型上下文协议-（mcp）-快速入门-----quick-primer-on-model-context-protocol-(mcp)_raw.md)

## TL;DR
MCP是一个开放协议，简化LLM应用与外部数据源和工具的集成，提供标准化的工具接入方式，支持文本生成、企业数据集成等应用场景。

## Summary
1. **MCP简介**：
   - MCP（Model Context Protocol）是一个开放协议，它允许LLM应用与外部数据源（如数据库、文件等）和工具（如GitHub、ServiceNow等）无缝集成。
   - MCP解决了工具集成缺乏行业标准的挑战，为各种智能框架（如LangChain、LlamaIndex等）提供统一的工具集成方式。

2. **MCP核心组件**：
   - **MCP服务器**：连接到各种外部和内部数据源及工具，向智能LLM应用暴露特定功能，类似于服务提供商。
   - **MCP客户端**：以标准化的方式连接和交互MCP服务器。
   - **MCP主机**：使用MCP客户端访问MCP服务器的LLM应用。

3. **MCP应用场景**：
   - LLM应用用于文本生成、文本情感分析、文本摘要等任务。
   - LLM应用与企业数据资产集成，通过向量存储使用RAG进行上下文知识检索。
   - LLM应用驱动企业环境中的自动化任务。

4. **安装与设置**：
   - 使用Ubuntu 24.04 LTS基于Linux桌面。
   - 确保已安装Python 3.x编程语言。
   - 安装Ollama平台。
   - 下载LLM模型（如IBM Granite-3.3 2B模型）。
   - 安装必要的Python模块。

5. **Python实践**：
   - 使用Ollama和LangChain进行MCP实践。
   - 创建环境变量文件`.env`。
   - 编写Python代码，实现MCP服务器和客户端。
   - 使用命令行执行Python代码。

6. **MCP传输模式**：
   - **标准IO（stdio）**：通过标准输入和输出流进行通信，适用于与命令行工具的集成。
   - **服务器发送事件（sse）**：通过HTTP POST请求实现服务器到客户端的流式传输，适用于与网络服务集成。

7. **MCP服务器示例**：
   - 使用FastMCP创建MCP服务器。
   - 定义计算简单利息和复利利率的工具。

8. **MCP客户端示例**：
   - 使用MCP客户端连接到MCP服务器。
   - 调用MCP服务器上的工具进行利息计算。

9. **MCP服务器与客户端通信**：
   - 使用stdio和sse两种传输模式实现MCP服务器与客户端的通信。

10. **总结**：
    - MCP为构建和部署智能LLM应用提供了强大的工具。
    - 通过MCP，LLM应用可以与外部数据源和工具无缝集成，实现更强大的功能。
