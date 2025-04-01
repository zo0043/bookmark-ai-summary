Title: 🌟《从一到二：基于Trae的多智能体合作Prompt自动生成迭代指南》#VibeCoding #Trae

URL Source: https://juejin.cn/post/7488013596523118601

Published Time: 2025-04-01T08:28:53+00:00

Markdown Content:
背景
--

Multi-agent结合MCP已经成为非常明确的新一轮发展趋势，但日常工作发现，很多刚接触的小伙伴还在受“如何编写一个能完成自己预期需求的prompt”这一需求而感到困扰。那么结合Multi-agent，我们不妨设计和实现一个多智能体合作来自动化完成prompt自动迭代生成的系统，Let's do it!

框架和LLM部署方式选型
------------

不同于我们之前采用[langroid](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Flangroid%2Flangroid "https://github.com/langroid/langroid")的选型，本期我们将采用langchain，这里做出变更的原因主要在于langchain似乎大家使用的更为广泛，但在易用性上本文仍然推荐langroid，感兴趣的小伙伴可以参看我们前一系列中的内容。

*   Multi-Agent: [langchain（python）](https://link.juejin.cn/?target=https%3A%2F%2Fpython.langchain.com%2Fdocs%2Fintroduction%2F "https://python.langchain.com/docs/introduction/")
    
*   LLM部署（同前一系列）：
    
    *   需所选定的Multi-agent框架支持，理论上流行的框架目前都支持类openai的接口方式来接入远程大模型，或者是本地部署的LLM模型，甚至是类似于coze这种直接选取即可。
    *   考虑到本地部署模型无合规风险，query无额外限制（如速率限制），且免费，本项目以[Ollama](https://link.juejin.cn/?target=https%3A%2F%2Follama.com%2F "https://ollama.com/")部署本地模型为例，进行展示。
    *   [ollma使用](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Follama%2Follama%3Ftab%3Dreadme-ov-file "https://github.com/ollama/ollama?tab=readme-ov-file") & [ollma提供的模型列表](https://link.juejin.cn/?target=https%3A%2F%2Follama.com%2Flibrary "https://ollama.com/library")
    *   ![Image 1](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4d5705c99dae4b56aec0dd5b5f0d1fbb~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5p2O5biFMTQ5Njk4MjQxOTE2Nw==:q75.awebp?rk3s=f64ab15b&x-expires=1744101205&x-signature=P20fAu2JEwbJxy1Ptk3FpWsRa5s%3D)

方案设计
----

暂时无法在飞书文档外展示此内容

###### workflow

*   用户需求
    
    *   包括用户想要设计一个什么样的prompt
    *   针对这个想设计的prompt，用户需提供一个预期输入和相应的预期输出
*   Main Agent
    
    *   根据用户需求和预期输入输出，生成初始Prompt
    *   根据反馈迭代Prompt，当超出最大迭代次数或当前调整后的prompt已达成需求，则输出最终prompt
*   Validator Agent
    
    *   读取prompt并加载，以预期输入为输入，得到实际输出，对比预期输出，输出Output差异
*   Analysis Agent
    
    *   分析Output差异，向Main Agent提出针对性的反馈调整意见

从头开始
----

![Image 2](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e647eb35e9b9494395c99a73f3bc44a5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5p2O5biFMTQ5Njk4MjQxOTE2Nw==:q75.awebp?rk3s=f64ab15b&x-expires=1744101205&x-signature=32%2FOxf8OI0as1VZscn4M4XfWm2M%3D)

###### 环境准备

1.  部署本地LLM：
    
    1.  下载安装[ollama](https://link.juejin.cn/?target=https%3A%2F%2Follama.com%2F "https://ollama.com/")
    2.  ![Image 3](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/9f27a9e363d84a6099b658a348d8c163~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5p2O5biFMTQ5Njk4MjQxOTE2Nw==:q75.awebp?rk3s=f64ab15b&x-expires=1744101205&x-signature=fDizfETmLh3izvqIG8oaUEO%2FZk4%3D)
    3.  pull下来`deepseek-r1:14b`模型，你可以[按需选择](https://link.juejin.cn/?target=https%3A%2F%2Follama.com%2Flibrary "https://ollama.com/library")
    4.  ```
          ollama pull deepseek-r1:14b
        ```
        
    
2.  安装langchain，langgraph等相关依赖
    

```
pip3 install -r requirements.txt
```

requirements.txt为当前项目依赖的python lib信息，如下：

```
langchain>=0.1.0
langgraph>=0.0.10
langchain-community>=0.0.10
langchain-core>=0.1.0
typing-extensions>=4.8.0
typing>=3.7.4
pydantic>=2.5.0
ollama>=0.1.5
python-dotenv>=1.0.0
```

###### Coding

IDE：[Trae](https://www.trae.ai/ "https://www.trae.ai/") 或 [Trae CN](https://www.trae.com.cn/ "https://www.trae.com.cn/")

1.**创建工作流**：首先让我们按照上述方案设计里的workflow来创建一个工作流

```
def create_workflow() -> Graph:
    workflow = Graph()

    # 定义工作流节点
    workflow.add_node("generate_prompt", generate_prompt)
    workflow.add_node("validate_prompt", validate_prompt)
    workflow.add_node("generate_feedback", generate_feedback)
    workflow.add_node("check_completion", check_completion)

    # 定义工作流边和条件
    workflow.add_edge("generate_prompt", "validate_prompt")
    workflow.add_edge("validate_prompt", "check_completion")
    workflow.add_conditional_edges(
        "check_completion",
        lambda x: x[0],
        {
            "continue": "generate_feedback", 
            "end": END
        }
    )
    workflow.add_edge("generate_feedback", "generate_prompt")

    # 设置工作流入口
    workflow.set_entry_point("generate_prompt")

    return workflow.compile()
```

2.**实现工作流中的关键节点**：

*   generate\_prompt(对应MainAgent)：

```
def generate_prompt(state: WorkflowState) -> WorkflowState:
    print("\n🎯 进入生成提示词阶段...")
    main_agent = MainAgent()
    if len(state["current_prompt"]) == 0:
        # 将所有示例传递给主智能体
        state["current_prompt"] = main_agent.generate_initial_prompt(
            state["user_goal"],
            state["examples"]
        )
    else:
        state["current_prompt"] = main_agent.optimize_prompt(
            state["feedback"],
            state["current_prompt"]
        )
    return state
```

*   validate\_prompt（对应validatorAgent）：

```
def validate_prompt(state: WorkflowState) -> WorkflowState:
    print("\n🔍 进入验证提示词阶段...")
    validator = ValidatorAgent()
    validation_result = validator.validate_output(state["current_prompt"], state["examples"])
    
    # 确保validation_result包含is_acceptable字段
    if isinstance(validation_result, dict):
        validation_result.setdefault("is_acceptable", False)
    else:
        validation_result = {"is_acceptable": False, "individual_results": [], "overall_score": 0.0}
    
    state["validation_result"] = validation_result
    return state
```

*   generate\_feedback（对应AnalysisAgent）：

```
def generate_feedback(state: WorkflowState) -> WorkflowState:
    print("\n💭 进入生成反馈阶段...")
    feedback_agent = FeedbackAgent()
    
    # 处理check_completion返回的元组状态
    if isinstance(state, tuple):
        _, state = state
    
    # 确保state是字典类型并包含所有必需键
    if not isinstance(state, dict) or not all(key in state for key in ["current_prompt", "validation_result", "feedback", "user_goal", "examples", "iteration_count", "max_retries", "is_complete"]):
        print(f"警告：状态对象不完整或不是字典类型，当前状态内容为: {str(state)}")
        if hasattr(state, '__dict__'):
            state = vars(state)
        else:
            state = {
                "feedback": getattr(state, 'feedback', ""), 
                "current_prompt": getattr(state, 'current_prompt', ""), 
                "validation_result": getattr(state, 'validation_result', {}), 
                "user_goal": getattr(state, 'user_goal', ""), 
                "examples": getattr(state, 'examples', []), 
                "iteration_count": getattr(state, 'iteration_count', 0), 
                "max_retries": getattr(state, 'max_retries', 3), 
                "is_complete": getattr(state, 'is_complete', False)
            }
        
        # 确保所有必需键都存在
        for key in ["current_prompt", "validation_result", "feedback", "user_goal", "examples", "iteration_count", "max_retries", "is_complete"]:
            if key not in state:
                state[key] = "" if key in ["current_prompt", "feedback", "user_goal"] else ([] if key == "examples" else ({} if key == "validation_result" else (0 if key == "iteration_count" else (3 if key == "max_retries" else False))))
    
    try:
        # 检查必要的键是否存在
        if "current_prompt" not in state or "validation_result" not in state:
            print(f"错误：状态对象缺少必要的键")
            state["feedback"] = ""
            return state
            
        # 检查是否有差异
        has_differences = any(
            len(result.get('analysis_result', {}).get('differences', [])) > 0
            for result in state["validation_result"].get("individual_results", [])
        )
        
        feedback = feedback_agent.generate_feedback(
            state["current_prompt"],
            state["validation_result"]
        )
            
        if feedback == "NO_DIFFERENCES":
            state["validation_result"]["is_acceptable"] = True
            state["is_complete"] = True
            return state
        
        state["feedback"] = feedback
    except Exception as e:
        print(f"错误：生成反馈时发生异常 - {str(e)}")
        state["feedback"] = ""
    return state
```

*   check\_completion(用来检查迭代后的prompt是不是ok，或者超过最大迭代次数了)：

```
def check_completion(state: WorkflowState) -> tuple[str, WorkflowState]:
    print("\n✨ 进入完成检查阶段...")
    state["iteration_count"] += 1
    
    # 检查验证结果是否为空或无效
    if not state.get("validation_result") or not isinstance(state["validation_result"], dict):
        print("警告：无效的验证结果")
        return ("continue", state)
    
    # 检查是否有差异
    has_differences = any(
        len(result.get('analysis_result', {}).get('differences', [])) > 0
        for result in state["validation_result"].get("individual_results", [])
    )
    
    if state["validation_result"]["is_acceptable"] and not has_differences:
        state["is_complete"] = True
        return ("end", state)
    
    if state["iteration_count"] >= state["max_retries"]:
        state["is_complete"] = True
        return ("end", state)
    
    return ("continue", state)
```

3.实现关键Agent处理逻辑：

*   Main Agent：

```
from langchain.agents import AgentExecutor, BaseSingleActionAgent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from typing import Dict, List, Any, Optional
from langchain.schema import AgentAction

class MainAgent(BaseSingleActionAgent):
    llm: ChatOllama = None
    initial_template: str = None
    optimization_template: str = None
    prompt_template: Optional[ChatPromptTemplate] = None
    iteration_history: List[Dict[str, Any]] = None

    def __init__(self):
        super().__init__()
        # 推荐换个小一点size参数量的模型，实测下来32G内存的mbp，跑起来还是卡
        self.llm = ChatOllama(model='gemma3:27b')
        self.iteration_history = []
        self.prompt_template = None  # 将在具体方法中根据需要选择使用哪个模板
        self.initial_template = """您是一个专业的提示词工程师，请严格按照以下要求生成system prompt：
            1. 目标分析：
               - 深入分析用户目标：{user_goal}
               - 识别关键需求和约束条件
               - 确保生成的prompt直接服务于目标
               - 考虑目标的边界场景和异常情况
               - 评估目标的可扩展性和通用性
            
            2. 语义分析：
               - 确保prompt语义完整性和清晰度
               - 分析上下文关联性和依赖关系
               - 识别关键概念和术语
               - 考虑领域特定的专业术语和最佳实践
               - 确保指令的逻辑性和连贯性
            
            3. 输入输出示例处理：
               - 深入分析示例输入：{example_input}
               - 分析期望输出：{example_output}
               - 提取输入输出的关键特征和模式
               - 识别输入输出的边界条件和特殊情况
               - 确保prompt能够处理类似的输入场景并生成符合预期的输出格式
            
            4. 质量标准：
               - 确保prompt简洁明确系统且结构化，避免冗余
               - 使用精确的指令和约束条件
               - 保持一致的语言风格和格式
               - 确保输出格式与示例输出保持一致
               - 考虑prompt的可测试性和可维护性
               - 评估prompt的鲁棒性和容错性
            
            请基于以上要求，直接输出一个专业、全面且高质量的system prompt，不要包含任何解释性内容或分析过程。
            注意：生成的prompt应当具备良好的扩展性、鲁棒性和一致性，能够处理各种边界场景和异常情况。"""
            
        self.optimization_template = """您是一个专业的提示词工程师，请严格按照以下要求优化system prompt：
            当前Prompt：
            {example_input}            

            针对当前Prompt的反馈：
            {feedback}
            
            请你按照如下要求分析反馈，优化当前Prompt。
            1. 当前Prompt分析：
               - 深入分析当前prompt
               - 识别现有prompt的优点和不足
               - 评估prompt的结构和组织方式
               - 检查prompt的语义完整性和清晰度
            
            2. 反馈分析：
               - 仔细分析优化反馈
               - 识别需要改进的关键点
               - 确定优化的优先级和方向
               - 考虑反馈的合理性和可行性
            
            3. 优化策略：
               - 保持prompt的核心功能和优点
               - 针对性地解决反馈中提出的问题
               - 确保优化后的prompt更加专业和高效
               - 增强prompt的鲁棒性和适应性
            
            4. 质量保证：
               - 确保优化后的prompt结构清晰、逻辑严密
               - 保持语言风格的一致性和专业性
               - 验证优化是否解决了原有问题
               - 评估优化后的prompt是否更易于使用和维护
            
            请基于以上要求，直接输出一个经过优化的、更高质量的system prompt，不要包含任何解释性内容或分析过程。
            注意：优化后的prompt应当保持原有的优点，同时显著改进已识别的问题。"""
            
        self.prompt_template = None  # 将在具体方法中根据需要选择使用哪个模板
        
    @property
    def input_keys(self):
        return ["user_goal", "example_input", "example_output", "feedback"]

    @property
    def tool_run_logging_kwargs(self) -> Dict[str, Any]:
        return {"handle_tool_error": True}

    def plan(self, inputs: Dict[str, str], intermediate_steps: List = None) -> List[Dict[str, Any]]:
        return self.aplan(inputs, intermediate_steps)

    def generate_initial_prompt(self, user_goal: str, examples: List[Dict[str, str]]) -> str:
        """生成初始的system prompt"""
        print("\n🎯 正在生成初始提示词...")
        # 格式化所有示例
        formatted_examples = []
        for i, example in enumerate(examples, 1):
            formatted_examples.append(f"示例{i}：\n输入：{example['input']}\n预期输出：{example['expected_output']}")
        
        examples_text = "\n\n".join(formatted_examples)
        
        self.prompt_template = ChatPromptTemplate.from_template(self.initial_template)
        messages = self.prompt_template.format(
            user_goal=user_goal,
            example_input=examples_text,
            example_output=""  # 不再单独使用example_output
        )
        response = self.llm.invoke(messages)
        return response.content.strip()

    def aplan(self, inputs: Dict[str, str], intermediate_steps: List = None) -> List[Dict[str, Any]]:
        messages = self.prompt_template.format(
            user_goal=inputs["user_goal"],
            example_input=inputs["example_input"],
            example_output=inputs["example_output"],
            feedback=inputs["feedback"]
        )
        response = self.llm.invoke(messages)
        return [AgentAction(
            tool="prompt_optimization",
            tool_input={"optimized_prompt": response.content},
            log=f"Iteration {len(self.iteration_history)+1}"
        )]

    def optimize_prompt(self, feedback: str, current_prompt: str) -> str:
        """优化当前的system prompt"""
        print("\n✨ 正在根据反馈优化提示词...")
        self.prompt_template = ChatPromptTemplate.from_template(self.optimization_template)
        messages = self.prompt_template.format(
            example_input=current_prompt,
            feedback=feedback
        )
        response = self.llm.invoke(messages)
        return response.content.strip()
```

*   Validator agent：

```
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict
from analysis_agent import AnalysisAgent

class ValidatorAgent:
    def __init__(self):
        pass

    def validate_output(self, system_prompt: str, examples: list) -> Dict:
        """调用模型验证多个示例输出并计算差异"""
        print("\n🔄 正在验证模型输出...")
        chat = ChatOllama(model='gemma3:27b', temperature=0.2)
        
        all_results = []
        for example in examples:            
            print("📌 验证-输入内容：")
            print(example['input'])            
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=example['input'])
            ]
            response = chat.invoke(messages)
            
            actual_output = response.content.strip()            
            print("\n🔍 输出对比：")
            print(f"预期输出: {example['expected_output']}")
            print(f"实际输出: {actual_output}")
            
            # 调用分析智能体分析差异
            analysis = AnalysisAgent().analyze_diff([{
                'actual_output': actual_output,
                'expected_output': example['expected_output']
            }])
            
            all_results.append({
                'input': example['input'],
                'actual_output': actual_output,
                'expected_output': example['expected_output'],
                'analysis_result': analysis
            })
        
        # 计算总体评分（基于差异数量和质量）
        total_differences = sum(
            len(result['analysis_result']['differences'])
            for result in all_results
        )
        
        # 如果没有差异，评分为1；否则根据差异数量计算（差异越多分数越低）
        overall_score = 1.0 if total_differences == 0 else 1.0 / (1 + total_differences)
        
        # 判断是否可接受（评分大于0.7视为可接受）
        is_acceptable = overall_score > 0.7
        
        return {
            'is_acceptable': is_acceptable,
            'individual_results': all_results,
            'overall_score': overall_score
        }
```

*   Analysis agent:(上述validator agent主要调用analysis agent来识别差异)

```
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models.ollama import ChatOllama
from typing import Dict

class AnalysisAgent:
    llm: ChatOllama = None
    
    def __init__(self):
        self.llm = ChatOllama(model='deepseek-r1:14b')
        
    def analyze_diff(self, diff_reports: list) -> Dict:
        """使用结构化prompt进行差异分析"""
        print("\n📊 正在分析输出差异...")
        system_prompt = """您是一个专业的输出差异分析专家。请分析模型实际输出和预期输出的差异，重点关注以下维度：

        1. 内容差异：
           - 预期输出中存在但实际输出缺失的内容
           - 实际输出中出现但预期输出没有的内容
           - 内容的语义一致性和准确性
           - 关键信息的完整性和正确性

        2. 格式差异：
           - 输出格式是否符合预期（如JSON格式、列表格式等）
           - 输出结构是否一致
           - 格式规范性和标准化程度

        请直接指出具体的差异点，每个差异标注类型（内容缺失/内容多余/格式不一致/语义偏差），不要包含任何解释性内容、分析过程或一致的点。
        如果没有差异则输出:"无任何差异"。"""
        
        all_differences = []
        for i, diff_report in enumerate(diff_reports, 1):
            print(f"\n🔍 分析示例 {i}：")
            
            # 验证输入格式
            if not isinstance(diff_report, dict) or 'actual_output' not in diff_report or 'expected_output' not in diff_report:
                print(f"警告：示例 {i} 的差异报告格式不正确，应为包含actual_output和expected_output的字典")
                continue
                
            print("📌 差异报告内容：")
            print(f"实际输出: {diff_report['actual_output']}")
            print(f"预期输出: {diff_report['expected_output']}")
            
            diff_content = f"实际输出: {diff_report['actual_output']}\n预期输出: {diff_report['expected_output']}"
            
            result = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f'\n{diff_content}')
            ])
            
            print("\n🔍 分析结果：")
            print(result.content)
            
            if result and hasattr(result, 'content') and result.content:
                all_differences.append(result.content)
            
        return {
            'analysis_text': '\n'.join(all_differences) if all_differences else '没有发现有效差异',
            'differences': all_differences
        }
```

*   Feedback agent：

```
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate

class FeedbackAgent:
    optimization_history: list = None
    llm: ChatOllama = None
    
    def __init__(self):
        self.optimization_history = []
        self.llm = ChatOllama(model='deepseek-r1:14b')

    def generate_feedback(self, current_prompt: str, validation_result: Dict) -> str:
        """基于分析结果生成优化建议"""
        print("\n🔍 正在分析验证结果并生成优化建议...")
        
        # 添加类型检查和安全访问逻辑
        if not isinstance(validation_result, dict) or 'individual_results' not in validation_result:
            print("错误：无效的验证结果格式")
            return ""
            
        # 检查是否有差异
        has_differences = any(
            len(result.get('analysis_result', {}).get('differences', [])) > 0
            for result in validation_result['individual_results']
        )
        
        if not has_differences:
            print("✅ 无任何差异，返回特定字符串")
            return "NO_DIFFERENCES"
            
        # 生成每个示例的差异摘要
        example_summaries = []
        for i, result in enumerate(validation_result['individual_results']):
            if not isinstance(result, dict) or 'analysis_result' not in result:
                continue
                
            analysis_result = result.get('analysis_result', {})
            differences = analysis_result.get('differences', [])
            if differences:
                print(f"\n📌 示例 {i+1} 差异详情：")
                for diff in differences:
                    if isinstance(diff, str):
                        print(f"- {diff}")
                    elif isinstance(diff, dict):
                        print(f"- {diff.get('description', '')}（类型：{diff.get('type', '')}）")
                
                example_summaries.append(f"示例 {i+1} 分析：\n" + 
                    "\n".join([f"- {diff}" if isinstance(diff, str) else 
                              f"- {diff['description']}（类型：{diff['type']}）" 
                              for diff in differences])
                )
        
        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content="""您是一个提示词优化专家，请根据以下维度深入分析并生成专业的优化建议：
            1. 语义分析：
               - 当前prompt的语义完整性和清晰度
               - 上下文关联性和依赖关系
               - 关键概念和术语的准确性
               - 指令的逻辑性和连贯性
            
            2. 质量评估：
               - 验证结果中的关键差异点分析
               - prompt的可扩展性和通用性
               - 边界场景和异常情况的处理能力
               - prompt的鲁棒性和容错性
               - 输出的一致性和可预测性
            
            3. 改进建议：
               - 具体的优化方向和修改建议
               - 如何提高prompt的专业性和全面性
               - 如何增强prompt的可测试性和可维护性
               - 如何优化prompt的性能和效率
            
            请基于以上维度，直接提供具体的优化建议，不要包含任何解释性内容或分析过程。
            特别注意：请综合考虑所有示例的验证结果，找出共性问题和特殊情况。"""),
            HumanMessage(content=f"""当前系统提示为：\n{current_prompt}

            验证分析结果：
            1. 示例分析：
            {chr(10).join(example_summaries) if example_summaries else '无差异'}
            """)
        ])
        
        chain = prompt_template | ChatOllama(model='deepseek-r1:14b', temperature=0.5)
        response = chain.invoke({})
        
        print("\n💡 优化建议：")
        print(response.content)
        
        # 将优化建议添加到历史记录
        self.optimization_history.append({
            'prompt': current_prompt,
            'feedback': response.content,
            'validation_result': validation_result
        })
        
        return response.content.strip()
```

4.设计main函数入口，接收用户诉求和预期输入输出，启动整个多agent合作的workflow：

```
from workflow import run_workflow

def collect_examples():
    examples = []
    while True:
        example_input = input("\n请输入示例输入（输入'q'结束）：")
        if example_input.lower() == 'q':
            break
        example_output = input("请输入期望输出：")
        examples.append({
            "input": example_input,
            "expected_output": example_output
        })
        
        more = input("\n是否继续添加示例？(y/n)：")
        if more.lower() != 'y':
            break
    return examples

def main():
    print("\n🚀 启动智能提示词优化系统...")
    user_goal = input("请输入您的目标描述：")
    
    print("\n📝 开始收集示例...")
    examples = collect_examples()
    
    if not examples:
        print("\n⚠️ 未提供任何示例，程序退出")
        return
    
    print("\n⚙️ 开始执行优化工作流...")
    final_state = run_workflow(user_goal, examples)
    
    print(f"\n=== 执行了 {final_state['iteration_count']} 次迭代 ===")
    
    if final_state['validation_result'].get('is_acceptable', False):
        print("\n✅ 验证通过，达到可接受标准")
    else:
        print("\n⛔ 达到最大迭代次数仍未通过验证")
    
    print("\n🎉 最终优化结果：")
    print(final_state['current_prompt'])

if __name__ == "__main__":
    main()
```

让我们来看一下效果
---------

感觉还行~小伙伴们可以试试~

![Image 4](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/18cd31b1aac644f5b1bccde6858f4434~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5p2O5biFMTQ5Njk4MjQxOTE2Nw==:q75.awebp?rk3s=f64ab15b&x-expires=1744101205&x-signature=7ldwP%2F4wFILXiPtMWYEQ2wrHa40%3D)

结语
--

配合上MCP/Function Calling以及RAG，大有可为哦~冲!冲!冲!

![Image 5](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/803747f904ac4d94815af9ce41208857~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5p2O5biFMTQ5Njk4MjQxOTE2Nw==:q75.awebp?rk3s=f64ab15b&x-expires=1744101205&x-signature=wcM4%2FNgI5Bvhyye7%2BnvkOfDiABw%3D)

~喜欢的话，请给个点赞三连哦~(づ￣ 3￣)づ
