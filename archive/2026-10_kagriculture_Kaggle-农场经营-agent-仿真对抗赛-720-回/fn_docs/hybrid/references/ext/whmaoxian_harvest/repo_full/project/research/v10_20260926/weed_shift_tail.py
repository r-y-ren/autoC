
# V10 experiment: bounded recovery of weed-blocked native work.
# A one-action delay is permitted only with a known later PASS in this day.
_V10_WEED_ORIGINAL = Chassis._weed_repair
_V10_WEED_REPORT = {'started':0,'recovered':0,'shifted_turns':0,'planted':0,'errors':0}

def _v10_weed_repair(self, action, view, st, route, step):
    raw = [list(action.get('farmer') or ['PASS'])] + [list(c) for c in action.get('hands', [])]
    _V10_WEED_ORIGINAL(self, action, view, st, route, step)
    cmds = [action.get('farmer') or ['PASS']] + list(action.get('hands', []))
    day = step // 24
    if st.get('v10_delay_day') != day:
        st['v10_delay_day'] = day
        st['v10_delay'] = {}
    states = st['v10_delay']
    tape = self.routes[route]
    for actor, cmd in enumerate(raw[:len(view.positions)]):
        pos = tuple(view.positions[actor]); tile = _tile_at(view.tiles, pos)
        if actor not in states:
            if not (cmd and cmd[0] in ('PLANT','BUILD_COOP','BUILD_PASTURE') and isinstance(tile,dict) and tile.get('kind')=='WEED'):
                continue
            if day>=29 or step%24>20:
                continue
            spare = False
            for t in range(step+1,min((day+1)*24,719,len(tape))):
                a=tape[t]; seq=[a.get('farmer') or ['PASS']]+list(a.get('hands',[]))
                if actor>=len(seq) or not seq[actor] or seq[actor]==['PASS']:
                    spare=True;break
            if not spare:continue
            states[actor] = [cmd]
            st['pending'].pop(actor,None)
            cmds[actor] = ['DIG']
            _V10_WEED_REPORT['started'] += 1
            continue
        st['pending'].pop(actor,None)
        queue=states[actor]
        if cmd and cmd!=['PASS']:queue.append(cmd)
        inv=view.inv(actor)
        while queue:
            head=queue[0];op=head[0]
            harmless=(op=='PASS' or (op in ('WATER','CARE','COLLECT_FERTILIZER','FEED','DROP') and _is_noop(head,tile,inv,view.seeds,pos,view.board)))
            if not harmless:break
            queue.pop(0)
        if queue:
            head=queue.pop(0)
            if head[0]=='PLANT':_V10_WEED_REPORT['planted']+=1
            cmds[actor]=head
            _V10_WEED_REPORT['shifted_turns']+=1
        else:cmds[actor]=['PASS']
        if not queue:
            states.pop(actor,None)
            _V10_WEED_REPORT['recovered']+=1
    action['farmer']=cmds[0];action['hands']=cmds[1:]

Chassis._weed_repair = _v10_weed_repair
_V10_WEED_PARENT = round9_slack_agent

def v10_weed_shift_agent(observation, configuration=None):
    if int(observation['step'])==0:
        for key in _V10_WEED_REPORT:_V10_WEED_REPORT[key]=0
    return _V10_WEED_PARENT(observation, configuration)
v10_weed_shift_agent.telemetry = _V10_WEED_REPORT
agent = v10_weed_shift_agent
kaggle_submission_agent = v10_weed_shift_agent
