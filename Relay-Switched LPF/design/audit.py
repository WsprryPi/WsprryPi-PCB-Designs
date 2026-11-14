#!/usr/bin/env python3
"""Audit exported net membership, saved PCB parity, and default RF paths.

Uses only Python's standard library. Expected connections are enumerated here,
independently of the generator's connections.json. This is a topology audit,
not an electromagnetic, switching-transient, or physical test.
"""
from pathlib import Path
from collections import defaultdict, deque
import json
import re
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
expected={}
def add(ref,net,*pins):
    for pin in pins: expected[(ref,str(pin))]=net
for pin,net in enumerate(['+5V','BAND5_N','BAND3_N','BAND4_N','BAND1_N','BAND2_N','GND','RFI','GND','RFO'],1): add('J1',net,pin)
add('W1','+5V',1);add('W1','RELAY_VPLUS',2)
add('W7','RFO',1);add('W7','FINAL_NC',2);add('W7','GND',3)
add('W8','GND',1);add('W8','GND_OUT',2)
add('W9','LPF1_OUT',1);add('W9','FINAL_RELAY_COM',2)
for ref in ['X1','X2','J26']: add(ref,'LPF1_OUT',1);add(ref,'GND_OUT',2)
for i in range(1,6):
    r=f'RL{i}'
    for pin,net in [(1,'RELAY_VPLUS'),(12,f'BAND{i}_N'),(8,'RFI'),(9,f'LPF{i}_IN'),(10,'FINAL_NC' if i==1 else 'GND'),(3,'GND'),(4,'FINAL_RELAY_COM' if i==1 else f'LPF{i}_OUT'),(5,f'RELAY{i}_OUT')]: add(r,net,pin)
    add(f'D{i}','RELAY_VPLUS',1);add(f'D{i}',f'BAND{i}_N',2)
    add(f'J{i*2}','GND',1,2);add(f'J{i*2}',f'LPF{i}_IN',3,4)
    add(f'J{i*2+1}',f'LPF{i}_OUT',1,2);add(f'J{i*2+1}','GND_OUT' if i==1 else 'GND',3,4)
    add(f'W{i+1}',f'RELAY{i}_OUT',1);add(f'W{i+1}','RFO',2);add(f'W{i+1}',f'ANT{i}',3)
    add(f'J{20+i}',f'ANT{i}',1);add(f'J{20+i}','GND',2)

doc=ET.parse(root/'generated/connectivity.xml')
actual={}
for net in doc.findall('.//nets/net'):
    for node in net.findall('node'): actual[(node.get('ref'),node.get('pin'))]=net.get('name').lstrip('/')
assert actual==expected, f'Schematic mismatch: {set(actual.items()) ^ set(expected.items())}'

def parse(text):
    stack=[]; result=None
    for token in re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',text):
        if token=='(':
            item=[]
            if stack: stack[-1].append(item)
            stack.append(item)
        elif token==')': result=stack.pop()
        else: stack[-1].append(json.loads(token) if token.startswith('"') else token)
    return result
def children(obj,key): return [v for v in obj if isinstance(v,list) and v and v[0]==key]
pcb=parse((root/'Relay-Switched LPF.kicad_pcb').read_text())
board={}
for fp in children(pcb,'footprint'):
    ref=next(v[2] for v in children(fp,'property') if v[1]=='Reference')
    if ref.startswith('H'): continue
    for pad in children(fp,'pad'):
        net=children(pad,'net')[0][1].lstrip('/')
        key=(ref,pad[1])
        assert key not in board or board[key]==net, f'Duplicate numbered pad has conflicting net: {key}'
        board[key]=net
assert board==expected, f'Board mismatch: {set(board.items()) ^ set(expected.items())}'

paths={}
for selected in range(6):
    graph=defaultdict(list)
    def edge(a,bb,label=''):
        graph[a].append((bb,label));graph[bb].append((a,label))
    for i in range(1,6):
        r=f'RL{i}'
        for com,no,nc in [(9,8,10),(4,5,3)]:
            edge(expected[(r,str(com))],expected[(r,str(no if i==selected else nc))])
        edge(f'LPF{i}_IN',f'LPF{i}_OUT',f'LPF{i}')
    for ref in ['W1','W3','W4','W5','W6','W7']: edge(expected[(ref,'1')],expected[(ref,'2')])
    start='RFO' if selected==0 else 'RFI'
    queue=deque([(start,[])]); seen={start}; found=None
    while queue:
        node,filters=queue.popleft()
        if node=='LPF1_OUT': found=filters;break
        for target,label in graph[node]:
            if target not in seen:
                seen.add(target);queue.append((target,filters+([label] if label else [])))
    wanted=['LPF1'] if selected in [0,1] else [f'LPF{selected}','LPF1']
    assert found==wanted,(selected,found,wanted)
    # Check grounding separately without stopping the traversal at the output.
    queue=deque([start]);seen={start}
    while queue:
        for target,_ in graph[queue.popleft()]:
            if target not in seen: seen.add(target);queue.append(target)
    assert 'GND' not in seen and 'GND_OUT' not in seen, f'Selected RF path grounded in state {selected}'
    paths[selected]=found
print(f'PASS: {len(expected)} unique component pins, {len(set(expected.values()))} nets; schematic and PCB agree.')
print('PASS: default filter paths for external band 0 and selected bands 1-5:',paths)

# The delivered folder must resolve every part without global CAD libraries.
local='relay-switched-lpf'
symbols=parse((root/(local+'.kicad_sym')).read_text())
symbol_names={v[1] for v in children(symbols,'symbol')}
schematic=parse((root/'Relay-Switched LPF.kicad_sch').read_text())
for inst in children(schematic,'symbol'):
    lib_id=children(inst,'lib_id')[0][1]
    assert lib_id.startswith(local+':') and lib_id.split(':',1)[1] in symbol_names,lib_id
bare={*[f'H{i}' for i in range(1,5)],*[f'J{i}' for i in range(21,27)],'W2','W8','W9'}
model_count=0;footprint_count=0;assets=set()
for fp in children(pcb,'footprint'):
    footprint_count+=1
    ref=next(v[2] for v in children(fp,'property') if v[1]=='Reference')
    assert fp[1].startswith(local+':'),(ref,fp[1])
    name=fp[1].split(':',1)[1]
    assert (root/(local+'.pretty')/(name+'.kicad_mod')).exists(),(ref,name)
    models=children(fp,'model')
    assert bool(models)==(ref not in bare),(ref,'unexpected model population')
    for model in models:
        assert model[1].startswith('${KIPRJMOD}/'),model[1]
        target=root/model[1][len('${KIPRJMOD}/'):]
        assert target.is_file(),target
        model_count+=1;assets.add(target.name)
for footprint in (root/(local+'.pretty')).glob('*.kicad_mod'):
    for model in children(parse(footprint.read_text()),'model'):
        assert model[1].startswith('${KIPRJMOD}/'),(footprint,model[1])
        assert (root/model[1][len('${KIPRJMOD}/'):]).is_file(),(footprint,model[1])
print(f'PASS: {footprint_count} local footprints; {model_count} model instances / {len(assets)} local assets; all schematic symbols local.')
