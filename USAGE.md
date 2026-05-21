# BeyondCV - User Manual

<!--toc:start-->
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Step 1 — Implement an LLM Invoker](#step-1--implement-an-llm-invoker)
- [Step 2 — Define a CV Template](#step-2--define-a-cv-template)
  - [Table Layout Primitives](#table-layout-primitives)
  - [Section vs RepeatingSection](#section-vs-repeatingsection)
  - [Placeholders](#placeholders)
- [Step 3 — Run the Pipeline](#step-3--run-the-pipeline)
- [Configuration](#configuration)
- [Extra Extraction Modules](#extra-extraction-modules)
- [Extending the Library](#extending-the-library)
<!--toc:end-->

---

## Installation

BeyondCV is a package on PyPI, so it can easily be installed using pip:
```bash
pip install BeyondCV
```

---

## Quick Start

The full pipeline in four lines:

```python
from pathlib import Path
from BeyondCV.Template import CVTemplate
from BeyondCV.Translator import DocxTranslator
from my_impl.ProfileMaker import MyLLMInvoker   # your LLMInvoker subclass
from my_impl.template import make_template       # your CVTemplate definition

profile = MyLLMInvoker(Path("path/to/cv.pdf"))
data    = profile.get_result_json()

template = make_template()
output   = DocxTranslator("output.docx", template).build(data)
print(f"Saved to: {output}")
```

---

## Step 1 — Implement an LLM Invoker

`LLMInvoker` is an abstract base class. Subclass it and implement `invoke()`, which receives the full prompt string and must return the LLM's raw text response.

```python
from typing import override
from openai import OpenAI
from BeyondCV.LLM.LLMInvoker import LLMInvoker

class MyLLMInvoker(LLMInvoker):
    @override
    def invoke(self, prompt: str) -> str:
        client = OpenAI(base_url="https://...", api_key="sk-...")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=4096,
        )
        return str(completion.choices[0].message.content)
```

The base class handles everything else automatically:
- Extracts text from the PDF via `pypdf`
- Builds the prompt from `prompt.txt` and the `BASE_TEMPLATE` JSON schema
- Parses the LLM's JSON response
- Caches the result to `~/.beyondcv/archive/<filename>.json`

**Using a `.env` file for secrets** (recommended):

```
# .env
BASE_URL=https://api.openai.com/v1
API_KEY=sk-...
MODEL=gpt-4o
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

class MyLLMInvoker(LLMInvoker):
    @override
    def invoke(self, prompt: str) -> str:
        client = OpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("API_KEY"),
        )
        ...
```

---

## Step 2 — Define a CV Template

### Table Layout Primitives

The layout system is a hierarchy of four classes, all importable from `BeyondCV.TableBuilder`:

| Class | Description |
|---|---|
| `Paragraph(text, config?)` | A single block of text. `text` may contain `{placeholder}` tokens. |
| `Cell(content, config?)` | Holds one or more `Paragraph` objects. |
| `Row(cells, min_height_cm?, row_width_cm?)` | A horizontal list of `Cell` objects. |
| `Table(rows)` | A list of `Row` objects forming one visual block. |

**`ParagraphConfig`** controls text styling:

```python
from BeyondCV.TableBuilder import ParagraphConfig

ParagraphConfig(
    font_name="Aptos",   # defaults to config value
    font_size_pt=10.0,
    bold=False,
    italic=False,
    underline=False,
    bullet=False,        # render as a bullet-list item
)
```

**`CellConfig`** controls cell layout and appearance:

```python
from BeyondCV.TableBuilder import CellConfig
from colour import Color

CellConfig(
    width_cm=4.0,                      # 0.0 = auto (equal share of row width)
    color=Color("#42b0f5"),            # background fill color
    content_alignment={
        "vertical": "center",          # "top" | "center" | "bottom"
        "horizontal": "left",          # "left" | "center" | "right"
    },
    show_borders=False,
)
```

**Example — a simple two-column row:**

```python
from BeyondCV.TableBuilder import Row, Cell, Paragraph, ParagraphConfig, CellConfig
from colour import Color

row = Row([
    Cell(
        Paragraph("{name}", ParagraphConfig(bold=True, font_size_pt=18)),
        CellConfig(width_cm=10),
    ),
    Cell(
        Paragraph("{title}", ParagraphConfig(italic=True)),
        CellConfig(width_cm=6, color=Color("#eeeeee")),
    ),
])
```

---

### Section vs RepeatingSection

Both are importable from `BeyondCV.Template`:

```python
from BeyondCV.Template import CVTemplate, Section, RepeatingSection
```

**`Section(*rows)`** — a fixed block rendered once.

```python
Section(
    Row([Cell(Paragraph("{name}", ParagraphConfig(bold=True, font_size_pt=24)))]),
    Row([Cell(Paragraph("{profile_summary}", ParagraphConfig(italic=True)))]),
)
```

**`RepeatingSection(source_key, item, header?)`** — iterates over a list field in the data and renders one `Table` per item.

| Parameter | Type | Description |
|---|---|---|
| `source_key` | `str` | The key in the extracted JSON whose value is a list (e.g. `"experience"`). |
| `item` | `Table` | The row template to repeat for each list entry. |
| `header` | `Row` or `list[Row]` or `None` | Optional header row(s) prepended once before all repeated items. When provided, all items are merged into a single table. |

```python
# Repeating section without a header — one table per experience entry
RepeatingSection(
    source_key="experience",
    item=Table([
        Row([
            Cell(Paragraph("{organisation}", ParagraphConfig(bold=True))),
            Cell(Paragraph("{job_title}")),
            Cell(Paragraph("{job_period}", ParagraphConfig(italic=True))),
        ]),
        Row([
            Cell(Paragraph("{description}", ParagraphConfig(bullet=True))),
        ]),
    ]),
)

# Repeating section with a header row — all items merged into one table
RepeatingSection(
    source_key="experience",
    item=Table([
        Row([
            Cell(Paragraph("{organisation}")),
            Cell(Paragraph("{job_title}")),
            Cell(Paragraph("{job_period}")),
        ]),
    ]),
    header=Row([
        Cell(Paragraph("Organisation", ParagraphConfig(bold=True)), CellConfig(color=Color("#42b0f5"))),
        Cell(Paragraph("Job Title",    ParagraphConfig(bold=True)), CellConfig(color=Color("#42b0f5"))),
        Cell(Paragraph("Period",       ParagraphConfig(bold=True)), CellConfig(color=Color("#42b0f5"))),
    ]),
)
```

**`CVTemplate(sections)`** — composes all sections into the final document.

```python
template = CVTemplate([
    Section(...),
    RepeatingSection(...),
    RepeatingSection(...),
])
```

---

### Placeholders

Placeholder tokens (`{field_name}`) are resolved against the JSON extracted by the LLM. The default extracted fields are:

| Placeholder | Type | Description |
|---|---|---|
| `{name}` | string | Full name |
| `{title}` | string | Job title / headline |
| `{profile_summary}` | string | Profile summary paragraph |
| `{institute}` | string | (inside `education` list) Institution name |
| `{degree}` | string | (inside `education` list) Degree name |
| `{year}` | string | (inside `education` list) Graduation year |
| `{organisation}` | string | (inside `experience` list) Employer name |
| `{job_title}` | string | (inside `experience` list) Role title |
| `{job_period}` | string | (inside `experience` list) Employment period |
| `{description}` | list[string] | (inside `experience` list) Bullet points — auto-expanded into multiple `Paragraph` objects |
| `{project_name}` | string | (inside `projects` list) Project name |
| `{group_name}` | string | (inside `skill_groups` list) Skill group label |
| `{items}` | list[string] | (inside `skill_groups` list) Skill items |
| `{language}` | string | (inside `languages` list) Language name |
| `{proficiency}` | string | (inside `languages` list) Proficiency level |
| `{certifications}` | list[string] | List of certifications |

**List field expansion:** When a placeholder resolves to a list (e.g. `{description}`), the cell automatically expands into one `Paragraph` per item. You can append a suffix to all but the last item:

```python
# Renders as "Python, C++, Go" (comma after each item except the last)
Cell(Paragraph("{items}, "))
```

---

## Step 3 — Run the Pipeline

```python
from pathlib import Path
from BeyondCV.Template import CVTemplate
from BeyondCV.Translator import DocxTranslator
from my_impl.invoker import MyLLMInvoker

def main():
    # 1. Extract structured data from the PDF
    invoker = MyLLMInvoker(Path("my_cv.pdf"))
    data = invoker.get_result_json()

    # 2. Build the template
    template = CVTemplate([...])   # your Section / RepeatingSection definitions

    # 3. Render to .docx
    output_path = DocxTranslator("my_cv.docx", template).build(data)
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
```

The output `.docx` is saved to `~/.beyondcv/outfiles/<filename>.docx`.

---

## Configuration

Place a `config.yaml` file in your working directory to override any default settings. Only the keys you specify are overridden; everything else falls back to the defaults.

```yaml
# config.yaml
paper_size: "letter"     # "A4" (default) or "letter"
margin_top_cm: 1.5
margin_bottom_cm: 1.5
margin_left_cm: 1.5
margin_right_cm: 1.5
default_font: "Calibri"
use_cache: true          # always reuse cached LLM results without prompting
```

**Default values** (from `BeyondCV/default_config.yaml`):

| Key | Default |
|---|---|
| `paper_size` | `"A4"` |
| `margin_top_cm` | `2.54` |
| `margin_bottom_cm` | `2.54` |
| `margin_left_cm` | `2.54` |
| `margin_right_cm` | `2.54` |
| `default_font` | `"Aptos"` |
| `use_cache` | `false` |

---

## Extra Extraction Modules

Pass optional module names to your `LLMInvoker` constructor to extract additional fields beyond the defaults.

```python
invoker = MyLLMInvoker(Path("my_cv.pdf"), modules=["social", "salary", "military_status"])
data = invoker.get_result_json()
```

| Module | Extra fields added to the JSON |
|---|---|
| `"social"` | `linkedin`, `github`, `email` |
| `"salary"` | `salary_expectation` |
| `"military_status"` | `military_status` |

Use them in your template like any other placeholder:

```python
Cell(Paragraph("{linkedin}"))
Cell(Paragraph("{salary_expectation}"))
```

---

## Extending the Library

### Custom LLM backend

Subclass `LLMInvoker` and override `invoke(prompt) -> str`. See [Step 1](#step-1--implement-an-llm-invoker).

### Custom output format

Subclass `DocTranslator` and override `build(data) -> str | Path`:

```python
from BeyondCV.Translator.DocTranslator import DocTranslator

class MyTeXTranslator(DocTranslator):
    def build(self, data):
        # render self.tables to a .tex file
        ...
```

### Custom archive location

Override `get_default_archive_path()` in your `LLMInvoker` subclass:

```python
class MyLLMInvoker(LLMInvoker):
    def get_default_archive_path(self):
        return Path("./cache") / f"{self.file_name}.json"

    def invoke(self, prompt):
        ...
```

### Adding new extraction fields

Add entries to `EXTRA_MODULES` in `BeyondCV/LLM/CVFields.py`:

```python
EXTRA_MODULES["portfolio"] = [
    {
        "key": "portfolio_url",
        "description": "Candidate's portfolio website URL",
        "type": "string"
    }
]
```

Then request the module when constructing your invoker:

```python
invoker = MyLLMInvoker(Path("cv.pdf"), modules=["portfolio"])
```
