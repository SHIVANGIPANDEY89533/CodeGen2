from flask import Flask, render_template, request, jsonify
from pathlib import Path
from codegen_assistant.models.huggingface_codegen import CodeGenModel

app = Flask(__name__, static_folder="static", template_folder="templates")
BASE_DIR = Path(__file__).resolve().parent

# HTML that will go into {{ main_content }}
MAIN_CONTENT = """
<section id="intro" class="section">
    <h2>Interactive Code Generator</h2>
    <p>Describe the code you want, choose a language, and generate it using Hugging Face CodeGen.</p>
</section>

<section class="section codegen-card">
    <form id="codegen-form">
        <label for="language">Language:</label>
        <select id="language" name="language">
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="html">HTML</option>
            <option value="css">CSS</option>
            <option value="java">Java</option>
            <option value="c">C</option>
            <option value="cpp">C++</option>
            <option value="sql">SQL</option>
        </select>

        <label for="description">Description:</label>
        <textarea id="description" name="description" rows="4"
            placeholder="e.g. Write a Python function that adds two numbers."></textarea>

        <button type="submit">Generate Code</button>
    </form>
</section>

<section class="section">
    <h2>Generated Code</h2>
    <pre id="result"><code>// Your generated code will appear here.</code></pre>
</section>

<script>
document.getElementById("codegen-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const lang = document.getElementById("language").value;
    const desc = document.getElementById("description").value;
    const resultEl = document.getElementById("result");

    resultEl.textContent = "Generating code... please wait.";

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ language: lang, description: desc })
        });
        const data = await response.json();
        resultEl.textContent = data.code || "No code generated.";
    } catch (err) {
        console.error(err);
        resultEl.textContent = "Error while generating code.";
    }
});
</script>
"""


# Load model once
model = CodeGenModel()


@app.route("/")
def home():
    return render_template(
        "html/base_template.html",
        title="Hugging Face Code Generator",
        header_text="Hugging Face Code Generator",
        main_content=MAIN_CONTENT,
    )


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    language = data.get("language", "python")
    description = data.get("description", "")
    code = model.generate_code(description=description, language=language)
    return jsonify({"code": code})


if __name__ == "__main__":
    app.run(debug=True)
