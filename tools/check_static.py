import re
p='templates/base.html'
s=open(p).read()
for i,l in enumerate(s.splitlines(),1):
    if '{% static' in l:
        print(i, l.strip())
        m=re.search(r"\{\%\s*static\s*(.*?)\s*\%\}", l)
        if not m:
            print('  -> malformed static tag')
        else:
            inner=m.group(1)
            print('  -> inner:', repr(inner))
            if inner.strip()=='':
                print('  -> empty arg')
print('done')