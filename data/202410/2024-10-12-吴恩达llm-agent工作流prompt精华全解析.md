# 吴恩达LLM Agent工作流Prompt精华全解析
- URL: https://juejin.cn/post/7384353583183036452
- Added At: 2024-10-12 07:55:20
- [Link To Text](2024-10-12-吴恩达llm-agent工作流prompt精华全解析_raw.md)

## TL;DR
本文介绍了Prompt设计原则和要素，通过ReAct、CoT、Reflexion等框架案例，展示如何针对不同任务优化Prompt。强调示例、引导和反思的重要性，并探讨了工具调用和多智能体协作的设计策略，最终总结心得并推荐进一步学习资源。

## Summary
1. **Prompt设计原则**：
   - **任务特定性**：没有万能的Prompt，需针对特定任务设计。
   - **示例重要性**：提供3到5个任务示例，帮助模型理解任务。
   - **强烈引导**：使用“必须”、“奖励”等字眼引导模型。

2. **Prompt构成要素**：
   - **解决任务的方法**
   - **任务的输入和输出**
   - **任务的示例**
   - **任务的历史记录**
   - **用户输入的问题**

3. **规划Prompt设计案例**：
   - **ReAct框架**：
     - **TAO循环**：思考（Thought）→ 行动（Action）→ 观察（Observation）。
     - **Prompt示例**：包含方法说明、输入输出、样例和用户问题。
   - **CoT框架**：
     - **思维链引导**：通过示例引导模型按思维链思考。
     - **Prompt示例**：提供背景信息、问题和示例。

4. **反思Prompt设计案例**：
   - **Reflexion框架**：
     - **自我优化**：根据历史记录排除错误答案。
     - **Prompt示例**：包含之前的尝试、问题和反思。

5. **工具调用Prompt设计案例**：
   - **分组策略**：将类似工具函数分组，避免超过Token限制。
   - **HuggingGPT示例**：分类任务，逐步思考解决用户请求。
   - **参数提示**：提示模型不要捏造参数，请求用户提供。

6. **多智能体Prompt设计**：
   - **分工合作**：不同智能体专用Prompt，提高效率。
   - **AutoGen示例**：设计对话登机服务，展示多智能体合作。

7. **总结**：
   - **Prompt设计心得**：针对不同工作流设计Prompt，提升模型表现。
   - **进一步学习**：推荐LangChain实战课程，深入LLM应用开发。
