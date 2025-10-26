Title: 分享一个 文章 -> 图文 的提示词，炒鸡好用 - 开发调优 - LINUX DO

URL Source: https://linux.do/t/topic/1092453

Published Time: 2025-10-26T06:28:04+00:00

Markdown Content:
[![Image 1: titto](https://linux.do/user_avatar/linux.do/titto/48/363546_2.png)](https://linux.do/u/titto)

之前想做自媒体相关的内容，调研了一番，发现有些平台上特别喜欢图文内容，纯文字展示效果不太好，于是自制了一个提示词专门用来实现文字转图文。

实现机制其实带有取巧性质，流程为`文章->网页->自动截图->图文`

 话不多说，直接上效果

[![Image 2: image](https://linux.do/uploads/default/optimized/4X/9/5/a/95aca493e12e6cda36a5f4c029c3e92e918ad5a5_2_344x163.png)](https://linux.do/uploads/default/original/4X/9/5/a/95aca493e12e6cda36a5f4c029c3e92e918ad5a5.png "image")

[![Image 3: image](https://linux.do/uploads/default/optimized/4X/c/e/0/ce0bf350988a1a273d0d0a3b9b482d81c1123fce_2_345x163.jpeg)](https://linux.do/uploads/default/original/4X/c/e/0/ce0bf350988a1a273d0d0a3b9b482d81c1123fce.jpeg "image")

[![Image 4: image](https://linux.do/uploads/default/optimized/4X/e/1/a/e1ac1ac6eaec2197a9ddbaf91b8c9bc7ddb11dd6_2_345x163.jpeg)](https://linux.do/uploads/default/original/4X/e/1/a/e1ac1ac6eaec2197a9ddbaf91b8c9bc7ddb11dd6.jpeg "image")

使用流程为

 建议使用gemini 2.5 pro，是网页端大模型中效果最好的了，输入提示词和自己的文章，别忘了打开`Canvas`选项(在**工具**下拉框里)

 还没有用过cc去生成，佬友们想用的话也可以试试，欢迎分享体验效果

提示词如下

> 提示词我认为还有很多优化的空间，佬友们有想法欢迎分享优化后的提示词

```
# AI网页生成提示词：创建"高级设计感"文字卡片报告

## 1. 核心任务与角色定义
**你的角色：** 你是一位精通UI/UX设计和视觉传达的专家。你的核心任务是将一篇结构化的纯文本文档，转化为一系列具有高级设计感、信息图表(Infographic)风格的、适合截图分享的视觉卡片。

**核心原则：** 绝对尊重原文内容。你的工作是进行视觉美化，而不是内容修改或概括。必须尽可能完整地保留用户提供的所有文本。

**最终交付物：** 一个单一、完整、自包含的HTML文件。所有CSS和JavaScript代码都必须内联。

**核心目标：** 生成的网页主要用于截图，最终成品应为严格的 9:16 纵向比例。

---

## 2. 强制性技术与结构规范
这是任务的技术基础，必须严格遵守。

### 文件结构与布局：
- 单一 `.html` 文件，使用 **Tailwind CSS CDN**、**Font Awesome CDN (v6.5+)** 和 **Noto Serif SC 字体**。
- 整体页面背景为非常浅的灰色 (`bg-gray-50` 或 `#F9FAFB`)，以衬托卡片。
- 内容区域 (`.content-card`) 必须强制应用固定尺寸：`width: 474px; height: 844px;`（严格的9:16比例）。
- 卡片内部应有足够的内边距 (`padding`)，例如 `p-8` 或 `p-10`，以创造呼吸感。

### 分页与交互：
- 内容必须按语义逻辑分割成多个页面 (`<section class="page">`)。
- 提供"上一页"/"下一页"按钮和页面指示器（使用小圆点样式），上下页按钮必须与内容完全独立。
- 所有交互逻辑使用内联JavaScript实现。

### **[新增] 自动截图功能：**
必须在页面底部集成自动截图下载功能，具体要求如下：

#### 技术依赖：
- 引入 **html2canvas** 库（使用CDN，版本1.4.1或更高）：
  
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  

#### UI组件：
- 在分页控件下方添加一个独立的"自动截图所有页面"按钮
- 按钮样式应与整体设计风格一致（使用绿色系，如 `bg-green-700`）
- 添加状态提示文本区域，显示截图进度（如"正在渲染第 X / Y 页..."）

#### 截图功能实现要点：
1. **字体加载检测**：
   - 使用 `await document.fonts.ready` 确保字体完全加载
   - 添加额外的500ms延迟确保渲染稳定

2. **渐变文字处理**（重要）：
   - 由于html2canvas不支持 `-webkit-background-clip: text` 渐变效果
   - 必须实现双重样式策略：
     - 正常浏览时：使用CSS渐变文字（`.title-gradient` 和 `.highlight`）
     - 截图时：通过添加 `.capturing` 类自动切换为实色显示
   - CSS示例：
     
     .title-gradient {
         background: linear-gradient(to right, #2563EB, #7C3AED);
         -webkit-background-clip: text;
         -webkit-text-fill-color: transparent;
         background-clip: text;
     }

     .content-card.capturing .title-gradient {
         background: none;
         -webkit-text-fill-color: #2563EB;
         color: #2563EB;
     }
     

3. **html2canvas配置**：
   
   const canvas = await html2canvas(cardElement, {
       useCORS: true,
       allowTaint: true,
       scale: 2,  // 2倍分辨率，确保清晰度
       backgroundColor: '#FFFFFF',
       logging: false,
       width: cardElement.offsetWidth,
       height: cardElement.offsetHeight,
       windowWidth: cardElement.offsetWidth,
       windowHeight: cardElement.offsetHeight,
       onclone: function(clonedDoc) {
           // 在克隆文档中也添加capturing类
           const clonedCard = clonedDoc.querySelector('.content-card');
           if (clonedCard) {
               clonedCard.classList.add('capturing');
           }
       }
   });
   

4. **截图流程**：
   - 遍历所有页面（总页数根据实际分页自动计算）
   - 对每一页执行：
     a. 调用 `showPage(i)` 切换到目标页
     b. 等待800ms确保CSS过渡完成
     c. 添加 `.capturing` 类并等待100ms
     d. 执行 `html2canvas` 截图
     e. 移除 `.capturing` 类
     f. 下载为PNG文件（命名格式：`报告标题-第XX页.png`）
     g. 间隔300ms后处理下一页

5. **下载实现**：
   
   const link = document.createElement('a');
   link.href = canvas.toDataURL('image/png');
   link.download = `文章标题-第${String(i + 1).padStart(2, '0')}页.png`;
   document.body.appendChild(link);
   link.click();
   document.body.removeChild(link);
   

6. **用户反馈**：
   - 截图开始时禁用按钮并显示加载图标
   - 实时更新进度文本
   - 完成后显示"全部下载完成!"并自动重置到第一页
   - 3秒后清空状态提示

---

## 3. 内容元素处理规则 (核心)
这是将纯文本转化为高级视觉设计的关键指令。

### 标题 (Headings):
#### 一级标题 (文档主标题):
- 必须在视觉上被打散成多个层级。
- 使用大字号、粗体 (`font-bold`)。
- 必须使用醒目的 `.title-gradient` 渐变文字效果（例如：从 `from-blue-600` 到 `to-purple-600`）。

#### 二级标题 (章节标题):
- 必须与一个相关的 Font Awesome 图标配对出现。
- 图标和文字应使用醒目的品牌色（例如 `text-indigo-600`），并使用 `font-bold` 和 `text-2xl`。
- 禁止使用简单的背景高亮块。

#### 三级/四级标题 (小节标题):
- 使用加粗 (`font-semibold`) 和次一级品牌色（例如 `text-gray-800`）。

### 段落 (Paragraphs):
#### 字体与间距：
- 全局使用 `'Noto Serif SC'` 字体，`text-gray-600`。段落之间必须有足够的垂直间距 (`mb-4` 或 `mb-6`)。
- 中文字体使用衬线体
#### 强调段落：
- 如果一个段落是总结性或强调性的，应将其放入一个内嵌的浅色背景卡片中（例如 `bg-gray-50 p-4 rounded-xl border border-gray-200`）。

### 列表 (Lists):
#### 核心规则：
- 这是关键的设计机会，绝对禁止使用默认项目符号或简单的菱形。

#### 转化逻辑：
- 必须将列表转化为一系列丰富的视觉卡片。
- 每个列表项应是一个独立的 `<div>`，拥有浅色背景（`bg-gray-50`）、圆角（`rounded-xl`）、内边距（`p-4`）。
- 每个列表项必须配有一个相关的 Font Awesome 图标，图标应使用品牌色，并与列表项的标题/文本在视觉上对齐。

### 关键词与强调：
#### 高亮处理：
- 当原文中出现需要强调的关键词、术语或引用时（例如 "Context Rot"），必须对其进行强烈的视觉高亮。

#### 实现方式：
- 必须使用 `.highlight` 渐变文字效果（例如：从 `from-green-400` 到 `to-blue-500`）。
- **注意**：避免在HTML中使用内联 `style="color: xxx"` 覆盖渐变效果。
- 避免使用简单的 `bg-yellow-100` 背景高亮，这种方式过于简洁，缺乏设计感。

### 装饰性元素与视觉隐喻：
#### 信息图表化：
- 指导AI主动寻找可以视觉化的内容。例如，如果内容描述了一个"从A到B"的过程，应使用箭头图标 (`<i class="fas fa-arrow-right"></i>`) 来连接两个视觉块。

#### 对比处理：
- 如果内容是关于"问题"与"解决方案"或"A"与"B"的对比，必须使用不同颜色的背景块来承载它们（例如，问题使用 `bg-red-50`，解决方案使用 `bg-green-50`），以创造强烈的视觉对比。

#### 元信息：
- 可以在文档开头（第一页）加入一些元信息，如"全文XXX字 | 阅读需要XX分钟"，并使用较小的字号和浅灰色文字（`text-sm text-gray-400`）。

---

## 4. 分页逻辑与内容保留

### 分页原则：
- 严格按照原文的章节结构（如 "第一部分", "第二部分"）进行分页。
- **以视觉平衡为导向：** 确保每一页的内容在9:16的画幅内都是饱满且匀称的，避免页面顶部或底部出现大面积的尴尬空白。
- 一个完整的视觉模块（如一个列表卡片组）应尽量保持在同一页内。

### 内容完整性：
- **这是最高优先级。** 必须100%保留用户提供的原始文本，包括所有的括号、英文术语和标点符号。你的任务是美化它，而不是删改它。

---

## 5. 样式兼容性要求（针对截图）

### 渐变文字的处理策略：
由于html2canvas库不支持 `-webkit-background-clip: text` 的渐变效果，必须实现以下兼容方案：

1. **CSS层面**：为所有渐变文字类（`.title-gradient`, `.highlight`）准备双重样式
   - 默认样式：使用渐变效果（浏览器中正常显示）
   - 截图样式：当 `.content-card` 带有 `.capturing` 类时，使用实色替代

2. **JavaScript层面**：在执行截图前后动态添加/移除 `.capturing` 类

3. **避免内联样式冲突**：不要在HTML标签上使用 `style="color: xxx"` 覆盖类样式

---

## 6. 执行指令
现在，请严格遵循以上所有规则，将下方【用户提供的内容】转化为一个符合"高级设计感"的HTML文件。

**重要提醒：**
- 确保包含完整的自动截图功能
- 确保渐变文字在截图时能正确显示（实色后备方案）
- 确保所有依赖库（Tailwind、Font Awesome、html2canvas）都通过CDN正确引入
- 确保生成的HTML是完全自包含的，可以直接在浏览器中打开使用

---

【用户提供的内容】
xxx
```

[![Image 5](https://linux.do/user_avatar/linux.do/handsome/48/736205_2.png)](https://linux.do/u/handsome)

感谢大佬 ！
