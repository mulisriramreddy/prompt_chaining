#!/usr/bin/env python3
"""
Prompt chaining in one file — run: python3 simple_chain.py
"""

# --- Fake LLM (no API key) ---


def mock_llm(prompt: str) -> str:
    p = prompt.lower()
    if "summarize" in p:
        return "Chaining = many LLM calls where output feeds the next prompt."
    if "beginner" in p or "explain this" in p:
        return "Think of it as an assembly line: plan, then write, then polish."
    if "3-bullet" in p or "bullet outline" in p:
        return "1. What is chaining\n2. Why use it\n3. Quick example"
    if "2 sentences" in p:
        return "Chaining runs prompts in order. Each step uses the last answer."
    if "polish" in p or "under 60" in p:
        return "**Chaining** runs prompts in order; each step uses the prior answer."
    return "(mock) " + prompt[:60] + "..."


# --- Chain runner ---


def run_chain(llm, steps, **start_values):
    """
    steps: list of (name, template_string)
    start_values: e.g. topic="...", text="..."
    Returns list of (step_name, output) and final text.
    """
    context = dict(start_values)
    results = []
    previous = ""

    for name, template in steps:
        context["previous_output"] = previous
        prompt = template.format(**context)
        output = llm(prompt)
        context[f"step_{name}"] = output
        results.append((name, output))
        previous = output

    return results, previous


# --- Demo 1: two steps ---


def demo_basic():
    steps = [
        ("summarize", "Summarize in one sentence:\n\n{text}"),
        ("lesson", "Explain this to a beginner:\n\n{previous_output}"),
    ]
    results, final = run_chain(
        mock_llm,
        steps,
        text="Prompt chaining calls the LLM multiple times; each answer becomes input for the next prompt.",
    )
    print("=== Demo 1: basic (2 steps) ===\n")
    for name, out in results:
        print(f"{name}: {out}\n")
    print(f"Final: {final}\n")


# --- Demo 2: blog outline → draft → edit ---


def demo_blog():
    topic = "Why use prompt chaining?"
    steps = [
        (
            "outline",
            "Topic: {topic}\nWrite a 3-bullet outline only.",
        ),
        (
            "draft",
            "Topic: {topic}\nOutline:\n{previous_output}\nWrite 2 sentences.",
        ),
        (
            "edit",
            "Polish this draft (under 60 words):\n{previous_output}",
        ),
    ]
    results, final = run_chain(mock_llm, steps, topic=topic)
    print("=== Demo 2: blog (3 steps) ===\n")
    for name, out in results:
        print(f"{name}: {out}\n")
    print(f"Final: {final}\n")


if __name__ == "__main__":
    demo_basic()
    # demo_blog()
