#!/usr/bin/env python3
"""Thread 4: tiebreak-margin flip-candidate analysis over the 21 current-era r1000 losses."""
import sys, json
sys.path.insert(0, "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad/toolkit")
from fetch_replay import fetch
from replay_lib import load_replay, game_meta, norm_team

GAMES = [
    ("2cfcb658-8c59-4473-9ee0-9971aab1f53a", 2, "nordkap"),
    ("c00e6c30-1604-4f79-9389-99919c37c16f", 3, "jackpot"),
    ("3712fb12-b052-4f1e-bc61-ae517a1585c0", 1, "saga"),
    ("c106d3d2-c401-4769-b958-b4a4cb7997ad", 3, "hive"),
    ("abbf93b4-cbca-4ba7-af80-583d628c6bed", 2, "antler"),
    ("12df1f45-3317-4ce3-bd3e-ecb2fd26f552", 1, "saga"),
    ("12df1f45-3317-4ce3-bd3e-ecb2fd26f552", 3, "drumlin"),
    ("17622ae0-d28d-480b-bf12-334997b95116", 1, "saga"),
    ("17622ae0-d28d-480b-bf12-334997b95116", 3, "heart"),
    ("17622ae0-d28d-480b-bf12-334997b95116", 5, "jackpot"),
    ("3b2c12df-d6b2-4ac0-a788-6edb8d4a3876", 3, "atoll"),
    ("15cabb2e-219e-4c10-b559-bfdf0d1308a6", 5, "fjordgate"),
    ("c2e57b46-13ed-46be-9a85-c6e3d5af9acd", 4, "eider"),
    ("2618b9b4-c4b8-47f6-acbc-bee5cff5d25f", 2, "saga"),
    ("2618b9b4-c4b8-47f6-acbc-bee5cff5d25f", 3, "atoll"),
    ("2618b9b4-c4b8-47f6-acbc-bee5cff5d25f", 4, "drumlin"),
    ("57d5f794-d52f-499c-a04e-3b5d0f60a351", 1, "antler"),
    ("706faea6-52be-46bf-9b2f-e8d084fc85ed", 1, "eider"),
    ("706faea6-52be-46bf-9b2f-e8d084fc85ed", 3, "hive"),
    ("706faea6-52be-46bf-9b2f-e8d084fc85ed", 4, "snowflake"),
    ("ad08eb70-4926-4d8a-b459-b48ace96f56c", 2, "jackpot"),
]

HARVESTER_BASE_COST = 20
ANCHOR_ROUND = 960          # "endgame" anchor for both lever (a) and lever (b)
END_ROUND = 999             # last round index (1000 rounds, 0-indexed)
REACH_N = 12                # Chebyshev-distance "roughly reachable by a builder" threshold


def occupied_tiles(r, rnd):
    """Building-occupied tiles (non-builder_bot entities alive at rnd) + core footprints."""
    occ = set()
    for e in r.entities.values():
        if e.kind == "builder_bot":
            continue
        if e.alive_at(rnd):
            occ.add(e.pos_at(rnd))
    occ |= r.core_footprint(0)
    occ |= r.core_footprint(1)
    return occ


def is_empty(r, pos, occ):
    x, y = pos
    if not (0 <= x < r.width and 0 <= y < r.height):
        return False
    if pos in r.walls:
        return False
    if pos in occ:
        return False
    return True


def cheby(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def analyze(mid, game, expect_map):
    meta = game_meta(mid, game)
    assert meta["mapName"] == expect_map, (mid, game, meta["mapName"], expect_map)
    us = meta["our_side"]
    them = 1 - us
    path = fetch(mid, game)
    r = load_replay(path)
    n = r.n_rounds
    assert n == 1000, (mid, game, n)

    delivered_us = r.delivered_curve(us)[-1]
    delivered_them = r.delivered_curve(them)[-1]
    harv_us = r.count_curve(us, "harvester")[-1]
    harv_them = r.count_curve(them, "harvester")[-1]
    stored_us = r.titanium_curve(us)[-1]
    stored_them = r.titanium_curve(them)[-1]

    d_delta = delivered_us - delivered_them
    h_delta = harv_us - harv_them
    s_delta = stored_us - stored_them

    if d_delta != 0:
        decider = "1-delivered"
    elif h_delta != 0:
        decider = "2-harvesters"
    elif s_delta != 0:
        decider = "3-stored"
    else:
        decider = "4-coinflip"

    # ---- lever (a): endgame spend-switch at r960 ----
    bank_960 = r.titanium_curve(us)[ANCHOR_ROUND]
    h960 = r.count_curve(us, "harvester")[ANCHOR_ROUND]
    bank = bank_960
    h = h960
    k_afford = 0
    while True:
        cost = int((1 + 0.05 * h) * HARVESTER_BASE_COST)
        if bank >= cost:
            bank -= cost
            h += 1
            k_afford += 1
        else:
            break
    production_per_harvester = ((1000 - ANCHOR_ROUND) // 4) * 10   # 100 Ti (task formula)
    a_total_delivered_if_max = k_afford * production_per_harvester

    # Full tiebreak-order simulation: k harvesters built at r960, each adding
    # production_per_harvester to delivered AND +1 to our final harvester count.
    # (Correctly falls through delivered-tie -> harvester-count -> stored, so a
    # game already tied on delivered flips on k=1 via tiebreak #1, not on
    # however many harvesters it takes to out-count the opponent on tiebreak #2.)
    def outcome(k):
        d_us = delivered_us + k * production_per_harvester
        h_us = harv_us + k
        if d_us != delivered_them:
            return d_us > delivered_them
        if h_us != harv_them:
            return h_us > harv_them
        if stored_us != stored_them:
            return stored_us > stored_them
        return None  # still a coinflip

    a_flip_k = None
    a_flip_lever = None
    for k in range(1, k_afford + 1):
        res = outcome(k)
        if res is True:
            a_flip_k = k
            d_us_k = delivered_us + k * production_per_harvester
            a_flip_lever = "delivered" if d_us_k != delivered_them else "harvester-count"
            break
    a_flippable = a_flip_k is not None

    # ---- lever (b): harvester-adjacent conveyor splice at r960 ----
    occ960 = occupied_tiles(r, ANCHOR_ROUND)
    their_harvesters_960 = [e for e in r.entities.values()
                             if e.kind == "harvester" and e.team == them and e.alive_at(ANCHOR_ROUND)]
    our_builders_960 = [e.pos_at(ANCHOR_ROUND) for e in r.entities.values()
                         if e.kind == "builder_bot" and e.team == us and e.alive_at(ANCHOR_ROUND)]

    spliceable = 0
    for hv in their_harvesters_960:
        pos = hv.pos_at(ANCHOR_ROUND)
        adj = [(pos[0], pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1])]
        empties = [a for a in adj if is_empty(r, a, occ960)]
        if not empties:
            continue
        if not our_builders_960:
            continue
        reachable = any(min(cheby(a, b) for b in our_builders_960) <= REACH_N for a in empties)
        if reachable:
            spliceable += 1

    remaining_rounds = 1000 - ANCHOR_ROUND
    diverted_per_harvester = remaining_rounds * 2.5 * 0.5   # 50 Ti diverted
    b_swing_per_harvester = 2 * diverted_per_harvester       # double swing = 100 Ti
    b_total_swing = spliceable * b_swing_per_harvester

    b_flippable = False
    b_flip_n = None
    if decider == "1-delivered" and d_delta < 0:
        need_swing = -d_delta
        import math
        nn = math.ceil(need_swing / b_swing_per_harvester) if b_swing_per_harvester else None
        if nn is not None and nn <= spliceable:
            b_flippable = True
            b_flip_n = nn

    # ---- lever (c): one more delivered stack ----
    deficit = -d_delta if d_delta < 0 else 0   # Ti we'd need on top of delivered to tie/flip tiebreak1
    c_flip_k1 = deficit <= 10 and deficit > 0
    c_flip_k5 = deficit <= 50 and deficit > 0
    c_flip_k19 = deficit <= 190 and deficit > 0
    # also record smallest k (in stacks of 10) that would flip, if any within 19
    c_min_stacks = None
    if deficit > 0:
        import math
        c_min_stacks = math.ceil(deficit / 10)

    return {
        "mid": mid, "mid8": mid[:8], "game": game, "map": expect_map,
        "opponent": meta["opponent"], "our_side": meta["our_side_name"],
        "our_version": meta["our_version"], "opponent_version": meta["opponent_version"],
        "current_line": meta["our_version"] is not None and meta["our_version"] >= 59,
        "delivered_us": delivered_us, "delivered_them": delivered_them, "d_delta": d_delta,
        "harv_us": harv_us, "harv_them": harv_them, "h_delta": h_delta,
        "stored_us": stored_us, "stored_them": stored_them, "s_delta": s_delta,
        "decider": decider,
        "bank_960": bank_960, "h960": h960, "k_afford": k_afford,
        "a_total_delivered_if_max": a_total_delivered_if_max,
        "a_flippable": a_flippable, "a_flip_k": a_flip_k, "a_flip_lever": a_flip_lever,
        "their_harvesters_960_n": len(their_harvesters_960),
        "spliceable": spliceable, "b_total_swing": b_total_swing,
        "b_flippable": b_flippable, "b_flip_n": b_flip_n,
        "deficit": deficit,
        "c_flip_k1": c_flip_k1, "c_flip_k5": c_flip_k5, "c_flip_k19": c_flip_k19,
        "c_min_stacks": c_min_stacks,
    }


def main():
    results = []
    for mid, game, mapname in GAMES:
        res = analyze(mid, game, mapname)
        results.append(res)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
