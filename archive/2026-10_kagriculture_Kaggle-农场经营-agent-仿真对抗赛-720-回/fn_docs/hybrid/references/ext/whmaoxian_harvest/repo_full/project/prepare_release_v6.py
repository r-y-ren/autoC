"""Generate the v6 release checker from the already exercised v5 checker."""
from pathlib import Path

root = Path(__file__).parent
s = (root / 'build_release_v5.py').read_text()
s = s.replace('a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e',
              '10f58185b916392ca39697c83f67f455df81a74dfb6eb1aacd60fd81d50c9970')
s = s.replace('external/ahmed_exact.py', 'external/one_more_wheat.py').replace('release_v5', 'release_v6')
s = s.replace('"release": "v5"', '"release": "v6"')
s = s.replace('Ahmed Berat Ozer V38, Kaggle Notebook version 2, unmodified', 'Dmitrii Gluzdov One More Wheat, frozen public source, unmodified')
s = s.replace('https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins',
              'https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-one-more-wheat')
s = s.replace('timeout=120', 'timeout=240')
s = s.replace('tf.addfile(info, io.BytesIO(source))', '''tf.addfile(info, io.BytesIO(source))
            for name in ("NOTICE.txt", "LICENSE.txt"):
                payload = (ROOT / ("external/one_more_wheat_" + name)).read_bytes()
                (release / name).write_bytes(payload)
                member = tarfile.TarInfo(name)
                member.size, member.mode, member.mtime = len(payload), 0o644, 0
                tf.addfile(member, io.BytesIO(payload))''')
s = s.replace('["main.py"]', '["main.py", "NOTICE.txt", "LICENSE.txt"]')
(root / 'build_release_v6.py').write_text(s, encoding='utf-8')
print('Prepared v6 checker; v5 remains unchanged.')
