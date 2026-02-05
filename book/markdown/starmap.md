# STARMAP

Paul C. Berry
John R. Thorstensen

APL PRESS
Pleasantville
New York

---

Copyright APL Press 1978

First published 1973 by IBM Corp. as Technical Report No. 02.665.

ISBN 0-917326-07-5

---

## Introduction

In many fields of science or commerce, it is possible to define a set of functions (i.e. computer programs) in such a way that each corresponds to a term or concept used in that discipline. Such a set of functions in effect constitutes a "user language" for that particular area of application. If that language has a simple and consistent syntax, and if its various functions refer to the data on which they work in a consistent way, it is possible to achieve a programming package that is easy to understand, to revise, or to adapt to new applications. At the same time, such a package constitutes an *executable model* of some of the concepts of that discipline.

Constructing a particular definition by referring to a set of simpler or more general sub-definitions is the principal technique of what has come to be called *modular programming*; the program used for a particular job consists of a brief invocation of the concepts or components from which it is made. They in turn are defined by invoking modules at the next level of detail. Reading programs that have been written in that way, the student sees at the outer level a brief summary of the organization of the work; pursuing the definitions further, he or she may obtain explanation to whatever level of detail is desired.

The aim of this paper is to illustrate this style of programming in APL by presenting in detail the definitions used in a particular project. We selected for this purpose the set of programs contained in an APL workspace called STARMAP, which was in use as part of a display on astronomy at the IBM Exhibit Center in New York during 1973 and 1974. That set of programs served to print at a terminal a map showing the positions of the brighter stars, the planets, and the comet Kohoutek, as they would appear above any point on Earth at any time on any date--at least for some number of years on either side of the present.

To generate a map, the user started work by invoking a function called `DISPLAY`. Thereupon he or she was asked to specify the date for which a map was wanted, the local time, and the latitude and longitude. The program then computed the positions of the stars and planets, and drew the map, either at the typewriter terminal (using a special type element for fine plotting) or on a cathode-ray display tube. A sample of the conversation in which a user enters the specifications of a map is shown in Figure 1; the resulting chart (photographically reduced from the original size of about 35 cm. square) is shown in Figure 2.

![Fig. 1 Dialog during user's request for a star map](figure-01.png)

*Fig. 1 Dialog during user's request for a star map*

Following this dialog, the keyboard is unlocked, awaiting a carriage return from the user to indicate that the fine plotting element has been inserted and the paper is ready to receive the printed map.

On the opposite page appears the map generated in response to the request shown in Figure 1. The map has been photographically reduced; the actual print-out is about 35 cm. high. The fine plotting type element (number 114) carries fifteen dots and fifteen crosses, one for each position of a 3-by-5 matrix, giving a resolution of about .85 mm (1/30 inch) between adjacent points vertically or horizontally. Four additional star maps are shown beginning on page 28.

![Fig. 2 Sample chart produced by the STARMAP workspace](figure-02.png)

*Fig. 2 Sample chart produced by the STARMAP workspace*

To generate such a map requires solving the formulas for planetary motion in order to know where in the solar system the planets should be located at the date requested, and then to translate those coordinates to show their apparent positions as seen from the Earth. The coordinates thus obtained, together with those of the fixed stars, could then be rotated for the desired time and location on the surface of the Earth.

The motions of the planets may be described by formulas that were first developed by Kepler early in the seventeenth century. Kepler's function states the time needed for a planet to traverse a given angle through its orbit. To find the position at a given time requires the inverse of that function; a general iterative method, applicable to evaluating that inverse, was worked out by Newton later in the same century. The rest of the task is an exercise in analytic geometry, to translate and rotate the coordinates appropriately. Formulas for doing so were familiar in the seventeenth and eighteenth centuries, but were simplified by the matrix algebra developed in the nineteenth century. Thus the programming task involved here consists mainly of representing in terms executable by the computer a set of classical formulas.

The interest in these programs lies not in the method itself, which has been well known for many years, but in the style in which classical and familiar formulas may be stated in APL. Our aim was to provide APL definitions for a vocabulary of terms which would not only make clear the process by which the work is done, but would permit the student of astronomy to apply them to new problems or applications. Where possible, we used names that correspond to those in general use in astronomy. Occasionally we had to coin names for functions which are not usually explicitly identified, but even here our terms should be recognizable to astronomers. To make our APL definitions correspond more directly to familiar formulas, we also made free use of defined functions such as `SIN`, `COS`, `PI`, `RADIAN`, etc. despite the fact that their effects could be readily obtained from APL primitives.

Clearly, programs to convert the coordinates into a printed map or video display were also necessary to this project, but these are standard packages in widespread use, and we have not chosen to discuss them here.

## Organization and Key Parameters

The function `DISPLAY` initiates the entire task. It calls functions corresponding to the various stages of work. A tabular outline of the functions used is shown in Table 1. At the top left of the table the name `DISPLAY` appears, indicating that this is the primary function. Indented five spaces below it appear the names of each of the functions called by `DISPLAY`. Indented below them appear the names of functions they call, and so on. (For simplicity, some references to functions such as `SIN`, `COS`, `RADIAN`, etc. have been omitted from the table.) The rest of this paper provides an explication of the work being done at each of these stages, in top-down order.

In the text that follows, the symbol `∇` (del) is used to indicate the `header` of a function, containing the name of the function, names for its arguments and results, and names for temporary variables used as intermediate steps in its definition, if any. As may be seen below, `DISPLAY` calls `ENTRY` (which requests input for the parameters governing a particular map), then pauses to permit the user to align the paper and insert the fine plotting element (indicated by the input symbol `⎕`), and then calls `WORK`, which does the necessary calculations and prints the map:

```apl
DISPLAY
ENTRY
⎕
WORK
```

The function `ENTRY` establishes the values of the input parameters by calling the functions `GETDATE`, `GETTIME`, `GETLAT`, and `GETLONG`, and adjusts the date and time stated by the user to correct for the indicated longitude:

```apl
ENTRY
STATEDDAYNO←GETDATE
STATEDTIME←GETTIME
LAT←GETLAT
LONG←GETLONG
TIME←LONG TIMEADJUST STATEDTIME
DATE←STATEDDAYNO+(TIME÷24)-LONG÷360
```

When execution of `ENTRY` is complete, values have been established for the following variables:

`TIME`: Time is a single number indicating the number of hours since midnight in the exact local time for the indicated longitude. (However, the user enters the time in conventional form as it would appear on a clock in the nearest time zone.)

`DATE`: Although entered in a conventional form, the date is represented internally as the Julian day number; a function `JNU` converts the date to that form. (The Julian day number of 1 January 1974 was 2442049.) The fractional part of the day number indicates how far through the day by universal time the indicated time is. Thus before the major calculations take place, all information on time is contained in the single number `DATE`.

`LAT`: Number of degrees north of the Equator.

`LONG`: Number of degrees east of the prime meridian.

The time and date as entered by the user are preserved as `STATEDTIME` and `STATEDDATE`, and the Julian day number of the stated date as `STATEDDAYNO`; in some circumstances the adjusted value of `DATE` (in universal time) may fall within a day 1 more or less than the stated date.

## Stages of Calculation

The task of calculation and printing may be divided into seven stages, each defined by a single function:

```apl
WORK
CAPTION
CALCULATEPLANETS
REPORTPLANETS
CALCULATESTARS
PLOTSTARS
REPORTSTARS
PRINTED
```

The sequence of segments is designed to overlap output to the terminal (produced by `CAPTION` or `REPORTPLANETS`) with the segments that require substantial calculation.

The function `CAPTION` recapitulates the stated input parameters, and adds the day of the week (directly obtainable from 7|STATEDDAYNO). The function `REPORTPLANETS` prints a table showing for each planet (and the moon, sun, and comet) its right ascension and declination. For those that are visible, the altitude and azimuth are included, together with the coordinates on the map grid. The phase of the moon is reported.

The function `PLOTSTARS` calls `FPLOT`, which is adapted from the fine-plotting function in IBM program 5798-AGL, "Graphs and Histograms in APL." The stars and planets visible above the horizon are plotted, together with a circular frame of dots at 3-degree intervals around the horizon, and cross marks at intervals of 15 degrees of elevation. The standard plotting program was modified to insert a label showing the name of each planet, and to print a special symbol for the sun and moon.

The function `REPORTSTARS` prints a table showing the names of bright stars appearing in the plot, together with the altitude, azimuth and map-grid coordinates of each. The function `PRINTED` permits the finished map to be labelled with the name of the person for whom it was prepared, and reports the date and time at which it was printed. The input and output functions are not described further in this article.

The functions `CALCULATEPLANETS` and `CALCULATESTARS` use the global arguments `DATE`, `TIME`, `LAT`, and `LONG`, as well as the following reference tables:

`STARS`: A table containing the right ascension and declination of about 300 bright stars.

`planets`: A table of the elements for the elliptical orbits of the nine planets.

`MOON`: A similar table for the elements of the moon's elliptical orbit about the Earth.

`KOHOUTEK`: A table of the elements for the parabolic orbit of the comet.

`BRIGHT`: A logical vector indicating which members of `STARS` represent stars of magnitude 1.5 or brighter.

`BP`: A logical vector indicating which planets are usually of magnitude 1.5 or brighter.

The positions of the stars are taken from the Yale Catalog of Bright Stars, and the elements of the planetary orbits from the American Ephemeris and Nautical Almanac for 1973. The orbital functions which follow were written after consulting the text by Marion (1965) Classical Dynamics of Particles and Systems.

## Coordinate Systems Used in Describing the Positions of the Planets

Calculating the appearance of the heavens can be divided into two principal tasks: finding the locations of the planets in the solar system, and then calculating how they appear to an observer. A large part of the work thus involves rotation of coordinate axes, or translation from one system of coordinates to another. It will help to understand the programs that determine the positions of the planets if the various coordinate systems are first described.

*Two-dimensional coordinates in the plane of each planet.* Each of the objects in orbit around the sun is first considered to be moving along an ellipse (or, in the case of the comet, along a parabola) lying in a plane. Each planet can thus be located by two coordinates. During the initial solution of the orbits, these are polar coordinates; they are then converted to Cartesian coordinates, describing the planet's position by its distance from the solar focus along the major and minor axes of the ellipse. Two-dimensional coordinates appear only within the functions `PLANETPOS`, `MOONPOS`, and `COMETPOS`.

*Heliocentric Cartesian coordinates.* The two-dimensional Cartesian coordinates that specify each planet's position within the plane of its own orbit are converted to a common three-dimensional coordinate system whose center is in the sun. The first coordinate points from the sun in a direction opposite to the Earth at the moment of the vernal equinox. The second points perpendicularly out of the plane of the ecliptic, on the same side as the north pole. The third points in the plane of the ecliptic, perpendicularly to the other two, so that the three form a right-handed coordinate system. It intersects the celestial sphere at a right ascension of 18 hours (i.e. 270 degrees) and a declination (due to the tilt of the Earth's axis) of -23.45 degrees.

Positions stated in the heliocentric system are given the name `H` in the functions `PLANETPOS`, `MOONPOS`, `COMETPOS`, and in `EARTHVIEW` (which translates from heliocentric to geocentric coordinates).

The function `ORBROTATE` converts the two-dimensional Cartesian coordinates of the planets within their own planes to three-dimensional heliocentric coordinates, taking into account the orientation and tilt of the plane of each orbit, by reference to the elements `PERIANGLE` (angle of perihelion), `INCLINATION`, and `ASCENDING` (the angle of the ascending node); see pp. 14-15.

*Geocentric ecliptic coordinates.* The axes of this system are parallel to those of the heliocentric system, but have their origin in the center of the Earth rather than in the sun; values in this system are obtained simply by subtracting the heliocentric coordinates of the Earth from those of the object in question. Coordinates stated in this system are given the name `GC`. They appear as intermediate steps in the function `EARTHVIEW`.

*Geocentric equatorial coordinates.* This is a Cartesian form of the standard astronomical system of right ascension and declination. The first axis points (as before) to the vernal equinox. The second points to the north celestial pole. The third points at a location on the equator at the right ascension of the winter solstice.

Positions in this coordinate system are obtained from those stated in the geocentric ecliptic system by a rotation of 23.45 degrees around the first axis. Variables stated in these coordinates are given the name `GQ`.

*Egocentric coordinates.* The final transformation is to adjust for the position on Earth of the observer for whom the map is calculated. The first axis points due south. The second points to the zenith (above the observer). The third points due west. Positions in this system are obtained from positions in the geocentric equatorial system by a sequence of rotations in the course of the function `SKYPOS`, whose arguments are the positions of the planets in geocentric equatorial coordinates (`GQ`) and the latitude, date, and time of the viewing point on Earth. The result is in units of altitude and azimuth, and such variables are given the name `AA`.

## Calculating the Positions of the Planetary Bodies

The function `CALCULATEPLANETS` finds `PLANETS`, a table of the positions of the sun, moon, and planets at the desired date. When first calculated by the function `PLANETPOS`, these positions are stated in 3-dimensional heliocentric Cartesian coordinates. But the function `EARTHVIEW` converts them to geocentric polar coordinates (right ascension in hours, declination in degrees, and distance in astronomical units), locating the planets with respect to the center of the Earth.

In order to plot the sky above a particular place, the function `SKYPOS` (see p. 29) is used to calculate `AA`, a table of altitude and azimuth with respect to given time and location on the Earth's surface. The function `VISIBLE` is used to select from `P` those members that are above the horizon, and saves them in the table `AAE`. Finally, the `PROJECTION` of these coordinates onto a flat surface is calculated, and translated to the Cartesian form expected by the plotting function; the function `IF` is simply a compression of the left argument by the APL symbol `/`.

```apl
CALCULATEPLANETS; AA; MOON; SUN; KOHOUTEK
PLANETCOORD←AAE←PLANETS←VP←10
PLANETS←DATE EARTHVIEW DATE PLANETPOS (3×19)/planets
SUN←DATE EARTHVIEW 0 0 0
K←100≥|DATE-JNU 12 28 1973
KOHOUTEK←DATE EARTHVIEW (DATE IF K) COMETPOS KOHOUTEK
MOON←MOONPOS DATE
PHASE←MOON[1;1] MOONPHASE SUN[1;1]
PLANETS←MOON,[1] SUN,[1] PLANETS,[1] KOHOUTEK
MOON←MOON[;3] PARALLAXADJUST (LAT,DATE,TIME) SKYPOS MOON
AA←MOON,[1] (LAT,DATE,TIME) SKYPOS 1 0+PLANETS
PLANETCOORD←MAPCARTESIAN PROJECTION AAE←AA IF VP←VISIBLE AA
```

Execution of `CALCULATEPLANETS` causes new values to be assigned to four global variables. (These are initially set to 10 in the first statement, mainly to draw attention to a list of the global variables which will be reset as a consequence of executing this function.) The four are:

`PLANETS`: The right ascension and declination of the moon, sun, planets, and Kohoutek.

`VP`: A logical vector indicating which planets are visible from the place, date, and time requested.

`AAE`: The altitude and azimuth of the visible planets.

`PLANETCOORD`: The Cartesian coordinates used to plot the projection of the visible planets.

## Orbital Parameters

The functions that locate the positions of the planets in their orbits make reference to a set of parameters usually called the `elements` of the orbit. The reference set of orbital elements for the planets is stored in the matrix `planets`. Each row contains the set of elements for a particular planet. For example:

```apl
Z←EARTH
Z←planets[,3;]
```

Each column corresponds to a particular element of the various orbits. Each of the functions that makes use of the orbital elements (`PLANETPOS`, `MOONPOS`, or `COMETPOS`) take as one of its arguments a matrix containing the rows of the table `planets` that are appropriate: i.e. those corresponding to the particular planets being considered. This sub-table is given the name `ORB`. Functions are provided corresponding to each orbital element (for example, `PERIOD`, `ECCENTRICITY`, `INCLINATION`, etc.). Those functions select the appropriate column of the table `ORB`. In that way, terms such as `PERIOD`, `ECCENTRICITY` or `INCLINATION` refer to those elements for the planets currently under consideration, whatever those may be. This is achieved by making `ORB`, the table from which the values are selected, global with respect to these selection functions, but local to the functions such as `PLANETPOS` which use the elements, since `ORB` there appears as the explicit argument.

The geometrical meanings of the terms inclination, ascending node, and angle of perihelion are illustrated in Figure 5.

```apl
Z←SEMIMAJOR                    Z←ASCENDING
Z←ORB[;1]                      Z←ORB[;5]

Z←PERIOD                       Z←PERIANGLE
Z←ORB[;2]                      Z←ORB[;6]

Z←ECCENTRICITY                 Z←ANOMALY
Z←ORB[;3]                      Z←ORB[;7]

Z←INCLINATION                  Z←ANOMALYDATE
Z←ORB[;4]                      Z←ORB[;10]
```

The date of perihelion is computed from the elements already tabled:

```apl
Z←PERIDATE
Z←ANOMALYDATE - PERIOD×ANOMALY÷360
```

![Fig. 3 Elements of an elliptical orbit](figure-03.png)

*Fig. 3 Elements of an elliptical orbit*

The rectangular plane represents the plane of the ecliptic. The focus of the planet's elliptical orbit is the sun. `INCLINATION` is the angle between the plane of the ellipse and the plane of the ecliptic.

The `ASCENDING` node is the point at which the planet's orbit passes through the plane of the ecliptic from south to north.

The angle Ω is measured in the plane of the ecliptic, from a line from the sun through the vernal equinox, to a line from the sun to the ascending node.

The angle ω is measured in the plane of the planet's orbit, from a line from the sun to the ascending node, to the major axis on the side of perihelion.

The parameter `PERIANGLE` used in this article is defined as Ω+ω.

In finding where a planet is located at a particular date, one must know what portion of its total period has elapsed since its last perihelion. This is provided by the function `PERIODER`:

```apl
Z←PERIODER DATE
Z←1|(ANOMALY÷360) + (DATE-ANOMALYDATE) ÷ PERIOD×TROPYR
```

## Epochal Adjustment of Planetary Elements

The orientations of the major axes of the elliptical orbits of the planets are not fixed, but themselves rotate steadily; the effect is appreciable over long intervals. Allowance for this secular shift requires an adjustment to the elements `ASCENDING` (the angular coordinate of the ascending node) and `PERIANGLE` (the angular coordinate of perihelion). An approximate adjustment is made by the function `EPOCHADJUST`. It revises the values in columns 5 and 6 of `ORB` (i.e. the ascending node and the angle of perihelion) by the size of the secular shift per unit time, multiplied by the interval since the epoch date. The secular effect is here considered to be linear with time:

```apl
Z←INTERVAL EPOCHADJUST ORB
ORB[; 5 6]←ORB[; 5 6] + SECULAR × INTERVAL
Z←ORB

Z←SECULAR                      Z←EPOCHDATE
Z←ORB[;8 9]                    Z←ORB[;10 11]
```

## Procedure for Locating the Planets

The function `PLANETPOS` finds the positions of any or all the planets as a function of the date and their orbital elements.

```apl
H←DATE PLANETPOS ORB; E; THETA
ORB←(DATE-EPOCHDATE) EPOCHADJUST ORB
E←ECCENTRICITY
THETA←E TRUEANOMALY E KEPLINVERSE 2×PI×PERIODER DATE
H←ORBROTATE CARTESIAN THETA,[1.5] RADIUS THETA
```

The third statement of `PLANETPOS` finds `THETA`, the angle between each planet's position at perihelion and its position on the indicated date. The function `RADIUS` finds the distance that angle intersects the ellipse:

```apl
Z←RADIUS THETA; E
E←ECCENTRICITY
Z←SEMIMAJOR×(1-E×2)÷1+E×COS THETA
```

In the last statement of `PLANETPOS`, the polar coordinates `THETA` calculated in the preceding step are converted to Cartesian heliocentric coordinates `H`.

## The Inverse of Kepler's Function

The formula for an ellipse permits us to state the distance from the solar focus to a point on the ellipse (that is, the radius at that point) as a function of the angle `THETA` between the major axis and a line through the focus to that point. However, finding the true anomaly `THETA` directly as a function of time is difficult. An easier method is due to Kepler. He discovered that a closely related angle `PSI` could be constructed (see Figure 4) for which the solution is simpler. A quantity proportional to the time is computed by `KEPLERFN` as a function of `PSI` and the eccentricity `E`:

```apl
TIME←E KEPLERFN PSI
K←⊖(⊂1+ρPSI),ρE)ρE
TIME←PSI - E×SIN PSI
```

Notice that as `E` goes to zero (meaning that the ellipse approaches a circle) `KEPLERFN PSI` approaches `PSI`.

To find `PSI` as a function of time, `KEPLERFN` must be inverted. Because `KEPLERFN` involves both `PSI` and `SIN PSI`, it is transcendental, and approximations must be used to evaluate its inverse. We used an iterative method. In this procedure, each estimate of `PSI` is adjusted by correcting the previous approximation by an amount inversely proportional to the derivative. That general procedure is known as Newton's method; it was while working on solutions to Kepler's equations that Newton developed the method:

```apl
PSI←E KEPLINVERSE TIME; ERROR; TOL
TOL←1E¯10
TIME←PSI←((ρE),ρTIME)ρTIME
TEST: →END IF ∧/,TOL>|ERROR←TIME-E KEPLERFN PSI
PSI←PSI+ERROR÷E KEPDERIV PSI
→TEST
END: PSI←+/PSI×(2ρE)ρ(1+ρE)÷1
```

The restructuring appearing in the second statement and the last statement (and also in `KEPDERIV`, below) is introduced to permit parallel solution for multiple values of `E` and `TIME`, so that all planets can be treated at once.

The derivative of Kepler's functions is given as follows:

```apl
Z←E KEPDERIV PSI
E←⊖(⊂1+ρPSI),ρE)ρE
Z←1-E×COS PSI
```

Now that `PSI` has been found, the more useful true anomaly can be found by analytic geometry:

```apl
THETA←E TRUEANOMALY PSI
THETA←(2×PI)|2×ARCTAN (SQRT(1+E)÷1-E) × TAN PSI÷2
```

The function `RADIUS` can now used to find the planet's distance from the sun in astronomical units.

![Fig. 4 Angles θ and ψ in the calculation of true anomaly](figure-04.png)

*Fig. 4 Angles θ and ψ in the calculation of true anomaly*

The angle `THETA` is measured between the major axis and a line drawn from the focus to the planet's position on the ellipse.

The angle `PSI` is measured from the major axis to a line drawn from the center of a circle circumscribed about the ellipse, to the point where a line drawn perpendicular to the axis and passing through the planet intersects the Earth.

## Plotting the Heliocentric Coordinates of the Planets

The aim in preparing this set of functions was to draw maps showing the sky as it appears above a particular place on Earth. To achieve that, the heliocentric coordinates just calculated must be further translated and rotated to allow for the position of the Earth in the solar system and of the observer on the Earth. However, before introducing the functions that carry out that part of the task, we illustrate a use of the heliocentric coordinates. A function `PLANETSPOS` constructs (iteratively) a table showing for a selected set of dates the positions of selected planets (and also of the comet Kohoutek) for each of an array of dates:

```apl
H←DATES PLANETSPOS P; I; D; PL
DATES←,DATES
PL←planets[P;]
H←(0,(1+ρP),3)ρI←0
TEST: →0 IF (ρDATES)<I←I+1
D←DATES[I]
H←H,[1] (D PLANETPOS PL),[1] D COMETPOS KOHOUTEK
→TEST
```

The result is a 3-dimensional array, dates by planets by coordinates. Plotting the first coordinate against the third, we obtain a diagram showing the positions of the planets projected in the plane of the ecliptic (Figure 5).

![Fig. 5 Sample output of program to plot heliocentric coordinates](figure-05.png)

*Fig. 5 Sample output of program to plot heliocentric coordinates*

The plot shows the orbits of the four inner planets and the comet Kohoutek at 2-day intervals from 20 October 1973 through 30 March 1974.

## Positions of the Earth and Moon

In order to find the geocentric coordinates of the other bodies, the heliocentric coordinates of the Earth are required. However, this does not require a special function, since they are directly obtainable from the expression

```apl
DATE PLANETPOS EARTH
```

in which `EARTH` is the function which selects the orbital elements of the Earth.

Since the moon is in an elliptical orbit about the Earth, the position of the moon with respect to the earth can be found by the same procedure used to locate the planets with respect to the sun. In calculating the position of the moon, the positions of the ascending node and the angle of perihelion are subject to linear epochal adjustments that are larger than those for the planets, but they are computed in exactly the same way:

```apl
GQ←MOONPOS DATE; GC
GC←DATE PLANETPOS MOON
GQ←3 RADECDIST GC+.×INCLROTATE RADIAN AXITILT×23.4428
```

In the case of the moon, the unit of distance is the semimajor axis of the orbit of the moon rather than of the Earth.

The rotation functions will be discussed below (see pp. 26-27); the function `RADECDIST` calculates polar coordinates in units of right ascension, declination, and distance; the left argument 3 indicates that in this case all three are to be retained.

Since `MOONPOS` finds the moon's position with respect to the Earth, the result is stated with respect to the Earth, and there is no need for subsequent translation from heliocentric to geocentric coordinates. (In the definition of `CALCULATEPLANETS`, p. 13, the expressions for `PLANETS`, `SUN` and `KOHOUTEK` require the application of the function `EARTHVIEW`, whereas the expression for `MOON` does not.) However, the moon is sufficiently close to the Earth that in calculating its apparent position allowance must be made for the parallax introduced by the fact that the observer's position on the surface of the Earth may depart significantly from a line between the center of the Earth and the center of the moon. Such a correction to the moon's altitude is used in `CALCULATEPLANETS`:

```apl
Z←DIST PARALLAXADJUST AA; ALT
ALT←AA[;1]
Z←AA
Z[;1]←ALT - (COS RADIAN ALT)×MOONRATIO÷DIST
```

in which `MOONRATIO` is the ratio of the semimajor axis of the moon's orbit to the radius of the Earth, expressed in radians; the value is about 0.95.

The phase of the moon depends upon the difference between the right ascensions of the sun and moon:

```apl
Z←MOON MOONPHASE SUN
Z←1|(MOON-SUN)÷24
```

The moon is full when their right ascensions differ by 12 hours, and new when they are equal. When both the right ascension and the declination of the moon are equal to those of the sun, there is an eclipse of the sun; when their right ascensions differ by 12 hours and their declinations are equal but of opposite sign, there is an eclipse of the moon.

## Position of the Comet

The position of Kohoutek is calculated only for dates within 100 days of its perihelion, 28 December 1973. The logical variable `K` (set in `CALCULATEPLANETS`) has the value 1 when Kohoutek is within range, 0 otherwise. The expression *K/DATE* thus makes the date empty when the position of the comet is not needed.

```apl
H←DATE COMETPOS ORB; X
H← 0 3ρ0
→0 IF 0=ρ,DATE
X←COMETSOLVE (PI×SQRT 2×PERIDIST)×(DATE-ANOMALYDATE)÷TROPYR
H←ORBROTATE (PARABOLA X), ¯X
```

The method used to locate the comet is similar to that used for the planets. However, for several reasons the polar coordinates used in the initial two-dimensional solution for the planets are here replaced with Cartesian coordinates. The approximations for planets (whose orbits are nearly circular) do not converge easily when applied to the comet, whose orbit is almost exactly parabolic. The usual polar expression in the function `RADIUS` is singular when `E` is 1 (parabola) and `THETA` is `PI`. Moreover, the Cartesian expression for a parabola is simple to integrate; hence Kepler's equal-areas equal-times law is easily applied.

The time required to reach a point on the parabolic path of the comet as a function of the distance from the axis of the parabola is given by the function `AREA`:

```apl
Z←AREA X
Z←(PERIDIST×X÷2) + (X×3)÷4×PERIDIST
```

in which the orbital element `PERIDIST` is the distance from the sun at perihelion, in astronomical units:

```apl
Z←PERIDIST
Z←ORB[;1]
```

The function `COMETSOLVE` provides an iterative definition for the inverse of `AREA`, giving the perpendicular distance from the axis of the parabola as a function of the time interval from perihelion:

```apl
X←COMETSOLVE TIME; ERROR
X←2×TIME÷PERIDIST
TEST: →0 IF 1E¯8>|ERROR←TIME-AREA X
X←X+ERROR÷AREADERIV X
→TEST
```

Here again the inverse is found by Newton's method; convergence is speeded by the use of the derivative of the area function with respect to the abscissa:

```apl
Z←AREADERIV X
Z←(PERIDIST÷2) + (X×2)÷8×PERIDIST
```

The second coordinate of the comet's position (within the plane of its orbit) is measured in the direction of the axis of the parabola. It is obtained from the first coordinate by the function `PARABOLA`:

```apl
Z←PARABOLA X
Z←PERIDIST - (X×2)÷4×PERIDIST
```

## Rotation of the Stars

The positions of the stars are represented by a table of their right ascensions and declinations, as of 1 January 2000, contained in the matrix `STARS`. There is no provision for the proper motions of the stars, nor for the effects of parallax between different positions on the Earth's orbit, since both these effects are small compared to the precision of the rest of the calculation or to the resolution of the plotting program. The calculation thus reduces to the correction for the observer's position at a given latitude, date, and time, and the long-run variation introduced by precession.

```apl
CALCULATESTARS; STARS
VE←BRIGHT←STARCOORD←AAE←10
STARS←(LAT,DATE,TIME) SKYPOS DATE PRECESS STARS
BRIGHT←BRIGHT IF VE←VISIBLE STARS
AAE←STARS IF BRIGHT∧VE
STARCOORD←MAPCARTESIAN PROJECTION STARS IF VE
```

The global results of this function (initially set to 10 in the first statement) are as follows:

`STARCOORD`: Cartesian coordinates on the map for the stars visible from the indicated time, date, and location.

`BRIGHT`: A logical vector indicating which of the visible stars are of magnitude 1.5 or brighter.

`VE`: A logical vector indicating which stars are visible.

`AAE`: A matrix containing the altitude and azimuth of the visible bright stars.

## Correction for Precession

The effect of precession is to alter the direction in which the Earth's axis is tilted. A line drawn from the north pole to the zenith (which today points approximately to the star Polaris) in the course of 25800 years describes a complete circle, with radius 23.45 degrees. What changes with precession is the direction in which the Earth's north pole departs from a point perpendicular to the plane of the Earth's orbit. However, since the direction of the equinox enters into the definition of one of the axes of both the heliocentric and the geocentric ecliptic coordinates, the effect appears as a systematic rotation of the entire star table. The function `PRECESS` makes this adjustment by first removing the Earth's axial tilt, then rotating about the second axis through an angle that would amount to a complete rotation in 25800 years, and then restoring the axial tilt.

```apl
Z←INTERVAL PRECESS X; PRECESSION; ROT; TILT; DETILT; RETILT
X←CARTRIPLET X
RETILT←INCLROTATE TILT←RADIAN AXITILT
DETILT←INCLROTATE -TILT
PRECESSION←LONGROTATE INTERVAL × 2×PI÷25800×YRLENGTH
ROT←RETILT+.×PRECESSION+.×DETILT
Z←2 RADECDIST X+.×⊖ROT
```

The variable `TROPYR` is the length of the tropical year in days; `EQUINOX` is the Julian date of a vernal equinox (in this case, for 1973).

The function `LATROTATE` prepares a matrix of sines and cosines, exploiting the relation between rotation of latitude and rotation of inclination:

```apl
Z←LATROTATE LAT
Z←⊖⊖INCLROTATE LAT
```

## Conversion of Units

The positions of objects in the sky are described in spherical polar coordinates, usually as right ascension, declination, and distance. The first two are stated as angles in hours or degrees, and the last in astronomical units. The function `RADECDIST` converts from Cartesian to polar coordinates in which right ascension is stated in hours and declination in degrees. Since the distance of celestial objects is not apparent from the Earth, only the right ascension and declination are required for some calculations; by using a left argument of 2, only the first two coordinates are retained, and distance is dropped where it is no longer appropriate:

```apl
Z←COL RADECDIST GQ; DIST
Z←ARCCOS GQ[;1]÷(GQ[; 1 3]+.*2)×0.5
Z←(12÷PI)×Z+(GQ[;3]>0)×2×PI-Z
DIST←(GQ+.*2)×0.5
Z←Z,[1.5] (180÷PI)×ARCSIN GQ[;2]÷DIST
→0 IF COL<3
Z←Z,DIST
```

The norm is defined as the square root of the sum of the squares:

```apl
Z←NORM X
Z←(X+.*2)×0.5
```

Conversion to Cartesian from polar coordinates is provided by the function `CARTESIAN`:

```apl
Z←CARTESIAN POLAR; RHO; THETA
THETA←POLAR[;1]
RHO←POLAR[;2]
Z←(RHO×COS THETA),[1.5] -RHO×SIN THETA
```

Conversion to non-normalized three-dimensional Cartesian coordinates from spherical polar coordinates is provided by the function `CARTRIPLET`:

```apl
Z←CARTRIPLET RADEC; Z1; Z2; Z3
Z1←COS PI×RADEC[;1]÷12
Z2←TAN RADIAN RADEC[;2]
Z3←-SIN PI×RADEC[;1]÷12
Z←Z1, Z2,[1.5] Z3
```

## Sample Star Maps

On the following pages maps generated by these programs are reproduced, showing the views from Philadelphia on 14 January 1974 (when Kohoutek was visible), and from the Arctic circle at midnight on 21 June 1974. On two further charts, showing the views from the north and south poles at the vernal equinox, lines linking stars in the same constellation have been drawn in by hand.

![Fig. 7 Star map at Philadelphia on January 14, 1974](figure-07.png)

*Fig. 7 Star map at Philadelphia on January 14, 1974*

![Fig. 8 Star map at Fort Yukon on June 31, 1974](figure-08.png)

*Fig. 8 Star map at Fort Yukon on June 31, 1974*

![Fig. 9 Star map at North Pole on March 19, 1974](figure-09.png)

*Fig. 9 Star map at North Pole on March 19, 1974*

![Fig. 10 Star map at South Pole on March 19, 1974](figure-10.png)

*Fig. 10 Star map at South Pole on March 19, 1974*

## Projection of the Visible Sky

Once the altitude and azimuth of moon, sun, planets, and comet have been calculated, it remains only to select those that are visible, and calculate a suitable projection for the map. Objects are considered to be visible if they are on or above the horizon, i.e. if they have non-negative altitude:

```apl
Z←VISIBLE X; ALT
ALT←X[;1]
Z←ALT≥0
```

To preserve the apparent shapes of constellations when projected onto a flat surface, the altitudes near the zenith are condensed and those near the horizon expanded by the function `PROJECTION` which makes the distance from the center of the map proportional to the tangent of one half the coaltitude:

```apl
Z←PROJECTION X
Z←(TAN 0.5×COALTITUDE X[;1]),[1.5] RADIAN X[;2]
```

in which coaltitude is defined thus:

```apl
Z←COALTITUDE X
Z←RADIAN 90-X
```

Since the plotting routine expects its data to be stated in Cartesian coordinates, the projected polar coordinates are converted back to that form. The function `MAPCARTESIAN` makes allowance for the fact that altitude and azimuth are conventionally grouped in the opposite order from right ascension and declination:

```apl
Z←MAPCARTESIAN X
Z←⊖CARTESIAN⊖X
```

## Functions for Rotation and Translation of Coordinates

The function `ORBROTATE` converts the two-dimensional Cartesian coordinates of the planets within their own planes to three-dimensional heliocentric coordinates, taking into account the orientation and tilt of the plane of each orbit:

```apl
H←ORBROTATE X; INCL; I; OMEGA; O; OMEG4; Q
X←((ρX),1)ρX← 1 0 1 \X
OMEGA←RADIAN PERIANGLE-ASCENDING
OMEG4←RADIAN ASCENDING
INCL←RADIAN INCLINATION
I←INCLROTATE INCL
O←LONGROTATE OMEGA
Q←LONGROTATE OMEG4
H←(Q TIMES I TIMES O) TIMES X
H←((1+ρH),×/1+ρH)ρH
```

The rotations are achieved by a series of matrix products. The functions `INCLROTATE` and `LONGROTATE` generate the appropriate matrices of sines and cosines, stacking them in a three-dimensional array since several sets of coordinates are to be rotated at once. The function `TIMES` (not shown) calculates the ordinary matrix product of the corresponding pairs of matrices in a three-dimensional stack.

The functions `INCLROTATE` and `LONGROTATE` generate stacks of matrices containing the appropriate sines and cosines of the angles through which rotation is to occur (see Figure 6):

```apl
Z←INCLROTATE INCL; RHO
RHO←ρINCL
Z←((ρ,INCL), 3 3)ρ9↑1
Z[;2;2]←Z[;3;3]←COS INCL
Z[;2;3]←-Z[;3;2]←SIN INCL
→(0<ρRHO)/0
Z← 3 3 ρZ

Z←LONGROTATE OMEGA; RHO
Z←((ρ,OMEGA), 3 3)ρ 0 0 0 0 1 0 0 0 0
Z[;1;1]←Z[;3;3]←COS OMEGA
Z[;3;1]←-Z[;1;3]←SIN OMEGA
→(0<ρRHO)/0
Z← 3 3 ρZ
```

These functions are used in translating the heliocentric coordinates of the planets to geocentric equatorial coordinates (i.e. the view from the center of the Earth):

```apl
GQ←DATE EARTHVIEW H; GC
GC←H-(ρH)ρDATE PLANETPOS EARTH
GQ←3 RADECDIST GC+.×INCLROTATE -RADIAN AXITILT
```

in which `AXITILT` is the angle between the axis of the Earth and the plane of the ecliptic.

![Fig. 6 Stacking of rotation matrices](figure-06.png)

*Fig. 6 Stacking of rotation matrices*

Each plane represents the rotation matrix for one of the planets.

The next transformation adjusts for the location on the Earth of the observer for whom the map is calculated. The coordinates with respect to the observer are described in a system in which the three coordinates point respectively south, overhead, and west. These are calculated by `SKYPOS` as a function of the geocentric equatorial coordinates `GQ`, and the observer's latitude and true local time:

```apl
AA←EARTH SKYPOS GQ; SUN; ROT; LAT; DATE; TIME; ALT; AZ; NEG; S
LAT←EARTH[1]
DATE←EARTH[2]
TIME←EARTH[3]
SUN←(24÷YRLENGTH)×YRLENGTH|DATE-EQUINOX
ROT←PI×(SUN+TIME-12)÷12
LAT←RADIAN 90-LAT
GQ←GQ+⊖(⊖ρGQ)ρNORM GQ←CARTRIPLET GQ
GQ←GQ+.×⊖(LATROTATE LAT)+.×LONGROTATE-ROT
ALT←DEGREES ARCSIN GQ[;2]
NEG←-S×GQ[;3]
AZ←(360×S≥0)+NEG×DEGREES ARCCOS GQ[; 1 3]÷NORM GQ[; 1 3]
AA←ALT,[1.5] AZ
```

---

## References

Marion, Jerry B., <cite>Classical Dynamics of Particles and Systems</cite>, New York: Academic Press, 1965.

<cite>American Ephemeris and Nautical Almanac</cite>, Explanatory Supplement, U.S. Naval Observatory, 1961.

Hoffleit, Dorrit, <cite>Catalog of Bright Stars</cite>, New Haven: Yale University, 1964.

---

## Appendix

### Tables

The tables in this appendix were prepared by Mr. Per Gjerlov of IBM Denmark, using data from the Yale Catalogue of Bright Stars.

On the first page, values are given for the orbital elements of the nine planets, of the moon, and of the comet Kohoutek. These are the values used to produce the sample charts shown in this report.

Following that, there appear the coordinates of 332 stars. The stars included are roughly the first 300 in visual magnitude, plus a handful of others chosen because they help complete the outline of certain constellations. The table shows the popular name (where there is one), the Bayer designation, and the number in the Yale catalogue. The coordinates are shown as right ascension in hours, minutes, and seconds, and declination, in degrees and minutes, epoch 1 January 2000. The last two columns show the visual magnitude, and the annual parallax in seconds. Where there is a bright double star, only one star is listed.

The stars in Pleiades are here named PLE, although they are commonly referred to the constellation Taurus. To improve visual display, they are shown with positions slightly different from the correct ones.

### Mean orbital elements for the planets (columns 1-7 of `planets`)

```
           SEMIMAJOR     PERIOD   ECCENT'Y   INCLINAT'N   ASCENDING   PERIANGLE     ANOMALY
MERCURY        0.387    0.24085    0.20563     7.004330    48.07347    77.11704    289.6550
VENUS          0.723    0.61521    0.00678     3.394420    76.48402   131.26501    150.2801
EARTH          1        1.00004    0.01672     0            0         102.56835     34.4957
MARS           1.524    1.88089    0.09338     1.849810    49.38973   335.65866    271.1460
JUPITER        5.202   11.86223    0.04794     1.305540   100.21550    14.10850    283.9167
SATURN         9.578   29.45772    0.05759     2.486680   113.49100    94.40310    348.2963
URANUS        19.178   84.01529    0.04808     0.771410    74.00020   168.86530     25.4394
NEPTUNE       29.965  164.78829    0.01119     1.772070   131.54740    59.57130    224.9265
PLUTO         39.543  248.43020    0.24934    17.137130   109.88680   223.14830    335.6904
```

### Mean orbital elements for the planets (columns 8-11 of `planets`)

```
              SECULAR ASCENDING   SECULAR PERIANGLE   DATE (ASC)   DATE (PERI)
MERCURY       0.000 032 444 198   0.000 042 559 243    2443600.5     2443600.5
VENUS         0.000 024 641 163   0.000 038 505 620    2443600.5     2443600.5
EARTH         0.000 000 000 000   0.000 047 000 737    2443600.5     2443600.5
MARS          0.000 021 188 358   0.000 050 392 700    2443600.5     2443600.5
JUPITER       0.000 027 683 282   0.000 044 110 724    2443600.5     2443600.5
SATURN        0.000 023 880 633   0.000 053 617 346    2443600.5     2443600.5
URANUS        0.000 013 689 535   0.000 044 110 724    2443600.5     2443600.5
NEPTUNE       0.000 030 040 924   0.000 018 252 713    2443600.5     2443600.5
PLUTO         0.000 038 026 486   0.000 038 026 486    2443600.5     2443600.5
```

### Orbital elements for the moon (with respect to Earth)

```
    SEMIMAJOR    PERIOD ECCENTRICITY INCLINATION  ASCENDING   PERIANGLE
MOON    1       0.07544      0.05490     5.14342  260.38369   331.80423

       SECULAR ASCENDING   SECULAR PERIANGLE    DATE (ASC)   DATE (PERI)
MOON  ¯0.005 295 392 200   0.011 140 408 030   2414997.831   2414997.831
```

### Orbital elements for the comet Kohoutek

```
          PERIDIST   INCLINATION  ASCENDING  PERIANGLE       PERIDATE
KOHOUTEK     0.142       14.2969    257.7153  295.5891    2442046.463
```

### Bright Stars

```
Popular Name          Bayer Yale   Right Asc.     Decl.     Mag.  Prlx
                             No.   Hr Min Sec   Deg Min           Secs

ALPHERATZ          1  α AND   15    0   8  23    29   5     2.06  .032
MIRACH             2  β AND  337    1   9  44    35  37     2.06  .049
ALMACH             3  γ AND  603    2   3  54    42  19     2.26  .013
                   4  δ AND  165    0  39  20    30  51     3.27  .028
ALTAIR             5  α AQL 7557   19  50  47     8  52     0.77  .198
                   6  β AQL 7602   19  55  19     6  24     3.71  .070
                   7  γ AQL 7525   19  46  16    10  36     2.72  .016
                   8  δ AQL 7377   19  25  30     3   6     3.36  .072
                   9  ζ AQL 7235   19   5  25    13  51     2.99  .045
                  10  η AQL 7570   19  52  28     1   0     3.90  .010
                  11  θ AQL 7710   20  11  18    ¯0 ¯49     3.23  .012
                  12  λ AQL 7236   19   6  15    ¯4 ¯52     3.44  .032
                  13  α AQR 8414   22   5  47    ¯0 ¯19     2.96  .012
                  14  β AQR 8232   21  31  34    ¯5 ¯34     2.91  .006
                  15  δ AQR 8709   22  54  39   ¯15 ¯49     3.27  .038
                  16  β ARA 6461   17  25  18   ¯55 ¯31     2.85  .034
                  17  γ ARA 6462   17  25  24   ¯56 ¯22     3.34  .000
                  18  ζ ARA 6285   16  58  37   ¯55 ¯59     3.13  .044
HAMAL             19  α ARI  617    2   7  10    23  27     2.00  .049
SHERATAN          20  β ARI  553    1  54  38    20  48     2.64  .074
CAPELLA           21  α AUR 1708    5  16  41    45  59     0.08  .073
MENKALINAN        22  β AUR 2088    5  59  32    44  56     1.90  .041
                  23  δ AUR 2077    5  59  32    54  17     3.72  .022
                  24  ε AUR 1605    5   1  58    43  49     2.99  .007
                  25  θ AUR 2095    5  59  43    37  12     2.62  .022
                  26  ι AUR 1577    4  56  60    33   9     2.69  .021
ARCTURUS          27  α BOO 5340   14  15  40    19  10    ¯0.04  .090
                  28  β BOO 5602   15   1  57    40  23     3.50  .037
                  29  γ BOO 5435   14  32   5    38  18     3.03  .025
                  30  δ BOO 5681   15  15  30    33  18     3.47  .030
                  31  ε BOO 5506   14  44  59    27   4     2.70  .016
                  32  ζ BOO 5477   14  41   9    13  43     4.83  .009
                  33  η BOO 5235   13  54  41    18  23     2.68  .108
                  34  ρ BOO 5429   14  31  50    30  22     3.58  .029
                  35  α CAP 7754   20  18   3   ¯12 ¯32     3.57  .034
                  36  β CAP 7776   20  21   1   ¯14 ¯46     3.08  .010
                  37  δ CAP 8322   21  47   2   ¯16  ¯7     2.87  .087
                  38  θ CAP 8075   21   5  57   ¯17 ¯13     4.07  .017
                  39  ω CAP 7980   20  51  49   ¯26 ¯55     4.11  .001
CANOPUS           40  α CAR 2326    6  23  57   ¯52 ¯41    ¯0.72  .028
MIAPLACIDUS       41  β CAR 3685    9  13  12   ¯69 ¯43     1.68  .021
                  42  ε CAR 3307    8  22  31   ¯59 ¯30     1.86  .000
                  43  η CAR 4210   10  45   4   ¯59 ¯41     6.21  .000
                  44  θ CAR 4199   10  42  57   ¯64 ¯23     2.76  .000
                  45  ι CAR 3699    9  17   5   ¯59 ¯16     2.25  .017
                  46  υ CAR 3890    9  47   6   ¯65  ¯4     3.01  .027
                  47  χ CAR 3117    7  56  47   ¯52 ¯58     3.47  .004
                  48  ω CAR 4037   10  13  44   ¯70  ¯2     3.32  .000
                  49    CAR 4050   10  17   5   ¯61 ¯19     3.40  .027
SCHEDIR           50  α CAS  168    0  40  30    56  32     2.23  .016
CAPH              51  β CAS   21    0   9  11    59   8     2.27  .072
                  52  γ CAS  264    0  56  42    60  43     2.47  .016
RUCHBAH           53  δ CAS  403    1  25  49    60  14     2.68  .037
                  54  ε CAS  542    1  54  24    63  40     3.38  .010
RIGIL KENTAURUS   55  α CEN 5459   14  39  36   ¯60 ¯50    ¯0.01  .751
                  56  β CEN 5267   14   3  49   ¯60 ¯22     0.61  .009
                  57  γ CEN 4819   12  41  31   ¯48 ¯57     2.17  .016
                  58  δ CEN 4621   12   8  22   ¯50 ¯43     2.60  .026
                  59  ε CEN 5132   13  39  53   ¯53 ¯27     2.30  .000
                  60  ζ CEN 5231   13  55  32   ¯47 ¯17     2.55  .000
                  61  η CEN 5440   14  35  30   ¯42  ¯9     2.31  .000
                  62  θ CEN 5288   14   6  41   ¯36 ¯22     2.06  .065
                  63  ι CEN 5028   13  20  36   ¯36 ¯42     2.75  .062
                  64  λ CEN 4467   11  35  47   ¯63  ¯1     3.13  .000
                  65  ν CEN 5190   13  49  30   ¯41 ¯41     3.41  .000
ALDERAMIN         66  α CEP 8162   21  18  35    62  35     2.44  .068
                  67  β CEP 8238   21  28  40    70  33     3.23  .014
                  68  γ CEP 8974   23  39  21    77  37     3.21  .064
                  69  ζ CEP 8465   22  10  51    58  12     3.35  .017
                  70  ι CEP 8694   22  49  41    66  12     3.52  .041
MENKAR            71  α CET  911    3   2  17     4   5     2.53  .009
DENEB-KAITOS      72  β CET  188    0  43  35   ¯17 ¯59     2.04  .061
                  73  γ CET  804    2  43  18     3  14     3.47  .052
                  74  δ CET  779    2  39  29     0  19     4.07  .001
                  75  ζ CET  539    1  51  28   ¯10 ¯20     3.73  .031
                  76  η CET  334    1   8  35   ¯10 ¯10     3.45  .041
                  77  θ CET  402    1  24   1    ¯8 ¯11     3.60  .041
                  78  ι CET   74    0  19  26    ¯8 ¯49     3.56  .013
                  79  ο CET  681    2  19  21    ¯2 ¯58     3.04  .024
                  80  τ CET  509    1  44   4   ¯15 ¯56     3.50  .275
SIRIUS            81  α CMA 2491    6  45   9   ¯16 ¯42    ¯1.46  .375
                  82  β CMA 2294    6  22  42   ¯17 ¯57     1.98  .019
                  83  γ CMA 2657    7   3  46   ¯15 ¯38     4.12  .000
                  84  δ CMA 2693    7   8  24   ¯26 ¯23     1.84 ¯.011
ADHARA            85  ε CMA 2618    6  58  38   ¯28 ¯58     1.50  .001
                  86  ζ CMA 2282    6  20  19   ¯30  ¯3     3.02  .004
                  87  η CMA 2827    7  24   6   ¯29 ¯18     2.45  .000
PROCYON           88  α CMI 2943    7  39  18     5  13     0.38  .288
                  89  β CMI 2845    7  27   9     8  17     2.90  .019
                  90  α CNC 3572    8  58  29    11  51     4.25  .024
                  91  β CNC 3249    8  16  31     9  11     3.52  .012
                  92  δ CNC 3461    8  44  41    18   9     3.94  .025
PHACT             93  α COL 1956    5  39  39   ¯34  ¯4     2.64  .001
                  94  β COL 2040    5  50  58   ¯35 ¯46     3.12  .023
ALPHECA           95  α CRB 5793   15  34  41    26  42     2.23  .045
                  96    CRB 5958   15  59  30    25  55     2.00  .000
                  97  α CRU 4730   12  26  36   ¯63  ¯5     1.33  .008
                  98  β CRU 4853   12  47  43   ¯59 ¯41     1.25  .000
                  99  γ CRU 4763   12  31  10   ¯57  ¯6     1.63  .000
                 100  δ CRU 4656   12  15   9   ¯58 ¯44     2.80  .003
                 101  β CRV 4786   12  34  23   ¯23 ¯23     2.65  .034
                 102  γ CRV 4662   12  15  48   ¯17 ¯32     2.59  .000
                 103  δ CRV 4757   12  29  52   ¯16 ¯30     2.95  .024
                 104  ε CRV 4630   12  10   8   ¯22 ¯37     3.00  .027
COR CAROLI       105  α CYG 4914   12  56   0    38  18     5.60  .027
DENEB            106  α CYG 7924   20  41  26    45  16     1.25 ¯.006
ALBIREO          107  β CYG 7417   19  30  43    27  57     3.08  .017
                 108  γ CYG 7796   20  22  14    40  15     2.20  .003
                 109  δ CYG 7528   19  44  58    45   7     2.87  .030
                 110  ε CYG 7949   20  46  13    33  58     2.46  .057
                 111  ζ CYG 8115   21  12  56    30  13     3.20  .027
                 112  η CYG 7615   19  56  18    35   5     3.89  .015
                 113  τ CYG 8130   21  14  48    38   2     3.72  .055
                 114  α DEL 7906   20  39  38    15  54     3.77  .008
                 115  β DEL 7882   20  37  33    14  35     3.63  .028
                 116  γ DEL 7947   20  46  39    16   7     5.14  .026
                 117  ε DEL 7852   20  33  13    11  18     4.03  .025
                 118  α DOR 1465    4  33  60   ¯55  ¯2     3.27  .018
                 119  β DOR 1922    5  33  38   ¯62 ¯29     3.76  .012
THUBAN           120  α DRA 5291   14   4  23    64  22     3.65  .018
                 121  β DRA 6536   17  30  26    52  18     2.79  .013
ETAMIN           122  γ DRA 6705   17  56  36    51  29     2.23  .025
                 123  δ DRA 7310   19  12  33    67  39     3.07  .032
                 124  ε DRA 7582   19  48  10    70  16     3.83  .016
                 125  ζ DRA 6396   17   8  47    65  42     3.17  .023
                 126  η DRA 6132   16  23  60    61  30     2.74  .051
                 127  θ DRA 5986   16   1  53    58  33     4.01  .051
                 128  ι DRA 5744   15  24  56    58  57     3.29  .040
                 129  κ DRA 4787   12  33  29    69  47     3.87  .013
                 130  λ DRA 4434   11  31  24    69  19     3.84  .026
                 131  ν DRA 6554   17  32  11    55  11     4.88  .035
                 132  ζ DRA 6688   17  53  32    56  52     3.75  .035
                 133  ο DRA 7125   18  51  12    59  23     4.66  .006
                 134  χ DRA 6927   18  21   3    72  43     3.57  .120
ACHERNAR         135  α ERI  472    1  37  43   ¯57 ¯14     0.46  .026
                 136  β ERI 1666    5   7  51    ¯5  ¯5     2.79  .050
                 137  γ ERI 1231    3  58   2   ¯13 ¯30     2.95  .010
                 138  δ ERI 1136    3  43  15    ¯9 ¯45     3.54  .109
                 139  ε ERI 1084    3  32  56    ¯9 ¯27     3.73  .303
                 140  η ERI  874    2  56  26    ¯8 ¯53     3.89  .033
ACAMAR           141  θ ERI  897    2  58  16   ¯40 ¯18     3.24  .035
                 142  ο ERI 1325    4  15  16    ¯7 ¯39     4.43  .209
                 143  τ ERI 1003    3  19  31   ¯21 ¯45     3.69 ¯.013
                 144  φ ERI  674    2  16  31   ¯51 ¯30     3.56  .000
CASTOR           145  α GEM 2890    7  34  36    31  53     2.88  .067
POLLUX           146  β GEM 2990    7  45  19    28   1     1.14  .094
                 147  γ GEM 2421    6  37  43    16  23     1.93  .033
                 148  δ GEM 2777    7  20   7    21  58     3.53  .061
                 149  ε GEM 2473    6  43  56    25   7     2.98  .017
                 150  η GEM 2216    6  14  53    22  30     3.28  .014
                 151  λ GEM 2763    7  18   6    16  32     3.58  .047
AL NAIR          152  α GRU 8425   22   8  14   ¯46 ¯57     1.74  .057
                 153  β GRU 8636   22  42  40   ¯46 ¯53     2.10  .008
                 154  γ GRU 8353   21  53  56   ¯37 ¯21     3.01  .013
                 155  α HER 6406   17  14  39    14  23     3.48 ¯.002
                 156  β HER 6148   16  30  13    21  29     2.77  .024
                 157  γ HER 6095   16  21  55    19   9     3.75  .024
                 158  δ HER 6410   17  15   2    24  50     3.14  .044
                 159  ε HER 6324   17   0  17    30  55     3.92  .028
                 160  ζ HER 6212   16  41  17    31  36     2.81  .102
                 161  η HER 6220   16  42  54    38  55     3.53  .034
                 162  η HER 6588   17  39  28    46   0     3.80  .005
                 163  μ HER 6623   17  46  28    27  43     3.42  .108
                 164  π HER 6418   17  15   3    36  48     3.16  .025
                 165  τ HER 6092   16  19  44    46  18     3.89  .030
ALPHARD          166  α HYA 3748    9  27  35    ¯8 ¯39     1.98  .022
                 167  γ HYA 5020   13  18  55   ¯23 ¯10     3.00  .027
                 168  ζ HYA 3547    8  55  24     5  56     3.11  .035
                 169  δ HYA 3665    9  14  22     2  18     3.88  .027
                 170  ν HYA 4232   10  49  38   ¯16 ¯11     3.11  .028
                 171  π HYA 5287   14   6  22   ¯26 ¯40     3.27  .049
                 172  α HYI  591    1  58  46   ¯61 ¯34     2.86  .048
                 173  β HYI   98    0  25  45   ¯77 ¯15     2.80  .153
                 174  γ HYI 1208    3  47  14   ¯74 ¯14     3.24  .005
                 175  α IND 7869   20  37  34   ¯47 ¯17     3.11  .046
REGULUS          176  α LEO 3982   10   8  22    11  58     1.35  .045
DENEBOLA         177  β LEO 4534   11  49   4    14  34     2.14  .082
                 178  γ LEO 4057   10  19  58    19  50     2.61  .022
                 179  δ LEO 4357   11  14   6    20  31     2.56  .048
                 180  ε LEO 3873    9  45  51    23  46     2.98  .010
                 181  ζ LEO 4031   10  16  41    23  25     3.44  .017
                 182  η LEO 3975   10   7  20    16  45     3.52  .003
                 183  θ LEO 4359   11  14  14    15  25     3.34  .026
                 184  μ LEO 3905    9  52  46    26   0     3.88  .025
                 185  ρ LEO 4133   10  32  49     9  18     3.85  .011
ARNEB            186  α LEP 1865    5  32  44   ¯17 ¯49     2.58  .007
                 187  β LEP 1829    5  28  15   ¯20 ¯45     2.84  .020
                 188  ε LEP 1654    5   5  28   ¯22 ¯22     3.19  .011
                 189  μ LEP 1702    5  12  56   ¯16 ¯12     3.31  .023
                 190  α LIB 5530   14  50  41   ¯15 ¯59     5.15  .050
                 191  β LIB 5685   15  17   0    ¯9 ¯22     2.61 ¯.003
                 192  γ LIB 5603   15   4   4   ¯25 ¯16     3.29  .064
                 193  σ LIB 5787   15  35  32   ¯14 ¯47     3.91  .041
                 194  τ LIB 5812   15  38  39   ¯29 ¯46     3.66  .000
                 195  α LUP 5469   14  41  56   ¯47 ¯23     2.30  .000
                 196  β LUP 5571   14  58  32   ¯43  ¯8     2.68  .000
                 197  γ LUP 5776   15  35   8   ¯41 ¯10     2.78  .008
                 198  δ LUP 5695   15  21  22   ¯40 ¯38     3.22  .000
                 199  ε LUP 5708   15  22  41   ¯44 ¯41     3.37  .009
                 200  ζ LUP 5649   15  12  17   ¯52  ¯5     3.41  .043
                 201  α LYR 3705    9  21   3    34  23     3.13  .025
VEGA             202  α LYR 7001   18  36  56    38  47     0.03  .123
                 203  β LYR 7106   18  50   5    33  21     3.45 ¯.002
                 204  γ LYR 7178   18  58  57    32  41     3.24  .021
                 205  δ LYR 7141   18  56  13     4  12     4.62  .030
                 206  ζ LYR 7056   18  44  46    37  36     4.36  .031
                 207  α MUS 4798   12  37  11   ¯69  ¯8     2.69  .000
RASALAGUE        208  α OPH 6556   17  34  56    12  33     2.08  .067
                 209  β OPH 6603   17  43  28     4  34     2.77  .033
                 210  δ OPH 6056   16  14  21    ¯3 ¯41     2.74  .034
                 211  ε OPH 6075   16  18  19    ¯4 ¯41     3.24  .043
                 212  ζ OPH 6175   16  37  10   ¯10 ¯34     2.56  .003
SABIK            213  η OPH 6378   17  10  23   ¯15 ¯43     2.43  .052
                 214  θ OPH 6453   17  22   1   ¯24 ¯59     3.27  .000
                 215  κ OPH 6299   16  57  40     9  22     3.20  .031
                 216  ν OPH 6698   17  59   2    ¯9 ¯46     3.34  .021
BETELGEUX        217  α ORI 2061    5  55  10     7  24     0.50  .005
RIGEL            218  β ORI 1713    5  14  32    ¯8 ¯12     0.12  .013
BELLATRIX        219  γ ORI 1790    5  25   8     6  20     1.64  .029
                 220  δ ORI 1852    5  32   0    ¯0 ¯17     2.23  .014
ALNILAM          221  ε ORI 1903    5  36  13    ¯1 ¯12     1.70 ¯.002
                 222  ζ ORI 1948    5  40  46    ¯1 ¯56     2.05  .024
                 223  ι ORI 1899    5  35  26    ¯5 ¯54     2.77  .025
                 224  κ ORI 2004    5  47  45    ¯9 ¯40     2.06  .015
                 225  λ ORI 1879    5  35   8     9  56     3.54  .007
                 226  α PAV 7790   20  25  39   ¯56 ¯44     1.94  .000
MARKAB           227  α PEG 8781   23   4  46    15  12     2.49  .038
SCHEAT           228  β PEG 8775   23   3  46    28   4     2.42  .022
ALGENIB          229  γ PEG   39    0  13  14    15  11     2.83 ¯.002
ENIF             230  ε PEG 8308   21  44  11     9  52     2.39  .006
                 231  ζ PEG 8634   22  41  28    10  49     3.40  .023
                 232  η PEG 8650   22  43   0    30  13     2.94  .017
                 233  θ PEG 8450   22  10  12     6  11     3.53  .049
                 234  μ PEG 8684   22  50   0    24  36     3.48  .040
MARFAK           235  α PER 1017    3  24  19    49  51     1.79  .016
ALGOL            236  β PER  936    3   8  10    40  57     2.12  .045
                 237  γ PER  915    3   4  48    53  30     2.93  .016
                 238  δ PER 1122    3  42  56    47  47     3.01  .016
                 239  ε PER 1220    3  57  51    40   0     2.89  .009
                 240  ζ PER 1203    3  54   8    31  53     2.85  .010
                 241  τ PER  854    2  54  16    52  45     3.95  .019
                 242  α PHE   99    0  26  17   ¯42 ¯18     2.39  .035
                 243  β PHE  322    1   6   5   ¯46 ¯43     3.31  .021
                 244  γ PER  429    1  28  22   ¯43 ¯19     3.41  .000
                 245    PLE 1165    3  47  29    24   6     2.87  .008
                 246    PLE 1156    3  46  20    23  56     4.18  .000
                 247    PLE 1142    3  44  52    24   6     3.70  .020
                 248    PLE 1149    3  45  50    24  22     3.87  .000
                 249    PLE 1178    3  49  10    24   3     3.63 ¯.026
FOMALHAUT        250  α PSA 8728   22  57  39   ¯29 ¯37     1.16  .149
                 251  α PSC  595    2   2   3     2  45     5.23  .005
                 252  ζ PUP 3165    8   3  35   ¯40  ¯0     2.25  .000
                 253  ν PUP 2451    6  37  46   ¯43 ¯11     3.17  .000
                 254  ξ PUP 3045    7  49  18   ¯24 ¯51     3.34  .003
                 255  π PUP 2773    7  17   9   ¯37  ¯5     2.70  .032
                 256  ρ PUP 3185    8   7  33   ¯24 ¯18     2.81  .035
                 257  σ PUP 2878    7  29  14   ¯43 ¯18     3.25  .020
                 258  τ PUP 2553    6  49  56   ¯50 ¯36     2.93  .000
                 259  α SCO 6134   16  29  24   ¯26 ¯25     0.96  .024
                 260  β SCO 5984   16   5  26   ¯19 ¯48     2.62  .009
                 261  δ SCO 5953   16   0  20   ¯22 ¯37     2.32  .000
                 262  ε SCO 6241   16  50  10   ¯34 ¯17     2.29  .022
                 263  η SCO 6380   17  12   9   ¯43 ¯14     3.33  .063
                 264  θ SCO 6553   17  37  19   ¯42 ¯59     1.87  .027
                 265  ι SCO 6615   17  47  35   ¯40  ¯7     3.03  .019
                 266  κ SCO 6580   17  42  29   ¯39  ¯1     2.41  .000
                 267  λ SCO 6527   17  33  36   ¯37  ¯6     1.63  .000
                 268  µ SCO 6247   16  51  52   ¯38  ¯2     3.08  .000
                 269  υ SCO 6508   17  30  46   ¯37 ¯17     2.69  .000
                 270  π SCO 5944   15  58  51   ¯26  ¯6     2.89  .010
                 271  σ SCO 6084   16  21  11   ¯25 ¯35     2.89  .000
                 272  τ SCO 6165   16  35  53   ¯28 ¯12     2.82  .020
                 273  τ SER 5845   15  41  55    18  27     5.81  .021
                 274  η SER 6869   18  21  19    ¯2 ¯53     3.26  .058
                 275  γ SGR 6746   18   5  48   ¯30 ¯25     2.99  .025
                 276  δ SGR 6859   18  20  60   ¯29 ¯49     2.70  .047
                 277  ε SGR 6879   18  24  10   ¯34 ¯23     1.85  .023
                 278  ζ SGR 7194   19   2  37   ¯29 ¯52     2.60  .025
                 279  η SGR 6832   18  17  38   ¯36 ¯45     3.11  .045
                 280  λ SGR 6913   18  27  58   ¯25 ¯25     2.81  .053
                 281  π SGR 7264   19   9  46   ¯21  ¯1     2.89  .026
                 282  σ SGR 7121   18  55  16   ¯26 ¯17     2.02  .000
                 283  τ SGR 7234   19   6  56   ¯27 ¯40     3.32  .044
                 284  φ SGR 7039   18  45  39   ¯26 ¯59     3.17  .000
                 285  α TAU 1457    4  35  55    16  30     0.85  .048
                 286  β TAU 1791    5  26  18    28  36     1.65  .028
                 287  γ TAU 1346    4  19  48    15  37     3.65  .028
                 288  δ TAU 1373    4  22  56    17  32     3.76  .021
                 289  ε TAU 1409    4  28  37    19  10     3.53  .020
                 290  ζ TAU 1910    5  37  39    21   8     3.00  .008
                 291  θ TAU 1411    4  28  34    15  57     3.84  .038
                 292  τ TAU 1497    4  42  15    22  57     4.28  .017
                 293  α TRA 6217   16  48  40   ¯69  ¯1     1.92  .031
                 294  β TRA 5897   15  55   8   ¯63 ¯25     2.85  .083
                 295  γ TRA 5671   15  18  55   ¯68 ¯40     2.89  .010
                 296  α TRI  544    1  53   5    29  34     3.41  .057
                 297  β TRI  622    2   9  33    34  59     3.00  .022
                 298  γ TRI  664    2  17  19    33  50     4.01  .039
                 299  α TUC 8502   22  18  30   ¯60 ¯15     2.86  .026
                 300  α UMA 4301   11   3  44    61  45     1.79  .038
MERAK            301  β UMA 4295   11   1  50    56  22     2.37  .053
PHECDA           302  γ UMA 4554   11  53  50    53  41     2.44  .028
MEGREZ           303  δ UMA 4660   12  15  26    57   1     3.31  .061
ALIOTH           304  ε UMA 4905   12  54   2    55  57     1.77  .009
MIZAR (+ALCOR)   305  ζ UMA 5054   13  23  56    54  55     2.27  .047
ALKAID           306  η UMA 5191   13  47  32    49  18     1.86  .035
                 307  θ UMA 3775    9  32  51    51  40     3.17  .052
                 308  ι UMA 3569    8  59  12    48   2     3.14  .075
                 309  μ UMA 4069   10  22  20    41  29     3.05  .035
                 310  ν UMA 3888    9  50  59    59   2     3.80  .041
                 311  ο UMA 3323    8  30  16    60  43     3.36  .009
                 312  χ UMA 4518   11  46   3    47  46     3.71  .019
                 313  ψ UMA 4335   11   9  40    44  29     3.01  .000
                 314    UMA 3757    9  31  32    63   3     3.67  .041
POLARIS          315  α UMI  424    2  31  49    89  15     2.02  .007
                 316  β UMI 5563   14  50  42    74   9     2.08  .039
                 317  γ UMI 5735   15  20  44    71  50     3.05  .003
                 318  δ UMI 6789   17  32  13    86  35     4.36  .004
                 319  ε UMI 6322   16  45  58    82   2     4.23  .010
                 320  ζ UMI 5909   15  52  56    17  24     6.36  .000
                 321  η UMI 6116   16  17  30    75  45     4.95  .043
AL SUHAIL        322  γ VEL 3207    8   9  32   ¯47 ¯20     1.78  .017
                 323  δ VEL 3485    8  44  42   ¯54 ¯42     1.96  .051
                 324  κ VEL 3734    9  22   7   ¯55  ¯0     2.50  .013
                 325  λ VEL 3634    9   7  60   ¯43 ¯25     2.21  .022
                 326  μ VEL 4216   10  46  46   ¯49 ¯25     2.69  .022
                 327  ο VEL 3447    8  40  18   ¯52 ¯55     3.62  .000
SPICA            328  α VIR 5056   13  25  12   ¯11  ¯9     0.98  .023
                 329  γ VIR 4825   12  41  40    ¯1 ¯26     3.65  .099
                 330  δ VIR 4910   12  55  36     3  23     3.38  .022
                 331  ε VIR 4932   13   2  11    10  57     2.83  .043
                 332  ζ VIR 5107   13  34  42    ¯0 ¯35     3.37  .044
```
