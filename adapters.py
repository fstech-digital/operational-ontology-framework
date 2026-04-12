"""
LLM Adapters — Model-agnostic interface for the Operational Ontology Framework
===============================================================================

The agent.py reference implementation uses Anthropic by default, but the
framework is model-agnostic. These adapters demonstrate how to swap providers.

Usage:
    # Anthropic (default)
    python agent.py examples/customer-support

    # OpenAI
    ADAPTER=openai OPENAI_API_KEY=sk-... python agent.py examples/customer-support --model gpt-4o

    # Ollama (local models — Gemma, Llama, Mistral, etc.)
    ADAPTER=ollama python agent.py examples/customer-support --model gemma4:e2b

    # Custom adapter
    Set ADAPTER=custom and implement create_message() following the interface below.

Each adapter must implement:
    create_message(model, max_tokens, system, messages) -> str
    Returns the text content of the LLM response.
"""

import os
import sys


def get_adapter(name: str = None):
    """Return an adapter by name. Default: anthropic."""
    name = name or os.environ.get("ADAPTER", "anthropic")
    adapters = {
        "anthropic": AnthropicAdapter,
        "openai": OpenAIAdapter,
        "ollama": OllamaAdapter,
    }
    if name not in adapters:
        print(f"Unknown adapter: {name}. Available: {', '.join(adapters)}")
        sys.exit(1)
    return adapters[name]()


class AnthropicAdapter:
    """Adapter for Anthropic's Claude models."""

    def __init__(self):
        try:
            import anthropic
            self._anthropic = anthropic
        except ImportError:
            print("Install anthropic SDK: pip install anthropic")
            sys.exit(1)

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("ANTHROPIC_API_KEY not set.")
            sys.exit(1)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.retryable_errors = (
            anthropic.RateLimitError,
            anthropic.APIConnectionError,
        )
        self.status_error = anthropic.APIStatusError

    def create_message(self, model: str, max_tokens: int, system: str, messages: list) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text


class OpenAIAdapter:
    """Adapter for OpenAI's GPT models."""

    def __init__(self):
        try:
            from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError
            self._rate_limit_error = RateLimitError
            self._connection_error = APIConnectionError
            self._status_error = APIStatusError
        except ImportError:
            print("Install openai SDK: pip install openai")
            sys.exit(1)

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY not set.")
            sys.exit(1)
        self.client = OpenAI(api_key=api_key)
        self.retryable_errors = (self._rate_limit_error, self._connection_error)
        self.status_error = self._status_error

    def create_message(self, model: str, max_tokens: int, system: str, messages: list) -> str:
        openai_messages = [{"role": "system", "content": system}]
        for m in messages:
            openai_messages.append({"role": m["role"], "content": m["content"]})

        response = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=openai_messages,
        )
        return response.choices[0].message.content


class OllamaAdapter:
    """Adapter for Ollama (local models via OpenAI-compatible API).

    Works with any model Ollama serves: gemma4, llama3, mistral, phi, etc.
    Set OLLAMA_HOST to override the default http://localhost:11434.
    No API key required.

    Usage:
        ADAPTER=ollama python agent.py examples/customer-support --model gemma4:e2b
        ADAPTER=ollama OLLAMA_HOST=http://192.168.1.100:11434 python agent.py ... --model llama3
    """

    def __init__(self):
        try:
            from openai import OpenAI
        except ImportError:
            print("Install openai SDK: pip install openai  (Ollama uses OpenAI-compatible API)")
            sys.exit(1)

        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.client = OpenAI(base_url=f"{host}/v1", api_key="ollama")
        self.retryable_errors = (ConnectionError,)
        self.status_error = Exception

    def create_message(self, model: str, max_tokens: int, system: str, messages: list) -> str:
        openai_messages = [{"role": "system", "content": system}]
        for m in messages:
            openai_messages.append({"role": m["role"], "content": m["content"]})

        response = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=openai_messages,
        )
        return response.choices[0].message.content
