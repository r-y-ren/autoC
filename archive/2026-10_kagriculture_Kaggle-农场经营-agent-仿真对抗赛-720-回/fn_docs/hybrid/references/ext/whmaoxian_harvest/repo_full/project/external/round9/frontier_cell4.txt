import base64, hashlib, json, lzma
namespace = {}
exec(compile(AGENT_SOURCE, 'main.py', 'exec'), namespace)
Path('LICENSE.txt').write_text(LICENSE_TEXT, encoding='utf-8', newline='\n')
print('Compiled public source:', len(AGENT_SOURCE), 'bytes')
print('Callable exports:', sum(callable(v) for v in namespace.values()))
