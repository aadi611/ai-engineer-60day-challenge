# 🎓 GATE 2027: Robotics and Automation (RA) Prep Plan

**Exam window:** Feb 6, 7, 13, 14, 20, 21, 2027 (your exact date/session is on the admit card) · **Result:** Mar 19, 2027
**Prep window:** Nov 11, 2026 → exam (~12-14 weeks) · **Status at start:** syllabus ~half done
**Mode:** GATE first. The AI/Cyber plan runs at a 30-min/day maintenance pace until the exam (see [../progress_tracker.md](../progress_tracker.md)).

Official syllabus: [RA_GATE2027_Syllabus_official.pdf](RA_GATE2027_Syllabus_official.pdf) (from gate2027.iitm.ac.in).
Topic-by-topic checklist: **[syllabus_tracker.md](syllabus_tracker.md)**.

---

## Exam pattern

| Section | Marks | Questions | Notes |
|---|---|---|---|
| General Aptitude | 15 | 10 | Common to all GATE papers |
| **Part A** (compulsory): A.1 Eng. Maths · A.2 Mechatronics · A.3 Robotics & Automation | **60** | 39 | The core. Most of your time goes here |
| **Part B** (choose **one** in the exam): B1 Electrical **or** B2 Mechanical | **25** | 16 | Prepare only one |

3 hours, 65 questions, MCQ/MSQ/NAT, virtual calculator only. Negative marking only on MCQs (−1/3 and −2/3).
*(Marks split is from a third-party guide quoting the brochure. Confirm in the official information brochure.)*

### Choose B1 or B2 now (don't prepare both)

- **B1 Electrical (default in this plan):** analog + embedded, signals & systems, control systems. Control
  systems and signals reuse your A.1 maths (Laplace, Fourier) and have **many** previous-year questions in EE/IN/EC.
  It also fits the AI/software direction better.
- **B2 Mechanical:** mechanics of materials, kinematics & dynamics of machines, machine design. Pick it only if you
  have a mechanical background, since it is heavy on derivations and formulas you haven't used recently.

---

## ⚠️ RA is a brand-new paper, so there are no RA previous-year questions

Practice each topic with past GATE questions from the papers that share it:

| Topic | Practise with GATE PYQs from |
|---|---|
| Engineering Maths | ME, EE, IN (same syllabus style) |
| Network elements, digital circuits | EE, IN, EC |
| Sensors & transducers | IN |
| Actuators / motors | EE (basic machines), IN |
| Engineering mechanics | ME, CE |
| Python + data structures | DA, CS |
| Robotics kinematics (A.3) | Almost none → textbook exercises (S.K. Saha *Introduction to Robotics*; J.J. Craig) |
| CIM: PLC, AS/RS, AMHS, CNC, auto-ID (A.3) | ME manufacturing PYQs + **Groover**, *Automation, Production Systems, and CIM*. The syllabus headings follow its chapters almost word for word |
| B1 control, signals, analog | EE, IN, EC (dense PYQ coverage) |
| General Aptitude | Any GATE paper, any year |

Also take any **RA-specific mock series** you can find (coaching institutes launched RA test series for 2027), because the
question style of a new paper is the biggest unknown.

---

## Daily schedule (work 12–9)

| Time | What |
|---|---|
| **8:00–10:15** | GATE: new topic (learn phase) / revision or full mock (later phases) |
| **10:15–10:45** | AI/DSA/Cyber maintenance (30 min) |
| **10:45–11:00** | Commit: GATE notes, mistake log, daily log |
| **9:45–10:30 pm** | GATE practice: 15-20 PYQs or formula-sheet revision. No new topics at night |
| **Saturday** | Weekly topic test or full mock (3 hrs) + analysis (1-1.5 hrs) + 1 hr AI |
| **Sunday** | Weak topics / backlog (3 hrs) + 1 GA set, then **rest** |

≈ 22 GATE hours a week.

---

## The plan, phase by phase

### Phase 1: Finish the syllabus (Nov 11 – Dec 22, 6 weeks)

**Nov 11 (Day 1):** open [syllabus_tracker.md](syllabus_tracker.md), mark every topic you've already learned, and **pick B1 or B2**.
Then work down the queue below, **skipping anything already done** (for done subjects, do 20 PYQs to confirm, then move on).
Pace: ~2-3 queue items per week.

**Priority queue (do in this order):**

| # | Topic | Section | Est. hrs (fresh) | Why this position |
|---|---|---|---|---|
| 1 | Robot classification, DOF, rotation matrices, homogeneous transforms, forward kinematics | A.3 | 10 | The paper's identity. Small syllabus, likely heavy weight, and no PYQs, so learn it early |
| 2 | Linear algebra + Probability & statistics | A.1 | 14 | Fast marks; used by A.3 (rotations) and B1 |
| 3 | Calculus + differential equations + Laplace + Fourier series | A.1 | 18 | Prerequisite for control systems and signals |
| 4 | Control systems | B1.3 | 12 | Biggest PYQ bank in B1; reuses Laplace |
| 5 | Signals & systems | B1.2 | 10 | Reuses Fourier/Laplace; add Z-transform |
| 6 | Network elements (KCL/KVL, theorems, transients, AC, 2-port, 3-phase) | A.2 | 14 | Large but very formulaic |
| 7 | Robot applications + CIM (PLC, AMHS, AS/RS, auto-ID, CNC, positioning, concurrent design) | A.3 | 10 | Theory-heavy; read Groover chapters |
| 8 | Sensors + actuators (DC/stepper/servo, hydraulic/pneumatic) | A.2 | 12 | Use IN PYQs |
| 9 | Engineering mechanics (FBD, friction, belts, trusses, plane rigid-body dynamics) | A.2 | 8 | Use ME/CE PYQs |
| 10 | Analog circuits + embedded (filters, op-amps, ADC/DAC, microcontrollers, interrupts) | B1.1 | 12 | |
| 11 | Digital circuits (Boolean, MUX/encoders/decoders, flip-flops, counters) | A.2 | 6 | |
| 12 | Numerical methods | A.1 | 5 | Short, predictable |
| 13 | Python + data structures | A.2 | 3 | You already know these. Just practice tracing code output |
| — | General Aptitude | GA | ongoing | 1 set every Sunday + Wednesday night |

Saturday of each week: a **timed topic test** on that week's subjects (30-40 PYQs), then log every mistake.

**Checkpoint Dec 22:** every row in the syllabus tracker has "Learned ✅". Anything not done gets the
Dec 23-29 week as overflow; don't let it eat into revision.

### Phase 2: Revision + tests (Dec 23 – Jan 12, 3 weeks)

- Revision round 1 of every subject, using your own notes + **formula sheets** ([formula_sheets/](formula_sheets/))
- 1 full-length mock every **Saturday** (8:00–11:00 equivalent slot); analysis on Sunday
- Weekday nights: mixed PYQs from your weakest 3 subjects (see the mistake log)

### Phase 3: Mock phase (Jan 13 – Feb 2, 3 weeks)

- **2-3 full mocks a week.** A full mock fits your 8:00–11:00 morning, then analyse it the next morning
- Revision round 2: formula sheets + mistake log only, no new material
- AI plan **paused** (10-min commit of GATE notes keeps the streak)

### Phase 4: Final week → exam (Feb 3 → your exam day)

- 1-2 mocks **at your actual exam session time** (GATE sessions are typically 9:30–12:30 or 14:30–17:30)
- Formula sheets + mistake log only; sleep on a fixed schedule
- 📅 **Take leave from work for your exam day.** An afternoon session clashes with your 12–9 shift.
  Apply for it as soon as the admit card shows your date/session.

---

## Tracking files

- [syllabus_tracker.md](syllabus_tracker.md): every official topic × Learned / Rev 1 / Rev 2 / PYQs
- [mistake_log.md](mistake_log.md): every wrong or guessed question goes here. This is your #1 revision tool in January
- [mock_scores.md](mock_scores.md): score, section-wise, attempt rate, accuracy per mock
- [formula_sheets/](formula_sheets/): one-page sheet per subject, written by you

Commit these daily. They keep your GitHub streak alive during GATE mode.

## After the exam

Return to the AI × Cybersecurity × Agent Marketplace plan at full pace, from v2 Day 9 (see [../progress_tracker.md](../progress_tracker.md)).
