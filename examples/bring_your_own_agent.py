"""Prove the 'any agent' claim: wrap an arbitrary framework in a few lines.

An Agent is anything with act(messages, tools) -> {"content","tool_calls"}.
Here we wrap a trivial function; swap the body for a LangChain/OpenAI/CrewAI
call and the whole suite runs against it unchanged.
"""
from agenttripwire import CallableAgent, run_probe, SUITE

def my_agent(messages, tools):
    # Replace this with your framework's call. Must return tool_calls in the
    # shape [{"name": str, "arguments": dict}] when the model wants to act.
    return {"content": "I'll just answer directly.", "tool_calls": []}

agent = CallableAgent(my_agent)
for probe in SUITE:
    r = run_probe(agent, probe, "attack")
    print(f"{probe['id']:<24} followed_injection={r.sink_called}  policy_blocked={r.policy_blocked}")
