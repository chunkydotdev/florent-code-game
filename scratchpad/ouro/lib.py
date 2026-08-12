import csv, collections, statistics
ROOT = "/Users/junghard/Projects/Work/florent-code-game"

def load(t):
    meta = {}
    for r in csv.DictReader(open(f"{ROOT}/scratchpad/ouro/files_{t}.tsv"), delimiter="\t"):
        meta[r["file"]] = r
    cen = {r["file"]: r for r in csv.DictReader(open(f"{ROOT}/scratchpad/ouro/census_{t}.tsv"), delimiter="\t")}
    out = []
    for f, m in meta.items():
        c = cen.get(f)
        if not c: continue
        r = dict(m); r.update(c)
        r["us"] = m["us_side"]; r["them"] = "b" if m["us_side"] == "a" else "a"
        r["us_i"] = 0 if m["us_side"] == "a" else 1
        r["them_i"] = 1 - r["us_i"]
        r["won"] = (c["winner"].lower() == m["us_side"])
        r["rounds"] = int(c["rounds"])
        r["ourver"] = int(m["ourver"])
        out.append(r)
    return out

def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

def num(v, default=None):
    try: return int(v)
    except Exception:
        try: return float(v)
        except Exception: return default
