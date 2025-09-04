from __future__ import annotations

from typing import Optional, Dict, Any


class LLM:
    def generate_text(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        raise NotImplementedError

    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> Dict[str, Any]:
        import json
        text = self.generate_text(system_prompt, user_prompt, temperature=temperature)
        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError(f"LLM did not return valid JSON: {exc}\n{text}")
