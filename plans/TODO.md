# TODO

## Active tasks

- Housekeeping after merge of PR #3 (#10)

## Up next

- Book phase 1: complete Typst rendering of existing content (#4)
- Book phases 2-3: audit code listings and apply Dyalog code (#5)
- Star catalogue errata: stars 205, 244, 320 (#6)
- Constellation stick figures matched to the 332-star catalogue (#7, after #6)
- Document UTC input convention in ENTRY (#8)
- Tighten Sun tolerance in TEST_POSITIONS (#9; test change, needs approval)
- Book bugs replicated in the modern version, to fix after modernisation: CometSolve stops when any element converges (#19); PRINTED shows the observation's weekday, not the print date's (#22); ANIMATEDSVG ignores HIRES (#26)
- Continue proofreading transcribed book text

## Blocked

None currently.

## Completed

- **Modernisation for Dyalog APL 21** (see `plans/PLAN-MODERN.md`): the modern version in `Starmap/`, linked as `#.Starmap`, reproduces the book version's results exactly, bugs included
  - Stages 1-6 (#12, #13, #14, #15, #24, #16; PRs #17, #18, #20, #21, #23, #25, #27)

- **Dyalog implementation, web UI and book rendering** (PR #3, Neil Kirsopp, merged 2026-10-08)
  - Recorded in the session log entries 2026-02-23 to 2026-03-23 below and in `CHANGES.md`; branch names in those entries refer to the fork

- **Restore book-faithful APL architecture** (branch `restore-book-architecture`)
  - 11 selector functions: removed `:If`/`:Else` rank guards, restored `Z←ORB[;N]` one-liners
  - EARTHVIEW: removed `⍣` power-operator rank guard, callers now pass matrices
  - SKYPOS: restored book's `⍉(⌽⍴GQ)⍴NORM` normalization idiom (replaces `∘.×` outer product)
  - CALCULATESTARS: restored `10` placeholders, `STARDATA` local (Dyalog scoping prevents shadowing `STARS` niladic function)
  - CALCULATEPLANETS: restored `(3≠⍳9)⌿planets` boolean mask, `10` placeholders, `1 3⍴0 0 0` matrix for sun, kept `PLANETAA`
  - Dyalog constraints: `⌿` instead of `IF` for matrix compression (book's `/` via `IF` doesn't work on N×2 matrices in Dyalog); `STARDATA`/`MN`/`SN`/`KO` variable names (can't shadow niladic functions)
  - Fixed COMETPOS: ensure always-matrix output for EARTHVIEW (prevented RANK ERROR for live comet dates Oct 1973–Apr 1974)
  - Fixed PLANETSPOS: `planets[,P;]` ensures matrix ORB for scalar planet index
  - New TEST_SKYPOS: 9 bright stars + Sun alt/az, visibility count (0.005 deg max error)
  - New TEST_PIPELINE: CALCULATESTARS + CALCULATEPLANETS end-to-end shapes and values
  - All 7 tests pass, visual render matches EXAMPLE_RENDER.png reference

- **Planet epoch fix** (branch `fix-sky-coordinates`)
  - Fixed ANOMALYDATE inconsistency in `planets.aplf`: column 10 changed from JD 2443600.5 to JD 2441720.5
  - After fix: planet RA/Dec matches JPL Horizons to 1–7 minutes
  - Documented as bug #12 in `docs/calculation-fixes.md`

- **Sky position fix** (branch `fix-sky-coordinates`)
  - Root-caused the "all objects in top-right quadrant" bug to two transcription errors
  - JNU.aplf: `B←2-A+⌊A÷4` → `B←(2-A)+⌊A÷4` (APL precedence)
  - SKYPOS.aplf: `S←×GQ[;3]` → `S←-×GQ[;3]` (azimuth sign)
  - Added TEST_JNU with 5 reference Julian day numbers
  - Created `docs/calculation-fixes.md`

- **Terminal rendering** (branch `terminal-rendering`)
  - New utilities: JNUINV, DAYNAME with tests
  - 5 output functions: CAPTION, REPORTPLANETS, PLOTSTARS, REPORTSTARS, PRINTED
  - Full pipeline end-to-end at ⎕PW=80 and ⎕PW=120

- **Star table reconstruction** (issue #1, PR #2 merged)
  - Re-derived 332 rows from Yale BSC5 catalog
  - Documented in `docs/star-table-reconstruction.md`

- Initial transcription of book to Markdown
- Extraction of figures from page images
- Inclusion of "Expository Programming" article
- Manual proofread of expository programming article

---

## Session log

### 2026-10-11 to 2026-10-12 (modernisation stages 1-6)
- Agreed the modernisation plan (`plans/PLAN-MODERN.md`, PR #17): book version stays in `APLSource/` as `#.sm`; modern version in `Starmap/` as `#.Starmap`, sharing data tables through `Data`; tests first, one issue and branch per stage
- Stage 1 (#12): test runner `test/run.apls` and its tests `test/test_run.sh`
- Stage 2 (#13): orbital selectors take the element table as argument; `→` loops and guards replaced
- Stage 3 (#14): `SkyAt` returns a sky namespace, replacing ENTRY, CALCULATEPLANETS and CALCULATESTARS
- Stage 4 (#15): terminal output functions return lines from the sky namespace
- Rulings of 2026-10-12: all code in scope, including Neil Kirsopp's additions; tradfns become dfns with bicameral names; immutable constants become upper-case variables set by `Initialise`
- Stage 5 (#24): dfns and bicameral names throughout
- Stage 6 (#16): SVG, animation and web, PR #27; `TestStyle` now ignores string literals, as approved
- Found inside dfns in Dyalog 21: an embedded assignment after a function call (`x←F t←⍵`) and a strand of indexed names (`a[;1]b[;2]`) do not behave as in tradfns; such lines are split
- Opened issues #19, #22 and #26 for book bugs the modern version replicates
- Stage 6 merged (PR #27); README notes the video dependencies (`rsvg-convert`, `ffmpeg`)
- Drafted a one-page summary of the modernisation for the Dyalog user meeting, as a Claude Doc ("Reviving STARMAP with Claude")

### 2026-10-11 (post-merge housekeeping)
- Pulled PR #3 (Neil Kirsopp's fork) into main
- Ran all 12 `TEST_*` functions in Dyalog 21.0: all pass
- Opened issues #4-#10 for the open items from the fork's TODO
- Branch `10-housekeeping-after-merge-of-3`: README status section replaces the fork note; TODO restated in terms of issues; removed duplicate root `starmap-animation-demo.mp4`

### 2026-03-23 (constellation data rebuild)
- Switched constellation source from dcf21 to Stellarium modern_iau (CC BY-SA 4.0)
- Rewrote `scripts/rebuild_constellations.py`: deterministic HR→HIP matching via VizieR IV/27A (was angular distance guessing)
- Added 3 known HR→HIP overrides for stars missing from IV/27A: Castor (HR 2890), ε Boo (HR 5506), ζ UMi (HR 5909)
- Fixed TEST_CONSTELLATIONS: added XBOUND exception list for cross-boundary links, fixed `∊` operator bug (needed `⊂`)
- All 8 tests pass
- Discovered 3 new star catalog errata (bugs 18-20 in docs/calculation-fixes.md):
  - Star 205: book says δ Lyr (HR 7141) but HR 7141 = θ¹ Ser at Dec +4° (not δ Lyr at Dec +37°). Coordinates correct, Bayer designation wrong.
  - Star 244: book says γ Per but position (Dec -43°) is γ Phe. Typo PER→PHE.
  - Star 320: book says ζ UMi (HR 5909) at Dec +17°, mag 6.36. Real ζ UMi is Dec +78°, mag 4.3. Position garbled.
- Coverage analysis: our 332-star catalog covers only 36% of Stellarium's 843 segments (310/745 HIP IDs matched)
  - 50 constellations have at least one segment, but most are incomplete
  - Only 4 constellations at 100% with Stellarium (Cas, CMi, Tri, UMi); 6 with dcf21 simplified (adds Car, Leo)
  - Root cause: external stick figure sources use many fainter stars not in our catalog
- Tried filtering to only complete Ptolemaic constellations — too aggressive (6 constellations)
- Reverted to full 50-constellation Stellarium data (no wrong lines, just incomplete figures)
- Open question: the book's 332 stars were chosen to "complete the outline of certain constellations" — we need stick figures designed for our catalog, not generic modern ones
- Created comparison tools: `scripts/compare_constellations.py` (HTML page with In-The-Sky.org reference images), `scripts/verify_constellations.py` (4-page SVG plots)
- Downloaded reference data: `scripts/stellarium_modern_iau.json`, `scripts/dcf21_simplified.dat`, `scripts/dcf21_iau.dat`

### 2026-03-22 (book modernisation — Typst setup)
- Created `plans/PLAN-BOOK.md` — plan for re-rendering the book with updated code
- Goal: same book, new Dyalog v20 code, A5 PDF via Typst, faithful to original layout
- Principle: render existing content first, then update code
- Created `book/typst/` project structure:
  - `template.typ` — A5 page layout, Courier body, APL385 code, underlined headings, justified text
  - `starmap.typ` — full document converted from `starmap.md` to Typst markup
  - `star-table.txt` — extracted 332-row star catalog for inclusion
- Template features:
  - `#apl-block` wrapper for APL code (APL385 Unicode font)
  - `#data-table` wrapper for orbital element tables (Courier 5pt)
  - `#param` helper for parameter definitions (hanging indent)
  - `#indent` helper for paragraph breaks
  - Figures with sans-serif italic captions, inline placement
  - Two-column grid layout for selector function pairs
- First render: ~38 pages, all body text, code blocks, 10 figures, all data tables, full star catalog
- Data table font fix: global `show raw` rule handles layout only; `apl-block` and `data-table` set fonts via scoped `#set text` to avoid conflicts
- Known issues remaining: Table 1 missing, figure numbering out of sequence, page breaks untuned

### 2026-03-18 (hover tooltips + constellation lines)
- Reworked star/planet tooltips from click to hover (mouseover/mouseout)
- Removed invisible hit circles (sh*/ph*), added transparent stroke for hover targets
- Added constellation stick figure display on hover (single `<path>` behind stars)
- Only shows lines when hovered star is in the stick figure (not just in the constellation region)
- Rebuilt CONSTELLATIONS.aplf from IAU reference data (dcf21/constellation-stick-figures)
  - Matched HIP numbers → RA/Dec via VizieR → nearest star in our 332-star catalog
  - 50 constellations (was 51 hand-crafted), cross-constellation links preserved (Aur/Tau, Car/Vel, Pup/Car)
  - Removed hand-crafted errors (Draco head used wrong star, Aquila had crossing lines)
- Replaced CL flat array with CG grouped object in JS (constellation abbreviation → pairs)
- Found STARS catalog errors: dLyr(205) Dec=4.2° (should ~37°), zUMi(320) Dec=17.4° (should ~78°)
- Verification script: scripts/verify_constellations.py generates per-constellation plots

### 2026-03-17 session 2 (animated SVG polish + web UI)
- Bright star table: 2-column layout (11 rows each), below-horizon rows dimmed (#555) not hidden
- Planet table: below-horizon rows dimmed (same pattern as bright stars)
- Replaced foreignObject controls with pure SVG elements (foreignObject + viewBox scaling = broken mouse mapping)
  - SVG scrub bar: rect track + fill + circle thumb, click-to-seek and drag via `getScreenCTM().inverse()`
  - SVG speed buttons: rect+text groups
  - Two-line layout: scrub bar on top, speed controls + date label below
- Added OPTS left arg: `FPS [HIRES [SKIP]]` — frame skipping (every Nth day), display size
- Removed explicit SVG width/height (responsive viewBox)
- WebApp: added `/api/generate-svg` POST + `/api/svg/{id}` GET endpoints
- Web UI: two buttons (Generate SVG / Generate .mp4), checkboxes for large display and every-other-day
- iframe embedding for SVG output, auto-sizing via viewBox aspect ratio
- All 9 tests pass

### 2026-03-17 session 1 (animated SVG)
- Branch `animate`
- Created ANIMATEDSVG.aplf: JS-animated SVG generator
  - Stars computed client-side (ported PRECESS/SKYPOS/PROJECTION to JS)
  - Planet data pre-computed in APL, embedded as JSON
  - `FJS` helper formats APL numbers for JS (replaces `¯` with `-` at source)
  - `hm()` JS function displays `¯` for negative numbers in tables
- Created TEST_ANIMATEDSVG.aplf (passes)
- Bumped frame padding from 4 to 5 digits (supports 99,999 frames)
- Parallelised rsvg-convert in MAKEVIDEO via `xargs -P 8`
- All 9 tests pass

### 2026-03-02 (CHANGES.md audit)
- Audited CHANGES.md against actual source files, found and corrected several discrepancies
- Fixed: EARTHVIEW entry (⍣ guard was removed, not present), SKYPOS normalization idiom, azimuth formula details, CALCULATEPLANETS Earth exclusion method, PLOTSTARS symbols (Unicode not ASCII), PLANETNAMES count (11 not 12), STARNAMES count (332 not 50)
- Added 7 previously undocumented fixes: LATROTATE (⊖⊖→⌽⊖), PRECESS (sign + reverse), MOONPOS (negation), planets.aplf (epoch date), moon.aplf (decimal places), COMETPOS (matrix reshape), PLANETSPOS (scalar index)
- Added 11 selector function rank-guard removal, all new/rewritten files, complete file tables
- Updated TODO.md: moved stale "this session" items to "previously completed"
- Branch: `hacks`

### 2026-02-26 (restore book architecture)
- Created branch `restore-book-architecture` from `fix-sky-coordinates`
- Removed `:If`/`:Else` rank guards from 11 selector functions (ANOMALY, ANOMALYDATE, ASCENDING, ECCENTRICITY, EPOCHDATE, INCLINATION, PERIANGLE, PERIDIST, PERIOD, SECULAR, SEMIMAJOR)
- Removed `⍣` rank guard from EARTHVIEW, updated callers to pass matrices
- Restored book's `⍉(⌽⍴GQ)⍴NORM` normalization idiom in SKYPOS
- Restructured CALCULATESTARS and CALCULATEPLANETS: `10` placeholders, `(3≠⍳9)⌿planets`, restored globals comments
- Fixed COMETPOS to always return matrix (prevented latent RANK ERROR for comet-active dates)
- Fixed PLANETSPOS `planets[,P;]` for scalar planet index
- Updated TEST_POSITIONS to pass `1 3⍴0 0 0` to EARTHVIEW
- New TEST_SKYPOS: alt/az validation for 9 bright stars + Sun
- New TEST_PIPELINE: end-to-end CALCULATESTARS + CALCULATEPLANETS validation
- Thorough review: verified TEST_POSITIONS JPL reference data is correct (date, precession, angular error formula, frame consistency, reference generation script)
- All 7 tests pass, visual render matches EXAMPLE_RENDER.png
- Files changed: 16 modified, 2 new tests
- Branch: `restore-book-architecture`

### 2026-02-25 (planet epoch fix)
- Fixed ANOMALYDATE inconsistency: planets.aplf column 10 changed from JD 2443600.5 to JD 2441720.5
- ANOMALY values were for ~1973 epoch, DATE_ASC claimed 1978 — all planet positions wrong by large amounts
- Added bug #12 to docs/calculation-fixes.md with impact analysis and JPL Horizons validation
- Updated Anaheim validation section to reference planet RA/Dec comparison
- Branch: `fix-sky-coordinates`

### 2026-02-25 (sky position fix)
- Root-caused the "all objects in top-right quadrant" bug using Python numerical verification against JPL Horizons
- Identified two transcription errors: JNU Gregorian correction (APL precedence) and SKYPOS azimuth sign
- Fixed JNU.aplf, SKYPOS.aplf, simplified JNUINV.aplf
- Added TEST_JNU.aplf (5 reference Julian day numbers)
- Created `docs/calculation-fixes.md` — comprehensive calculation bug report (11 bugs total)
- Updated CHANGES.md, TODO.md
- Branch: `fix-sky-coordinates` from `terminal-rendering`

### 2026-02-23 (session 2 — terminal rendering)
- Created branch `terminal-rendering` from `hacks`
- Wrote and tested JNUINV and DAYNAME utility functions
- Rewrote all 5 output functions (CAPTION, REPORTPLANETS, PLOTSTARS, REPORTSTARS, PRINTED) to match EXAMPLE_RENDER.png layout
- Added `PLANETAA←AA` to CALCULATEPLANETS (one line, preserves uncompressed alt/az)
- Fixed STARNAMES `⊂` bug, PLANETNAMES length mismatch, various APL precedence issues
- Full pipeline works at ⎕PW=80 and ⎕PW=120
- Identified critical bug: all sky objects cluster in top-right quadrant (upstream of rendering)
- Files changed: CALCULATEPLANETS, CAPTION, DAYNAME (new), JNUINV (new), PLOTSTARS, PRINTED, REPORTPLANETS, REPORTSTARS, STARNAMES, TEST_DAYNAME (new), TEST_JNUINV (new)

### 2026-02-23 (session 1)
- Fixed moon duplication bug in CALCULATEPLANETS: book's `1 0⌽PLANETS` was misread `1 0↓PLANETS`
- Fixed off-by-one planet labelling (consequence of moon duplication)
- Removed spurious Earth from planet computation (row 3 of `planets` excluded from `PLANETPOS` call)
- Replaced ASCII planet symbols with Unicode astronomical symbols (☾☉☿♀♂♃♄⛢♆♇☄)
- Updated PLANETNAMES to remove Earth
- Updated CHANGES.md section 6

### 2026-02-05
- Completed star table reconstruction from BSC5 catalog
- Created extraction script `yale-catalog/extract_stars.py`
- Compared BSC5 values against test rows from printed book
- Decision: use BSC5 values (current authoritative source)
- Discrepancies documented in `docs/star-table-reconstruction.md`
- Replaced table in `book/markdown/starmap.md` (332 rows)
- Fixed Pleiades row formatting, parallax column alignment
- Created PR #2, merged to main
- Issue #1 closed

### 2026-02-04
- Read project files and CLAUDE.md standing instructions
- Discussed star table reconstruction approach
- Decision: derive from Yale BSC5 catalog (original source)
- Key decisions documented:
  - Use J2000 epoch
  - Preserve original 332-star selection
  - Use APL high minus (¯) notation
- Created `plans/` folder with PLAN.md and TODO.md
- Created GitHub issue #1 for star table work
- Downloaded BSC5 catalog from Harvard/CfA
