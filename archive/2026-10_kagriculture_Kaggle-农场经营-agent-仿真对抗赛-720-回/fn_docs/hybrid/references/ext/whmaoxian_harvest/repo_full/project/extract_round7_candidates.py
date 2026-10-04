"""Extract public notebook payloads as data only; never execute notebook code."""
import ast
import base64
import gzip
import hashlib
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
reports = []
for name, blob_key in [('ahmed_v56', 'SOURCE_BLOB'), ('orderbook', 'PAYLOAD')]:
    response = json.loads((ROOT / f'external/{name}_response.json').read_text(encoding='utf-8'))
    notebook = json.loads(response['blob']['sourceNullable'])
    tree = ast.parse(''.join(notebook['cells'][2]['source']))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            value = node.value
            if (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                    and value.func.attr == 'join' and isinstance(value.func.value, ast.Constant)
                    and value.func.value.value == ''):
                value = ast.Constant(''.join(ast.literal_eval(value.args[0])))
            try:
                values[node.targets[0].id] = ast.literal_eval(value)
            except (ValueError, TypeError):
                pass
    raw = zlib.decompress(base64.b85decode(values[blob_key]))
    expected = values.get('EXPECTED_MAIN_SHA256', values.get('EXPECTED_SHA256'))
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == expected, (name, sha, expected)
    (ROOT / f'external/{name}.py').write_bytes(raw)
    print(name, len(raw), sha, flush=True)
    pending, seen, imports, sensitive = [raw.decode('utf-8')], set(), set(), []
    while pending:
        source = pending.pop()
        digest = hashlib.sha256(source.encode()).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        audit_path = ROOT / f'external/{name}_audit_{len(seen)-1}.py'
        audit_path.write_text(source, encoding='utf-8', newline='\n')
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.add(ast.unparse(node))
            if isinstance(node, ast.Call):
                func = ast.unparse(node.func)
                if func.split('.')[-1] in {'exec','eval','compile','open','__import__','read_text','write_text','read_bytes','write_bytes','system','popen','run','getenv'}:
                    sensitive.append({'file':audit_path.name,'line':node.lineno,'call':ast.unparse(node)[:300]})
            if not isinstance(node, ast.Constant) or not isinstance(node.value, (str,bytes)) or len(node.value)<200:
                continue
            payloads = []
            if isinstance(node.value,str) and ('def ' in node.value or 'import ' in node.value):
                payloads.append(node.value)
            for decode in (base64.b85decode,base64.b64decode):
                for decompress in (zlib.decompress,gzip.decompress):
                    try:
                        payloads.append(decompress(decode(node.value)).decode())
                    except Exception:
                        pass
            for candidate in payloads:
                try:
                    parsed = ast.parse(candidate)
                except (SyntaxError,ValueError):
                    continue
                if any(isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.Import,ast.ImportFrom)) for n in parsed.body):
                    pending.append(candidate)
    reports.append({'name':name,'sha256':sha,'bytes':len(raw),'decoded_python_units':len(seen),'imports':sorted(imports),'sensitive_calls':sensitive})
    print('imports', name, sorted(imports), flush=True)
(ROOT / 'research/round7/source_audit.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
