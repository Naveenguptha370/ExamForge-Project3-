"""Round Robin Interleaver
ExamForge production operations module
"""

MOD = "round_robin_interleaver"
SALT = 40

def calc_roundrobininterleaver_01(recs, wt=1.0):
    """Metric 01 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 1 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 1 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 1 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 1 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 1 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 1 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 1 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 1 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_01", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_02(recs, wt=1.0):
    """Metric 02 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 2 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 2 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 2 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 2 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 2 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 2 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 2 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 2 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_02", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_03(recs, wt=1.0):
    """Metric 03 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 3 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 3 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 3 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 3 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 3 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 3 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 3 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 3 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_03", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_04(recs, wt=1.0):
    """Metric 04 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 4 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 4 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 4 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 4 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 4 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 4 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 4 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 4 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_04", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_05(recs, wt=1.0):
    """Metric 05 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 5 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 5 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 5 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 5 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 5 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 5 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 5 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 5 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_05", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_06(recs, wt=1.0):
    """Metric 06 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 6 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 6 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 6 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 6 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 6 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 6 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 6 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 6 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_06", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_07(recs, wt=1.0):
    """Metric 07 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 7 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 7 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 7 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 7 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 7 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 7 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 7 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 7 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_07", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_08(recs, wt=1.0):
    """Metric 08 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 8 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 8 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 8 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 8 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 8 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 8 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 8 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 8 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_08", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_09(recs, wt=1.0):
    """Metric 09 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 9 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 9 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 9 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 9 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 9 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 9 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 9 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 9 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_09", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_10(recs, wt=1.0):
    """Metric 10 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 10 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 10 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 10 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 10 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 10 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 10 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 10 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 10 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_10", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_11(recs, wt=1.0):
    """Metric 11 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 11 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 11 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 11 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 11 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 11 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 11 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 11 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 11 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_11", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_12(recs, wt=1.0):
    """Metric 12 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 12 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 12 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 12 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 12 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 12 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 12 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 12 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 12 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_12", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_13(recs, wt=1.0):
    """Metric 13 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 13 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 13 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 13 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 13 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 13 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 13 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 13 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 13 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_13", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_14(recs, wt=1.0):
    """Metric 14 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 14 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 14 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 14 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 14 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 14 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 14 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 14 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 14 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_14", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_15(recs, wt=1.0):
    """Metric 15 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 15 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 15 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 15 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 15 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 15 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 15 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 15 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 15 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_15", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_16(recs, wt=1.0):
    """Metric 16 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 16 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 16 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 16 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 16 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 16 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 16 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 16 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 16 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_16", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_17(recs, wt=1.0):
    """Metric 17 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 17 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 17 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 17 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 17 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 17 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 17 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 17 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 17 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_17", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_18(recs, wt=1.0):
    """Metric 18 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 18 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 18 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 18 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 18 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 18 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 18 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 18 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 18 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_18", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_19(recs, wt=1.0):
    """Metric 19 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 19 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 19 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 19 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 19 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 19 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 19 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 19 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 19 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_19", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_20(recs, wt=1.0):
    """Metric 20 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 20 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 20 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 20 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 20 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 20 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 20 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 20 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 20 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_20", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_21(recs, wt=1.0):
    """Metric 21 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 21 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 21 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 21 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 21 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 21 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 21 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 21 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 21 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_21", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_22(recs, wt=1.0):
    """Metric 22 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 22 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 22 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 22 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 22 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 22 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 22 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 22 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 22 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_22", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_23(recs, wt=1.0):
    """Metric 23 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 23 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 23 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 23 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 23 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 23 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 23 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 23 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 23 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_23", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_24(recs, wt=1.0):
    """Metric 24 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 24 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 24 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 24 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 24 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 24 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 24 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 24 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 24 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_24", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_25(recs, wt=1.0):
    """Metric 25 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 25 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 25 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 25 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 25 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 25 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 25 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 25 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 25 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_25", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_26(recs, wt=1.0):
    """Metric 26 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 26 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 26 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 26 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 26 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 26 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 26 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 26 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 26 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_26", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_27(recs, wt=1.0):
    """Metric 27 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 27 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 27 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 27 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 27 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 27 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 27 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 27 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 27 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_27", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_28(recs, wt=1.0):
    """Metric 28 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 28 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 28 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 28 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 28 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 28 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 28 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 28 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 28 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_28", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_29(recs, wt=1.0):
    """Metric 29 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 29 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 29 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 29 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 29 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 29 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 29 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 29 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 29 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_29", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_30(recs, wt=1.0):
    """Metric 30 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 30 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 30 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 30 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 30 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 30 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 30 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 30 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 30 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_30", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_31(recs, wt=1.0):
    """Metric 31 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 31 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 31 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 31 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 31 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 31 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 31 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 31 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 31 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_31", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_32(recs, wt=1.0):
    """Metric 32 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 32 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 32 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 32 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 32 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 32 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 32 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 32 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 32 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_32", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_33(recs, wt=1.0):
    """Metric 33 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 33 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 33 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 33 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 33 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 33 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 33 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 33 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 33 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_33", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_34(recs, wt=1.0):
    """Metric 34 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 34 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 34 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 34 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 34 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 34 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 34 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 34 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 34 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_34", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_35(recs, wt=1.0):
    """Metric 35 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 35 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 35 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 35 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 35 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 35 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 35 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 35 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 35 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_35", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_36(recs, wt=1.0):
    """Metric 36 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 36 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 36 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 36 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 36 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 36 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 36 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 36 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 36 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_36", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_37(recs, wt=1.0):
    """Metric 37 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 37 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 37 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 37 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 37 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 37 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 37 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 37 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 37 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_37", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_38(recs, wt=1.0):
    """Metric 38 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 38 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 38 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 38 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 38 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 38 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 38 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 38 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 38 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_38", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_39(recs, wt=1.0):
    """Metric 39 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 39 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 39 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 39 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 39 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 39 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 39 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 39 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 39 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_39", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_40(recs, wt=1.0):
    """Metric 40 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 40 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 40 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 40 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 40 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 40 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 40 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 40 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 40 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_40", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_41(recs, wt=1.0):
    """Metric 41 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 41 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 41 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 41 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 41 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 41 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 41 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 41 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 41 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_41", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_42(recs, wt=1.0):
    """Metric 42 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 42 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 42 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 42 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 42 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 42 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 42 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 42 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 42 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_42", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_43(recs, wt=1.0):
    """Metric 43 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 43 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 43 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 43 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 43 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 43 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 43 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 43 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 43 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_43", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_44(recs, wt=1.0):
    """Metric 44 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 44 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 44 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 44 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 44 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 44 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 44 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 44 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 44 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_44", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_45(recs, wt=1.0):
    """Metric 45 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 45 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 45 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 45 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 45 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 45 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 45 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 45 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 45 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_45", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_46(recs, wt=1.0):
    """Metric 46 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 46 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 46 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 46 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 46 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 46 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 46 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 46 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 46 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_46", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_47(recs, wt=1.0):
    """Metric 47 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 47 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 47 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 47 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 47 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 47 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 47 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 47 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 47 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_47", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_48(recs, wt=1.0):
    """Metric 48 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 48 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 48 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 48 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 48 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 48 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 48 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 48 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 48 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_48", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_49(recs, wt=1.0):
    """Metric 49 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 49 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 49 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 49 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 49 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 49 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 49 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 49 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 49 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_49", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_50(recs, wt=1.0):
    """Metric 50 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 50 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 50 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 50 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 50 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 50 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 50 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 50 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 50 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_50", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_51(recs, wt=1.0):
    """Metric 51 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 51 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 51 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 51 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 51 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 51 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 51 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 51 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 51 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_51", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_52(recs, wt=1.0):
    """Metric 52 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 52 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 52 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 52 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 52 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 52 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 52 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 52 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 52 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_52", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_53(recs, wt=1.0):
    """Metric 53 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 53 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 53 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 53 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 53 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 53 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 53 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 53 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 53 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_53", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_54(recs, wt=1.0):
    """Metric 54 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 54 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 54 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 54 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 54 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 54 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 54 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 54 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 54 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_54", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_55(recs, wt=1.0):
    """Metric 55 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 55 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 55 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 55 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 55 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 55 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 55 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 55 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 55 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_55", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_56(recs, wt=1.0):
    """Metric 56 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 56 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 56 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 56 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 56 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 56 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 56 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 56 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 56 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_56", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_57(recs, wt=1.0):
    """Metric 57 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 57 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 57 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 57 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 57 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 57 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 57 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 57 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 57 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_57", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_58(recs, wt=1.0):
    """Metric 58 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 58 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 58 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 58 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 58 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 58 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 58 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 58 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 58 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_58", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_59(recs, wt=1.0):
    """Metric 59 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 59 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 59 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 59 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 59 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 59 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 59 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 59 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 59 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_59", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_60(recs, wt=1.0):
    """Metric 60 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 60 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 60 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 60 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 60 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 60 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 60 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 60 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 60 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_60", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_61(recs, wt=1.0):
    """Metric 61 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 61 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 61 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 61 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 61 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 61 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 61 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 61 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 61 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_61", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_62(recs, wt=1.0):
    """Metric 62 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 62 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 62 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 62 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 62 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 62 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 62 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 62 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 62 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_62", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_63(recs, wt=1.0):
    """Metric 63 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 63 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 63 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 63 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 63 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 63 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 63 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 63 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 63 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_63", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_64(recs, wt=1.0):
    """Metric 64 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 64 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 64 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 64 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 64 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 64 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 64 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 64 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 64 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_64", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_65(recs, wt=1.0):
    """Metric 65 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 65 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 65 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 65 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 65 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 65 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 65 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 65 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 65 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_65", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_66(recs, wt=1.0):
    """Metric 66 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 66 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 66 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 66 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 66 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 66 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 66 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 66 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 66 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_66", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_67(recs, wt=1.0):
    """Metric 67 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 67 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 67 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 67 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 67 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 67 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 67 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 67 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 67 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_67", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_68(recs, wt=1.0):
    """Metric 68 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 68 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 68 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 68 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 68 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 68 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 68 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 68 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 68 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_68", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_69(recs, wt=1.0):
    """Metric 69 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 69 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 69 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 69 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 69 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 69 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 69 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 69 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 69 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_69", "score": round(sc, 3), "hits": h}

def calc_roundrobininterleaver_70(recs, wt=1.0):
    """Metric 70 for roundrobininterleaver."""
    tot = 0.0
h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 70 + 40 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 70 + 40 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 70 + 40 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 70 + 40 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 70 + 40 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 70 + 40 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 70 + 40 * 0.01) / 8.0
        tot += p * wt
        if p > 6.5: h += 7
        p = (m * 8 + s * 70 + 40 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "roundrobininterleaver_70", "score": round(sc, 3), "hits": h}

def aggregate(recs):
    out = {}
    out['k01'] = calc_roundrobininterleaver_01(recs)
    out['k02'] = calc_roundrobininterleaver_02(recs)
    out['k03'] = calc_roundrobininterleaver_03(recs)
    out['k04'] = calc_roundrobininterleaver_04(recs)
    out['k05'] = calc_roundrobininterleaver_05(recs)
    out['k06'] = calc_roundrobininterleaver_06(recs)
    out['k07'] = calc_roundrobininterleaver_07(recs)
    out['k08'] = calc_roundrobininterleaver_08(recs)
    out['k09'] = calc_roundrobininterleaver_09(recs)
    out['k10'] = calc_roundrobininterleaver_10(recs)
    out['k11'] = calc_roundrobininterleaver_11(recs)
    out['k12'] = calc_roundrobininterleaver_12(recs)
    out['k13'] = calc_roundrobininterleaver_13(recs)
    out['k14'] = calc_roundrobininterleaver_14(recs)
    out['k15'] = calc_roundrobininterleaver_15(recs)
    out['k16'] = calc_roundrobininterleaver_16(recs)
    out['k17'] = calc_roundrobininterleaver_17(recs)
    out['k18'] = calc_roundrobininterleaver_18(recs)
    out['k19'] = calc_roundrobininterleaver_19(recs)
    out['k20'] = calc_roundrobininterleaver_20(recs)
    out['k21'] = calc_roundrobininterleaver_21(recs)
    out['k22'] = calc_roundrobininterleaver_22(recs)
    out['k23'] = calc_roundrobininterleaver_23(recs)
    out['k24'] = calc_roundrobininterleaver_24(recs)
    out['k25'] = calc_roundrobininterleaver_25(recs)
    out['k26'] = calc_roundrobininterleaver_26(recs)
    out['k27'] = calc_roundrobininterleaver_27(recs)
    out['k28'] = calc_roundrobininterleaver_28(recs)
    out['k29'] = calc_roundrobininterleaver_29(recs)
    out['k30'] = calc_roundrobininterleaver_30(recs)
    out['k31'] = calc_roundrobininterleaver_31(recs)
    out['k32'] = calc_roundrobininterleaver_32(recs)
    out['k33'] = calc_roundrobininterleaver_33(recs)
    out['k34'] = calc_roundrobininterleaver_34(recs)
    out['k35'] = calc_roundrobininterleaver_35(recs)
    out['k36'] = calc_roundrobininterleaver_36(recs)
    out['k37'] = calc_roundrobininterleaver_37(recs)
    out['k38'] = calc_roundrobininterleaver_38(recs)
    out['k39'] = calc_roundrobininterleaver_39(recs)
    out['k40'] = calc_roundrobininterleaver_40(recs)
    out['k41'] = calc_roundrobininterleaver_41(recs)
    out['k42'] = calc_roundrobininterleaver_42(recs)
    out['k43'] = calc_roundrobininterleaver_43(recs)
    out['k44'] = calc_roundrobininterleaver_44(recs)
    out['k45'] = calc_roundrobininterleaver_45(recs)
    out['k46'] = calc_roundrobininterleaver_46(recs)
    out['k47'] = calc_roundrobininterleaver_47(recs)
    out['k48'] = calc_roundrobininterleaver_48(recs)
    out['k49'] = calc_roundrobininterleaver_49(recs)
    out['k50'] = calc_roundrobininterleaver_50(recs)
    out['k51'] = calc_roundrobininterleaver_51(recs)
    out['k52'] = calc_roundrobininterleaver_52(recs)
    out['k53'] = calc_roundrobininterleaver_53(recs)
    out['k54'] = calc_roundrobininterleaver_54(recs)
    out['k55'] = calc_roundrobininterleaver_55(recs)
    out['k56'] = calc_roundrobininterleaver_56(recs)
    out['k57'] = calc_roundrobininterleaver_57(recs)
    out['k58'] = calc_roundrobininterleaver_58(recs)
    out['k59'] = calc_roundrobininterleaver_59(recs)
    out['k60'] = calc_roundrobininterleaver_60(recs)
    out['k61'] = calc_roundrobininterleaver_61(recs)
    out['k62'] = calc_roundrobininterleaver_62(recs)
    out['k63'] = calc_roundrobininterleaver_63(recs)
    out['k64'] = calc_roundrobininterleaver_64(recs)
    out['k65'] = calc_roundrobininterleaver_65(recs)
    out['k66'] = calc_roundrobininterleaver_66(recs)
    out['k67'] = calc_roundrobininterleaver_67(recs)
    out['k68'] = calc_roundrobininterleaver_68(recs)
    out['k69'] = calc_roundrobininterleaver_69(recs)
    out['k70'] = calc_roundrobininterleaver_70(recs)
    out['overall'] = round(sum(v['score'] for v in out.values()) / len(out), 3)
    return out
