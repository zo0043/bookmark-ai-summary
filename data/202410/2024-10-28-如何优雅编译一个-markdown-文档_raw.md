Title: 如何优雅编译一个 Markdown 文档

URL Source: https://diygod.cc/unified-markdown?locale=zh

Published Time: 2024-01-18T12:50:37.757Z

Markdown Content:
Markdown 是一种广泛使用的轻量级标记语言，允许人们使用易读易写的纯文本格式编写文档，也是 [xLog](https://xlog.app/) 主要使用的文章格式，本文就以 [xLog Flavored Markdown](https://github.com/Crossbell-Box/xLog/blob/dev/src/markdown/index.ts) 为例来说明如何优雅地解析一个 Markdown 文档

### 架构[#](https://diygod.cc/unified-markdown?locale=zh#user-content-%E6%9E%B6%E6%9E%84)

解析过程可以用这样一个架构来表示：

Mermaid Loading...

关键概念：

*   [unified](https://github.com/unifiedjs)：通过语法树和插件来解析、检查、转换和序列化内容的库
*   [remark](https://github.com/remarkjs)：unified 的生态项目之一，由插件驱动的 Markdown 处理库
*   [rehype](https://github.com/rehypejs)：unified 的生态项目之一，由插件驱动的 HTML 处理库
*   [mdast](https://github.com/syntax-tree/mdast)：remark 使用的用于表示 Markdown 的抽象语法树规范
*   [hast](https://github.com/syntax-tree/hast)：rehype 使用的用于表示 HTML 的抽象语法树规范

简单来说就是把 Markdown 文档交给一个 unified 生态的解析器解析成 unified 可识别的语法树，再通过一系列 unified 生态的插件转换为需要的内容，再通过一系列 unified 生态的工具库输出为需要的格式，下面就从 解析、转换、输出 这三个步骤来分别说明

### 解析 Parse[#](https://diygod.cc/unified-markdown?locale=zh#user-content-%E8%A7%A3%E6%9E%90-parse)

Mermaid Loading...

> 无论输入是 Markdown、HTML 还是纯文本，都需要将其解析为可操作的格式。这种格式被称为语法树。规范（例如 mdast）定义了这样一个语法树的外观。处理器（如 mdast 的 remark）负责创建它们。

最简单的一步，我们需要解析的是 Markdown，所以这里就应该使用 [remark-parse](https://github.com/remarkjs/remark/tree/main/packages/remark-parse) 来把 Markdown 文档编译成 mdast 格式的语法树

对应 [xLog Flavored Markdown](https://github.com/Crossbell-Box/xLog/blob/dev/src/markdown/index.ts) 中的

```
const processor = unified().use(remarkParse)

const file = new VFile(content)
const mdastTree = processor.parse(file)
```

### 转换 Transform[#](https://diygod.cc/unified-markdown?locale=zh#user-content-%E8%BD%AC%E6%8D%A2-transform)

Mermaid Loading...

> 这就是魔法发生的地方。用户组合插件以及它们运行的顺序。插件在此阶段插入并转换和检查它们获得的格式。

这一步最为关键，不仅包含了从 Markdown 到 HTML 的转换，还包含我们想在编译过程中夹带的私货，比如增加一些非标准的语法糖、清理 HTML 防止 XSS、增加语法高亮、嵌入自定义组件等

unified 的插件非常多，更新也比较及时，基本需求几乎都能满足，对于不能满足的特定需求，自己编写转换脚本也很容易实现

里面有一个特殊的插件是 remark-rehype，它会把 mdast 语法树转为 hast 语法树，所以在它之前必须使用处理 Markdown 的 remark 插件，在它之后必须使用处理 HTML 的 rehype 插件

[xLog Flavored Markdown](https://github.com/Crossbell-Box/xLog/blob/dev/src/markdown/index.ts) 中就加入了非常多的转换插件

```
const processor = unified()
  .use(remarkParse)
  .use(remarkGithubAlerts)
  .use(remarkBreaks)
  .use(remarkFrontmatter, ["yaml"])
  .use(remarkGfm, {
    singleTilde: false,
  })
  .use(remarkDirective)
  .use(remarkDirectiveRehype)
  .use(remarkCalloutDirectives)
  .use(remarkYoutube)
  .use(remarkMath, {
    singleDollarTextMath: false,
  })
  .use(remarkPangu)
  .use(emoji)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeRaw)
  .use(rehypeIpfs)
  .use(rehypeSlug)
  .use(rehypeAutolinkHeadings, {
    behavior: "append",
    properties: {
      className: "xlog-anchor",
      ariaHidden: true,
      tabIndex: -1,
    },
    content(node) {
      return [
        {
          type: "text",
          value: "#",
        },
      ]
    },
  })
  .use(rehypeSanitize, strictMode ? undefined : sanitizeScheme)
  .use(rehypeTable)
  .use(rehypeExternalLink)
  .use(rehypeMermaid)
  .use(rehypeWrapCode)
  .use(rehypeInferDescriptionMeta)
  .use(rehypeEmbed, {
    transformers,
  })
  .use(rehypeRemoveH1)
  .use(rehypePrism, {
    ignoreMissing: true,
    showLineNumbers: true,
  })
  .use(rehypeKatex, {
    strict: false,
  })
  .use(rehypeMention)

const hastTree = pipeline.runSync(mdastTree, file)
```

下面介绍部分用到的插件

*   [remarkGithubAlerts](https://github.com/hyoban/remark-github-alerts)：增加 GitHub 风格的 Alerts 语法，[演示](https://xlog.xlog.app/xfm#alerts)
*   [remarkBreaks](https://github.com/remarkjs/remark-breaks)：不再需要空一行才能被识别为新的自然段
*   [remarkFrontmatter](https://github.com/remarkjs/remark-frontmatter)：支持前置内容（YAML、TOML 等）
*   [remarkGfm](https://github.com/remarkjs/remark-gfm)：支持非标准的 GitHub 在原版 Markdown 语法上扩展的一系列[语法](https://github.github.com/gfm/)（但其实这系列语法已经被非常广泛使用，成为了事实意义上的标准）
*   [remarkDirective](https://github.com/remarkjs/remark-directive?tab=readme-ov-file) [remarkDirectiveRehyp](https://github.com/IGassmann/remark-directive-rehype)：支持非标准的 Markdown [通用指令提案](https://talk.commonmark.org/t/generic-directives-plugins-syntax/444)
*   [remarkMath rehypeKatex](https://github.com/remarkjs/remark-math)：支持复杂的数学公式，[演示](https://xlog.xlog.app/xfm#supports-mathematical-expressions)
*   [rehypeRaw](https://github.com/rehypejs/rehype-raw)：支持 Markdown 中夹杂的自定义 HTML
*   rehypeIpfs：自定义插件，为图片、音频、视频支持 `ipfs://` 协议的地址
*   [rehypeSlug](https://github.com/rehypejs/rehype-slug)：为标题添加 id
*   [rehypeAutolinkHeadings](https://github.com/rehypejs/rehype-autolink-headings)：为标题添加指向自身的链接 rel = "noopener noreferrer"
*   [rehypeSanitize](https://github.com/rehypejs/rehype-sanitize)：清理 HTML，用于确保 HTML 安全避免 XSS 攻击
*   rehypeExternalLink：自定义插件，给外部链接添加 `target="_blank"` 和 `rel="noopener noreferrer"`
*   rehypeMermaid：自定义插件，渲染绘图和制表工具 [Mermaid](https://mermaid.js.org/)，本文的架构图就是通过 Mermaid 渲染的
*   [rehypeInferDescriptionMeta](https://github.com/rehypejs/rehype-infer-description-meta)：用于自动生成文档的描述
*   rehypeEmbed：自定义插件，用于根据链接自动嵌入 YouTube、Twitter、GitHub 等卡片
*   rehypeRemoveH1：自定义插件，用于把 h1 转为 h2
*   [rehypePrism](https://github.com/timlrx/rehype-prism-plus)：支持语法高亮
*   rehypeMention：自定义插件，支持 @DIYgod 这样艾特其他 xLog 用户

### 输出 Stringify[#](https://diygod.cc/unified-markdown?locale=zh#user-content-%E8%BE%93%E5%87%BA-stringify)

Mermaid Loading...

> 最后一步是将（调整后的）格式转换为 Markdown、HTML 或纯文本（可能与输入格式不同！）

unified 的工具库也很多，可以输出各种我们需要的格式

比如 xLog 需要在文章右侧展示自动生成的目录、需要输出纯文本来计算预估阅读时间和生成 AI 摘要、需要生成 HTML 来给 RSS 使用、需要生成 React Element 来渲染到页面、需要提取文章的图片和描述来展示文章卡片，就分别使用了 mdast-util-toc、hast-util-to-text、hast-util-to-html、hast-util-to-jsx-runtime、unist-util-visit 这些工具

对应 [xLog Flavored Markdown](https://github.com/Crossbell-Box/xLog/blob/dev/src/markdown/index.ts) 中的

```
{
  toToc: () =>
    mdastTree &&
    toc(mdastTree, {
      tight: true,
      ordered: true,
    }),
  toHTML: () => hastTree && toHtml(hastTree),
  toElement: () =>
    hastTree &&
    toJsxRuntime(hastTree, {
      Fragment,
      components: {
        // @ts-expect-error
        img: AdvancedImage,
        mention: Mention,
        mermaid: Mermaid,
        // @ts-expect-error
        audio: APlayer,
        // @ts-expect-error
        video: DPlayer,
        tweet: Tweet,
        "github-repo": GithubRepo,
        "xlog-post": XLogPost,
        // @ts-expect-error
        style: Style,
      },
      ignoreInvalidStyle: true,
      jsx,
      jsxs,
      passNode: true,
    }),
  toMetadata: () => {
    let metadata = {
      frontMatter: undefined,
      images: [],
      audio: undefined,
      excerpt: undefined,
    } as {
      frontMatter?: Record<string, any>
      images: string[]
      audio?: string
      excerpt?: string
    }

    metadata.excerpt = file.data.meta?.description || undefined

    if (mdastTree) {
      visit(mdastTree, (node, index, parent) => {
        if (node.type === "yaml") {
          metadata.frontMatter = jsYaml.load(node.value) as Record<
            string,
            any
          >
        }
      })
    }
    if (hastTree) {
      visit(hastTree, (node, index, parent) => {
        if (node.type === "element") {
          if (
            node.tagName === "img" &&
            typeof node.properties.src === "string"
          ) {
            metadata.images.push(node.properties.src)
          }
          if (node.tagName === "audio") {
            if (typeof node.properties.cover === "string") {
              metadata.images.push(node.properties.cover)
            }
            if (!metadata.audio && typeof node.properties.src === "string") {
              metadata.audio = node.properties.src
            }
          }
        }
      })
    }

    return metadata
  },
}
```

这样我们就优雅地从原始 Markdown 文档开始，获得了我们需要的各种格式的输出

除此之外，我们还能利用解析出的 unified 语法树来编写一个可以左右同步滚动和实时预览的 Markdown 编辑器，可以参考 xLog 的双栏 Markdown 编辑器（[代码](https://github.com/Crossbell-Box/xLog/blob/dev/src/components/dashboard/DualColumnEditor.tsx)），有机会我们下次再聊
