"""
Prompt chaining: run LLM steps in order, passing outputs forward.

Context dict keys:
  - Keys you pass into run() (e.g. topic="...")
  - After each step: step_<name> = that step's output
  - previous_output = last step's output (convenience for templates)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.llm import LLM


@dataclass
class ChainStep:
    """
    One link in the chain.

    template: str with {placeholders} filled from context
    input_key: if set, only this context value is passed as previous_output
               (advanced; default uses full previous_output)
    """

    name: str
    template: str
    input_key: str | None = None


@dataclass
class ChainResult:
    """All step outputs from a single chain run."""

    context: dict[str, Any]
    steps: list[tuple[str, str]] = field(default_factory=list)

    @property
    def final_output(self) -> str:
        if not self.steps:
            return ""
        return self.steps[-1][1]


class PromptChain:
    """Runs ChainSteps sequentially through an LLM."""

    def __init__(self, llm: LLM, steps: list[ChainStep]) -> None:
        if not steps:
            raise ValueError("PromptChain requires at least one step")
        self._llm = llm
        self._steps = steps

    def run(self, **initial_context: Any) -> ChainResult:
        context: dict[str, Any] = dict(initial_context)
        recorded: list[tuple[str, str]] = []

        for step in self._steps:
            if step.input_key is not None:
                context["previous_output"] = context.get(step.input_key, "")
            elif recorded:
                context["previous_output"] = recorded[-1][1]
            else:
                context["previous_output"] = ""

            prompt = step.template.format(**context)
            output = self._llm.complete(prompt)

            context[f"step_{step.name}"] = output
            recorded.append((step.name, output))

        return ChainResult(context=context, steps=recorded)
