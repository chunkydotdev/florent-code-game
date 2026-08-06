import re, html, urllib.request, sys

# NOTE: enumerate these from the /docs index page, NOT from the JS bundle --
# the bundle only lists a subset of the routes (this cost us 10 pages once).
#   curl -sL https://game.code.florent.vc/docs | grep -oE 'href="/docs/[a-z0-9/_-]*"' | sort -u
DOCS = """florent-code-league quick-start
game-rules-overview game-rules-core game-rules-builder-bot game-rules-turrets
game-rules-conveyors game-rules-harvester game-rules-other-buildings
game-rules-resources game-rules-reference
global-comms robot-api api-types agents-md
platform-matches platform-ladder platform-submitting
cli-installation cli-first-bot cli-running-matches cli-reference cli-submitting""".split()

TUTS = """movement-sensing/01-welcome movement-sensing/02-spawning movement-sensing/03-moving
movement-sensing/04-sensing movement-sensing/05-recap
harvesting-titanium/01-the-titanium-economy harvesting-titanium/02-finding-ore
harvesting-titanium/03-building-a-harvester harvesting-titanium/04-cost-scaling
harvesting-titanium/05-recap
conveyors-logistics/01-why-routing-matters conveyors-logistics/02-building-a-conveyor-chain
conveyors-logistics/03-the-last-mile conveyors-logistics/04-splitting-the-flow
conveyors-logistics/05-recap
turrets-combat/01-meet-the-turrets turrets-combat/02-building-a-gunner
turrets-combat/03-the-ammo-gap turrets-combat/04-healing-and-sabotage turrets-combat/05-recap
comms-strategy/01-the-global-communication-store comms-strategy/02-coordinating-roles
comms-strategy/03-putting-it-together comms-strategy/04-where-to-go-from-here""".split()

BLOCKS = []


def detag(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def stash_pre(m):
    parts = re.split(r'<span class="line">', m.group(0))[1:]
    lines = [detag(p.rsplit("</span>", 1)[0]).rstrip() for p in parts]
    if not lines:
        lines = [detag(m.group(0))]
    BLOCKS.append("\n".join(lines).strip("\n"))
    return f"\n\n@@CODE{len(BLOCKS)-1}@@\n\n"


def extract(h):
    m = re.search(r"<main.*?</main>", h, re.S)
    body = m.group(0) if m else h
    body = re.sub(r"(?s)<(script|style|nav|head|aside)\b.*?</\1>", "", body)
    body = re.sub(r"(?s)<pre\b.*?</pre>", stash_pre, body)
    body = re.sub(r"(?s)<(h[1-6])[^>]*>(.*?)</\1>", lambda m: "\n\n### " + detag(m.group(2)).strip() + "\n\n", body)
    body = re.sub(r"(?s)<li[^>]*>", "\n- ", body)
    body = re.sub(r"(?s)</t[dh]>", " | ", body)
    body = re.sub(r"(?s)</tr>", "\n", body)
    body = re.sub(r"(?s)</(p|div|li|ul|ol|table|section)>", "\n", body)
    body = re.sub(r"<br\s*/?>", "\n", body)
    txt = detag(body)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n[ \t]+", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    txt = re.sub(r"@@CODE(\d+)@@", lambda m: "```\n" + BLOCKS[int(m.group(1))] + "\n```", txt)
    return txt.strip()


def grab(url, label, out):
    try:
        h = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
    except Exception as e:
        out.append(f"\n\n=== {label} ===\nERROR {e}\n")
        return
    t = extract(h)
    i = t.find("· Step")
    j = t.find("### ")
    cut = i if i > 0 else (j if j > 0 else 0)
    out.append(f"\n\n\n=== {label} ===\n" + t[cut:].strip())
    print("ok", label, file=sys.stderr)


docs = []
for d in DOCS:
    grab("https://game.code.florent.vc/docs/" + d, "docs/" + d, docs)
open("docs.md", "w").write("\n".join(docs))

tuts = []
for t in TUTS:
    grab("https://game.code.florent.vc/tutorials/" + t, "tutorials/" + t, tuts)
open("tutorials-clean.md", "w").write("\n".join(tuts))
print("done")
