Title: How I've run major projects

URL Source: https://www.benkuhn.net/pjm/

Markdown Content:
Contents

*   [Focus](https://www.benkuhn.net/pjm/#focus)
*   [Maintain a detailed plan for victory](https://www.benkuhn.net/pjm/#maintain-a-detailed-plan-for-victory)
*   [Run a fast OODA loop](https://www.benkuhn.net/pjm/#run-a-fast-ooda-loop)
*   [Overcommunicate](https://www.benkuhn.net/pjm/#overcommunicate)
*   [Break off subprojects](https://www.benkuhn.net/pjm/#break-off-subprojects)
*   [Have fun](https://www.benkuhn.net/pjm/#have-fun)
*   [Appendix: my project DRI starter kit](https://www.benkuhn.net/pjm/#appendix-my-project-dri-starter-kit)
    *   [Goals of this playbook](https://www.benkuhn.net/pjm/#goals-of-this-playbook)
    *   [Weekly meeting](https://www.benkuhn.net/pjm/#weekly-meeting)
    *   [Landing page / working doc](https://www.benkuhn.net/pjm/#landing-page--working-doc)
    *   [Plan / roadmap / milestones](https://www.benkuhn.net/pjm/#plan--roadmap--milestones)
    *   [Who’s working on what](https://www.benkuhn.net/pjm/#whos-working-on-what)
    *   [Slack norms](https://www.benkuhn.net/pjm/#slack-norms)
    *   [Weekly broadcast updates](https://www.benkuhn.net/pjm/#weekly-broadcast-updates)
    *   [Retrospectives](https://www.benkuhn.net/pjm/#retrospectives)

* * *

My few most productive individual weeks at Anthropic have all been “crisis project management:” coordinating major, time-sensitive implementation or debugging efforts.

In a company like Anthropic, excellent project management is an extremely high-leverage skill, and not just during crises: our work has tons of moving parts with complex, non-obvious interdependencies and hard schedule constraints, which means organizing them is a huge job, and can save weeks of delays if done right. Although a lot of the examples here come from crisis projects, most of the principles here are also the way I try to run any project, just more-so.

I think excellent project management is also _rarer than it needs to be_. During the crisis projects I didn’t feel like I was doing anything particularly impressive; mostly it felt like I was putting in a lot of work but doing things that felt relatively straightforward. On the other hand, I often see other people miss chances to do those things, maybe for lack of having seen a good playbook.

So here’s an attempt to describe my playbook for when I’m being intense about project management.

(I’ve described what I did as “coordinating” above, but that’s underselling it a bit; it mattered a lot for this playbook that I had enough technical context, and organizational trust, to autonomously make most prioritization decisions about the project. Sometimes we instead try to have the trusted decisionmakers not be highly involved in managing execution, and instead farm that out to a lower-context or less-trusted project manager to save the trusted decisionmaker time, but IMO this is usually a false economy for projects where it’s critical that they be executed well.)

Focus
-----

For each of the crisis management projects I completely cleared my schedule to focus on them, and ended up spending 6+ hours a day organizing them.

This is a bit unintuitive because I’m used to thinking of information processing as basically a free action. After all, you’re “just” moving info from place to place, not doing real work like coding, right? But if you add it all up—running meetings, pinging for updates, digesting Slack threads, pinging for updates again, thinking about what’s next, pinging for updates a third time, etc.—it’s surprisingly time-intensive.

Even more importantly than freeing up time, clearing my schedule made sure the project was the [top idea in my mind](https://paulgraham.com/top.html). If I don’t do that, it’s easy for me to let projects “go on autopilot,” where I keep them running but don’t proactively make time to think through things like whether we should change goals, add or drop priorities, or do other “non-obvious” things.

For non-crisis projects, it’s often not tenable (or the right prioritization) to spend 6+ hours a day project-managing; but it’s still the case that you can improve execution a lot if you focus and make them a top priority, e.g. by carving out dedicated time every day to check statuses, contemplate priorities, broadcast updates, and so on.

Maintain a detailed plan for victory
------------------------------------

A specific tool that I’ve found critical for staying oriented and updating quickly is a _detailed plan for victory_, i.e., a list of steps, as concrete as possible, that end with the goal being achieved.

The plan is important because whether or not we’re achieving the plan is the best way to figure out how well or badly things are going. Knowing how well or badly things are going is important because it tells me when to start asking for more support, cutting scope, escalating problems, and otherwise sounding more alarms. One of the most common megaproject failure modes is to _not freak out soon enough_, and having a concrete plan is the best antidote.

As a both positive and negative example of this, during a recent sprint to release a new implementation of a model, we took a detailed accounting of all the work we thought we had to do to launch.

*   On the plus side, this made it clear three months before launch that things were going to be _very_ tight, and this enabled us to ask for help from another team, who loaned us someone who sped up the project a fair amount.
*   On the minus side, we also massively underestimated a few components of the project, and because of this, we still ended up very crunched at the end.

As the above example shows, having a plan can’t completely save you if you underestimate how long all the steps in the plan will take. But it certainly helps! My sense is that the main things that would have helped even more in the above case were:

*   We were inexperienced at estimating tasks, especially tasks related to new model implementations (which most people on the team were too new to have done before), and we were too cowardly to add the requisite amount of “slop” to our plan.
*   We didn’t check in frequently enough against the plan once we made it, or sound the alarm early enough when we went off-plan.

Run a fast OODA loop
--------------------

OODA stands for “observe, orient, decide, act”—in other words, the process by which you _update your plans and behavior based on new information_.

Most of the large projects I’ve worked on have been characterized by incomplete information:

*   Our cluster’s networking is bad, but we don’t understand why.
*   We have a correctness bug but we don’t know where it is.
*   We need to rewrite the system but we’re not totally sure what the rewrite should look like.

In fact, I’d make a stronger claim: usually getting complete information _was the hard part of the project_, and took up a substantial fraction of the overall critical-path timeline.

For example, let’s take a recent project to kick off a training run. The critical path probably looked something like:

1.  Chips for the training run are delivered
2.  We run some tests
3.  We discover one aspect of performance is unexpectedly poor
4.  We escalate the problem with our compute partner
5.  Compute partner staffs a large debugging effort
6.  We realize we had given our compute partner an outdated benchmark that is causing them to target the wrong improvements
7.  Compute partner switches benchmark and prioritizes different improvements
8.  We share our benchmarks with compute partner so they can run the exact same code as us
9.  Compute partner rolls out improvements
10.  We test the improvements
11.  Performance is still poor and we tell them that
12.  Repeat steps 8-10 until eventually it’s good enough

Practically all of these steps are about information-processing, not writing code! Even the step where the compute partner debugged the problems on their side was itself constrained by information processing speed, since there were tens of people working on the debugging effort and coordinating / sharing info between them was difficult. Overall, the project timeline was strongly constrained by how quickly information could round-trip from our compute partner’s large-scale debugging effort, through their tech lead, me, and Anthropic’s large-scale debugging effort.

This pattern generalizes to most projects I’ve been a part of, and as a result, one of my most productive project management habits is to try to run the fastest OODA loop that I can.

A few specific things that I’ve found help:

*   **Spend time on it:** running OODA loops takes time, and is one of the primary reasons that, as mentioned above, I usually spend 6+ hours a day on running a megaproject if it’s in crisis mode.
*   **Communicate uncomfortably much:** For the training run debugging, to reduce the round-trip time between orgs as much as possible, I had multiple daily calls with my counterpart at our compute partner (9am and 6pm). For the model implementation effort, I was basically constantly bouncing between different groups of debuggers, asking for updates and processing them.
*   **Track and prioritize the biggest open questions:** For most big projects I’ve maintained a living doc with a ranked list of all my _biggest open questions_ about the project. Resolving or de-risking these uncertainties basically turns into the project’s priority list.  
    Ideally, there are enough people working on the project that we can work on resolving multiple of the uncertainties in parallel, since that’s one of the best ways to speed things up. (And for a project in “crisis mode,” if we have more top priorities than we can parallel-path with the current set of people working on the problem, that’s also a good test for whether it’s time to pull in more folks.)
*   **Step back and reorient frequently:** Other than asking for updates, the main thing I spend time on was _reorienting_—looking at our list of priorities, asking myself whether they should still be the top priorities, then looking at what people were working on, and making sure those things were attacking the top priorities. I probably reviewed the project’s priorities multiple times a day as well, although I often didn’t make changes as a result.
    *   (Note that it is possible to change what people are working on too often, since switching tasks is costly. Parallelizing work on the top few priorities, as mentioned above, helps with this, since if you decide that priority #3 is now #1, but there are 2 people working on each, then nobody has to switch tasks. The thing that kills you is when _no one_ is working on the new priority #1.)

Overcommunicate
---------------

It’s not just enough for me personally to be running a fast OODA loop—in a large group, _everyone_ needs to be autonomously making frequent, high-quality, _local_ prioritization decisions, without needing a round-trip through me. To get there, they need to be ambiently aware of:

1.  what else is going on around them, so they can coordinate and update on new info quickly (“oh, we’re planning to kick off the next derisking run in three days, so I have to have my new RL environment ready and tested by then”)
2.  how their goal fits into the overall project, so they can make correct decisions about the details of their approach (“we’re trying to scale up as much as possible right now, so this direction isn’t valuable to pursue since it could never provide the scale of data we need”)

I’ve usually found that to create the right level of ambient awareness, I have to repeat the same things way more often than I intuitively expect. This is roughly the same “communicate uncomfortably much” principle above, but applied to broadcasts and not just 1:1 conversations with people.

For example, although the first team I managed at Anthropic started with a daily asynchronous standup, we found that synchronous meetings were much more effective for creating common knowledge and reorienting, so we moved to a twice-weekly synchronous standup, which probably qualified as “uncomfortably much” synchronous communication for Anthropic at the time.

Break off subprojects
---------------------

Once a project gets over maybe 10 people, I can’t track everything myself in enough detail to project-manage the entire thing myself. At this point, it becomes critical to delegate.

Here I mean delegating the _project management_, not just the execution (that’s what I’d be delegating to the first 10 people). This is the point where I need other people to help split up the work, monitor and communicate progress, escalate blockers, etc.

A few things I try to keep in mind when delegating project management:

*   The ideal unit of delegation is a crisp, _simple_, high-level goal, with limited overlap with other workstreams. (This is as opposed to, e.g., a list of tasks like “see if X helps.“) Good examples: “get X training technique working over Y networking protocol at Z throughput,” “get identical evals between model implementations A and B.” Bad examples: “follow this 10-step checklist that we hope results in training working,” “try these 3 techniques for debugging the loss eval.”
*   The best project-managers are often _not_ the strongest technical ICs. Instead the most important traits are that they’re highly organized and great at staying laser focused on end goals, perhaps to the point of being annoying about it. IC depth helps and I’ll never say no to it, but it’s not what I’d optimize for.
*   People running subprojects are probably also doing a lot of the same stuff I do, in particular e.g. spending a lot of time on it. That means they’ll take a substantial hit to their IC productivity. This is expected, and is often worth it. “Direction is more important than magnitude”—it’s usually better to have a lower-velocity project that works on the right things, than a higher-velocity one that’s pointed at the wrong goal.

One of my favorite things to make delegation easier is to _keep goals simple_—if they can fit in a Slack message while still crisply describing a path to the desired end state, then the people working on the goal will be much more able to prioritize autonomously, and point their work at the real end goal rather than doing something that turns out to be useless for some reason they didn’t think about.

“Keep goals simple” doesn’t have to mean “do less”—the best way to keep goals simple is to _find the latent structure that enables a clean recursive decomposition into subgoals_. This often requires a deceptive amount of work—both cognitive and hands-on-keyboard—to identify the right intermediate goals, but I’ve found that it pays off immensely by clarifying what’s important to work on.

Have fun
--------

Some of my favorite memories of Anthropic are of helping out with these big projects. While they can be intense, it’s also really inspiring to see how our team comes together, and the feeling of being part of a big team of truly excellent people cooking something ambitious together can be really magical! So I try to enjoy the chaos :)

* * *

Appendix: my project DRI starter kit
------------------------------------

_Here’s the internal doc I share with folks on my team who are getting into being responsible for large projects._

So you’re the DRI of a project (or part of one). Concretely, what do you do to “be DRI”?

This doc is my suggested “starter kit” answer to that question. The habits and rituals described here aren’t perfect for every situation, but they’re lightweight and broadly helpful. I suggest you use them as a starting point for iteration: try them out, then adjust as necessary. This is an SL init; the RL is your job :)

### Goals of this playbook

The goal is to help you do your job as DRI—

*   Make your project go quickly:
    *   Participants deeply understand the root goal and can autonomously choose the most important next things to work on
    *   People have “situational awareness” of what other people are working on, learn about relevant updates quickly, and coordinate quickly when needed
    *   People get quick feedback on their work
    *   If things aren’t going fast enough, you (the DRI) can notice and course-correct quickly
*   “Play well with others:”
    *   Observers can figure out where to go to follow along
    *   Adjacent or intersecting people/projects don’t miss important updates or get caught by surprise
    *   People notice quickly if the project is behind or off-track, and can identify opportunities to help

—without adding too much overhead:

*   <1 hour of setup to make a working doc, schedule a weekly meeting, etc.
*   30 min/week of meetings
*   15-30 min/week to write an update

(Note: _being DRI_ will still unavoidably add some overhead—e.g. you’ll have to track what other people are doing, delegate work, unblock people, set and communicate goals, etc. The goal is specifically for the _process/paperwork_ to be minimal.)

### Weekly meeting

You should schedule at least one 30-minute weekly meeting with everyone working on the project.

The goal of this meeting is to (1) be a backstop for any coordination that needs to happen and didn’t happen asynchronously; (2) be an efficient way to create [common knowledge](https://en.wikipedia.org/wiki/Common_knowledge_%28logic%29) of goals, updates, etc.; (3) help you track whether things are going well.

*   Starter-kit agenda:
    *   \[5m\] DRI reviews major updates from last week and sets goals for next week
    *   \[10m\] Silent write and comment on discussion topics
    *   \[10m\] Synchronous discussion of most important things not addressed during silent write
*   Signs that more meetings might help (e.g. a second weekly standup):
    *   you have a very tight deadline and can’t afford to lose time
    *   people aren’t working on the most important thing
    *   people need feedback frequently
    *   people step on each others’ toes or miss opportunities to help each other out
    *   if you just like hanging out with each other :)

### Landing page / working doc

It’s really helpful for discoverability and wayfinding to have a single “master doc” with all the most important info about a project. As you loop more people in, they can read the doc to get up to speed. And anyone who thinks “I wonder how X is going” can stop by there to find out.

Create a doc for your workstream with:

*   A [go/ link](https://www.golinks.io/) in the name (if a subproject, maybe use go/project/subproject)
    *   → This makes it easier to find quickly (search is kinda rough)
*   A clear description of a **concrete top level goal** and how it fits into broader goals
    *   → This is critical info for participants, so they can autonomously prioritize the most important things; and for observers, so that they know what outcome to expect.
*   **Staffing:** A list of people working on the project, your name as the DRI, and a link to the slack channel that’s being used for discussion
*   **Links:** A short list of relevant links at the top (work trackers, the project’s Slack channel, major design docs, etc.). If needed, a longer “docs / see also” section later links to relevant docs.
    *   → It’s really easy to lose track of relevant docs otherwise!
*   A **roadmap** section with intermediate goals and target dates
    *   → See the [section on plans](https://www.benkuhn.net/pjm/#plan--roadmap--milestones); these will help people understand what the overall shape of the project is expected to be.
*   A section for “running notes” containing meeting notes from your weekly meetings (and any other ad-hoc meetings) and [broadcast updates](https://www.benkuhn.net/pjm/#weekly-broadcast-updates)
    *   → This really helps observers and new-joiners get up to speed!
*   I like maintaining a list of **important open questions / uncertainties/ risks** and updating it over time. This helps me stay focused on removing risk from the project as quickly as possible.

If it’s part of a larger project, your doc should be nested within the larger project’s working doc.

If this ends up being too much for one doc, you can fork these out into sub-docs (esp. running notes and updates).

### Plan / roadmap / milestones

*   In your working doc, include a section with some intermediate goals and dates by which you hope to accomplish them.
    *   → This is helpful mostly for noticing you’re off track or behind without getting frog-boiled.
    *   → Or noticing when you need to make a direction change because the intermediate goals don’t seem good anymore.
*   You might feel some pressure to add false certainty or precision, but avoid this and be honest about your uncertainty instead. For a lot of research projects it’s hard to plan more than a couple weeks ahead. You can make the milestones fuzzier / more aspirational beyond that, or just drop them.
    *   I often find it helpful to phrase milestones in probabilitis and distributions (e.g. “my 90% confidence interval for this date is X-Y” or “I think there’s a 75% chance this technique works”)

### Who’s working on what

*   You should have something somewhere that describes what people are working on.
*   The minimum viable version of this is a list of what people are working on in your working doc.
    *   If you end up with a large set of tasks and a big backlog, maybe use a checklist and/or move to a subdoc.
*   **Stack rank your work list.** It’s really important for people to understand priorities!
*   If there’s more different people/TODOs, I suggest using some app to make a kanban board with “backlog” / “up next” / “in progress” / “done” columns.
    *   This is probably most helpful for more deterministic/plannable projects where there’s a clear backlog + set of future tasks, and a lot of things you need to remember to do.
*   If you have an external task tracker, link it in the wiki section of the working doc.

### Slack norms

*   Have conversations about the project in a Slack channel (not DMs).
    *   Reference the channel in your working doc.
    *   Link the working doc in the Slack channel bookmarks.
*   Cross-post notebook posts and experiment write-ups into the channel so observers don’t have to follow tons of notebook channels.
*   **Do not use DMs.** These make it hard to make info discoverable or share it further.
    *   If people send you important stuff in a DM, ask them to put it in the project channel.
    *   If you need confidentiality, make a private channel.
*   **Avoid centithreads.** Most ≥10-message Slack threads would be better as a ~5-minute Tuple.
    *   (This is hard to do with people who are in tons and tons of meetings like execs. But you should try to do it for others.)
    *   If you end up with a centithread, assume nobody will read it; post a summary back to the channel afterwards.
*   Bias towards fewer, larger, noisier channels. The right time to create a channel is when discussion is either not happening, or getting lost.
    *   → Too many slack channels makes it harder to manage membership, decide where to put things, or find where discussion is happening.
*   Channel organization and membership matters. Invest in routing conversations to the right place and curating the channel “architecture.”

### Weekly broadcast updates

*   Once a week, probably either just before or just after your weekly meeting, write up a **brief** update for a broader audience with:
    *   The overall vibe
    *   What’s changed since last update
    *   What’s coming up next
*   When writing these updates, optimize for **signal to noise ratio**.
    *   Err towards concision
    *   No “we worked on X”—tell me “we accomplished Y” or “we learned Z”
    *   Remember your audience (= people not familiar with the project)
    *   State things crisply and concretely (“X improves eval Y by Z points,” not “we got X working”)
    *   Leave out anything that’s not actionable—you don’t need to be exhaustive
*   Post the update in your project Slack channel, and cross-post it to other relevant channels (e.g. a larger “megaproject” channel) if necessary.
    *   If your project is part of a larger megaproject, these updates might feed into something broader like a weekly meeting of DRIs or an aggregated status update.

### Retrospectives

*   Every so often, step back and ask “how could the last X weeks have gone better?”
    *   Frequency depends on how much there is going on—every 2 weeks is good if there’s a lot, maybe every 4-8 weeks for smaller projects
*   Suggested meeting format
    *   Friday afternoon
    *   \[13 min\] Async brainstorm 2 lists of items: “what went well” / “what we could improve”
    *   \[2 min\] Dedupe topics and emoji vote by putting :heavy\_plus\_sign: next to ones you agree with
    *   Sort “what we could improve” by highest votes
    *   \[10 min\] Synchronous discussion of top points (either highest voted or flagged by DRI); figure out action items

_Thanks to Kelley Rivoire for many thoughtful comments on a draft!_
