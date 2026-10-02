"""Private JSON-lines worker used by evaluate.py to isolate agent packages."""

from contextlib import redirect_stdout
import importlib.util
import json
import os
from pathlib import Path
import sys
import traceback


def main():
    os.environ["KAGGRICULTURE_RAISE_AGENT_ERRORS"] = "1"
    entry = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(entry.parent))
    with redirect_stdout(sys.stderr):
        spec = importlib.util.spec_from_file_location("_evaluation_agent", entry)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    for line in sys.stdin:
        request = json.loads(line)
        try:
            with redirect_stdout(sys.stderr):
                action = module.agent(request["observation"], request["configuration"])
            response = {"action": action}
        except Exception:
            traceback.print_exc(file=sys.stderr)
            response = {"error": "agent execution failed; see stderr"}
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
