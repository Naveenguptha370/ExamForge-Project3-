# ExamForge — Python Constraint-Satisfaction Timetable Engine (Member 3)

## 1. Executive Summary & Problem Formulation

The **ExamForge Scheduling Subsystem** addresses the NP-hard University Examination Timetabling Problem (UETP) using a deterministic Constraint Satisfaction Problem (CSP) architecture.

The engine guarantees:
1. **Zero Student Double-Booking (Hard Constraint)**: No student enrolled in $N$ subjects can ever be assigned to two examinations in the same time slot or on the same calendar date.
2. **Branch & Semester Collision Avoidance (Hard Constraint)**: Disjoint or common core subjects for the same branch and semester are distributed across distinct examination days.
3. **Institutional Usable Capacity Feasibility (Hard Constraint)**: Total simultaneous candidate load in any slot $\sum \text{Candidates}(S_i)$ never exceeds total campus usable exam capacity $C_{\text{campus}}$.
4. **Study Gap Optimization (Soft Constraint)**: Insertion of 1 to 2 rest days between heavy computation and high-difficulty subjects.
5. **Weekend Policy Compliance**: Configurable inclusion/exclusion of Saturdays and Sundays.

---

## 2. Mathematical Formulation

### Variables
Let $\mathcal{V} = \{X_1, X_2, \dots, X_N\}$ represent the set of configured examination subjects for a session.

### Domains
Each variable $X_i$ has a discrete domain $\mathcal{D}_i$:
$$\mathcal{D}_i = \{ (d, s) \mid d \in [D_{\text{start}}, D_{\text{end}}], \; s \in \mathcal{S}_{\text{active}}, \; \text{ValidDay}(d) \}$$

### Hard Constraints
1. **Student Conflict Exclusion**:
   $$\forall X_i, X_j \in \mathcal{V} \; (i \neq j): \quad \left( \text{Students}(X_i) \cap \text{Students}(X_j) \neq \emptyset \right) \implies \text{Date}(X_i) \neq \text{Date}(X_j)$$

2. **Branch & Semester Exclusion**:
   $$\forall X_i, X_j \in \mathcal{V}: \quad \left( \text{Branch}(X_i) = \text{Branch}(X_j) \land \text{Sem}(X_i) = \text{Sem}(X_j) \right) \implies \text{Date}(X_i) \neq \text{Date}(X_j)$$

3. **Room Capacity Limit**:
   $$\forall (d, s) \in \mathcal{D}: \quad \sum_{X_i \in \text{Assigned}(d, s)} \text{ExpectedStudents}(X_i) \le C_{\text{campus}}$$

---

## 3. Search Algorithm & Heuristics

### A. Variable Ordering
- **Minimum Remaining Values (MRV)**: Selects the variable with the smallest legal domain size first.
- **Degree Heuristic**: Breaks ties by choosing the subject enrolled by the highest number of students or belonging to larger branch cohorts.

### B. Value Ordering
- **Least-Constraining Value (LCV)**: Prioritizes date-slot pairs that leave the maximum number of options open for remaining unassigned variables and minimize consecutive difficult exams.

### C. Forward Checking & Backtracking
- Employs iterative depth-first backtracking with domain reduction.
- Safety cutoff timer (default 30s) prevents unbounded search, returning an accurate diagnostic outcome (`SUCCESS`, `PARTIAL`, or `INFEASIBLE`).

---

## 4. Execution Lifecycle & Outcomes

```
[Exam Session Configured] 
       ↓
[Populate Active Subjects] 
       ↓
[Run CSP Solver Engine] 
       ↓
 ├── 100% Conflict-Free? ──> [Status: VALIDATED] ──> [Admin Approval] ──> [Published to Campus]
 └── Unplaced Subjects? ───> [Status: DRAFT] ─────> [Manual Override / Date Extension]
```
