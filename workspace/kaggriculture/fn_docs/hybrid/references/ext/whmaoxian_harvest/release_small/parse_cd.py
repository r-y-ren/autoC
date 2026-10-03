import struct, json

data = open('kaggriculture-complete-20261001.zip.part005','rb').read()
TOTAL = 2150343616; PARTSZ = 536870912
base = TOTAL - len(data)

z64loc = data.rfind(b'PK\x06\x07')
_, dsk, z64_off, ndisks = struct.unpack('<IIQI', data[z64loc:z64loc+20])
rel = z64_off - base
z = data[rel:rel+56]
sig, sz, vmade, vneed, d1, d2, nd, n, cds, cdo = struct.unpack('<IQHHIIQQQQ', z)
print(f'entries={n:,}, cd_size={cds:,}, cd_offset={cdo:,}')
cd = data[cdo-base:cdo+cds-base]
print('cd bytes:', len(cd))

FMT = '<4s2B2BHHHHHIIIHHHHHII'  # not used; use explicit
entries = []
i = 0
CNT = 0
while i < len(cd)-4:
    if cd[i:i+4] != b'PK\x01\x02':
        print('stop at', i, cd[i:i+4]); break
    hdr = cd[i:i+46]
    vmade = int.from_bytes(hdr[4:6],'little'); vneed = int.from_bytes(hdr[6:8],'little')
    flag = int.from_bytes(hdr[8:10],'little'); method = int.from_bytes(hdr[10:12],'little')
    crc = int.from_bytes(hdr[16:20],'little'); csize = int.from_bytes(hdr[20:24],'little')
    usize = int.from_bytes(hdr[24:28],'little')
    nlen = int.from_bytes(hdr[28:30],'little'); elen = int.from_bytes(hdr[30:32],'little')
    clen = int.from_bytes(hdr[32:34],'little')
    lhoff = int.from_bytes(hdr[42:46],'little')
    name = cd[i+46:i+46+nlen].decode('utf-8','replace')
    if usize == 0xFFFFFFFF or csize == 0xFFFFFFFF or lhoff == 0xFFFFFFFF:
        j = i+46+nlen; end = j+elen
        while j < end:
            hid = int.from_bytes(cd[j:j+2],'little'); hsz = int.from_bytes(cd[j+2:j+4],'little')
            if hid == 0x0001:
                k = j+4; avail = hsz
                if usize == 0xFFFFFFFF and avail >= 8:
                    usize = struct.unpack('<Q', cd[k:k+8])[0]; k += 8; avail -= 8
                if csize == 0xFFFFFFFF and avail >= 8:
                    csize = struct.unpack('<Q', cd[k:k+8])[0]; k += 8; avail -= 8
                if lhoff == 0xFFFFFFFF and avail >= 8:
                    lhoff = struct.unpack('<Q', cd[k:k+8])[0]; k += 8; avail -= 8
                break
            j += 4+hsz
    entries.append(dict(name=name, method=method, csize=csize, usize=usize, lhoff=lhoff, crc=crc))
    i += 46+nlen+elen+clen
    CNT += 1
print('parsed entries:', CNT)

for e in entries:
    if e['name'].startswith('checkpoints/'):
        span_start, span_end = e['lhoff'], e['lhoff']+30+len(e['name'])+e['csize']
        p1, p2 = span_start//PARTSZ+1, span_end//PARTSZ+1
        print(f"  {e['name']:<55} m={e['method']} csize={e['csize']:>13,} usize={e['usize']:>13,} lhoff={e['lhoff']:>13,} parts {p1}..{p2}")

json.dump(entries, open('central_directory.json','w'))
print('saved central_directory.json')
