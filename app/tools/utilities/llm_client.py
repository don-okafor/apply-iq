# llm_client.py
import abc
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LLMClient(abc.ABC):
    @abc.abstractmethod
    def complete(self,
                 prompt: str,
                 system: Optional[str] = None,
                 **kwargs) -> str:
        """Run a text completion/instruct call. Return the response text."""
        pass

class OpenAIClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling OpenAI...")
        resp = self.client.chat.completions.create(
            model=kwargs.pop("model", "gpt-4o"),
            messages=[m for m in [
                {"role": "system", "content": system}] if system] +
                     [{"role": "user", "content": prompt}],
            **kwargs
        )
        content = resp.choices[0].message.content
        return content

class GeminiClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        import google.genai as genai
        genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.client = genai
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling Gemini...")
        resp = self.client.generate_content(
            model=kwargs.pop("model", "gemini-2.5-flash"),
            prompt=prompt,
            **kwargs
        )
        return resp.text

class GrokClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=api_key or os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1")
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling Grok...")
        msgs = ([{"role":"system","content":system}] if system else []) + \
               [{"role":"user","content":prompt}]
        resp = self.client.chat.completions.create(
            model=kwargs.pop("model", "grok-beta"),
            messages=msgs,
            **kwargs
        )
        return resp.choices[0].message.content

class DeepSeekClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        from openai import OpenAI
        self.client = OpenAI(
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com")
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling DeepSeek...")
        msgs = ([{"role":"system","content":system}] if system else []) + \
               [{"role":"user","content":prompt}]
        resp = self.client.chat.completions.create(
            model=kwargs.pop("model", "deepseek-chat"),
            messages=msgs,
            **kwargs
        )
        return resp.choices[0].message.content
    

# factory + runner
from typing import Dict
from llm_client import OpenAIClient, GeminiClient, GrokClient, DeepSeekClient, LLMClient

class LLMFactory:
    _clients: Dict[str, LLMClient] = {
        "openai": OpenAIClient(),
        "gemini": GeminiClient(),
        "grok": GrokClient(),
        "deepseek": DeepSeekClient(),
    }

    @staticmethod
    def get_client(provider: str) -> LLMClient:
        client = LLMFactory._clients.get(provider.lower())
        if not client:
            raise ValueError(f"Unknown provider: {provider}")
        return client

def run_completion(provider: str, prompt: str, system: Optional[str] = None, **kwargs) -> str:
    client = LLMFactory.get_client(provider)
    return client.complete(prompt, system=system, **kwargs)

