# Browser Compatibility Restrictions
### Targets: Internet Explorer 4 (1997), Internet Explorer 8 (2009), PSP NetFront

This document records the combined rule set used to build `ie8-netfront-demo.html`.
When targets disagree, the page follows the *strictest* target for that feature —
in practice IE4 or NetFront, since both predate or fall short of IE8 in most areas.

---

## 1. Document structure

| Rule | Reason |
|---|---|
| Doctype: `HTML 4.01 Transitional` | Baseline all three engines parse predictably; HTML5 doctype triggers inconsistent quirks/standards handling in IE8, and NetFront/IE4 have no HTML5 awareness at all |
| No HTML5 semantic tags (`<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`) | Unrecognized by all three; IE8 needs a JS shim to even style them, and "no required JS" rules that out |
| No `<video>`, `<audio>`, `<canvas>` | Not supported by IE4/IE8/NetFront without plugins or shims |
| Table-based page layout | Only layout method all three render consistently; floats are unreliable in IE4 and inconsistent in NetFront firmware versions |
| Fixed width, 460px | Fits inside the PSP's 480×272 screen; renders as a normal fixed-width column on IE4/IE8 desktop |

## 2. CSS

| Rule | Reason |
|---|---|
| CSS1 properties only (color, background-color, border, padding, margin, font-family, font-size, font-weight, text-align) | IE4 has partial/buggy CSS1 support and no CSS2; going beyond CSS1 risks silent failures in IE4 specifically |
| No CSS2/CSS3 selectors: `:nth-child`, `:not()`, attribute selectors, child (`>`) or sibling (`+`) combinators | Unsupported in IE4; largely unsupported in IE8; inconsistent in NetFront |
| No flexbox, no grid | Did not exist at IE8's release and are unsupported by NetFront and IE4 |
| No `border-radius`, `box-shadow`, gradients | CSS3-only, unsupported by all three |
| No `rgba()` / `hsla()` | Hex colors (`#rrggbb`) only |
| No CSS `opacity`, no IE `alpha` filter hack | IE8's filter hack is IE-only and NetFront/IE4 ignore it outright, so it was dropped rather than relied on |
| No `@font-face` web fonts | System fonts only (Arial/Helvetica/sans-serif fallback) |
| No CSS transitions or animations | CSS3-only |
| Font sizes in `pt`, not `px` or `em` | IE4's px handling is unreliable; pt is the most consistent unit across all three |
| No `position: fixed`; `position: absolute` avoided | Unreliable in IE4, inconsistent in NetFront |
| No centering via `margin: auto` on block content — table alignment used instead for critical layout | `auto` margins are inconsistently honored pre-CSS2-complete engines; table-based centering is the safe fallback |

## 3. JavaScript

| Rule | Reason |
|---|---|
| **Zero JavaScript on the page** | The strictest possible baseline. IE4's JScript is pre-ES1 with no `addEventListener`/`attachEvent`, no DOM standard methods, and no JSON. NetFront's JS support is minimal and inconsistent across PSP firmware, with early versions lacking `XMLHttpRequest` entirely |
| No AJAX / `fetch` | Form uses a plain full-page `GET` submit instead of any async request |
| No `Promise`, array methods (`forEach`/`map`/`filter`), `JSON.parse` | Not present in IE4; inconsistent/absent depending on IE8 mode and NetFront version |

If JavaScript becomes a hard requirement later, it should be layered on top as
progressive enhancement, feature-detected (not browser-sniffed), and the page
must remain fully usable with it absent.

## 4. Images

| Rule | Reason |
|---|---|
| GIF and JPG only | PNG alpha transparency is broken in IE8 (needs AlphaImageLoader filter) and unreliable in NetFront; not a concern worth solving for a page this constrained |
| No SVG | Unsupported by all three targets |
| `border` attribute on `<img>` set explicitly (not relying on CSS reset) | Predictable across all three without depending on a CSS reset stylesheet |

## 5. Forms

| Rule | Reason |
|---|---|
| Standard HTML4 form elements only (`<input type="text">`, `<input type="submit">`) | HTML5 input types (`email`, `date`, `number`, etc.) fall back to plain text anyway on all three targets, so plain text inputs are used directly with no assumption of native validation |
| No client-side validation | Requires JavaScript, which is excluded entirely (see Section 3) |

## 6. Not attempted on this page (noted for completeness)

These are known constraints of the three target browsers that this particular
demo doesn't happen to exercise, but should be kept in mind for future pages:

- **TLS/HTTPS**: XP-era systems (which most IE8 usage implies) may only
  support outdated TLS versions; a server requiring TLS 1.2+ can fail to
  connect before any HTML/CSS/JS is even evaluated. Not a document-level
  concern, but a hosting/server-configuration one.
- **Frames**: still functional in IE4 and a viable historical layout
  technique, but not used here since table layout covers this page's needs.
- **`<font>` tag / `bgcolor` attributes**: valid last-resort fallbacks for
  IE4 if CSS1 support proves too inconsistent in practice; not needed for
  this page's simple styling.

---

## Summary

The page is effectively designed to the standard of a **late-1990s /
early-2000s static HTML site**: HTML 4.01, table layout, CSS1-only styling,
GIF/JPG images, and no JavaScript dependency at all. Enhancements for modern
browsers should be added as strictly optional, feature-detected layers on
top — never required for the page to function.
