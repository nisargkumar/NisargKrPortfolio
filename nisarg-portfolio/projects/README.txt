PROJECT CUBE — IMAGES AND LINKS
===============================

The "Things I've shipped" cube has four faces. Each one takes an image and a
destination URL, and both come from this folder. You never have to touch the
HTML: drop the files in, edit links.txt, then run

    python3 build.py

from the nisarg-portfolio folder. It rewrites one small block in index.html
and prints what it found.


THE FOUR FACES
--------------
The slug is the filename and the key in links.txt — spelling matters.

  1  oneguardian-design-system   OneGuardian Design System
  2  gnc-crazy-deals             GNC Crazy Deals
  3  bellavita-plp               Bellavita PLP Experience
  4  embarouge-homepage          Embarouge US Homepage


IMAGES
------
File name   <slug>.png   (.jpg, .jpeg and .webp also work)
            A natural name works too — "gnc crazy deal.webp" or "embarouge us
            homepage.webp" are matched to their project on word overlap. An
            exact <slug> filename always wins. If two files could match the
            same project the build says so and skips rather than guessing.
            Your original exports are kept in projects/originals/.
Size        2400 x 1500 px recommended, 1600 x 1000 acceptable
Aspect      16:10 exactly (1.60) — the face is locked to this, so anything
            else gets cropped by object-fit: cover

Why 2400 x 1500: the largest the face ever renders is 1153 x 720 CSS px, on a
1920-wide screen or bigger. 2400 x 1500 is a shade over 2x that, so it stays
sharp on a Retina display. Smaller screens scale down cleanly.

  1920 wide and up   face renders 1153 x 720
  1512 x 950         face renders  957 x 598
  1280 x 800         face renders  730 x 457
   834 x 1112        face renders  693 x 433
   390 x 844         face renders  287 x 180

(These shrank slightly when the CTA buttons were added under the cube — the
row takes 38px of the same vertical budget.)

Composition notes
  - The image IS the face. As soon as one is present the chip, title,
    description and "View project" arrow all disappear — nothing is drawn on
    top of your artwork. So the image has to carry the project name itself.
  - Full bleed, square corners. The face clips its own 18px radius, so keep
    anything important a little away from the corners.
  - The whole face is the click target, and it lifts very slightly on hover.
  - A face with no image falls back to the old white text card, so you can
    add them one at a time without the section looking broken.
  - The project title stays in the page for screen readers even though it is
    not visible.


IF YOUR IMAGE ISN'T 16:10
-------------------------
Don't crop it by hand if there is artwork near the edges — pad it instead, so
nothing is lost. Sample the background colour at the edge, then:

    sips -p <height> <width> --padColor EEEAF8 in.png --out out.png

Width for a given height is height x 1.6. A 1536 x 1024 image becomes
1638 x 1024 with 51px of background added on each side, and no crop at all.
That is how oneguardian-design-system.jpg was made — its edges are flat all
the way round, so the added strips are invisible.

Padding is wrong when artwork bleeds off an edge: the bleed shape ends up
with a flat band beside it and reads as a mistake. Crop instead, from
whichever edge has only background or bleed on it. gnc-crazy-deals.jpg went
the other way for exactly this reason — its pink circle bleeds off the
bottom-left corner, so 64px came off the bottom to land on 1536 x 960, which
is 1.600 exactly. The circle still bleeds, just slightly more.

    sips -c 960 1536 --cropOffset 0 0 in.png --out out.png

(-c is height then width; --cropOffset is top then left.)

Export as JPEG at quality 95, not PNG. On a graphic this dense it is visually
identical and about a fifth of the size (0.31 MB against 1.46 MB), which
matters because everything is embedded into the one HTML file.


LINKS
-----
Edit links.txt. A project can have up to two destinations:

    <slug>.case = https://...     ->  "View case study"  button
    <slug>.live = https://...     ->  "See live website" button

A bare "<slug> = <url>" counts as the case study.

For a project that has shipped but has no public site yet, write:

    <slug>.live = soon

That renders a solid, muted, non-clickable "Live website - coming soon"
button. It is deliberately different from the dashed [LINK] slot: "soon" means
there is nothing to link to yet, [LINK] means the address is simply missing.

The buttons appear in a row under the cube and swap as it turns, always
showing the project currently facing you. Give a project one link and it gets
one button; give it both and it gets two. The face itself is also clickable
and opens the case study, or the live site if there is no case study.

Anything works as a destination: a live site, a Behance or Dribbble case
study, a Notion page, a Drive PDF. Links open in a new tab.

A project that has an image but no links yet shows both CTAs as dashed,
greyed-out slots marked [LINK]. They are deliberately inert — the pair is
visible so you can see the shape of it, but nothing looks like a working
button that goes nowhere. Adding the URL to links.txt turns the slot into a
real button. So partial is fine; fill them in as you get them.


CHECKING YOUR WORK
------------------
build.py prints one line per face for both the image and the link, so you can
see at a glance what is still missing. It also prints the file size — the
artifact ceiling is 16 MB and four 2400 x 1500 JPEGs land well inside it. If
you use PNGs and the total gets close, re-export them as JPEG at quality 85.
