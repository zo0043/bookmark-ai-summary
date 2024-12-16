Title: How Can I Be An AI Engineer?

URL Source: https://timkellogg.me/blog/2024/12/09/ai-engineer

Markdown Content:
Mon December 09, 2024

![Image 3: How Can I Be An AI Engineer?](https://cdn.pixabay.com/photo/2020/03/17/17/08/woman-4941164_1280.jpg)You want to be an AI Engineer? Do you even have the right skills? What do they do? All great questions. I’ve had this same conversation several times, so I figured it would be best to write it down. Here I answer all those, and break down the job into archetypes that should help you understand how you’ll contribute.

What is it?
-----------

An AI engineer is a specialized software engineer that integrates GenAI models into applications. It can involve training or fine-tuning LLMs, but it often does not. It can involve working on low-level harnesses, like [llama.cpp](https://github.com/ggerganov/llama.cpp) or [vLLM](https://github.com/vllm-project/vllm), but it often does not.

More often AI engineering involves building UIs, APIs, and data pipelines. It can look wildly different from job to job. The common thread is that you send prompts to an LLM or image model, e.g. via OpenAI’s API, and use the result in an application somehow.

Am I a good fit?
----------------

You’ll be a great AI engineer if:

1.  You’re a software engineer
2.  You have breadth (broad knowledge of a lot of domains)

Seriously, you don’t typically need to have AI experience, it’s a new field so not many people actually have prior experience. It’s tempting to think machine learning (ML) expierience is helpful, but it’s actually often more of a liability[\[1\]](https://timkellogg.me/blog/2024/12/09/ai-engineer#footnotes) to approach problems like a data scientist does.

Here are a few archetypes of AI engineers distinguished by how they look at problems. You’ll likely know which archetype you are based on what you already do.

### The Data Pipeline Archetype

An extension of a data engineer, this archetype is most likely to use [RAG architecture](https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-customize-rag.html) to build AI applications using company databases or knowledge banks. When asked, “how can I make this better?”, your answer is to improve the quality of the data, or how it’s indexed, or the model used to index it, etc. All problems center around the data.

This archetype should have a thorough understanding of RAG architecture and [embeddings](https://www.pinecone.io/learn/series/rag/embedding-models-rundown/), holds strong opinions about [vector databases](https://www.cloudflare.com/learning/ai/what-is-vector-database/) vs just using a [vector index](https://github.com/pgvector/pgvector), and maybe can diagram out how the [HNSW algorithm](https://www.pinecone.io/learn/series/faiss/hnsw/) works on the back of a bar napkin.

### The UX Archetype

This arechetype of AI engineer views “intelligence” as an inseperable collaboration between human & AI. They aren’t necessarily a UX designer or frontend engineer, but you typically can’t live as this archetype without slinging a fair bit of React code.

If you’re living this archetype, you might work with the Data Pipeline Archetype, or even also be one. But when it comes to, “how can I make this app better”, your answer is typically “tighter collaboration with the user”. You work to improve the quality of information you glean from the user, or use AI to improve the user’s experience with the app or the value they get out of it.

You might be a UX Archetype if you admire [ChatGPT](https://chatgpt.com/), [Cursor](https://www.cursor.com/), or [NotebookLM](https://notebooklm.google/) for how they helped us reimagine how we can use LLMs. You probably get excited about new LLMs that are faster or lower latency, multimodal, or new modalities.

### The Researcher Archetype

The Researcher Archetype isn’t necessarily a researcher, but they’re focused on the models and algorithms. When asked, “how can I make this app better”, their answer is about algorithms, new models, more compute, etc.

The Researcher Archetype is most likely to fine-tune their own model. To be successful as this archetype, you need to spend a lot of time keeping track of AI news on X/Bluesky/Reddit. The AI space moves fast, but as this archetype especially, you ride the bleeding edge, so it takes extra effort to keep pace. Make time to read 1-5 papers per week, and become adept at using [NotebookLM](https://notebooklm.google/).

Also, hack a lot in your spare time. You should definitely be running models locally (e.g. via [Ollama](https://ollama.com/)). You should be comfortable running [pytorch](https://pytorch.org/) models via [the Transformers library](https://huggingface.co/docs/transformers/en/index) in a [Jupyter notebook](https://jupyter.org/). You’re eyes probably light up every time [SmolLM](https://huggingface.co/blog/smollm) is in the news. And you may have a desktop with a RTX 3060 (and not for gaming).

### Other Archetypes

There’s probably several others. For example, I have a poorly-understood concept of an “artist” archetype, that uses AI to create something beautiful. Maybe more for safety, philosophy, and others. The ones outlined above are what you’re most likely to be hired for.

How is AI Engineering different from Software Engineering?
----------------------------------------------------------

For the most part, AI & Software engineering are the same. The main difference is how fast the AI field moves. Because of this, you have to be extra okay with throwing out all your work from time to time. For example, if a new framework comes out and you rewrite everything in [DSPy](https://dspy.ai/).

(By the way, you should really checkout [DSPy](https://dspy.ai/) 🔥)

Another thing is management. I keep thinking about how using AI as a tool in your work feels a lot like management, or at least being your own tech lead. I’m not sure we’ve properly equipped most engineers with the right skills, but if you thrive in the next few years, you’ll be well set up to go into management, if that’s your thing.

How do I get started?
---------------------

You’re already a solid engineer, so you’re most of the way there already. The other part is getting your continuing education setup.

I personally am not a fan of courses. There’s an absolute ton of them out there, but I believe that the mere fact that a course has to be prepared in advance and delivered many times in order to make money, that kinda implies the material is going to be a bit stale since AI moves so fast.

My recommendations:

1.  Subscribe to [The Rundown](https://www.therundown.ai/) — it’s mostly business & product releases, table stakes imo.
2.  Read everything [Simon Wilison](https://simonwillison.net/) writes. He’s basically the godfather of AI Engineering, and everything he writes is intensely practical.

Data archetypes should check out [episode S2E16 from the How AI Is Built podcast](https://open.spotify.com/episode/5bzbisAvKyp7untRUCzMJ2?si=df4db503e3914ab7). It goes into detail on trategies for improving the quality of the source data.

All archetypes should probably have a solid social media source. I think [🦋 Bluesky](https://bsky.app/) is the best, it has starter packs to get you zeroed into the right group very quickly. I know X has a lot of great chatter, but it’s extremely noisy, so it’s hard to recommend. Feel free to scrape [my account](https://bsky.app/profile/timkellogg.me) for followers.

That’s it! I hope that helps.

*   \[1\] “prior ML experience is a liability” turned out to be quite a controversial statement. I’ve followed it up with [a new post](https://timkellogg.me/blog/2024/12/10/ml-liability) expanding on the pros and cons of prior ML experience.

Discussion
----------

*   [Hacker News](https://news.ycombinator.com/item?id=42371315)
*   [🦋 Bluesky](https://bsky.app/profile/timkellogg.me/post/3lcvro2sbw22i)
*   [Threads](https://www.threads.net/@kelloggt/post/DDX-BRtvxN4?xmt=AQGz9ZtiaY_70Rlpjsxx0ja5GcQzPABr9cIhpYO8dmyJOA)
*   [LinkedIn](https://www.linkedin.com/posts/tim-kellogg-69802913_do-you-want-to-be-an-ai-engineer-heres-activity-7272017657036509186-dy42/?utm_source=share&utm_medium=member_ios)
