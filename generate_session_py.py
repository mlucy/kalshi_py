import json
import re

with open('session_head.py', 'r') as f:
    session = f.read()

def add_line(n, s=''):
    global session
    session += ' '*n + s + '\n'

with open('swagger.json', 'r') as f:
    spec = json.load(f)

for path in spec['paths']:
    if path in ['/log_in']:
        continue
    for method in spec['paths'][path]:
        obj = spec['paths'][path][method]
        fname = re.sub(r'(?<!^)(?=[A-Z])', '_', obj['operationId']).lower()
        arglist='self'
        objcode=''
        for param in obj.get('parameters', []):
            if param.get('required', False):
                arglist += f", {param['name']}"
            else:
                arglist += f", {param['name']}=None"

            if param['in'] == 'query':
                objcode += f", ('{param['name']}', {param['name']})"

        objcode = objcode[2:]
        if objcode == '':
            objcode = None
        else:
            objcode = f"dict((x, y) for x, y in [{objcode}] if y is not None)"

        add_line(4, f'def {fname}({arglist}):')

        add_line(8, f"return self.{method}(f'{path}', {objcode})")
        add_line(0)

with open('kalshi/session.py', 'w') as f:
    f.write(session)
