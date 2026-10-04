"""Download only the public Kaggriculture reference-agent data set."""
from pathlib import Path
import hashlib,io,json,requests,zipfile
OUT=Path(__file__).resolve().parent/'reference_agents';OUT.mkdir(exist_ok=True)
url='https://www.kaggle.com/api/v1/datasets/download/raykkretzschmar/kaggriculture-reference-agents'
response=requests.get(url,timeout=90);response.raise_for_status();data=response.content
assert len(data)<50000000,'Unexpectedly large reference dataset'
(OUT/'public_dataset.zip').write_bytes(data)
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    assert sum(info.file_size for info in archive.infolist())<100000000
    for info in archive.infolist():
        path=OUT/info.filename
        assert path.resolve().is_relative_to(OUT.resolve()),'Unsafe archive path'
        if info.is_dir():path.mkdir(parents=True,exist_ok=True);continue
        if path.suffix.lower() not in ('.py','.json','.csv','.md','.txt','.gz'):continue
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(archive.read(info))
    names=archive.namelist()
(OUT/'provenance.json').write_text(json.dumps(dict(url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),files=names),indent=2),encoding='utf-8')
print('Public reference files',names,flush=True)
