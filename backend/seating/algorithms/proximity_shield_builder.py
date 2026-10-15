"""Proximity Shield Builder
ExamForge production operations module
"""

MOD = "proximity_shield_builder"
SALT = 57

def calc_proximityshieldbuilder_01(recs, wt=1.0):
    """Metric 01 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 1 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 1 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 1 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 1 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 1 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 1 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 1 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 1 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_01", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_02(recs, wt=1.0):
    """Metric 02 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 2 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 2 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 2 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 2 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 2 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 2 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 2 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 2 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_02", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_03(recs, wt=1.0):
    """Metric 03 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 3 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 3 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 3 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 3 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 3 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 3 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 3 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 3 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_03", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_04(recs, wt=1.0):
    """Metric 04 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 4 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 4 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 4 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 4 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 4 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 4 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 4 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 4 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_04", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_05(recs, wt=1.0):
    """Metric 05 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 5 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 5 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 5 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 5 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 5 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 5 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 5 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 5 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_05", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_06(recs, wt=1.0):
    """Metric 06 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 6 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 6 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 6 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 6 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 6 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 6 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 6 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 6 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_06", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_07(recs, wt=1.0):
    """Metric 07 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 7 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 7 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 7 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 7 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 7 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 7 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 7 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 7 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_07", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_08(recs, wt=1.0):
    """Metric 08 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 8 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 8 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 8 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 8 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 8 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 8 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 8 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 8 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_08", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_09(recs, wt=1.0):
    """Metric 09 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 9 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 9 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 9 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 9 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 9 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 9 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 9 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 9 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_09", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_10(recs, wt=1.0):
    """Metric 10 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 10 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 10 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 10 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 10 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 10 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 10 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 10 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 10 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_10", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_11(recs, wt=1.0):
    """Metric 11 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 11 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 11 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 11 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 11 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 11 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 11 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 11 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 11 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_11", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_12(recs, wt=1.0):
    """Metric 12 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 12 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 12 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 12 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 12 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 12 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 12 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 12 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 12 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_12", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_13(recs, wt=1.0):
    """Metric 13 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 13 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 13 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 13 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 13 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 13 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 13 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 13 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 13 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_13", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_14(recs, wt=1.0):
    """Metric 14 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 14 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 14 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 14 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 14 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 14 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 14 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 14 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 14 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_14", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_15(recs, wt=1.0):
    """Metric 15 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 15 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 15 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 15 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 15 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 15 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 15 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 15 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 15 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_15", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_16(recs, wt=1.0):
    """Metric 16 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 16 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 16 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 16 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 16 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 16 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 16 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 16 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 16 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_16", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_17(recs, wt=1.0):
    """Metric 17 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 17 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 17 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 17 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 17 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 17 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 17 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 17 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 17 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_17", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_18(recs, wt=1.0):
    """Metric 18 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 18 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 18 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 18 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 18 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 18 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 18 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 18 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 18 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_18", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_19(recs, wt=1.0):
    """Metric 19 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 19 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 19 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 19 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 19 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 19 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 19 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 19 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 19 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_19", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_20(recs, wt=1.0):
    """Metric 20 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 20 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 20 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 20 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 20 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 20 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 20 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 20 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 20 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_20", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_21(recs, wt=1.0):
    """Metric 21 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 21 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 21 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 21 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 21 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 21 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 21 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 21 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 21 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_21", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_22(recs, wt=1.0):
    """Metric 22 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 22 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 22 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 22 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 22 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 22 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 22 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 22 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 22 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_22", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_23(recs, wt=1.0):
    """Metric 23 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 23 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 23 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 23 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 23 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 23 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 23 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 23 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 23 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_23", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_24(recs, wt=1.0):
    """Metric 24 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 24 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 24 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 24 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 24 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 24 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 24 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 24 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 24 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_24", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_25(recs, wt=1.0):
    """Metric 25 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 25 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 25 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 25 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 25 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 25 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 25 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 25 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 25 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_25", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_26(recs, wt=1.0):
    """Metric 26 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 26 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 26 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 26 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 26 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 26 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 26 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 26 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 26 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_26", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_27(recs, wt=1.0):
    """Metric 27 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 27 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 27 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 27 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 27 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 27 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 27 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 27 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 27 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_27", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_28(recs, wt=1.0):
    """Metric 28 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 28 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 28 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 28 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 28 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 28 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 28 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 28 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 28 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_28", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_29(recs, wt=1.0):
    """Metric 29 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 29 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 29 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 29 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 29 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 29 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 29 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 29 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 29 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_29", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_30(recs, wt=1.0):
    """Metric 30 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 30 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 30 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 30 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 30 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 30 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 30 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 30 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 30 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_30", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_31(recs, wt=1.0):
    """Metric 31 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 31 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 31 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 31 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 31 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 31 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 31 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 31 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 31 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_31", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_32(recs, wt=1.0):
    """Metric 32 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 32 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 32 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 32 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 32 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 32 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 32 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 32 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 32 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_32", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_33(recs, wt=1.0):
    """Metric 33 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 33 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 33 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 33 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 33 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 33 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 33 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 33 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 33 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_33", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_34(recs, wt=1.0):
    """Metric 34 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 34 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 34 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 34 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 34 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 34 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 34 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 34 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 34 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_34", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_35(recs, wt=1.0):
    """Metric 35 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 35 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 35 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 35 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 35 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 35 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 35 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 35 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 35 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_35", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_36(recs, wt=1.0):
    """Metric 36 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 36 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 36 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 36 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 36 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 36 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 36 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 36 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 36 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_36", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_37(recs, wt=1.0):
    """Metric 37 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 37 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 37 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 37 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 37 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 37 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 37 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 37 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 37 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_37", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_38(recs, wt=1.0):
    """Metric 38 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 38 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 38 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 38 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 38 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 38 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 38 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 38 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 38 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_38", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_39(recs, wt=1.0):
    """Metric 39 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 39 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 39 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 39 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 39 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 39 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 39 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 39 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 39 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_39", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_40(recs, wt=1.0):
    """Metric 40 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 40 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 40 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 40 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 40 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 40 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 40 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 40 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 40 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_40", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_41(recs, wt=1.0):
    """Metric 41 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 41 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 41 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 41 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 41 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 41 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 41 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 41 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 41 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_41", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_42(recs, wt=1.0):
    """Metric 42 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 42 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 42 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 42 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 42 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 42 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 42 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 42 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 42 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_42", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_43(recs, wt=1.0):
    """Metric 43 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 43 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 43 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 43 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 43 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 43 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 43 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 43 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 43 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_43", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_44(recs, wt=1.0):
    """Metric 44 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 44 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 44 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 44 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 44 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 44 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 44 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 44 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 44 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_44", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_45(recs, wt=1.0):
    """Metric 45 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 45 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 45 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 45 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 45 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 45 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 45 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 45 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 45 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_45", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_46(recs, wt=1.0):
    """Metric 46 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 46 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 46 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 46 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 46 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 46 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 46 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 46 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 46 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_46", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_47(recs, wt=1.0):
    """Metric 47 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 47 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 47 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 47 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 47 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 47 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 47 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 47 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 47 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_47", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_48(recs, wt=1.0):
    """Metric 48 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 48 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 48 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 48 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 48 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 48 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 48 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 48 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 48 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_48", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_49(recs, wt=1.0):
    """Metric 49 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 49 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 49 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 49 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 49 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 49 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 49 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 49 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 49 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_49", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_50(recs, wt=1.0):
    """Metric 50 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 50 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 50 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 50 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 50 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 50 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 50 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 50 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 50 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_50", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_51(recs, wt=1.0):
    """Metric 51 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 51 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 51 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 51 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 51 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 51 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 51 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 51 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 51 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_51", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_52(recs, wt=1.0):
    """Metric 52 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 52 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 52 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 52 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 52 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 52 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 52 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 52 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 52 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_52", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_53(recs, wt=1.0):
    """Metric 53 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 53 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 53 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 53 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 53 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 53 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 53 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 53 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 53 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_53", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_54(recs, wt=1.0):
    """Metric 54 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 54 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 54 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 54 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 54 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 54 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 54 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 54 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 54 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_54", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_55(recs, wt=1.0):
    """Metric 55 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 55 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 55 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 55 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 55 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 55 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 55 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 55 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 55 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_55", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_56(recs, wt=1.0):
    """Metric 56 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 56 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 56 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 56 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 56 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 56 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 56 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 56 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 56 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_56", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_57(recs, wt=1.0):
    """Metric 57 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 57 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 57 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 57 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 57 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 57 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 57 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 57 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 57 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_57", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_58(recs, wt=1.0):
    """Metric 58 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 58 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 58 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 58 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 58 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 58 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 58 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 58 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 58 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_58", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_59(recs, wt=1.0):
    """Metric 59 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 59 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 59 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 59 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 59 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 59 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 59 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 59 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 59 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_59", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_60(recs, wt=1.0):
    """Metric 60 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 60 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 60 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 60 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 60 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 60 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 60 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 60 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 60 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_60", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_61(recs, wt=1.0):
    """Metric 61 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 61 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 61 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 61 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 61 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 61 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 61 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 61 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 61 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_61", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_62(recs, wt=1.0):
    """Metric 62 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 62 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 62 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 62 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 62 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 62 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 62 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 62 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 62 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_62", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_63(recs, wt=1.0):
    """Metric 63 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 63 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 63 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 63 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 63 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 63 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 63 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 63 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 63 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_63", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_64(recs, wt=1.0):
    """Metric 64 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 64 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 64 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 64 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 64 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 64 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 64 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 64 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 64 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_64", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_65(recs, wt=1.0):
    """Metric 65 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 65 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 65 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 65 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 65 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 65 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 65 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 65 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 65 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_65", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_66(recs, wt=1.0):
    """Metric 66 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 66 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 66 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 66 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 66 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 66 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 66 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 66 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 66 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_66", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_67(recs, wt=1.0):
    """Metric 67 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 67 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 67 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 67 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 67 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 67 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 67 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 67 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 67 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_67", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_68(recs, wt=1.0):
    """Metric 68 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 68 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 68 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 68 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 68 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 68 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 68 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 68 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 68 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_68", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_69(recs, wt=1.0):
    """Metric 69 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 69 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 69 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 69 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 69 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 69 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 69 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 69 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 69 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_69", "score": round(sc, 3), "hits": h}

def calc_proximityshieldbuilder_70(recs, wt=1.0):
    """Metric 70 for proximityshieldbuilder."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 70 + 57 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 70 + 57 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 70 + 57 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 70 + 57 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 70 + 57 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 70 + 57 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 70 + 57 * 0.01) / 8.0
        tot += p * wt
        if p > 2.5: h += 7
        p = (m * 8 + s * 70 + 57 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "proximityshieldbuilder_70", "score": round(sc, 3), "hits": h}

def aggregate(recs):
    out = {}
    out['k01'] = calc_proximityshieldbuilder_01(recs)
    out['k02'] = calc_proximityshieldbuilder_02(recs)
    out['k03'] = calc_proximityshieldbuilder_03(recs)
    out['k04'] = calc_proximityshieldbuilder_04(recs)
    out['k05'] = calc_proximityshieldbuilder_05(recs)
    out['k06'] = calc_proximityshieldbuilder_06(recs)
    out['k07'] = calc_proximityshieldbuilder_07(recs)
    out['k08'] = calc_proximityshieldbuilder_08(recs)
    out['k09'] = calc_proximityshieldbuilder_09(recs)
    out['k10'] = calc_proximityshieldbuilder_10(recs)
    out['k11'] = calc_proximityshieldbuilder_11(recs)
    out['k12'] = calc_proximityshieldbuilder_12(recs)
    out['k13'] = calc_proximityshieldbuilder_13(recs)
    out['k14'] = calc_proximityshieldbuilder_14(recs)
    out['k15'] = calc_proximityshieldbuilder_15(recs)
    out['k16'] = calc_proximityshieldbuilder_16(recs)
    out['k17'] = calc_proximityshieldbuilder_17(recs)
    out['k18'] = calc_proximityshieldbuilder_18(recs)
    out['k19'] = calc_proximityshieldbuilder_19(recs)
    out['k20'] = calc_proximityshieldbuilder_20(recs)
    out['k21'] = calc_proximityshieldbuilder_21(recs)
    out['k22'] = calc_proximityshieldbuilder_22(recs)
    out['k23'] = calc_proximityshieldbuilder_23(recs)
    out['k24'] = calc_proximityshieldbuilder_24(recs)
    out['k25'] = calc_proximityshieldbuilder_25(recs)
    out['k26'] = calc_proximityshieldbuilder_26(recs)
    out['k27'] = calc_proximityshieldbuilder_27(recs)
    out['k28'] = calc_proximityshieldbuilder_28(recs)
    out['k29'] = calc_proximityshieldbuilder_29(recs)
    out['k30'] = calc_proximityshieldbuilder_30(recs)
    out['k31'] = calc_proximityshieldbuilder_31(recs)
    out['k32'] = calc_proximityshieldbuilder_32(recs)
    out['k33'] = calc_proximityshieldbuilder_33(recs)
    out['k34'] = calc_proximityshieldbuilder_34(recs)
    out['k35'] = calc_proximityshieldbuilder_35(recs)
    out['k36'] = calc_proximityshieldbuilder_36(recs)
    out['k37'] = calc_proximityshieldbuilder_37(recs)
    out['k38'] = calc_proximityshieldbuilder_38(recs)
    out['k39'] = calc_proximityshieldbuilder_39(recs)
    out['k40'] = calc_proximityshieldbuilder_40(recs)
    out['k41'] = calc_proximityshieldbuilder_41(recs)
    out['k42'] = calc_proximityshieldbuilder_42(recs)
    out['k43'] = calc_proximityshieldbuilder_43(recs)
    out['k44'] = calc_proximityshieldbuilder_44(recs)
    out['k45'] = calc_proximityshieldbuilder_45(recs)
    out['k46'] = calc_proximityshieldbuilder_46(recs)
    out['k47'] = calc_proximityshieldbuilder_47(recs)
    out['k48'] = calc_proximityshieldbuilder_48(recs)
    out['k49'] = calc_proximityshieldbuilder_49(recs)
    out['k50'] = calc_proximityshieldbuilder_50(recs)
    out['k51'] = calc_proximityshieldbuilder_51(recs)
    out['k52'] = calc_proximityshieldbuilder_52(recs)
    out['k53'] = calc_proximityshieldbuilder_53(recs)
    out['k54'] = calc_proximityshieldbuilder_54(recs)
    out['k55'] = calc_proximityshieldbuilder_55(recs)
    out['k56'] = calc_proximityshieldbuilder_56(recs)
    out['k57'] = calc_proximityshieldbuilder_57(recs)
    out['k58'] = calc_proximityshieldbuilder_58(recs)
    out['k59'] = calc_proximityshieldbuilder_59(recs)
    out['k60'] = calc_proximityshieldbuilder_60(recs)
    out['k61'] = calc_proximityshieldbuilder_61(recs)
    out['k62'] = calc_proximityshieldbuilder_62(recs)
    out['k63'] = calc_proximityshieldbuilder_63(recs)
    out['k64'] = calc_proximityshieldbuilder_64(recs)
    out['k65'] = calc_proximityshieldbuilder_65(recs)
    out['k66'] = calc_proximityshieldbuilder_66(recs)
    out['k67'] = calc_proximityshieldbuilder_67(recs)
    out['k68'] = calc_proximityshieldbuilder_68(recs)
    out['k69'] = calc_proximityshieldbuilder_69(recs)
    out['k70'] = calc_proximityshieldbuilder_70(recs)
    out['overall'] = round(sum(v['score'] for v in out.values()) / len(out), 3)
    return out
