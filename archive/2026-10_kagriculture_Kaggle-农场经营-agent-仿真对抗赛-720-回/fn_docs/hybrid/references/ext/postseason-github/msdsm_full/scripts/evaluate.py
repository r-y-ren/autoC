"""Evaluate two local agent entry points with the pinned official environment."""

import argparse
import json
from pathlib import Path
from contextlib import ExitStack
import select
import subprocess
import sys


class AgentProcess:
    def __init__(self, entry: Path):
        self.process = subprocess.Popen(
            [sys.executable, "-u", str(Path(__file__).with_name("_agent_worker.py")), str(entry.resolve())],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def __call__(self, observation, configuration):
        self.process.stdin.write(json.dumps({"observation": observation, "configuration": configuration}) + "\n")
        self.process.stdin.flush()
        if not select.select([self.process.stdout], [], [], 120)[0]:
            raise TimeoutError("agent process did not respond")
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("agent process exited")
        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(response["error"])
        return response["action"]

    def close(self):
        self.process.stdin.close()
        if self.process.poll() is None:
            self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent_a", type=Path)
    parser.add_argument("agent_b", type=Path)
    parser.add_argument("--games", type=int, default=2, help="even count; reverse seats for each seed")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("artifacts/evaluation.json"))
    args = parser.parse_args()
    if args.games < 2 or args.games % 2:
        parser.error("games must be a positive even number")
    from importlib.metadata import version

    if version("kaggle-environments") != "1.32.7":
        raise RuntimeError("evaluation requires kaggle-environments==1.32.7")
    from kaggle_environments import make

    records = []
    for seed in range(args.seed, args.seed + args.games // 2):
        for seat in (0, 1):
            with ExitStack() as stack:
                workers = [AgentProcess(args.agent_a), AgentProcess(args.agent_b)]
                for worker in workers:
                    stack.callback(worker.close)
                if seat:
                    workers.reverse()

                # Real function signatures let the reference runner pass configuration.
                def first(observation, configuration):
                    return workers[0](observation, configuration)

                def second(observation, configuration):
                    return workers[1](observation, configuration)

                environment = make("kaggriculture", configuration={"seed": seed}, debug=False)
                environment.run([first, second])
                last = environment.steps[-1]
                records.append(
                    {
                        "seed": seed,
                        "a_seat": seat,
                        "rewards": [s.reward for s in last],
                        "statuses": [s.status for s in last],
                    }
                )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps({"games": len(records), "output": str(args.output)}))


if __name__ == "__main__":
    main()
