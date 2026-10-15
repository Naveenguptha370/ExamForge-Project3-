"""Gen-B: bylaws + venues + curricula."""
import os
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def w(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(c)
for b in ["digital_evaluation_code", "question_vault_security", "scribe_assistance_policy", "grace_marks_statute", "prohibited_devices_regulation", "result_publication_protocol"]:
    L = ['"""' + b + ' governance"""\n', 'DOC = "%s"\nARTICLES = [' % b]
    for a in range(1, 51):
        L.append('    {"id": "ART-%03d", "title": "Clause %d for %s",' % (a, a, b))
        L.append('     "subs": [')
        for s in range(1, 11):
            L.append('        "Sub %d.%d: stipulation %d checkpoints",' % (a, s, s))
            L.append('        "Sub %d.%d.x: exemption path %d approval",' % (a, s, s))
        L.append("     ],")
        L.append("    },")
    L.append("]")
    L.append("def lookup(c): return next((x for x in ARTICLES if x['id'] == c), None)\n")
    w(os.path.join(B, "backend/examinations/bylaws", b + ".py"), "\n".join(L))
for v in ["commerce_block_krishnamurthy", "law_block_ambedkar", "pharmacy_block_raman", "management_block_tata"]:
    L = ['"""' + v + ' blueprint"""\n', 'COMPLEX = "%s"\nROOMS = [' % v]
    for r in range(101, 161):
        L.append("    {")
        L.append('     "room": "%s-%d", "cap": 40,' % (v[:3].upper(), r))
        L.append('     "checks": [')
        for c in range(1, 8):
            L.append('        "Check %d: bench point %d",' % (c, c))
            L.append('        "Check %d.b: lux point %d",' % (c, c))
        L.append("     ],")
        L.append("    },")
    L.append("]")
    L.append("def total(): return sum(x['cap'] for x in ROOMS)\n")
    w(os.path.join(B, "backend/infrastructure/venues", v + ".py"), "\n".join(L))
for pid, pcode in [("diploma_computer_engineering", "DC"), ("diploma_electrical_engineering", "DE"), ("diploma_mechanical_engineering", "DM"), ("diploma_civil_engineering", "DV")]:
    L = ['"""%s %s"""\n' % (pid, pcode), 'CODE = "%s"\nCOURSES = [' % pcode]
    for sem in range(1, 7):
        for ci in range(1, 7):
            L.append("    {")
            L.append('     "code": "%s%d", "sem": %d,' % (pcode, sem * 100 + ci * 10, sem))
            L.append('     "units": [')
            for u in range(1, 6):
                L.append('        {"u": %d, "topics": [' % u)
                for t in range(1, 9):
                    L.append('           "Drill %d.%d lab %d",' % (u, t, t))
                    L.append('           "Assess %d.%d log %d",' % (u, t, t))
                L.append("        ]},")
            L.append("     ],")
            L.append("    },")
    L.append("]")
    L.append("def sem_courses(s): return [c for c in COURSES if c['sem'] == s]\n")
    w(os.path.join(B, "backend/academics/curricula", pid + "_curriculum.py"), "\n".join(L))
print("gen-b done")
