import sys, json, glob
rs = []
for f in glob.glob(sys.argv[1] if len(sys.argv) > 1 else 'sweep/s*.jsonl'):
    rs += [json.loads(l) for l in open(f)]
rs.sort(key=lambda r: -r['ratio'])
print(len(rs), 'configs')
for r in rs[:8]:
    print(r['ratio'], r['cfg'])
if rs:
    print('worst', rs[-1]['ratio'])
