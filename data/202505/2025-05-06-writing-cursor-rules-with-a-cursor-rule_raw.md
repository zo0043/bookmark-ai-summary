Title: Writing Cursor Rules with a Cursor Rule | Adithyan

URL Source: https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule

Markdown Content:
Writing Cursor Rules with a Cursor Rule | Adithyan
===============

[Adithyan](https://www.adithyan.io/)

[Blog](https://www.adithyan.io/blog)Subscribe

More

Writing Cursor Rules with a Cursor Rule
=======================================

Apr 10, 2025

I spend most of my coding time in Cursor. It's a fantastic tool for LLM assisted coding.

But coding with LLMs has a specific quirk: they possess strong **contextual memory** but lack **episodic memory**.

In simpler words, they recall information within a single conversation but forget everything once a new chat session begins. No learnings from previous chats on how you like things. No accumulation of instituation quirks and knowledge.

Think of it like working with a brilliant assistant who has amnesia. Every day, you repeat the same instructions:

*   "Remember, we use camelCase here."
*   "Our shared utilities go in the `lib` folder with this specific structure."
*   "This is how the backend API expects requests."
*   "We use this specific folder structure for our projects."

If you use Cursor often, this should sound familiar. You constantly nudge the AI back toward your project's standards and personal preferences. If you're already nodding in agreement and (from the title) understand where I'm going with this, you probably just want the meta cursor rule template that I use. In that case, you can jump straight to [The Plug-and-Play Meta-Cursor Rule](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#the-what-a-plug-and-play-meta-cursor-rule).

If you're still unsure what I'm talking about, I'll explain in more detail why this is necessary, how we solve the problem with cursor rules, and how to create cursor rules efficiently using a meta-rule approach.

![Image 1: A visual representation of cursor rules showing how they provide consistent instructions to AI across different chat sessions](https://www.adithyan.io/_next/image?url=%2Fblog%2Fwriting-cursor-rules-with-a-cursor-rule%2Frules.png&w=1920&q=75)

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#why-how-then-what)Why, How, Then What
-------------------------------------------------------------------------------------------------------------

My approach when writing posts in this blog is to help others understand _why_ we need to do something and _how_ we might go about creating a solution.

The _what_ (the specific implementation or solution) becomes much more obvious after understanding the _why_ and _how_. Especially the _why_!

I personally think you will come up with a better solution (_what_) than the one I provide that is specific to your project and personal preferences.

So let's start with the _why_.

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#why-you-need-systems-for-ai)Why You Need Systems for AI
-------------------------------------------------------------------------------------------------------------------------------

Imagine you're managing several projects, each with a brilliant developer assigned.

Here's the catch: every morning, all your developers wake up with complete amnesia. They forget your coding conventions, project architecture, yesterday's discussions, and how their work connects with other projects.

Each day, you repeat the same explanations:

*   "We use camelCase in this project but snake\_case in that one."
*   "The authentication flow works like this, as I explained yesterday."
*   "Your API needs to match the schema your colleague is expecting."

What would you do to stop this endless cycle of repetition?

**You would build systems!**

*   Documentation
*   Style guides
*   Architecture diagrams
*   Code templates

These ensure your amnesiac developers can quickly regain context and maintain consistency across projects, allowing you to focus on solving new problems instead of repeating old explanations.

Now, apply this to coding with AI.

We work with intelligent LLMs that are powerful but start fresh in every new chat. They have no memory of your preferences, how you structure your projects, how you like things done, or the institutional knowledge you've accumulated.

So, you end up repeating yourself. How do you solve this?

**Exactly the same way: You build systems!**

You need a way to instantly bring each LLM you work with up to speed.

⚠️

**Caveat:** For quick, disposable one-off scripts you won't reuse, this might not matter much and I actually don't recommend you create rules for them.

However, for serious applications built over time, growing brick by brick over weeks and months, it absolutely matters. I can tell you this from personal experience. You waste valuable time re-explaining.

Without a system to give the AI this information, you'll keep wasting time on repetitive explanations. Fortunately, Cursor provides built-in ways to create such systems. Let's look at one specific solution.

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#how-do-we-do-this-cursor-rules)How Do We Do This? Cursor Rules
--------------------------------------------------------------------------------------------------------------------------------

Cursor Rules are permanent instruction documents for the AI within your projects.

For each git repository, you create rule files (stored in `.cursor/rules/`) that tell the LLM how to work with your specific codebase. Different repositories can have different rules, and each repository typically has multiple rules addressing various aspects of the project.

These rules solve the AI's memory gap. They act as instruction documents, teaching the AI your project's patterns and preferences. When Cursor sees a file matching a rule's pattern (`glob`), it loads that knowledge automatically. This creates consistency every time you chat with the AI.

I've provided my own summary here, but you can [read the official documentation](https://docs.cursor.com/context/rules-for-ai) for more details. It should take no more than five minutes to read, and I highly recommend it.

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#creating-rules-without-the-friction)Creating Rules Without the Friction
--------------------------------------------------------------------------------------------------------------------------------

The concept sounds simple: read the documentation and write some `.mdc` files.

But let's be honest. Many developers understand the benefits but hesitate because creating rules feels like extra work. It adds friction.

Here's something I've noticed both with myself and when explaining this to friends: We all get the concept, we all see the long-term benefit, but we rarely implement it. Even when I know a cursor rule would save me time in the long run, I often don't create one because writing it feels like a hurdle.

So how do you overcome this resistance? **You build a system to build the system itself.**

I know it sounds meta, but that's exactly what we need: **Use AI to write the rules for itself.**

How? By creating a **meta-cursor rule**.

This means creating _one_ rule that serves as a template for writing _all other_ rules. It defines the structure and content all your rules should follow.

Once you have this meta-rule, the process becomes simple:

1.  Notice a pattern you want to codify
2.  Open the Cursor chat
3.  Point the AI to your meta-rule (e.g., "Using the `cursor-rule-creation.mdc` guide...")
4.  Ask it to write a new rule based on your conversation (e.g., "write a rule for our component structure based on this chat")

In practice, I personally use this in two common scenarios:

*   **During a long coding session**: After spending hours working with the AI on a specific pattern or convention, I'll realize, "I don't want to explain this again next time." I simply tell the AI: "Based on everything we've discussed so far and following the meta-cursor rule pattern, please create a rule for this approach and name it appropriately." The AI drafts it, and I save it for future use.
    
*   **When I have a specific idea**: Sometimes I already know exactly what pattern I want to codify. I'll open a chat, briefly describe my intention, point to the meta-cursor rule, and ask the AI to write a targeted rule. It's like dictating my thoughts directly into a structured document.
    

This approach drastically reduces the effort needed to build your rule library. The AI follows your template to generate well-structured drafts that you can quickly save and use.

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#the-what-a-plug-and-play-meta-cursor-rule)The What: A Plug-and-Play Meta-Cursor Rule
--------------------------------------------------------------------------------------------------------------------------------

So finally, here's the "what" part of the equation - my actual meta-cursor rule that I use across all my repositories. This is a plug-and-play solution you can copy directly into your own projects.

Simply save this as `.cursor/rules/cursor-rule-creation.mdc` (or any similar name you prefer) and it will immediately work as your foundation for creating all other rules:

`````
---
title: Creating Effective Cursor Project Rules
description: Comprehensive guidelines for creating well-structured Cursor Project Rules (.mdc files) to help AI understand your codebase and coding style.
glob: "**/*.{mdc}"
alwaysApply: true
---

# Creating Effective Cursor Project Rules

This meta-rule provides comprehensive guidance on creating effective Cursor Project Rules. These are `.mdc` files stored in your project's `.cursor/rules` directory that help the AI understand your specific codebase, conventions, and preferences. Following these guidelines will help you create rules that are easily understood by both humans and the AI, leading to more consistent and helpful AI interactions.

## What are Cursor Project Rules?

Project Rules are the recommended way to provide persistent, project-specific instructions to Cursor's AI. They live alongside your code (in `.cursor/rules/`) and are automatically activated when files matching their defined patterns (`glob`) are referenced in chat or other AI features.

Think of them as a structured knowledge base for your project, teaching the AI:

* Coding conventions and style guides
* Architectural patterns
* API usage and interfaces
* Domain-specific knowledge
* Your personal or team preferences

## Rule File Structure

While flexible, a well-structured rule file improves clarity for both humans and the AI. Consider including the following components:

### 1. YAML Frontmatter (Crucial)

**Placement:** The YAML frontmatter block (`--- ... ---`) **must** be the absolute first content in the file. Any leading spaces, lines, or characters can prevent the rule from loading correctly.

```yaml
---
title: Brief Title of the Rule (e.g., React Component Guidelines)
description: Guidelines for [what this rule covers and its purpose, e.g., structuring functional React components]
glob: "[pattern/to/match/files/**/*.{ext}]" # See examples below
alwaysApply: false # Optional: Set to true to always include this rule
---
```

* **`title`**: A clear, descriptive title (5-7 words recommended).
* **`description`**: A concise, semantic description. Start with phrases like "Guidelines for..." or "Instructions on..." This likely helps Cursor automatically select the most relevant rule when multiple match.
* **`glob`**: File pattern(s) that trigger this rule's automatic activation. Be specific.
 * Examples:
 _ `src/components/**/_.{tsx,jsx}` (React components)
 _ `src/server/api/**/_.ts` (Server API routes)
 _ `_.{json,yaml,yml}` (Configuration files)
 _ `src/utils/!(test).ts` (Utility files, excluding tests)
 _ `{package.json,pnpm-lock.yaml}` (Specific root files)
* **`alwaysApply`** (Optional, defaults to `false`): If `true`, the rule is included in context regardless of the files being referenced.

### 2. Content Sections (Recommended Structure)

Organize the rule's content logically. Using markdown headings (`##`, `###`) is recommended.

#### Introduction / Problem

* Briefly explain _what_ problem this rule solves or _what_ pattern it defines.
* Explain *why* this pattern/convention is important for this project.
* Mention _when_ this rule is typically relevant.

#### Pattern Description

* Clearly document the recommended pattern(s) or conventions.
* Use text explanations combined with clear code examples (using language-specific fenced code blocks).
* Highlight key components, functions, or concepts involved.
* If applicable, link to other relevant rules: `[See API Conventions](mdc:api-conventions.mdc)`

#### Implementation Steps (If Applicable)

* Provide a clear, step-by-step guide if the rule describes a process.
* Use ordered lists.
* Identify decision points or variations.

#### Real-World Examples (Highly Recommended)

* Link to _actual code_ in the current repository using relative paths: `[Example Button](mdc:../src/components/ui/Button.tsx)`.
* Briefly explain *why* the linked code is a good example of the rule.
* Keep examples focused on the rule being described.

#### Common Pitfalls / Anti-Patterns

* List common mistakes or deviations related to this rule.
* Explain how to recognize these issues.
* Suggest how to fix or avoid them.

**Note:** Adapt this structure based on the rule's complexity. Simpler rules might only need frontmatter and a brief description or a few key points.

## Advanced Features

### File References (`@file`)

Include critical context files directly within your rule using the `@file` directive. Place these *after* the frontmatter but ideally *before* the main content.

```markdown
@file ../tsconfig.json
@file ../package.json
@file ./docs/ARCHITECTURE.md
```

* Use relative paths from the rule file's location (`.cursor/rules/`).
* These files will be added to the context *whenever this rule is activated*, providing consistent background information to the AI.
* Use sparingly for essential files (configs, core types, architectural overviews) to avoid excessive context.

### Code Blocks

Always use fenced code blocks with language specifiers for correct rendering and potential syntax highlighting by the AI:

````markdown
```typescript
function greet(name: string): string {
 // Correctly formatted TypeScript
 return `Hello, ${name}!`;
}
```
````

## Rule Activation and Interaction

* **Automatic Activation:** Rules are primarily activated automatically when files matching their `glob` pattern are included in the context (e.g., opened file, @-referenced files, files included in `@codebase` search results).
* **Semantic Selection:** The `description` field likely helps Cursor choose the _most relevant_ rule if multiple rules match the same file via their `glob` patterns.
* **Manual Activation:** You can explicitly include specific rules in a chat prompt using the `@Cursor Rules` symbol (e.g., `@Cursor Rules(react-component-guide.mdc)`).
* **Specificity:** More specific `glob` patterns are generally preferred to avoid unintended rule overlaps. If rules overlap, the exact selection logic isn't documented, but clearer descriptions and more specific globs likely lead to better results.
* **Modularity:** Break down complex domains (like your entire backend) into smaller, more focused rules (e.g., `api-routing.mdc`, `database-models.mdc`, `auth-middleware.mdc`) rather than creating one monolithic rule.

## Best Practices

* **Start Simple, Iterate:** Don't aim for perfection immediately. Start with basic rules for core conventions and add/refine them over time as you observe the AI's behavior and identify gaps.
* **Be Specific but Flexible:** Provide clear, actionable guidance with concrete examples. Use recommending language ("prefer", "consider", "typically") rather than overly rigid commands ("must", "always") unless a strict convention is required. Explain the *why* behind rules.
* **Focus on Patterns:** Rules should define repeatable patterns, conventions, or project knowledge, not fix one-off bugs.
* **Keep Rules Updated:** Regularly review rules. Update them when conventions change or code evolves. *Delete* rules that become obsolete or if the AI consistently follows the pattern without the rule.
* **Trust the LLM (to an extent):** While rules provide guidance, allow the LLM some flexibility. It can often infer patterns from the existing codebase, especially as it grows.
* **Troubleshooting:** If rules aren't activating as expected, double-check:
 * The YAML frontmatter is the _absolute first_ content in the file.
 _ The `glob` pattern correctly matches the intended files.
 _ File paths in `@file` directives are correct.
 _ The `.mdc` file encoding is standard (UTF-8). 

## Team Collaboration

_ **Version Control:** Commit the `.cursor/rules` directory to your repository so rules are shared and versioned alongside your code.
* **Conventions:** Establish team conventions for naming, structuring, and updating rules.
* **Review Process:** Consider code reviews for changes to important rules.
* **Onboarding:** Use rules as living documentation to help onboard new team members to project standards.
* **Shared vs. Personal:** If needed, establish naming conventions (e.g., `_personal-_.mdc`) and potentially use `.gitignore` within `.cursor/rules` to separate team-wide rules from personal experimental ones.

## Full Rule Example

```markdown
---
title: React Functional Component Structure
description: Guidelines for structuring functional React components using TypeScript, including prop definitions, state management, and hook usage.
glob: "src/components/**/_.tsx"
alwaysApply: false
---

@file ../../tsconfig.json
@file ../../tailwind.config.js

# React Functional Component Structure

## Introduction

This rule defines the standard structure for functional React components in this project to ensure consistency, readability, and maintainability. We use TypeScript for type safety and prefer hooks for state and side effects.

## Pattern Description

Components should generally follow this order:

1. `'use client'` directive (if needed)
2. Imports (React, libs, internal, types, styles)
3. Props interface definition (`ComponentNameProps`)
4. Component function definition (`function ComponentName(...)`)
5. State hooks (`useState`)
6. Other hooks (`useMemo`, `useCallback`, `useEffect`, custom hooks)
7. Helper functions (defined outside or memoized inside)
8. `useEffect` blocks
9. Return statement (JSX)

```typescript
'use client' // Only if browser APIs or hooks like useState/useEffect are needed

import React, { useState, useEffect, useCallback } from 'react';
import { cn } from '@/lib/utils'; // Example internal utility
import { type VariantProps, cva } from 'class-variance-authority';

// Define props interface
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
 isLoading?: boolean;
}

// Define component
function Button({ className, variant, size, isLoading, children, ...props }: ButtonProps): React.ReactElement {
 // State hooks
 const [isMounted, setIsMounted] = useState(false);

 // Other hooks
 const handleClick = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
 if (isLoading) {
 event.preventDefault();
 return;
 }
 props.onClick?.(event);
 }, [isLoading, props.onClick]);

 // Effects
 useEffect(() => {
 setIsMounted(true);
 }, []);

 // Conditional rendering logic can go here

 // Return JSX
 return (
 <button
 className={cn(buttonVariants({ variant, size, className }))}
 disabled={isLoading}
 onClick={handleClick}
 {...props}
 >
 {isLoading ? 'Loading...' : children}
 </button>
 );
}

// Example variant definition (could be in the same file or imported)
const buttonVariants = cva(
 'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
 {
 variants: {
 variant: {
 default: 'bg-primary text-primary-foreground hover:bg-primary/90',
 // ... other variants
 },
 size: {
 default: 'h-10 py-2 px-4',
 // ... other sizes
 },
 },
 defaultVariants: {
 variant: 'default',
 size: 'default',
 },
 }
);

export { Button, buttonVariants }; // Prefer named exports
```

## Implementation Steps

1. Define a clear `interface` for props.
2. Use standard React hooks for state and side effects.
3. Keep components focused on a single responsibility.
4. Use named exports for components.

## Real-World Examples

* [Standard Button Component](mdc:../src/components/ui/button.tsx)
* [Complex Card Component](mdc:../src/components/ui/card.tsx)

## Common Pitfalls

* Forgetting `'use client'` when using hooks like `useState` or `useEffect`.
* Defining helper functions directly inside the component body without `useCallback` (can cause unnecessary re-renders).
* Overly complex components; consider breaking them down.
* Not using TypeScript for props or state.

```

## Minimal Rule Template

Use this as a quick starting point for new rules:

```markdown
---
title: [Rule Name]
description: Guidelines for [purpose]
glob: "[pattern]"
alwaysApply: false
---

# [Rule Name]

## Introduction / Problem

[Why this rule exists and what problem it solves.]

## Pattern Description

[Explain the pattern with code examples.]

## Real-World Examples

* [Link to code](mdc:../path/to/example.ts)

## Common Pitfalls

* [Common mistake 1]
* [Common mistake 2]

```
`````

Copy

[](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule#building-systems-pays-off)Building Systems Pays Off
---------------------------------------------------------------------------------------------------------------------------

Using a meta-rule like this one helps you build systems for your AI interactions. You teach the AI how to create its own documentation consistently.

This creates a positive feedback loop, boosting consistency in your projects and saving you significant time. The small upfront investment in defining a good meta-rule pays off quickly as you spend less time repeating instructions and more time building.

As AI becomes increasingly integrated into our development workflows, those who create effective systems will gain a significant advantage.

I encourage you to try this approach in your own projects. The entire blog post is my own interpretation of what Cursor rule is but the actual official documentation itself is not too long so I highly recommend you also read the [original documentation from Cursor](https://docs.cursor.com/context/rules-for-ai) too.

Start small with one or two critical patterns, and watch how quickly your AI collaboration improves. And if you develop your own meta-rule variations, I'd love to hear about them!

© 2025 [Adithyan](https://x.com/adithyan_ai)

Subscribe|

[](https://x.com/adithyan_ai)[](https://github.com/AdithyanI)[](https://www.instagram.com/adithyan.ai/)[](https://www.linkedin.com/in/adithyan-ai/)[](mailto:adi@aipodcast.ing)[](https://www.adithyan.io/rss.xml)
