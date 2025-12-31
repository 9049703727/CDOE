from pathlib import Path
import re
p = Path('templates')
changed = []
pattern = re.compile(r"\{\%\s*static\s*\x01([^'\"]*?)'\s*\%\}")
for f in p.glob('*.html'):
    s = f.read_text(encoding='utf-8')
    new = pattern.sub(lambda m: "{% static '"+m.group(1)+"' %}", s)
    # also fix cases with double quote at end (unlikely but safe)
    new = re.sub(r"\{\%\s*static\s*\x01([^'\"]*?)\"\s*\%\}", lambda m: "{% static '"+m.group(1)+"' %}", new)
    if new != s:
        f.write_text(new, encoding='utf-8')
        changed.append(str(f))
print('fixed:', changed)
