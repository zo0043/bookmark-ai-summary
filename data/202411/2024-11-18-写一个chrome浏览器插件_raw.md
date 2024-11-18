Title: 写一个Chrome浏览器插件作者：京东工业 焦丁 一、什么是浏览器插件 浏览器插件是依附于浏览器，用来拓展网页能力的程序 - 掘金

URL Source: https://juejin.cn/post/7438494617508888610

Markdown Content:
作者：京东工业 焦丁

一、什么是浏览器插件
----------

浏览器插件是依附于浏览器，用来拓展网页能力的程序。插件具有监听浏览器事件、获取和修改网页元素、拦截网络请求、添加快捷菜单等功能。使用浏览器插件可以实现很多有趣的功能。

![Image 1](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/94ea01e5efa543f68ac72969581c7723~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=OVt%2BrDL9rz7L7WGUGotfNmEJnHM%3D)

二、浏览器插件有哪些种类
------------

•以chromium为内核的浏览器插件如Chrome

•﻿firefox浏览器插件

•﻿﻿safari浏览器插件

本文只介绍Chrome插件的原生开发流程。

三、插件目录介绍
--------

![Image 2](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/77ec65d3cb394de2a4da615ebed88539~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=JRwA5gKpvYcRpG5pOT9tNsCx7UA%3D)

| a的文件名 | 文件介绍 |
| --- | --- |
| [manifest](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fmanifest%3Fhl%3Den "https://developer.chrome.com/docs/extensions/reference/manifest?hl=en") | 核心配置文件，配置插件平台版本、名称、[权限](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fpermissions-list%3Fhl%3Dzh-cn "https://developer.chrome.com/docs/extensions/reference/permissions-list?hl=zh-cn")、Aicon、[Api权限](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fapi%3Fhl%3Den "https://developer.chrome.com/docs/extensions/reference/api?hl=en")、host权限等。 |
| popup.html | 插件弹出页面，原生html、css页面。 |
| popup.js | 插件页面的脚本文件。 |
| popup.css | 插件页面的样式文件 |
| background.js | 后台文件，可以监听浏览器事件，在浏览器后台持续运行。 |
| [content.js](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Fdevelop%2Fconcepts%2Fcontent-scripts%3Fhl%3Dzh-cn "https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts?hl=zh-cn") | 插入到页面中的js脚本，可以监听DOM事件，操作DOM元素。 |

四、开始写一个插件
---------

### 1\. 配置manifest。

以下是一个基础的manifest配置

![Image 3](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ac423b188a1042899ad61d1f61d6416c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=sqcVxP8DWfz5vYPLbk68Zt08wMo%3D)

### 2\. 写一个插件的弹框界面popup.html

和写html页面一样，在body里面写元素，但是需要注意样式文件popup.css和脚本文件popup.js需要外部引入。

![Image 4](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5f24137e1c1f448c98531302dc084cff~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=iYY3TWuQqkFMb0yqfuojRCNvZro%3D)

### 3\. 写一个插件弹框界面的样式文件popup.css。

### 4\. 写一个插件弹框界面的脚本文件popup.js。

脚本文件的主要作用在于响应插件弹窗的行为事件，并发送消息给内容脚本或者后台脚本。

以下代码是在popup.js中，监听id为tag元素的点击事件，获取当前窗口active标签页，并给此标签页推送一个message。

![Image 5](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7a0efa62f7ef4e1695a1094dfe624f91~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=8YDstw4AK2DVKycfbQGht6f6fTs%3D)

### 4\. 写一个插件的内容脚本content.js

content.js会被插入到网页环境中，用于监听浏览器事件，读取和操作DOM元素。

以下代码是监听页面load事件，和接收来自第三步中send的message。

```

window.addEventListener("load", function () {
    // 监听页面load事件
})

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
 console.log("-----------");
 if (request.greeting === "tag") {
    console.log(request.greeting)
 }
});
```

### 5\. 写一个插件的后台脚本background.js

后台脚本会在浏览器窗口打开期间持续运行，监听浏览器事件，网络请求等。

以下代码是浏览器屏蔽漏某些url请求的实现。

![Image 6](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/2891462eb87c4dbca82e97d1b4acc4b5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=3K5HNAkXQhJ4NXibSj4fkoQf%2BmY%3D)

把上述的几个文件创建完成之后就实现了一个简单的插件，然后直接安装到浏览器扩展即可。

五、解释几个消息发送和接收的Api
-----------------

### 1\. 获取指定的浏览器标签页：

```
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {})
```

### 2\. 向指定标签页中的内容脚本发送一条消息，其中包含在发送回响应时运行的可选回调函数。在当前扩展程序的指定标签页中运行的每个内容脚本中都会触发 [runtime.onMessage](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fruntime%2F%3Fhl%3Dzh-cn%23event-onMessage "https://developer.chrome.com/docs/extensions/reference/runtime/?hl=zh-cn#event-onMessage") 事件。

```
chrome.tabs.sendMessage(tabs[0].id, { greeting: "tag-remove" }, function (response) { console.log(response); });
```

### 3\. 向扩展程序或其他扩展程序/应用中的事件监听器发送一条消息。[请注意，扩展程序无法使用此方法向内容脚本发送消息。如需向内容脚本发送消息，请使用](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fapi%2Fruntime%3Fhl%3Dzh-cn%23method-connect "https://developer.chrome.com/docs/extensions/reference/api/runtime?hl=zh-cn#method-connect")

```
chrome.runtime.sendMessage(  extensionId?: string,  message: any,  options?: object,  callback?: function,)
```

### 4\. onMessage，通过扩展程序进程（通过 [`runtime.sendMessage`](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fapi%2Fruntime%3Fhl%3Dzh-cn%23method-sendMessage "https://developer.chrome.com/docs/extensions/reference/api/runtime?hl=zh-cn#method-sendMessage")）或内容脚本（通过 [`tabs.sendMessage`](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Ftabs%2F%3Fhl%3Dzh-cn%23method-sendMessage "https://developer.chrome.com/docs/extensions/reference/tabs/?hl=zh-cn#method-sendMessage")）发送消息时触发。

```
chrome.runtime.onMessage.addListener(  callback: function,)
```

想了解其他浏览器插件Api，请点击[跳转](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fapi%3Fhl%3Dzh-cn "https://developer.chrome.com/docs/extensions/reference/api?hl=zh-cn")﻿
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

六、接下来让我们丰富插件的能力
---------------

### 1\. 实时删除页面上的元素，我们经常会遇到一些烦人的广告，删掉他。广告一般都是有固定的元素节点的，找到元素节点的class或者id，按以下处理。

以[百度一下](https://link.juejin.cn/?target=https%3A%2F%2Fwww.baidu.com%2F "https://www.baidu.com/")页面举例，以下代码实时监听网页元素，发现class为s-p-top的元素后就会删除改元素，这里我给被删除元素的位置加了一个红色边框用来测试，实际使用中可以删除添加红框的代码。

在content.js中添加以下代码：

![Image 7](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/388b765dfb4546b48806583bbf89c8fc~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=9L%2BU0gmmaOC83zddMxbRkYuUeN0%3D)

**通过下面两个图对比可以看出使用插件后百度图片被删除了：**

![Image 8](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/566389e23eea42849eb9e1fd1afc7af0~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=%2BKHpJ5VNIK05JfaUoNI%2FmSr1fO0%3D)

![Image 9](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4c99f44194074b49bb85f99b2463549b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=Jd4Q7Iit5K6k%2BRAgJRfb27slACo%3D)

### 2\. 有人不习惯点开右上角插件再点击功能按钮，怎么办呢，简单，给浏览器右键菜单添加快捷键。

以下代码为添加浏览器右键菜单的快捷键，并监听菜单点击事件，可在menu2中发起请求。

在background.js中：

![Image 10](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a0e46702a62145d48a75c17581de31e2~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=GxgPE7lbxTlL1QI5WU3g1imN1kU%3D)

效果如下：

![Image 11](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/31f96e9afaa64026a54d8ab7d68aecce~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=HiHYRRSr3XAndVJ7hKES7syhwUg%3D)

### 3\. 还是拦截广告，广告可能出现在**iframe中**，但是呢我不想使用删除DOM的方式，怎么办呢，那就直接拦截网络请求。

在background.js中：

![Image 12](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1038e2c7658342fab20c188a962b82a6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=PNA9nvRg5aiG%2BBEWpKW8F0wQT7Q%3D)

**我们还以baidu.com为例，在**[**MDN**](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWeb%2FHTML%2FElement%2Fiframe "https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/iframe")**中测试，修改iframe src的值为baidu.com.**

**使用插件前结果如下:**

![Image 13](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/bd653adcf4a149dcad2dfeea0ddcd2d7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=4yBjgKQsgktaIZoFdjUsmAWrPLY%3D)

**使用插件后结果如下，可以发现iframe中没有渲染baidu.com，并且在network中可以看到baidu.com被屏蔽了:**

![Image 14](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0f8f711c34a44474a41b504a7cc025aa~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=mzKg6GCnO0pI9%2BcFyY4yh93SPLA%3D)

### 4\. 自定义一个自己的新开页

两步走

**第一步：在manifest中定义newtab（就是一个html文件，这个文件会覆盖原生的浏览器新开页）**

![Image 15](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fd71592a52b94f2f85140692bdf31a3d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=Q7sJVjW2zX2ztFybZwCINdVTbQk%3D)

**第二步：创建newtab.html文件，可以在这个文件定义新开页的样式和js，且此样式文件和js文件不用添加到content\_scripts中**

![Image 16](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c6084dc6779542f89a396326120d4da8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=fsWRcnP6j%2BXfwtWGIWpXFOT8wMg%3D)

**效果如下**

![Image 17](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/33fb110456f04b898cc26858d125919c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=NmGwSoPd6eAFRXddQWFg%2Fm8%2FKd4%3D)

### **5\. 标记页面文本**

**在阅读网页文档时，经常会想标记一些重点文本，可以直接用扩展来实现：**

**在background.js中：**

![Image 18](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/fb50bcfba0fe40a2a7c1798b6997aeef~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=MXX13Yb%2FSLIyub9u6%2BXtNoj0O6w%3D)

**在content.js中：**

![Image 19](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c21cc2138f7b4da38e4bfd634e381dae~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=s4d1KcXwghzgEcl%2F68wnfiC0W1k%3D)

**效果：**

![Image 20](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5c159ca5a66a473691334b550a606320~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=1I4A9RGMLxScrJT0M2XDHOjUfqA%3D)

功能先丰富到这里，后面再继续补充~

![Image 21](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d6aea6721a9e440f8323fe60516a3879~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5Lqs5Lic5LqR5byA5Y-R6ICF:q75.awebp?rk3s=f64ab15b&x-expires=1732521167&x-signature=SC0qXU5XtPOQ9Qj9Sp3Vdd10BC4%3D)

七、参考文档
------

[chrome扩展参考文档](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Fget-started%3Fhl%3Dzh-cn "https://developer.chrome.com/docs/extensions/get-started?hl=zh-cn")

[chrome Api文档](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fapi%2FdeclarativeNetRequest%3Fhl%3Dzh-cn%23type-ResourceType "https://developer.chrome.com/docs/extensions/reference/api/declarativeNetRequest?hl=zh-cn#type-ResourceType")

[manifest权限配置文档](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fextensions%2Freference%2Fpermissions-list%3Fhl%3Dzh-cn "https://developer.chrome.com/docs/extensions/reference/permissions-list?hl=zh-cn")
