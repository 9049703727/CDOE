import re
from pathlib import Path
p = Path('templates')
files = list(p.glob('*.html'))
changed = []
for f in files:
    s = f.read_text(encoding='utf-8')
    new = re.sub(r"\{\%\s*static\s*(['\"])assets/","{% static \1", s)
    if new != s:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))
print('changed files:', changed)
