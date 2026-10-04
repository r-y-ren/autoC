import json, hashlib, struct, zlib, os

PARTSZ = 536870912; TOTAL = 2150343616
es = json.load(open('central_directory.json'))
by_name = {e['name']: e for e in es}

parts = {}
def get_part(n):
    if n not in parts:
        fn = f'kaggriculture-complete-20261001.zip.part{n:03d}'
        parts[n] = open(fn,'rb')
    return parts[n]

def read_entry(entry):
    off = entry['lhoff']
    pnum = off // PARTSZ + 1
    base = (pnum-1)*PARTSZ
    f = get_part(pnum)
    f.seek(off-base)
    hdr = f.read(30)
    assert hdr[:4] == b'PK\x03\x04', 'bad local header'
    nlen = int.from_bytes(hdr[26:28],'little'); elen = int.from_bytes(hdr[28:30],'little')
    f.read(nlen); f.read(elen)
    raw = f.read(entry['csize'])
    assert len(raw) == entry['csize'], 'truncated read'
    data = zlib.decompress(raw, -15) if entry['method'] == 8 else raw
    crc = zlib.crc32(data) & 0xFFFFFFFF
    assert crc == entry['crc'], 'CRC mismatch'
    return data

targets = [
    'kaggriculture/V10反馈信息/113447926.json',
    'kaggriculture/V7反馈/111934255.json',
    'kaggriculture/V8反馈/112293400.json',
    'kaggriculture/V9反馈信息/112455606.json',
    'kaggriculture/反馈信息3/111485103.json',
]
m = json.load(open('../repo_full/ARCHIVE_MANIFEST.json'))
norm = lambda p: p.replace('\\','/')
want = {norm(f['path']): f['sha256'] for f in m['files']}

os.makedirs('../feedback_replays', exist_ok=True)
for t in targets:
    e = by_name[t]
    span_end = e['lhoff'] + 30 + len(t) + e['csize']
    pnum = e['lhoff'] // PARTSZ + 1
    pend = span_end // PARTSZ + 1
    if pend != pnum:
        print('SKIP (spans parts)', t); continue
    if pnum not in (1, 5):
        print('SKIP (part not local)', t, 'part', pnum); continue
    data = read_entry(e)
    h = hashlib.sha256(data).hexdigest()
    key = t.replace('kaggriculture/','')
    ok = h == want.get(key)
    out = os.path.join('../feedback_replays', key.replace('/','__'))
    open(out,'wb').write(data)
    print(f"{key:<45} {len(data):>12,}B sha256_manifest={'MATCH' if ok else 'MISMATCH'} -> {out}")
