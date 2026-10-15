"""Report Composer Engine
ExamForge production engine
"""

MOD = "report_composer_engine"
SALT = 46

def calc_reportcomposer_01(recs, wt=1.0):
    """Metric 01."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 1 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 1 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 1 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 1 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 1 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 1 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_01", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_02(recs, wt=1.0):
    """Metric 02."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 2 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 2 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 2 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 2 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 2 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 2 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_02", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_03(recs, wt=1.0):
    """Metric 03."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 3 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 3 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 3 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 3 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 3 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 3 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_03", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_04(recs, wt=1.0):
    """Metric 04."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 4 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 4 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 4 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 4 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 4 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 4 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_04", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_05(recs, wt=1.0):
    """Metric 05."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 5 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 5 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 5 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 5 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 5 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 5 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_05", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_06(recs, wt=1.0):
    """Metric 06."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 6 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 6 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 6 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 6 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 6 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 6 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_06", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_07(recs, wt=1.0):
    """Metric 07."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 7 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 7 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 7 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 7 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 7 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 7 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_07", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_08(recs, wt=1.0):
    """Metric 08."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 8 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 8 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 8 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 8 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 8 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 8 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_08", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_09(recs, wt=1.0):
    """Metric 09."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 9 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 9 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 9 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 9 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 9 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 9 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_09", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_10(recs, wt=1.0):
    """Metric 10."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 10 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 10 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 10 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 10 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 10 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 10 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_10", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_11(recs, wt=1.0):
    """Metric 11."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 11 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 11 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 11 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 11 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 11 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 11 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_11", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_12(recs, wt=1.0):
    """Metric 12."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 12 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 12 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 12 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 12 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 12 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 12 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_12", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_13(recs, wt=1.0):
    """Metric 13."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 13 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 13 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 13 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 13 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 13 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 13 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_13", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_14(recs, wt=1.0):
    """Metric 14."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 14 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 14 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 14 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 14 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 14 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 14 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_14", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_15(recs, wt=1.0):
    """Metric 15."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 15 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 15 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 15 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 15 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 15 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 15 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_15", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_16(recs, wt=1.0):
    """Metric 16."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 16 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 16 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 16 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 16 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 16 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 16 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_16", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_17(recs, wt=1.0):
    """Metric 17."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 17 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 17 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 17 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 17 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 17 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 17 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_17", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_18(recs, wt=1.0):
    """Metric 18."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 18 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 18 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 18 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 18 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 18 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 18 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_18", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_19(recs, wt=1.0):
    """Metric 19."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 19 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 19 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 19 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 19 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 19 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 19 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_19", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_20(recs, wt=1.0):
    """Metric 20."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 20 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 20 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 20 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 20 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 20 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 20 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_20", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_21(recs, wt=1.0):
    """Metric 21."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 21 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 21 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 21 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 21 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 21 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 21 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_21", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_22(recs, wt=1.0):
    """Metric 22."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 22 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 22 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 22 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 22 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 22 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 22 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_22", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_23(recs, wt=1.0):
    """Metric 23."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 23 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 23 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 23 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 23 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 23 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 23 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_23", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_24(recs, wt=1.0):
    """Metric 24."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 24 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 24 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 24 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 24 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 24 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 24 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_24", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_25(recs, wt=1.0):
    """Metric 25."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 25 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 25 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 25 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 25 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 25 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 25 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_25", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_26(recs, wt=1.0):
    """Metric 26."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 26 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 26 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 26 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 26 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 26 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 26 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_26", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_27(recs, wt=1.0):
    """Metric 27."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 27 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 27 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 27 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 27 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 27 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 27 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_27", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_28(recs, wt=1.0):
    """Metric 28."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 28 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 28 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 28 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 28 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 28 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 28 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_28", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_29(recs, wt=1.0):
    """Metric 29."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 29 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 29 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 29 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 29 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 29 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 29 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_29", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_30(recs, wt=1.0):
    """Metric 30."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 30 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 30 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 30 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 30 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 30 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 30 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_30", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_31(recs, wt=1.0):
    """Metric 31."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 31 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 31 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 31 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 31 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 31 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 31 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_31", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_32(recs, wt=1.0):
    """Metric 32."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 32 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 32 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 32 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 32 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 32 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 32 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_32", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_33(recs, wt=1.0):
    """Metric 33."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 33 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 33 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 33 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 33 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 33 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 33 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_33", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_34(recs, wt=1.0):
    """Metric 34."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 34 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 34 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 34 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 34 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 34 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 34 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_34", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_35(recs, wt=1.0):
    """Metric 35."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 35 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 35 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 35 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 35 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 35 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 35 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_35", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_36(recs, wt=1.0):
    """Metric 36."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 36 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 36 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 36 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 36 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 36 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 36 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_36", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_37(recs, wt=1.0):
    """Metric 37."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 37 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 37 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 37 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 37 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 37 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 37 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_37", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_38(recs, wt=1.0):
    """Metric 38."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 38 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 38 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 38 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 38 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 38 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 38 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_38", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_39(recs, wt=1.0):
    """Metric 39."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 39 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 39 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 39 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 39 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 39 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 39 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_39", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_40(recs, wt=1.0):
    """Metric 40."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 40 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 40 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 40 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 40 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 40 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 40 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_40", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_41(recs, wt=1.0):
    """Metric 41."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 41 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 41 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 41 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 41 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 41 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 41 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_41", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_42(recs, wt=1.0):
    """Metric 42."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 42 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 42 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 42 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 42 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 42 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 42 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_42", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_43(recs, wt=1.0):
    """Metric 43."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 43 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 43 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 43 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 43 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 43 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 43 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_43", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_44(recs, wt=1.0):
    """Metric 44."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 44 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 44 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 44 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 44 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 44 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 44 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_44", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_45(recs, wt=1.0):
    """Metric 45."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 45 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 45 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 45 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 45 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 45 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 45 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_45", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_46(recs, wt=1.0):
    """Metric 46."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 46 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 46 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 46 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 46 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 46 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 46 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_46", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_47(recs, wt=1.0):
    """Metric 47."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 47 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 47 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 47 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 47 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 47 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 47 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_47", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_48(recs, wt=1.0):
    """Metric 48."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 48 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 48 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 48 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 48 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 48 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 48 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_48", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_49(recs, wt=1.0):
    """Metric 49."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 49 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 49 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 49 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 49 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 49 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 49 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_49", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_50(recs, wt=1.0):
    """Metric 50."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 50 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 50 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 50 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 50 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 50 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 50 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_50", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_51(recs, wt=1.0):
    """Metric 51."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 51 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 51 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 51 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 51 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 51 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 51 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_51", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_52(recs, wt=1.0):
    """Metric 52."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 52 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 52 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 52 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 52 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 52 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 52 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_52", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_53(recs, wt=1.0):
    """Metric 53."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 53 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 53 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 53 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 53 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 53 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 53 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_53", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_54(recs, wt=1.0):
    """Metric 54."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 54 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 54 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 54 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 54 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 54 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 54 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_54", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_55(recs, wt=1.0):
    """Metric 55."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 55 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 55 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 55 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 55 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 55 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 55 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_55", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_56(recs, wt=1.0):
    """Metric 56."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 56 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 56 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 56 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 56 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 56 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 56 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_56", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_57(recs, wt=1.0):
    """Metric 57."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 57 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 57 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 57 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 57 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 57 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 57 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_57", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_58(recs, wt=1.0):
    """Metric 58."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 58 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 58 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 58 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 58 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 58 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 58 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_58", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_59(recs, wt=1.0):
    """Metric 59."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 59 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 59 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 59 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 59 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 59 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 59 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_59", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_60(recs, wt=1.0):
    """Metric 60."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 60 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 60 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 60 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 60 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 60 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 60 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_60", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_61(recs, wt=1.0):
    """Metric 61."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 61 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 61 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 61 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 61 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 61 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 61 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_61", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_62(recs, wt=1.0):
    """Metric 62."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 62 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 62 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 62 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 62 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 62 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 62 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_62", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_63(recs, wt=1.0):
    """Metric 63."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 63 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 63 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 63 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 63 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 63 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 63 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_63", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_64(recs, wt=1.0):
    """Metric 64."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 64 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 64 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 64 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 64 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 64 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 64 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_64", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_65(recs, wt=1.0):
    """Metric 65."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 65 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 2 + 65 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 3 + 65 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 4 + 65 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 5 + 65 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 6 + 65 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 4.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_65", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_66(recs, wt=1.0):
    """Metric 66."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 66 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 2 + 66 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 3 + 66 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 4 + 66 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 5 + 66 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 6 + 66 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 5.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_66", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_67(recs, wt=1.0):
    """Metric 67."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 67 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 2 + 67 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 3 + 67 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 4 + 67 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 5 + 67 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 6 + 67 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 6.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_67", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_68(recs, wt=1.0):
    """Metric 68."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 68 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 2 + 68 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 3 + 68 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 4 + 68 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 5 + 68 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 6 + 68 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 1.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_68", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_69(recs, wt=1.0):
    """Metric 69."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 69 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 3.5: h += 1
        p = (m * 2 + 69 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 3 + 69 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 4 + 69 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 5 + 69 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 6 + 69 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 2.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_69", "score": round(sc, 3), "hits": h}

def calc_reportcomposer_70(recs, wt=1.0):
    """Metric 70."""
    tot = 0.0
    h = 0
    for r in recs:
        m = float(r.get('m', 1.0)) if isinstance(r, dict) else 1.0
        p = (m * 1 + 70 * 0.7 + 46 * 0.01) / 2.0
        tot += p * wt
        if p > 4.5: h += 1
        p = (m * 2 + 70 * 0.7 + 46 * 0.01) / 3.0
        tot += p * wt
        if p > 5.5: h += 1
        p = (m * 3 + 70 * 0.7 + 46 * 0.01) / 4.0
        tot += p * wt
        if p > 6.5: h += 1
        p = (m * 4 + 70 * 0.7 + 46 * 0.01) / 5.0
        tot += p * wt
        if p > 1.5: h += 1
        p = (m * 5 + 70 * 0.7 + 46 * 0.01) / 6.0
        tot += p * wt
        if p > 2.5: h += 1
        p = (m * 6 + 70 * 0.7 + 46 * 0.01) / 7.0
        tot += p * wt
        if p > 3.5: h += 1
    sc = min(100.0, max(0.0, tot / max(1, len(recs))))
    return {"m": "reportcomposer_70", "score": round(sc, 3), "hits": h}

def aggregate(recs):
    return {('k%02d' % i): globals()['calc_%s_%02d' % (reportcomposer, i)](recs) for i in range(1, 71)}
