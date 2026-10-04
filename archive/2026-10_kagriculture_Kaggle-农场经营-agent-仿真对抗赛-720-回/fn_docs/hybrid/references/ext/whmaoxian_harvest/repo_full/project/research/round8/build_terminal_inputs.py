from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]
base=(root/'experiments/round8_fullfusion.py').read_bytes()
assert hashlib.sha256(base).hexdigest()=='8fd54efa56048cc63bdbc80d35b0817a789da9de2a2aad8134c35c97650fe347'
suffix=(root/'experiments/round8_terminal_inputs_suffix.txt').read_text(encoding='utf-8-sig').encode()
source=base+b'\n'+suffix
path=root/'experiments/round8_terminal_inputs.py';path.write_bytes(source)
ns={};exec(compile(source,str(path),'exec'),ns)
entry=[v for v in ns.values() if callable(v)][-1]
assert entry.__name__=='round8_terminal_inputs_agent'
notice=(root/'submissions/release_v7/NOTICE.txt').read_text(encoding='utf-8')+'''\n\nRound 8 experimental integration, 2026-09-22. Apache-2.0.\nMarket layers: Ahmed Berat Ozer EXP277/EXP293, sdy623/jaxa623,\nIG opening and queue closure as retained by haideptry in\nhttps://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine (version 4).\nTerminal input inspiration: busyaprime's 2026-09-21 Apache-2.0 seed-float\ntrim and fertilizer knockout experiments retained in that same source.\nLocal changes: conservative bounds retain each seed species for all future\nproductive planting opportunities plus pending retries; fertilizer purchases\nare clipped only after rejecting any visible final-day yield benefit and\nreserving native future pickups/sales. Empty order slots are preserved.\nThe unsafe current-price future crop prediction and unconditional fertilizer\nknockout have NOT been copied. Full source comments and prior notices retained.\n'''
(root/'experiments/round8_terminal_inputs_NOTICE.txt').write_text(notice,encoding='utf-8')
report={'candidate':str(path.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(source).hexdigest(),'base_sha256':hashlib.sha256(base).hexdigest(),'entry':entry.__name__,'notice':'experiments/round8_terminal_inputs_NOTICE.txt','license':'submissions/release_v7/LICENSE.txt','public_inspiration':'https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine','upstream_evidence':'exact source comments name busyaprime and Apache-2.0; no separate notebook license metadata returned by pull API'}
(root/'research/round8/terminal_inputs_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
