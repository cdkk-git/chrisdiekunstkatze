/* snes.js - decodes sprites.snp (SNES 4bpp planar tiles + BGR555 palettes) onto a canvas
   and swaps the result into every <img data-snes="NAME">. The original PNG/GIF in src=
   stays as the fallback: if anything below is unsupported or fails, nothing changes.
   ES3/ES5 syntax only so old parsers (IE4/IE8/NetFront) skip it harmlessly. */
(function () {
  if (!window.Uint8Array || !window.XMLHttpRequest || !document.getElementsByTagName) return;
  var test = document.createElement("canvas");
  if (!test || !test.getContext || !test.toDataURL) return;

  function parse(buf) {
    var b = new Uint8Array(buf), out = {};
    if (b[0] !== 83 || b[1] !== 78 || b[2] !== 83 || b[3] !== 80) return out; /* "SNSP" */
    var n = b[6] | (b[7] << 8);
    for (var i = 0; i < n; i++) {
      var e = 8 + i * 32, name = "";
      for (var k = 0; k < 16 && b[e + k]; k++) name += String.fromCharCode(b[e + k]);
      var w = b[e + 16] | (b[e + 17] << 8), h = b[e + 18] | (b[e + 19] << 8);
      var opaque = b[e + 20] & 1, ahas = (b[e + 20] >> 1) & 1, np = (b[e + 22] | (b[e + 23] << 8)) || 1;
      var off = (b[e + 24] | (b[e + 25] << 8) | (b[e + 26] << 16)) + b[e + 27] * 16777216;
      out[name] = { w: w, h: h, opaque: opaque, ahas: ahas, np: np, off: off };
    }
    out._b = b;
    return out;
  }

  function dataUrl(pack, s) {
    var b = pack._b, c = document.createElement("canvas");
    c.width = s.w; c.height = s.h;
    var ctx = c.getContext("2d"), img = ctx.createImageData(s.w, s.h), d = img.data;
    var np = s.np, pal = [], i, k;
    for (i = 0; i < 16 * np; i++) {
      var v = b[s.off + i * 2] | (b[s.off + i * 2 + 1] << 8);
      var r = v & 31, g = (v >> 5) & 31, bl = (v >> 10) & 31;
      pal[i] = [(r << 3) | (r >> 2), (g << 3) | (g >> 2), (bl << 3) | (bl >> 2)];
    }
    var aOff = s.off + 32 * np, tw = (s.w + 7) >> 3, th = (s.h + 7) >> 3;
    var mOff = aOff + (s.ahas ? 16 * np : 0);          /* per-tile palette numbers, if np > 1 */
    var t0 = mOff + (np > 1 ? tw * th : 0);
    for (var y = 0; y < s.h; y++) {
      for (var x = 0; x < s.w; x++) {
        var ti = (y >> 3) * tw + (x >> 3), t = t0 + ti * 32, r8 = y & 7, bit = 7 - (x & 7);
        var idx = ((b[t + r8 * 2] >> bit) & 1) |
                  (((b[t + r8 * 2 + 1] >> bit) & 1) << 1) |
                  (((b[t + 16 + r8 * 2] >> bit) & 1) << 2) |
                  (((b[t + 16 + r8 * 2 + 1] >> bit) & 1) << 3);
        k = np > 1 ? b[mOff + ti] : 0;
        var p = (y * s.w + x) * 4, col = pal[k * 16 + idx];
        d[p] = col[0]; d[p + 1] = col[1]; d[p + 2] = col[2];
        d[p + 3] = s.ahas ? b[aOff + k * 16 + idx] : ((idx === 0 && !s.opaque) ? 0 : 255);
      }
    }
    ctx.putImageData(img, 0, 0);
    return c.toDataURL("image/png");
  }

  function apply(buf) {
    var pack = parse(buf), imgs = document.getElementsByTagName("img");
    for (var i = 0; i < imgs.length; i++) {
      var name = imgs[i].getAttribute("data-snes"), s = name && pack[name];
      if (s && !imgs[i].getAttribute("data-snes-done")) {
        try { imgs[i].src = dataUrl(pack, s); imgs[i].setAttribute("data-snes-done", "1"); } catch (e) {}
      }
    }
  }

  try {
    var x = new XMLHttpRequest();
    x.open("GET", "sprites.snp", true);
    x.responseType = "arraybuffer";
    x.onreadystatechange = function () {
      if (x.readyState === 4 && (x.status === 200 || (x.status === 0 && x.response)) && x.response) {
        try { apply(x.response); } catch (e) {}
      }
    };
    x.send(null);
  } catch (e) {}
})();
