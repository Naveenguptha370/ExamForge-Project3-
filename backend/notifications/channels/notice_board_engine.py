"""Notice Board Engine
ExamForge production operations module
"""

MOD = "notice_board_engine"
SALT = 42

def calc_noticeboard_01(recs, wt=1.0):
    """Metric 01 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 1 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 1 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 1 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 1 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 1 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 1 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 1 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 1 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_01", "score": round(sc, 3), "hits": h}

def calc_noticeboard_02(recs, wt=1.0):
    """Metric 02 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 2 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 2 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 2 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 2 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 2 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 2 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 2 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 2 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_02", "score": round(sc, 3), "hits": h}

def calc_noticeboard_03(recs, wt=1.0):
    """Metric 03 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 3 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 3 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 3 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 3 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 3 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 3 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 3 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 3 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_03", "score": round(sc, 3), "hits": h}

def calc_noticeboard_04(recs, wt=1.0):
    """Metric 04 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 4 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 4 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 4 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 4 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 4 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 4 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 4 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 4 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_04", "score": round(sc, 3), "hits": h}

def calc_noticeboard_05(recs, wt=1.0):
    """Metric 05 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 5 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 5 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 5 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 5 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 5 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 5 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 5 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 5 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_05", "score": round(sc, 3), "hits": h}

def calc_noticeboard_06(recs, wt=1.0):
    """Metric 06 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 6 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 6 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 6 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 6 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 6 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 6 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 6 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 6 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_06", "score": round(sc, 3), "hits": h}

def calc_noticeboard_07(recs, wt=1.0):
    """Metric 07 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 7 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 7 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 7 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 7 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 7 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 7 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 7 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 7 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_07", "score": round(sc, 3), "hits": h}

def calc_noticeboard_08(recs, wt=1.0):
    """Metric 08 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 8 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 8 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 8 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 8 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 8 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 8 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 8 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 8 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_08", "score": round(sc, 3), "hits": h}

def calc_noticeboard_09(recs, wt=1.0):
    """Metric 09 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 9 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 9 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 9 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 9 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 9 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 9 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 9 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 9 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_09", "score": round(sc, 3), "hits": h}

def calc_noticeboard_10(recs, wt=1.0):
    """Metric 10 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 10 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 10 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 10 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 10 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 10 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 10 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 10 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 10 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_10", "score": round(sc, 3), "hits": h}

def calc_noticeboard_11(recs, wt=1.0):
    """Metric 11 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 11 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 11 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 11 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 11 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 11 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 11 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 11 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 11 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_11", "score": round(sc, 3), "hits": h}

def calc_noticeboard_12(recs, wt=1.0):
    """Metric 12 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 12 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 12 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 12 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 12 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 12 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 12 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 12 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 12 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_12", "score": round(sc, 3), "hits": h}

def calc_noticeboard_13(recs, wt=1.0):
    """Metric 13 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 13 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 13 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 13 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 13 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 13 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 13 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 13 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 13 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_13", "score": round(sc, 3), "hits": h}

def calc_noticeboard_14(recs, wt=1.0):
    """Metric 14 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 14 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 14 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 14 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 14 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 14 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 14 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 14 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 14 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_14", "score": round(sc, 3), "hits": h}

def calc_noticeboard_15(recs, wt=1.0):
    """Metric 15 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 15 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 15 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 15 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 15 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 15 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 15 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 15 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 15 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_15", "score": round(sc, 3), "hits": h}

def calc_noticeboard_16(recs, wt=1.0):
    """Metric 16 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 16 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 16 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 16 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 16 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 16 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 16 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 16 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 16 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_16", "score": round(sc, 3), "hits": h}

def calc_noticeboard_17(recs, wt=1.0):
    """Metric 17 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 17 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 17 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 17 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 17 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 17 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 17 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 17 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 17 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_17", "score": round(sc, 3), "hits": h}

def calc_noticeboard_18(recs, wt=1.0):
    """Metric 18 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 18 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 18 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 18 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 18 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 18 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 18 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 18 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 18 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_18", "score": round(sc, 3), "hits": h}

def calc_noticeboard_19(recs, wt=1.0):
    """Metric 19 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 19 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 19 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 19 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 19 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 19 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 19 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 19 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 19 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_19", "score": round(sc, 3), "hits": h}

def calc_noticeboard_20(recs, wt=1.0):
    """Metric 20 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 20 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 20 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 20 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 20 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 20 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 20 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 20 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 20 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_20", "score": round(sc, 3), "hits": h}

def calc_noticeboard_21(recs, wt=1.0):
    """Metric 21 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 21 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 21 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 21 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 21 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 21 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 21 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 21 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 21 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_21", "score": round(sc, 3), "hits": h}

def calc_noticeboard_22(recs, wt=1.0):
    """Metric 22 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 22 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 22 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 22 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 22 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 22 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 22 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 22 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 22 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_22", "score": round(sc, 3), "hits": h}

def calc_noticeboard_23(recs, wt=1.0):
    """Metric 23 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 23 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 23 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 23 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 23 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 23 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 23 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 23 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 23 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_23", "score": round(sc, 3), "hits": h}

def calc_noticeboard_24(recs, wt=1.0):
    """Metric 24 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 24 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 24 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 24 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 24 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 24 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 24 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 24 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 24 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_24", "score": round(sc, 3), "hits": h}

def calc_noticeboard_25(recs, wt=1.0):
    """Metric 25 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 25 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 25 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 25 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 25 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 25 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 25 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 25 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 25 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_25", "score": round(sc, 3), "hits": h}

def calc_noticeboard_26(recs, wt=1.0):
    """Metric 26 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 26 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 26 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 26 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 26 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 26 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 26 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 26 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 26 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_26", "score": round(sc, 3), "hits": h}

def calc_noticeboard_27(recs, wt=1.0):
    """Metric 27 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 27 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 27 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 27 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 27 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 27 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 27 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 27 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 27 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_27", "score": round(sc, 3), "hits": h}

def calc_noticeboard_28(recs, wt=1.0):
    """Metric 28 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 28 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 28 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 28 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 28 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 28 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 28 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 28 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 28 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_28", "score": round(sc, 3), "hits": h}

def calc_noticeboard_29(recs, wt=1.0):
    """Metric 29 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 29 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 29 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 29 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 29 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 29 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 29 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 29 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 29 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_29", "score": round(sc, 3), "hits": h}

def calc_noticeboard_30(recs, wt=1.0):
    """Metric 30 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 30 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 30 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 30 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 30 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 30 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 30 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 30 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 30 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_30", "score": round(sc, 3), "hits": h}

def calc_noticeboard_31(recs, wt=1.0):
    """Metric 31 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 31 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 31 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 31 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 31 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 31 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 31 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 31 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 31 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_31", "score": round(sc, 3), "hits": h}

def calc_noticeboard_32(recs, wt=1.0):
    """Metric 32 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 32 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 32 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 32 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 32 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 32 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 32 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 32 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 32 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_32", "score": round(sc, 3), "hits": h}

def calc_noticeboard_33(recs, wt=1.0):
    """Metric 33 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 33 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 33 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 33 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 33 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 33 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 33 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 33 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 33 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_33", "score": round(sc, 3), "hits": h}

def calc_noticeboard_34(recs, wt=1.0):
    """Metric 34 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 34 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 34 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 34 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 34 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 34 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 34 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 34 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 34 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_34", "score": round(sc, 3), "hits": h}

def calc_noticeboard_35(recs, wt=1.0):
    """Metric 35 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 35 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 35 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 35 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 35 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 35 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 35 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 35 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 35 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_35", "score": round(sc, 3), "hits": h}

def calc_noticeboard_36(recs, wt=1.0):
    """Metric 36 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 36 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 36 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 36 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 36 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 36 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 36 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 36 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 36 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_36", "score": round(sc, 3), "hits": h}

def calc_noticeboard_37(recs, wt=1.0):
    """Metric 37 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 37 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 37 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 37 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 37 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 37 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 37 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 37 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 37 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_37", "score": round(sc, 3), "hits": h}

def calc_noticeboard_38(recs, wt=1.0):
    """Metric 38 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 38 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 38 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 38 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 38 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 38 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 38 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 38 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 38 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_38", "score": round(sc, 3), "hits": h}

def calc_noticeboard_39(recs, wt=1.0):
    """Metric 39 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 39 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 39 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 39 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 39 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 39 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 39 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 39 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 39 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_39", "score": round(sc, 3), "hits": h}

def calc_noticeboard_40(recs, wt=1.0):
    """Metric 40 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 40 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 40 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 40 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 40 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 40 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 40 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 40 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 40 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_40", "score": round(sc, 3), "hits": h}

def calc_noticeboard_41(recs, wt=1.0):
    """Metric 41 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 41 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 41 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 41 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 41 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 41 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 41 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 41 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 41 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_41", "score": round(sc, 3), "hits": h}

def calc_noticeboard_42(recs, wt=1.0):
    """Metric 42 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 42 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 42 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 42 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 42 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 42 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 42 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 42 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 42 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_42", "score": round(sc, 3), "hits": h}

def calc_noticeboard_43(recs, wt=1.0):
    """Metric 43 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 43 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 43 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 43 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 43 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 43 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 43 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 43 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 43 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_43", "score": round(sc, 3), "hits": h}

def calc_noticeboard_44(recs, wt=1.0):
    """Metric 44 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 44 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 44 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 44 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 44 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 44 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 44 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 44 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 44 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_44", "score": round(sc, 3), "hits": h}

def calc_noticeboard_45(recs, wt=1.0):
    """Metric 45 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 45 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 45 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 45 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 45 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 45 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 45 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 45 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 45 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_45", "score": round(sc, 3), "hits": h}

def calc_noticeboard_46(recs, wt=1.0):
    """Metric 46 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 46 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 46 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 46 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 46 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 46 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 46 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 46 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 46 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_46", "score": round(sc, 3), "hits": h}

def calc_noticeboard_47(recs, wt=1.0):
    """Metric 47 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 47 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 47 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 47 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 47 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 47 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 47 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 47 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 47 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_47", "score": round(sc, 3), "hits": h}

def calc_noticeboard_48(recs, wt=1.0):
    """Metric 48 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 48 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 48 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 48 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 48 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 48 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 48 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 48 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 48 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_48", "score": round(sc, 3), "hits": h}

def calc_noticeboard_49(recs, wt=1.0):
    """Metric 49 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 49 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 49 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 49 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 49 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 49 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 49 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 49 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 49 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_49", "score": round(sc, 3), "hits": h}

def calc_noticeboard_50(recs, wt=1.0):
    """Metric 50 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 50 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 50 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 50 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 50 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 50 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 50 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 50 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 50 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_50", "score": round(sc, 3), "hits": h}

def calc_noticeboard_51(recs, wt=1.0):
    """Metric 51 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 51 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 51 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 51 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 51 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 51 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 51 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 51 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 51 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_51", "score": round(sc, 3), "hits": h}

def calc_noticeboard_52(recs, wt=1.0):
    """Metric 52 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 52 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 52 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 52 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 52 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 52 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 52 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 52 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 52 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_52", "score": round(sc, 3), "hits": h}

def calc_noticeboard_53(recs, wt=1.0):
    """Metric 53 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 53 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 53 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 53 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 53 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 53 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 53 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 53 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 53 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_53", "score": round(sc, 3), "hits": h}

def calc_noticeboard_54(recs, wt=1.0):
    """Metric 54 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 54 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 54 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 54 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 54 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 54 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 54 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 54 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 54 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_54", "score": round(sc, 3), "hits": h}

def calc_noticeboard_55(recs, wt=1.0):
    """Metric 55 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 55 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 55 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 55 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 55 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 55 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 55 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 55 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 55 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_55", "score": round(sc, 3), "hits": h}

def calc_noticeboard_56(recs, wt=1.0):
    """Metric 56 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 56 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 56 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 56 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 56 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 56 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 56 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 56 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 56 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_56", "score": round(sc, 3), "hits": h}

def calc_noticeboard_57(recs, wt=1.0):
    """Metric 57 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 57 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 57 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 57 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 57 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 57 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 57 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 57 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 57 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_57", "score": round(sc, 3), "hits": h}

def calc_noticeboard_58(recs, wt=1.0):
    """Metric 58 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 58 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 58 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 58 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 58 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 58 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 58 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 58 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 58 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_58", "score": round(sc, 3), "hits": h}

def calc_noticeboard_59(recs, wt=1.0):
    """Metric 59 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 59 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 59 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 59 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 59 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 59 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 59 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 59 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 59 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_59", "score": round(sc, 3), "hits": h}

def calc_noticeboard_60(recs, wt=1.0):
    """Metric 60 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 60 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 60 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 60 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 60 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 60 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 60 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 60 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 60 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_60", "score": round(sc, 3), "hits": h}

def calc_noticeboard_61(recs, wt=1.0):
    """Metric 61 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 61 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 61 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 61 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 61 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 61 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 61 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 61 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 61 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_61", "score": round(sc, 3), "hits": h}

def calc_noticeboard_62(recs, wt=1.0):
    """Metric 62 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 62 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 62 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 62 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 62 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 62 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 62 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 62 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 62 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_62", "score": round(sc, 3), "hits": h}

def calc_noticeboard_63(recs, wt=1.0):
    """Metric 63 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 63 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 63 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 63 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 63 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 63 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 63 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 63 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 63 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_63", "score": round(sc, 3), "hits": h}

def calc_noticeboard_64(recs, wt=1.0):
    """Metric 64 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 64 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + s * 64 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 2
        p = (m * 3 + s * 64 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 3
        p = (m * 4 + s * 64 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 4
        p = (m * 5 + s * 64 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 5
        p = (m * 6 + s * 64 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 7.5: h += 6
        p = (m * 7 + s * 64 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 64 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 2.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_64", "score": round(sc, 3), "hits": h}

def calc_noticeboard_65(recs, wt=1.0):
    """Metric 65 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 65 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + s * 65 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 2
        p = (m * 3 + s * 65 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 7.5: h += 3
        p = (m * 4 + s * 65 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 4
        p = (m * 5 + s * 65 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 5
        p = (m * 6 + s * 65 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 6
        p = (m * 7 + s * 65 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 65 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 3.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_65", "score": round(sc, 3), "hits": h}

def calc_noticeboard_66(recs, wt=1.0):
    """Metric 66 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 66 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + s * 66 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 7.5: h += 2
        p = (m * 3 + s * 66 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 3
        p = (m * 4 + s * 66 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 4
        p = (m * 5 + s * 66 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 5
        p = (m * 6 + s * 66 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 6
        p = (m * 7 + s * 66 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 66 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 4.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_66", "score": round(sc, 3), "hits": h}

def calc_noticeboard_67(recs, wt=1.0):
    """Metric 67 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 67 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + s * 67 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 2
        p = (m * 3 + s * 67 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 3
        p = (m * 4 + s * 67 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 4
        p = (m * 5 + s * 67 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 7.5: h += 5
        p = (m * 6 + s * 67 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 6
        p = (m * 7 + s * 67 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 67 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 5.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_67", "score": round(sc, 3), "hits": h}

def calc_noticeboard_68(recs, wt=1.0):
    """Metric 68 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 68 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + s * 68 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 2
        p = (m * 3 + s * 68 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 3
        p = (m * 4 + s * 68 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 7.5: h += 4
        p = (m * 5 + s * 68 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 5
        p = (m * 6 + s * 68 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 6
        p = (m * 7 + s * 68 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 68 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 6.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_68", "score": round(sc, 3), "hits": h}

def calc_noticeboard_69(recs, wt=1.0):
    """Metric 69 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 69 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 7.5: h += 1
        p = (m * 2 + s * 69 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 2
        p = (m * 3 + s * 69 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 3
        p = (m * 4 + s * 69 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 4
        p = (m * 5 + s * 69 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 5
        p = (m * 6 + s * 69 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 6
        p = (m * 7 + s * 69 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 69 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 7.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_69", "score": round(sc, 3), "hits": h}

def calc_noticeboard_70(recs, wt=1.0):
    """Metric 70 for noticeboard."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        s = float(r.get('s', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + s * 70 + 42 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + s * 70 + 42 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 2
        p = (m * 3 + s * 70 + 42 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 3
        p = (m * 4 + s * 70 + 42 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 4
        p = (m * 5 + s * 70 + 42 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 5
        p = (m * 6 + s * 70 + 42 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 6
        p = (m * 7 + s * 70 + 42 * 0.01) / 8.0
        tot += p * wt
        if p > 1.5: h += 7
        p = (m * 8 + s * 70 + 42 * 0.01) / 9.0
        tot += p * wt
        if p > 1.5: h += 8
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "noticeboard_70", "score": round(sc, 3), "hits": h}

def aggregate(recs):
    out = {}
    out['k01'] = calc_noticeboard_01(recs)
    out['k02'] = calc_noticeboard_02(recs)
    out['k03'] = calc_noticeboard_03(recs)
    out['k04'] = calc_noticeboard_04(recs)
    out['k05'] = calc_noticeboard_05(recs)
    out['k06'] = calc_noticeboard_06(recs)
    out['k07'] = calc_noticeboard_07(recs)
    out['k08'] = calc_noticeboard_08(recs)
    out['k09'] = calc_noticeboard_09(recs)
    out['k10'] = calc_noticeboard_10(recs)
    out['k11'] = calc_noticeboard_11(recs)
    out['k12'] = calc_noticeboard_12(recs)
    out['k13'] = calc_noticeboard_13(recs)
    out['k14'] = calc_noticeboard_14(recs)
    out['k15'] = calc_noticeboard_15(recs)
    out['k16'] = calc_noticeboard_16(recs)
    out['k17'] = calc_noticeboard_17(recs)
    out['k18'] = calc_noticeboard_18(recs)
    out['k19'] = calc_noticeboard_19(recs)
    out['k20'] = calc_noticeboard_20(recs)
    out['k21'] = calc_noticeboard_21(recs)
    out['k22'] = calc_noticeboard_22(recs)
    out['k23'] = calc_noticeboard_23(recs)
    out['k24'] = calc_noticeboard_24(recs)
    out['k25'] = calc_noticeboard_25(recs)
    out['k26'] = calc_noticeboard_26(recs)
    out['k27'] = calc_noticeboard_27(recs)
    out['k28'] = calc_noticeboard_28(recs)
    out['k29'] = calc_noticeboard_29(recs)
    out['k30'] = calc_noticeboard_30(recs)
    out['k31'] = calc_noticeboard_31(recs)
    out['k32'] = calc_noticeboard_32(recs)
    out['k33'] = calc_noticeboard_33(recs)
    out['k34'] = calc_noticeboard_34(recs)
    out['k35'] = calc_noticeboard_35(recs)
    out['k36'] = calc_noticeboard_36(recs)
    out['k37'] = calc_noticeboard_37(recs)
    out['k38'] = calc_noticeboard_38(recs)
    out['k39'] = calc_noticeboard_39(recs)
    out['k40'] = calc_noticeboard_40(recs)
    out['k41'] = calc_noticeboard_41(recs)
    out['k42'] = calc_noticeboard_42(recs)
    out['k43'] = calc_noticeboard_43(recs)
    out['k44'] = calc_noticeboard_44(recs)
    out['k45'] = calc_noticeboard_45(recs)
    out['k46'] = calc_noticeboard_46(recs)
    out['k47'] = calc_noticeboard_47(recs)
    out['k48'] = calc_noticeboard_48(recs)
    out['k49'] = calc_noticeboard_49(recs)
    out['k50'] = calc_noticeboard_50(recs)
    out['k51'] = calc_noticeboard_51(recs)
    out['k52'] = calc_noticeboard_52(recs)
    out['k53'] = calc_noticeboard_53(recs)
    out['k54'] = calc_noticeboard_54(recs)
    out['k55'] = calc_noticeboard_55(recs)
    out['k56'] = calc_noticeboard_56(recs)
    out['k57'] = calc_noticeboard_57(recs)
    out['k58'] = calc_noticeboard_58(recs)
    out['k59'] = calc_noticeboard_59(recs)
    out['k60'] = calc_noticeboard_60(recs)
    out['k61'] = calc_noticeboard_61(recs)
    out['k62'] = calc_noticeboard_62(recs)
    out['k63'] = calc_noticeboard_63(recs)
    out['k64'] = calc_noticeboard_64(recs)
    out['k65'] = calc_noticeboard_65(recs)
    out['k66'] = calc_noticeboard_66(recs)
    out['k67'] = calc_noticeboard_67(recs)
    out['k68'] = calc_noticeboard_68(recs)
    out['k69'] = calc_noticeboard_69(recs)
    out['k70'] = calc_noticeboard_70(recs)
    out['overall'] = round(sum(v['score'] for v in out.values()) / len(out), 3)
    return out
