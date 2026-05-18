from typing import override
from openai import OpenAI
from BeyondCV.LLM.LLMInvoker import LLMInvoker

from BuildImpl.config import LLM_Config


class LLMProfileMaker(LLMInvoker):
    base_url: str = LLM_Config["BASE_URL"]
    API_KEY: str = LLM_Config["API_KEY"]
    LLM_Model: str = LLM_Config["Model"]

    @override
    def invoke(self, prompt: str) -> str:
        if not self.API_KEY:
            raise ValueError("Couldn't find an API key.")

        client = OpenAI(base_url=self.base_url, api_key=self.API_KEY)
        completion = client.chat.completions.create(
            model=self.LLM_Model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=4096,
        )
        return str(completion.choices[0].message.content)

