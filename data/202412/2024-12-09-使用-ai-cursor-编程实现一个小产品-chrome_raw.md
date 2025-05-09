Title: 使用 AI Cursor 编程实现一个小产品 Chrome - 即刻App

URL Source: https://m.okjike.com/originalPosts/67568a6894480c3f73631772

Markdown Content:
使用

AI

Cursor

编程实现一个小产品

Chrome

扩展插件

MVP

功能，提前编写小产品需求技术文档作为上下文，再使用

currsor

单个页面维度生成，能够有效的减少错误，提升开发效率，所以我做了一个\[小产品需求技术文档\]

提示词分享出来，如下：

编写一个

\[主题\]

Chrome

扩展插件产品技术文档，产品核心功能包括\[功能描述1\]、\[功能描述2\]、\[功能描述3\]等，具体流程如下：  
1：产品背景：\[基于产品核心功能，拆解出产品背景和用户故事，并分析其主要特点和优势\]  
2：产品目标：\[根据产品背景生成三个产品目标\]  
3：产品需求：\[

请按照产品功能需求描述1、需求2、需求3拆解出子需求  
\]  
4：SEO

关键词：\[基于产品核心功能，拆解出产品SEO关键词、长尾关键词、相似关键词等\]  
5：技术架构：使用

plasmoJS

+

React

+

Typescript

+

Tailwindcss

+

ShadcnUI

开发  
6：项目结构：\[理解并分析产品需求

+

技术架构生成新的项目结构\]  
7：UI

设计：\[  
整体：使用

Tailwindcss

实现响应式设计,

并使用

ShadcnUI

提供现代化的

UI

组件  
布局：根据内容自动选择卡片式

+

网格式的布局方式，选择合适的布局方式进行展示  
配色：使用

三色渐变配色

+

动画配色，并使用

Tailwindcss

提供的

color

类实现颜色变化  
字体：使用

Google

Fonts

字体，基于当前系统字体和其他字体进行混合  
\]  
8：代码规范：\[  
原则：使用

SOLID、DRY、KISS、YAGNI、SRP、OCP、LSP

原则，易扩展、易维护、易理解、易单元测试、易迭代  
需求：深入分析并全理解产品需求和用户期望  
拆分：将复杂逻辑拆分为可管理的子需求，使得开发过程更加高效，减少返工  
结构：拆解出项目结构，并根据理解的需求拆解项目结构、页面、组件、数据和状态  
页面：给出合理的页面布局，并根据理解的需求拆解页面结构、组件、数据和状态  
组件：hooks和纯函数方式完成，组件划分为页面组件、公共组件、UI组件、功能组件，并且组合优于继承，减少副作用  
数据：数据请求和处理，使用

useSWR

完成，并且尽量使用

TypeScript

类型定义数据结构  
状态：保持状态最小必需状态，如多组件需要共享状态时，将状态提升至最近公共父组件，保持单一数据源，避免冲突问题；优先使用

Props

数据传递，保持单向数据流，严格遵循

React

生命周期最佳实践，尽量避免使用副作用

hooks

时，减少重复计算的依赖项，并保持简洁的依赖或无依赖。全局状态尽量使用

useContext

和

useReducer

方式管理，确保状态的可控性和可观测性。  
\]

请严格按照流程一步一步和用户互动进行完成，文档内容应当充分补充，以便后续的版本升级和扩展。并且，当用户确认完成以后，再进行下一步，直到整体流程完成。
