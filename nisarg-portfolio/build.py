#!/usr/bin/env python3
"""Embed the project-cube images and their destination links into index.html.

Everything the four cube faces need lives in projects/:

    projects/<slug>.png|jpg|jpeg|webp   the face image (16:10, 2400x1500)
    projects/links.txt                  one "<slug> = <url>" line per project

Run  python3 build.py  after changing either. The script rewrites a single
<script id="cubedata"> block near the top of index.html; nothing else is
touched, so the phone screenshots and the About video stay where they are.

A face with no image keeps the plain white card. A face with no link stays
inert and keeps showing its [LINK] token — never a dead or invented URL.
"""
import base64, io, mimetypes, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, 'index.html')
DIR = os.path.join(ROOT, 'projects')

# the four faces, in the order the cube turns through them
SLUGS = ['oneguardian-design-system', 'gnc-crazy-deals', 'bellavita-plp',
         'embarouge-homepage']
EXTS = ['.png', '.jpg', '.jpeg', '.webp']  # .webp too — that is what Figma exports

# the "brands I've worked with" marquee in the About section
BRAND_DIR = os.path.join(ROOT, 'brands')
BRAND_EXTS = ['.svg', '.png', '.webp', '.jpg', '.jpeg']
BRANDS = ['bellavita', 'gnc', 'rubans', 'kenaz',
          'embarouge', 'guzz', 'bevzilla', 'thrive']


def words(name):
    """Lowercase word set, with a trailing plural s stripped off each word."""
    return {w[:-1] if len(w) > 3 and w.endswith('s') else w
            for w in re.split(r'[^a-z0-9]+', name.lower()) if w}


def find_image(slug):
    """An exact <slug>.<ext> wins. Otherwise match on words, so a file saved as
    "gnc crazy deal.webp" or "embarouge us homepage.webp" is still found — that
    is how the files actually arrive, and silently ignoring them is worse than
    matching them."""
    for ext in EXTS:
        path = os.path.join(DIR, slug + ext)
        if os.path.exists(path):
            return path
    want, hits = words(slug), []
    for fn in sorted(os.listdir(DIR)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in EXTS or stem in SLUGS:
            continue
        got = words(stem)
        if got and (want <= got or got <= want):
            hits.append(os.path.join(DIR, fn))
    if len(hits) > 1:
        sys.stderr.write('%s: several files could match (%s) — rename one to %s\n'
                         % (slug, ', '.join(os.path.basename(h) for h in hits), slug))
        return None
    return hits[0] if hits else None


# a project can point at a case study and/or the live site
KINDS = {'case': 'study', 'study': 'study', 'live': 'live'}


def read_brands():
    """Embed brands/<slug>.svg|png|... — a missing file keeps the wordmark."""
    out = {}
    for slug in BRANDS:
        for ext in BRAND_EXTS:
            path = os.path.join(BRAND_DIR, slug + ext)
            if not os.path.exists(path):
                continue
            mime = 'image/svg+xml' if ext == '.svg' else (
                mimetypes.guess_type(path)[0] or 'image/png')
            with open(path, 'rb') as fh:
                data = base64.b64encode(fh.read()).decode('ascii')
            out[slug] = 'data:%s;base64,%s' % (mime, data)
            print('  %-26s %s  %.0f KB' % (slug, os.path.basename(path), len(data) / 1024.0))
            break
        else:
            print('  %-26s wordmark (no logo file)' % slug)
    return out


def read_links():
    """Parse projects/links.txt into {slug: {study: url, live: url}}.

    Lines look like  "<slug>.case = <url>"  or  "<slug>.live = <url>".
    A bare "<slug> = <url>" is treated as the case study. Blank lines and
    everything after a # are ignored.
    """
    links, path = {}, os.path.join(DIR, 'links.txt')
    if not os.path.exists(path):
        return links
    for n, raw in enumerate(io.open(path, encoding='utf-8'), 1):
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        if '=' not in line:
            sys.stderr.write('links.txt:%d  skipped, no "=": %s\n' % (n, line))
            continue
        key, url = [part.strip() for part in line.split('=', 1)]
        if not url:
            continue
        slug, _, suffix = key.partition('.')
        kind = KINDS.get(suffix or 'case')
        if kind is None:
            sys.stderr.write('links.txt:%d  unknown link type ".%s" — use '
                             '.case or .live\n' % (n, suffix))
            continue
        if slug not in SLUGS:
            sys.stderr.write('links.txt:%d  unknown project "%s"\n' % (n, slug))
            continue
        # "soon" marks a project that has shipped but has no public site yet;
        # it renders as a disabled button rather than a missing one
        if url.lower() in ('soon', 'coming-soon', 'comingsoon'):
            links.setdefault(slug, {})[kind] = 'soon'
            continue
        # only ever emit an absolute http(s) destination — a relative or
        # javascript: value here would either 404 or be an injection vector
        if not re.match(r'^https?://', url):
            sys.stderr.write('links.txt:%d  needs a full https:// URL: %s\n' % (n, url))
            continue
        links.setdefault(slug, {})[kind] = url
    return links


def js_string(text):
    """JSON-safe, and </script> can't break out of the block it sits in."""
    import json
    return json.dumps(text).replace('</', '<\\/')


def main():
    cubes, links = {}, read_links()
    for slug in SLUGS:
        path = find_image(slug)
        if not path:
            print('  %-26s no image' % slug)
            continue
        mime = mimetypes.guess_type(path)[0] or 'image/png'
        with open(path, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode('ascii')
        cubes[slug] = 'data:%s;base64,%s' % (mime, data)
        print('  %-26s %s  %.2f MB' % (slug, os.path.basename(path),
                                       len(data) / 1048576.0))

    for slug in SLUGS:
        L = links.get(slug, {})
        bits = []
        if L.get('study'):
            bits.append('case: ' + L['study'])
        if L.get('live') == 'soon':
            bits.append('live: coming soon (disabled button)')
        elif L.get('live'):
            bits.append('live: ' + L['live'])
        print('  %-26s %s' % (slug, '  '.join(bits) or '(no link yet)'))

    print('\nbrand marquee')
    brands = read_brands()

    block = ('<script id="cubedata">window.CUBES=%s;window.PROJECT_LINKS=%s;'
             'window.BRANDS=' + '{' + ','.join(
                 '%s:%s' % (js_string(k), js_string(v)) for k, v in brands.items())
             + '};</script>') % (
        '{' + ','.join('%s:%s' % (js_string(k), js_string(v))
                       for k, v in cubes.items()) + '}',
        '{' + ','.join('%s:{%s}' % (js_string(k), ','.join(
            '%s:%s' % (js_string(kk), js_string(vv)) for kk, vv in v.items()))
            for k, v in links.items()) + '}')

    html = io.open(HTML, encoding='utf-8').read()
    existing = re.search(r'<script id="cubedata">.*?</script>', html, re.S)
    if existing:
        html = html[:existing.start()] + block + html[existing.end():]
    else:
        # sits above the page script, which reads both maps on DOM ready
        marker = '<script>window.SHOTS='
        at = html.index(marker)
        html = html[:at] + block + '\n' + html[at:]
    io.open(HTML, 'w', encoding='utf-8').write(html)
    print('\nindex.html is now %.2f MB (16 MB is the artifact ceiling)'
          % (os.path.getsize(HTML) / 1048576.0))


if __name__ == '__main__':
    main()
