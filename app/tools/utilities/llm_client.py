# llm_client.py
import abc
import os
import logging
from typing import List, Dict, Optional
from openai import OpenAI, OpenAIError
from google import genai
from google.genai import types
from google.api_core.exceptions import GoogleAPIError

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
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling OpenAI...")
        try:
            resp = self.client.chat.completions.create(
                model=kwargs.pop("model", os.getenv("OPENAI_VERSION")),
                messages=[m for m in [
                    {"role": "system", "content": system}] if system] +
                    [{"role": "user", "content": prompt}],
                    **kwargs
                    )
            return resp.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"OpenAI error: {e}")
            raise RuntimeError(f"OpenAI API failure: {e}")

class GeminiClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.client =  genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.types = types
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling Gemini...")
        try:
            resp = self.client.models.generate_content(
                model=kwargs.pop("model", os.getenv("GEMINI_VERSION")),
                config=self.types.GenerateContentConfig(
                    system_instruction=system
                    ),
                contents=prompt
            )
            return resp.text
        except GoogleAPIError as e:
            logger.error(f"Gemini API error: {e}")
            raise RuntimeError(f"Gemini API failure: {e}")
        
class GrokClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(
            api_key=api_key or os.getenv("GROK_API_KEY"),
            base_url=os.getenv("GROK_BASE_URL"))
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling Grok...")
        msgs = ([{"role":"system","content":system}] if system else []) + \
               [{"role":"user","content":prompt}]
        try:
            resp = self.client.chat.completions.create(
                model=kwargs.pop("model", os.getenv("GROK_VERSION")),
                messages=msgs,
                **kwargs
                )
            return resp.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"Grok API error: {e}")
            raise RuntimeError(f"Grok API failure: {e}")

class DeepSeekClient(LLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL"))
    def complete(self, prompt: str, system=None, **kwargs):
        logger.info("Calling DeepSeek...")
        msgs = ([{"role":"system","content":system}] if system else []) + \
               [{"role":"user","content":prompt}]
        try:
            resp = self.client.chat.completions.create(
                model=kwargs.pop("model", os.getenv("DEEPSEEK_VERSION")),
                messages=msgs,
                **kwargs
                )
            return resp.choices[0].message.content
        except OpenAIError as e:
            logger.error(f"DeepSeek API error: {e}")
            raise RuntimeError(f"DeepSeek API failure: {e}")
    

# factory + runner
from typing import Dict
from ..utilities.llm_client import OpenAIClient, GeminiClient, GrokClient, DeepSeekClient, LLMClient

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

