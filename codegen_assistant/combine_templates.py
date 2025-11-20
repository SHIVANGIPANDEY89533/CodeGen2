import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates" / "html"
OUTPUT_DIR = BASE_DIR / "public"

def build_page(
    title: str = "CodeGen Assistant",
    header_text: str = "Hugging Face Code Generator",
    base_template: str = "base_template.html",
    main_template: str = "sample_page.html",
    output_file: str = "index.html",
) -> None:
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Read base template
    base_path = TEMPLATES_DIR / base_template
    base_html = base_path.read_text(encoding="utf-8")

    # Read main content template
    main_path = TEMPLATES_DIR / main_template
    main_html = main_path.read_text(encoding="utf-8")

    # Replace placeholders
    final_html = (
        base_html
        .replace("{{ title }}", title)
        .replace("{{ header_text }}", header_text)
        .replace("{{ main_content }}", main_html)
    )

    # Write final HTML
    output_path = OUTPUT_DIR / output_file
    output_path.write_text(final_html, encoding="utf-8")
    print(f"Built page at: {output_path}")

if __name__ == "__main__":
    build_page()
