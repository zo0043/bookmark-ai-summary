Title: llama-agents+chainlit打造超级智能体

URL Source: https://blog.stoeng.site/20240701.html

Markdown Content:
https://github.com/run-llama/llama-agents

[https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems](https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems)

### chainlit安装

```
安装
pip install chainlit

#运行
chainlit run app-ui.py -w
```

### yfinance安装

> yfinance 是一个 Python 库，用于从 Yahoo Finance 下载市场数据。它提供了一种线程化和 Python 化的方式来获取股票、ETF、共同基金、货币、期权等金融工具的历史和实时数据。

```
pip install yfinance
```

### llama-agents安装

```

pip install llama-agents llama-index-agent-openai llama-index-embeddings-openai llama-index-program-openai

#.env文件中放入api key
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-xxx


https://docs.llamaindex.ai/en/stable/api_reference/llms/ollama/






```

### ollama接口支持示例

```

from llama_index.llms.ollama import Ollama

ollama_llm = Ollama(model="gemma2", request_timeout=120.0)

tool = FunctionTool.from_defaults(fn=<function>)

agent1 = ReActAgent.from_tools([tool], llm=ollama_llm)
agent2 = ReActAgent.from_tools([], llm=ollama_llm)


```

**👉👉👉如有问题请联系我的徽信 stoeng**
----------------------------

**🔥🔥🔥本项目代码由AI超元域频道制作，观看更多大模型微调视频请访问我的频道⬇**
---------------------------------------------

### **👉👉👉****[我的哔哩哔哩频道](https://space.bilibili.com/3493277319825652)**

### **👉👉👉****[我的YouTube频道](https://www.youtube.com/@AIsuperdomain)**

### **👉👉👉我的开源项目** **[https://github.com/win4r/AISuperDomain](https://github.com/win4r/AISuperDomain)**

### Anthropic接口支持示例

```
import os
from dotenv import load_dotenv
import yfinance as yf
from llama_agents.launchers.local import LocalLauncher
from llama_agents.services import AgentService, ToolService
from llama_agents.tools import MetaServiceTool
from llama_agents.control_plane.server import ControlPlaneServer
from llama_agents.message_queues.simple import SimpleMessageQueue
from llama_agents.orchestrators.agent import AgentOrchestrator
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic

from llama_index.llms.ollama import Ollama


# 加载.env文件
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv("ANTHROPIC_API_KEY")

# 确保API密钥已设置
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# 设置OpenAI API密钥
os.environ["ANTHROPIC_API_KEY"] = api_key

# 其余代码保持不变
def get_stock_price(symbol: str) -> str:
    """获取给定股票代码的当前价格"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return f"The current price of {symbol} is ${current_price:.2f}"
        else:
            return f"Unable to fetch the current price for {symbol}. The stock data is empty."
    except Exception as e:
        return f"Error fetching stock price for {symbol}: {str(e)}"

def get_company_info(symbol: str) -> str:
    """获取给定股票代码的公司信息"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return f"{info['longName']} ({symbol}) is in the {info.get('sector', 'Unknown')} sector. {info.get('longBusinessSummary', '')[:200]}..."
    except Exception as e:
        return f"Error fetching company info for {symbol}: {str(e)}"

stock_price_tool = FunctionTool.from_defaults(fn=get_stock_price)
company_info_tool = FunctionTool.from_defaults(fn=get_company_info)

# 指定 OpenAI 模型
llm = Anthropic(model="claude-3-sonnet-20240229")


# create our multi-agent framework components
message_queue = SimpleMessageQueue()
tool_service = ToolService(
    message_queue=message_queue,
    tools=[stock_price_tool, company_info_tool],
    running=True,
    step_interval=0.5,
)
control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=AgentOrchestrator(llm=llm),
)
meta_tools = [
    MetaServiceTool(
        tool_metadata=tool.metadata,
        message_queue=message_queue,
        tool_service_name=tool_service.service_name,
    ) for tool in [stock_price_tool, company_info_tool]
]
worker1 = FunctionCallingAgentWorker.from_tools(
    meta_tools,
    llm=llm,
)
agent1 = worker1.as_agent()
agent_server_1 = AgentService(
    agent=agent1,
    message_queue=message_queue,
    description="Useful for getting stock information.",
    service_name="stock_info_agent",
)
# launch it
launcher = LocalLauncher(
    [agent_server_1, tool_service],
    control_plane,
    message_queue,
)
result = launcher.launch_single("What's the current price of AAPL and what does the company do?")
print(f"Result: {result}")
```

### 股票分析：

```
# 导入所需的库
import os
import logging
from dotenv import load_dotenv
import yfinance as yf
from llama_agents.launchers.local import LocalLauncher
from llama_agents.services import AgentService, ToolService
from llama_agents.tools import MetaServiceTool
from llama_agents.control_plane.server import ControlPlaneServer
from llama_agents.message_queues.simple import SimpleMessageQueue
from llama_agents.orchestrators.agent import AgentOrchestrator
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

# 设置日志级别为INFO
logging.basicConfig(level=logging.INFO)

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取OpenAI API密钥
api_key = os.getenv("OPENAI_API_KEY")

# 确保API密钥已设置,否则抛出异常
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# 设置OpenAI API密钥为环境变量
os.environ["OPENAI_API_KEY"] = api_key

# 定义获取股票当前价格的函数
def get_stock_price(symbol: str) -> str:
    """获取给定股票代码的当前价格"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return f"The current price of {symbol} is ${current_price:.2f}"
        else:
            return f"Unable to fetch the current price for {symbol}. The stock data is empty."
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {str(e)}")
        return f"Error fetching stock price for {symbol}: {str(e)}"

# 定义获取公司信息的函数
def get_company_info(symbol: str) -> str:
    """获取给定股票代码的公司信息"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return f"{info['longName']} ({symbol}) is in the {info.get('sector', 'Unknown')} sector. {info.get('longBusinessSummary', '')[:200]}..."
    except Exception as e:
        logging.error(f"Error fetching company info for {symbol}: {str(e)}")
        return f"Error fetching company info for {symbol}: {str(e)}"

# 定义获取财务比率的函数
def get_financial_ratios(symbol: str) -> str:
    """获取给定股票的关键财务比率"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        pe_ratio = info.get('trailingPE', 'N/A')
        pb_ratio = info.get('priceToBook', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        if dividend_yield != 'N/A':
            dividend_yield = f"{dividend_yield * 100:.2f}%"
        return f"{symbol} financial ratios: P/E: {pe_ratio}, P/B: {pb_ratio}, Dividend Yield: {dividend_yield}"
    except Exception as e:
        logging.error(f"Error fetching financial ratios for {symbol}: {str(e)}")
        return f"Error fetching financial ratios for {symbol}: {str(e)}"

# 定义获取分析师推荐的函数
def get_analyst_recommendations(symbol: str) -> str:
    """获取分析师对给定股票的推荐"""
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations
        if recommendations is not None and not recommendations.empty:
            latest_rec = recommendations.iloc[-1]
            return f"Latest analyst recommendation for {symbol}: {latest_rec['To Grade']} as of {latest_rec.name.date()}"
        else:
            return f"No analyst recommendations available for {symbol}"
    except Exception as e:
        logging.error(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
        return f"Unable to fetch analyst recommendations for {symbol} due to an error: {str(e)}"

# 定义获取最新新闻的函数
def get_recent_news(symbol: str) -> str:
    """获取与给定股票相关的最新新闻"""
    try:
        stock = yf.Ticker(symbol)
        news = stock.news
        if news:
            latest_news = news[0]
            return f"Latest news for {symbol}: {latest_news['title']} - {latest_news['link']}"
        else:
            return f"No recent news available for {symbol}"
    except Exception as e:
        logging.error(f"Error fetching recent news for {symbol}: {str(e)}")
        return f"Error fetching recent news for {symbol}: {str(e)}"

# 定义获取行业比较的函数
def get_industry_comparison(symbol: str) -> str:
    """获取股票与行业平均水平的比较"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        pe_ratio = info.get('trailingPE', 'N/A')
        industry_pe = info.get('industryPE', 'N/A')

        comparison = f"{symbol} is in the {sector} sector, specifically in the {industry} industry. "
        if pe_ratio != 'N/A' and industry_pe != 'N/A':
            if pe_ratio < industry_pe:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is lower than the industry average ({industry_pe:.2f}), which could indicate it's undervalued compared to its peers."
            elif pe_ratio > industry_pe:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is higher than the industry average ({industry_pe:.2f}), which could indicate it's overvalued compared to its peers."
            else:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is in line with the industry average ({industry_pe:.2f})."
        else:
            comparison += "Unable to compare P/E ratio with industry average due to lack of data."

        return comparison
    except Exception as e:
        logging.error(f"Error fetching industry comparison for {symbol}: {str(e)}")
        return f"Unable to fetch industry comparison for {symbol} due to an error: {str(e)}"

# 创建工具对象,每个工具对应一个函数
stock_price_tool = FunctionTool.from_defaults(fn=get_stock_price)
company_info_tool = FunctionTool.from_defaults(fn=get_company_info)
financial_ratios_tool = FunctionTool.from_defaults(fn=get_financial_ratios)
analyst_recommendations_tool = FunctionTool.from_defaults(fn=get_analyst_recommendations)
recent_news_tool = FunctionTool.from_defaults(fn=get_recent_news)
industry_comparison_tool = FunctionTool.from_defaults(fn=get_industry_comparison)

# 指定使用的OpenAI模型
llm = OpenAI(model="gpt-4o", temperature=0)

# 创建消息队列
message_queue = SimpleMessageQueue()

# 创建工具服务,包含所有定义的工具
tool_service = ToolService(
    message_queue=message_queue,
    tools=[stock_price_tool, company_info_tool, financial_ratios_tool, analyst_recommendations_tool, recent_news_tool,
           industry_comparison_tool],
    running=True,
    step_interval=0.5,
)

# 创建控制平面服务器
control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=AgentOrchestrator(llm=llm),
)

# 创建元工具列表,每个元工具对应一个实际工具
meta_tools = [
    MetaServiceTool(
        tool_metadata=tool.metadata,
        message_queue=message_queue,
        tool_service_name=tool_service.service_name,
    ) for tool in
    [stock_price_tool, company_info_tool, financial_ratios_tool, analyst_recommendations_tool, recent_news_tool,
     industry_comparison_tool]
]

# 创建代理工作器,设置系统提示
worker1 = FunctionCallingAgentWorker.from_tools(
    meta_tools,
    llm=llm,
    system_prompt="""你是一个专业的股票分析师。你的任务是分析给定的股票,并根据所有可用信息提供是否购买的建议。
    请使用所有可用工具来收集相关信息,然后给出全面的分析和明确的建议。
    考虑当前价格、公司信息、财务比率、分析师推荐、最新新闻和行业比较。
    解释你的推荐理由,并提供一个清晰的"买入"、"持有"或"卖出"建议。
    如果某些信息无法获取,请在分析中说明,并基于可用信息给出最佳判断。
    """
)

# 将工作器转换为代理
agent1 = worker1.as_agent()

# 创建代理服务
agent_server_1 = AgentService(
    agent=agent1,
    message_queue=message_queue,
    description="Useful for analyzing stocks and providing investment recommendations.",
    service_name="stock_analysis_agent",
)

# 创建本地启动器
launcher = LocalLauncher(
    [agent_server_1, tool_service],
    control_plane,
    message_queue,
)

# 执行股票分析
result = launcher.launch_single("""
分析 AAPL 股票是否值得购买。
请考虑以下因素:
1. 当前股价
2. 公司基本信息
3. 关键财务比率（如 P/E、P/B、股息收益率）
4. 分析师推荐
5. 最新相关新闻
6. 与行业平均水平的比较
根据这些信息，给出你的投资建议（买入、持有或卖出）并详细解释理由。
如果某些信息无法获取，请在分析中说明，并基于可用信息给出最佳判断。
""")

# 打印分析结果
print(f"Result: {result}")
```

### RAG

```
import os
import logging
from dotenv import load_dotenv

# 导入必要的 llama_index 模块
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
# 导入 llama_agents 相关模块
from llama_agents import (
    AgentService,
    ToolService,
    LocalLauncher,
    MetaServiceTool,
    ControlPlaneServer,
    SimpleMessageQueue,
    AgentOrchestrator,
)
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.llms.openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 OpenAI API 密钥
api_key = os.getenv("OPENAI_API_KEY")

# 确保 API 密钥已设置,否则抛出异常
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# 设置 OpenAI API 密钥为环境变量
os.environ["OPENAI_API_KEY"] = api_key

# 设置 llama_agents 的日志级别为 INFO
logging.getLogger("llama_agents").setLevel(logging.INFO)

# 加载并索引数据
def load_and_index_data():
    try:
        # 尝试从已保存的存储中加载索引
        storage_context = StorageContext.from_defaults(persist_dir="./storage/lyft")
        lyft_index = load_index_from_storage(storage_context)

        storage_context = StorageContext.from_defaults(persist_dir="./storage/uber")
        uber_index = load_index_from_storage(storage_context)
    except:
        # 如果索引不存在,则创建新的索引
        lyft_docs = SimpleDirectoryReader(input_files=["./data/10k/lyft_2021.pdf"]).load_data()
        uber_docs = SimpleDirectoryReader(input_files=["./data/10k/uber_2021.pdf"]).load_data()

        lyft_index = VectorStoreIndex.from_documents(lyft_docs)
        uber_index = VectorStoreIndex.from_documents(uber_docs)

        # 保存新创建的索引
        lyft_index.storage_context.persist(persist_dir="./storage/lyft")
        uber_index.storage_context.persist(persist_dir="./storage/uber")

    return lyft_index, uber_index

# 设置查询引擎和工具
def setup_query_engines_and_tools(lyft_index, uber_index):
    # 创建 Lyft 和 Uber 的查询引擎
    lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)
    uber_engine = uber_index.as_query_engine(similarity_top_k=3)

    # 创建查询引擎工具列表
    query_engine_tools = [
        QueryEngineTool(
            query_engine=lyft_engine,
            metadata=ToolMetadata(
                name="lyft_10k",
                description="Provides information about Lyft financials for year 2021. "
                            "Use a detailed plain text question as input to the tool.",
            ),
        ),
        QueryEngineTool(
            query_engine=uber_engine,
            metadata=ToolMetadata(
                name="uber_10k",
                description="Provides information about Uber financials for year 2021. "
                            "Use a detailed plain text question as input to the tool.",
            ),
        ),
    ]

    return query_engine_tools

# 设置代理和服务
async def setup_agents_and_services(query_engine_tools):
    # 创建消息队列
    message_queue = SimpleMessageQueue()
    # 创建控制平面服务器
    control_plane = ControlPlaneServer(
        message_queue=message_queue,
        orchestrator=AgentOrchestrator(llm=OpenAI(model="gpt-4o")),
    )

    # 创建工具服务
    tool_service = ToolService(
        message_queue=message_queue,
        tools=query_engine_tools,
        running=True,
        step_interval=0.5,
    )

    # 创建元工具列表
    meta_tools = [
        await MetaServiceTool.from_tool_service(
            t.metadata.name,
            message_queue=message_queue,
            tool_service=tool_service,
        )
        for t in query_engine_tools
    ]

    # 创建函数调用代理工作器
    worker1 = FunctionCallingAgentWorker.from_tools(
        meta_tools,
        llm=OpenAI(),
    )
    # 将工作器转换为代理
    agent1 = worker1.as_agent()
    # 创建代理服务
    agent_server_1 = AgentService(
        agent=agent1,
        message_queue=message_queue,
        description="Used to answer questions over Uber and Lyft 10K documents",
        service_name="uber_lyft_10k_analyst_agent",
    )

    # 创建本地启动器
    launcher = LocalLauncher(
        [agent_server_1, tool_service],
        control_plane,
        message_queue,
    )

    return launcher

# 主函数,用于运行整个脚本
async def main():
    # 加载并索引数据
    lyft_index, uber_index = load_and_index_data()
    # 设置查询引擎和工具
    query_engine_tools = setup_query_engines_and_tools(lyft_index, uber_index)
    # 设置代理和服务
    launcher = await setup_agents_and_services(query_engine_tools)

    # 示例查询
    queries = [
        "What are the risk factors for Uber?",
        "What was Lyft's revenue growth in 2021?",
    ]

    # 执行查询并打印结果
    for query in queries:
        print(f"Query: {query}")
        result = await launcher.alaunch_single(query)  # 使用 alaunch_single 而不是 launch_single
        print(f"Result: {result}\n")

# 运行主函数
if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```

### chainlit+llama-agents

```
import chainlit as cl
import os
import logging
from dotenv import load_dotenv
import yfinance as yf
from llama_agents.launchers.local import LocalLauncher
from llama_agents.services import AgentService, ToolService
from llama_agents.tools import MetaServiceTool
from llama_agents.control_plane.server import ControlPlaneServer
from llama_agents.message_queues.simple import SimpleMessageQueue
from llama_agents.orchestrators.agent import AgentOrchestrator
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

# 设置日志
logging.basicConfig(level=logging.INFO)

# 加载.env文件
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv("OPENAI_API_KEY")

# 确保API密钥已设置
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# 设置OpenAI API密钥
os.environ["OPENAI_API_KEY"] = api_key


# 定义所有需要的函数
def get_stock_price(symbol: str) -> str:
    """获取给定股票代码的当前价格"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return f"The current price of {symbol} is ${current_price:.2f}"
        else:
            return f"Unable to fetch the current price for {symbol}. The stock data is empty."
    except Exception as e:
        logging.error(f"Error fetching stock price for {symbol}: {str(e)}")
        return f"Error fetching stock price for {symbol}: {str(e)}"


def get_company_info(symbol: str) -> str:
    """获取给定股票代码的公司信息"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return f"{info['longName']} ({symbol}) is in the {info.get('sector', 'Unknown')} sector. {info.get('longBusinessSummary', '')[:200]}..."
    except Exception as e:
        logging.error(f"Error fetching company info for {symbol}: {str(e)}")
        return f"Error fetching company info for {symbol}: {str(e)}"


def get_financial_ratios(symbol: str) -> str:
    """获取给定股票的关键财务比率"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        pe_ratio = info.get('trailingPE', 'N/A')
        pb_ratio = info.get('priceToBook', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        if dividend_yield != 'N/A':
            dividend_yield = f"{dividend_yield * 100:.2f}%"
        return f"{symbol} financial ratios: P/E: {pe_ratio}, P/B: {pb_ratio}, Dividend Yield: {dividend_yield}"
    except Exception as e:
        logging.error(f"Error fetching financial ratios for {symbol}: {str(e)}")
        return f"Error fetching financial ratios for {symbol}: {str(e)}"


def get_analyst_recommendations(symbol: str) -> str:
    """获取分析师对给定股票的推荐"""
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations
        if recommendations is not None and not recommendations.empty:
            latest_rec = recommendations.iloc[-1]
            return f"Latest analyst recommendation for {symbol}: {latest_rec['To Grade']} as of {latest_rec.name.date()}"
        else:
            return f"No analyst recommendations available for {symbol}"
    except Exception as e:
        logging.error(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
        return f"Unable to fetch analyst recommendations for {symbol} due to an error: {str(e)}"


def get_recent_news(symbol: str) -> str:
    """获取与给定股票相关的最新新闻"""
    try:
        stock = yf.Ticker(symbol)
        news = stock.news
        if news:
            latest_news = news[0]
            return f"Latest news for {symbol}: {latest_news['title']} - {latest_news['link']}"
        else:
            return f"No recent news available for {symbol}"
    except Exception as e:
        logging.error(f"Error fetching recent news for {symbol}: {str(e)}")
        return f"Error fetching recent news for {symbol}: {str(e)}"


def get_industry_comparison(symbol: str) -> str:
    """获取股票与行业平均水平的比较"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        pe_ratio = info.get('trailingPE', 'N/A')
        industry_pe = info.get('industryPE', 'N/A')

        comparison = f"{symbol} is in the {sector} sector, specifically in the {industry} industry. "
        if pe_ratio != 'N/A' and industry_pe != 'N/A':
            if pe_ratio < industry_pe:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is lower than the industry average ({industry_pe:.2f}), which could indicate it's undervalued compared to its peers."
            elif pe_ratio > industry_pe:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is higher than the industry average ({industry_pe:.2f}), which could indicate it's overvalued compared to its peers."
            else:
                comparison += f"Its P/E ratio ({pe_ratio:.2f}) is in line with the industry average ({industry_pe:.2f})."
        else:
            comparison += "Unable to compare P/E ratio with industry average due to lack of data."

        return comparison
    except Exception as e:
        logging.error(f"Error fetching industry comparison for {symbol}: {str(e)}")
        return f"Unable to fetch industry comparison for {symbol} due to an error: {str(e)}"


# 创建全局变量来存储launcher
global_launcher = None


@cl.on_chat_start
async def start():
    global global_launcher

    # 创建工具对象,每个工具对应一个函数
    stock_price_tool = FunctionTool.from_defaults(fn=get_stock_price)
    company_info_tool = FunctionTool.from_defaults(fn=get_company_info)
    financial_ratios_tool = FunctionTool.from_defaults(fn=get_financial_ratios)
    analyst_recommendations_tool = FunctionTool.from_defaults(fn=get_analyst_recommendations)
    recent_news_tool = FunctionTool.from_defaults(fn=get_recent_news)
    industry_comparison_tool = FunctionTool.from_defaults(fn=get_industry_comparison)

    # 指定 OpenAI 模型
    llm = OpenAI(model="gpt-4o", temperature=0)

    # 创建多代理框架组件
    message_queue = SimpleMessageQueue()
    tool_service = ToolService(
        message_queue=message_queue,
        tools=[stock_price_tool, company_info_tool, financial_ratios_tool, analyst_recommendations_tool,
               recent_news_tool,
               industry_comparison_tool],
        running=True,
        step_interval=0.5,
    )
    control_plane = ControlPlaneServer(
        message_queue=message_queue,
        orchestrator=AgentOrchestrator(llm=llm),
    )
    meta_tools = [
        MetaServiceTool(
            tool_metadata=tool.metadata,
            message_queue=message_queue,
            tool_service_name=tool_service.service_name,
        ) for tool in
        [stock_price_tool, company_info_tool, financial_ratios_tool, analyst_recommendations_tool, recent_news_tool,
         industry_comparison_tool]
    ]

    # 创建代理工作器
    worker1 = FunctionCallingAgentWorker.from_tools(
        meta_tools,
        llm=llm,
        system_prompt="""你是一个专业的股票分析师。你的任务是分析给定的股票,并根据所有可用信息提供是否购买的建议。
        请使用所有可用工具来收集相关信息,然后给出全面的分析和明确的建议。
        考虑当前价格、公司信息、财务比率、分析师推荐、最新新闻和行业比较。
        解释你的推荐理由,并提供一个清晰的"买入"、"持有"或"卖出"建议。
        如果某些信息无法获取,请在分析中说明,并基于可用信息给出最佳判断。
        """
    )
    agent1 = worker1.as_agent()
    agent_server_1 = AgentService(
        agent=agent1,
        message_queue=message_queue,
        description="Useful for analyzing stocks and providing investment recommendations.",
        service_name="stock_analysis_agent",
    )

    # 启动
    global_launcher = LocalLauncher(
        [agent_server_1, tool_service],
        control_plane,
        message_queue,
    )

    await cl.Message(content="股票分析助手已准备就绪。请输入您想分析的股票代码。").send()


@cl.on_message
async def main(message: cl.Message):
    stock_symbol = message.content.strip().upper()

    prompt = f"""
    分析 {stock_symbol} 股票是否值得购买。
    请考虑以下因素:
    1. 当前股价
    2. 公司基本信息
    3. 关键财务比率（如 P/E、P/B、股息收益率）
    4. 分析师推荐
    5. 最新相关新闻
    6. 与行业平均水平的比较
    根据这些信息，给出你的投资建议（买入、持有或卖出）并详细解释理由。
    如果某些信息无法获取，请在分析中说明，并基于可用信息给出最佳判断。
    """

    result = await global_launcher.alaunch_single(prompt)

    await cl.Message(content=f"对 {stock_symbol} 的分析结果：\n\n{result}").send()
```
