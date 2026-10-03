import ast, hashlib, json

MAIN = WORKDIR / 'main.py'
EXPECTED_MAIN_SHA256 = 'a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e'
source_bytes = MAIN.read_bytes().replace(b'\r\n', b'\n')
MAIN.write_bytes(source_bytes)
assert hashlib.sha256(source_bytes).hexdigest() == EXPECTED_MAIN_SHA256, 'main.py integrity check failed.'
compile(source_bytes, 'main.py', 'exec')

imports, trees = set(), [ast.parse(source_bytes)]
while trees:
    for node in ast.walk(trees.pop()):
        if isinstance(node, ast.Import):
            imports.update(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module
            imports.add(node.module.split('.')[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'exec':
            assert isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)
            trees.append(ast.parse(node.args[0].value))
assert imports <= sys.stdlib_module_names, 'A non-standard-library import was found.'
namespace = {}
exec(compile(source_bytes, '<v38>', 'exec'), namespace)
entry = [value for value in namespace.values() if callable(value)][-1]
assert entry is namespace['agent'], 'The final callable is not the tested agent.'
assert isinstance(entry({}), dict), 'Safe fallback check failed.'
print('PASS: source hash, Python syntax, embedded imports and entry point.', flush=True)
