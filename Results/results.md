# What the solver produced

## Normal day (99 pallets)

The solver found 4 routes using only the big trucks.
Total distance: 215 km

Truck 1 visited: L04, L01, L08, L06, L05, L10, L20, L19
- Left depot at 07:00
- First store (L04) arrived at 08:00
- Last store (L19) arrived at 11:35
- Back at depot: 12:17
- Carried 32 out of 33 pallets
- Drove 49 km

Truck 2 visited: L11, L18, L21, L23, L24, L25, L22
- Left depot at 07:00
- First store (L11) arrived at 08:00
- Last store (L22) arrived at 11:46
- Back at depot: 12:42
- Carried 26 out of 33 pallets
- Drove 86 km

Truck 3 visited: L17, L14, L16, L12, L13, L15, L07
- Left depot at 07:00
- First store (L17) arrived at 08:00
- Last store (L07) arrived at 11:49
- Back at depot: 12:29
- Carried 29 out of 33 pallets
- Drove 64 km

Truck 4 visited: L03, L09, L02
- Left depot at 07:00
- First store (L03) arrived at 08:00
- Last store (L02) arrived at 09:06
- Back at depot: 09:42
- Carried 12 out of 33 pallets
- Drove 16 km

All 25 stores received their delivery.
All trucks finished before 12:00 (or close to it).

---

## Busy day (150 pallets)

The solver needed 6 trucks this time — 4 big and 2 small.
Total distance: 220 km

Truck 1: L15, L16, L14, L17, L20, L19 — 33/33p — 71 km — 312 min
Truck 2: L05, L06, L07, L04, L03 — 33/33p — 23 km — 240 min
Truck 3: L22, L25, L24, L23, L21 — 28/33p — 64 km — 281 min
Truck 4: L10, L13, L12, L18, L11 — 32/33p — 48 km — 268 min
Small truck 1: L02, L09 — 12/12p — 8 km — 129 min
Small truck 2: L01, L08 — 12/12p — 6 km — 130 min

All 25 stores served. All on time.

---

## Stress test (174 pallets)

The solver could not find a valid solution.

The trucks had enough space (174 pallets vs 180 capacity).
But there was not enough time — the stores need to be 
served between 08:00 and 12:00 and each stop takes longer 
because there are more pallets to unload. Plus the morning 
traffic makes the first legs slower.

The solver confirmed: no valid solution exists under 
these constraints.
