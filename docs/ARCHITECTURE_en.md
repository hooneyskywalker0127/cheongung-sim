# System Architecture

**Project Name:** Cheongung Sim  
**Date:** 2026-04-04 | **Last Updated:** 2026-04-12  
**Version:** 1.0 (Complete)

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
  - Distance to base (closer = higher score)
- **Engagement filter:**
  - Minimum speed threshold 25 (skips stationary threats)
  - 5-second trajectory prediction — only engage threats predicted to enter 150px of base
- Fire interval: 0.8 seconds (prevents burst firing)
- Max simultaneous engagements: 5
- Manages remaining intercept missiles (initial 20, auto-reload 4 every 10 seconds)

### InterceptMissile
Tracks the target using a 3-phase guidance system.

| Phase | Guidance | Behavior |
|-------|----------|----------|
| Phase 1 (INS) | Inertial Navigation | Flies autonomously to predicted target position after launch |
| Phase 2 (Command Guidance) | Radar Command | Radar tracks both missile and target simultaneously, sends correction commands |
| Phase 3 (Active Radar Homing) | Onboard Radar | Missile's own radar directly tracks and hits the target |

- Phase transitions triggered by distance thresholds
- Separate steering logic implemented per phase

#### Phase-by-Phase Detail

**Phase 1 — INS (Inertial Navigation System)**

Immediately after launch, the radar cannot yet track the missile (too close to the battery).
The missile flies using only its internal sensors — no external signals.

At launch, the predicted position of the threat is calculated based on its current position and velocity.
The missile flies straight toward that predicted point with no course correction until the next phase.

Simulation: Calculate predicted `(x, y)` from threat's position + velocity at launch time → set missile `vx, vy` toward that point.

---

**Phase 2 — Command Guidance**

Once the missile has flown far enough, the ground radar can track it.
The radar simultaneously tracks both the missile and the threat, then transmits correction commands wirelessly to the missile.

Commands like "turn 3 degrees left" or "increase altitude" are sent every frame.
The missile does not make its own decisions — it simply follows ground instructions.

Simulation: Each frame, calculate direction vector from battery (radar) to threat → correct missile `vx, vy`.

---

**Phase 3 — Active Radar Homing (ARH)**

When the missile is close enough to the threat, the missile's own onboard radar takes over.
It detects and tracks the threat directly, with no need for ground commands.
The missile autonomously chases the threat — the most precise phase.

Even if the threat maneuvers, the missile adjusts in real time.

Simulation: Each frame, look directly at threat's current `(x, y)` → adjust missile `vx, vy`.

---

**Phase Transition (Distance-Based)**

```
Just after launch     → Phase 1: INS            (distance to threat > 700m)
Mid-range             → Phase 2: Command Guid.  (200m < distance ≤ 700m)
Close range           → Phase 3: Active Homing  (distance ≤ 200m)
```

※ Transition distances are adjustable simulation parameters.

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
- **pygame:** Real-time 2D rendering
  - Grid background, radar detection range circle
  - Per-threat color (red/orange/yellow) + trail effect + label (BM/CM/DR)
  - Intercept missiles (blue) + trail
  - Explosion effect (`Explosion` class — ring + fade-out)
  - Base icon + HP bar (green → orange → red)
  - Military HUD: AMMO / IN FLIGHT / RELOAD timer / threat counts / BASE HP
  - AMMO LOW warning (≤5 rounds)
- **Intro screen:** `show_intro()` — mission background text + space to start
- **matplotlib:** Post-simulation metrics graph (dark theme)

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
