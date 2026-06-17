# Research Inbox

Lightweight holding area for ideas that are interesting but should not interrupt
the current GameCodex launch path.

## WorldCupCodex: Football Tactical Shapes

**Status:** parked.

**Why it is interesting**

- World Cups are strong global circulation events: tactical labels and shapes
  become public, named, copied, and debated.
- Football formations are a popular-facing Codex object: `4-4-2`, `4-3-3`,
  `4-2-3-1`, back threes, box midfields, and rest-defense shapes are all
  transmissible tactical signs.
- The topic has timely public attention during the World Cup cycle.

**Why it is hard**

- Formation labels are unstable: a team may defend as `4-4-2`, build as
  `3-2-5`, and press as something else.
- Tactical shape does not determine success. Outcomes are heavily confounded by
  player quality, opponent strength, match state, injuries, red cards,
  finishing variance, and set pieces.
- Orthogonal encoding is much harder than in Go. Time, space, possession,
  pressure, role, and phase of play are entangled.

**Viable framing**

Do not study formations as causes of winning. Study them as public tactical
signs: coarse-grained Codex units that can be named, copied, and re-stabilized.

Possible question:

> How do World Cups change the circulation of football tactical shapes?

**Possible MVP**

- Use StatsBomb open-data World Cup / Euro / Copa data.
- Start with formation labels where available, then test whether event-location
  shape fingerprints tell a cleaner story.
- Build a small interactive page around formation timelines, shape fingerprints,
  and tournament shock/adoption cycles.

**Stop rule**

Do not pursue as a mainline project unless the data supports a stable shape
fingerprint that avoids claiming tactics determine match outcomes.
