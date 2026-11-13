#!/usr/bin/env python3
"""Link schematic/PCB drawing-sheet fields to native project text variables.

Edits only each title_block and the project's text_variables. PCB geometry,
layout settings, and the current title/date/revision/company values are kept.
Change shared values in KiCad's Project Text Variables, not the placeholders.
"""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
NAME='Relay-Switched LPF'
project_path=ROOT/(NAME+'.kicad_pro')
project=json.loads(project_path.read_text())
variables=project.setdefault('text_variables',{})
mapping={'title':'DOC_TITLE','date':'DOC_DATE','rev':'DOC_REVISION','company':'DOC_COMPANY'}
defaults={'title':NAME,'date':'2026-11-13','rev':'0.0.1','company':'Lee Bussy [AA0NT]'}
def block(text):
    start=text.find('(title_block')
    if start<0:raise ValueError('Expected an existing title block')
    depth=0;quoted=False;escaped=False
    for i in range(start,len(text)):
        c=text[i]
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth==0:return start,i+1
    raise ValueError('Unbalanced title block')
paths=[ROOT/(NAME+'.kicad_sch'),ROOT/(NAME+'.kicad_pcb')]
texts=[path.read_text() for path in paths]
for field,var in mapping.items():
    if var in variables:continue
    for text in texts:
        a,b=block(text)
        match=re.search(r'\('+field+r'\s+("(?:\\.|[^"\\])*")\)',text[a:b])
        value=json.loads(match[1]) if match else ''
        if value and not value.startswith('${'):
            variables[var]=value;break
    else:variables[var]=defaults[field]
for number in range(1,10):
    var=f'DOC_COMMENT{number}'
    if var in variables:continue
    value=''
    for text in texts:
        a,b=block(text)
        match=re.search(r'\(comment\s+'+str(number)+r'\s+("(?:\\.|[^"\\])*")\)',text[a:b])
        candidate=json.loads(match[1]) if match else ''
        if candidate and not candidate.startswith('${'):value=candidate;break
    variables[var]=value
fields='\n'.join(f'    ({field} "${{{var}}}")' for field,var in mapping.items())
fields+='\n'+'\n'.join(f'    (comment {number} "${{DOC_COMMENT{number}}}")' for number in range(1,10))
replacement='(title_block\n'+fields+'\n  )'
for path,text in zip(paths,texts):
    a,b=block(text)
    path.write_text(text[:a]+replacement+text[b:])
project_path.write_text(json.dumps(project,indent=2)+'\n')
print('Title, date, revision, company, and nine comments use shared DOC_* project variables.')
