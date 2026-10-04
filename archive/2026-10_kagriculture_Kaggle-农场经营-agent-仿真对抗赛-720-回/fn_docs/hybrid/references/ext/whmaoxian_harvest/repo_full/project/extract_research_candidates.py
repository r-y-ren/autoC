"""Decode public notebook source as data; never execute notebook cells."""
import ast
import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zlib

ROOT = Path(__file__).parent


def literal(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "join":
        return "".join(ast.literal_eval(node.args[0]))
    return ast.literal_eval(node)


for name, cell in [("ahmed_v53", 2), ("one_more_wheat", 4), ("pipe16", 6)]:
    response = json.loads((ROOT / f"external/{name}_response.json").read_text(encoding="utf-8"))
    notebook = json.loads(response["blob"]["sourceNullable"])
    tree = ast.parse("".join(notebook["cells"][cell]["source"]))
    values = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
            try:
                values[n.targets[0].id] = literal(n.value)
            except (ValueError, TypeError):
                pass
    if name == "ahmed_v53":
        raw = zlib.decompress(base64.b85decode(values["SOURCE_BLOB"]))
    elif name == "pipe16":
        raw = gzip.decompress(base64.b64decode(values["AGENT_B64"]))
    else:
        n = next(n for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == "ARCHIVE_BYTES")
        archive = base64.b64decode(ast.literal_eval(n.value.args[0]))
        assert hashlib.sha256(archive).hexdigest() == values["EXPECTED_ARCHIVE_SHA256"]
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tf:
            raw = tf.extractfile("main.py").read()
            for member in ("NOTICE.txt", "LICENSE.txt"):
                (ROOT / f"external/{name}_{member}").write_bytes(tf.extractfile(member).read())
    expected = values.get("EXPECTED_MAIN_SHA256", values.get("EXPECTED_SHA256"))
    assert hashlib.sha256(raw).hexdigest() == expected
    (ROOT / f"external/{name}.py").write_bytes(raw)
    print(name, len(raw), expected)
    # Recursively inspect literal Python payloads (encoded data arrays remain data).
    pending, seen, imports, calls = [raw.decode()], set(), set(), set()
    while pending:
        s = pending.pop()
        if s in seen:
            continue
        seen.add(s)
        tr = ast.parse(s)
        for n in ast.walk(tr):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                imports.add(ast.unparse(n))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                calls.add(n.func.id)
            if not isinstance(n, ast.Constant) or not isinstance(n.value, (str, bytes)) or len(n.value) < 400:
                continue
            payloads = []
            if isinstance(n.value, str) and ("def " in n.value or "import " in n.value):
                payloads.append(n.value)
            for decoder in (base64.b85decode, base64.b64decode):
                for decompress in (zlib.decompress, gzip.decompress):
                    try:
                        payloads.append(decompress(decoder(n.value)).decode())
                    except Exception:
                        pass
            for payload in payloads:
                try:
                    pt = ast.parse(payload)
                except (SyntaxError, ValueError):
                    continue
                if any(isinstance(v, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.ClassDef)) for v in pt.body):
                    pending.append(payload)
    print("imports", sorted(imports))
    print("sensitive call names", sorted(calls & {"exec", "eval", "open", "__import__", "compile"}))
    for i, s in enumerate(sorted(seen, key=len)):
        (ROOT / f"external/{name}_audit_{i}.py").write_text(s, encoding="utf-8")
