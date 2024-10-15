# llama-agents+chainlit打造超级智能体
- URL: https://blog.stoeng.site/20240701.html
- Added At: 2024-10-15 12:57:35
- [Link To Text](2024-10-15-llama-agents+chainlit打造超级智能体_raw.md)

## TL;DR
该项目通过结合llama-agents和chainlit框架，构建了一个多智能体系统，用于股票分析和数据检索。依赖安装包括chainlit、yfinance和llama-agents等。示例代码展示了智能体创建、工具交互及RAG模型应用。项目开源，提供多种联系方式。

## Summary
1. **项目介绍**：
   - 项目名为“llama-agents+chainlit打造超级智能体”，是一个基于llama-agents和chainlit框架构建的多智能体系统。
   - 项目代码托管在GitHub上，网址为：[https://github.com/run-llama/llama-agents](https://github.com/run-llama/llama-agents)。

2. **依赖安装**：
   - **chainlit**：通过`pip install chainlit`安装，用于构建和部署Web应用程序。
   - **yfinance**：通过`pip install yfinance`安装，用于获取金融市场数据。
   - **llama-agents**：通过`pip install llama-agents llama-index-agent-openai llama-index-embeddings-openai llama-index-program-openai`安装，用于构建多智能体系统。
   - 需要在`.env`文件中配置OpenAI和Anthropic的API密钥。

3. **ollama接口支持**：
   - 示例代码展示了如何使用`Ollama`类创建智能体，并使用`ReActAgent`类来与工具交互。

4. **Anthropic接口支持**：
   - 示例代码展示了如何使用`Anthropic`类创建智能体，并使用`yfinance`获取股票数据。
   - 定义了多个函数来获取股票价格、公司信息、财务比率等，并创建了相应的工具。

5. **股票分析**：
   - 定义了多个函数来获取股票价格、公司信息、财务比率等，并创建了相应的工具。
   - 使用`OpenAI`模型进行智能体创建和股票分析。
   - 示例代码展示了如何使用`LocalLauncher`来启动智能体服务，并进行股票分析。

6. **RAG（Retrieval-Augmented Generation）**：
   - 示例代码展示了如何使用`llama_index`来构建检索增强生成模型。
   - 加载并索引了Lyft和Uber的财务数据，并创建了查询引擎工具。
   - 使用`AgentService`和`ToolService`来创建智能体服务。

7. **chainlit+llama-agents**：
   - 示例代码展示了如何将`chainlit`与`llama-agents`结合使用，构建股票分析助手。
   - 定义了股票分析所需的函数和工具。
   - 使用`cl.on_chat_start`和`cl.on_message`来处理用户输入和输出。

8. **联系方式**：
   - 项目作者提供了微信、哔哩哔哩频道和YouTube频道的联系方式。
   - 开源项目地址：[https://github.com/win4r/AISuperDomain](https://github.com/win4r/AISuperDomain)。
