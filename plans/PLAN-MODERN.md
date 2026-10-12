# Modernisation plan

Rewrite STARMAP in idiomatic Dyalog APL 21 alongside the book-faithful version.

## Decisions (agreed 2026-10-11)

1. **Two versions.** `APLSource/` stays the book version, linked as `#.sm`; it remains the reference for the book audit (#5). The modern version lives in `Starmap/`, linked as `#.Starmap`. Both use the same data tables.
2. **Naming.** A function is *revised* if its signature or behaviour changes, and then takes a bicameral name (`SkyPos`, `PlanetPositions`). New functions also take bicameral names. A function whose body is only restructured (for example `→` replaced by `:While`) keeps its name. *Superseded 2026-10-12: see decision 8.*
3. **Tests.** The existing `TEST_*` functions stay unchanged and test the book version. The modern version gets its own tests, written first and reviewed before implementation, and checked against the same JPL reference positions. Where possible, modern results are also checked for equality with the book version for the same inputs.
4. **No globals for data flow.** Values pass as arguments and results. One top-level function takes date, time, latitude and longitude and returns a namespace holding stars, planets and moon phase. The output functions take that namespace as an argument.
5. **Dyalog 20/21 features** (array notation in `.apla` files, newer operators) are used where they make the code clearer, not for their own sake.
6. **One issue and one branch per stage**, tests first, with a pause for review.

## Decisions (revised 2026-10-12)

7. **Scope.** All the code in `APLSource/` is in scope: the book's functions as corrected by Neil Kirsopp, and the functions he added (output, SVG, animation, web). The modern version must reproduce the book version's results exactly, bugs included; bugs are raised as issues and fixed later.
8. **Dfns by default, bicameral names throughout.** The modern version demonstrates a modernised STARMAP, not a minimal edit of it. Every function becomes a dfn with a bicameral name (`LATROTATE` becomes `LatRotate`), keeping the book's abbreviations. Nothing is copied unchanged.
9. **Tradfns** remain only for niladic functions that are not constants: the input prompts (`GetDate`, `GetTime`, `GetLat`, `GetLong`), `Entry`, `Display`, `ExampleRender`, `Initialise`, and in stage 6 `ExampleSvg`, `STARTSERV` (loops for ever) and `MakeVideo`. The `WebApp` class stays a class.
10. **Constants.** A niladic function that returns an immutable constant becomes a variable named in upper case (`PI←○1`, `EARTH`), set by one niladic function, `Initialise`, which is run after `Data` is set (by the test runner, or by hand after linking). Data tables stay in the book namespace, reached through `Data`.
11. **Size.** No modern function exceeds 100 lines.

## Current state

- 114 source files in `APLSource/`; 12 test functions, all passing in Dyalog 21.0.
- `→` branches in 10 functions. Three are loops: `COMETSOLVE`, `KEPLINVERSE` and `PLANETSPOS`. The rest are guards or early exits.
- Data flows through globals at three levels:
  - **Orbital-element selectors** (`ANOMALY`, `ECCENTRICITY`, `PERIOD` …) are niladic and read `ORB` from their caller's scope (dynamic scoping).
  - **`ENTRY`** sets `LAT`, `LONG`, `DATE` and `TIME`.
  - **`CALCULATESTARS` and `CALCULATEPLANETS`** set `VE`, `BRIGHTVIS`, `AAE`, `STARCOORD`, `PLANETS`, `VP`, `PLANETCOORD`, `PLANETAA` and `PHASE`. The output functions (`CAPTION`, `REPORTPLANETS`, `PLOTSTARS`, `REPORTSTARS`, `PRINTED`, `PLOTSVG`, `ANIMATE`, `ANIMATEDSVG`, `WebApp`) read these.

## Stages

### Stage 1 (#12): layout, loading and test runner

- Create `Starmap/`, linked as `#.Starmap`, with a way to reach the shared data tables from the book version.
- Add a test runner script under `test/` that loads both versions and runs every `TEST_*` function in each, reporting pass or fail. It replaces ad hoc loading. It must work in Dyalog script mode without the session Link: load functions with `⎕FIX` and arrays from `.apla`.
- Document how to load and test both versions in the README.
- Tests: the runner reports the 12 existing book tests as passing; a modern smoke test confirms the modern namespace loads and can see the data tables.

### Stage 2 (#13): core calculations

- Remove dynamic scoping of `ORB`: orbital-element selectors take the element table as an argument. This changes their signatures, so they get bicameral names. Alternatively, replace them with named column indices; decide while writing the tests.
- Rewrite the `→` loops: `KEPLINVERSE` and `COMETSOLVE` (Newton iteration: `⍣` with a convergence test, or `:Until`) and `PLANETSPOS` (an each or rank over dates).
- Replace the remaining `→` guards with control structures or guarded results.
- `SKYPOS`: unpack the observer as an argument structure rather than reusing global-looking names.
- Tests: each revised function is compared with its book counterpart over the inputs the book tests use, plus edge cases (scalar planet index, comet dates inside and outside the 100-day window).

### Stage 3 (#14): calculation drivers

- Replace `ENTRY`, `CALCULATESTARS` and `CALCULATEPLANETS` with one function, for example `Sky←SkyAt date time lat long`, returning a namespace: star alt/az, visibility, bright-star subset, projected coordinates, planet positions, moon phase.
- Keep prompting for input separate from calculation: a `Prompt` function returns the four inputs.
- Tests: the namespace's members equal the book globals for the Anaheim 1974-05-16 05:00 UTC observation, and agree with `reference_positions` to the existing tolerances.

### Stage 4 (#15): terminal output

- `CAPTION`, `REPORTPLANETS`, `PLOTSTARS`, `REPORTSTARS` and `PRINTED` take the sky namespace and return character matrices instead of printing. A display function prints them in order, replacing `WORK` and `DISPLAY`.
- Tests: output is character-for-character identical to the book version's for the Anaheim observation at `⎕PW` 80 and 120.

### Stage 5 (#24): dfns and bicameral names throughout

- Convert every function from stages 2–4 to a dfn with a bicameral name (decisions 8–11). Loops become guarded tail recursion where `⍣` would change the number of iterations, so `KeplInverse` and `CometSolve` stop exactly where the book's do.
- Tests: the existing modern tests call the new names; `TestConverted` compares each function converted without other change with its book counterpart; `TestInventory` holds the name table and checks that every function is a dfn except the agreed tradfns, that the constants are upper-case variables, and that there are no other functions; `TestStyle` adds the 100-line limit and upper-case constants.

### Stage 6 (#16): SVG, animation and web

- `PLOTSVG`, `FRAMESVG`, `SAVESVG`, `EXAMPLE_SVG`, `ANIMATE`, `ANIMATEDSVG`, `STARTSERV`, `MAKEVIDEO` and `WebApp` take the sky namespace or explicit arguments, following the stage 5 conventions. Large functions (`ANIMATEDSVG`, 642 lines; `PLOTSVG`, 226 lines) are split into smaller single-purpose functions.
- Tests: SVG output, animation frames and animated SVG are identical to the book version's for the same inputs, and no globals are set.

## Issues

1. #12 Stage 1: layout, loading and test runner
2. #13 Stage 2: core calculations without globals or branches
3. #14 Stage 3: single calculation function returning a sky namespace
4. #15 Stage 4: terminal output from the sky namespace
5. #24 Stage 5: dfns and bicameral names throughout
6. #16 Stage 6: SVG, animation and web from the sky namespace
