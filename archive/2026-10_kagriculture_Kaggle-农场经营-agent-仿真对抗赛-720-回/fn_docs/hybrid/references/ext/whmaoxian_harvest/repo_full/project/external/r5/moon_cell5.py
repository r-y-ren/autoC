# The public source is the experiment; keep its bytes unchanged.
candidate_bytes = AGENT_SOURCE if isinstance(AGENT_SOURCE, bytes) else AGENT_SOURCE.encode('utf-8')
CANDIDATE_SHA = hashlib.sha256(candidate_bytes).hexdigest()
Path('main.py').write_bytes(candidate_bytes)
compile(candidate_bytes, 'main.py', 'exec')
print('Source bytes:', len(candidate_bytes), 'SHA256:', CANDIDATE_SHA)
