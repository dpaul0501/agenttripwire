"""agenttripwire — behavioral third-party readiness testing for any agent.

Bring your own agent (wrap it as an Agent), run the 3P probe suite, get a
trust-boundary scorecard. Report-only: dangerous tool calls are observed and
denied by the harness policy, never executed.
"""
from .agent import Agent, OllamaAgent, CallableAgent
from .harness import run_probe, ProbeResult
from .report import score, Scorecard
from .probes import SUITE
__all__ = ["Agent","OllamaAgent","CallableAgent","run_probe","ProbeResult","score","Scorecard","SUITE"]
