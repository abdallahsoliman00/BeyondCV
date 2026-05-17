import json
from typing import override, Any
from openai import OpenAI
from pathlib import Path
from BeyondCV.LLM.LLMInvoker import LLMInvoker

from BuildImpl.utils import load_prompt
from BuildImpl.config import LLM_Config


class LLMProfileMaker(LLMInvoker):
    base_url: str = LLM_Config["BASE_URL"]
    API_KEY: str = LLM_Config["API_KEY"]
    LLM_Model: str = LLM_Config["Model"]

    @override
    def invoke(self, path_to_pdf: str | Path) -> Any:
        prompt: str = load_prompt(path_to_pdf=path_to_pdf)
        print(prompt)

        if self.API_KEY == "":
            raise ValueError("Couldn't find an API key.")

        client = OpenAI(
            base_url=self.base_url,
            api_key=self.API_KEY
        )

        completion = client.chat.completions.create(
            model=self.LLM_Model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=4096
        )
        response_text = completion.choices[0].message.content

        try:
            if not response_text:
                raise ValueError("response_text is empty or not a string")

            # Try direct parsing to verify the output is correctly formatted
            data_json: Any = json.loads(response_text)
            return data_json

        except json.JSONDecodeError:
            # Handle markdown-wrapped JSON
            extracted = None

            if response_text is not None and "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                extracted = response_text[json_start:json_end].strip()

            elif response_text is not None and "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                extracted = response_text[json_start:json_end].strip()

            if extracted:
                data_json_retry: Any = json.loads(extracted)
            else:
                raise ValueError("No valid JSON found in response_text")
            
            return data_json_retry

# For testing
if __name__ == "__main__":
    profile_maker = LLMProfileMaker(
        r"C:\Users\absolima\OneDrive - Capgemini\Documents\OneDrive_2026-05-05\OLIVETTI - SW Talent Needs\Software Integration Engineer\Mohamed Adel - B2 Fullstack.pdf"
    )
