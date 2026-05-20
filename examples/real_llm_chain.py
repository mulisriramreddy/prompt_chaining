"""
Same blog chain as blog_writer_chain.py, but calls OpenAI.

Requires: OPENAI_API_KEY in environment or .env (load manually if you use python-dotenv).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.chain import ChainStep, PromptChain
from src.llm import OpenAILLM
from src.prompts import BLOG_DRAFT, BLOG_EDIT, BLOG_OUTLINE


def main() -> None:
    chain = PromptChain(
        llm=OpenAILLM(),
        steps=[
            ChainStep(name="outline", template=BLOG_OUTLINE),
            ChainStep(name="draft", template=BLOG_DRAFT),
            ChainStep(name="edit", template=BLOG_EDIT),
        ],
    )

    result = chain.run(topic="Prompt chaining for software engineers")

    for name, output in result.steps:
        print(f"--- {name} ---")
        print(output)
        print()

    print("=== Final ===")
    print(result.final_output)


if __name__ == "__main__":
    main()
