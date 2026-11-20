"""Stops the build if projects.json has a mistake, so a broken page is never published."""
import json,os,sys
req=['id','reg_','suburb','pc','ll','price','img','pts','b','ba','c','title']
regs={'south','west','north','coast'}
errs=[];ids=set()
data=json.load(open('projects.json'))
for o in data:
    n=o.get('id','?')
    for k in req:
        if k not in o: errs.append(f'{n}: missing field "{k}"')
    if n in ids: errs.append(f'{n}: duplicate id')
    ids.add(n)
    if o.get('reg_') not in regs: errs.append(f'{n}: reg_ must be one of {sorted(regs)}')
    if o.get('dev') and (len(o['dev'])!=1 or not o['dev'].isalpha()): errs.append(f'{n}: dev must be one letter')
    for k in ('img','plan','interior'):
        f=o.get(k) or (f'i_{n}.jpg' if k=='interior' else '')
        if f and not os.path.exists('images/'+f): errs.append(f'{n}: image not found images/{f}')
    if not o.get('plan'): errs.append(f'{n}: no floor plan (field "plan")')
if errs:
    print('\n'.join(errs));sys.exit(1)
print('OK',len([o for o in data if o.get("status","active")=="active"]),'active packages')
