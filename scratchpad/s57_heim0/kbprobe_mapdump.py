import sys
from pathlib import Path
sys.path.insert(0, "tools")
from map_encode import parse_map26
for name in sys.argv[1:]:
    p = Path(f"maps/{name}.map26")
    w,h,rows,cores = parse_map26(p)
    print(f"== {name} {w}x{h} cores={cores}")
    ch = {0:'.',1:'#',2:'o'}
    for y in range(h):
        print(f"{y:2d} " + "".join(ch.get(rows[y][x],'?') for x in range(w)))
    print("   " + "".join(str(x%10) for x in range(w)))
