# System Architecture

**Project Name:** Cheongung Sim  
**Date:** 2026-04-04  
**Version:** 0.1  

---

## Overall Structure

```
┌─────────────────────────────────────────────┐
│              ThreatGenerator                │
│  Generate ballistic / cruise / drone threats│
│  and update trajectories each frame         │
└────────────────────┬────────────────────────┘
                     │ threat object list
          ┌──────────▼──────────┐
          │       Radar         │
          │  Detect threats in  │
          │  radar range        │
          │  Difficulty by type │
          └──────────┬──────────┘
                     │ detected threat list
          ┌──────────▼──────────┐
          │  EngagementControl  │
          │  Threat prioritization│
          │  Missile assignment  │
          │  Engagement window   │
          └──────────┬──────────┘
                     │ engagement command
          ┌──────────▼──────────┐
          │   InterceptMissile  │
          │   Phase 1: INS      │
          │   Phase 2: Command  │
          │   Phase 3: ARH      │
          └──────────┬──────────┘
                     │ collision check
          ┌──────────▼──────────┐
          │    HitJudgement     │
          │  Hit-to-Kill check  │
          │  Success / Failure  │
          └──────┬──────────────┘
                 │
       ┌─────────┴──────────┐
       │                    │
┌──────▼──────┐    ┌────────▼────────┐
│   Metrics   │    │   Visualizer    │
│   Logger    │    │  pygame (live)  │
│ CSV / JSON  │    │  matplotlib     │
└─────────────┘    └─────────────────┘
```

---

## Component Descriptions

### ThreatGenerator
Creates threat objects and updates their trajectories each frame.

- **Ballistic missile:** Parabolic trajectory (gravity 9.8 applied), high speed (up to Mach 5), high altitude — x moves + vy decreases
- **Cruise missile:** Horizontal straight flight (constant altitude), medium speed, low altitude — x only
- **Drone:** Irregular maneuvering, low speed, very low altitude — random variation in both x and y
- Loads threat launch time and quantity from scenario file (JSON)

### Radar
Detects threats within detection range and passes them to EngagementControl.

- Detection range based on configuration (referenced from Cheongung-II specs)
- Differentiated detection probability by threat type:
  - Ballistic missile: High
  - Cruise missile: Medium
  - Drone: Low (small size, very low altitude)

### EngagementControl
Evaluates detected threats and decides intercept missile assignment.

- **Priority score calculation:**
  - Speed (faster = higher score)
  - Altitude (lower = higher score — less time to intercept)
  - Remaining distance to defense target (closer = higher score)
- Engagement Window calculation
- Manages remaining intercept missile count

### InterceptMissile
Tracks the target using a 3-phase guidance system.

| Phase | Guidance | Behavior |
|-------|----------|----------|
| Phase 1 (INS) | Inertial Navigation | Flies autonomously to predicted target position after launch |
| Phase 2 (Command Guidance) | Radar Command | Radar tracks both missile and target simultaneously, sends correction commands |
| Phase 3 (Active Radar Homing) | Onboard Radar | Missile's own radar directly tracks and hits the target |

- Phase transitions triggered by distance thresholds
- Separate steering logic implemented per phase

### HitJudgement
Handles collision detection between intercept missiles and threats.

- Distance calculation every frame
- Distance below threshold → intercept success
- Threat enters defense target radius → hit registered

### Metrics Logger
Collects and stores simulation data.

- Intercept success/failure count by threat type
- Number of intercept missiles expended
- Number of hits on defense target
- Saved as CSV / JSON

### Visualizer
- **pygame:** Real-time 2D rendering (threats, intercept missiles, radar range, explosion effects)
- **matplotlib:** Metrics graphs output after simulation ends

---

## Directory Structure

```
cheongung-sim/
├── docs/
│   ├── BR_ko.md
│   ├── BR_en.md
│   ├── ARCHITECTURE_ko.md
│   └── ARCHITECTURE_en.md
├── src/
│   ├── main.py              # Simulation entry point
│   ├── threat.py            # ThreatGenerator
│   ├── radar.py             # Radar
│   ├── engagement.py        # EngagementControl
│   ├── missile.py           # InterceptMissile
│   ├── judgement.py         # HitJudgement
│   ├── metrics.py           # Metrics Logger
│   └── visualizer.py        # Visualizer
├── scenarios/
│   └── default.json         # Default scenario (threat launch config)
├── results/
│   └── (simulation results saved here)
└── requirements.txt
```

---

## Tech Stack Summary

| Component | Technology |
|-----------|-----------|
| Language | Python |
| Real-time visualization | pygame |
| Result graphs | matplotlib |
| Physics calculation | numpy |
| Data storage | CSV / JSON |
