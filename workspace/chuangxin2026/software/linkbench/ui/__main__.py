"""CLI：python -m linkbench.ui [--host 0.0.0.0] [--port 8000]"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.ui")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args(argv)
    from linkbench.ui.server import serve
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
