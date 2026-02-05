# Star table reconstruction

## Background

The star table in `book/markdown/starmap.md` is an appendix to the STARMAP book, listing 332 bright stars with their coordinates, magnitudes, and parallaxes. The original table was prepared by Per Gjerlov of IBM Denmark using data from the Yale Catalogue of Bright Stars.

## Problem

Automated transcription of the star table from scanned pages was unreliable:
- Many transcription errors, particularly with minus signs and Greek letters
- Rows 251-300 were entirely missing coordinate data (only names remained)

Manual proofreading would have been error-prone and incomplete.

## Solution

The table was re-derived from the Yale Bright Star Catalog, 5th Revised Edition (BSC5), available at http://tdc-www.harvard.edu/catalogs/bsc5.html. This is the current authoritative edition of the catalog cited in the original book.

### Data sources

- **Rows 1-250, 301-332**: Yale catalog numbers extracted from the existing (partially correct) transcription
- **Rows 251-300**: Yale catalog numbers transcribed manually from the printed book

### Extraction process

1. Downloaded BSC5 catalog (1991 revision) from Harvard/CfA
2. Extracted J2000 coordinates (bytes 76-90), visual magnitude (bytes 103-107), and parallax (bytes 162-166) for each star
3. Formatted output to match the book's table structure
4. Used APL high minus (¯) for negative values, as in the original

## Discrepancies with printed book

Comparison of five test rows read directly from the printed book against BSC5 values:

```
                      Book (1978)                   BSC5 (1991)
Row  Star       Yale  RA        Dec      Mag    RA        Dec      Mag
───────────────────────────────────────────────────────────────────────
  1  ALPHERATZ    15   0  9 23   29   5  2.00    0  8 23   29   5  2.06
 27  ARCTURUS   5340  14 15 40   19  11  0.06   14 15 40   19  10 ¯0.04
 81  SIRIUS     2491   6 45  9  ¯16 ¯43 ¯1.47    6 45  9  ¯16 ¯42 ¯1.46
250  FOMALHAUT  8728  22 57 39  ¯29 ¯37  1.16   22 57 39  ¯29 ¯37  1.16
332  ζ VIR      5107  13 34 42    0 ¯36  3.40   13 34 42   ¯0 ¯35  3.37
```

Typical differences:
- RA: up to 1 minute
- Dec: up to 1 arcminute
- Magnitude: up to 0.1

### Possible sources of discrepancies

1. **Catalog improvements**: The BSC5 (1991) incorporates improved measurements and corrections made since the book's publication in 1978

2. **Original compilation errors**: Per Gjerlov may have made transcription or rounding errors when preparing the original table

3. **Different catalog editions**: The book may have used an earlier edition of the Yale catalog with different values

We cannot determine which explanation is correct without access to the 1978 catalog edition.

## Decision

Use BSC5 values for the reconstructed table. Rationale:
- BSC5 is the current authoritative source for the Yale Bright Star Catalog
- The reconstructed table will be more accurate than the original for astronomical purposes
- The project's goal is a working STARMAP, not a facsimile of the 1978 publication

## Manual corrections

After automated extraction, the following manual corrections were applied to the table in `book/markdown/starmap.md`:

1. **Parallax column alignment**: Negative numbers shifted left 1 space to align decimal points vertically

2. **Bayer designation formatting**: Some constellation abbreviations without Greek letters were incorrectly split (e.g., " S CO " corrected to "  SCO ")

These corrections address formatting issues in the extraction script output that were not worth fixing programmatically.

## Files

- `yale-catalog/ybsc5` - BSC5 catalog data
- `yale-catalog/ybsc5.readme` - Catalog format documentation
- `yale-catalog/extract_stars.py` - Extraction script
- `yale-catalog/star_table_new.txt` - Generated table (before manual corrections)
- `book/markdown/yale-numbers-251-300.txt` - Manually transcribed Yale numbers for missing rows
- `book/markdown/star-table-test-rows.md` - Test rows from printed book
