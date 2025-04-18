# Python 从0到1构建MCP Server & Client_python mcp-CSDN博客
- URL: https://blog.csdn.net/GOBinCC/article/details/146290820
- Added At: 2025-04-18 15:52:42
- [Link To Text](2025-04-18-python-从0到1构建mcp-server-&-client_python-mcp-csdn博客_raw.md)

## TL;DR
本文介绍了MCP（模型上下文协议）的搭建教程，涵盖概念、协议、项目结构、环境配置、工具函数、客户端构建等。

## Summary
1. **MCP 简介**：MCP (模型上下文协议) 是一个服务器，提供标准化接口连接外部数据源和工具，如文件系统、数据库或 API。

2. **MCP 优势**：
   - 统一大模型厂商 Function Call 格式。
   - 统一相关工具的封装管理。

3. **MCP 传输协议**：
   - **Stdio 传输协议**：适用于本地使用，需要安装命令行工具。
   - **SSE（Server-Sent Events）传输协议**：适用于云服务部署，基于 HTTP 长连接实现。

4. **项目结构**：
   - **MCP Server**：包含 Stdio 和 SSE 传输协议。
   - **MCP Client**：包含自建客户端（Python）、Cursor 和 Cline。

5. **环境配置**：
   - 安装 UV 包：通过命令行安装 UV 包。
   - 初始化项目：创建项目目录、虚拟环境，安装依赖。

6. **构建工具函数**：
   - 构建相关文档映射字典。
   - 构建 MCP 工具：实现搜索网页、提取网页文本的功能。

7. **封装 MCP Server**：
   - 基于 Stdio 协议：使用 FastMCP 库，实现搜索文档的功能。
   - 客户端配置：
     - 基于 Cline：在 Visual Studio Code 安装 Cline 插件，配置 MCP。
     - 基于 Cursor：创建 .cursor 文件夹和 mcp.json 文件，配置 MCP。

8. **构建 SSE MCP Server**：
   - 封装 MCP Server：实现 SSE 传输协议，使用 FastMCP 库。
   - 客户端配置：
     - 启动命令：使用 `uv run main.py --host 0.0.0.0 --port 8020` 命令启动。

9. **构建 MCP Client**：
   - 实现连接到 SSE 服务器、处理查询、交互式聊天等功能。
   - 启动命令：使用 `uv run client.py http://0.0.0.0:8020/sse` 命令启动。

10. **总结**：通过 Python 从 0 到 1 搭建 MCP Server 以及 MCP Client 的完整教程，介绍了 MCP 的概念、传输协议、项目结构、环境配置、构建工具函数、封装 MCP Server、构建 SSE MCP Server、构建 MCP Client 等内容。
