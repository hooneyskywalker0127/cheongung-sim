# Business Requirements Document

**Project Name:** Cheongung Sim  
**Date:** 2026-04-04  
**Version:** 0.1  

---

## 1. Background

During the 2026 US-Iran War, Cheongung-II (KM-SAM II) deployed in the UAE achieved a 96% intercept rate against ballistic missiles and 100% against cruise missiles in real combat. This validated the operational value of Korea's indigenous air defense system and highlighted the growing need for simulation research in complex multi-threat environments.

This project aims to implement an intercept simulation based on Cheongung-II's actual engagement logic, covering complex threat environments including ballistic missiles, cruise missiles, and drones.

---

## 2. Objectives

- Implement Cheongung-II's 3-phase guidance system (INS → Command Guidance → Active Radar Homing) in simulation
- Implement threat prioritization and multi-target simultaneous engagement logic in a mixed-threat environment
- Derive defense efficiency metrics such as intercept success rate and remaining missile count

---

## 3. Scope

**Phase 1 (This Document)**
- 2D top-view simulation
- Threat types: Ballistic missiles, cruise missiles, drones (mixed)
- Friendly assets: 1 Cheongung-II battery
- Defense target: 1 key facility (e.g., air base)

**Phase 2 and Beyond (TBD)**
- Multi-battery cooperative engagement
- 3D simulation expansion
- Reinforcement learning-based autonomous engagement decision

---

## 4. Functional Requirements

### 4.1 Threat Generation
- Ballistic missile: High speed (up to Mach 5), high altitude, parabolic trajectory
- Cruise missile: Medium speed, low altitude, horizontal flight
- Drone: Low speed, very low altitude, irregular maneuvering
- Multiple threats can be launched simultaneously or sequentially

### 4.2 Radar Detection
- Detect threats within radar range
- Threats outside detection range cannot be engaged
- Differentiated detection difficulty by threat type (drones harder to detect)

### 4.3 Threat Prioritization (Engagement Control)
- Evaluation criteria: speed, altitude, remaining distance to defense target
- Score-based ranking; highest-priority threats assigned intercept missiles first
- Only engage targets within the Engagement Window

### 4.4 Intercept Missile Guidance (3 Phases)
- **Initial (INS):** Inertial navigation after launch
- **Mid-course (Command Guidance):** Radar tracks both missile and target simultaneously, sends guidance commands
- **Terminal (Active Radar Homing):** Missile's onboard radar tracks and directly hits the target

### 4.5 Intercept Judgment
- Hit-to-Kill method (direct collision)
- Intercept success when distance falls below threshold
- If intercept fails, threat reaches the defense target

### 4.6 Metrics Collection
- Intercept success rate (by threat type)
- Number of intercept missiles expended
- Number of hits on defense target
- Engagement duration

### 4.7 Visualization
- **pygame:** Real-time 2D simulation (threat trajectories, missile paths, collision events)
- **matplotlib:** Post-simulation metrics graphs

---

## 5. Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python |
| Real-time visualization | pygame |
| Result graphs | matplotlib |
| Physics calculation | numpy |
| Data storage | CSV / JSON |

---

## 6. Success Criteria

- Priority-based engagement works correctly in a scenario with all 3 threat types launched simultaneously
- 3-phase guidance logic is implemented so the missile behaves differently in each phase
- Real-time simulation is visually verifiable via pygame
- Metrics graph is output after simulation ends

---

## 7. Constraints

- Solo development, 2-week completion target
- No classified military data (based on public information only)
- No 3D rendering (2D only)
