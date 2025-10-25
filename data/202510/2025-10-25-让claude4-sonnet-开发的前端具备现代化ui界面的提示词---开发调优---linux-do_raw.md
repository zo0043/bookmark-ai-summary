Title: 让claude4 sonnet 开发的前端具备现代化UI界面的提示词 - 开发调优 - LINUX DO

URL Source: https://linux.do/t/topic/837381

Published Time: 2025-08-02T11:59:18+00:00

Markdown Content:
[![Image 1: Cx Rainy](https://linux.do/user_avatar/linux.do/cx_rainy/48/838260_2.png)](https://linux.do/u/cx_rainy)

[](https://linux.do/t/topic/837381#p-7648132-h-1)效果如下项目所示：
----------------------------------------------------------

[](https://linux.do/t/topic/837381#p-7648132-h-2)以下项目做的有点粗糙（
------------------------------------------------------------

[](https://linux.do/t/topic/837381#p-7648132-h-3)个人博客
-----------------------------------------------------

[![Image 2: image](https://linux.do/uploads/default/optimized/4X/3/5/d/35dc7ab9703ee155dce8979675a5755d6aced488_2_690x328.png)](https://linux.do/uploads/default/original/4X/3/5/d/35dc7ab9703ee155dce8979675a5755d6aced488.png "image")

[![Image 3: image](https://linux.do/uploads/default/optimized/4X/6/0/6/60663d61a7717228f2ee4beb52cc8ddab55a7b96_2_690x325.png)](https://linux.do/uploads/default/original/4X/6/0/6/60663d61a7717228f2ee4beb52cc8ddab55a7b96.png "image")

只做了前端后端其他很多功能没有配置如果你看到README.MD文件中有说配置那纯属AI胡言乱语：

[](https://linux.do/t/topic/837381#p-7648132-h-4)文件管理系统
-------------------------------------------------------

文件系统分析首页

[![Image 4: image](https://linux.do/uploads/default/optimized/4X/b/d/3/bd3ffbfae5c1df13b3b3a65f0bb02d02bbcd0b4c_2_690x327.png)](https://linux.do/uploads/default/original/4X/b/d/3/bd3ffbfae5c1df13b3b3a65f0bb02d02bbcd0b4c.png "image")

文件管理目录

[![Image 5: image](https://linux.do/uploads/default/optimized/4X/9/6/f/96f2395ee5a858e92a04f4f28b1034e5a56429ae_2_690x327.png)](https://linux.do/uploads/default/original/4X/9/6/f/96f2395ee5a858e92a04f4f28b1034e5a56429ae.png "image")

文件预览

[![Image 6: image](https://linux.do/uploads/default/optimized/4X/e/0/0/e0040b64aa89ac48d84354bea0f756d0ba22565f_2_690x327.png)](https://linux.do/uploads/default/original/4X/e/0/0/e0040b64aa89ac48d84354bea0f756d0ba22565f.png "image")

好友文件分享：

[![Image 7: image](https://linux.do/uploads/default/optimized/4X/6/b/7/6b71259984c2705d6d80df49bc5540adb1a705ec_2_690x327.png)](https://linux.do/uploads/default/original/4X/6/b/7/6b71259984c2705d6d80df49bc5540adb1a705ec.png "image")

其他功能我就不展示了可以拉取此项目玩玩（系统设置功能没有做）：

[](https://linux.do/t/topic/837381#p-7648132-h-5)爬虫可视化管理平台
----------------------------------------------------------

[![Image 8: image](https://linux.do/uploads/default/optimized/4X/c/3/7/c37d9c49e95f45eda4c5bfa1381d443e3a573e2e_2_690x324.png)](https://linux.do/uploads/default/original/4X/c/3/7/c37d9c49e95f45eda4c5bfa1381d443e3a573e2e.png "image")

[![Image 9: image](https://linux.do/uploads/default/optimized/4X/4/0/6/40655b537cc6b268664b1b5ca4c03dba0284e383_2_690x326.png)](https://linux.do/uploads/default/original/4X/4/0/6/40655b537cc6b268664b1b5ca4c03dba0284e383.png "image")

[![Image 10: image](https://linux.do/uploads/default/optimized/4X/3/2/d/32d206e5d8a4dd4755194eeaf1aa7a0b4d867a50_2_690x325.png)](https://linux.do/uploads/default/original/4X/3/2/d/32d206e5d8a4dd4755194eeaf1aa7a0b4d867a50.png "image")

[![Image 11: image](https://linux.do/uploads/default/optimized/4X/a/5/9/a5980feef34d6258008d7689678b456f73b586f5_2_690x328.png)](https://linux.do/uploads/default/original/4X/a/5/9/a5980feef34d6258008d7689678b456f73b586f5.png "image")

同样的也可以在下面可以试一下这个系统：

* * *

[](https://linux.do/t/topic/837381#p-7648132-h-6)下面是提示词文档
---------------------------------------------------------

* * *

[](https://linux.do/t/topic/837381#p-7648132-h-7)前端设计关键词与提示词指南
--------------------------------------------------------------

[](https://linux.do/t/topic/837381#p-7648132-h-8)![Image 12: :bullseye:](https://linux.do/images/emoji/twemoji/bullseye.png?v=14) 核心设计关键词
-----------------------------------------------------------------------------------------------------------------------------------------

### [](https://linux.do/t/topic/837381#p-7648132-h-9)视觉设计关键词

```
现代化、简洁、专业、科技感、高效、清晰、一致、优雅、流畅、直观
```

### [](https://linux.do/t/topic/837381#p-7648132-h-10)交互设计关键词

```
响应式、即时反馈、平滑过渡、直观操作、快速响应、智能提示、友好错误处理
```

### [](https://linux.do/t/topic/837381#p-7648132-h-11)用户体验关键词

```
易用性、可访问性、可扩展性、可维护性、性能优化、用户友好、操作便捷
```

### [](https://linux.do/t/topic/837381#p-7648132-h-12)技术实现关键词

```
组件化、模块化、类型安全、状态管理、数据缓存、实时更新、错误边界
```

[](https://linux.do/t/topic/837381#p-7648132-h-13)![Image 13: :artist_palette:](https://linux.do/images/emoji/twemoji/artist_palette.png?v=14) 详细设计提示词
------------------------------------------------------------------------------------------------------------------------------------------------------

### [](https://linux.do/t/topic/837381#p-7648132-h-1-14)1. 布局设计提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-15)主布局结构

```
创建一个现代化的管理界面布局，包含以下元素：

- 可折叠的侧边栏导航（宽度：展开256px，折叠64px）

- 固定的顶部导航栏（高度64px）

- 响应式主内容区域（自适应剩余空间）

- 支持明暗主题切换

- 流畅的过渡动画效果（duration: 300ms）

- 使用CSS Grid或Flexbox实现响应式布局
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-16)侧边栏设计

```
设计一个智能的侧边栏组件：

- 支持展开/折叠状态切换

- 导航项包含图标和文字标签

- 当前页面高亮显示

- 折叠时只显示图标，鼠标悬停显示工具提示

- 底部显示版本信息和系统状态

- 使用CSS变量控制主题色彩
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-17)顶部导航栏

```
创建一个功能丰富的顶部导航栏：

- 左侧显示当前页面标题和面包屑导航

- 右侧包含通知中心、主题切换、用户菜单

- 通知图标显示未读消息数量

- 主题切换支持浅色、深色、跟随系统

- 用户菜单包含个人资料、设置、退出登录
```

### [](https://linux.do/t/topic/837381#p-7648132-h-2-18)2. 组件设计提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-19)按钮组件系统

```
设计一个完整的按钮组件系统：

- 支持多种变体：default、destructive、outline、secondary、ghost、link

- 支持多种尺寸：sm、default、lg、icon

- 支持加载状态和禁用状态

- 使用class-variance-authority管理变体

- 支持asChild模式，可渲染为其他元素

- 包含焦点管理和键盘导航支持
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-20)表单组件系统

```
创建一套完整的表单组件：

- 输入框：支持文本、数字、密码、搜索等类型

- 选择器：下拉选择、多选、级联选择

- 开关和复选框：支持自定义样式

- 日期时间选择器：支持日期、时间、日期时间

- 文件上传：支持拖拽上传、进度显示

- 表单验证：实时验证、错误提示、成功反馈
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-21)数据展示组件

```
设计高效的数据展示组件：

- 表格：支持排序、筛选、分页、选择

- 卡片：支持多种布局和内容类型

- 列表：支持虚拟滚动、无限加载

- 图表：集成Recharts，支持多种图表类型

- 统计卡片：显示关键指标和趋势

- 进度条：支持多种样式和动画效果
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-22)反馈组件系统

```
创建用户友好的反馈组件：

- Toast通知：支持成功、错误、警告、信息类型

- 对话框：确认对话框、表单对话框、自定义对话框

- 加载指示器：旋转器、骨架屏、进度条

- 空状态：友好的空数据提示

- 错误边界：优雅的错误处理和恢复
```

### [](https://linux.do/t/topic/837381#p-7648132-h-3-23)3. 交互设计提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-24)动画和过渡

```
实现流畅的用户交互体验：

- 页面切换：使用framer-motion实现平滑过渡

- 组件进入/退出：淡入淡出、滑动、缩放效果

- 悬停效果：颜色变化、阴影变化、缩放效果

- 加载动画：骨架屏、旋转器、进度条

- 微交互：按钮点击、表单提交、状态切换
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-25)状态管理

```
设计高效的状态管理策略：

- 本地状态：使用useState管理组件内部状态

- 全局状态：使用Zustand管理应用级状态

- 服务状态：使用React Query管理API数据

- 主题状态：使用CSS变量和localStorage

- 表单状态：使用react-hook-form管理表单
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-26)数据流设计

```
优化数据获取和更新流程：

- 缓存策略：使用React Query进行智能缓存

- 实时更新：WebSocket或轮询实现实时数据

- 乐观更新：立即响应用户操作，后台同步

- 错误处理：友好的错误提示和重试机制

- 离线支持：PWA功能，支持离线操作
```

### [](https://linux.do/t/topic/837381#p-7648132-h-4-27)4. 主题设计提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-28)颜色系统

```
创建一套完整的颜色系统：

- 主色调：蓝色系（HSL: 221.2 83.2% 53.3%）

- 辅助色：灰色系（HSL: 210 40% 96%）

- 语义色：成功绿、警告橙、错误红、信息蓝

- 中性色：背景色、前景色、边框色、输入色

- 支持明暗主题切换

- 考虑可访问性，确保对比度达标
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-29)字体系统

```
设计统一的字体规范：

- 字体族：系统字体栈，支持中英文

- 字体大小：xs(12px)、sm(14px)、base(16px)、lg(18px)、xl(20px)、2xl(24px)

- 字重：normal(400)、medium(500)、semibold(600)、bold(700)

- 行高：1.4-1.6倍字体大小

- 字间距：适当的字母和单词间距
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-30)间距系统

```
建立一致的间距规范：

- 基础单位：4px (0.25rem)

- 间距等级：xs(4px)、sm(8px)、md(16px)、lg(24px)、xl(32px)、2xl(48px)

- 组件间距：内边距、外边距、边框间距

- 布局间距：页面边距、区块间距、元素间距

- 响应式间距：根据屏幕尺寸调整间距
```

### [](https://linux.do/t/topic/837381#p-7648132-h-5-31)5. 响应式设计提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-32)断点系统

```
设计移动端优先的响应式系统：

- 断点：sm(640px)、md(768px)、lg(1024px)、xl(1280px)、2xl(1536px)

- 移动端：单列布局，侧边栏可折叠

- 平板端：双列布局，保持侧边栏可见

- 桌面端：三列布局，充分利用屏幕空间

- 大屏端：优化内容密度，增加信息展示
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-33)触摸友好设计

```
优化移动端交互体验：

- 触摸目标：最小44px×44px

- 手势支持：滑动、长按、双击

- 虚拟键盘：适配输入框和表单

- 滚动优化：平滑滚动、惯性滚动

- 性能优化：减少重绘和回流
```

### [](https://linux.do/t/topic/837381#p-7648132-h-6-34)6. 性能优化提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-35)代码分割

```
实现高效的代码分割策略：

- 路由级分割：使用React.lazy分割页面组件

- 组件级分割：大型组件按需加载

- 第三方库分割：将大型库分离到独立chunk

- 预加载：关键路径组件预加载

- 缓存策略：合理设置缓存时间
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-36)渲染优化

```
优化React渲染性能：

- 虚拟化：长列表使用虚拟滚动

- 记忆化：使用React.memo、useMemo、useCallback

- 防抖节流：优化频繁触发的事件

- 图片优化：懒加载、WebP格式、响应式图片

- 动画优化：使用transform和opacity
```

### [](https://linux.do/t/topic/837381#p-7648132-h-7-37)7. 可访问性提示词

#### [](https://linux.do/t/topic/837381#p-7648132-h-38)键盘导航

```
实现完整的键盘导航支持：

- Tab键导航：所有可交互元素可访问

- 快捷键：常用功能支持快捷键

- 焦点管理：清晰的焦点指示器

- 跳过链接：提供跳过导航的链接

- 语义化HTML：使用正确的HTML标签
```

#### [](https://linux.do/t/topic/837381#p-7648132-h-39)屏幕阅读器支持

```
优化屏幕阅读器体验：

- ARIA标签：提供完整的aria属性

- 语义化结构：使用正确的HTML语义

- 替代文本：为图片和图标提供alt文本

- 状态通知：动态内容变化时通知用户

- 表单标签：为表单控件提供标签
```

[](https://linux.do/t/topic/837381#p-7648132-h-40)![Image 14: :bullseye:](https://linux.do/images/emoji/twemoji/bullseye.png?v=14) 具体实现提示词
------------------------------------------------------------------------------------------------------------------------------------------

### [](https://linux.do/t/topic/837381#p-7648132-h-41)创建按钮组件

```
创建一个现代化的按钮组件，包含：

- 支持多种变体：default、destructive、outline、secondary、ghost、link

- 支持多种尺寸：sm、default、lg、icon

- 支持加载状态，显示加载动画

- 支持禁用状态，视觉和功能都禁用

- 使用class-variance-authority管理样式变体

- 支持asChild模式，可渲染为其他元素

- 包含完整的TypeScript类型定义

- 支持键盘导航和焦点管理
```

### [](https://linux.do/t/topic/837381#p-7648132-h-42)创建表单组件

```
设计一个完整的表单系统：

- 输入框：支持文本、数字、密码、搜索、邮箱等类型

- 选择器：下拉选择、多选、级联选择、日期选择

- 开关和复选框：支持自定义样式和标签

- 文件上传：支持拖拽上传、进度显示、文件预览

- 表单验证：使用react-hook-form和zod进行验证

- 错误处理：友好的错误提示和成功反馈

- 无障碍支持：完整的ARIA标签和键盘导航
```

### [](https://linux.do/t/topic/837381#p-7648132-h-43)创建数据表格

```
实现一个功能丰富的数据表格：

- 支持排序：点击列头进行升序/降序排序

- 支持筛选：每列支持文本筛选、日期筛选、选择筛选

- 支持分页：可配置每页条数，支持跳转页面

- 支持选择：单选、多选、全选功能

- 支持操作：行操作、批量操作、自定义操作

- 支持展开：行展开显示详细信息

- 支持虚拟化：大数据量时使用虚拟滚动

- 支持导出：CSV、Excel等格式导出
```

### [](https://linux.do/t/topic/837381#p-7648132-h-44)创建通知系统

```
设计一个智能的通知系统：

- 支持多种类型：success、error、warning、info

- 支持多种位置：top-right、top-left、bottom-right、bottom-left

- 支持自动关闭：可配置自动关闭时间

- 支持手动关闭：点击关闭按钮

- 支持进度条：显示剩余显示时间

- 支持堆叠：多个通知合理堆叠显示

- 支持优先级：重要通知优先显示

- 支持持久化：重要通知可持久化显示
```

[](https://linux.do/t/topic/837381#p-7648132-h-45)![Image 15: :clipboard:](https://linux.do/images/emoji/twemoji/clipboard.png?v=14) 设计检查清单
-------------------------------------------------------------------------------------------------------------------------------------------

### [](https://linux.do/t/topic/837381#p-7648132-h-46)视觉设计检查

*   颜色对比度符合WCAG 2.1 AA标准

*   字体大小和行高适合阅读

*   图标和文字对齐一致

*   间距和留白合理

*   视觉层次清晰明确

### [](https://linux.do/t/topic/837381#p-7648132-h-47)交互设计检查

*   所有可交互元素有hover状态

*   表单验证提供即时反馈

*   错误信息清晰易懂

*   加载状态有适当的指示器

*   操作结果有明确的反馈

### [](https://linux.do/t/topic/837381#p-7648132-h-48)响应式设计检查

*   在移动端测试所有功能

*   触摸目标大小符合标准

*   横向滚动最小化

*   字体大小适配不同屏幕

*   布局在不同设备上合理

### [](https://linux.do/t/topic/837381#p-7648132-h-49)性能优化检查

*   图片使用适当格式和大小

*   代码分割合理

*   缓存策略有效

*   首屏加载时间达标

*   动画帧率保持60fps

### [](https://linux.do/t/topic/837381#p-7648132-h-50)可访问性检查

*   支持键盘导航

*   提供alt文本和aria标签

*   颜色不是唯一的信息传达方式

*   焦点指示器清晰可见

*   符合WCAG 2.1 AA标准

* * *

_这些关键词和提示词将帮助您创建高质量的前端界面，确保用户体验的一致性和专业性。_
