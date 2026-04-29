# Prompt Versioning System for Portfolio Publisher

This document outlines a robust prompt versioning system designed to manage and track changes to prompt templates used within the Portfolio Publisher. Effective prompt versioning is crucial for maintaining consistency, reproducibility, and traceability of generated content, especially when dealing with various platforms and artifact types.

## 1. Core Principles

*   **Centralized Storage:** All prompt templates reside in the `portfolio-publisher/prompts/` directory.
*   **Semantic Versioning:** Prompts will follow a simplified semantic versioning scheme (MAJOR.MINOR.PATCH) to indicate changes.
*   **Immutability:** Once a prompt version is released, its content should not be altered. Any changes require a new version.
*   **Clear Naming Conventions:** Consistent naming helps in identifying and retrieving specific prompt versions.
*   **Metadata:** Each prompt version should be accompanied by metadata describing its purpose, changes, and compatibility.

## 2. Directory Structure

The `prompts/` directory will be organized by platform or artifact type, and then by prompt name, with each prompt having its own versioned sub-directory.

```
portfolio-publisher/prompts/
├── flippa/
│   ├── listing_description/
│   │   ├── v1.0.0/
│   │   │   └── template.txt
│   │   │   └── metadata.json
│   │   ├── v1.1.0/
│   │   │   └── template.txt
│   │   │   └── metadata.json
│   ├── highlights_generator/
│   │   ├── v1.0.0/
│   │   │   └── template.txt
│   │   │   └── metadata.json
├── readme/
│   ├── project_overview/
│   │   ├── v1.0.0/
│   │   │   └── template.txt
│   │   │   └── metadata.json
└── ...
```

## 3. File Structure within a Version Directory

Each version directory (e.g., `v1.0.0/`) will contain:

*   **`template.txt`**: The actual prompt template content. This file can be a plain text file, Markdown, or any other format suitable for the LLM.
*   **`metadata.json`**: A JSON file containing essential information about the prompt version.

### Example `metadata.json`

```json
{
  "version": "1.0.0",
  "name": "listing_description",
  "platform": "flippa",
  "description": "Generates a comprehensive Flippa listing description based on app details.",
  "author": "Manus AI",
  "date_created": "2023-10-27T10:00:00Z",
  "last_updated": "2023-10-27T10:00:00Z",
  "changes": "Initial release of the Flippa listing description template.",
  "parameters": [
    "app_name",
    "tagline",
    "overview",
    "category",
    "tech_stack",
    "monetization",
    "metrics",
    "highlights",
    "operations",
    "reason_for_sale",
    "included"
  ],
  "llm_compatibility": [
    "gpt-4.1-mini",
    "gemini-2.5-flash"
  ]
}
```

## 4. Versioning Strategy

*   **MAJOR version (e.g., `1.0.0` to `2.0.0`):** Incremented for incompatible API changes in the prompt (e.g., removal of a required parameter, significant change in expected output format).
*   **MINOR version (e.g., `1.0.0` to `1.1.0`):** Incremented for adding functionality in a backward-compatible manner (e.g., adding an optional parameter, improving prompt clarity without breaking existing integrations).
*   **PATCH version (e.g., `1.0.0` to `1.0.1`):** Incremented for backward-compatible bug fixes or minor improvements (e.g., typo corrections, slight rephrasing for better LLM performance).

## 5. Usage in `src/core/prompt_renderer.py` (Conceptual)

The `prompt_renderer` utility would be responsible for loading the correct prompt version. It could accept parameters like `platform`, `prompt_name`, and an optional `version`.

```python
# Conceptual Python code snippet
class PromptRenderer:
    def __init__(self, base_path="./prompts"):
        self.base_path = base_path

    def load_prompt(self, platform: str, prompt_name: str, version: str = "latest") -> dict:
        prompt_path = os.path.join(self.base_path, platform, prompt_name)

        if version == "latest":
            # Logic to find the highest version number
            versions = sorted([d for d in os.listdir(prompt_path) if os.path.isdir(os.path.join(prompt_path, d))], reverse=True)
            if not versions:
                raise ValueError(f"No versions found for {platform}/{prompt_name}")
            latest_version_dir = os.path.join(prompt_path, versions[0])
        else:
            latest_version_dir = os.path.join(prompt_path, version)

        if not os.path.exists(latest_version_dir):
            raise FileNotFoundError(f"Prompt version {version} not found for {platform}/{prompt_name}")

        with open(os.path.join(latest_version_dir, "template.txt"), "r") as f:
            template = f.read()
        with open(os.path.join(latest_version_dir, "metadata.json"), "r") as f:
            metadata = json.load(f)

        return {"template": template, "metadata": metadata}

    def render_prompt(self, platform: str, prompt_name: str, data: dict, version: str = "latest") -> str:
        prompt_data = self.load_prompt(platform, prompt_name, version)
        template = prompt_data["template"]
        # Simple string formatting for demonstration; a more robust templating engine (e.g., Jinja2) would be used
        rendered_prompt = template.format(**data)
        return rendered_prompt

# Example Usage (conceptual)
# renderer = PromptRenderer()
# data_for_prompt = {"app_name": "Taskflow Studio", ...}
# rendered_text = renderer.render_prompt("flippa", "listing_description", data_for_prompt, version="1.0.0")
# print(rendered_text)
```

## 6. Workflow for Updating Prompts

1.  **Create a new version directory:** Copy the previous version and increment the version number according to semantic versioning rules.
2.  **Modify `template.txt`:** Make the necessary changes to the prompt content.
3.  **Update `metadata.json`:** Reflect the new version, `last_updated` timestamp, and a clear `changes` description.
4.  **Test:** Thoroughly test the new prompt version to ensure it produces the desired output.
5.  **Integrate:** Update any code that explicitly references the prompt version, or rely on the "latest" retrieval mechanism.

This system provides a clear, organized, and maintainable approach to managing prompt templates, essential for the long-term success of the Portfolio Publisher. 

---

*Generated by Manus AI*
