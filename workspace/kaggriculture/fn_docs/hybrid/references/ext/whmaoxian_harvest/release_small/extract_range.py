import json, hashlib, struct, zlib, os

PARTSZ = 536870912
es = json.load(open('central_directory.json'))
by_name = {e['name']: e for e in es}

part1 = open('kaggriculture-complete-20261001.zip.part001','rb')

def read_zip_bytes(entry):
    off = entry['lhoff']
    assert off + 30 + len(entry['name']) + entry['csize'] <= PARTSZ, 'spans beyond part001'
    part1.seek(off)
    hdr = part1.read(30)
    assert hdr[:4] == b'PK\x03\x04', 'bad local header'
    nlen = int.from_bytes(hdr[26:28],'little'); elen = int.from_bytes(hdr[28:30],'little')
    name = part1.read(nlen); part1.read(elen)
    raw = part1.read(entry['csize'])
    return name, raw

targets = [
    'kaggriculture/checkpoints/round10_20260923_150427.zip',
    'kaggriculture/checkpoints/round10_latest.json',
    'kaggriculture/checkpoint_round10.py',
    'kaggriculture/checkpoints/round9_latest.json',
]
os.makedirs('../checkpoint_sample', exist_ok=True)
for t in targets:
    if t not in by_name:
        print('MISSING in CD:', t); continue
    e = by_name[t]
    try:
        name, raw = read_zip_bytes(e)
    except AssertionError as ex:
        print('SKIP', t, ex); continue
    print(f"{t}: local-name={name.decode()!r} method={e['method']} raw={len(raw):,}B")
    if e['method'] == 8:
        data = zlib.decompress(raw, -15)
    elif e['method'] == 0:
        data = raw
    else:
        print('  unknown method', e['method']); continue
    crc = zlib.crc32(data) & 0xFFFFFFFF
    ok = 'OK' if crc == e['crc'] else 'BAD(%08x vs %08x)' % (crc, e['crc'])
    print(f"  inflated={len(data):,}B crc={ok}")
    out = os.path.join('../checkpoint_sample', t.split('/')[-1])
    open(out,'wb').write(data)
    h = hashlib.sha256(data).hexdigest()
    print(f"  saved {out} sha256={h}")
