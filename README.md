# Cheongung-II Air Defense Simulation

A real-time 2D intercept simulation based on the KM-SAM II (Cheongung-II) air defense system — inspired by its combat deployment during the 2026 US-Iran conflict in the UAE.

---

## Background

In 2026, Cheongung-II batteries deployed in the UAE achieved **96% intercept rate against ballistic missiles** and **100% against cruise missiles** in actual combat. This project simulates the core engagement logic behind that system.

---

## Demo

- Intro screen → press SPACE to start
- Real-time simulation: threats spawn from 3 directions, interceptor missiles launch from the KM-SAM II battery
- Ends after 60 seconds or when base HP reaches 0
- Results graph displayed after simulation

---

## Features

### Threat System
| Type | Color | Behavior |
|------|-------|----------|
| Ballistic Missile (BM) | Red | Parabolic trajectory, gravity applied, high speed |
| Cruise Missile (CM) | Orange | Horizontal straight flight, constant altitude |
| Drone (DR) | Yellow | Irregular maneuvering, random velocity changes |

- 3-directional spawn: right / top / bottom
- Individual spawn every 4 seconds
- **Saturation attack** every 15 seconds (5–8 threats simultaneously)

### Engagement System
- **3-phase guidance:** INS → Command Guidance → Active Radar Homing (phase transitions by distance)
- **Trajectory prediction filter:** Only engage threats predicted to reach base within 5 seconds
- Fire interval: 0.8s — max 5 simultaneous engagements
- **Reload system:** Auto-reload 4 rounds every 10 seconds (max 20)

### Visualization
- Grid background + radar detection range circle
- Per-threat trail trails and BM/CM/DR labels
- Explosion effect on intercept success
- Military HUD: AMMO / IN FLIGHT / RELOAD timer / threat counts / BASE HP bar
- AMMO LOW warning when ≤5 rounds remain

---

## Tech Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| Language | Python | Fast development, rich ecosystem |
| Real-time rendering | pygame | Frame-by-frame simulation loop |
| Result graphs | matplotlib | Post-simulation metrics |
| Physics / math | numpy | Efficient vector operations |
| Data storage | CSV | Simple metrics export |

---

## Project Structure

```
cheongung-sim/
├── src/
│   ├── main.py          # Entry point, game loop
│   ├── threat.py        # BallisticMissile / CruiseMissile / Drone
│   ├── radar.py         # Detection range + probability
│   ├── engagement.py    # Priority scoring + trajectory filter + fire control
│   ├── missile.py       # 3-phase guidance (INS → Command → ARH)
│   ├── judgement.py     # Hit-to-Kill collision detection
│   ├── metrics.py       # Success/fail counters + CSV export
│   └── visualizer.py    # pygame rendering + HUD + intro + ResultGraph
├── docs/
│   ├── BR_ko.md / BR_en.md
│   ├── ARCHITECTURE_ko.md / ARCHITECTURE_en.md
│   └── SCHEDULE.md
├── results/             # metrics.csv saved here
└── requirements.txt
```

---

## How to Run

```bash
pip install -r requirements.txt
python3 src/main.py
```

---

## Portfolio Context

This project is part of a defense AI portfolio targeting MUM-T (Manned-Unmanned Teaming) roles at Korean defense companies (LIG Nex1, Hanwha).

Progression:
1. **cheongung-sim** ← this project
2. Mountain search (ground + aerial drone cooperation)
3. korea-combat-sim (BT vs RL combat simulation — main project)

---

## References

- Cheongung-II (KM-SAM II): [나무위키](https://namu.wiki/w/%EC%B2%9C%EA%B6%81-II)
- 2026 UAE combat data: 96% ballistic / 100% cruise intercept rate
- Guidance system: INS → Command Guidance → Active Radar Homing (Hit-to-Kill)
