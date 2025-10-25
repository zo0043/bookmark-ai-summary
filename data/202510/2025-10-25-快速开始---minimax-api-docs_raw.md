Title: 快速开始 - MiniMax API Docs

URL Source: https://minimax-zh.mintlify.dev/docs/guides/quickstart

Markdown Content:
快速开始 - MiniMax API Docs

===============

[跳转到主要内容](https://minimax-zh.mintlify.dev/docs/guides/quickstart#content-area)

[MiniMax API Docs home page![Image 3: light logo](https://mintcdn.com/minimax-zh/5Q2zihEIHZrfAlAY/logo/light.svg?fit=max&auto=format&n=5Q2zihEIHZrfAlAY&q=85&s=dd237feebaeeadf61295efcd239ef00a)![Image 4: dark logo](https://mintcdn.com/minimax-zh/5Q2zihEIHZrfAlAY/logo/dark.svg?fit=max&auto=format&n=5Q2zihEIHZrfAlAY&q=85&s=cd767ae65d641fe7ad80cdbd7433dab9)](https://minimaxi.com/)

![Image 5: CN](https://d3gk2c5xim1je2.cloudfront.net/flags/CN.svg)

简体中文

[开放平台](https://minimaxi.com/platform_overview)

搜索...

Ctrl K

*   [API调试台](https://platform.minimaxi.com/examination-center/voice-experience-center/t2a_v2)
*   [文档中心](https://platform.minimaxi.com/docs)
*   [账户管理](https://platform.minimaxi.com/user-center/basic-information)
*   [登录](https://platform.minimaxi.com/user-center/basic-information)
*   [登录](https://platform.minimaxi.com/user-center/basic-information)

搜索...

Navigation

开始使用

快速开始

[开发指南](https://minimax-zh.mintlify.dev/docs/guides/quickstart)[API参考](https://minimax-zh.mintlify.dev/docs/api-reference/text-intro)[解决方案](https://minimax-zh.mintlify.dev/docs/solutions/audiobook)[更新日志](https://minimax-zh.mintlify.dev/docs/release-notes/models)[常见问题](https://minimax-zh.mintlify.dev/docs/faq/about-apis)

##### 开始使用

*   [快速开始](https://minimax-zh.mintlify.dev/docs/guides/quickstart)
*   [平台介绍](https://minimax-zh.mintlify.dev/docs/guides/platform-intro)
*   使用 MiniMax-M2 
    *   [文本生成指南](https://minimax-zh.mintlify.dev/docs/guides/text-generation)
    *   [M2 函数调用指南](https://minimax-zh.mintlify.dev/docs/guides/text-m2-function-call)
    *   [在 AI 编程工具里使用 M2](https://minimax-zh.mintlify.dev/docs/guides/text-ai-coding-tools)

##### 模型与服务

*   [模型介绍](https://minimax-zh.mintlify.dev/docs/guides/models-intro)
*   [产品定价](https://minimax-zh.mintlify.dev/docs/guides/pricing)
*   [资源保障](https://minimax-zh.mintlify.dev/docs/guides/rate-limits)

##### 使用指南

*   文本 
*   语音 
*   视频 
*   图像 
*   音乐 
*   MCP 

##### 测试与评估指南

*   [语音模型测试与评估](https://minimax-zh.mintlify.dev/docs/guides/speech-evaluate)

##### 条款与政策

*   [用户协议](https://platform.minimaxi.com/protocol/user-agreement)
*   [隐私条款](https://platform.minimaxi.com/protocol/privacy-policy)

在此页面
*   [注册指南](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E6%B3%A8%E5%86%8C%E6%8C%87%E5%8D%97)
*   [主账号与子账号的关系](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E4%B8%BB%E8%B4%A6%E5%8F%B7%E4%B8%8E%E5%AD%90%E8%B4%A6%E5%8F%B7%E7%9A%84%E5%85%B3%E7%B3%BB)
*   [获取鉴权信息](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E8%8E%B7%E5%8F%96%E9%89%B4%E6%9D%83%E4%BF%A1%E6%81%AF)
*   [使用方式](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F)
*   [1. 通过 API 调用 MiniMax-M2 模型](https://minimax-zh.mintlify.dev/docs/guides/quickstart#1-%E9%80%9A%E8%BF%87-api-%E8%B0%83%E7%94%A8-minimax-m2-%E6%A8%A1%E5%9E%8B)
*   [2. 在 AI 编程工具中使用 MiniMax-M2 模型](https://minimax-zh.mintlify.dev/docs/guides/quickstart#2-%E5%9C%A8-ai-%E7%BC%96%E7%A8%8B%E5%B7%A5%E5%85%B7%E4%B8%AD%E4%BD%BF%E7%94%A8-minimax-m2-%E6%A8%A1%E5%9E%8B)

开始使用

快速开始
====

复制页面

欢迎访问 MiniMax 开放平台，可参考快速开始指南，体验模型能力。

复制页面

[​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E6%B3%A8%E5%86%8C%E6%8C%87%E5%8D%97)

注册指南
------------------------------------------------------------------------------------------------------

若您是首次使用，需要先在 MiniMax 开放平台进行注册。 企业团队注册时，建议采用**主账号+子账号**的形式创建和管理。
*   **个人注册**：若您是单人使用，直接在 [MiniMax 开放平台](https://platform.minimaxi.com/user-center/basic-information) 进行注册即可
*   **企业团队注册**：若您是多人业务团队进行使用，建议采用**主账号+子账号**的形式进行管理 
    1.   在 [MiniMax 开放平台](https://platform.minimaxi.com/user-center/basic-information) 注册一个账号（此账号即为主账号，注册时填写的姓名与手机号会成为本企业账号的管理员信息）
    2.   登录该主账号，在 [账户管理 > 子账号](https://platform.minimaxi.com/user-center/basic-information/child-account)，创建您所需要数量的子账户（子账号的创建数量暂时没有限制）
    3.   为您企业的人员，分配不同的子账户，进行登陆使用

### [​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E4%B8%BB%E8%B4%A6%E5%8F%B7%E4%B8%8E%E5%AD%90%E8%B4%A6%E5%8F%B7%E7%9A%84%E5%85%B3%E7%B3%BB)

主账号与子账号的关系

*   子账号和主账号享用相同的使用权益与速率限制，子账号和主账号的 api 消耗可以进行共享，最后进行统一结算
*   子账号的限制：子账号无法查看和管理“支付”页面的查看与管理，也无法进行子账号、以及子账号的接口密钥的管理操作

[​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E8%8E%B7%E5%8F%96%E9%89%B4%E6%9D%83%E4%BF%A1%E6%81%AF)

获取鉴权信息
--------------------------------------------------------------------------------------------------------------------------

( 1 ). 通过 [账户管理 > 账户信息 > 基本信息](https://platform.minimaxi.com/user-center/basic-information)，获取 **group_id**。![Image 6: 获取 group_id](https://filecdn.minimax.chat/public/80adc2d6-6ebb-4e41-9986-d40836df7475.png)( 2 ). 通过 [账户管理 > 接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key)，获取 **API Key**。 点击“创建新的密钥”，在弹窗中输入密钥的名称，创建成功后，系统将展示 API Key。**请务必复制并妥善保存**，该密钥**只会显示一次**，无法再次查看。![Image 7: 获取 API Key](https://filecdn.minimax.chat/public/44528a3e-7815-4ddb-80d2-a662519b0df2.png)
[​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F)

使用方式
------------------------------------------------------------------------------------------------------

### [​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#1-%E9%80%9A%E8%BF%87-api-%E8%B0%83%E7%94%A8-minimax-m2-%E6%A8%A1%E5%9E%8B)

1. 通过 API 调用 MiniMax-M2 模型

支持通过 Anthropic 或 OpenAI 兼容的 API 接口调用模型

[OpenAI API 兼容 ------------- 通过 OpenAI SDK 调用 MiniMax 模型 点击查看](https://minimax-zh.mintlify.dev/docs/api-reference/text-openai-api)[Anthropic API 兼容 ---------------- 通过 Anthropic SDK 调用 MiniMax 模型 点击查看](https://minimax-zh.mintlify.dev/docs/api-reference/text-anthropic-api)

### [​](https://minimax-zh.mintlify.dev/docs/guides/quickstart#2-%E5%9C%A8-ai-%E7%BC%96%E7%A8%8B%E5%B7%A5%E5%85%B7%E4%B8%AD%E4%BD%BF%E7%94%A8-minimax-m2-%E6%A8%A1%E5%9E%8B)

2. 在 AI 编程工具中使用 MiniMax-M2 模型

[在 AI 编程工具里使用 MiniMax-M2 ----------------------- 具备代码理解能力，适用于代码助手等场景。 点击查看](https://minimax-zh.mintlify.dev/docs/guides/text-ai-coding-tools)

此页面对您有帮助吗？

是 否

[平台介绍](https://minimax-zh.mintlify.dev/docs/guides/platform-intro)

Ctrl+I

[discord](https://discord.com/invite/hvvt8hAye6)[x](https://x.com/MiniMax__AI)[linkedin](https://www.linkedin.com/company/minimax-ai)[github](https://github.com/MiniMax-AI)

[由Mintlify提供支持](https://mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=minimax-zh)

助手

Responses are generated using AI and may contain mistakes.

![Image 8: 获取 group_id](https://filecdn.minimax.chat/public/80adc2d6-6ebb-4e41-9986-d40836df7475.png)

![Image 9: 获取 API Key](https://filecdn.minimax.chat/public/44528a3e-7815-4ddb-80d2-a662519b0df2.png)
