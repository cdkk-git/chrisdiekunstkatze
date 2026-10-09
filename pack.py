#!/usr/bin/env python3
"""
pack.py - pack the site's images into sprites.snp (SNES-style tiles, 15-bit colour).

    python3 pack.py              build sprites.snp + sprites_manifest.txt, tag <img> tags
    python3 pack.py extra.png    also pack extra images (any number)
    python3 pack.py --no-html    don't touch the .html files
    python3 pack.py --verify     rebuild, then decode the result and report per-sprite error

Sources: inline data: images in index/about/lionsgate/template.html (<img> tags and the
--c1/--c2 cursor variables), favicon.png, apple-touch-icon.png, every *_ref.png in this
folder, and the files in EXTRA below. Needs Python 3 + Pillow. Safe to re-run.

Each <img> gets data-snes="NAME"; snes.js swaps in the decoded sprite at load time and
the original PNG/GIF stays in src= as the fallback for browsers that can't run it.

SNP FORMAT (little-endian)
  0   "SNSP"   u8 version (2)   u8 bits per pixel (4)   u16 entry count N
  8   N x 32-byte entries:
        char[16] name (NUL padded)  u16 width  u16 height
        u16 flags   bit0: colour 0 is opaque (no transparency)
                    bit1: alpha tables present (anti-aliased edges survive)
        u16 palette count P (0 or 1 = single palette)
        u32 data offset (from file start)   u32 data size
  data block per entry, in this order:
        P x 32 B   palettes, 16 x BGR555 each (0bbbbbgggggrrrrr, same as SNES CGRAM);
                   if colour 0 is not opaque, entry 0 of every palette is transparent
        P x 16 B   alpha tables, one 0-255 byte per palette entry   (only if flags bit1)
        T x 1 B    palette index for each tile, row-major           (only if P > 1)
        T x 32 B   tiles, T = ceil(w/8)*ceil(h/8), row-major, SNES 4bpp planar:
                   rows 0-7 as [bp0,bp1] byte pairs (16 B), then rows 0-7 as [bp2,bp3].
                   bit 7 = leftmost pixel. Edge tiles are padded with colour 0.
  Up to 8 palettes per sprite, like SNES sprite/BG palette slots. Plain SNES data has no
  alpha table; it is an addition so heading and cursor edges don't turn jagged.
"""
import re, io, os, sys, base64, hashlib, struct, glob

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index.html", "about.html", "lionsgate.html", "template.html"]
ICONS = ["favicon.png", "apple-touch-icon.png"]
EXTRA = ["ffix_pix_ico_stack.png"]          # reference images that don't end in _ref.png
MAX_PALETTES = 8

IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
SRC_RE = re.compile(r'src="data:image/(?:png|gif);base64,([A-Za-z0-9+/=]+)"')
CUR_RE = re.compile(r'(--c[12]):url\(\s*["\']?data:image/png;base64,([A-Za-z0-9+/=]+)["\']?\s*\)')


# ---------- colour helpers ----------
def to555(r, g, b):
    return (b >> 3) << 10 | (g >> 3) << 5 | (r >> 3)

def from555(v):
    r, g, b = v & 31, (v >> 5) & 31, v >> 10
    return (r << 3 | r >> 2, g << 3 | g >> 2, b << 3 | b >> 2)

def a5(a):                      # 8-bit alpha -> 5-bit
    return 31 if a >= 252 else (a + 4) >> 3

def a8(q):                      # 5-bit alpha -> 8-bit
    return (q << 3) | (q >> 2)


# ---------- palette packing ----------
def group_tiles(tilesets, limit):
    """Greedy: put each tile's colour set into a palette of <= limit colours.
    Returns (assign[tile] -> palette no., palettes as sets) or None if it doesn't fit."""
    order = sorted(range(len(tilesets)), key=lambda t: -len(tilesets[t]))
    pals, assign = [], [0] * len(tilesets)
    for t in order:
        s = tilesets[t]
        if not s:
            continue
        if len(s) > limit:
            return None
        best, grow = None, None
        for i, p in enumerate(pals):
            g = len(s - p)
            if len(p) + g <= limit and (best is None or g < grow):
                best, grow = i, g
        if best is None:
            if len(pals) >= MAX_PALETTES:
                return None
            pals.append(set())
            best = len(pals) - 1
        pals[best] |= s
        assign[t] = best
    return assign, (pals or [set()])

def quantise(pix, w, h, n):
    """Reduce the image's (colour, alpha) pairs to at most n; returns a new pix dict."""
    opaque = len(pix) == w * h and all(q == 31 for _, q in pix.values())
    qi = Image.new("RGB" if opaque else "RGBA", (w, h), (0, 0, 0, 0)[:3 if opaque else 4])
    qp = qi.load()
    for (x, y), (c, q) in pix.items():
        qp[x, y] = from555(c) if opaque else from555(c) + (a8(q),)
    # median cut is better for opaque art; RGBA only supports the octree quantiser
    qq = qi.quantize(colors=n, method=Image.Quantize.MEDIANCUT if opaque else Image.Quantize.FASTOCTREE,
                     dither=Image.Dither.NONE)
    table = qq.getpalette(rawmode="RGB" if opaque else "RGBA")
    step = 3 if opaque else 4
    out = {}
    for (x, y) in pix:
        i = qq.getpixel((x, y))
        q = 31 if opaque else a5(table[i * 4 + 3])
        if q:
            out[(x, y)] = (to555(*table[i * step:i * step + 3]), q)
    return out

def quantise_tiles(pix, w, h, k):
    """Reduce each 8x8 tile on its own to at most k colours (lets many palettes share colours)."""
    qi = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    qp = qi.load()
    for (x, y), (c, q) in pix.items():
        qp[x, y] = from555(c) + (a8(q),)
    out = {}
    for ty in range((h + 7) // 8):
        for tx in range((w + 7) // 8):
            box = (tx * 8, ty * 8, min(w, tx * 8 + 8), min(h, ty * 8 + 8))
            tile = qi.crop(box)
            qq = tile.quantize(colors=k, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
            table = qq.getpalette(rawmode="RGBA")
            for y in range(box[1], box[3]):
                for x in range(box[0], box[2]):
                    if (x, y) in pix:
                        i = qq.getpixel((x - box[0], y - box[1]))
                        q = a5(table[i * 4 + 3])
                        if q:
                            out[(x, y)] = (to555(*table[i * 4:i * 4 + 3]), q)
    return out

def convert(raw):
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    w, h = im.size
    px = im.load()
    src = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            q = a5(a)
            if q:
                src[(x, y)] = (to555(r, g, b), q)
    any_t = len(src) < w * h or any(q < 31 for _, q in src.values())
    partial = any(0 < q < 31 for _, q in src.values())
    first = 1 if any_t else 0
    limit = 16 - first
    tw, th = (w + 7) // 8, (h + 7) // 8

    def tilesets_of(pix):
        ts = [set() for _ in range(tw * th)]
        for (x, y), k in pix.items():
            ts[(y >> 3) * tw + (x >> 3)].add(k)
        return ts

    def assemble(pix, assign, pals):
        """map every source pixel to an index in its tile's palette; returns (idx, mean error)"""
        idx = [[0] * w for _ in range(h)]
        err, count = 0.0, 0
        for (x, y), (c, q) in src.items():
            k = pix.get((x, y), (c, q))
            pl = pals[assign[(y >> 3) * tw + (x >> 3)]]
            if k in pl:
                j = pl.index(k)
            else:
                r, g, b = from555(k[0])
                j = min(range(len(pl)), key=lambda i: (from555(pl[i][0])[0]-r)**2 + (from555(pl[i][0])[1]-g)**2
                        + (from555(pl[i][0])[2]-b)**2 + 2*(a8(pl[i][1])-a8(k[1]))**2)
            idx[y][x] = j + first
            r0, g0, b0 = from555(c)
            r1, g1, b1 = from555(pl[j][0])
            err += ((r0-r1)**2 + (g0-g1)**2 + (b0-b1)**2) ** 0.5
            count += 1
        return idx, err / max(1, count)

    grouped = group_tiles(tilesets_of(src), limit)
    lossy = grouped is None
    if grouped:
        assign, pal_sets = grouped
        pals = [sorted(p) for p in pal_sets]
        idx, merr = assemble(src, assign, pals)
    else:
        # lossy: try several reductions and keep whichever fits and looks closest to the source
        best = None
        tries = [("g", n) for n in (limit * 8, 96, 64, 48, 32, 24, limit)] + [("t", k) for k in (8, 6, 5, 4, 3)]
        for kind, n in tries:
            pix = quantise(src, w, h, n) if kind == "g" else quantise_tiles(src, w, h, n)
            g = group_tiles(tilesets_of(pix), limit)
            if not g:
                continue
            pl = [sorted(p) for p in g[1]]
            ix, e = assemble(pix, g[0], pl)
            if best is None or e < best[0]:
                best = (e, g[0], pl, ix)
        merr, assign, pals, idx = best
    P = len(pals)

    cols, alph = [], []
    for pl in pals:
        cc = [0] * first + [c for c, _ in pl]
        aa = [0] * first + [a8(q) for _, q in pl]
        cols.append(cc + [0] * (16 - len(cc)))
        alph.append(aa + [0] * (16 - len(aa)))
    flags = (0 if any_t else 1) | (2 if partial else 0)
    stats = dict(colours=len(set(src.values())), lossy=lossy, err=merr, pals=P)
    return w, h, flags, cols, alph, assign if P > 1 else None, idx, stats

def tiles_4bpp(w, h, idx):
    out = bytearray()
    for ty in range((h + 7) // 8):
        for tx in range((w + 7) // 8):
            bp = [[0] * 8 for _ in range(4)]
            for r in range(8):
                for c in range(8):
                    x, y = tx * 8 + c, ty * 8 + r
                    v = idx[y][x] if x < w and y < h else 0
                    for p in range(4):
                        bp[p][r] |= ((v >> p) & 1) << (7 - c)
            for r in range(8):
                out += bytes((bp[0][r], bp[1][r]))
            for r in range(8):
                out += bytes((bp[2][r], bp[3][r]))
    return bytes(out)


# ---------- reference decoder (used by --verify, mirrors snes.js) ----------
def decode(blob):
    n = struct.unpack_from("<H", blob, 6)[0]
    res = {}
    for i in range(n):
        name, w, h, flags, P, off, size = struct.unpack_from("<16sHHHHII", blob, 8 + 32 * i)
        name = name.rstrip(b"\0").decode()
        P = max(1, P)
        o = off
        pals = [struct.unpack_from("<16H", blob, o + 32 * k) for k in range(P)]
        o += 32 * P
        alph = None
        if flags & 2:
            alph = [blob[o + 16 * k:o + 16 * k + 16] for k in range(P)]
            o += 16 * P
        tw, th = (w + 7) // 8, (h + 7) // 8
        tmap = None
        if P > 1:
            tmap = blob[o:o + tw * th]
            o += tw * th
        rgba = []
        for y in range(h):
            for x in range(w):
                t = o + ((y >> 3) * tw + (x >> 3)) * 32
                r8, bit = y & 7, 7 - (x & 7)
                v = (((blob[t + r8*2] >> bit) & 1) | (((blob[t + r8*2 + 1] >> bit) & 1) << 1)
                     | (((blob[t + 16 + r8*2] >> bit) & 1) << 2) | (((blob[t + 16 + r8*2 + 1] >> bit) & 1) << 3))
                k = tmap[(y >> 3) * tw + (x >> 3)] if tmap else 0
                rr, gg, bb = from555(pals[k][v])
                a = alph[k][v] if alph else (0 if (v == 0 and not flags & 1) else 255)
                rgba.append((rr, gg, bb, a))
        res[name] = (w, h, rgba)
    return res


def main():
    args = sys.argv[1:]
    do_html = "--no-html" not in args
    verify = "--verify" in args
    extras = [a for a in args if not a.startswith("--")]

    sprites, order = {}, []
    def add(raw, label, name=None):
        key = hashlib.sha1(raw).hexdigest()
        if key in sprites:
            sprites[key]["used"].append(label)
            return sprites[key]["name"]
        nm = name or "s" + key[:7]
        taken = {s["name"] for s in sprites.values()}
        while nm in taken:
            nm = nm[:-1] + "x"
        sprites[key] = dict(name=nm, raw=raw, used=[label])
        order.append(key)
        return nm

    changed = {}
    for p in PAGES:
        path = os.path.join(ROOT, p)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        def tag(m):
            t = m.group(0)
            sm = SRC_RE.search(t)
            if not sm:
                return t
            name = add(base64.b64decode(sm.group(1)), p + " <img>")
            if "data-snes=" in t:
                return t
            return t[:-1].rstrip() + ' data-snes="%s">' % name
        s2 = IMG_RE.sub(tag, s)
        for m in CUR_RE.finditer(s2):
            add(base64.b64decode(m.group(2)), p + " cursor " + m.group(1))
        if s2 != s:
            changed[p] = s2

    files = ICONS + EXTRA + [os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, "*_ref.png")))]
    files += extras
    seen = set()
    for f in files:
        fp = f if os.path.isabs(f) else os.path.join(ROOT, f)
        if fp in seen or not os.path.exists(fp):
            continue
        seen.add(fp)
        stem = os.path.splitext(os.path.basename(fp))[0]
        add(open(fp, "rb").read(), os.path.basename(fp), None if f in ICONS else stem[:16])

    entries, blocks, mani, conv = [], [], [], {}
    for key in order:
        sp = sprites[key]
        w, h, flags, cols, alph, tmap, idx, st = convert(sp["raw"])
        blk = b"".join(struct.pack("<16H", *c) for c in cols)
        if flags & 2:
            blk += b"".join(bytes(a) for a in alph)
        if tmap:
            blk += bytes(tmap)
        blk += tiles_4bpp(w, h, idx)
        entries.append((sp["name"], w, h, flags, st["pals"], len(blk)))
        blocks.append(blk)
        conv[sp["name"]] = (key, st)
        mani.append("%-16s %4dx%-4d %6d B  pal %d  src colours %-5d %s err %5.2f  used: %s" % (
            sp["name"], w, h, len(blk), st["pals"], st["colours"],
            "LOSSY     " if st["lossy"] else "exact     ", st["err"], ", ".join(sorted(set(sp["used"])))))

    off = 8 + 32 * len(entries)
    out = b"SNSP" + struct.pack("<BBH", 2, 4, len(entries))
    table = b""
    for (name, w, h, flags, P, size) in entries:
        table += struct.pack("<16sHHHHII", name.encode(), w, h, flags, P, off, size)
        off += size
    blob = out + table + b"".join(blocks)
    with open(os.path.join(ROOT, "sprites.snp"), "wb") as f:
        f.write(blob)
    with open(os.path.join(ROOT, "sprites_manifest.txt"), "w") as f:
        f.write("SPRITES.SNP MANIFEST - 4bpp SNES planar tiles, BGR555 palettes (format: see pack.py)\n\n")
        f.write("\n".join(mani) + "\n")
    if do_html:
        for p, s in changed.items():
            open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)
    print("\n".join(mani))
    print("\n%d sprites, %d bytes%s" % (len(entries), len(blob), "" if do_html or not changed else "  (html not modified)"))

    if verify:
        dec = decode(blob)
        print("\nVERIFY (decoded .snp vs source image)")
        for key in order:
            nm = sprites[key]["name"]
            w, h, rgba = dec[nm]
            src = Image.open(io.BytesIO(sprites[key]["raw"])).convert("RGBA").load()
            mr = ma = 0
            for y in range(h):
                for x in range(w):
                    r, g, b, a = src[x, y]
                    d = rgba[y * w + x]
                    ma = max(ma, abs(a - d[3]))
                    if a >= 128:
                        mr = max(mr, abs(r - d[0]) + abs(g - d[1]) + abs(b - d[2]))
            print("%-16s %4dx%-4d max RGB diff %3d   max alpha diff %3d" % (nm, w, h, mr, ma))

if __name__ == "__main__":
    main()
