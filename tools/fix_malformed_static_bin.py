from pathlib import Path
p = Path('templates')
changed = []
replacements = [
    (b"{% static \xef\xbf\xbd", b"{% static '") , # U+FFFD (utf-8 EF BF BD)
    (b"{% static \x01", b"{% static '"),
    (b"{% static \x1a", b"{% static '")
]
for f in p.glob('*.html'):
    b = f.read_bytes()
    new = b
    for a,bv in replacements:
        new = new.replace(a, bv)
    if new != b:
        f.write_bytes(new)
        changed.append(str(f))
print('fixed (binary):', changed)
