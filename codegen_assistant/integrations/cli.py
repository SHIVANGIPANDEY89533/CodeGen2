# codegen_assistant/integrations/cli.py

import argparse
import pathlib
from datetime import datetime
from codegen_assistant.models.huggingface_codegen import CodeGenModel, LanguageType

GENERATED_DIR = pathlib.Path(__file__).resolve().parents[1] / "generated"

EXTENSIONS = {
    "python": ".py",
    "javascript": ".js",
    "html": ".html",
    "css": ".css",
    "java": ".java",
    "c": ".c",
    "cpp": ".cpp",
    "sql": ".sql",
}


def save_code(code: str, language: LanguageType, description: str) -> pathlib.Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    safe_desc = "_".join(description.lower().split()[:4])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = EXTENSIONS[language]
    filename = f"{language}_{safe_desc}_{timestamp}{ext}"
    path = GENERATED_DIR / filename
    path.write_text(code, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Hugging Face CodeGen CLI")
    parser.add_argument(
        "-l",
        "--language",
        choices=["python", "javascript", "html","java", "c", "cpp", "sql"],
        default="python",
        help="Target language for generated code",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=True,
        help="Natural language description of the code to generate",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=200,
        help="Maximum number of tokens to generate",
    )
    args = parser.parse_args()

    model = CodeGenModel()
    lang: LanguageType = args.language  # type: ignore[assignment]
    code = model.generate_code(
        description=args.description,
        language=lang,
        max_tokens=args.max_tokens,
    )

    print("\n=== Generated code ===\n")
    print(code)

    path = save_code(code, lang, args.description)
    print(f"\nSaved to: {path}")


if __name__ == "__main__":
    main()
