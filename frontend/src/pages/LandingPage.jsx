import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import {
  Shield, Sparkles, Calendar, Users, DoorOpen, Grid, FileText, CheckCircle2,
  ArrowRight, Layers, Clock, Cpu, Award, HelpCircle, ChevronDown, ChevronUp,
  Download, BarChart2, BookOpen, AlertCircle
} from 'lucide-react';

export default function LandingPage({ onNavigate }) {
  const [activeFaq, setActiveFaq] = useState(null);

  const modulesList = [
    { num: '01', title: 'User & Role Access Control', member: 'Member 1', desc: 'Secure Django authentication, RBAC permissions, and administrative session controls.' },
    { num: '02', title: 'Faculty Profile & Availability', member: 'Member 1', desc: 'Faculty directory, availability schedules, leave approvals, and workload counters.' },
    { num: '03', title: 'Curriculum & Academic Structure', member: 'Member 2', desc: 'Departments, degree courses, branches, semesters, and subject credit catalogs.' },
    { num: '04', title: 'Student Enrollment & CSV Engine', member: 'Member 2', desc: 'Student profile management, bulk CSV validation preview, duplicate detection, and exports.' },
    { num: '05', title: 'Subject & Exam Registration', member: 'Member 2', desc: 'Prerequisites, attendance shortage calculation (<75%), and exam eligibility verification.' },
    { num: '06', title: 'Examination Session Configuration', member: 'Member 3', desc: 'Session terms, session types (Regular/Backlog), and customizable time slots.' },
    { num: '07', title: 'Constraint-Based Timetable Solver', member: 'Member 3', desc: 'Python heuristic engine using MRV and backtracking to generate conflict-free schedules.' },
    { num: '08', title: 'Timetable Approval & Publishing', member: 'Member 3', desc: 'Controller sign-off workflow, version control, and multi-channel publication.' },
    { num: '09', title: 'Halls & Infrastructure Management', member: 'Member 4', desc: 'Building blocks, exam rooms, CCTV surveillance readiness, and usable capacity calculator.' },
    { num: '10', title: 'Smart Seating Plan & Visual Grid', member: 'Member 4', desc: 'Alternate-seat and checkerboard spacing algorithms, visual grid charts, and shortage alerts.' },
    { num: '11', title: 'Invigilator Allocation & Duty Roster', member: 'Member 4', desc: 'Leave-aware duty assignments, fair workload distribution, and room staffing checks.' },
    { num: '12', title: 'Hall Ticket Generation (ReportLab)', member: 'Member 5', desc: 'Local PDF generation with security hashes, seating details, and admit card verification.' },
    { num: '13', title: 'Exam Attendance & Malpractice Audit', member: 'Member 5', desc: 'Hall-wise attendance marking, answer booklet logging, and correction audit trails.' },
    { num: '14', title: 'Announcements & Notification Center', member: 'Member 5', desc: 'Role-targeted notices, schedule change alerts, and database-backed in-app messages.' },
    { num: '15', title: 'Executive Analytics & System Settings', member: 'Member 5', desc: 'Lifecycle readiness index, room utilization, PDF/CSV export, and institutional governance.' },
  ];

  const teamMembers = [
    {
      name: 'Member 1',
      role: 'Authentication & Faculty Subsystem',
      color: 'var(--color-forest)',
      deliverables: ['Custom User model & RBAC', 'Token Authentication & Passwords', 'Faculty Directory & Designations', 'Availability & Leave Approvals']
    },
    {
      name: 'Member 2',
      role: 'Academics & Student Management',
      color: 'var(--color-emerald)',
      deliverables: ['Departments, Courses & Semesters', 'Student Profiles & Roll Numbers', 'Bulk CSV Import & Validation', 'Subject Registration & Eligibility']
    },
    {
      name: 'Member 3',
      role: 'Examinations & Scheduling Engine',
      color: '#047857',
      deliverables: ['Exam Session Configuration', 'Python Constraint Solver Engine', 'Student Conflict & Clash Prevention', 'Timetable Approval & Publishing']
    },
    {
      name: 'Member 4',
      role: 'Infrastructure & Seating Allocation',
      color: '#b45309',
      deliverables: ['Rooms & Usable Capacity Rules', 'Visual Row/Col Seating Grid', 'Alternate Spacing Algorithm', 'Fair Invigilator Duty Roster']
    },
    {
      name: 'Member 5 (Lead & Integration)',
      role: 'Documents, Attendance & System Integration',
      color: '#D4A72C',
      deliverables: ['ReportLab Local PDF Generator', 'Hall Tickets & Eligibility Gates', 'Hall Attendance & Correction Audits', 'Readiness Index & Final QA']
    },
  ];

  const workflowSteps = [
    { step: 1, title: 'Session Setup', desc: 'Configure academic year, session codes, dates, and active time slots.' },
    { step: 2, title: 'Constraint Solving', desc: 'Python heuristics schedule all subjects with 0 student double-bookings.' },
    { step: 3, title: 'Room & Seating', desc: 'Allocate students to examination halls using alternate column spacing.' },
    { step: 4, title: 'Staffing Roster', desc: 'Assign invigilators fairly based on availability and leave records.' },
    { step: 5, title: 'Admit Card Issuance', desc: 'Generate verified Hall Ticket PDFs locally using ReportLab.' },
    { step: 6, title: 'Attendance & Reports', desc: 'Record room attendance, answer booklets, and export executive analytics.' },
  ];

  const faqs = [
    { q: 'Does ExamForge require third-party or cloud APIs to operate?', a: 'No. ExamForge operates 100% locally on institutional infrastructure without any external cloud APIs. All PDF generation is handled locally via ReportLab, and the timetable scheduling engine runs entirely on local Python constraint algorithms.' },
    { q: 'How does the constraint-based timetable engine prevent student exam clashes?', a: 'The engine models the scheduling problem as a constraint satisfaction problem (CSP). It builds an internal student conflict graph from active subject registrations. Exams sharing common students are strictly constrained from occupying the same date and time slot.' },
    { q: 'What happens if exam hall capacity is less than the number of registered students?', a: 'ExamForge detects capacity deficits immediately during the seating generation phase. Rather than silently omitting students, it generates a prominent Capacity Shortage Alert detailing exact unallocated roll numbers so administrators can assign additional halls.' },
    { q: 'How are Hall Tickets verified and protected against tampering?', a: 'Every issued Hall Ticket includes a unique cryptographic verification hash, institutional headers, exact assigned room and seat coordinates, and a digital approval record generated directly into the PDF.' },
    { q: 'Can examination hall attendance be corrected after submission?', a: 'Yes. Any subsequent status correction (e.g. absent to present) requires an authorized reason and is immutably logged into the AttendanceCorrectionAudit table with timestamp and acting user identity.' }
  ];

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--color-ivory)' }}>
      <Navbar onNavigate={onNavigate} />

      {/* Hero Section */}
      <section id="hero" style={{
        padding: '5rem 2rem 4rem 2rem',
        maxWidth: '1280px',
        margin: '0 auto',
        textAlign: 'center'
      }}>
        {/* Release Pill */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          backgroundColor: 'var(--color-sage)',
          color: 'var(--color-forest)',
          padding: '0.375rem 1rem',
          borderRadius: '9999px',
          fontSize: '0.8125rem',
          fontWeight: 700,
          marginBottom: '1.5rem',
          border: '1px solid #c8dec8'
        }}>
          <Sparkles size={14} color="#D4A72C" />
          Five-Member Integrated Operations System • Zero Blue Design
        </div>

        {/* Master Heading */}
        <h1 style={{
          fontSize: 'clamp(2.5rem, 5vw, 4rem)',
          fontWeight: 800,
          color: 'var(--color-forest)',
          lineHeight: 1.15,
          maxWidth: '900px',
          margin: '0 auto 1.5rem auto'
        }}>
          Examinations, Organized. From Schedule to Success.
        </h1>

        {/* Supporting Text */}
        <p style={{
          fontSize: 'clamp(1rem, 2vw, 1.25rem)',
          color: 'var(--color-charcoal)',
          maxWidth: '780px',
          margin: '0 auto 2.5rem auto',
          lineHeight: 1.6
        }}>
          Plan examinations, prevent scheduling conflicts, organize examination halls, allocate invigilators, and manage every stage of your examination process from one centralized platform.
        </p>

        {/* Hero CTAs */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => onNavigate('dashboard')}
            className="btn btn-primary"
            style={{ padding: '0.875rem 2rem', fontSize: '1rem', borderRadius: '0.625rem' }}
          >
            Launch Command Console <ArrowRight size={18} />
          </button>
          <button
            onClick={() => {
              const el = document.getElementById('modules');
              if (el) el.scrollIntoView({ behavior: 'smooth' });
            }}
            className="btn btn-outline"
            style={{ padding: '0.875rem 2rem', fontSize: '1rem', borderRadius: '0.625rem' }}
          >
            Explore 15 Modules
          </button>
        </div>

        {/* Live Dashboard Preview Card */}
        <div style={{
          marginTop: '4rem',
          backgroundColor: '#FFFFFF',
          borderRadius: '1.25rem',
          border: '1px solid var(--color-border)',
          boxShadow: 'var(--shadow-xl)',
          overflow: 'hidden',
          textAlign: 'left'
        }}>
          {/* Mock Browser Header */}
          <div style={{
            backgroundColor: '#F8FAF7',
            padding: '0.75rem 1.25rem',
            borderBottom: '1px solid var(--color-border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#ef4444' }} />
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#f59e0b' }} />
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#10b981' }} />
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)', marginLeft: '0.5rem' }}>
                https://examforge.internal/console/dashboard
              </span>
            </div>
            <span className="badge badge-success">Production Ready</span>
          </div>

          {/* Interactive Preview Content */}
          <div style={{ padding: '2rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
              <div style={{ padding: '1rem', backgroundColor: 'var(--color-sage-light)', borderRadius: '0.75rem', border: '1px solid var(--color-sage)' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Registered Candidates</div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-forest)' }}>1,480</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 600 }}>100% Validated in Database</div>
              </div>

              <div style={{ padding: '1rem', backgroundColor: 'var(--color-sage-light)', borderRadius: '0.75rem', border: '1px solid var(--color-sage)' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Timetable Status</div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-forest)' }}>0 Clashes</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 600 }}>Constraint Solver Verified</div>
              </div>

              <div style={{ padding: '1rem', backgroundColor: 'var(--color-sage-light)', borderRadius: '0.75rem', border: '1px solid var(--color-sage)' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-muted)' }}>Usable Hall Capacity</div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-forest)' }}>1,850 Seats</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 600 }}>Alternate Spacing Applied</div>
              </div>

              <div style={{ padding: '1rem', backgroundColor: 'var(--color-gold-light)', borderRadius: '0.75rem', border: '1px solid #fed7aa' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#92400e' }}>Lifecycle Readiness</div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#92400e' }}>100%</div>
                <div style={{ fontSize: '0.75rem', color: '#92400e', fontWeight: 600 }}>All 5 Phases Cleared</div>
              </div>
            </div>

            {/* Timetable Snippet Preview */}
            <div style={{ border: '1px solid var(--color-border)', borderRadius: '0.75rem', padding: '1rem', backgroundColor: '#FFFFFF' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-forest)' }}>
                  Active Examination Timetable — Spring Session
                </span>
                <span className="badge badge-success">Approved by Controller</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.75rem' }}>
                <div style={{ padding: '0.75rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#FBFDFB' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>11-May-2026 | 09:30 AM</div>
                  <div style={{ fontWeight: 700, color: 'var(--color-forest)' }}>CS401: Algorithms</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)' }}>Hall LH-101 • 30 Candidates</div>
                </div>
                <div style={{ padding: '0.75rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#FBFDFB' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>13-May-2026 | 09:30 AM</div>
                  <div style={{ fontWeight: 700, color: 'var(--color-forest)' }}>CS402: Operating Systems</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)' }}>Hall LH-101 • 30 Candidates</div>
                </div>
                <div style={{ padding: '0.75rem', border: '1px solid var(--color-border-light)', borderRadius: '0.5rem', backgroundColor: '#FBFDFB' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>15-May-2026 | 09:30 AM</div>
                  <div style={{ fontWeight: 700, color: 'var(--color-forest)' }}>CS403: Database Systems</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)' }}>Hall LH-102 • 30 Candidates</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 15 Modules Showcase Section */}
      <section id="modules" style={{ padding: '5rem 2rem', backgroundColor: '#FFFFFF', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <span className="badge badge-success" style={{ marginBottom: '0.5rem' }}>Full Functional Coverage</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--color-forest)', margin: '0.5rem 0' }}>
              15 Comprehensive System Modules
            </h2>
            <p style={{ color: 'var(--color-muted)', maxWidth: '650px', margin: '0 auto' }}>
              Every assigned module is implemented with real database schemas, complete validation, and internal DRF endpoints.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.5rem' }}>
            {modulesList.map((m) => (
              <div key={m.num} className="card" style={{ padding: '1.5rem', borderLeft: '4px solid var(--color-emerald)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontSize: '1.125rem', fontWeight: 800, color: 'var(--color-forest)' }}>{m.num}</span>
                  <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>{m.member}</span>
                </div>
                <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
                  {m.title}
                </h3>
                <p style={{ fontSize: '0.8125rem', color: 'var(--color-muted)', lineHeight: 1.5 }}>
                  {m.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 5-Member Team Architecture Overview */}
      <section id="team" style={{ padding: '5rem 2rem', backgroundColor: 'var(--color-ivory)', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <span className="badge badge-gold" style={{ marginBottom: '0.5rem' }}>Team Collaboration</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--color-forest)', margin: '0.5rem 0' }}>
              Five-Member Responsibility Architecture
            </h2>
            <p style={{ color: 'var(--color-muted)', maxWidth: '650px', margin: '0 auto' }}>
              Structured division of responsibilities with Member 5 coordinating final integration and end-to-end quality assurance.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: '1.25rem' }}>
            {teamMembers.map((tm, idx) => (
              <div key={idx} className="card" style={{ padding: '1.5rem', backgroundColor: '#FFFFFF' }}>
                <div style={{
                  width: '2.5rem',
                  height: '2.5rem',
                  borderRadius: '0.5rem',
                  backgroundColor: 'var(--color-sage)',
                  color: 'var(--color-forest)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '0.875rem',
                  marginBottom: '1rem'
                }}>
                  M{idx + 1}
                </div>
                <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-forest)', marginBottom: '0.25rem' }}>
                  {tm.name}
                </h3>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-emerald)', fontWeight: 600, marginBottom: '1rem' }}>
                  {tm.role}
                </div>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {tm.deliverables.map((d, dIdx) => (
                    <li key={dIdx} style={{ fontSize: '0.75rem', color: 'var(--color-charcoal)', display: 'flex', alignItems: 'flex-start', gap: '0.375rem' }}>
                      <CheckCircle2 size={13} color="var(--color-emerald)" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{d}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Complete Examination Workflow */}
      <section id="workflow" style={{ padding: '5rem 2rem', backgroundColor: '#FFFFFF', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <span className="badge badge-success" style={{ marginBottom: '0.5rem' }}>End-to-End Lifecycle</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--color-forest)', margin: '0.5rem 0' }}>
              The 6-Stage Examination Workflow
            </h2>
            <p style={{ color: 'var(--color-muted)', maxWidth: '650px', margin: '0 auto' }}>
              From student enrollment to final attendance reports, each phase strictly uses validated records from previous stages.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1.25rem', position: 'relative' }}>
            {workflowSteps.map((ws) => (
              <div key={ws.step} className="card" style={{ padding: '1.5rem', textAlign: 'center', position: 'relative' }}>
                <div style={{
                  width: '3rem',
                  height: '3rem',
                  borderRadius: '50%',
                  backgroundColor: 'var(--color-forest)',
                  color: '#FFFFFF',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1.125rem',
                  margin: '0 auto 1rem auto'
                }}>
                  {ws.step}
                </div>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.375rem' }}>
                  {ws.title}
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)', lineHeight: 1.5 }}>
                  {ws.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits for Colleges */}
      <section id="benefits" style={{ padding: '5rem 2rem', backgroundColor: 'var(--color-ivory)', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <span className="badge badge-success" style={{ marginBottom: '0.5rem' }}>Institutional Value</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--color-forest)', margin: '0.5rem 0' }}>
              Engineered for Higher Education Excellence
            </h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            <div className="card" style={{ padding: '1.75rem' }}>
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.75rem' }}><Clock size={28} /></div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
                90% Reduction in Scheduling Time
              </h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--color-muted)', lineHeight: 1.6 }}>
                Eliminate weeks of manual spreadsheet calculations. The constraint solver schedules hundreds of exam combinations in seconds.
              </p>
            </div>

            <div className="card" style={{ padding: '1.75rem' }}>
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.75rem' }}><Shield size={28} /></div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
                Zero Clashes & Malpractice Prevention
              </h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--color-muted)', lineHeight: 1.6 }}>
                Enforce alternate-seat spacing and branch separation so adjacent candidates never write the same paper.
              </p>
            </div>

            <div className="card" style={{ padding: '1.75rem' }}>
              <div style={{ color: 'var(--color-forest)', marginBottom: '0.75rem' }}><FileText size={28} /></div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-forest)', marginBottom: '0.5rem' }}>
                100% Self-Contained Local Operations
              </h3>
              <p style={{ fontSize: '0.875rem', color: 'var(--color-muted)', lineHeight: 1.6 }}>
                Generates high-resolution PDF admit cards and attendance logs locally on campus servers without recurring external SaaS costs.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Frequently Asked Questions */}
      <section id="faq" style={{ padding: '5rem 2rem', backgroundColor: '#FFFFFF', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ maxWidth: '840px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <span className="badge badge-gold" style={{ marginBottom: '0.5rem' }}>Operational Clarity</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--color-forest)', margin: '0.5rem 0' }}>
              Frequently Asked Questions
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {faqs.map((faq, idx) => {
              const isOpen = activeFaq === idx;
              return (
                <div key={idx} style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '0.75rem',
                  overflow: 'hidden',
                  backgroundColor: '#FFFFFF'
                }}>
                  <button
                    onClick={() => setActiveFaq(isOpen ? null : idx)}
                    style={{
                      width: '100%',
                      padding: '1.25rem 1.5rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      background: 'none',
                      border: 'none',
                      textAlign: 'left',
                      cursor: 'pointer',
                      fontWeight: 700,
                      fontSize: '1rem',
                      color: 'var(--color-forest)'
                    }}
                  >
                    <span>{faq.q}</span>
                    {isOpen ? <ChevronUp size={20} color="var(--color-muted)" /> : <ChevronDown size={20} color="var(--color-muted)" />}
                  </button>

                  {isOpen && (
                    <div style={{
                      padding: '0 1.5rem 1.25rem 1.5rem',
                      fontSize: '0.875rem',
                      color: 'var(--color-charcoal)',
                      lineHeight: 1.6,
                      borderTop: '1px solid var(--color-border-light)'
                    }}>
                      {faq.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Call to Action Footer Section */}
      <section style={{
        padding: '5rem 2rem',
        backgroundColor: 'var(--color-forest)',
        color: '#FFFFFF',
        textAlign: 'center'
      }}>
        <div style={{ maxWidth: '780px', margin: '0 auto' }}>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#FFFFFF', marginBottom: '1rem' }}>
            Ready to Streamline Examination Operations?
          </h2>
          <p style={{ fontSize: '1.125rem', color: 'var(--color-sage)', marginBottom: '2.5rem', lineHeight: 1.6 }}>
            Launch the ExamForge control console to explore all five integrated modules with live database records.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <button
              onClick={() => onNavigate('dashboard')}
              className="btn btn-gold"
              style={{ padding: '0.875rem 2.25rem', fontSize: '1rem', borderRadius: '0.625rem' }}
            >
              Open Command Console <ArrowRight size={18} />
            </button>
            <button
              onClick={() => onNavigate('login')}
              style={{
                backgroundColor: 'transparent',
                color: '#FFFFFF',
                border: '1px solid #FFFFFF',
                padding: '0.875rem 2rem',
                fontSize: '1rem',
                borderRadius: '0.625rem',
                cursor: 'pointer',
                fontWeight: 600
              }}
            >
              User Login
            </button>
          </div>
        </div>
      </section>

      {/* Institutional Footer */}
      <footer style={{
        backgroundColor: '#0f3d21',
        color: '#a3b8a3',
        padding: '3rem 2rem',
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        fontSize: '0.8125rem'
      }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Shield size={20} color="#D4A72C" />
            <span style={{ fontWeight: 800, color: '#FFFFFF', fontSize: '1rem' }}>ExamForge</span>
            <span>— Examination Operations System</span>
          </div>

          <div>
            Built with Django REST Framework, PostgreSQL/SQLite, React.js & ReportLab.
          </div>

          <div>
            © 2026 Five-Member Integrated Academic Consortium. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
