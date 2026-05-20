"""Prompt templates for example chains."""

BLOG_OUTLINE = """You are a writing planner.

Topic: {topic}

Create a short numbered outline (4 bullets max) for a blog post on this topic.
Return only the outline."""

BLOG_DRAFT = """You are a writer.

Topic: {topic}

Use this outline:
{previous_output}

Write a 2–3 sentence draft paragraph. Plain text only."""

BLOG_EDIT = """You are an editor.

Improve clarity and flow. Keep it under 80 words.
You may use one short markdown bold phrase for emphasis.

Draft to edit:
{previous_output}

Return only the polished paragraph."""

SUMMARIZE = """Summarize the following in one sentence:

{text}"""
