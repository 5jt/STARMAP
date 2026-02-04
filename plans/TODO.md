# TODO

## Active tasks

### Star table reconstruction
- [ ] Create GitHub issue for star table work
- [ ] Download Yale Bright Star Catalog (BSC5) from Harvard/CfA
- [ ] Analyse catalog format and identify required fields
- [ ] Extract the 332 stars by Yale catalog number (column 3 of existing table)
- [ ] Verify/calculate J2000 coordinates
- [ ] Format output to match book table structure
- [ ] Replace incomplete table in `book/markdown/starmap.md`
- [ ] Verify against original where data exists

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

### 2026-02-04
- Read project files and CLAUDE.md standing instructions
- Discussed star table reconstruction approach
- Decision: derive from Yale BSC5 catalog (original source)
- Key decisions documented:
  - Use J2000 epoch
  - Preserve original 332-star selection
  - Use APL high minus (¯) notation
- Created `plans/` folder with PLAN.md and TODO.md
- Next: create GitHub issue, begin catalog extraction
