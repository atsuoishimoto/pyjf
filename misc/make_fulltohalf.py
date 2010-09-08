import unicodedata

import unicodedata
chars = []
for c in range(1, 65536):
    c = unichr(c)
    name = unicodedata.name(c, '')
    if name.startswith("FULLWIDTH") or name.startswith("HALFWIDTH"):
        chars.append((name, c))


d = {}
for name, c in chars:
    p = name.split()
    if p[0] in ('HALFWIDTH', 'FULLWIDTH'):
        name = " ".join(p[1:])
    
    normal = full = half = None
    try:
        normal = unicodedata.lookup(name)
    except KeyError:
        pass
    try:
        full = unicodedata.lookup("FULLWIDTH "+name)
    except KeyError:
        pass
    
    try:
        half = unicodedata.lookup("HALFWIDTH "+name)
    except KeyError:
        pass
    
    if normal or full or half:
        d[name] = (normal, full, half)


d2 = {}

for name, (normal, full, half) in d.items():
    
    if full:
        if normal:
            pair = (full, normal)
        elif half:
            pair = (full, half)

    if half:
        if normal:
            pair = (normal, half)
        elif full:
            pair = (full, half)
    
    try:
        pair[0].encode("cp932")
        pair[1].encode("cp932")
    except UnicodeEncodeError:
        continue

    d2[name] = pair

d2['YEN SIGN'] = (u'\uffe5', u'\x5c')
l = []
for name, (full, half) in d2.items():
    print "%r:%r,\t# %s" % (full, half, name)


