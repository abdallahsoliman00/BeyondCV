from typing import override, Any
from BeyondCV.Translator.DocTranslator import DocTranslator

class TeXTranslator(DocTranslator):
    @override
    def build(self, data: dict[str, Any]) -> str:
        pass
