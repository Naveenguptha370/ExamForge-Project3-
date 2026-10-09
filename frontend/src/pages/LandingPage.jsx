import React, { useState } from 'react';
import {
  Calendar, Clock, Shield, Sparkles, CheckCircle2,
  ArrowRight, Users, BookOpen, Layers, Grid, FileText,
  CheckSquare, Bell, BarChart3, ChevronDown, ChevronUp, Download, Play
} from 'lucide-react';

export const LandingPage = ({ onGetStarted, onLogin }) => {
  const [openFaq, setOpenFaq] = useState(null);

  const modules15 = [
    { num: '01', title: 'Authentication & Access Control', member: 'Member 1', desc: 'Secure Django authentication, role-based permissions (Admin, Faculty, Staff, Student), session security.' },
    { num: '02', title: 'Faculty & Workload Directory', member: 'Member 1', desc: 'Faculty profiles, departmental designations, shift availability schedules, and leave tracking.' },
    { num: '03', title: 'Academic Structure & Curriculum', member: 'Member 2', desc: 'Departments, degree programs, branches, semesters, subject credits, and difficulty ratings.' },
    { num: '04', title: 'Student Records & CSV Importer', member: 'Member 2', desc: 'Student catalog, bulk CSV import with instant validation, duplicate detection, and eligibility checks.' },
    { num: '05', title: 'Subject & Exam Registration', member: 'Member 2', desc: 'Regular and supplementary subject enrollments, eligibility matrix, and fee validation.' },
    { num: '06', title: 'Examination Configuration', member: 'Member 3', desc: 'Exam sessions, academic terms, date ranges, subject selection, and lifecycle states (Draft to Published).' },
    { num: '07', title: 'Time Slots & Shift Management', member: 'Member 3', desc: 'Morning, afternoon, and evening examination shift definitions with strict duration constraints.' },
    { num: '08', title: 'AI Constraint Scheduling Engine', member: 'Member 3', desc: 'Genuine Python CSP solver using MRV, Degree heuristics, LCV, and backtracking with forward checking.' },
    { num: '09', title: 'Conflict Radar & Revalidation', member: 'Member 3', desc: 'Automatic detection of student double-booking, branch clashes, room capacity limits, and manual override audit.' },
    { num: '10', title: 'Rooms & Campus Infrastructure', member: 'Member 4', desc: 'Exam halls, usable seating capacities, CCTV coverage, accessibility, and maintenance schedules.' },
    { num: '11', title: 'Seating Arrangement Matrix', member: 'Member 4', desc: 'Visual grid seating generation, alternate desk spacing rules, and hall-wise student allocations.' },
    { num: '12', title: 'Invigilator Workload Balancing', member: 'Member 4', desc: 'Automated duty roster with fair distribution of exam duties across available faculty.' },
    { num: '13', title: 'Hall Ticket Generator (Local PDF)', member: 'Member 5', desc: 'Individual and bulk admit card generation with barcodes, seating details, and printable ReportLab PDFs.' },
    { num: '14', title: 'Examination Attendance & Malpractice', member: 'Member 5', desc: 'Room-wise attendance sheets, answer booklet logging, and malpractice incident recording.' },
    { num: '15', title: 'Institutional Analytics & Audit Logs', member: 'Member 5', desc: 'Readiness score gauge, room utilization heatmaps, daily load charts, and tamper-resistant audit logs.' },
  ];

  const faqs = [
    { q: 'How does the constraint-based scheduling engine prevent student clashes?', a: 'ExamForge formulates examination timetabling as a Constraint Satisfaction Problem (CSP). It queries real student enrollment records and branch structures. Using Minimum Remaining Values (MRV) and forward checking, it ensures that no student is scheduled for more than one exam in the same slot or on the same day.' },
    { q: 'Can administrators manually override the generated timetable?', a: 'Yes! The Timetable Studio provides an interactive schedule matrix where authorized users can drag or reassign any subject to a new date/slot. Upon saving, the system live-revalidates all hard and soft constraints, logs a revision entry, and increments the timetable version.' },
    { q: 'Does ExamForge require external API keys or cloud services?', a: 'No. ExamForge is 100% self-contained. All scheduling algorithms, local PDF generators, database operations, and notification services run locally on your institutional infrastructure without third-party dependencies.' },
    { q: 'How are hall tickets and attendance sheets generated?', a: 'Hall tickets are dynamically compiled using ReportLab directly from validated timetable entries and seating allocations. Students and staff can preview and download high-resolution official PDF passes locally.' },
  ];

  return (
    <div style={{ backgroundColor: 'var(--color-bg)', minHeight: '100vh', color: 'var(--color-text)' }}>
      {/* SaaS Landing Navigation */}
      <nav
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          backgroundColor: 'rgba(250, 249, 246, 0.92)',
          backdropFilter: 'blur(10px)',
          borderBottom: '1px solid #E7E5E4',
          padding: '0 40px',
          height: 76,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div
            style={{
              width: 42,
              height: 42,
              borderRadius: 12,
              backgroundColor: '#14532D',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#D4A72C',
              fontWeight: 800,
              fontSize: '1.3rem',
              boxShadow: '0 2px 10px rgba(20, 83, 45, 0.25)'
            }}
          >
            EF
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '1.35rem', fontWeight: 800, color: '#14532D', fontFamily: 'var(--font-display)', letterSpacing: '-0.02em' }}>
              Exam<span style={{ color: '#D4A72C' }}>Forge</span>
            </span>
            <span style={{ fontSize: '0.7rem', fontWeight: 700, color: '#15803D', letterSpacing: '0.04em' }}>
              EXAMINATION OPERATIONS SYSTEM
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 28, fontSize: '0.92rem', fontWeight: 600, color: '#242923' }}>
          <a href="#features" style={{ transition: 'color 0.15s' }}>Features</a>
          <a href="#modules" style={{ transition: 'color 0.15s' }}>15 Modules</a>
          <a href="#workflow" style={{ transition: 'color 0.15s' }}>Workflow</a>
          <a href="#preview" style={{ transition: 'color 0.15s' }}>Studio Preview</a>
          <a href="#faq" style={{ transition: 'color 0.15s' }}>FAQ</a>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <button onClick={onLogin} className="btn btn-secondary btn-sm">
            Sign In
          </button>
          <button onClick={onGetStarted} className="btn btn-primary btn-sm">
            <span>Launch Operations</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        style={{
          padding: '80px 40px 60px',
          maxWidth: 1240,
          margin: '0 auto',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <div
          className="animate-fade-in"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '6px 16px',
            borderRadius: 9999,
            backgroundColor: '#DDEBDD',
            border: '1px solid #c0dcbf',
            color: '#14532D',
            fontSize: '0.85rem',
            fontWeight: 700,
            marginBottom: 24
          }}
        >
          <Sparkles size={16} color="#15803D" />
          <span>Powered by Genuine Python Constraint-Satisfaction Engine</span>
        </div>

        <h1
          style={{
            fontSize: '3.6rem',
            fontWeight: 800,
            color: '#14532D',
            lineHeight: 1.15,
            maxWidth: 950,
            marginBottom: 24,
            letterSpacing: '-0.03em'
          }}
        >
          Examinations, Organized.<br />
          <span style={{ color: '#D4A72C' }}>From Schedule to Success.</span>
        </h1>

        <p
          style={{
            fontSize: '1.2rem',
            color: '#575E54',
            maxWidth: 780,
            lineHeight: 1.6,
            marginBottom: 36
          }}
        >
          Plan examinations, eliminate student scheduling conflicts, allocate halls with precision, balance invigilation duties, and manage every stage of your examination lifecycle from one centralized platform.
        </p>

        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 50 }}>
          <button onClick={onGetStarted} className="btn btn-primary btn-lg">
            <span>Explore Examination Studio</span>
            <ArrowRight size={18} />
          </button>
          <a href="#modules" className="btn btn-secondary btn-lg">
            <span>View All 15 Modules</span>
          </a>
        </div>

        {/* Live Interactive Hero Preview Card */}
        <div
          id="preview"
          className="card animate-fade-in"
          style={{
            width: '100%',
            maxWidth: 1100,
            backgroundColor: '#FFFFFF',
            borderRadius: 24,
            padding: 28,
            boxShadow: '0 25px 50px -12px rgba(20, 83, 45, 0.18)',
            border: '1px solid #DDEBDD',
            textAlign: 'left'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid #E7E5E4' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#15803D' }} />
              <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#D4A72C' }} />
              <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#F59E0B' }} />
              <span style={{ marginLeft: 10, fontSize: '0.92rem', fontWeight: 700, color: '#14532D' }}>
                End Semester Examinations — Autumn 2025 [ESE-AUT-2025]
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#15803D', backgroundColor: '#DCFCE7', padding: '4px 10px', borderRadius: 9999 }}>
                ✓ CSP Solver: 0 Clashes (100% Conflict-Free)
              </span>
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ backgroundColor: '#FAF9F6', padding: '14px 18px', borderRadius: 12, border: '1px solid #E7E5E4' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#6B7280' }}>Configured Subjects</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#14532D' }}>24 Subjects</div>
            </div>
            <div style={{ backgroundColor: '#FAF9F6', padding: '14px 18px', borderRadius: 12, border: '1px solid #E7E5E4' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#6B7280' }}>Total Candidates</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#14532D' }}>155 Students</div>
            </div>
            <div style={{ backgroundColor: '#FAF9F6', padding: '14px 18px', borderRadius: 12, border: '1px solid #E7E5E4' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#6B7280' }}>Halls Allocated</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#14532D' }}>15 Rooms (640 Cap)</div>
            </div>
            <div style={{ backgroundColor: '#FAF9F6', padding: '14px 18px', borderRadius: 12, border: '1px solid #E7E5E4' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#6B7280' }}>Readiness Score</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#D4A72C' }}>92% Ready</div>
            </div>
          </div>

          {/* Sample Schedule Table */}
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Date & Shift</th>
                  <th>Time Slot</th>
                  <th>Subject Code & Title</th>
                  <th>Department / Branch</th>
                  <th>Credits</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><b>10-Nov-2025 (Mon)</b></td>
                  <td>09:30 AM - 12:30 PM <span style={{ color: '#15803D', fontWeight: 700 }}>(Morning)</span></td>
                  <td><b>CS501</b> - Operating Systems</td>
                  <td>B.Tech Computer Science (Sem 5)</td>
                  <td>4.0</td>
                  <td><span className="badge badge-validated">Scheduled</span></td>
                </tr>
                <tr>
                  <td><b>10-Nov-2025 (Mon)</b></td>
                  <td>01:30 PM - 04:30 PM <span style={{ color: '#D97706', fontWeight: 700 }}>(Afternoon)</span></td>
                  <td><b>EC501</b> - Digital Signal Processing</td>
                  <td>B.Tech Electronics (Sem 5)</td>
                  <td>4.0</td>
                  <td><span className="badge badge-validated">Scheduled</span></td>
                </tr>
                <tr>
                  <td><b>11-Nov-2025 (Tue)</b></td>
                  <td>09:30 AM - 12:30 PM <span style={{ color: '#15803D', fontWeight: 700 }}>(Morning)</span></td>
                  <td><b>ME501</b> - Design of Machine Elements</td>
                  <td>B.Tech Mechanical (Sem 5)</td>
                  <td>4.0</td>
                  <td><span className="badge badge-validated">Scheduled</span></td>
                </tr>
                <tr>
                  <td><b>12-Nov-2025 (Wed)</b></td>
                  <td>09:30 AM - 12:30 PM <span style={{ color: '#15803D', fontWeight: 700 }}>(Morning)</span></td>
                  <td><b>CS502</b> - Database Management Systems</td>
                  <td>B.Tech Computer Science (Sem 5)</td>
                  <td>4.0</td>
                  <td><span className="badge badge-validated">Scheduled</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 15 Modules Section */}
      <section id="modules" style={{ padding: '80px 40px', backgroundColor: '#FFFFFF', borderTop: '1px solid #E7E5E4' }}>
        <div style={{ maxWidth: 1240, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 50 }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#15803D', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Full-Stack Architecture
            </span>
            <h2 style={{ fontSize: '2.5rem', color: '#14532D', marginTop: 8 }}>
              15 Integrated Enterprise Modules
            </h2>
            <p style={{ fontSize: '1.05rem', color: '#6B7280', maxWidth: 680, margin: '10px auto 0' }}>
              Designed by a team of 5 engineering members, united into one cohesive platform with zero external API dependencies.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24 }}>
            {modules15.map((m, idx) => (
              <div
                key={idx}
                className="card card-hover"
                style={{
                  padding: 24,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 12,
                  backgroundColor: '#FAF9F6',
                  borderColor: m.member.includes('3') ? '#b8d6b8' : '#E7E5E4',
                  borderTop: m.member.includes('3') ? '4px solid #15803D' : '1px solid #E7E5E4'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#15803D', fontFamily: 'var(--font-display)' }}>
                    {m.num}
                  </span>
                  <span
                    style={{
                      fontSize: '0.72rem',
                      fontWeight: 700,
                      padding: '3px 8px',
                      borderRadius: 6,
                      backgroundColor: m.member.includes('3') ? '#DDEBDD' : '#E7E5E4',
                      color: m.member.includes('3') ? '#14532D' : '#575E54'
                    }}
                  >
                    {m.member}
                  </span>
                </div>
                <h3 style={{ fontSize: '1.1rem', color: '#14532D' }}>{m.title}</h3>
                <p style={{ fontSize: '0.88rem', color: '#575E54', lineHeight: 1.5 }}>{m.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5-Member Workflow Timeline */}
      <section id="workflow" style={{ padding: '80px 40px', maxWidth: 1240, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#15803D', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Seamless Lifecycle
          </span>
          <h2 style={{ fontSize: '2.5rem', color: '#14532D', marginTop: 8 }}>
            End-to-End Examination Workflow
          </h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16 }}>
          {[
            { step: '01', title: 'Curriculum & Intake', lead: 'Member 1 & 2', desc: 'Configure departments, subjects, faculty schedules, and bulk import students via CSV.' },
            { step: '02', title: 'CSP Constraint Solving', lead: 'Member 3 (Primary)', desc: 'Run genuine Python CSP solver with MRV & degree heuristics to build clash-free timetables.' },
            { step: '03', title: 'Approval & Publishing', lead: 'Member 3 & Admin', desc: 'Resolve soft advisories, lock timetable revisions, and officially publish to campus.' },
            { step: '04', title: 'Halls & Seating Matrix', lead: 'Member 4', desc: 'Auto-allocate students into rooms with alternate desk spacing and assign faculty duties.' },
            { step: '05', title: 'Passes, Attendance & Audit', lead: 'Member 5', desc: 'Generate ReportLab PDF Hall Tickets, record room attendance, and inspect audit logs.' },
          ].map((wf, idx) => (
            <div key={idx} className="card" style={{ padding: 20, display: 'flex', flexDirection: 'column', gap: 10, backgroundColor: '#FFFFFF' }}>
              <div style={{ width: 34, height: 34, borderRadius: 8, backgroundColor: '#14532D', color: '#D4A72C', fontWeight: 800, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.9rem' }}>
                {wf.step}
              </div>
              <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#15803D' }}>{wf.lead}</span>
              <h4 style={{ fontSize: '1rem', color: '#242923' }}>{wf.title}</h4>
              <p style={{ fontSize: '0.82rem', color: '#6B7280', lineHeight: 1.45 }}>{wf.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ Accordion */}
      <section id="faq" style={{ padding: '80px 40px', backgroundColor: '#FFFFFF', borderTop: '1px solid #E7E5E4' }}>
        <div style={{ maxWidth: 860, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 40 }}>
            <h2 style={{ fontSize: '2.3rem', color: '#14532D' }}>Frequently Asked Questions</h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {faqs.map((f, idx) => (
              <div
                key={idx}
                className="card"
                style={{ overflow: 'hidden', cursor: 'pointer' }}
                onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
              >
                <div style={{ padding: '18px 22px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '1.02rem', fontWeight: 700, color: '#14532D' }}>{f.q}</span>
                  {openFaq === idx ? <ChevronUp size={20} color="#15803D" /> : <ChevronDown size={20} color="#6B7280" />}
                </div>
                {openFaq === idx && (
                  <div style={{ padding: '0 22px 18px', fontSize: '0.92rem', color: '#575E54', lineHeight: 1.6, borderTop: '1px solid #F3F4F6' }}>
                    {f.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action & Footer */}
      <footer style={{ backgroundColor: '#14532D', color: '#FFFFFF', padding: '60px 40px 40px', textAlign: 'center' }}>
        <div style={{ maxWidth: 1240, margin: '0 auto' }}>
          <h2 style={{ fontSize: '2.5rem', color: '#FFFFFF', marginBottom: 16 }}>
            Ready to Transform Your Institutional Examinations?
          </h2>
          <p style={{ fontSize: '1.1rem', color: '#DDEBDD', maxWidth: 650, margin: '0 auto 30px' }}>
            Eliminate scheduling bottlenecks, automate seating layouts, and issue verified admit cards seamlessly.
          </p>
          <button onClick={onGetStarted} className="btn btn-gold btn-lg" style={{ color: '#14532D', fontWeight: 800 }}>
            <span>Enter Examination Studio</span>
            <ArrowRight size={18} />
          </button>

          <div style={{ marginTop: 60, paddingTop: 30, borderTop: '1px solid rgba(255, 255, 255, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.85rem', color: '#DDEBDD' }}>
            <span>© 2026 ExamForge — Examination Operations System. All rights reserved.</span>
            <span>Strict Green & Gold UI Theme • Zero External API Keys</span>
          </div>
        </div>
      </footer>
    </div>
  );
};
