Title: The 6 Types of Conversations with Generative AI

URL Source: https://www.nngroup.com/articles/AI-conversation-types/

Published Time: 2023-11-10T18:00:00+0000

Markdown Content:
Summary:  When interacting with generative-AI bots, users engage in six types of conversations, depending on their skill levels and their information needs. Interfaces for UI bots should support and accommodate this diversity of conversation styles.

Through analyzing 425 interactions with generative-AI bots like ChatGPT, Bing Chat, and Bard, we've discovered that conversations could involve many vague, underspecified prompts or few, razor-sharp ones. Why does this matter? First, **different conversation types serve distinct information needs and demand varied UI designs**. Second, **there is no one optimal conversation length** — both short and long conversations can be helpful, as they might support different user goals.

*   [Our Research](https://www.nngroup.com/articles/AI-conversation-types/#toc-our-research-1)
*   [Types of Conversations](https://www.nngroup.com/articles/AI-conversation-types/#toc-types-of-conversations-2)
*   [Conversation Length Is Not a Success Indicator](https://www.nngroup.com/articles/AI-conversation-types/#toc-conversation-length-is-not-a-success-indicator-3)
*   [Tips for Using Text-Based Generative-AI Bots](https://www.nngroup.com/articles/AI-conversation-types/#toc-tips-for-using-text-based-generative-ai-bots-4)
*   [Recommendations for Designing the UX of Generative AI](https://www.nngroup.com/articles/AI-conversation-types/#toc-recommendations-for-designing-the-ux-of-generative-ai-5)

Our Research
------------

In May and June 2023, we conducted a 2-week diary study involving 18 participants who used ChatGPT 4.0, Bard, and Bing Chat. Participants logged a total of 425 conversations and rated each for helpfulness and trustworthiness. At the end of the study, we conducted in-depth interviews with 14 participants.

The findings of this study are reported in several articles:

*   [Information foraging with generative AI](https://www.nngroup.com/articles/generative-ai-diary/): how AI bots change the process of finding information
*   [Differences in helpfulness and trustworthiness among ChatGPT, Bing Chat, and Bard](https://www.nngroup.com/articles/ai-bot-comparison/)
*   Different types of conversations with AI bots (this article)
*   Prompt structure in AI conversation (forthcoming)

Types of Conversations
----------------------

Several types of conversations emerged from our analysis:

*   Search queries
*   Funneling conversations
*   Exploring conversations
*   Chiseling conversations
*   Expanding conversations
*   Pinpointing conversations

Some conversations involved several prompts and reformulations, whereas others were relatively short.

![Image 1](https://media.nngroup.com/media/editor/2023/11/09/ai-convos_icon-metaphors.png)

_6 types of conversation with generative AI_

In what follows, we discuss each of these 6 types of conversations; for each, we provide tips for both users and interface designers of generative AI chatbots.

### Search Query

These conversations are **one-prompt, simple queries that are not followed by any refinements**. The prompt usually includes the question with no framing or format specification.

In our diary study, the intent behind search-query conversations was the same as for a web search: users were trying to locate a specific piece of information. These conversations were common when people were still trying to understand what the bots could do for them and what they were best at. In such situations, it is likely that users were simply transferring their search [mental models](https://www.nngroup.com/articles/mental-models/) to the AI bots.

Examples of search-query conversations from our diary study include:

*   _Rosie Odonnell_
*   _Concert dates for Toby Keith_
*   _What is a Chaffle?_

When these search-query conversations involved Bing, participants often clicked on the suggested links and visited the sites, as they normally would have done when using a search engine.

While short keyword phrases like _Rosie Odonnell_ might work well for search, they lack enough context to help AI chatbots understand what the user is asking for. Sometimes users realized that a search engine would be better suited for such queries and quit the bot.

 

_Upon seeing the results of_ her Independence Day themed foods _query in Bing Chat, the participant clicked on the thumbs-down button; she said_: I decided to turn to Google, for the results, and upon entering the same search, I was given pictures and recipes for Independence Day-themed foods and even party favors. _(The video was played at 1.5x speed.)_

Both users and designers need to consider what the best tool is for a given information need. Sometimes, it could be that an AI chatbot won’t do a job as good as a search engine.

#### Tips for Users of AI Bots

Avoid using this type of prompt when working with AI bots like ChatGPT. While search engines perform best with keywords, AI bots need more context to understand what kind of response or output you’re looking for.

**Search engines might (for now) give you as good if not better results as AI bots** if:

*   You are looking for an answer to a very specific, factual question about an event, a date, a location, or a person.
*   You need to inspect a lot of options before selecting a particular one.

#### Tips for Designers of AI Bots

Consider **allowing users to easily switch to a search-engine mode or access search-engine results_,_** like Bard does.

![Image 2](https://media.nngroup.com/media/editor/2023/11/07/bard-higher-res.jpg)

_Bard: Users can perform a Google search based on the query they entered, by selecting one of the blue topics at the bottom of the answer._

### Funneling Conversations

In funneling conversations, **the user starts with an underspecified, sometimes too vague query and then narrows it down with subsequent questions that specify additional constraints.** Often, the user doesn’t realize that they need to be more specific until they receive an unsatisfactory response from the bot.

For example, here is a sequence of queries asked by one user who was trying to find a recipe:

1.  _i am looking for a appetizer to serve pool side on memorial day weekend. i do not want to use pork and i want something fairly easy to make that can sit outside_
2.  _how about an easier appetizer that can be passed around 30 people or so_
3.  _anything other than skewers? i was thinking some sort of dip?_

If the user had anticipated all of these requirements, she could’ve achieved her desired result with a single prompt:

> _I want an easy appetizer recipe for 30 people to serve poolside on Memorial Day Weekend. I’m thinking of some sort of dip. I don’t want to use pork and the appetizer needs to be able to sit outside in the heat._

However, she likely did not consider this full set of constraints until she received the bot’s initial suggestions.

Funneling conversations are often long, as the user might need to input several prompts to refine their query. Sometimes they start with best-of prompts or other basic prompts that lack details. For example, here’s a sequence of prompts from a user interested in figuring out how to prevent her migraines:

1.  _What are the best cures for a migraine?_
2.  _What do you think would be the most effective cure for a migraine?_
3.  _I experience migraines 2-3 times a week, is there a likely cause for this?_
4.  _I normally have 2-3 cups of coffee per day and on days when I don't consume any, I usually get migraines. Can a lack of caffeine contribute to migraines?_
5.  _How many milligrams of caffeine are typically in a 12 oz cup of coffee?_

Note that, **in funneling conversations, the user’s information need is usually specific and well-defined, but poorly articulated**. In other words, the user will likely recognize a correct response, but will not be able (or sometimes will not be bothered) to say what that correct response should look like. However, **the bot can facilitate query articulation by asking the user helping questions**.

In some of the conversations we studied, the bot did ask for clarification. For example, one participant started the conversation with _Issue with swimming pool cleaner._ ChatGPT asked for specific information about the cleaner and the issue, expediting the funneling process.

![Image 3](https://media.nngroup.com/media/editor/2023/11/07/pool-cleaner.jpg)

_ChatGPT helped the user focus his funneling conversation by asking for a set of details relevant to providing an answer._

#### Tips for Using AI Bots

Consider **explicitly telling the AI bot to ask helping questions** to improve its output. For example, you may add phrasing such as _Ask me questions if you need additional information_, to get the bot to help you articulate the different constraints that you may be working with.

#### Tips for Designing AI Bots

To reduce the articulation load in funneling conversations, the **bot should ask helping questions that narrow down underspecified queries**.

### Exploring Conversations

In exploring conversations, the user starts with a general, less-defined query (usually lacking context or output-format specifications) and then **uses the AI to understand the information space and get ideas for new queries.**

Exploring conversations differ from funneling conversations in that, in the beginning, the user is not able to formulate a specific enough query **because they have a less-defined information need and lack the necessary vocabulary or knowledge** (rather than because they did not spend the time to think of all the requirements for their information need). The bot’s responses help the user learn about the structure of the information space and give them new terminology and ideas about what to ask next.

An exploring conversation often **feels like a conversation with a real teacher;** the user acts as a student **learning by** **acquiring depth into a topic** and asking questions as they learn. The user is building queries based on the information received from the bot.

For example, one user asked _What is the meaning of life?_ The bot talked about various kinds of views, including philosophical, religious, and absurdist views. The user then asked to know more about one of these — absurdism. When the bot mentioned the book “The Myth of Sisyphus” by Albert Camus, the user asked for other works by the same author.

 

_A study participant started by asking_ what are some safe sleeping habits for newborns_. When the bot mentioned sudden infant death syndrome (SIDS), which the user did not know of, he selected the suggested query_ What is SIDS? _Bing was good at offering suggested followup prompts that allowed the user to further explore the subject. (The video was played at 1.5x speed.)_

In exploring conversations, users can be supported with **suggested followup prompts that naturally build upon the information presented in the bot’s answer.**

#### Tips for Designing AI Bots

If the user’s information need is broad and the bot’s response is complex, containing jargon and domain-specific facts or concepts, **offer a list of suggested followup prompts** that build upon these details.

The followup prompts can include:

*   Definitions for domain-specific words (e.g., _What is …_?)
*   Additional information about any of the facts or concepts included in the response (e.g., W_hy…?, What caused …?, How can one do …?_)

However, detail-oriented suggested followup prompts do not need to be included in all conversations. **Conversations with well-defined information needs (such as pinpointing conversations — see below) rarely benefit from such followup prompts.** For example, a user rewriting her resume said:

> _if I'm asking you to put something in my resume, like, I do research in \[…\] B-cell malignancies, I don't necessarily need to ask ‘what are B-cell malignancies.’_

### Chiseling Conversations

In chiseling conversations, the user asks **about different facets of the same topic, fleshing it out from a variety of angles** like a sculptor chisels a sculpture from a piece of stone. Chiseling conversations cast a wide net over a topic to acquire **breadth**. They can feel like research on a specific topic, but the research is person-driven rather than driven by the bot’s answers.

Here is a sequence of questions asked in the same chiseling conversation about ADHD:

1.  _What are some tips for people with ADHD to remember daily tasks more effectively?_
2.  _who are some famously successful people who have ADHD_
3.  _is ADHD considered a disability?_

While these questions are all related to ADHD, they cover various aspects of ADHD and do not explore any one of these in depth. It feels as if the respondent is trying to learn many facts about the topic, without focusing on the logical relationship between these facts.

Another user was doing research on the company Insperity. She asked multiple questions related to different aspects of the company:

1.  _What does insperity do?_
2.  _How does Insperity make money?_
3.  _What percentage of revenue comes from each area?_
4.  _How is Insperity's revenue broken down? (reformulation of previous question)_
5.  _What are some goals of Insperity?_
6.  _What are executive priorities at Insperity?_
7.  _How is Insperity's stock doing?_
8.  _Do you have access to analyst reports? for example analysts from Morgan Stanley?_

**Both exploring and chiseling conversations correspond to less-defined information needs and imply learning about a topic**. But, while in exploring conversations, the learning involves acquiring depth into the topic, in chiseling conversations the learning is carried out through breadth.

![Image 4](https://media.nngroup.com/media/editor/2023/11/08/ai-convos_ex_ch.png)

_Exploring conversations explore a topic in depth; chiseling conversations favor breadth by examining different facets of the same topic._

Tips for Designing AI Bots

Like exploring conversations, chiseling conversations benefit from suggested followup queries. However, for chiseling conversations, **suggested followup prompts should be broad, inquiring about multiple facets of the same topic or about related topics (e.g., _How about…?)_**.

In contrast, for exploring conversations, these prompts should go in **depth**, delving into details about a particular concept or fact in the answer.

### Pinpointing Conversations

In pinpointing conversations, the user has a defined topic in mind and **creates a very specific prompt from the very beginning**. The prompt often includes context and a format specification.

> _Summer Cocktail Party: My wife and I are hosting a small cocktail and dinner party welcoming my daughter's future in-laws for a visit to California in late July. The party will be indoors and outdoors by the pool, and we will be grilling something no doubt for the meal. It will be hot in late July so drinks that are refreshing would be order. I am not a professional bartender, but I have been studying "mixology" for the past year and do have all of the bar tools. I know how to make all of the classic cocktails. I would like a summer-themed cocktail menu of four to five drinks with clever names. I will put them on a framed menu on the counter in my outdoor kitchen and bar areas where I will make the drinks._

Sometimes the query might also include pasted text from another source or some other supporting documentation, like in the prompt below, which quoted a previous email chain (names were changed for privacy):

> _I would like to reach out to Bob to ask if he can do some part-time work for the \[…\] school site visits for my department starting in August through the end of September. Here is some background from an email exchange last year:_
> 
> _You bet! We’ll keep you posted, Bob!_
> 
> _John Smith, Ed.D. Department Administrator College & Career | Leadership Support Services_
> 
> _From: Bob Jones_
> 
> _Date: Monday, September 12, 2022 at 9:50 AM_
> 
> _To: John Smith_
> 
> _Subject: Re: Thank you!_
> 
> _Thank you John! I enjoyed the time I was able to spend with school leaders and with Andrew. With the new requirements and the possibility of more schools added to the three year cohort I would be available next year if you think I could help. Thank you for your confidence!_
> 
> _Bob Jones_
> 
> _Sent from my iPhone_
> 
> _On Sep 12, 2022, at 9:38 AM, John Smith wrote:_
> 
> _Good Morning, Bob, I wanted to thank you for your support of the \[school\] visits this year. Your expertise and experience as a former district leader really benefited the process. Even with some new requirements, it was one of our smoothest years ever with your help! I hope you enjoyed this work, too, and will consider leading visits again next year if you’re available. Thanks again for lending us your time in this area!_
> 
> _John_

**Pinpointing conversations require great effort from the user,** who needs to provide all the information necessary for a comprehensive response. They often contain well-specified, “engineered” prompts. However, unlike with other conversation types, the user rarely needs to spend time on query refinements and the result is a shorter, straight-to-the-point exchange.

Funneling conversations can sometimes be converted into pinpointing conversations if the bot asks the user detailed questions about their query, inviting them to specify all those details in their next prompt.

#### Tips for Designing AI Bots

Ask the user for **specific details** about their question, as well as about the format of the answer.

Consider giving users **examples of the information they could provide** in a prompt if the prompt is too vague or underspecified.

### Expanding Conversations

The expanding conversation usually starts with a **narrow topic that gets expanded**, often because the results from the original prompt were unsatisfactory (e.g., not up to date) or because the user decides they need more detail.

For example, in the following sequence, the user expanded his original query twice.

| **Example of Expanded Conversation**
 |
| --- |
| Start prompt

 | 

1.  _What is the cheapest airport to fly between Japan and Hong Kong?_

 |
| Expanded prompt:  
The user realized there was no cheapest airport based on ChatGPT’s response to question #1 and expanded his query.

 | 

2.  _What is the cheapest airline that flies between Japan and Hong Kong?_

 |
| Expanded prompt:  
In response to question #2, ChatGPT said that prices will vary depending on various factors, so the user expanded his query again.

 | 

3.  _Can you provide the full list of budget airlines between Hong Kong and Japan?_

 |

When the expanding conversations involved Bing, the expansions were usually selected from the suggested followup queries.

![Image 5](https://media.nngroup.com/media/editor/2023/11/07/bingchat_expanding.jpg)

_Bing could not provide a response to the query_ Who is running on the independent ticket for president_, so the participant broadened it by selecting a suggested followup question,_ Who are the potential candidates for the 2024 presidential election?

Expanding conversations remind us of what happens when people get zero search results for a search query: they often try to remove one of the criteria of their query in the hope that they will get something good enough. In such situations, [**search facets**](https://www.nngroup.com/articles/filters-vs-facets/) have been shown to help people by guiding them to ask queries that have one or more results.

Similarly, in the context of expanding conversations with AI, suggested followup prompts can show the user how to expand their question to get a meaningful answer. However, such **broader suggested followup prompts should have a different answer than the original question.**

For instance, one study participant used Bing Chat to look for _free events happening in Nashville this weekend_. Unsatisfied with the response she received, she expanded her query using a suggested followup _What are some popular free events in Nashville_. Disappointingly, she found the results were very similar. She commented:

> _I used one of the suggested follow up questions as the chatbot was not providing very specific information regarding Nashville events. It yielded pretty much identical results to the question I had posed. While it was nice to have the prompts below, I feel that they should maybe pose newer information._

#### Tips for Designers of AI Bots

When the bot is not able to provide an answer to the user’s query, **provide suggested followup prompts that relax some of the criteria in the user’s original question and return an answer**.

### Combinations of Several Types

Some conversations start as one type and then morph into a different one. For example, chiseling conversations may also have exploratory elements that build upon something that the bot has said.

One user had the following exchanges with ChatGPT; they combined chiseling and exploring conversations.

| **A Conversation Combining Chiseling and Exploring Prompts**
 |
| --- |
| Chiseling prompts:  
The user was trying to find information about various facets of day training with no reference to previous bot answers.

 | 

1.  _Tell me how to do well in day trading?_

 |
| 

2.  _Are there courses on day trading?_

 |
| 

3.  _Define day trading_

 |
| Exploring prompt:  
The question was triggered by the answer provided by the bot to question #3.

 | 

4.  _define the various techniques and tools mentioned \[in answer to question #3\]_

 |
| Exploring prompt:  
The question built upon the bot’s response to question #4.

 | 

5.  _how much do trading platforms and software \[mentioned in answer to question #4\] typically cost_

 |
| Chiseling prompt:  
The questions were unrelated to the previous prompts within the same conversation.

 | 

6.  _What are popular blogs about day trading?_

 |

Conversation Length Is Not a Success Indicator
----------------------------------------------

On average, **a conversation in our diary study included 3.6 participant-generated prompts** (95% confidence interval: 3.3–3.9); the median length was 3.

In general, the higher the number of attempts to do a task, the worse the usability. (For example, if the average number of submit attempts on a form was 3.6, that would mean that the form was pretty bad.)

However, with AI conversations, it is not the case that longer conversations necessarily represent more strenuous attempts at getting information from the bots**. In fact, there was no correlation between the length of the conversation and its helpfulness or trustworthiness ratings,** as collected from our study**.**

For certain types of conversations like funneling and pinpointing, **the length indicates how well-articulated the initial prompt was.** Long funneling chats start with vague prompts that need more detail. Short pinpointing chats begin with detailed prompts that already lay out all the requirements for an acceptable answer. In both such conversations, the user’s information need is constrained and fairly narrow — they need a specific piece of information or a specific output.

**For exploring and chiseling conversations, length is part of the conversation’s nature** and serves the user’s less well-defined information need. Exploring conversations require a back-and-forth between the bot and the human, with the human learning from the bot and choosing to go deeper and build upon the bot’s response. Chiseling conversations are also long because the goal is to acquire breadth in a subject, therefore requiring the user to ask multiple, loosely related questions about different aspects of given topic. In both these types of conversations, the goal is learning about a topic, and the conversation serves to define the user’s information need.

A special type of short conversation is the search query. This type of conversation was usually more likely to occur when people were still exploring the range of tasks that the AI bot could do for them.

Search queries were common with Bard; that is likely why **conversations with Bard were shorter than conversations with ChatGPT (p <0.001) or Bing (p<0.001).** It could be that Bard participants were primed by the prominence of Google as a search engine and tended to use Bard as a proxy for Google search.

![Image 6](https://media.nngroup.com/media/editor/2023/11/08/ai-convos_convo-length.png)

_Conversations with Bard were shorter than conversations with other bots. These differences were statistically significant. Many of the Bard conversations were one-prompt search queries._

A final word about the length of expanding conversations: they can be long or short, depending on how successful the user is in finding a satisfactory prompt that the bot can answer. They can also evolve in other kinds of conversations once the user finds the right way of formulating their query.

| **Taxonomy of AI Conversations by Information Need**
 |
| --- |
| **Narrow, Well-Defined Information Need**

 | **Broad, Undefined Information Need**

 |
| Funneling

Pinpointing

Exploring

Search queries

 | Exploring conversations: acquiring depth of knowledge

Chiseling conversations: acquiring breadth of knowledge

 |

Tips for Using Text-Based Generative-AI Bots
--------------------------------------------

There is no ideal length for all conversations. If the user has a clear, well-defined information need, then a good, detailed, pinpointing prompt will get them what they need fast.

But if the user’s goal is broad and less well-defined, then a single exchange will likely not be enough. The user can use the bot’s responses to learn — either through breadth or depth.

*   Specific information needs benefit from detailed, pinpointing prompts.
*   Adding phrasing such as _Ask me questions if you need additional information_ at the end of the user’s prompts can get the bot to help articulate the different constraints that the user may be working with.
*   For factual queries, users may (for now) be better off using a search engine instead of generative AI.

Recommendations for Designing the UX of Generative AI
-----------------------------------------------------

The structure of the generative-AI conversations is teaching us about what designers can do to improve the overall experience of generative AI and allow users to efficiently address their information needs.

Bots should attempt to use the length and the structure of the user’s prompt, as well as the complexity of the answer to **determine the conversation type early in the exchange and adjust behavior accordingly.** That is because different conversation types address different information needs and the support provided by the bot needs to be tailored to each need.

Specifically:

*   **Search queries** (i.e., prompts that are short, often incomplete sentences) can indicate that users are inexperienced with AI. These conversations can be treated as funneling conversations; the user can be asked further questions so that the bot can provide a satisfactory response. Alternatively, the bot can also offer the user the option to access search results for the same question.
*   **When bots receive vague, underspecified prompts (as in funneling conversations),** they should ask the user questions to **help them narrow down the conversation topic**. For example, for a prompt such as _best Mother’s Day gifts_, the bot can ask for specific information (e.g., age, hobbies, location) about the gift recipient. The bot can also offer example pinpointing prompts to help inexperienced users learn to use the AI.
*   In broad conversations (such as exploring or chiseling conversations) that require long or complex and nuanced responses, **suggested followup prompts should help the user learn**. While it may be difficult to establish what kind of intent the user has from a first prompt, bots could offer both depth-focused and breadth-focused suggested followup prompts.
*   In **expanding conversations,** which usually map onto situations when the bot was not able to provide an answer, the suggested followup prompts need to be slightly broader refinements that allow the user to find something useful, even if they will not precisely match their original need.
