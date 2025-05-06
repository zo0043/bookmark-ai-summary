Title: Quick Primer on Model Context Protocol (MCP)

URL Source: https://www.polarsparc.com/xhtml/MCP.html

Markdown Content:


	PolarSPARC



Quick Primer on Model Context Protocol (MCP)



Bhaskar S	04/13/2025



Overview

When LLMs first made their first appearance, the Enterprise apps built using LLMs were restricted to the knowledge on what the LLMs where trained on. These apps were useful for a set of tasks such as, text generation, text sentiment analysis, text summarization, etc.

The next evolution for LLM apps was the integration with Enterprise data assets via the Vector Stores for contextual knowledge retrieval using RAGs.

As agentic frameworks like LangChain came along with support for tools integration for automating manual tasks, the LLM apps evolved to drive automation in the Enterprise environment.

The challenge however was that there was no industry standard for tools integration and every framework had its own approach to tools integration.

Enter the Model Context Protocol (or MCP) that has changed the landscape for tools integration.

Think of MCP as a industry standard layer on top of the other Enterprise services that allows any agentic framework (such as LangChain, LlamaIndex, etc) to consistently integrate with the Enterprise tools.

In other words, MCP is an open protocol that enables seamless integration between the LLM apps and the external data sources (databases, files, etc) and tools (github, servicenow, etc).

The MCP specification consists of the following core components:

MCP Server: connects to various external as well as internal data sources and tools for exposing specific capabilities to the agentic LLM apps. Think of these as service providers
MCP Client: connects and interacts with the MCP Server(s) in a standardized manner
MCP Host: the LLM app(s) that use the MCP Client to access the MCP Server(s)



Installation and Setup

The installation and setup will be on a Ubuntu 24.04 LTS based Linux desktop. Ensure that Python 3.x programming language is installed and setup on the desktop.

In addition, ensure that Ollama is installed and setup on the Linux desktop (refer to for instructions).

Assuming that the ip address on the Linux desktop is 192.168.1.25, start the Ollama platform by executing the following command in the terminal window:




$ docker run --rm --name ollama --network=host -p 192.168.1.25:11434:11434 -v $HOME/.ollama:/root/.ollama ollama/ollama:0.6.5




For the LLM model, we will be using the recently released IBM Granite-3.3 2B model.

Open a new terminal window and execute the following docker command to download the LLM model:




$ docker exec -it ollama ollama run granite3.3:2b




To install the necessary Python modules for this primer, execute the following command:




$ pip install dotenv langchain lanchain-core langchain-ollama langgraph mcp langchain-mcp-adapters starlette sse-starlette uvicorn




This completes all the installation and setup for the MCP hands-on demonstrations using Python.




Hands-on with MCP (using Python)




In the following sections, we will get our hands dirty with the MCP using Ollama and LangChain. So, without further ado, let us get started !!!

Create a file called .env with the following environment variables defined:



.env
LLM_TEMPERATURE=0.2
OLLAMA_MODEL='granite3.3:2b'
OLLAMA_BASE_URL='http://192.168.1.25:11434'
PY_PROJECT_DIR='/projects/python/MCP/'
SSE_BASE_URL='http://192.168.1.25:8000/sse'



The following is a simple LangChain based ReACT app:



interest_client.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   06 April 2025
#

import asyncio
import logging
import os

from dotenv import load_dotenv, find_dotenv
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('interest_client')

load_dotenv(find_dotenv())

home_dir = os.getenv('HOME')
llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
ollama_model = os.getenv('OLLAMA_MODEL')
ollama_base_url = os.getenv('OLLAMA_BASE_URL')
py_project_dir = os.getenv('PY_PROJECT_DIR')

ollama_chat_llm = ChatOllama(base_url=ollama_base_url, model=ollama_model, temperature=llm_temperature)

@tool
def dummy():
  """This is a dummy tool"""
  return None

async def main():
  tools = [dummy]

  # Initialize a ReACT agent
  agent = create_react_agent(ollama_chat_llm, tools)

  # Case - 1 : Simple interest definition
  agent_response_1 = await agent.ainvoke(
    {'messages': 'what is the simple interest ?'})
  logger.info(agent_response_1['messages'][::-1])

  # Case - 2 : Simple interest calculation
  agent_response_2 = await agent.ainvoke(
    {'messages': 'compute the simple interest for a principal of 1000 at rate 3.75 ?'})
  logger.info(agent_response_2['messages'][::-1])

  # Case - 3 : Compound interest calculation
  agent_response_3 = await agent.ainvoke(
    {'messages': 'compute the compound interest for a principal of 1000 at rate 4.25 ?'})
  logger.info(agent_response_3['messages'][::-1])


if __name__ == '__main__':
  asyncio.run(main())



To execute the above Python code, execute the following command in a terminal window:




$ python interest_client.py




The following would be the typical output:



Output.1
INFO 2025-04-13 09:54:41,426 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 09:54:41,428 - [AIMessage(content='The simple interest (SI) is calculated using the formula:\n\nSI = P * R * T / 100\n\nWhere:\n- P is the principal amount (the initial sum of money)\n- R is the rate of interest per annum\n- T is the time in years\n\nFor example, if you have Rs. 1000 as a principal amount with an annual interest rate of 5% for 2 years, then:\n\nSI = 1000 * 5/100 * 2 / 100\nSI = 1000 * 0.05 * 2 / 100\nSI = 1000 * 0.10 / 100\nSI = Rs. 10', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T13:54:41.425392119Z', 'done': True, 'done_reason': 'stop', 'total_duration': 1338038780, 'load_duration': 6784726, 'prompt_eval_count': 84, 'prompt_eval_duration': 31132026, 'eval_count': 172, 'eval_duration': 1298733422, 'message': Message(role='assistant', content='The simple interest (SI) is calculated using the formula:\n\nSI = P * R * T / 100\n\nWhere:\n- P is the principal amount (the initial sum of money)\n- R is the rate of interest per annum\n- T is the time in years\n\nFor example, if you have Rs. 1000 as a principal amount with an annual interest rate of 5% for 2 years, then:\n\nSI = 1000 * 5/100 * 2 / 100\nSI = 1000 * 0.05 * 2 / 100\nSI = 1000 * 0.10 / 100\nSI = Rs. 10', images=None, tool_calls=None)}, id='run-d5a4f021-1a87-4bac-b6a4-5dc3239e6f7b-0', usage_metadata={'input_tokens': 84, 'output_tokens': 172, 'total_tokens': 256}), HumanMessage(content='what is the simple interest ?', additional_kwargs={}, response_metadata={}, id='aee2669b-36d3-42aa-bdb6-53fd2454ea12')]
INFO 2025-04-13 09:54:41,604 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 09:54:41,605 - [AIMessage(content='{"code":200,"message":"Interest Calculation Completed"}', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T13:54:41.603723234Z', 'done': True, 'done_reason': 'stop', 'total_duration': 173677918, 'load_duration': 6716296, 'prompt_eval_count': 99, 'prompt_eval_duration': 36381866, 'eval_count': 15, 'eval_duration': 129621404, 'message': Message(role='assistant', content='{"code":200,"message":"Interest Calculation Completed"}', images=None, tool_calls=None)}, id='run-a73da0a1-6862-4aba-ba1d-095df8a85e0c-0', usage_metadata={'input_tokens': 99, 'output_tokens': 15, 'total_tokens': 114}), HumanMessage(content='compute the simple interest for a principal of 1000 at rate 3.75 ?', additional_kwargs={}, response_metadata={}, id='2d929265-e096-4275-aaa1-001f15d34047')]
INFO 2025-04-13 09:54:41,771 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 09:54:41,773 - [AIMessage(content='{"code":301,"message":"Compound Interest Formula Calculation"}', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T13:54:41.771498307Z', 'done': True, 'done_reason': 'stop', 'total_duration': 164399085, 'load_duration': 6787425, 'prompt_eval_count': 99, 'prompt_eval_duration': 43029403, 'eval_count': 17, 'eval_duration': 113471897, 'message': Message(role='assistant', content='{"code":301,"message":"Compound Interest Formula Calculation"}', images=None, tool_calls=None)}, id='run-7dfd2c78-0847-461c-a822-eb4b4c4f54a3-0', usage_metadata={'input_tokens': 99, 'output_tokens': 17, 'total_tokens': 116}), HumanMessage(content='compute the compound interest for a principal of 1000 at rate 4.25 ?', additional_kwargs={}, response_metadata={}, id='284397b4-2575-46d6-bebc-83bff0c6f64f')]



It is evident from the above Output.1 that the LLM app was able to define what simple interest was, however was not able to compute either the simple interest or the compound interest.

Let us now build our first MCP Server for computing both the simple interest (for a year) and the compound interest (for a year).

The following is our first MCP Server code in Python:



interest_mcp_server.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   06 April 2025
#

from mcp.server.fastmcp import FastMCP

import logging

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('interest_mcp_server')

mcp = FastMCP('InterestCalculator')

@mcp.tool()
def yearly_simple_interest(principal: float, rate:float) -> float:
  """Tool to compute simple interest rate for a year."""
  logger.info(f'Simple interest -> Principal: {principal}, Rate: {rate}')
  return principal * rate / 100.00

@mcp.tool()
def yearly_compound_interest(principal: float, rate:float) -> float:
  """Tool to compute compound interest rate for a year."""
  logger.info(f'Compound interest -> Principal: {principal}, Rate: {rate}')
  return principal * (1 + rate / 100.0)

if __name__ == '__main__':
  logger.info(f'Starting the interest MCP server...')
  mcp.run(transport='stdio')



There are two types of transports supported by the MCP specification which are as follows:

Standard IO (stdio): enables communication through standard input and output streams that is useful for integrations with command-line tools
Server Sent Events (sse): enables server to client streaming with HTTP POST requests that is useful for integrations with network enabled services

In our example, we choose the stdio transport.

The next step is to build a MCP Host (LLM app) that uses a MCP Client to access the above MCP Server for computing both the simple interest and the compound interest.

The following is our first MCP Host LLM app code in Python:



interest_mcp_client.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   06 April 2025
#

from dotenv import load_dotenv, find_dotenv
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import asyncio
import logging
import os

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('interest_mcp_client')

load_dotenv(find_dotenv())

home_dir = os.getenv('HOME')
llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
ollama_model = os.getenv('OLLAMA_MODEL')
ollama_base_url = os.getenv('OLLAMA_BASE_URL')
py_project_dir = os.getenv('PY_PROJECT_DIR')

server_params = StdioServerParameters(
  command='python',
  # Full absolute path to mcp server
  args=[home_dir + py_project_dir + 'interest_mcp_server.py'],
)

ollama_chat_llm = ChatOllama(base_url=ollama_base_url, model=ollama_model, temperature=llm_temperature)

async def main():
  # Will launch the MCP server and communicate via stdio/stdout
  async with stdio_client(server_params) as (read, write):
    # Create a MCP client session
    async with ClientSession(read, write) as session:
      # Connect to the MCP server
      await session.initialize()

      # Get the list of all the registered tools
      tools = await load_mcp_tools(session)

      logger.info(f'Loaded MCP Tools -> {tools}')

      # Initialize a ReACT agent
      agent = create_react_agent(ollama_chat_llm, tools)

      # Case - 1 : Simple interest definition
      agent_response_1 = await agent.ainvoke(
        {'messages': 'explain the definition of simple interest ?'})
      logger.info(agent_response_1['messages'][::-1])

      # Case - 2 : Simple interest calculation
      agent_response_2 = await agent.ainvoke(
        {'messages': 'compute the simple interest for a principal of 1000 at rate 3.75 ?'})
      logger.info(agent_response_2['messages'][::-1])

      # Case - 3 : Compound interest calculation
      agent_response_3 = await agent.ainvoke(
        {'messages': 'compute the compound interest for a principal of 1000 at rate 4.25 ?'})
      logger.info(agent_response_3['messages'][::-1])

if __name__ == '__main__':
  asyncio.run(main())



To execute the above Python code, execute the following command in a terminal window:




$ python interest_mcp_client.py




The following would be the typical output:



Output.2
INFO 2025-04-13 10:24:36,353 - Starting the interest MCP server...
INFO 2025-04-13 10:24:36,358 - Processing request of type ListToolsRequest
INFO 2025-04-13 10:24:36,359 - Loaded MCP Tools -> [StructuredTool(name='yearly_simple_interest', description='Tool to compute simple interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_simple_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x76293a568720>), StructuredTool(name='yearly_compound_interest', description='Tool to compute compound interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_compound_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x76293a568900>)]
INFO 2025-04-13 10:24:38,406 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 10:24:38,408 - [AIMessage(content='Simple Interest (SI) is a method of calculating interest where only the principal amount (the initial sum of money) and not the accumulated interest, is used to calculate the total interest paid or earned over a specific period. The formula for Simple Interest is:\n\nSI = P * R * T / 100\n\nWhere:\n- P is the principal amount (the initial sum of money)\n- R is the rate of interest per annum\n- T is the time in years\n\nThe SI is calculated by multiplying the principal by the rate and then dividing it by 100. The result gives you the total interest for that period, expressed as a percentage of the principal amount. For example, if you have $1000 as your principal, an annual interest rate of 5%, and you want to know how much you would earn in one year, you would calculate:\n\nSI = 1000 * 5/100 * 1 = $50\n\nThis means that for every $1000 you have, you would earn $50 in interest over the course of a year.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T14:24:38.405888113Z', 'done': True, 'done_reason': 'stop', 'total_duration': 2038184289, 'load_duration': 4645995, 'prompt_eval_count': 179, 'prompt_eval_duration': 34893791, 'eval_count': 248, 'eval_duration': 1997458315, 'message': Message(role='assistant', content='Simple Interest (SI) is a method of calculating interest where only the principal amount (the initial sum of money) and not the accumulated interest, is used to calculate the total interest paid or earned over a specific period. The formula for Simple Interest is:\n\nSI = P * R * T / 100\n\nWhere:\n- P is the principal amount (the initial sum of money)\n- R is the rate of interest per annum\n- T is the time in years\n\nThe SI is calculated by multiplying the principal by the rate and then dividing it by 100. The result gives you the total interest for that period, expressed as a percentage of the principal amount. For example, if you have $1000 as your principal, an annual interest rate of 5%, and you want to know how much you would earn in one year, you would calculate:\n\nSI = 1000 * 5/100 * 1 = $50\n\nThis means that for every $1000 you have, you would earn $50 in interest over the course of a year.', images=None, tool_calls=None)}, id='run-4877f653-8e87-44b9-9f23-3ead28ba5441-0', usage_metadata={'input_tokens': 179, 'output_tokens': 248, 'total_tokens': 427}), HumanMessage(content='explain the definition of simple interest ?', additional_kwargs={}, response_metadata={}, id='046aef94-62e2-4b38-a398-84d3a57fba4d')]
INFO 2025-04-13 10:24:38,872 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 10:24:38,882 - Processing request of type CallToolRequest
INFO 2025-04-13 10:24:38,882 - Simple interest -> Principal: 1000.0, Rate: 3.75
INFO 2025-04-13 10:24:39,170 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 10:24:39,171 - [AIMessage(content='The simple interest for a principal of $1000 at an annual rate of 3.75% is $37.50.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T14:24:39.170273321Z', 'done': True, 'done_reason': 'stop', 'total_duration': 285605746, 'load_duration': 6872903, 'prompt_eval_count': 239, 'prompt_eval_duration': 46254681, 'eval_count': 32, 'eval_duration': 227943217, 'message': Message(role='assistant', content='The simple interest for a principal of $1000 at an annual rate of 3.75% is $37.50.', images=None, tool_calls=None)}, id='run-8bd6ce67-d04e-4320-a1e1-2fcc94811fac-0', usage_metadata={'input_tokens': 239, 'output_tokens': 32, 'total_tokens': 271}), ToolMessage(content='37.5', name='yearly_simple_interest', id='a7e69290-1162-41a7-bd05-08e4738e7a51', tool_call_id='eea9e5ab-d0a5-4092-9b80-9a7f7bfa9e11'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T14:24:38.879515025Z', 'done': True, 'done_reason': 'stop', 'total_duration': 469244684, 'load_duration': 6761794, 'prompt_eval_count': 193, 'prompt_eval_duration': 38995191, 'eval_count': 60, 'eval_duration': 422119871, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-f32cbb8e-2f7b-41b6-a144-f403fb30f956-0', tool_calls=[{'name': 'yearly_simple_interest', 'args': {'principal': 1000, 'rate': 3.75}, 'id': 'eea9e5ab-d0a5-4092-9b80-9a7f7bfa9e11', 'type': 'tool_call'}], usage_metadata={'input_tokens': 193, 'output_tokens': 60, 'total_tokens': 253}), HumanMessage(content='compute the simple interest for a principal of 1000 at rate 3.75 ?', additional_kwargs={}, response_metadata={}, id='2bf88431-a08e-4679-9d31-0c62bfbac9a5')]
INFO 2025-04-13 10:24:39,478 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 10:24:39,494 - Processing request of type CallToolRequest
INFO 2025-04-13 10:24:39,494 - Compound interest -> Principal: 1000.0, Rate: 4.25
INFO 2025-04-13 10:24:39,858 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 10:24:39,860 - [AIMessage(content='The compound interest for a principal of $1000 at a rate of 4.25% per year is approximately $1,042.50.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T14:24:39.858215452Z', 'done': True, 'done_reason': 'stop', 'total_duration': 362158794, 'load_duration': 6921843, 'prompt_eval_count': 241, 'prompt_eval_duration': 39011381, 'eval_count': 37, 'eval_duration': 312756614, 'message': Message(role='assistant', content='The compound interest for a principal of $1000 at a rate of 4.25% per year is approximately $1,042.50.', images=None, tool_calls=None)}, id='run-13a4f3b1-603e-44f1-963b-585b2b8fc0e5-0', usage_metadata={'input_tokens': 241, 'output_tokens': 37, 'total_tokens': 278}), ToolMessage(content='1042.5', name='yearly_compound_interest', id='6914a123-c9e0-4ea6-8070-7aa72b830c00', tool_call_id='597e2076-eb5c-4767-ad73-33b5d7810dbf'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T14:24:39.49171724Z', 'done': True, 'done_reason': 'stop', 'total_duration': 317826794, 'load_duration': 6408858, 'prompt_eval_count': 193, 'prompt_eval_duration': 37113360, 'eval_count': 39, 'eval_duration': 272645313, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-087af799-5faa-4b2d-9d99-480026fb63bc-0', tool_calls=[{'name': 'yearly_compound_interest', 'args': {'principal': 1000, 'rate': 4.25}, 'id': '597e2076-eb5c-4767-ad73-33b5d7810dbf', 'type': 'tool_call'}], usage_metadata={'input_tokens': 193, 'output_tokens': 39, 'total_tokens': 232}), HumanMessage(content='compute the compound interest for a principal of 1000 at rate 4.25 ?', additional_kwargs={}, response_metadata={}, id='81328b6c-5277-49e5-b9e6-da08da988a85')]



BINGO - it is evident from the above Output.2 that the LLM app was able to not only define what simple interest is, but also able to compute the simple interest and the compound interest using the tools exposed by the MCP server.

A typical Enterprise LLM agentic app invokes multiple MCP servers to perform a particular task. For our next example, the LLM host app will demonstrate how one can setup and use multiple tools.

The following is our second MCP Server code in Python that will invoke shell commands:



shell_mcp_server.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   12 April 2025
#

import subprocess

from mcp.server.fastmcp import FastMCP

import logging

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('shell_mcp_server')

mcp = FastMCP('ShellCommandExecutor')

# DISCLAIMER: This is purely for demonstration purposes and NOT to be used in production environment

@mcp.tool()
def execute_shell_command(command: str) -> str:
  """Tool to execute shell commands"""
  logger.info(f'Executing shell command: {command}')
  try:
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    if result.returncode != 0:
      return f'Error executing shell command - {command}'
    return result.stdout
  except subprocess.CalledProcessError as e:
    logger.error(e)

if __name__ == '__main__':
  logger.info(f'Starting the shell executor MCP server...')
  mcp.run(transport='stdio')



The following is our second MCP Host LLM app code in Python using multiple tools:



multi_mcp_client.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   12 April 2025
#

from dotenv import load_dotenv, find_dotenv
from langchain_ollama import ChatOllama
from  langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import asyncio
import logging
import os

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('multi_mcp_client')

load_dotenv(find_dotenv())

home_dir = os.getenv('HOME')
llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
ollama_model = os.getenv('OLLAMA_MODEL')
ollama_base_url = os.getenv('OLLAMA_BASE_URL')
py_project_dir = os.getenv('PY_PROJECT_DIR')

ollama_chat_llm = ChatOllama(base_url=ollama_base_url, model=ollama_model, temperature=llm_temperature)

async def main():
  async with MultiServerMCPClient() as client:
    await client.connect_to_server(
      'InterestCalculator',
      command='python',
      args=[home_dir + py_project_dir + 'interest_mcp_server.py'],
      transport='stdio',
    )

    await client.connect_to_server(
      'ShellCommandExecutor',
      command='python',
      args=[home_dir + py_project_dir + 'shell_mcp_server.py'],
      transport='stdio',
    )

    tools = client.get_tools()

    logger.info(f'Loaded Multiple MCP Tools -> {tools}')

    # Initialize a ReACT agent with multiple tools
    agent = create_react_agent(ollama_chat_llm, tools)

    # Case - 1 : Compound interest definition
    agent_response_1 = await agent.ainvoke(
      {'messages': 'explain the definition of compound interest'})
    logger.info(agent_response_1['messages'][::-1])

    # Case - 2 : Compound interest calculation
    agent_response_2 = await agent.ainvoke(
      {'messages': 'what is the compound interest for a principal of 1000 at rate 3.75 ?'})
    logger.info(agent_response_2['messages'][::-1])

    # Case - 3 : Execute a shell command
    agent_response_3 = await agent.ainvoke(
      {'messages': 'Execute the free shell command to find how much system memory'})
    logger.info(agent_response_3['messages'][::-1])

if __name__ == '__main__':
  asyncio.run(main())



To execute the above Python code, execute the following command in a terminal window:




$ python multi_mcp_client.py




The following would be the typical output:



Output.3
INFO 2025-04-13 12:09:03,259 - Starting the interest MCP server...
INFO 2025-04-13 12:09:03,265 - Processing request of type ListToolsRequest
INFO 2025-04-13 12:09:03,536 - Starting the shell executor MCP server...
INFO 2025-04-13 12:09:03,540 - Processing request of type ListToolsRequest
INFO 2025-04-13 12:09:03,541 - Loaded Multiple MCP Tools -> [StructuredTool(name='yearly_simple_interest', description='Tool to compute simple interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_simple_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x767fbd756160>), StructuredTool(name='yearly_compound_interest', description='Tool to compute compound interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_compound_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x767fbd756340>), StructuredTool(name='execute_shell_command', description='Tool to execute shell commands', args_schema={'properties': {'command': {'title': 'Command', 'type': 'string'}}, 'required': ['command'], 'title': 'execute_shell_commandArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x767fbd756f20>)]
INFO 2025-04-13 12:09:06,897 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 12:09:06,899 - [AIMessage(content="Compound interest is a type of interest calculated on the initial principal amount and also on any accumulated interest from previous periods. It's different from simple interest, which only considers the principal amount and the interest paid or earned during a single period. \n\nIn other words, with compound interest, your money grows at an increasing rate over time because it earns interest not just on the initial deposit but also on any previous interest accumulated. This results in a higher total value compared to simple interest for the same amount of principal and rate.\n\nFor example, if you invest $100 with an annual interest rate of 5% (simple interest) and leave it for one year, after one year, you would have $105 ($100 + $5). However, if you had invested the same amount at a 5% annual interest rate compounded annually, your money would grow to $107.20 ($100 * (1 + 0.05)^1) after one year. This is because the interest earned in the first year is added back to your principal for the second year, leading to a higher total amount.", additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T16:09:06.896491193Z', 'done': True, 'done_reason': 'stop', 'total_duration': 3346516305, 'load_duration': 1212696126, 'prompt_eval_count': 225, 'prompt_eval_duration': 246604191, 'eval_count': 247, 'eval_duration': 1885047710, 'message': Message(role='assistant', content="Compound interest is a type of interest calculated on the initial principal amount and also on any accumulated interest from previous periods. It's different from simple interest, which only considers the principal amount and the interest paid or earned during a single period. \n\nIn other words, with compound interest, your money grows at an increasing rate over time because it earns interest not just on the initial deposit but also on any previous interest accumulated. This results in a higher total value compared to simple interest for the same amount of principal and rate.\n\nFor example, if you invest $100 with an annual interest rate of 5% (simple interest) and leave it for one year, after one year, you would have $105 ($100 + $5). However, if you had invested the same amount at a 5% annual interest rate compounded annually, your money would grow to $107.20 ($100 * (1 + 0.05)^1) after one year. This is because the interest earned in the first year is added back to your principal for the second year, leading to a higher total amount.", images=None, tool_calls=None)}, id='run-3a71822d-690b-49f0-899d-d4b21980c94f-0', usage_metadata={'input_tokens': 225, 'output_tokens': 247, 'total_tokens': 472}), HumanMessage(content='explain the definition of compound interest', additional_kwargs={}, response_metadata={}, id='03a3e2e6-e77c-4f61-9edf-20bb26357e53')]
INFO 2025-04-13 12:09:07,182 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 12:09:07,193 - Processing request of type CallToolRequest
INFO 2025-04-13 12:09:07,193 - Compound interest -> Principal: 1000.0, Rate: 3.75
INFO 2025-04-13 12:09:07,531 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 12:09:07,533 - [AIMessage(content='The compound interest for a principal of 1000 at a rate of 3.75% per year is approximately $1,037.50.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T16:09:07.531146164Z', 'done': True, 'done_reason': 'stop', 'total_duration': 335663713, 'load_duration': 6423396, 'prompt_eval_count': 289, 'prompt_eval_duration': 39621454, 'eval_count': 37, 'eval_duration': 285564222, 'message': Message(role='assistant', content='The compound interest for a principal of 1000 at a rate of 3.75% per year is approximately $1,037.50.', images=None, tool_calls=None)}, id='run-be2948e7-7d6e-453a-9664-b6d8dde52047-0', usage_metadata={'input_tokens': 289, 'output_tokens': 37, 'total_tokens': 326}), ToolMessage(content='1037.5', name='yearly_compound_interest', id='c9efadd2-3c8c-40b0-be34-93af5aab986a', tool_call_id='b7ae46e6-8914-4960-b596-bb2bb0cce231'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T16:09:07.190388182Z', 'done': True, 'done_reason': 'stop', 'total_duration': 287410324, 'load_duration': 5683334, 'prompt_eval_count': 241, 'prompt_eval_duration': 40192209, 'eval_count': 35, 'eval_duration': 240304994, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-af8e8189-b525-4fc9-af51-6a3338e19ebd-0', tool_calls=[{'name': 'yearly_compound_interest', 'args': {'principal': 1000, 'rate': 3.75}, 'id': 'b7ae46e6-8914-4960-b596-bb2bb0cce231', 'type': 'tool_call'}], usage_metadata={'input_tokens': 241, 'output_tokens': 35, 'total_tokens': 276}), HumanMessage(content='what is the compound interest for a principal of 1000 at rate 3.75 ?', additional_kwargs={}, response_metadata={}, id='89096fbd-19af-4a16-9540-e035a9d4e183')]
INFO 2025-04-13 12:09:07,760 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 12:09:07,776 - Processing request of type CallToolRequest
INFO 2025-04-13 12:09:07,776 - Executing shell command: free -m
INFO 2025-04-13 12:09:08,391 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 12:09:08,393 - [AIMessage(content='The system has a total of 62 Gi memory, with 7.4 Gi currently in use and 35 Gi available for processes. Additionally, there is 138Mi of shared memory and 20Gi of buffered/cached memory. The swap space is unused at the moment, with 14Gi allocated but no usage.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-17T11:57:03.844036723Z', 'done': True, 'done_reason': 'stop', 'total_duration': 744242521, 'load_duration': 8122635, 'prompt_eval_count': 389, 'prompt_eval_duration': 11751427, 'eval_count': 76, 'eval_duration': 721895105, 'message': Message(role='assistant', content='The system has a total of 62 Gi memory, with 7.4 Gi currently in use and 35 Gi available for processes. Additionally, there is 138Mi of shared memory and 20Gi of buffered/cached memory. The swap space is unused at the moment, with 14Gi allocated but no usage.', images=None, tool_calls=None)}, id='run-0ed3e156-0e93-4436-aa29-6c814c43ad60-0', usage_metadata={'input_tokens': 389, 'output_tokens': 76, 'total_tokens': 465}), ToolMessage(content='               total        used        free      shared  buff/cache   available\nMem:            62Gi       7.4Gi        35Gi       138Mi        20Gi        55Gi\nSwap:           14Gi          0B        14Gi\n', name='execute_shell_command', id='dec53694-0e5d-434d-85eb-39cc5364f51c', tool_call_id='5a275018-b3ce-408d-aa5e-8ab6b19b980e'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-17T11:57:03.090458529Z', 'done': True, 'done_reason': 'stop', 'total_duration': 240456446, 'load_duration': 8643479, 'prompt_eval_count': 298, 'prompt_eval_duration': 9787648, 'eval_count': 23, 'eval_duration': 221516214, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-60cfb496-2063-4f0a-af34-7989c8c5586b-0', tool_calls=[{'name': 'execute_shell_command', 'args': {'command': 'free -h'}, 'id': '5a275018-b3ce-408d-aa5e-8ab6b19b980e', 'type': 'tool_call'}], usage_metadata={'input_tokens': 298, 'output_tokens': 23, 'total_tokens': 321}), HumanMessage(content='Execute the free shell command to find how much system memory', additional_kwargs={}, response_metadata={}, id='5bb00a6b-df5a-4e42-8f26-d4ec27743103')]



BOOM - it is evident from the above Output.3 that the LLM app was able to multiple tools exposed by the different MCP servers.

Until now we have used the stdio transport as the mode off communication between the MCP Client and the MCP Client. As indicated earlier, the other transport mode is the sse transport. In order to use this mode, we will need a web server with SSE enabled.

For this demonstration, we will leverage to the Starlette framework along with the uvicorn server.

The following is our MCP Server code in Python using the sse transport:



interest_mcp_server2.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   12 April 2025
#

import logging
import uvicorn

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.applications import Starlette

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('interest_mcp_server2')

mcp = FastMCP('InterestCalculator')

@mcp.tool()
def yearly_simple_interest(principal: float, rate:float) -> float:
  """Tool to compute simple interest rate for a year."""
  logger.info(f'Simple interest -> Principal: {principal}, Rate: {rate}')
  return principal * rate / 100.00

@mcp.tool()
def yearly_compound_interest(principal: float, rate:float) -> float:
  """Tool to compute compound interest rate for a year."""
  logger.info(f'Compound interest -> Principal: {principal}, Rate: {rate}')
  return principal * (1 + rate / 100.0)

if __name__ == "__main__":
  logger.info(f'Starting the interest calculator MCP server using SSE ...')

  async def handle_sse(request: Request):
    async with sse.connect_sse(
      request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
      await mcp._mcp_server.run(
        read_stream, write_stream, mcp._mcp_server.create_initialization_options()
      )

  sse = SseServerTransport('/messages/')

  app = Starlette(
    routes=[
      Route("/sse", endpoint=handle_sse),
      Mount("/messages/", app=sse.handle_post_message),
    ]
  )

  uvicorn.run(app, host='192.168.1.25', port=8000)



To execute the above Python code, execute the following command in a terminal window:




$ python interest_mcp_server2.py




The following would be the typical output:



Output.4
INFO 2025-04-13 14:02:02,761 - Starting the interest calculator MCP server using SSE ...
INFO:     Started server process [124909]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://192.168.1.25:8000 (Press CTRL+C to quit)



The following is our MCP Host LLM app code in Python, which invokes multiple tools, one of which is exposed as a network service:



multi_mcp_client2.py
#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   12 April 2025
#

from dotenv import load_dotenv, find_dotenv
from langchain_ollama import ChatOllama
from  langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import asyncio
import logging
import os

logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

logger = logging.getLogger('multi_mcp_client2')

load_dotenv(find_dotenv())

home_dir = os.getenv('HOME')
llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
ollama_model = os.getenv('OLLAMA_MODEL')
ollama_base_url = os.getenv('OLLAMA_BASE_URL')
py_project_dir = os.getenv('PY_PROJECT_DIR')
sse_base_url = os.getenv('SSE_BASE_URL')

ollama_chat_llm = ChatOllama(base_url=ollama_base_url, model=ollama_model, temperature=llm_temperature)

async def main():
  async with MultiServerMCPClient() as client:
    await client.connect_to_server(
      'InterestCalculator',
      url=sse_base_url,
      transport='sse',
    )

    await client.connect_to_server(
      'ShellCommandExecutor',
      command='python',
      args=[home_dir + py_project_dir + 'shell_mcp_server.py'],
      transport='stdio',
    )

    tools = client.get_tools()

    logger.info(f'Loaded Multiple MCP Tools -> {tools}')

    # Initialize a ReACT agent with multiple tools
    agent = create_react_agent(ollama_chat_llm, tools)

    # Case - 1 : Compound interest definition
    agent_response_1 = await agent.ainvoke(
      {'messages': 'explain the definition of compound interest'})
    logger.info(agent_response_1['messages'][::-1])

    # Case - 2 : Compound interest calculation
    agent_response_2 = await agent.ainvoke(
      {'messages': 'what is the compound interest for a principal of 1000 at rate 3.75 ?'})
    logger.info(agent_response_2['messages'][::-1])

    # Case - 3 : Execute a shell command
    agent_response_3 = await agent.ainvoke(
      {'messages': 'Execute the free shell command to find how much system memory'})
    logger.info(agent_response_3['messages'][::-1])

if __name__ == '__main__':
  asyncio.run(main())



To execute the above Python code, execute the following command in a terminal window:




$ python multi_mcp_client2.py




The following would be the typical output:



Output.5
INFO 2025-04-13 14:09:17,172 - Connecting to SSE endpoint: http://192.168.1.25:8000/sse
INFO 2025-04-13 14:09:17,194 - HTTP Request: GET http://192.168.1.25:8000/sse "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:17,195 - Received endpoint URL: http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7
INFO 2025-04-13 14:09:17,195 - Starting post writer with endpoint URL: http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7
INFO 2025-04-13 14:09:17,197 - HTTP Request: POST http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7 "HTTP/1.1 202 Accepted"
INFO 2025-04-13 14:09:17,198 - HTTP Request: POST http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7 "HTTP/1.1 202 Accepted"
INFO 2025-04-13 14:09:17,199 - HTTP Request: POST http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7 "HTTP/1.1 202 Accepted"
INFO 2025-04-13 14:09:17,472 - Starting the shell executor MCP server...
INFO 2025-04-13 14:09:17,477 - Processing request of type ListToolsRequest
INFO 2025-04-13 14:09:17,477 - Loaded Multiple MCP Tools -> [StructuredTool(name='yearly_simple_interest', description='Tool to compute simple interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_simple_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x72c72802a7a0>), StructuredTool(name='yearly_compound_interest', description='Tool to compute compound interest rate for a year.', args_schema={'properties': {'principal': {'title': 'Principal', 'type': 'number'}, 'rate': {'title': 'Rate', 'type': 'number'}}, 'required': ['principal', 'rate'], 'title': 'yearly_compound_interestArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x72c72802a840>), StructuredTool(name='execute_shell_command', description='Tool to execute shell commands', args_schema={'properties': {'command': {'title': 'Command', 'type': 'string'}}, 'required': ['command'], 'title': 'execute_shell_commandArguments', 'type': 'object'}, response_format='content_and_artifact', coroutine=.call_tool at 0x72c72802afc0>)]
INFO 2025-04-13 14:09:21,695 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:21,697 - [AIMessage(content="Compound interest is a type of interest calculated on the initial principal amount and also on any accumulated interest from previous periods. It's a powerful tool that can significantly increase the value of an investment over time, especially when compounded regularly. Here's how it works:\n\n1. **Simple Interest**: This is the simplest form of interest calculation where you only pay back the principal amount and no additional interest for each period. For example, if you invest $100 at a 5% annual interest rate (simple interest), after one year, you would have $105 ($100 + $5).\n\n2. **Compound Interest**: In this case, the interest is calculated on both the principal amount and any accumulated interest from previous periods. This means that for each compounding period, your total investment grows by a certain percentage (the annual rate of compounding) because some of your initial principal has already been added to the new principal.\n\nFor instance, if you have an investment of $100 with a 5% annual interest rate compounded annually, after one year, you would have:\n\n- Principal = $100\n- Interest from this period = $5 (since $100 * 5% = $5)\n- New Principal = $100 + $5 = $105\n\nAnd the interest for the next period would be calculated on the new principal of $105, which is $6.25 ($105 * 5%) because you've already earned $5 in the previous year. This process continues until the end of the compounding period.", additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T18:09:21.694022052Z', 'done': True, 'done_reason': 'stop', 'total_duration': 4206780120, 'load_duration': 1221121502, 'prompt_eval_count': 225, 'prompt_eval_duration': 229759310, 'eval_count': 350, 'eval_duration': 2754143527, 'message': Message(role='assistant', content="Compound interest is a type of interest calculated on the initial principal amount and also on any accumulated interest from previous periods. It's a powerful tool that can significantly increase the value of an investment over time, especially when compounded regularly. Here's how it works:\n\n1. **Simple Interest**: This is the simplest form of interest calculation where you only pay back the principal amount and no additional interest for each period. For example, if you invest $100 at a 5% annual interest rate (simple interest), after one year, you would have $105 ($100 + $5).\n\n2. **Compound Interest**: In this case, the interest is calculated on both the principal amount and any accumulated interest from previous periods. This means that for each compounding period, your total investment grows by a certain percentage (the annual rate of compounding) because some of your initial principal has already been added to the new principal.\n\nFor instance, if you have an investment of $100 with a 5% annual interest rate compounded annually, after one year, you would have:\n\n- Principal = $100\n- Interest from this period = $5 (since $100 * 5% = $5)\n- New Principal = $100 + $5 = $105\n\nAnd the interest for the next period would be calculated on the new principal of $105, which is $6.25 ($105 * 5%) because you've already earned $5 in the previous year. This process continues until the end of the compounding period.", images=None, tool_calls=None)}, id='run-3569b9ac-8cda-4196-b330-bbd315ecbaec-0', usage_metadata={'input_tokens': 225, 'output_tokens': 350, 'total_tokens': 575}), HumanMessage(content='explain the definition of compound interest', additional_kwargs={}, response_metadata={}, id='68e3e2da-7d30-4c25-9b6e-2d3cdc879d2f')]
INFO 2025-04-13 14:09:21,999 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:22,012 - HTTP Request: POST http://192.168.1.25:8000/messages/?session_id=9898861e27c04ee0b5e243e98216c9f7 "HTTP/1.1 202 Accepted"
INFO 2025-04-13 14:09:22,366 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:22,400 - [AIMessage(content='The compound interest for a principal of $1000 at a rate of 3.75% per year is approximately $1,037.50.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T18:09:22.365832725Z', 'done': True, 'done_reason': 'stop', 'total_duration': 350469941, 'load_duration': 8795119, 'prompt_eval_count': 289, 'prompt_eval_duration': 46233452, 'eval_count': 37, 'eval_duration': 290352383, 'message': Message(role='assistant', content='The compound interest for a principal of $1000 at a rate of 3.75% per year is approximately $1,037.50.', images=None, tool_calls=None)}, id='run-556cd53b-f38e-4549-af34-2fb333cd9b7f-0', usage_metadata={'input_tokens': 289, 'output_tokens': 37, 'total_tokens': 326}), ToolMessage(content='1037.5', name='yearly_compound_interest', id='fd0e7bec-a339-4bda-9bd6-981f59ab43a1', tool_call_id='abf08575-e66a-4b80-8b80-e042ea5156c3'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-13T18:09:22.008555615Z', 'done': True, 'done_reason': 'stop', 'total_duration': 309797162, 'load_duration': 4476504, 'prompt_eval_count': 241, 'prompt_eval_duration': 39846647, 'eval_count': 35, 'eval_duration': 264010946, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-a613074b-f9ea-4ae7-88fe-07e3718ef033-0', tool_calls=[{'name': 'yearly_compound_interest', 'args': {'principal': 1000, 'rate': 3.75}, 'id': 'abf08575-e66a-4b80-8b80-e042ea5156c3', 'type': 'tool_call'}], usage_metadata={'input_tokens': 241, 'output_tokens': 35, 'total_tokens': 276}), HumanMessage(content='what is the compound interest for a principal of 1000 at rate 3.75 ?', additional_kwargs={}, response_metadata={}, id='aef4e123-e2b7-4df6-ae88-b20f568b9f4a')]
INFO 2025-04-13 14:09:22,661 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:22,672 - Processing request of type CallToolRequest
INFO 2025-04-13 14:09:22,672 - Executing shell command: free -m
INFO 2025-04-13 14:09:23,169 - HTTP Request: POST http://192.168.1.25:11434/api/chat "HTTP/1.1 200 OK"
INFO 2025-04-13 14:09:23,171 - [AIMessage(content='The system memory is currently using 35 Gi out of the total 62 Gi available. The used memory includes 7.4 Gi in active use and 138Mi shared, with 20Gi in buff/cache and 55Gi available for further usage. Swap space is unused at the moment.', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-17T11:59:07.456996106Z', 'done': True, 'done_reason': 'stop', 'total_duration': 680005943, 'load_duration': 6665752, 'prompt_eval_count': 389, 'prompt_eval_duration': 10666800, 'eval_count': 71, 'eval_duration': 659332066, 'message': Message(role='assistant', content='The system memory is currently using 35 Gi out of the total 62 Gi available. The used memory includes 7.4 Gi in active use and 138Mi shared, with 20Gi in buff/cache and 55Gi available for further usage. Swap space is unused at the moment.', images=None, tool_calls=None)}, id='run-3766bd18-d071-4305-ab3b-7723996d8897-0', usage_metadata={'input_tokens': 389, 'output_tokens': 71, 'total_tokens': 460}), ToolMessage(content='               total        used        free      shared  buff/cache   available\nMem:            62Gi       7.4Gi        35Gi       138Mi        20Gi        55Gi\nSwap:           14Gi          0B        14Gi\n', name='execute_shell_command', id='64bab3ed-9889-4b01-8d18-f99a084de106', tool_call_id='1547a960-47e5-4fae-9d00-7849253a2e9a'), AIMessage(content='', additional_kwargs={}, response_metadata={'model': 'granite3.3:2b', 'created_at': '2025-04-17T11:59:06.770086604Z', 'done': True, 'done_reason': 'stop', 'total_duration': 232035188, 'load_duration': 9263074, 'prompt_eval_count': 298, 'prompt_eval_duration': 8805239, 'eval_count': 23, 'eval_duration': 213328962, 'message': Message(role='assistant', content='', images=None, tool_calls=None)}, id='run-137b8d2b-03b1-45f9-9448-4bc095eaecb8-0', tool_calls=[{'name': 'execute_shell_command', 'args': {'command': 'free -h'}, 'id': '1547a960-47e5-4fae-9d00-7849253a2e9a', 'type': 'tool_call'}], usage_metadata={'input_tokens': 298, 'output_tokens': 23, 'total_tokens': 321}), HumanMessage(content='Execute the free shell command to find how much system memory', additional_kwargs={}, response_metadata={}, id='9fd86a5e-ef7b-4a93-8054-736881201011')]



WALLA - it is evident from the above Output.5 that the LLM app was able to sucessfully able to communicate with the MCP server using both transport modes !!!

With this, we conclude the various hands-on demonstrations on using the MCP framework for building and deploying agentic LLM apps !!!




References

Model Context Protocol Documentation



© PolarSPARC
