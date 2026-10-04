EXPECTED_SOURCE_SHA='178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a'
EXPECTED_LOADER_NAME='_final_sell_block_reorder_entrypoint'
# Two actual-loader instances keep policy globals independent.
import time
from kaggle_environments import make
from kaggle_environments.agent import get_last_callable
assert hashlib.sha256(candidate_bytes).hexdigest() == CANDIDATE_SHA == EXPECTED_SOURCE_SHA
smoke_counts, smoke_errors, smoke_peak_ms = [0, 0], [0, 0], [0.0, 0.0]
smoke_final_order_reports = [{}, {}]
def isolated_smoke_agent(seat):
    policy = get_last_callable(candidate_bytes.decode('utf-8'), path='main.py')
    assert policy.__name__ == EXPECTED_LOADER_NAME
    assert policy is policy.__globals__['agent'] is policy.__globals__['kaggle_submission_agent']
    def counted(observation, configuration):
        smoke_counts[seat] += 1
        started = time.perf_counter()
        try:
            return policy(observation, configuration)
        except Exception:
            smoke_errors[seat] += 1
            raise
        finally:
            smoke_peak_ms[seat] = max(smoke_peak_ms[seat], 1000*(time.perf_counter()-started))
            smoke_final_order_reports[seat] = dict(policy.__globals__['_FRO_REPORT'])
    return counted
runtime_env = make('kaggriculture', configuration={'episodeSteps':720,
                   'townCenterSellInterval':24, 'farmHandCostMult':1, 'seed':730017}, debug=False)
runtime_env.run([isolated_smoke_agent(0), isolated_smoke_agent(1)])
assert len(runtime_env.steps) == 720
assert all(str(row['status']) == 'DONE' for row in runtime_env.steps[-1])
assert smoke_counts == [719,719] and smoke_errors == [0,0]
assert all(report['calls'] == 719 and report['errors'] == 0 for report in smoke_final_order_reports)
demo = [{'tested_source_sha256':CANDIDATE_SHA, 'candidate_calls':smoke_counts[0],
         'opponent_calls':smoke_counts[1], 'runtime_errors':sum(smoke_errors)}]
print('Exact-source smoke:', demo, 'peak milliseconds:', smoke_peak_ms)
display(pd.DataFrame(smoke_final_order_reports).assign(seat=[0,1]))
