Typography
==========

The body of the STARMAP.pdf is typeset in Courier, with code set in the APL face derived from Courier Oblique.

Headings are underlined.

Paragraphs are separated by empty lines.
The first line of each paragraph is indented by three spaces.
Printed lines are justified left and right by extra spaces between words.
None of this style is required in the ouput.

Within a paragraph, underlining indicates emphasis;
in the output it can be indicated with
the usual Markdown convention of asterisks or underscores.

Figure captions and page numbers are in a sans-serif face.

Page numbers are not required in the output.

The text is in American English.
It includes occasional Greek characters, such as Ω and ⍵. 

## Code elements

Code in the document is in the APL programming language.

The APL typeface is all upper case, with underscored alphabetic characters.
This style reflected the then common marking technology of an IBM ‘golfball’, which could overstrike characters.

Its limited range of glyphs, extended through overstrikes to produce

-   A-Z
-   A-Z underscored
-   0-9
-   punctuation
-   APL glyphs, such as `←∇○∘⍳`

Modern APL typography, unconstrained by the golfball,
uses upper and lower cases and has no underscored alphabetics.

The STARMAP code minimises its use of underscored alphabetics.
To maximise visual fidelity, map underscored alphabetics
to *lower case* alphabetics, e.g. underscored `PLANETS` to `planets`.


## Code blocks

Code blocks are indented by 3 spaces.

Each code block begins with a `∇` glyph in the first or second column.
This is not required in the output.
Thus, for example,

```txt
 ∇ DISPLAY
   ENTRY
   ⍞
   WORK
```

becomes

```apl
DISPLAY
⍞
WORK
```


## Figures

The book includes several figures.
Insert link elements to them in the Markdown output, e.g.

    ![Fig. 3 Elements of an elliptical orbit](figure3.jpg)

If the corresponding images can be extracted from the PDF,
save them as siblings of the Markdown output;
otherwise the images can be extracted manually.

## Tables

The appendix contains three tables.

For the Markdown output it suffices to reproduce the first two,
from page 34, as fixed-width text blocks, just as they appear.

The third table, on pages 35–41, lists 332 bright stars,
and can be rendered similarly in Markdown
as a single table,
with the following cautions:

-   The underscores in the column headers indicate column groups, and may be ignored
-   The first character of the Bayer column is (except for rows 245–249) a Greek character
-   The high minus characters in the numerical columns (e.g `¯.0122`) should be preserved – they are how APL represents negative numbers

