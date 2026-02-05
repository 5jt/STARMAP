# TODO

## Active tasks

### Star table reconstruction
- [x] Create GitHub issue for star table work (#1)
- [x] Download Yale Bright Star Catalog (BSC5) from Harvard/CfA
- [x] Analyse catalog format and identify required fields
- [x] Extract the 332 stars by Yale catalog number
- [x] Verify J2000 coordinates (BSC5 provides J2000 directly)
- [x] Format output to match book table structure
- [x] Replace incomplete table in `book/markdown/starmap.md`
- [x] Document decision to use BSC5 values over book values
- [ ] Create PR for review

## Up next

- Continue proofreading transcribed book text
- Address other transcription errors (code blocks, special characters)

## Blocked

None currently.

## Completed

- Initial transcription of book to Markdown
- Extraction of figures from page images
- Inclusion of "Expository Programming" article
- Manual corrections to star table (partial)
- Manual proofread of expository programming article

---

## Session log

### 2026-02-05
- Completed star table reconstruction from BSC5 catalog
- Created extraction script `yale-catalog/extract_stars.py`
- Compared BSC5 values against test rows from printed book
- Decision: use BSC5 values (current authoritative source)
- Discrepancies documented in `docs/star-table-reconstruction.md`
- Replaced table in `book/markdown/starmap.md` (332 rows)
- Fixed Pleiades row formatting (PLE constellation)
- Next: create PR for review

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
