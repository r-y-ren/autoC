"""JSON defaults with explicit command-line overrides."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def parse_config_args(parser: argparse.ArgumentParser, argv: Sequence[str] | None = None) -> argparse.Namespace:
    preliminary = argparse.ArgumentParser(add_help=False)
    preliminary.add_argument("--config", type=Path)
    config, _ = preliminary.parse_known_args(argv)
    parser.add_argument("--config", type=Path, help="JSON defaults; command-line flags take precedence")
    if config.config is None:
        return parser.parse_args(argv)
    values = json.loads(config.config.read_text())
    if not isinstance(values, dict):
        parser.error("the config must be a JSON object")
    actions = {action.dest: action for action in parser._actions}
    unknown = values.keys() - actions.keys()
    if unknown:
        parser.error(f"unknown config fields: {', '.join(sorted(unknown))}")
    for name, value in values.items():
        action = actions[name]
        if isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse.BooleanOptionalAction)):
            if not isinstance(value, bool):
                parser.error(f"{name} must be boolean")
        elif action.type is not None and value is not None:
            value = action.type(value)
        if action.choices is not None and value not in action.choices:
            parser.error(f"invalid value for {name}: {value!r}")
        values[name] = value
        action.required = False
    parser.set_defaults(**values)
    return parser.parse_args(argv)
