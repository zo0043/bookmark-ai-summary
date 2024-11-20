Title: 打包起来！把Agent接入GraphRAG！装进MAS中！加餐系列day7

URL Source: https://mp.weixin.qq.com/s?__biz=MzU4NDk0MDAwMw==&mid=2247486982&idx=1&sn=ccfb472bc6cc7479a6c86e9a1ce1e37e&chksm=fd936e8acae4e79cafa73196629a192d31a79d75863eb825154a4fe643fbdce69529981ee4ac&cur_album_id=3605740024773459977&scene=189

Markdown Content:
打包起来！把Agent接入GraphRAG！装进MAS中！加餐系列day7
Original 一意AI 一意AI增效家
 2024年11月13日 16:37

hi~

正在打卡，知识图谱系列的朋友，就知道！

把整个技术栈拆开+研究后，一定要懂重新组装！

组装回来那一刻！


你，完全手上！

上一篇，雄哥在Agent角度！把RAG作为一种子反馈，给Agent做服务！

他会知道何时调用GraphRAG，何时调用其他数据库！(理论支持任何开放产品)

这是一个完整的GraphRAG-Agent，但，孤掌难鸣！

复杂任务中，需要多Agent才能完成！

这就，需要编排！我们要在多智能体系统的角度，把他接入到MAS中！

今天，雄哥以上做的所有工作，把Agent产品化，做成一个API接口，最后，把他接入前端，上线！为用户提供服务！或接入MAS中！


整个系列，从数据处理开始，导入知识图谱，然后用它做GraphRAG！再到接入Agent，加餐系列是这样的(可直接点击跳转)：

day1：数据处理！把数据，转为知识图谱标准数据！

day2：构建知识图谱！把数据存到Neo4J中！

day3：企业批量创建！工程化批量处理知识数据！

day4：RAG学习合集！深入浅出学langchain核心！

day5：GraphRAG融合！增强RAG，做kg+rag应用！

day6：Agent接入GraphRAG！让它成为Agent决策工具！

day7：将Agent打包成后端服务！微调让他服务！【本篇】

day8：手把手构建Agent+GraphRAG的产品，提供用户！

整个加餐系列的内容，前后延展！非常丰富！从0-1把GraphRAG拆开，然后重新组装！

人的专注力只有10分钟，那！话不多说！

① 如何打包Agent？让他成为多智能体系统中一员？

② 实践环境搭建及底层技术有哪些？

③ 跑起来！边跑，边聊代码细节！ 

加餐系列内容，所有会员均可打卡！直接在知识星球获取代码！

朋友！你一定要动起手来跑！


AI发展飞快！只有动手了，才知道里面会遇到什么问题，才能知道，底层原理是什么！

识别下方二维码加入！

同时！这个系列也是知识图谱课程的补充和延展，此系列持续加餐！

说到这！一定要去知识图谱课程打卡！价值非常高！


市面上找不到的宝藏，代号“灵丹”！

这是雄哥主导的课程，不计成本做服务！

内容以视频+代码+技术支撑+高质量加餐！

报名在末尾联系工程师-小胖！更多介绍，看这！

“灵丹”-知识图谱+RAG项目官方wiki





第一部分：如何打包Agent？让他成为多智能体系统中一员？

多智能体系统(Multi-Agent System)，具有多并发+多线程特点！

由多个Agent及关键组件组成，就像一个井然有序的公司，各司其职！

雄哥之前已经分享过太多，默认你学过！点击↓


【首页】生产级AI多智能体系统MAS学习指南


不再做普及！


但，像把一个个的Agent，接入MAS，不简单！


这是一意研究多智能体系统时的发现与经验，市面上，没资料！


整个系统，定位生产！完成接入，核心6步！

前3步在Agent内部做，后3步在MAS中做！


序号	步骤	目标
1	定义Agent行为和目标	设定Agent的角色、目标和行为模式
2	抽象Agent接口	定义标准接口以共享基础功能和方法
3	实现感知-决策-行动的循环	构建感知、决策和行动的循环
4	设计Agent通信机制	建立消息传递和通信协议
5	管理环境和资源共享	实现共享环境中的状态同步和权限控制
6	实现多Agent并发	使用多线程或中间件支持并发运行

接下来，跟着雄哥，延展前三步，Agent内部该做的！

为什么后三个！在MAS内部的不讲？


不是今天重点，今天，是把已做好的Agent，做接入！




1.1 定义Agent行为和目标


任务目标：设定Agent的角色、目标和行为模式

在创建Agent之前，要明确其角色、行为和目标。确定其在系统中的职责、对环境的感知能力、决策策略和行为方式

因为在MAS系统中

不同角色、执行权限、行为标准、任务目标.....


完全不同！

我们要在顶层，定义Agent的角色和类型，他是谁，以什么标准干什么活


常见的Agent，有三类：

#A 反应式Agent

#B 基于模型的Agent

#C 基于类Q-learning的Agent

大部分的是基于模型来做的，往后，我们也会基于这三者，分别做实践！

类型	定义	特点
反应式Agent	直接根据环境作出反应，不依赖内部状态	简单任务，响应迅速但行为受限
基于模型的Agent	基于环境的内部模型进行决策，能够预测下一步状态	长期计划能力，适合复杂任务场景
基于学习的Agent	通过与环境交互学习和优化决策，适合动态环境	适应性强，可在环境变化中逐步优化行为

篇幅有限，雄哥不准备延展，再往里，整篇太拖沓！

后面Agent专题课程时，雄哥会往里底层一步步延展，包括代码！


一定要关注雄哥，先上部分：


反应式Agent

class ReactiveAgent:
    def __init__(self, name):
        self.name = name


    def perceive(self, environment):
        # 获取环境的当前状态（简单感知，如探测到障碍物或目标）
        return environment.get_status()


    def act(self, perception):
        # 依据感知的状态执行行动
        if perception == "obstacle":
            print(f"{self.name} moves around the obstacle.")
        elif perception == "goal":
            print(f"{self.name} reaches the goal.")
        else:
            print(f"{self.name} is waiting for further instructions.")


# 示例环境
class Environment:
    def get_status(self):
        # 环境中的状态示例（可以是动态或静态的）
        # 可以返回"obstacle"、"goal"或其他状态
        return "obstacle"
# 测试反应式Agent
env = Environment()
agent = ReactiveAgent("Agent A")
perception = agent.perceive(env)
agent.act(perception)




基于模型的Agent

class ModelBasedAgent:
    def __init__(self, name):
        self.name = name
        self.internal_state = {"position": (0, 0)}  # 例如，记录当前位置


    def update_state(self, new_position):
        # 更新内部状态
        self.internal_state["position"] = new_position


    def perceive(self, environment):
        # 从环境中感知，并更新内部状态
        return environment.get_status()


    def act(self, perception):
        # 依据感知和内部状态预测下一步行动
        if perception == "goal":
            print(f"{self.name} calculates the optimal path to the goal.")
            # 例如：利用路径算法
        elif perception == "obstacle":
            print(f"{self.name} recalculates to avoid the obstacle.")
            # 内部状态更新或改变路径
        else:
            print(f"{self.name} explores the environment.")


# 测试基于模型的Agent
env = Environment()
agent = ModelBasedAgent("Agent B")
perception = agent.perceive(env)
agent.act(perception)




基于学习型的Agent

import random


class LearningAgent:
    def __init__(self, name, learning_rate=0.1, discount_factor=0.9):
        self.name = name
        self.q_table = {}  # Q表初始为空
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor


    def choose_action(self, state, actions):
        # 基于Q表选择动作（探索与利用策略）
        if state in self.q_table:
            return max(self.q_table[state], key=self.q_table[state].get)
        else:
            return random.choice(actions)  # 初始阶段随机选择


    def learn(self, state, action, reward, next_state):
        # Q-learning更新公式
        current_q = self.q_table.get(state, {}).get(action, 0)
        max_future_q = max(self.q_table.get(next_state, {}).values(), default=0)
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount_factor * max_future_q)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q
# 示例环境与测试
actions = ["move_forward", "move_back", "turn_left", "turn_right"]
agent = LearningAgent("Agent C")
state = "initial_state"
action = agent.choose_action(state, actions)
reward = 1  # 假设行动后获得了奖励
next_state = "next_state"


# 更新学习
agent.learn(state, action, reward, next_state)
print(agent.q_table)  # 查看Q表的学习情况

只有明确了系统中的角色定义、任务、行为标准、权限等等！

才能接入MAS中，否则对整个系统来说，灾难影响！

轻则宕机，重则直接删裁关键组件，数据丢失、破坏环境！





1.2 抽象Agent接口

目标：定义标准接口以共享基础功能和方法

设计一个标准的接口，包含Agent的核心功能，如感知、决策、通信和执行动作。这个接口可以是一个编程接口或类定义，方便不同Agent共享基本方法，确保可以在同一个MAS框架中，无缝交互！

有了标准接口，我们可以做到这些：

统一的行为模式：所有Agent都实现同样的方法，简化系统的控制和管理。

多样性支持：可以在继承的基础上实现不同的决策逻辑，适应各种任务需求。

扩展性：基于标准接口，后续可以轻松添加新的Agent类型，不需更改系统整体结构。

绝大部分情况，MAS的任务多种多样，不一样的任务，接口定义，都不通用！

但在他这个类型中，是通用+有标准的！

一意常用接口任务类型，有这些：


感知（perceive）：从环境中获取信息，感知的输入可以是环境的状态、周围的Agent信息等。

决策（decide）：基于感知的信息做出决策。对于不同的Agent，决策的策略可能有所不同。

通信（communicate）：与其他Agent或系统进行信息交流。可以是直接的信息传递或基于消息的通信。

执行动作（act）：根据决策采取行动，例如移动、采集资源等。




具体代码，可以是这样的(示例)：

from abc import ABC, abstractmethod


class AgentInterface(ABC):
    @abstractmethod
    def perceive(self, environment):
        """从环境中感知信息"""
        pass


    @abstractmethod
    def decide(self):
        """基于感知的信息做出决策"""
        pass


    @abstractmethod
    def communicate(self, other_agent, message):
        """与其他Agent通信"""
        pass


    @abstractmethod
    def act(self):
        """执行具体行动"""
        pass

但他工作的时候， 不同类型的Agent可以继承该接口并实现具体的感知、决策、通信和行动逻辑。以下是一个反应式Agent的示例：


class ReactiveAgent(AgentInterface):
    def perceive(self, environment):
        # 获取环境状态，例如障碍物、目标位置等
        self.environment_state = environment.get_status()


    def decide(self):
        # 根据感知的环境状态做出简单决策
        if self.environment_state == "obstacle":
            self.action = "avoid"
        elif self.environment_state == "goal":
            self.action = "move_to_goal"
        else:
            self.action = "explore"


    def communicate(self, other_agent, message):
        # 向其他Agent传递简单信息
        print(f"{self.__class__.__name__} sends message to {other_agent}: {message}")


    def act(self):
        # 执行之前决策的行动
        if self.action == "avoid":
            print("Agent is avoiding an obstacle.")
        elif self.action == "move_to_goal":
            print("Agent is moving towards the goal.")
        elif self.action == "explore":
            print("Agent is exploring the environment.")




1.3 实现感知-决策-行动的循环

目标：构建感知、决策和行动的循环

实现感知-决策-行动（Perception-Decision-Action）循环是构建自适应、动态反应的Agent的核心！

保证每个Agent在多智能体系统（MAS）中能够实时响应环境变化并根据自己的目标做出合适的决策！

感知（Perception）


在这一阶段，Agent收集来自环境的信息，例如目标的距离、障碍物的位置或其他Agent传来的消息，感知可以通过各种传感器、API或通信协议完成。

def perceive(self, environment):
    # 感知环境中的信息（例如，障碍物或目标的位置）
    self.environment_state = environment.get_status()

这个示例，perceive从环境中获取信息，将其存储在Agent的状态变量environment_state中。

决策（Decision）

在决策阶段，Agent根据感知的数据来决定下一步行动。决策可以基于规则、策略或算法来实现。

比如，上面提到的反应式Agent可直接基于预设规则做出决策，而基于学习的Agent则使用强化学习来决定最优行为。

def decide(self):
    # 根据环境状态和内部状态进行决策
    if self.environment_state == "obstacle":
        self.action = "avoid"  # 遇到障碍物时的策略
    elif self.environment_state == "goal":
        self.action = "move_to_goal"  # 如果达到目标位置，直接行动到达
    else:
        self.action = "explore"  # 默认行为为探索环境

这里的decide方法会根据environment_state来决定当前的action（即下一步行动）。

行动（Action）

行动阶段是Agent根据决策结果采取具体行动的阶段。这可以是与环境交互、改变数据，或与其他Agent沟通等。这一动作对环境产生影响，从而形成闭环，为下一轮的感知提供更新后的状态。

def act(self):
    # 执行根据决策结果确定的行动
    if self.action == "avoid":
        print("Agent is avoiding an obstacle.")
        # 实际上可以包含更复杂的算法
    elif self.action == "move_to_goal":
        print("Agent is moving towards the goal.")
    elif self.action == "explore":
        print("Agent is exploring the environment.")

在act方法中，Agent会根据之前的决策执行相应的行为。这可能涉及路径规划、运动控制等复杂操作。

他真正工作起来时，循环的执行流程：

感知阶段：Agent调用perceive方法，从环境中获取最新状态。

决策阶段：根据感知到的环境状态，调用decide方法，确定下一个行动。

行动阶段：通过act方法，执行先前的决策行为。




代码示例如下：

class AgentInterface:
    def __init__(self, name):
        self.name = name
        self.environment_state = None
        self.action = None


    def perceive(self, environment):
        """感知环境状态"""
        self.environment_state = environment.get_status()


    def decide(self):
        """根据环境状态和内部状态进行决策"""
        if self.environment_state == "obstacle":
            self.action = "avoid"
        elif self.environment_state == "goal":
            self.action = "move_to_goal"
        else:
            self.action = "explore"


    def act(self):
        """执行决策的行为"""
        if self.action == "avoid":
            print(f"{self.name} is avoiding an obstacle.")
        elif self.action == "move_to_goal":
            print(f"{self.name} is moving towards the goal.")
        elif self.action == "explore":
            print(f"{self.name} is exploring the environment.")


    def run_cycle(self, environment):
        """感知-决策-行动循环"""
        self.perceive(environment)  # 感知环境
        self.decide()               # 进行决策
        self.act()                  # 执行动作


# 环境示例
class Environment:
    def get_status(self):
        # 模拟一个简单的环境状态（可以是动态更新的）
        # 返回 "obstacle", "goal", 或 "neutral"
        return "goal"


# 实例化Agent和环境，并运行感知-决策-行动循环
env = Environment()
agent = AgentInterface("Agent X")


# 连续运行多次感知-决策-行动循环，模拟Agent的动态反应
for _ in range(3):
    agent.run_cycle(env)

MAS中的接入，这里不延展了，否则过于拖沓，后面雄哥计划专门开发一个超高价值的MAS系统课程，再去延展！

好啦！说再多，都不及动手跑一跑！




第二部分：实践环境搭建

雄哥已做好的Agent，完成打包，并且封装成一个标准的FastAPI，你可以把他接入到MAS中，或直接本地部署，对外提供服务！

实践的环境，如下：

操作系统：Linux/WSL2


代码环境：Python 3.10


大模型：openai api（当然可以本地啦）

API接口：FastAPI

部署方案：docker


Agent数据库：neo4j

需要你在本地搭建好AI环境，还未搭建，在这里快速搭建！


第四天！手把手安装AI必备环境！4/45


所有的实践代码，都已经上传到会员盘（百度），如果你还不是会员，在末尾联系工程师，即可申请加入，加入后就能看到代码，也可以直接找到雄哥；

准备好以上之后，进入环境搭建实操！

因为雄哥已经把所有的内容，都已经打包好了，你只需要执行即可！

但！强烈推荐你自学！

如何生产打包，这些都是基本操作，后面会讲！

打开终端！跟着一行行执行！

进入工作目录！

不管你放在哪里，都不能有中文路径

cd day7/services/v1




创建独立虚拟环境！

这里创建一个Python的虚拟环境，用于管理依赖，不被污染！

python3 -m venv venv




激活环境！

source venv/bin/activate




安装雄哥打包好的依赖！

雄哥已经把依赖都打包出来了，版本对应！

喂饭到嘴！就不用你自己去安装，以免依赖冲突！

pip install -r requirements.txt




退回到主工作目录！

回到day7文件夹内！

cd ../../




这里，你要去neo4j，把图数据库打开，本地也可以，线上的，记得要开机，大概5分钟左右，才能用！

之前已经教过如何用了，今天不重复！

然后把你的api key，填到.env文件中！

保存！

然后启动docker！




我们开始构建服务后端！

非常简单！

docker-compose up --build

这个环境中的一切，会直接打包到Docker容器中！

包括Agent的服务！

耐心等待他几分钟(看你网速)，构建完成后，打开浏览器：

http://0.0.0.0:8000/docs

就能访问这个API了！

当然，他现在还是一个服务化的API！

这个API是一个标准性的，已经服务化部署出来了！

接下来，就可以用这个接口标准，接入MAS或成为独立Agent产品了！

明天会再展开！

那，他背后是怎样实现的呢？

跟着雄哥打开里面的代码，我们一步步跑！详细聊！




第三部分：深入聊聊代码！

当雄哥执行docker指令后，会先经过一个yaml配置文件，这里会定义本次指令执行的内容，然后会找到对应的fastapi.dockerfile

然后再根据dockerfile的内容，去执行对应的代码和脚本，完成依赖的打包和代码的定义！

这里，雄哥把他关键的代码拎出来！

3.1 dockerfile代码

代码路径：\ci_cd\docker\fastapi.dockerfile

# 使用Python官方镜像，可以提前下载，或者改国内源
FROM python:3.10-slim


# 设置镜像工作目录
WORKDIR /src
# 安装依赖
RUN apt-get update
RUN apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0


# 复制依赖到容器内
COPY ./services/v1/requirements.txt /src/services/v1/requirements.txt


# 安装容器内依赖
RUN python3 -m venv services/v1/.venv && \
    . services/v1/.venv/bin/activate && \
    pip install --no-cache-dir -r /src/services/v1/requirements.txt


# 复制工作目录
COPY ./ /src


# 指定环境文件
ENV PATH="/src/services/v1/.venv/bin:$PATH"


# 设置容器的端口
CMD ["uvicorn", "services.v1.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]




3.2 定义agent

代码路径：\services\v1\agents\main_agent.py

# 定义提示词
agent_prompt = hub.pull("hwchase17/openai-functions-agent")


tools = [employee_qa_tool, general_qa_tool]


# 指定工作的大模型
llm = ChatOpenAI(model="gpt-3.5-turbo")


# 定义agent模板
agent = create_tool_calling_agent(llm, tools, agent_prompt)


# 创建一个代理执行器，通过传入代理和工具
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    return_intermediate_steps=True
)




3.3 定义neo4j查询+总结回答生成任务

代码位置：\services\v1\chains\cypher_query_chain.py

雄哥在之前已经分享过这个代码了，不展开！




3.4 定义tools-函数调用

代码位置：\tools\employee_query_tool.py

这里雄哥定义了两个tools

@tool("employee-qa-tool", return_direct=True)
def employee_qa_tool(query: str) -> str:
    """Useful for answering questions about employees who work at a company."""
    response = employee_query_chain.invoke(query)


    return response.get("result")




以上就是关键的代码，就到这里吧！

明天把他接入到一个前端中，这样谁都能用这个产品了！

这个项目在雄哥做知识图谱课程时，已经基本做好了，一直比较忙，断断续续，有空就动手来敲键盘！

马上1年又过去了，今年雄哥要给会员朋友们，交付2场组队动手实践！

11月1场，12月1场！

有空的朋友一定要报名，在这里，就可以联系到雄哥工程师！

另外，慢病管理智能体系统，我们在筹备上线了！

第一阶段，会提供比较简单直接的服务！

医疗行业的各位兄弟，欢迎你直接找雄哥！
