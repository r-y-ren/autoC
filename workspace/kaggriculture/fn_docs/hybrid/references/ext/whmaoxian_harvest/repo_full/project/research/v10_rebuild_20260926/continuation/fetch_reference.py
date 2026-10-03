"""Bounded public data download and archive listing; executes no archive code."""
from pathlib import Path
import hashlib,io,json,requests,zipfile
D=Path(__file__).resolve().parent
URL='https://www.kaggle.com/api/v1/datasets/download/raykkretzschmar/kaggriculture-reference-agents'
def fetch():
 try:
  data=bytearray()
  with requests.get(URL,stream=True,timeout=35) as response:
   response.raise_for_status()
   for chunk in response.iter_content(131072):
    data.extend(chunk)
    if len(data)>30000000:raise ValueError('Public reference archive exceeds the download cap')
  with zipfile.ZipFile(io.BytesIO(data)) as archive:
   members=[dict(name=i.filename,bytes=i.file_size) for i in archive.infolist()]
   if sum(i['bytes'] for i in members)>100000000:raise ValueError('Expanded archive exceeds cap')
  path=D/'public_reference_agents.zip'; path.write_bytes(data)
  receipt=dict(url=URL,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),members=members)
  (D/'public_reference_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
  return receipt
 except Exception as error:
  result=dict(error=repr(error),url=URL)
  (D/'public_reference_error.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
  return result
if __name__=='__main__':print(json.dumps(fetch()),flush=True)
