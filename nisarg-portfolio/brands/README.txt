BRAND MARQUEE — "Brands I've worked with"
=========================================

The scrolling row of brands sits at the top of the About section. Right now
each brand is set as a plain wordmark. Drop a logo file in here and it replaces
the wordmark automatically — no HTML to touch.

    brands/<slug>.svg      (or .png, .webp, .jpg)

then, from the nisarg-portfolio folder:

    python3 build.py

It prints one line per brand telling you whether it found a logo or fell back
to the wordmark. Mixing is fine — logos for the ones you have, wordmarks for
the rest.


THE SLUGS
---------
  bellavita        Bellavita
  gnc              GNC
  rubans           Rubans
  kenaz            Kenaz
  embarouge        Embarouge
  guzz             Guzz
  bevzilla         Bevzilla
  thrive           Thrive Co.

These are the eight brands named in the OneGuardian design system. BetterAlt
and SleepyCat were dropped when the logos went in — a row mixing logos with
plain text wordmarks looks broken. Add their logo files and their entries in
build.py and index.html to bring them back.

To add or remove a brand, edit the BRANDS list in build.py and the matching
.mq-row items in index.html (there are two identical rows — the marquee clones
more at runtime, but the two in the markup must stay in step).


LOGO FILES
----------
Resolution
          Export at roughly 2x the size it renders, or it will look soft on a
          Retina screen. Current renders at desktop: bellavita 190x27,
          gnc 157x30, embarouge 148x30, kenaz 89x30, rubans 83x30, guzz 81x30,
          thrive 53x30, bevzilla 49x30.
          Three of the current files are below that: guzz (89x33 source),
          kenaz (92x31) and embarouge (178x36) are barely larger than their
          rendered size and will look soft. Replace when you can.

Format    SVG is best — it stays crisp at any size and the files are tiny.
          PNG with transparency works too; export at 2x.
Height    Logos are capped at 34px tall on desktop, 26px on mobile, and 150px
          wide. Anything wider than it is tall works best.
Colour    They render as-is, at 62% opacity, going to full opacity on hover.
          Dark or mid-tone marks read best on the #F7F7F7 background. A logo
          that is white or very pale will disappear — use the dark version.
Padding   Trim the file to the mark itself. Built-in whitespace becomes an
          uneven gap in the row.

Everything is embedded into index.html, so keep the files small. Ten SVGs will
be a few KB; ten large PNGs will not.


HOW THE LOOP WORKS
------------------
The markup ships with two identical rows. On load the marquee measures one row
against the window and clones more until the track is at least a window plus a
row wide, then slides by exactly one row width. That is why it stays seamless
on a 1920 screen even though a row is only ~1845px. Speed is fixed at about
45px a second, so wider rows simply take longer rather than moving faster.

It pauses on hover, and with "reduce motion" turned on it does not scroll at
all — the names just wrap onto as many lines as they need.
