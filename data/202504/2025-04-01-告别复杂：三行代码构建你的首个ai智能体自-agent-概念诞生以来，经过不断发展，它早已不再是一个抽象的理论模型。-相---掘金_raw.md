Title: 告别复杂：三行代码构建你的首个AI智能体

URL Source: https://juejin.cn/post/7487863095869882405

Published Time: 2025-04-01T04:39:27+00:00

Markdown Content:
自 Agent 概念诞生以来，经过不断发展，它早已不再是一个抽象的理论模型。

相反，随着业界对于 Agent 的定义、能力与特性逐步达成共识，一系列成熟的 Agent 框架纷纷涌现，如 AutoGen、CrewAI 等。然而，这些框架往往有着陡峭的学习曲线，让初学者望而却步。

那么，是否存在一个既简单易学、又能快速构建强大 Agent 的入门级框架呢？

答案是肯定的！正是今天我们要介绍的，由 Hugging Face 出品的轻量级 Agent 框架——**SmolAgents**。

我用 SmolAgents 框架做了什么？
---------------------

作为开发者经常会收到来自线上用户的Bug反馈，一个常规的排查路径就是通过日志来定位问题。

然而，频繁的排查任务会打乱正常的工作节奏，因此我用 Agent 开发了一个「智能反馈处理系统」来提效：

![Image 1](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/41f7c09f0fc54c259273cb50c39d6a22~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=rGZUI7E4Vzj9d6e5LgNGnXJH09I%3D)

![Image 2](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/575a0331c64c456697cee5958108e587~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=X8MUOIltg3VJSd%2BsHdTHXLNqr%2BE%3D)

这个系统的主要工作流程如下：

1.  **自动获取日志：** 收到用户反馈后，自动下载并解压用户日志。
2.  **匹配关键词：** 根据问题描述，匹配到正确的排查关键词。
3.  **精准查找日志：** 聚焦问题发生时间点附近的日志内容，快速定位问题。
4.  **解读错误信息：** 访问技术文档链接，找到错误码的具体解释。
5.  **记录操作过程：** 保存 Agent 的操作记录，便于后续审查和结论确认。

有初步感受到 SmolAgents 框架的魅力了吗？下面即开始我们的正式介绍。

SmolAgents 框架有多“Smol”？
----------------------

“Smol” 一词源自于网络俚语，原意为“小而可爱”。这一命名也恰好反映出了 SmolAgents 最突出的特点——极简。

那么，SmolAgents 的“极简”体现在哪里呢？

### 核心代码仅1000行左右

SmolAgents 框架非常小巧，它的核心实现（主要集中在 agents.py 中）仅 1000 行代码左右，只保留了最小程度的抽象。尽管代码层面极度精简，但它仍内置了几种 Agent 类型：

*   **CodeAgent**：支持编写和执行 Python 代码。
*   **ToolCallingAgent**：以 JSON 格式调用各类工具。

同时，由于它是开源的，因此也鼓励开发者们根据实际需求，对源码进行灵活修改和裁剪。

### 最少3行代码即可搭建Agent

用 SmolAgents 框架搭建一个 Agent 能有多简单？

只需安装软件包，然后初始化 Agent 并传入必要的参数，就能轻松启动一个具备联网搜索能力的 Agent：

```
pip install smolagents
```

```
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())
agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts?")
```

在这个最小化的 Agent 结构中，我们至少需要提供以下两个参数：

*   `model`：文本生成模型，用于提供推理能力支持（此处是 `HfApiModel`）。
*   `tools`：工具列表，用于提供任务解决方案（此处是 `DuckDuckGoSearchTool` ，提供联网搜索功能）。

最终，Agent 会针对查询返回结果，并以直观的方式展示搜索响应：

![Image 3](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c959e183a8d144f590371147493a9813~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=CihKi4TqnRt0m%2F2StgUodORWMO0%3D)

SmolAgents 的创新之举
----------------

如果只是“极简”，那还不足以让 SmolAgents 在一众 Agent 框架中脱颖而出，SmolAgents 最主要的一大创新点在于——

### 用代码执行替代 JSON 输出

传统 LLM 采用 JSON 作为工具调用的中间格式，通过生成 JSON 来描述要调用的工具及其参数。

```
{
  "type": "function",
  "function": {
    "name": "get_current_temperature",
    "description": "Get the current temperature for a specific location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g., San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["Celsius", "Fahrenheit"],
          "description": "The temperature unit to use. Infer this from the user's location."
        }
      },
      "required": ["location", "unit"]
    }
  }
}
```

这种方式虽然简单直观，但其局限性也十分明显：

*   **表达能力有限**：JSON 作为一种数据交换格式，无法表达复杂逻辑。
*   **缺乏灵活性**：作为一个中间层，任务执行流程固定，难以动态调整。
*   **对象管理能力欠缺**：无法有效处理非结构化数据（如图像或视频）。

相比之下，SmolAgents 采用**代码执行**的方式，将工具调用转化为真正可运行的代码。这不仅简化了执行流程，还赋予了 Agent 更高的灵活性，使其能够应对更复杂的任务场景。

#### 代码执行的核心优势

##### 动态可组合性

代码执行允许将工具调用嵌入到复杂的控制流中——如条件判断、循环和异常处理等。

这意味着 Agent 可以根据实际情况，动态地调整操作流程，以更好地适应由 AI 驱动的控制流的不确定性。

##### **高效的对象管理**\*\*\*\*

代码执行可以通过内存地址引用的形式来管理非结构化对象的生命周期，实现复用，从而大幅地提升任务执行的效率。

##### 通用性与扩展性

这一点无需多言，编程语言本就是表达计算机所要执行的操作的最佳方式。它不仅能调用外部工具，还能直接操作系统 API、执行系统命令，甚至与复杂的软件生态系统深度集成。

##### **预训练数据的呈现**

大量高质量的代码预训练样本，使得模型在代码生成和工具调用方面具备天然优势——代码结构清晰、语法严格，为输出提供了天然正则化约束。

这么说也许还不够直观，我们可以用一个现实中的场景来体现两者的区别。

#### 现实场景对比：从最便宜的渠道购买一部手机

假设我们想要购买一个特定型号的手机，需要综合考虑价格、汇率和税率等因素，判断从哪个国家的渠道买入最便宜。

![Image 4](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0ef41d2bc34a4e86b9e0c5cb881c731a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=5XhKqTSg59NlwEeM47KgjI%2F5ro4%3D)

左侧展示的是采用传统的 JSON 格式的方法，需要进行多轮的API调用和交互：

1.  首先查询德国汇率
2.  接着获取该手机在德国的价格
3.  随后使用税率和汇率来转换价格
4.  对其他国家重复上述步骤

而右侧展示的是采用代码执行的方法，这种方法更加高效：

1.  通过一个循环来遍历所有国家
2.  针对每个国家，查询汇率、价格，转换价格并计算运输成本
3.  使用 Python 内置的 min()函数找出最具性价比的国家

可以看出，**减少操作次数、降低任务复杂度、重用现有的库函数**——这就是代码执行所带来的优势。

SmolAgents 的其他亮点
----------------

### 多LLM支持

SmolAgents 可以轻松对接多种语言模型，并支持在不同模型之间无缝切换：

#### HfApiModel：HF 上托管的模型

```
from smolagents import HfApiModel

model = HfApiModel(
    model_id="deepseek-ai/DeepSeek-R1",
    provider="together",
```

HfApiModel 支持 Hugging Face 上托管的各种文本生成模型，在未指定 model 参数时，默认采用 Qwen/Qwen2.5-Coder-32B-Instruct 模型，无需 HF\_TOKEN 即可免费使用，但会有速率限制；

如需访问更高级的模型或提高速率限制，则需要HF PRO帐户的HF\_TOKEN。

![Image 5](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fc2e6df52fcc447895dae0076f70b24c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=y5kOC4qi0ZRev63f2Xn%2F2ZIYyTs%3D)

#### LiteLLMModel：第三方模型

```
from smolagents import LiteLLMModel

model = LiteLLMModel(
    "anthropic/claude-3-5-sonnet-latest",
    temperature=0.2,
    api_key=os.environ["ANTHROPIC_API_KEY"]
)
```

LiteLLM 是一个开源库，它提供了一个统一的 API 接口，使开发者能够使用与 OpenAI 风格一致的语法来与不同的 LLM 进行交互，从而减少了适配不同 API 的难度。

它支持多达100多个的第三方模型，基本主流的 LLM 提供商（如 OpenAI、Anthropic、Gemini、DeepSeek等）都支持。

![Image 6](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d694835b78f947da8069b60cf3541f4d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=4ihIrvHhQW%2B3XlJZUxGMp9dcU3k%3D)

#### TransformersModel：本地模型

```
from smolagents import TransformersModel

model = TransformersModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    max_new_tokens=4096,
    device_map="auto"
)
```

Transformers 库提供了一系列工具和 API，旨在简化预训练模型的下载和使用。而为了更简单地使用这些模型完成各种任务，它还提供了一个高级 API，叫做 pipeline。

TransformersModel 就依赖于 Transformers 库，它会根据你提供的 model\_id 构建建一个 Transformers pipeline，让你能在本地机器上高效地运行这些预训练模型，进行推理。

### 多工具支持

#### 内置的工具箱

Smolagents 框架自带了一个工具箱，通过设置 `add_base_tools = True` 即可启用，它包含以下几个预置工具：

*   PythonInterpreterTool：执行 Python 代码。
*   FinalAnswerTool：给出最终答案。
*   UserInputTool：处理用户输入。

其中，最重要的一个工具就是PythonInterpreterTool (Python 代码解释器工具)，它能够直接执行代码、返回结果、分析错误，让 Agent 具备编码和数据分析能力，而无需专门训练模型去理解代码。

除了这些，工具箱内还提供了以下工具，用于增强 Agent 的功能：

*   DuckDuckGoSearchTool：使用 Duckduckgo 搜索，返回最热门的搜索结果。
*   GoogleSearchTool：使用 Google 搜索，获取最前沿的信息。
*   VisitWebpageTool：访问网页并将内容转换为 markdown 格式。
*   SpeechToTextTool：将音频转录为文本。

除了内置的工具箱之外，Smolagents 的开放架构还允许你轻松接入外部工具，极大扩展 Agent 的功能边界，比如：

#### 从 HuggingFace Space 导入工具

Hugging Face 的 Space 是一个支持快速构建和部署 AI 应用的平台。利用 `Tool.from_space()` 方法，我们只需提供 Space 的 ID、名称及用途说明，即可将其无缝整合到 Agent 中。

比如，通过导入 FLUX.1-dev，你可以让 Agent 改进提示词后生成令人惊艳的图像：

```
from smolagents import CodeAgent, HfApiModel

image_generation_tool = Tool.from_space(
  "black-forest-labs/FLUX.1-schnell",
  name="image_generator",
  description="Generate an image from a prompt"
)
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(tools=[image_generation_tool], model=model)

agent.run(
    "Improve this prompt, then generate an image of it.", additional_args={'user_prompt': 'A rabbit wearing a space suit'}
)
```

![Image 7](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/386f0ce1990f40db95b21261cccc9703~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=qwXpwrnatU%2FHsWKiXlnA12oPT0c%3D)

![Image 8](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3dd1d77342864f9d91b9c565dd59eb61~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=dqhWAKaBmynfiynD9QqdNnJNd2g%3D)

#### 从 LangChain 导入工具

LangChain 是一个基于 LLM 构建应用的开源框架，内含诸多实用工具。只需调用 `Tool.from_langchain()` 方法，就能轻松引入如 Wikipedia 等工具。

例如，通过以下代码，Agent 能够快速搜索与“吴恩达”相关的百科词条，进行摘要并生成简明的介绍：

```
from smolagents import Tool, CodeAgent, HfApiModel
from langchain.agents import load_tools

wikipedia_tool = Tool.from_langchain(load_tools(["wikipedia"])[0])
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(tools=[wikipedia_tool], model=model)
agent.run("Andrew Ng")
```

![Image 9](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0309e59af61842e9a882be5a079965a8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=uD8M%2FtCN7fV%2FHxIpLo3RWBJDTIE%3D)

#### 从 MCP Server 导入工具

MCP 是一种开放协议，它通过标准化的方式将 LLM 连接到不同数据源和工具，使得 Agent 能够用自然语言访问本地或远端的数据源并执行操作。要从 MCP 导入工具，我们需要用到 ToolCollection.from\_mcp() 方法。

例如，下面这段代码就展示了如何利用 MCP Server 上的 filesystem 工具，访问本机的文件系统，读取 Markdown 文件内容并返回：

```
import os
from smolagents import ToolCollection, CodeAgent, HfApiModel
from mcp import StdioServerParameters

server_parameters = StdioServerParameters(
    command="npx",
    args=["-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/xxx/Downloads"]
)

model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

with ToolCollection.from_mcp(server_parameters) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model)
    agent.run("请读取以下目录下的md文件，并返回文件内容：/Users/xxx/Downloads/expample.md")
```

![Image 10](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2dde39c1667445cfa268601ac3af1edf~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=WiRF2lJ2v5BIrjoAQ9YiA8pgIBU%3D)

#### 自定义工具

当内置工具箱和外部工具都无法满足我们的需求时，我们还可以自定义工具。只需清晰定义以下属性：

*   **name**：工具名称，描述其用途；
*   **description**：详细说明，用于生成系统提示；
*   **输入类型和描述**：帮助 Python 解释器理解输入；
*   **output type**：定义输出格式；
*   **forward 方法**：包含实际执行的推理代码。

所有的这些属性都将在初始化时自动融入 Agent 的系统提示中。

我们可以将其封装成函数，并添加@tool注解：

```
from smolagents import tool

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id
```

也可以通过继承 Tool 类来实现，以提供更大的灵活性：

```
from smolagents import Tool

class ModelDownloadTool(Tool):
    name = "model_download_tool"
    description = "This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub. It returns the name of the checkpoint."
    inputs = {"task": {"type": "string", "description": "The task for which to get the download count."}}
    output_type = "string"

    def forward(self, task: str) -> str:
        most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
        return most_downloaded_model.id
```

随后像正常工具那样提供给 Agent 即可：

```
from smolagents import CodeAgent, HfApiModel
agent = CodeAgent(tools=[model_download_tool], model=HfApiModel())
agent.run(
    "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub?"
)
```

### 与 Gradio 无缝集成

Gradio 库是一个同样由 Hugging Face 出品的、可以使用 Python 代码快速构建 Web 交互界面的 UI 框架。

![Image 11](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4cbf0ba9c2784fc694831613aa48ba83~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=4lIYhP31c5RzXGrz4AGwPvcBiFE%3D)

为了实现更友好的用户交互体验，SmolAgents 内置了 GradioUI 类，方便我们以 ChatBot 的形式与 Agent 进行交互，还能实时观察 Agent 的思考与执行过程，极大降低了调试难度：

```
from smolagents import (
    load_tool,
    CodeAgent,
    HfApiModel,
    GradioUI
)

# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

model = HfApiModel(model_id)

# Initialize the agent with the image generation tool
agent = CodeAgent(tools=[image_generation_tool], model=model)

GradioUI(agent).launch()
```

![Image 12](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/435aab13d5594042bdf460b6926abf88~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=UpuTERGMCpAea30xvN%2FbAKV6Pww%3D)

可以看到，现在，我们不再需要以 agent.run() 的形式输入指令了，转而可以在 GradioUI 的输入框中输入。

而 Agent 在接收到我们的指令后，会先有一个思考（Thought）过程，思考需要调用哪个工具，随后输出 Python 代码并交由 Python 代码解释器执行。

SmolAgents 的核心设计
----------------

#### MultiStepAgent：ReAct 框架的抽象

ReAct 框架是目前构建 Agent 的主流方式，它的名字来自 "Reason"（推理）和 "Act"（行动）这两个词的组合。

Smolagents 库中的 MultiStepAgent 类即是 ReAct 框架的抽象。

采用这种框架的 Agent 会分多个步骤来解决问题，每一步都包含「推理」和「行动」。与单步骤的 Agent 不同，多步骤的 Agent 拥有记忆，会记住之前的步骤。

![Image 13](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2117c2ded3ca4c9d825b0a15c4f6ce41~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=Orbt07l%2Fjjg3Zl6nr%2FaI%2B6pWKMY%3D)

简单来说，多步骤 Agent 是通过 "思考/行动/观察" 这样一个循环来迭代解决问题的。

*   **思考**：基于当前任务和记忆做出推理。
*   **行动**：执行相应的工具调用。
*   **观察**：记录执行结果，并将其纳入记忆中。

它在执行工具调用后，会判断问题是否解决。如果没解决，就把观察到的结果记下来，然后继续循环。

因此，多步骤 Agent 是一个有记忆的循环过程，它会根据之前的观察来调整后续行动，逐步逼近问题的解决方案，直到问题解决。

用动图演示会更清楚一点：

![Image 14](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2a9fc90ffcfd421c9433a4a44305dbd3~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=ZPKhLT0eg0XBbRvnjBmJD%2BF9xM4%3D)

#### CodeAgent ：MultiStepAgent的实现

SmolAgents 默认采用的 CodeAgent 就是基于 MultiStepAgent 实现的。

以下这张图解释了 CodeAgent.run() 的工作流程：

![Image 15](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5e949c2fd05d42b080026ccabf98a781~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=LSGTBKqrVoVK0Po63FJbfDSOWTk%3D)

左侧显示了 CodeAgent 的主要组件：

*   **日志组件（logs）** ：记录系统提示（SystemPromptStep）、任务描述（TaskStep）及每一步的执行结果（ActionStep）。
*   **模型组件（model）** ：处理所有 LLM 调用。
*   **工具组件（tools）** ：提供各类实用工具。

右侧详细说明了执行流程，分为三个主要阶段：

1.  **准备阶段**：将任务放入 TaskStep，并记录到日志中。
2.  **循环执行 (直到调用 final\_answer 工具)** ：

*   *   **2.1**`agent.write_inner_memory_from_logs()`：解析日志，生成 LLM 可以理解的聊天消息列表。
    *   **2.2** 将这些消息发送给模型 (LLM/VLM)，模型返回包含代码块的回答，然后提取代码块。
    *   **2.3** 执行代码块，调用特定工具，然后继续运行代码 (执行阶段)。
    *   **2.4** 所有执行日志（包括可能的错误）都会被记录到 ActionStep，并附加到日志中。

3.  **结束阶段**：当 `final_answer` 工具被调用时，`run()` 方法返回它的参数。

实操：打造自己的旅游咨询 Agent
------------------

现在，让我们将学到的知识付诸实践，构建一个简易的旅游咨询 Agent，它可以为我们讲解目的地的历史文化、搜索当地的热门旅游景点，并提供实时的天气状况。

#### 步骤1：检查依赖

首先，请确保你的本地机器已经配置好了 Python 环境，并安装好了 `smolagents`库。如果尚未安装，请使用 pip 命令进行安装：

```
pip install smolagents
```

#### 步骤2：切换模型

在 Agent 的工作流程中，有相当一部分错误是因为模型自身的推理能力不足而导致的错误。因此，为了 Agent 能够更好的表现，我们的首要步骤之一便是选用更强大的模型。

在本例中，我们将通过 LiteLLM 库引入第三方模型 Gemini-2.0-Flash 作为替代方案。

```
# model = HfApiModel()
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

#### 步骤3：定义工具

为了实现旅游咨询 Agent 的各项功能，我们需要为其配备以下工具：

*   **维基百科工具**：借助 LangChain 提供的 Wikipedia 工具，获取指定地点的百科介绍。

```
wikipedia_tool = Tool.from_langchain(load_tools(["wikipedia"])[0])
```

*   **天气查询工具**：通过自定义工具调用 WeatherStack API ，实时查询指定地点的天气。

```
@tool
def get_weather(location: str, celsius: Optional[bool] = False) -> str:
    """
    使用 WeatherStack API 获取给定位置的当前天气。

    Args:
        location: 位置（城市名称）。
        celsius: 是否以摄氏度返回温度（默认为 False，返回华氏度）。

    Returns:
        描述给定位置当前天气的字符串。
    """
    api_key = "your_api_key"  # 替换为你从 https://weatherstack.com/ 获取的 API 密钥
    units = "m"  # 'm' 表示摄氏度，'f' 表示华氏度

    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}&units={units}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # 为 HTTP 错误引发异常

        data = response.json()

        if data.get("error"):  # 检查响应中是否存在错误
            return f"错误：{data['error'].get('info', '无法获取天气数据。')}"

        weather = data["current"]["weather_descriptions"][0]
        temp = data["current"]["temperature"]
        temp_unit = "°C" if celsius else "°F"

        return f"{location} 当前的天气是 {weather}，温度为 {temp} {temp_unit}。"

    except requests.exceptions.RequestException as e:
        return f"获取天气数据时出错：{str(e)}"
```

*   **网络搜索工具**：通过内置工具箱中的 DuckDuckGo 工具，搜索指定地点相关信息。

#### 步骤4：初始化 Agent

现在，我们就可以使用定义好的工具来初始化 `CodeAgent` 了：

```
agent = CodeAgent(
    tools=[
        get_weather,
        wikipedia_tool,
        DuckDuckGoSearchTool()
    ],
    model=model,
)
```

#### 步骤5：创建 Gradio 界面

为了方便与 Agent 进行交互，我们使用 GradioUI 创建一个简单的 Web 交互界面：

```
demo = GradioUI(agent)
if __name__ == "__main__":
    demo.launch()
```

#### 步骤6：运行与调试

以下是整合后的完整代码：

```
import os
from smolagents import CodeAgent, LiteLLMModel, tool, GradioUI, Tool, DuckDuckGoSearchTool
from langchain.agents import load_tools

# 定义语言模型
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

# 自定义天气查询工具
@tool
def get_weather(location: str, celsius: bool = False) -> str:
    api_key = "your_api_key"  # 替换为你的 WeatherStack API 密钥
    units = "m" if celsius else "f"
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}&units={units}"
    
    try:
        import requests
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return f"Error: {data['error'].get('info', 'Unable to fetch weather data.')}"
        
        weather = data["current"]["weather_descriptions"][0]
        temp = data["current"]["temperature"]
        unit = "°C" if celsius else "°F"
        return f"The current weather in {location} is {weather} with a temperature of {temp} {unit}."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"

# 引入维基百科工具
wikipedia_tool = Tool.from_langchain(load_tools(["wikipedia"])[0])

# 创建一个 CodeAgent
agent = CodeAgent(
    tools=[
        get_weather,
        wikipedia_tool,
        DuckDuckGoSearchTool()
    ],
    model=model
)

# 创建 Gradio 界面
demo = GradioUI(agent)

# 启动界面
if __name__ == "__main__":
    demo.launch()
```

1.  将以上的完整代码保存为 tourism\_agent.py。
2.  在终端运行以下命令：

```
python tourism_agent.py
```

3\. 打开 Gradio 提供的本地 Web 链接（通常 [http://127.0.0.1:7860），即可与](https://link.juejin.cn/?target=http%3A%2F%2F127.0.0.1%3A7860%25EF%25BC%2589%25EF%25BC%258C%25E5%258D%25B3%25E5%258F%25AF%25E4%25B8%258E "http://127.0.0.1:7860%EF%BC%89%EF%BC%8C%E5%8D%B3%E5%8F%AF%E4%B8%8E") Agent 进行交互。例如：

![Image 16](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5b998c864ba249fc944d85f524b29585~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=N3t5%2FgDAp4DruN%2Fvf6pqCet1i0Q%3D)

网友们都用 SmolAgents 做了什么？
----------------------

接下来，让我们把目光投向更广阔的社区，看看其他开发者们是如何利用 SmolAgents 框架，创造出各种令人惊艳的应用的。

#### Open Deep Search

一个复刻了 OpenAI 的 Deep Search 功能的简化版本

![Image 17](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1482c3acd7674166b3a0098dda957398~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=MIvGeo1nlulc%2FDRcXoVMwjbHaPA%3D)

#### Agent Dino

一个包含音频转录、图像识别、图像生成、联网搜索等功能的综合性 Agent。

![Image 18](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1d24ba43461540d7b3cae77d6aa9b4e6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=Vmm7odXM2uDC5MN6RxjsS%2Boi3DU%3D)

#### 数据分析助手

以自然语言交互，自动化分析上传的数据集。

![Image 19](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fae68dc3e24c4700a2114b2c53516a02~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=LGqmjPn8ecfAPajtL4JbZIGarXM%3D)

#### 博客生成器

生成特定主题、语气的博客内容。

![Image 20](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5698b87458be4d09b34b5b846289e4c7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5pif6ZmF56CB5LuU:q75.awebp?rk3s=f64ab15b&x-expires=1744087167&x-signature=9REUidaA8fTPOkodAWPBtOSE%2BNM%3D)

总结
--

在“极简”理念的推动下，SmolAgents 将复杂的 Agent 开发过程简化为了几行代码，大大降低了开发门槛。同时，它通过代码执行替代传统的 JSON 工具调用，为 Agent 提供了更强的灵活性和表达能力。

此外，SmolAgents 支持多种语言模型和工具集成，能够快速适应不同的场景需求，从自动化日志分析到定制化的旅游助手，展现出卓越的实用性和多样性。

更重要的是，SmolAgents 的开源特性和社区支持，为开发者提供了一个开放且协作的平台。无论是初学者希望快速入门，还是资深开发者想要构建复杂的智能系统，SmolAgents 都能提供理想的解决方案。

让我们从这篇文章开始，探索 SmolAgents 的更多可能性，创造出更多有趣的 Agent 应用吧！
