# codegen_assistant/models/huggingface_codegen.py

from typing import Literal
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Choose a reasonably small CodeGen model
DEFAULT_MODEL_NAME = "Salesforce/codegen-350M-multi"

LanguageType = Literal[
    "python",
    "javascript",
    "html",
    "css",
    "java",
    "c",
    "cpp",
    "sql",
]


class CodeGenModel:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, device: str | None = None) -> None:
        """
        Wrapper around Hugging Face CodeGen model for simple code generation.
        Supports prompts for multiple languages via text instructions.
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model.to(self.device)

    def _build_prompt(self, description: str, language: LanguageType) -> str:
        """
        Build a text prompt for the desired language.
        CodeGen is language-agnostic; we steer it with comments / tags.
        """
        if language == "python":
            prefix = "# Python function:\n"
        elif language == "javascript":
            prefix = "// JavaScript function:\n"
        elif language == "html":
            prefix = "<!-- HTML template -->\n"
        elif language == "css":
            prefix = "/* CSS styles */\n"
        elif language == "java":
            prefix = "// Java method:\n"
        elif language == "c":
            prefix = "/* C function */\n"
        elif language == "cpp":
            prefix = "// C++ function:\n"
        elif language == "sql":
            prefix = "-- SQL query:\n"
        else:
            prefix = ""

        return f"{prefix}{description}\n"

    def generate_code(
        self,
        description: str,
        language: LanguageType = "python",
        max_tokens: int = 120,
        temperature: float = 0.1,
    ) -> str:
        """
        Generate code snippet from a natural language description.
        Uses max_new_tokens and decodes only new tokens to avoid
        repeating the prompt many times.
        """
        prompt = self._build_prompt(description, language)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_len = inputs["input_ids"].shape[1]

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=temperature,
            repetition_penalty=1.2,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        # decode only the newly generated part, not the prompt itself
        new_tokens = output_ids[0][input_len:]
        generated = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return generated.strip()
