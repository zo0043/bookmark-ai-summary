Title: 代码质量与技术债系列分享之一 - 如何做好 Code Review

URL Source: https://mp.weixin.qq.com/s/KU0RH7sHAICqiXd9EqNZ_g

Markdown Content:
**名词解释**
--------

> CR: Code Review  
> CR：代码审查  
> CL: Stands for "changelist", which means one self-contained change that has been submitted to version control or which is undergoing code review. Other organizations often call this a "change", "patch", or "pull-request".  
> CL：代表“变更列表”，表示已提交到版本控制或正在进行代码审查的独立更改。其他组织通常将其称为“更改”、“补丁”或“拉取请求”。  
> LGTM: Means "Looks Good to Me". It is what a code reviewer says when approving a CL.  
> LGTM：意思是“对我来说看起来不错”。这是代码审查员在批准 CL 时所说的。

**CR意义**
--------

灵魂拷问：为什么我们接手的每个代码库都如此难以维护？
--------------------------

![Image 29](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyFzSFg22gVMVxwzpN4wiaNIOFa1HKmXmwbL19y1yH4yzUic93Z0hcmibiaw/640?wx_fmt=png&from=appmsg)重要原因之一：Code Review 执行不彻底  
万能借口：太忙！

*   疲于应付眼前
    
*   不可见，意识不到
    
*   CR 非功能性开发
    
*   CR 不是当务之急，没有眼前收益
    
*   危害被低估，忽视“复利”的威力（非线性）
    

**意义**
------

现代代码评审【modern Code Review】，业内认为有效的、基于最佳实践的质量保证工作流，可通过人工审代码降低风险、增强可维护性和提升研发效率，同时可以有效提升个人和团队技术能力。更是一种对代码精益求精、追求极致的态度、**是“工匠精神”的一种体现。**

**CR原则**
--------

*   只要CL可以提高整体代码健康状态，就应该倾向于批准合入，即使CL并不完美
    
*   基于技术事实和数据的沟通
    

*   基于技术事实和数据否决个人偏好和意见
    
*   软件设计问题不能简单归结为个人偏好
    

*   解决冲突：不要因为无法达成一致而卡壳
    
*   善用工具
    

*   基于Lint、公司代码规范等工具
    
*   大模型辅助
    

**发起CR**
--------

**发起前的准备**
----------

*   推荐自己做一个 checklist
    
*   把自己当作 Reviewer 来对自己的代码进行 CR
    
*   预估代码可能出问题的地方
    
*   进行充分自测，保证代码可运行
    
*   不要指望别人帮你找出问题
    

checklist 可参考Code Review 速查手册

**利用自动化工具进行前置检查**
-----------------

*   单元测试检查
    
*   新增单元测试检查
    
*   方法行数过多
    
*   圈复杂度过高
    
*   代码规范检查
    
*   lint 检查
    
*   体积监控
    

`建议平均时长不要超过10分钟， 所以 e2e，性能检查等建议不阻塞发起MR流程`

**合理的规模**
---------

![Image 30](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyibyjFcriac3pKsUibFhtW1jQHbCbeWyza4TWIpToWmEDp6fIqAVRRNjwA/640?wx_fmt=png&from=appmsg)  
![Image 31](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyy73lVb2l1ewrPIxQtuDTV3ga7uLICjGWI1Wd1dHJiahtSoTYWdDTibQg/640?wx_fmt=png&from=appmsg)  
https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/

*   一次评审200LOC为佳，最多400LOC
    
*   评审量应低于500LOC/小时
    
*   一次评审不要超过60分钟
    
*   采用轻量级评审方式
    
*   全员参与代码评审
    
*   每周花费0.5~1天开展CR
    
*   严格且彻底的评审
    

### 如何拆分 CL

https://google.github.io/eng-practices/review/developer/small-cls.html

**Commit 描述**
-------------

Bad Case：
---------

![Image 32](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyZUmEqgE4iaqVkuM1KkfcN0tiamdrTdMxjEQHribdHDg9ycTLoDibukohzw/640?wx_fmt=png&from=appmsg)  
“修复错误”是不充分的 CL 描述。什么 bug？你做了什么来修复它？

其他类似的不良描述包括：

*   逻辑修复
    
*   添加补丁
    
*   增加XX规则
    
*   删除XX逻辑
    

Good Case：  
◆ 摘要：【xx模块】新增xx功能  
◆ 背景：新功能需求，要求xxx， 详见\[卡片链接\]  
◆ 说明：由于xx，新增xx处理模块…

*   摘要：删除 RPC 服务器消息自由列表的大小限制
    
*   说明：像 FizzBuzz 这样的服务器有非常大的消息，可以从重用中受益。使自由列表更大，并添加一个 goroutine 随着时间的推移慢慢释放自由列表条目，以便空闲服务器最终释放所有自由列表条目。
    

必要时，应使用 cz 等工具进行规范。

**心态**
------

*   一次 CR 其实是开启的一次“对话”
    
*   应该期待评论和反馈，并及时进行回复
    
*   做好心理准备自己的代码可能会有缺陷
    
*   CR 的目的之一就是发现问题， 所以不要有抵触
    

**CR内容**
--------

> 代码是写给人看的, 不是写给机器看的,只是顺便计算机可以执行而已。------《计算机程序的构造和解释》

**应该被 CR 的内容：**
---------------

自上而下，优先级从高到低：  
![Image 33](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyVkZ7x8x2jU2sXnZiaX47wbvDibRKSMjl0CXxV8tCt7t23aPcCeUMwmiaA/640?wx_fmt=png&from=appmsg)

![Image 34](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgy30pMg74sJxSTMTlNl5riawlkQA13UXyVrY7z9Mcc6dWNib7FV946ZNibA/640?wx_fmt=png&from=appmsg)

https://google.github.io/eng-practices/review/reviewer/looking-for.html

CR流程顺序
------

![Image 35](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyunerybJfhlKDyeIksptzoUaENw7ECIxZAzC4XU19F34wwDWUcZRm5w/640?wx_fmt=png&from=appmsg)  
https://google.github.io/eng-practices/review/reviewer/navigate

京东实际代码片段评审讲解
------------

### 设计

#### 应该有合理的职责划分，合理的封装

good case

```
componentDidMount() {
```

bad case

```
componentDidMount() {
```

问题1，fetchUserInfo 未进行封装  
问题2，af 命名过于随意  
问题3，‘300000’ 魔法字符串  
问题4，选择使用 af 或 zpm 这两个URL的逻辑建议封装，避免多次调用 isSaveUrl

#### **优秀代码设计的特质 CLEAN**

• Cohesive：内聚的代码更容易理解和查找bug  
• Loosely Coupled：松耦合的代码让实体之间的副作用更少，更容易测试、复用、扩展  
• Encapsulated：封装良好的代码有助于管理复杂度，也更容易修改  
• Assertive：自主的代码其行为和其所依赖的数据放在一起，不与其它代码互相干预（Tell but not Ask）  
• Nonredundant：无冗余的代码意味着可以只在一个地方修复bug和进行更改

#### **应避免过度设计**

别人在阅读代码时，能清晰辨别我在代码中的设计模式，并且能够随着这个模式继续维护

### **功能**

#### 逻辑正确，逻辑合理，避免晦涩难懂的逻辑

bad case：一段表单代码（原代码过长，仅贴出其中典型的一段）

```
{ hasQuota ? (
```

关键问题：连续三元判断 + 嵌套三元判断  
其他问题：

*   魔法字符串， 且重复出现
    

```
['11', '12'].indexOf(invoiceType) === -1
```

*   无意义的空行，严重影响代码阅读
    
*   FormItem 重复过多
    

Reviewer 建议：

1.  对重复代码，梳理内容，进行合理命名
    

```
const isNotOnlineInvoice = ['11', '12'].indexOf(invoiceType) === -1;
```

2.  每个 FormItem 也进行命名，三元逻辑梳理，重构
    

![Image 36](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyIXzR6WkzZfy7uhP8Ss4KKHbEBmWgEF7jTF9kqRW2Pf21ZrUibW2wGTg/640?wx_fmt=png&from=appmsg)

### 安全性

代码中应注意，不要存储敏感内容

```
// 微信服务号 生产配置中复写
```

### 一致性

*   代码一致性：
    

*   函数名和实现一致
    
*   注释和代码一致
    

*   命名方式一致
    
*   异步写法一致（promise， async await，callback混用）
    
*   抽象层级一致
    
*   不建议混用 import 和 require
    

#### 注释与代码不一致

```
getCheckboxProps: record => ({
```

#### 命名不一致

```
this.state = {
```

#### 没事别写注释

good case：  
为什么接下来的代码要这么做  
bad case：  
接下来的代码做了什么

### 复杂度

*   优先使用标准库中的能力
    
*   封装细节
    
*   写的代码越简单, bug越少
    
*   尽量遵守单一职责原则
    
*   DRY——Don’t Repeat Yourself
    

#### 无意义的函数封装

```
// 根据admitStatus判断按钮试算前置灰状态
```

#### 建议使用moment、dayjs等标准时间库处理时间：

```
// 本季度开始时间、结束时间，返回毫秒值
```

#### DRY——Don’t Repeat Yourself

下面三个方法中重复逻辑非常多，应该进行合理的封装，降低复杂性。另一个比较常见的问题，console.log 这种调试代码不应该被合入主干。

```
handleMergedInvoice = selectedRows => {
```

```
updateInvoice = ({ ...data }, i) => {
```

```
addInvoice = ({ ...data }) => {
```

#### 封装细节

看到下面这段代码，大概能够想象 newValidate 出现的原因，为了文章阅读体验， 删除部分代码  
这个验证函数，严重违反了单一职责，首先包含了多种校验逻辑，还承担了 submit 数据预处理、submit、error处理；不仅如此，还和视图层耦合，包括了回到顶部、定位到错误位置、错误DOM样式调整的逻辑。  
当然了，看到newValidate代码行数，也没有好到哪去。  
此处200多行代码就成了这个工程的毒瘤。

![Image 37](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgye6BUmicOQcF80ib2lIPVhYTFSvOGNEQfcC2a23kCvbjPlcSgsk9Uqrvw/640?wx_fmt=png&from=appmsg)

```
validate = () => {
```

#### 认知复杂度与圈复杂度

整体来说正相关， 也有例外：

```
function getWords(number) {             // +1
```

```
function sumOfPrimes(max) {             // +1
```

#### **复杂度评判标准**

1.  需要添加“黑客代码（hack）”来保证功能的正常运行。
    
2.  总是有其他开发者询问代码的某部分是如何工作的。
    
3.  总是有其他开发者因为误用了你的代码而导致出现bug。
    
4.  即使是有经验的开发者也无法立即读懂某行代码。
    
5.  你害怕修改这一部分代码。
    
6.  管理层认真考虑雇用一个以上的开发人员来处理一个类或文件。
    
7.  很难搞清楚应该如何增加新功能。
    
8.  如何在这部分代码中实现某些东西常常会引起开发者之间的争论。
    
9.  人们常常对这部分代码做完全没有必要的修改，这通常在代码评审时，或者在变更被合并进入主干分支后才被发现。  
    \--- 《编程原则》
    

### **规范性**

这部分内容比较多，更多内容见 Code Review 手册

#### **import 排序的例子**

可以看到第一段代码，没有规律，阅读成本高，第1行, 第5行出现了重复引用。  
reviewer建议：  
使用工具进行格式化，提高可读性  
https://github.com/lydell/eslint-plugin-simple-import-sort  
https://github.com/import-js/eslint-plugin-import/

```
import { ref } from 'vue'
```

```
import Taro from '@tarojs/taro'
```

#### 命名（世上问题千千万，问题命名占一半）

*   不用宽泛的模块或文件名
    
*   没有拼写错误，单复数也应该正确
    
*   符合规范：
    

*   文件名kebab-case
    
*   类名PascalCase
    
*   文件作用域内 常量、变量、函数 camelCase
    
*   private 是否采用下划线，应保持一致
    

bad case:

```
// 无意义命名
```

### 其他

#### 连等

```
// 连等
```

#### 一段重试逻辑

虽然 if 嵌套不多， 但是让人心智负担很重， 无法快速看出 count 值是多少会 false， 代码写的像面试题

```
if ((data && data.eid) || count++ > 20) {
```

reviewer 建议：  
使用卫语句提前剔除负向逻辑后， 虽然代码更长， 但是更好理解了。

```
if (!data.eid && count <= 20) {
```

**CR落地-常见挑战**
-------------

**Code Review时看不出问题**
---------------------

参考解法：  
组织集体审查讨论，提升大家审查能力，在代码质量上达成共识

### 代码审查方式对比

![Image 38](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgydP0jlSWOCePyTNV2EMQaiaBs5ZY6iaK1eX2Q5KichyPXgqhdzzLsLY30A/640?wx_fmt=png&from=appmsg)

担心冲突、害怕出错
---------

比如 A 看出了不少问题，但是发现代码作者非常不耐烦，导致 A 不敢把看到的所有问题都提出来。  
参考解法：

#### 冲突发生

*   **解决冲突**  
    ✅ Leader协助沟通及仲裁  
    ✅ 协商达成共识  
    ✅ 寻求第三人评估  
    ✅ 组内讨论  
    ❌置若罔闻  
    ❌放任自由
    

#### 预防冲突

*   **沟通技巧**  
    尽量疑向、不要太肯定  
    ✅如果采用......是否会更合适？  
    ❌这里应该......  
    ✅是否考虑过......这样的方案？  
    ❌......方案肯定更好  
    ✅这个地方似乎会影响滚动性能？  
    ❌这样写肯定会影响滚动性能
    
*   **发现问题，尽量提供建议**  
    ✅......这样会更简洁  
    ❌你这代码复杂度太高了  
    ✅根据......项目规范，这里应该这样...  
    ❌你这代码不符合项目规范
    

#### 特别注意

不要吝啬称赞👍👍👍  
没必要力求完美👍👍👍

没有时间 CR
-------

> 浇花很有意义, 但是先把火灭了

首先区分紧急与真正紧急：

![Image 39](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXkZBLS1OZficV5Cm7W7eKgyy36OYz7x4cFE3ytgBZchQB8CdgibiczvyVMhUWuWj0icYEeN862lgcMzw/640?wx_fmt=png&from=appmsg)

### **CR 时间不够**

#### 工作量评估要包含 CR 时间

推荐预留 20% 的 CR 时间

#### **权衡：**

关注设计大于具体实现；  
保证不出线上问题为底线；

#### **管理好交付里程碑**

越大的里程碑越容易产生大型CL，会拖慢CR速度  
建议数据：400行/小时（样式、dom行可适当剔除）  
建议里程碑交付周期：1周，最长2周

### **真正紧急情况**

#### **同步CR**

写完代码当面或电话同步Review

#### **并行CR**

结对编程

#### **紧急情况后门**

google 的做法：自己是Owner，写“To be reviewed”可绕过审查

**历史包袱过重**
----------

**通解：卡住增量，治理存量**  
CR的目的是让每一次合并都在改善代码仓库的水平

**其他-提升团队工程素养**
---------------

✓ 设计模式: 掌握24种设计模式  
✓ 设计原则: 掌握SOLID原则（单一职责、开闭原则、里氏替换、接口隔离、依赖反转）  
✓ 方法学: 了解Devops，极限编程，Scrum，精益，看板，瀑布，结构化分析，结构化设计  
✓ 实践: 实践测试驱动开发，面向对象设计，结构化编程，函数式编程，持续集成，结对编程

**书籍推荐**
--------

《编程原则( understanding software)》  
《重构：改善既有代码的设计》  
《编写可读代码的艺术》  
《代码大全》  
《敏捷软件开发》  
《架构整洁之道》  
《代码整洁之道》

**TL;DR**
---------

Code Review 速查手册

**参考资料**
--------

https://composity.com/post/too-busy-to-improve  
https://commadot.com/wtf-per-minute/  
https://dl.acm.org/doi/10.1145/3585004#d1e372  
https://google.github.io/eng-practices/review/reviewer/standard.html  
https://book.douban.com/subject/35513153/  
https://zhuanlan.zhihu.com/p/549019453

![Image 40](https://mmbiz.qpic.cn/sz_mmbiz_png/9K73WSRq6BXGicp40bMAicmX9DpEDjMlfPJT23acLpRzmuyiaguHv0VlmVDyEFGwd36gZYRShzhv0EPleicHyvk7KA/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp)

扫一扫，加入技术交流群
