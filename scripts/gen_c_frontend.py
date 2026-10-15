"""Gen-C: frontend pages + services."""
import os
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def w(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(c)
pages = ["AnalyticsPage", "DutyRosterPage", "DoorChartsPage", "ShortageReportPage", "AccommodationPage", "RemunerationPage", "VaultAuditPage", "ModerationPage"]
for idx, name in enumerate(pages, 1):
    L = ["import React, { useMemo, useState } from 'react';\n"]
    L.append("const ROWS = [")
    for i in range(1, 151):
        st = "active" if i % 3 == 0 else ("pending" if i % 3 == 1 else "archived")
        L.append('  { code: "%s-%d", title: "%s record %d trail", owner: "Controller", status: "%s", score: %s },' % (name[:3].upper(), 1000 + idx * 200 + i, name, i, st, 88 + (i % 12)))
    L.append("];\n")
    L.append("export default function %s() {" % name)
    L.append("  const [q, setQ] = useState('');")
    L.append("  const [st, setSt] = useState('all');")
    L.append("  const rows = useMemo(() => ROWS.filter((r) => (q === '' || r.title.toLowerCase().includes(q.toLowerCase())) && (st === 'all' || r.status === st)), [q, st]);")
    L.append("  return (")
    L.append("    <div style={{ padding: '1.5rem' }}>")
    L.append("      <h1>%s</h1>" % name)
    L.append("      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Search...' />")
    L.append("      <select value={st} onChange={(e) => setSt(e.target.value)}><option value='all'>All</option><option value='active'>Active</option><option value='pending'>Pending</option></select>")
    L.append("      <table><tbody>{rows.map((r) => (<tr key={r.code}><td>{r.code}</td><td>{r.title}</td><td>{r.owner}</td><td>{r.status}</td><td>{r.score}</td></tr>))}</tbody></table>")
    L.append("    </div>")
    L.append("  );\n}")
    L.append("")
    w(os.path.join(B, "frontend/src/pages", name + ".jsx"), "\n".join(L))
for svc, base in [("analyticsService", "/api/analytics"), ("seatingService", "/api/seating"), ("venueService", "/api/venues"), ("bylawService", "/api/bylaws")]:
    L = ["import api from './api';", "const BASE = '%s';" % base, ""]
    for op in ["list", "retrieve", "create", "update", "remove", "search", "summary", "exportCsv", "bulkUpdate", "auditTrail", "stats", "history"]:
        L.append("export async function %s%s(p) { const r = await api.get(BASE + '/%s/', { params: p }); return r.data; }" % (svc, op[0].upper() + op[1:], op))
        L.append("")
    w(os.path.join(B, "frontend/src/services", svc + ".js"), "\n".join(L))
print("gen-c done")
