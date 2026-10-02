"""Build a local Kaggle archive without publishing or submitting it."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import _bootstrap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--agent-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--search-library", type=Path)
    args = parser.parse_args()
    from kaggriculture.checkpoints import load_training_source, export_policy
    import kaggriculture

    settings = json.loads(args.agent_config.read_text())
    variant = settings.get("variant")
    if variant not in {"A", "B"}:
        parser.error("agent config must select variant A or B")
    payload = load_training_source(args.checkpoint)
    if bool(payload["model_config"].get("sequential_patch", False)) != (variant == "B"):
        parser.error("checkpoint masks do not match the selected variant")
    library = args.search_library
    if variant == "A":
        library = library or Path(kaggriculture.__file__).parent / "search/terminal_search.so"
        header = library.read_bytes()[:20] if library.is_file() else b""
        if header[:4] != b"\x7fELF" or len(header) < 20 or int.from_bytes(header[18:20], "little") != 62:
            parser.error("Final A requires a Linux x86-64 search library; build it in the Linux container")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        shutil.copytree(
            Path(kaggriculture.__file__).parent,
            root / "kaggriculture",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.so", "*.pkl"),
        )
        shutil.copyfile(_bootstrap.ROOT / "python/main.py", root / "main.py")
        (root / "agent.json").write_text(json.dumps(settings, indent=2) + "\n")
        export_policy(args.checkpoint, root / "model_jax.pkl")
        if variant == "A":
            shutil.copyfile(library, root / "kaggriculture/search/terminal_search.so")
        else:
            shutil.rmtree(root / "kaggriculture/search")
        manifest = {
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*"))
            if p.is_file()
        }
        (root / "bundle-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        with tarfile.open(args.output, "w:gz") as archive:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    archive.add(path, arcname=str(path.relative_to(root)))
    print(json.dumps({"archive": str(args.output), "variant": variant, "bytes": args.output.stat().st_size}))


if __name__ == "__main__":
    main()
