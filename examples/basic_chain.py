"""
Minimal prompt chain — no API key required.

Flow: summarize user text → expand summary into a "lesson" line.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chain import ChainStep, PromptChain
from src.llm import MockLLM

SUMMARIZE_STEP = ChainStep(
    name="summarize",
    template="Summarize the following in one sentence:\n\n{text}",
)

EXPAND_STEP = ChainStep(
    name="expand",
    template=(
        "You are a teacher. Turn this summary into one clear lesson "
        "for a beginner learning prompt chaining:\n\n{previous_output}"
    ),
)


def main() -> None:
    chain = PromptChain(
        llm=MockLLM(),
        steps=[SUMMARIZE_STEP, EXPAND_STEP],
    )

    result = chain.run(
        text=(
            "Prompt chaining means calling an LLM multiple times in order. "
            "Each call uses the last answer as context for the next prompt."
        )
    )

    print("=== Prompt chaining demo (mock LLM) ===\n")
    for name, output in result.steps:
        print(f"[{name}]")
        print(output)
        print()

    print("Final:", result.final_output)


if __name__ == "__main__":
    main()
