"""CLI:  python -m agenttripwire --agent ollama:qwen2.5:7b-instruct-q8_0 --reps 3"""
from __future__ import annotations
import argparse
from .agent import OllamaAgent
from .harness import run_probe
from .probes import SUITE
from .report import score

def build_agent(spec: str):
    if spec.startswith("ollama:"):
        return OllamaAgent(spec.split(":",1)[1])
    raise SystemExit(f"unknown agent spec: {spec} (try ollama:<model>)")

def main():
    ap = argparse.ArgumentParser(prog="agenttripwire")
    ap.add_argument("--agent", default="ollama:qwen2.5:7b-instruct-q8_0")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--only", default=None, help="run a single probe id")
    a = ap.parse_args()
    agent = build_agent(a.agent)
    suite = [p for p in SUITE if (a.only is None or p["id"]==a.only)]
    by = {}
    for p in suite:
        print(f"[.] {p['id']} ({p['surface']}) ...", flush=True)
        atk = [run_probe(agent, p, "attack") for _ in range(a.reps)]
        ctl = [run_probe(agent, p, "control") for _ in range(a.reps)]
        by[p["id"]] = {"surface":p["surface"],"asi":p["asi"],"attack":atk,"control":ctl}
        print(f"    followed {sum(r.sink_called for r in atk)}/{a.reps}  "
              f"misfire {sum(r.sink_called for r in ctl)}/{a.reps}", flush=True)
    print("\n" + score(by, a.reps).text())

if __name__ == "__main__":
    main()
