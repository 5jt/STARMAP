# Project plan

## Overview

This project recreates STARMAP, a classic example of expository programming from IBM's APL culture. See README.md for background and goals.

## Phase 1: Republish STARMAP on the web

**Status**: In progress

The source is a printed copy of *STARMAP* by Paul C. Berry & John R. Thorstensen (APL Press, 1978).

### Completed
- Initial transcription of book to Markdown
- Extraction of figures from page images
- Inclusion of Paul Berry's "Expository Programming" article

### In progress
- Proofreading and correcting transcription errors
- **Star table reconstruction** (critical path item)

### Star table issues
The transcribed star table has significant problems:
1. Many transcription errors (minus signs, Greek letters)
2. Rows 251-300 entirely missing data values

**Decision**: Derive the table from the Yale Bright Star Catalog (BSC5), the original source cited in the book. This ensures accuracy and completeness.

### Key decisions
- **Epoch**: J2000 (1 January 2000), as in the published table
- **Selection**: Preserve original 332-star selection by matching Yale catalog numbers
- **APL notation**: Use high minus (¯) for negative values, not low minus (-)
  - In APL: `¯` is part of the number literal; `-` denotes negation/subtraction
  - Example: `-3 4` evaluates to `¯3 ¯4`

## Phase 2: Recreate code in Dyalog APL

**Status**: Not started

## Phase 3: Refactor code in Dyalog APL

**Status**: Not started

## Phase 4: Deploy as API

**Status**: Not started

## Phase 5: HTML front end

**Status**: Not started
