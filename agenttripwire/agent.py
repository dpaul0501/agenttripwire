"""The Agent seam — this is how 'any agent' connects.

Implement `act(messages, tools) -> {"content": str, "tool_calls": [...]}` for
your framework and the whole suite runs against it. Ships an Ollama adapter
(HTTP, native tool-calling, no deps) and a Callable wrapper.
"""
from __future__ import annotations
import json, urllib.request
from typing import Protocol, Callable

class Agent(Protocol):
    def act(self, messages: list[dict], tools: list[dict]) -> dict: ...

def _norm_tool_calls(raw) -> list[dict]:
    out = []
    for c in raw or []:
        fn = c.get("function", c)
        args = fn.get("arguments", {})
        if isinstance(args, str):
            try: args = json.loads(args)
            except Exception: args = {"_raw": args}
        out.append({"name": fn.get("name"), "arguments": args})
    return out

class OllamaAgent:
    """Any local model served by Ollama, via /api/chat native tool-calling."""
    def __init__(self, model: str, host: str = "http://localhost:11434", temperature: float = 0.0):
        self.model, self.host, self.temperature = model, host, temperature
    def act(self, messages, tools):
        body = {"model": self.model, "messages": messages, "tools": tools,
                "stream": False, "options": {"temperature": self.temperature}}
        req = urllib.request.Request(self.host + "/api/chat",
                data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read())
        m = d.get("message", {})
        return {"content": m.get("content","") or "", "tool_calls": _norm_tool_calls(m.get("tool_calls"))}

class CallableAgent:
    """Wrap any function (messages, tools) -> {'content','tool_calls'} as an Agent."""
    def __init__(self, fn: Callable[[list,list], dict]): self.fn = fn
    def act(self, messages, tools): return self.fn(messages, tools)
