"""LLM backends used by prompt chains."""

from __future__ import annotations

import os
from typing import Protocol


class LLM(Protocol):
    """Anything that can turn a prompt string into text."""

    def complete(self, prompt: str) -> str: ...


class MockLLM:
    """
    Deterministic fake LLM for learning without API keys.

    It pattern-matches on keywords in the prompt so you can see
    how context flows between steps.
    """

    def complete(self, prompt: str) -> str:
        lower = prompt.lower()

        # More specific patterns first — later steps often mention "outline" in context.
        if "edit" in lower or "polish" in lower or "improve" in lower:
            return (
                "**Prompt chaining** splits work across focused LLM calls. "
                "Earlier outputs feed the next prompt, which improves quality "
                "and makes failures easier to fix."
            )

        if "draft" in lower or ("write" in lower and "outline" not in lower[:120]):
            return (
                "Prompt chaining breaks a large task into steps. "
                "Step one might plan; step two drafts using that plan; "
                "step three polishes. Each step only sees what it needs."
            )

        if "writing planner" in lower or "numbered outline" in lower:
            return (
                "1. Hook: why prompt chaining matters\n"
                "2. Define chaining vs one-shot prompts\n"
                "3. Walk through a 3-step example\n"
                "4. Trade-offs: cost, latency, debuggability"
            )

        if "summarize" in lower:
            return "Chaining = sequential prompts where each output informs the next."

        if "teacher" in lower or "lesson" in lower:
            return (
                "Lesson: Think of prompt chaining like an assembly line—"
                "each LLM step does one job and hands its result to the next."
            )

        return f"[mock response for prompt fragment: {prompt[:80]}...]"


class OpenAILLM:
    """OpenAI Chat Completions backend."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "Install dependencies: pip install -r requirements.txt"
            ) from exc

        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError(
                "OPENAI_API_KEY is required. Copy .env.example to .env and set your key."
            )

        self._client = OpenAI(api_key=key)
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        message = response.choices[0].message.content
        return (message or "").strip()
