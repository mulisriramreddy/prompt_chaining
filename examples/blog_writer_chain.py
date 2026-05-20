"""
Classic 3-step writing chain: outline → draft → edit.

Uses MockLLM so you can run without credentials.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chain import ChainStep, PromptChain
from src.llm import MockLLM
from src.prompts import BLOG_DRAFT, BLOG_EDIT, BLOG_OUTLINE


def main() -> None:
    chain = PromptChain(
        llm=MockLLM(),
        steps=[
            ChainStep(name="outline", template=BLOG_OUTLINE),
            ChainStep(name="draft", template=BLOG_DRAFT),
            ChainStep(name="edit", template=BLOG_EDIT),
        ],
    )

    result = chain.run(topic="Why use prompt chaining instead of one big prompt?")

    print("=== Blog writer chain (mock LLM) ===\n")
    for name, output in result.steps:
        print(f"--- {name} ---")
        print(output)
        print()

    print("=== Published ===")
    print(result.final_output)


if __name__ == "__main__":
    main()
